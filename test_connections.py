#!/usr/bin/env python3
"""
Script para testar as conexões com Supabase e Google Sheets
"""
import os
import json
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def test_supabase():
    """Testa conexão com Supabase"""
    print("\n" + "=" * 60)
    print("🧪 TESTE DE CONEXÃO - SUPABASE")
    print("=" * 60)
    
    try:
        from supabase import create_client, Client
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Credenciais do Supabase não encontradas")
            return False
        
        print(f"📍 URL: {supabase_url}")
        print(f"🔑 Key: {supabase_key[:20]}...")
        print("\n🔌 Tentando conectar...")
        
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Cliente Supabase criado com sucesso")
        
        # Tenta fazer uma consulta simples
        print("\n📊 Testando consulta na tabela crypto_prices...")
        try:
            result = supabase.table("crypto_prices").select("*").limit(1).execute()
            print(f"✅ Consulta bem-sucedida! Registros encontrados: {len(result.data)}")
            
            if result.data:
                print(f"📝 Último registro: {result.data[0].get('symbol', 'N/A')}")
            else:
                print("ℹ️  Tabela vazia (isso é normal se for a primeira execução)")
            
        except Exception as e:
            print(f"⚠️  Erro na consulta: {e}")
            print("   Isso pode significar que a tabela não existe ainda.")
            return False
        
        # Tenta inserir um registro de teste
        print("\n💾 Testando inserção de dados...")
        try:
            test_data = {
                "symbol": "TEST",
                "price": 99999.99,
                "volume_24h": 1000000.00,
                "price_change_24h": 1.23
            }
            result = supabase.table("crypto_prices").insert(test_data).execute()
            print("✅ Inserção bem-sucedida!")
            
            # Remove o registro de teste
            if result.data:
                test_id = result.data[0]['id']
                supabase.table("crypto_prices").delete().eq('id', test_id).execute()
                print("🧹 Registro de teste removido")
            
        except Exception as e:
            print(f"❌ Erro na inserção: {e}")
            return False
        
        print("\n" + "=" * 60)
        print("✅ SUPABASE: TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao testar Supabase: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_google_sheets():
    """Testa conexão com Google Sheets"""
    print("\n" + "=" * 60)
    print("🧪 TESTE DE CONEXÃO - GOOGLE SHEETS")
    print("=" * 60)
    
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
        spreadsheet_id = os.getenv("SPREADSHEET_ID")
        
        if not creds_json or not spreadsheet_id:
            print("❌ Credenciais do Google não encontradas")
            return False
        
        print(f"📄 Spreadsheet ID: {spreadsheet_id}")
        print(f"🔑 Credentials: JSON com {len(creds_json)} caracteres")
        
        print("\n🔌 Tentando conectar...")
        
        # Parse do JSON
        try:
            creds_dict = json.loads(creds_json)
            print(f"✅ JSON parseado com sucesso")
            print(f"📧 Service Account: {creds_dict.get('client_email', 'N/A')}")
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao fazer parse do JSON: {e}")
            return False
        
        # Cria credenciais
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        print("✅ Credenciais criadas com sucesso")
        
        # Autoriza gspread
        gc = gspread.authorize(credentials)
        print("✅ Gspread autorizado")
        
        # Abre a planilha
        print(f"\n📖 Tentando abrir planilha {spreadsheet_id}...")
        try:
            spreadsheet = gc.open_by_key(spreadsheet_id)
            print(f"✅ Planilha aberta: '{spreadsheet.title}'")
        except gspread.exceptions.SpreadsheetNotFound:
            print("❌ Planilha não encontrada!")
            print("   Verifique se:")
            print("   1. O ID está correto")
            print("   2. A planilha foi compartilhada com o service account")
            return False
        except Exception as e:
            print(f"❌ Erro ao abrir planilha: {e}")
            return False
        
        # Acessa a primeira aba
        sheet = spreadsheet.sheet1
        print(f"✅ Aba acessada: '{sheet.title}'")
        
        # Tenta ler dados
        print(f"\n📊 Lendo dados da planilha...")
        try:
            values = sheet.get_all_values()
            print(f"✅ Leitura bem-sucedida! Linhas encontradas: {len(values)}")
            
            if values:
                print(f"📝 Primeira linha: {values[0][:3]}...")
        except Exception as e:
            print(f"⚠️  Erro na leitura: {e}")
        
        # Tenta escrever dados de teste
        print(f"\n💾 Testando escrita na planilha...")
        try:
            test_range = 'Z1'  # Usa uma célula bem distante para não atrapalhar
            test_value = "TEST"
            sheet.update(test_range, [[test_value]])
            print(f"✅ Escrita bem-sucedida em {test_range}")
            
            # Limpa o teste
            sheet.update(test_range, [[""]])
            print("🧹 Teste removido")
            
        except Exception as e:
            print(f"❌ Erro na escrita: {e}")
            print("   Verifique se o service account tem permissão de Editor")
            return False
        
        print("\n" + "=" * 60)
        print("✅ GOOGLE SHEETS: TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao testar Google Sheets: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🔬 TESTE DE CONEXÕES - CRYPTO MONITOR")
    print("=" * 60)
    
    supabase_ok = test_supabase()
    sheets_ok = test_google_sheets()
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    print(f"Supabase: {'✅ OK' if supabase_ok else '❌ FALHOU'}")
    print(f"Google Sheets: {'✅ OK' if sheets_ok else '❌ FALHOU'}")
    print("=" * 60)
    
    if supabase_ok and sheets_ok:
        print("\n🎉 TODOS OS SISTEMAS OPERACIONAIS!")
        print("Você pode executar: python main.py")
        return 0
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM")
        print("Corrija os problemas acima antes de executar o main.py")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())