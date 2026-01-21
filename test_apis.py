#!/usr/bin/env python3
"""
Testa acesso às APIs de criptomoedas
"""
import requests

def test_binance():
    """Testa API da Binance"""
    print("=" * 60)
    print("🧪 TESTANDO API DA BINANCE")
    print("=" * 60)
    
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        params = {"symbol": "BTCUSDC"}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        print(f"📡 Fazendo requisição para: {url}")
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 451:
            print("❌ ERRO 451: Binance está bloqueada geograficamente")
            print("   Os servidores do GitHub Actions estão em região bloqueada")
            print("   ✅ Solução: Usar API alternativa (CoinGecko)")
            return False
        
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Binance acessível!")
        print(f"💰 BTC/USDC: ${float(data['lastPrice']):,.2f}")
        print(f"📈 Variação 24h: {float(data['priceChangePercent']):.2f}%")
        return True
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro HTTP: {e}")
        print(f"   Status Code: {e.response.status_code}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_coingecko():
    """Testa API do CoinGecko"""
    print("\n" + "=" * 60)
    print("🧪 TESTANDO API DO COINGECKO")
    print("=" * 60)
    
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum,binancecoin,cardano,solana",
            "vs_currencies": "usd",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }
        
        print(f"📡 Fazendo requisição para: {url}")
        response = requests.get(url, params=params, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        response.raise_for_status()
        
        data = response.json()
        
        print(f"✅ CoinGecko acessível!")
        print(f"\n💰 Preços obtidos:")
        
        coin_names = {
            "bitcoin": "BTC",
            "ethereum": "ETH",
            "binancecoin": "BNB",
            "cardano": "ADA",
            "solana": "SOL"
        }
        
        for coin_id, coin_data in data.items():
            name = coin_names.get(coin_id, coin_id)
            price = coin_data.get("usd", 0)
            change = coin_data.get("usd_24h_change", 0)
            print(f"   {name}: ${price:,.2f} ({change:+.2f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_coincap():
    """Testa API do CoinCap (alternativa adicional)"""
    print("\n" + "=" * 60)
    print("🧪 TESTANDO API DO COINCAP")
    print("=" * 60)
    
    try:
        url = "https://api.coincap.io/v2/assets/bitcoin"
        
        print(f"📡 Fazendo requisição para: {url}")
        response = requests.get(url, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        response.raise_for_status()
        
        data = response.json()["data"]
        
        print(f"✅ CoinCap acessível!")
        print(f"💰 BTC: ${float(data['priceUsd']):,.2f}")
        print(f"📈 Variação 24h: {float(data['changePercent24Hr']):.2f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("=" * 60)
    print("🔬 TESTE DE APIS DE CRIPTOMOEDAS")
    print("=" * 60)
    print()
    
    binance_ok = test_binance()
    coingecko_ok = test_coingecko()
    coincap_ok = test_coincap()
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    print(f"Binance: {'✅ Acessível' if binance_ok else '❌ Bloqueada (usar alternativa)'}")
    print(f"CoinGecko: {'✅ Acessível' if coingecko_ok else '❌ Inacessível'}")
    print(f"CoinCap: {'✅ Acessível' if coincap_ok else '❌ Inacessível'}")
    print("=" * 60)
    
    if coingecko_ok or coincap_ok:
        print("\n✅ Pelo menos uma API alternativa está funcionando!")
        print("   O código usará automaticamente a API disponível.")
    else:
        print("\n❌ Nenhuma API está acessível!")
        print("   Verifique sua conexão de internet.")

if __name__ == "__main__":
    main()