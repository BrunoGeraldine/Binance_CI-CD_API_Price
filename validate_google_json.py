#!/usr/bin/env python3
"""
Valida o JSON das credenciais do Google
"""
import os
import json
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

def validate_google_json():
    print("=" * 60)
    print("🔍 VALIDAÇÃO DO GOOGLE_CREDENTIALS_JSON")
    print("=" * 60)
    print()
    
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    
    if not creds_json:
        print("❌ GOOGLE_CREDENTIALS_JSON não está definido")
        return False
    
    print(f"📏 Tamanho: {len(creds_json)} caracteres")
    print(f"🔤 Começa com: {creds_json[:20]}...")
    print(f"🔤 Termina com: ...{creds_json[-20:]}")
    print()
    
    # Tenta fazer parse do JSON
    print("📋 Tentando fazer parse do JSON...")
    try:
        creds_dict = json.loads(creds_json)
        print("✅ JSON parseado com sucesso!")
        print()
    except json.JSONDecodeError as e:
        print(f"❌ ERRO ao fazer parse do JSON:")
        print(f"   {e}")
        print()
        print("💡 Possíveis problemas:")
        print("   1. JSON não está em uma linha única")
        print("   2. Aspas não estão escapadas corretamente")
        print("   3. Caracteres especiais quebrados")
        print()
        return False
    
    # Valida campos obrigatórios
    print("🔍 Validando campos obrigatórios...")
    required_fields = [
        "type",
        "project_id",
        "private_key_id",
        "private_key",
        "client_email",
        "client_id",
        "auth_uri",
        "token_uri",
        "auth_provider_x509_cert_url",
        "client_x509_cert_url"
    ]
    
    all_ok = True
    for field in required_fields:
        if field in creds_dict:
            value = creds_dict[field]
            if field == "private_key":
                print(f"   ✅ {field}: {len(value)} caracteres")
            elif field == "client_email":
                print(f"   ✅ {field}: {value}")
            else:
                preview = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                print(f"   ✅ {field}: {preview}")
        else:
            print(f"   ❌ {field}: FALTANDO")
            all_ok = False
    
    print()
    
    if not all_ok:
        print("❌ Alguns campos obrigatórios estão faltando")
        return False
    
    # Valida tipo
    if creds_dict.get("type") != "service_account":
        print(f"⚠️  type: esperado 'service_account', encontrado '{creds_dict.get('type')}'")
    
    # Valida private_key
    private_key = creds_dict.get("private_key", "")
    if not private_key.startswith("-----BEGIN PRIVATE KEY-----"):
        print("❌ private_key não começa com '-----BEGIN PRIVATE KEY-----'")
        return False
    
    if not private_key.endswith("-----END PRIVATE KEY-----\n"):
        print("⚠️  private_key pode não terminar corretamente")
        print(f"   Termina com: ...{private_key[-50:]}")
    
    # Valida client_email
    client_email = creds_dict.get("client_email", "")
    if not client_email.endswith(".iam.gserviceaccount.com"):
        print(f"⚠️  client_email suspeito: {client_email}")
        print("   Deveria terminar com '.iam.gserviceaccount.com'")
    
    print()
    print("=" * 60)
    print("✅ JSON VÁLIDO E BEM FORMATADO!")
    print("=" * 60)
    print()
    print("📋 Para usar no GitHub Actions:")
    print("   1. Vá em Settings → Secrets → Actions")
    print("   2. Edite GOOGLE_CREDENTIALS_JSON")
    print(f"   3. Cole TODO o JSON (incluindo as chaves)")
    print(f"   4. Certifique-se de que está em UMA LINHA ÚNICA")
    print()
    print(f"📧 Service Account Email:")
    print(f"   {client_email}")
    print()
    print("   Compartilhe sua planilha Google Sheets com este email!")
    print()
    
    return True

if __name__ == "__main__":
    success = validate_google_json()
    sys.exit(0 if success else 1)