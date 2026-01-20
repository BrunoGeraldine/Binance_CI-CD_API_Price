# ============================================================
# CRYPTO MONITOR - VARIÁVEIS DE AMBIENTE
# ============================================================
# Copie este arquivo para .env e preencha com seus valores
# IMPORTANTE: Não adicione espaços antes ou depois do =
# ============================================================

# ------------------------------------------------------------
# BINANCE API
# ------------------------------------------------------------
# Obtenha em: https://www.binance.com/en/my/settings/api-management
BINANCE_API_KEY=sua_api_key_aqui
BINANCE_SECRET_KEY=sua_secret_key_aqui

# ------------------------------------------------------------
# SUPABASE
# ------------------------------------------------------------
# Obtenha em: https://supabase.com/dashboard/project/_/settings/api
# Project URL (formato: https://xxxxx.supabase.co)
SUPABASE_URL=https://xxxxx.supabase.co
# Project API Key (anon/public)
SUPABASE_KEY=sua_supabase_key_aqui

# ------------------------------------------------------------
# GOOGLE SHEETS
# ------------------------------------------------------------
# ID da planilha (extraia da URL)
# URL: https://docs.google.com/spreadsheets/d/[ID_AQUI]/edit
SPREADSHEET_ID=id_da_sua_planilha

# JSON completo da service account (cole todo o conteúdo em uma linha)
# Formato: {"type":"service_account","project_id":"...","private_key_id":"...",...}
GOOGLE_CREDENTIALS_JSON={"type":"service_account","project_id":"seu-projeto","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"...@....iam.gserviceaccount.com","client_id":"...","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/..."}

# ============================================================
# NOTAS:
# - Não compartilhe este arquivo
# - Não faça commit deste arquivo no Git
# - Use o arquivo .env.example como referência
# ============================================================