import os
import json
import sys

def check_env_var(name, is_json=False):
    """Verifica se uma variável de ambiente está configurada"""
    value = os.getenv(name)
    
    if not value:
        print(f"❌ {name}: NÃO CONFIGURADO")
        return False
    
    if is_json:
        try:
            json.loads(value)
            print(f"✅ {name}: Configurado (JSON válido)")
        except json.JSONDecodeError:
            print(f"❌ {name}: Configurado mas JSON INVÁLIDO")
            return False
    else:
        # Mostra apenas os primeiros e últimos caracteres
        masked = f"{value[:8]}...{value[-8:]}" if len(value) > 16 else "***"
        print(f"✅ {name}: Configurado ({masked})")
    
    return True

def main():
    print("=" * 60)
    print("🔍 VERIFICAÇÃO DE CONFIGURAÇÃO - CRYPTO MONITOR")
    print("=" * 60)
    print()
    
    all_ok = True
    
    print("📊 Binance API:")
    all_ok &= check_env_var("BINANCE_API_KEY")
    all_ok &= check_env_var("BINANCE_SECRET_KEY")
    print()
    
    print("💾 Supabase:")
    all_ok &= check_env_var("SUPABASE_URL")
    all_ok &= check_env_var("SUPABASE_KEY")
    print()
    
    print("📈 Google Sheets:")
    all_ok &= check_env_var("SPREADSHEET_ID")
    all_ok &= check_env_var("GOOGLE_CREDENTIALS_JSON", is_json=True)
    print()
    
    print("=" * 60)
    if all_ok:
        print("✅ TODAS AS VARIÁVEIS ESTÃO CONFIGURADAS!")
        print("=" * 60)
        print()
        print("Você pode executar: python main.py")
        sys.exit(0)
    else:
        print("❌ ALGUMAS VARIÁVEIS NÃO ESTÃO CONFIGURADAS")
        print("=" * 60)
        print()
        print("Passos para corrigir:")
        print("1. Verifique se o arquivo .env existe")
        print("2. Certifique-se de que todas as variáveis estão preenchidas")
        print("3. No GitHub Actions, verifique os Secrets em Settings → Secrets")
        sys.exit(1)

if __name__ == "__main__":
    main()