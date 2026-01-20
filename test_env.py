#!/usr/bin/env python3
"""
Script simples para testar se o arquivo .env está sendo carregado corretamente
"""
import os
from pathlib import Path

print("=" * 60)
print("🧪 TESTE DE LEITURA DO ARQUIVO .env")
print("=" * 60)

# Verifica se o arquivo existe
env_file = Path('.env')
print(f"\n📁 Verificando arquivo .env...")
print(f"   Caminho: {env_file.absolute()}")
print(f"   Existe: {'✅ SIM' if env_file.exists() else '❌ NÃO'}")

if env_file.exists():
    print(f"   Tamanho: {env_file.stat().st_size} bytes")
    
    # Mostra as primeiras linhas (sem revelar valores)
    print(f"\n📄 Primeiras linhas do arquivo (mascaradas):")
    with open(env_file, 'r') as f:
        for i, line in enumerate(f, 1):
            if i > 10:  # Mostra apenas as primeiras 10 linhas
                break
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key = line.split('=')[0]
                    print(f"   {i}. {key}=***")
                else:
                    print(f"   {i}. {line}")

# Tenta carregar com python-dotenv
print(f"\n🔧 Carregando variáveis com python-dotenv...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("   ✅ python-dotenv instalado e executado")
except ImportError:
    print("   ❌ python-dotenv NÃO instalado")
    print("   Execute: pip install python-dotenv")
    exit(1)

# Verifica se as variáveis foram carregadas
print(f"\n🔍 Verificando variáveis de ambiente:")
env_vars = [
    "BINANCE_API_KEY",
    "BINANCE_SECRET_KEY",
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "SPREADSHEET_ID",
    "GOOGLE_CREDENTIALS_JSON"
]

loaded_count = 0
for var in env_vars:
    value = os.getenv(var)
    if value:
        # Mostra apenas os primeiros caracteres
        preview = f"{value[:10]}..." if len(value) > 10 else "***"
        print(f"   ✅ {var}: {preview}")
        loaded_count += 1
    else:
        print(f"   ❌ {var}: NÃO ENCONTRADO")

print(f"\n" + "=" * 60)
if loaded_count == len(env_vars):
    print("✅ SUCESSO! Todas as variáveis foram carregadas")
    print("=" * 60)
    print("\nVocê pode executar:")
    print("  python check_config.py")
    print("  python main.py")
else:
    print(f"⚠️  Apenas {loaded_count}/{len(env_vars)} variáveis carregadas")
    print("=" * 60)
    print("\nVerifique se o arquivo .env está no formato correto:")
    print("  VARIAVEL=valor")
    print("  (sem espaços antes ou depois do =)")