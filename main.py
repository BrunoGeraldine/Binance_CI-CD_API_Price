import os
import json
from datetime import datetime
from typing import List, Dict
import requests
from supabase import create_client, Client
import gspread
from google.oauth2.service_account import Credentials
import time

# Carrega variáveis de ambiente do arquivo .env (para testes locais)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # No GitHub Actions não precisa do dotenv

# Configurações
BINANCE_API_URL = "https://api.binance.com/api/v3"
SYMBOLS = ["BTCUSDC", "ETHUSDC", "BNBUSDC", "XRPUSDC", "SOLUSDC", "LINKUSDC"]

class CryptoMonitor:
    def __init__(self):
        # Binance
        self.binance_api_key = os.getenv("BINANCE_API_KEY")
        self.binance_secret = os.getenv("BINANCE_SECRET_KEY")
        
        # Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados")
        
        try:
            self.supabase: Client = create_client(supabase_url, supabase_key)
            print("✅ Conectado ao Supabase")
        except Exception as e:
            print(f"❌ Erro ao conectar com Supabase: {e}")
            raise
        
        # Google Sheets
        self.setup_google_sheets()
    
    def setup_google_sheets(self):
        """Configura conexão com Google Sheets"""
        try:
            creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
            
            if not creds_json:
                raise ValueError("GOOGLE_CREDENTIALS_JSON não configurado")
            
            creds_dict = json.loads(creds_json)
            
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            credentials = Credentials.from_service_account_info(
                creds_dict, 
                scopes=scopes
            )
            
            self.gc = gspread.authorize(credentials)
            spreadsheet_id = os.getenv("SPREADSHEET_ID")
            
            if not spreadsheet_id:
                raise ValueError("SPREADSHEET_ID não configurado")
            
            self.sheet = self.gc.open_by_key(spreadsheet_id).sheet1
            print("✅ Conectado ao Google Sheets")
            
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao decodificar JSON do Google: {e}")
            raise
        except Exception as e:
            print(f"❌ Erro ao configurar Google Sheets: {e}")
            raise
    
    def _get_all_prices_from_coingecko(self) -> Dict[str, Dict]:
        """Obtém todos os preços do CoinGecko em uma única requisição (evita rate limiting)"""
        try:
            # Mapeia símbolos da Binance para IDs do CoinGecko
            symbol_map = {
                "BTCUSDC": "bitcoin",
                "ETHUSDC": "ethereum",
                "BNBUSDC": "binancecoin",
                "XRPUSDC": "ripple",
                "SOLUSDC": "solana",
                "LINKUSDC": "chainlink"
            }
            
            # Junta todos os IDs em uma única string separada por vírgula
            all_ids = ",".join(symbol_map.values())
            
            # Usa CoinGecko API (pública, sem necessidade de chave)
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": all_ids,
                "vs_currencies": "usd",
                "include_24hr_vol": "true",
                "include_24hr_change": "true"
            }
            
            # Retry com backoff exponencial para lidar com rate limiting
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.get(url, params=params, timeout=15)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Converte os dados para o formato esperado
                    result = {}
                    for symbol, coin_id in symbol_map.items():
                        if coin_id in data:
                            coin_data = data[coin_id]
                            result[symbol] = {
                                "symbol": symbol,
                                "price": float(coin_data["usd"]),
                                "volume_24h": float(coin_data.get("usd_24h_vol", 0)),
                                "price_change_24h": float(coin_data.get("usd_24h_change", 0)),
                                "timestamp": datetime.now().isoformat(),
                                "source": "CoinGecko"
                            }
                            print(f"  ✓ {symbol}: Obtido de CoinGecko")
                    
                    return result
                    
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429 and attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * 2  # 2s, 4s, 8s
                        print(f"  ⏳ Rate limit atingido, aguardando {wait_time}s antes de tentar novamente...")
                        time.sleep(wait_time)
                    else:
                        raise
            
        except Exception as e:
            print(f"  ✗ Erro ao obter preços do CoinGecko: {e}")
        
        return {}
    
    def get_binance_prices(self) -> List[Dict]:
        """Obtém preços da Binance, usando CoinGecko como fallback"""
        prices_data = []
        failed_symbols = []
        
        # Headers para evitar bloqueio
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        # Primeiro tenta obter de cada símbolo da Binance
        for symbol in SYMBOLS:
            try:
                # Usa endpoint público sem autenticação
                ticker_url = f"{BINANCE_API_URL}/ticker/24hr"
                params = {"symbol": symbol}
                
                response = requests.get(
                    ticker_url, 
                    params=params,
                    headers=headers,
                    timeout=10
                )
                
                # Se der erro 451 (bloqueio geográfico), marca para buscar no CoinGecko
                if response.status_code == 451:
                    print(f"⚠️  {symbol}: Bloqueado geograficamente (erro 451)")
                    failed_symbols.append(symbol)
                    continue
                
                response.raise_for_status()
                data = response.json()
                
                prices_data.append({
                    "symbol": symbol,
                    "price": float(data["lastPrice"]),
                    "volume_24h": float(data["volume"]),
                    "price_change_24h": float(data["priceChangePercent"]),
                    "timestamp": datetime.now().isoformat(),
                    "source": "Binance"
                })
                print(f"  ✓ {symbol}: Obtido da Binance")
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 451:
                    print(f"⚠️  {symbol}: Bloqueado geograficamente (erro 451)")
                    failed_symbols.append(symbol)
                else:
                    print(f"  ✗ Erro HTTP ao obter {symbol}: {e}")
                    failed_symbols.append(symbol)
            except Exception as e:
                print(f"  ✗ Erro ao obter preço de {symbol}: {e}")
                failed_symbols.append(symbol)
        
        # Se houver símbolos que falharam, busca todos de uma vez no CoinGecko
        if failed_symbols:
            print(f"\n🔄 Buscando {len(failed_symbols)} criptomoedas no CoinGecko (API alternativa)...")
            coingecko_data = self._get_all_prices_from_coingecko()
            
            # Adiciona os dados do CoinGecko para os símbolos que falharam
            for symbol in failed_symbols:
                if symbol in coingecko_data:
                    prices_data.append(coingecko_data[symbol])
                else:
                    print(f"  ✗ Não foi possível obter preço de {symbol}")
        
        return prices_data
    
    def save_to_supabase(self, prices_data: List[Dict]):
        """Salva dados no Supabase"""
        if not prices_data:
            print("⚠️  Nenhum dado para salvar no Supabase")
            return
        
        try:
            saved_count = 0
            for data in prices_data:
                try:
                    result = self.supabase.table("crypto_prices").insert(data).execute()
                    saved_count += 1
                    print(f"  ✓ {data['symbol']}: ${data['price']:.2f} (fonte: {data['source']})")
                except Exception as e:
                    print(f"  ✗ Erro ao salvar {data['symbol']}: {e}")
            
            print(f"✅ {saved_count}/{len(prices_data)} registros salvos no Supabase")
        except Exception as e:
            print(f"❌ Erro geral ao salvar no Supabase: {e}")
            import traceback
            traceback.print_exc()
    
    def update_google_sheets(self, prices_data: List[Dict]):
        """Atualiza Google Sheets com coluna Source"""
        if not prices_data:
            print("⚠️  Nenhum dado para atualizar no Google Sheets")
            return
        
        try:
            print(f"📝 Preparando dados para {len(prices_data)} criptomoedas...")
            
            # Cabeçalho - INCLUINDO A COLUNA SOURCE
            headers = [
                "Criptomoeda", 
                "Preço (USDC)", 
                "Variação 24h (%)", 
                "Volume 24h",
                "Source",  # Nova coluna
                "Última Atualização"
            ]
            
            # Dados
            rows = [headers]
            for data in prices_data:
                rows.append([
                    data["symbol"].replace("USDC", ""),
                    f"${data['price']:,.2f}",
                    f"{data['price_change_24h']:.2f}%",
                    f"${data['volume_24h']:,.0f}",
                    data["source"],  # Fonte dos dados (Binance ou CoinGecko)
                    datetime.fromisoformat(data["timestamp"]).strftime("%d/%m/%Y %H:%M:%S")
                ])
            
            print(f"📤 Enviando {len(rows)} linhas para Google Sheets...")
            
            # Limpa e atualiza a planilha
            self.sheet.clear()
            self.sheet.update(range_name='A1', values=rows)
            
            print(f"🎨 Aplicando formatação...")
            
            # Formata cabeçalho
            self.sheet.format('A1:F1', {
                "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2},
                "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
            })
            
            print("✅ Google Sheets atualizado com sucesso")
            
        except Exception as e:
            print(f"❌ Erro ao atualizar Google Sheets: {e}")
            import traceback
            traceback.print_exc()
    
    def run(self):
        """Executa o processo completo"""
        print("=" * 60)
        print("🚀 CRYPTO MONITOR - Iniciando coleta de dados...")
        print("=" * 60)
        print()
        
        # 1. Obtém preços
        print("1️⃣  Coletando preços da Binance...")
        prices_data = self.get_binance_prices()
        
        if not prices_data:
            print("❌ Nenhum dado coletado. Encerrando.")
            return
        
        print(f"\n✅ Obtidos {len(prices_data)}/{len(SYMBOLS)} preços com sucesso")
        print()
        
        # Mostra resumo dos dados coletados
        print("📊 Resumo dos dados coletados:")
        for data in prices_data:
            source_icon = "🟢" if data['source'] == "Binance" else "🔵"
            print(f"  {source_icon} {data['symbol']}: ${data['price']:,.2f} ({data['price_change_24h']:+.2f}%) - {data['source']}")
        print()
        
        # 2. Salva no Supabase
        print("2️⃣  Salvando no Supabase...")
        self.save_to_supabase(prices_data)
        print()
        
        # 3. Atualiza Google Sheets
        print("3️⃣  Atualizando Google Sheets...")
        self.update_google_sheets(prices_data)
        print()
        
        print("=" * 60)
        print("✨ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("=" * 60)

if __name__ == "__main__":
    monitor = CryptoMonitor()
    monitor.run()