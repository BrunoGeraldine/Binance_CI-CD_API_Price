# ============================================================
# CRYPTO MONITOR - ENVIRONMENT VARIABLES
# ============================================================
# Copy this file to .env and fill in with your values
# IMPORTANT: Do not add spaces before or after the =
# ============================================================

# ------------------------------------------------------------
# BINANCE API
# ------------------------------------------------------------
# Get from: https://www.binance.com/en/my/settings/api-management
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here

# ------------------------------------------------------------
# SUPABASE
# ------------------------------------------------------------
# Get from: https://supabase.com/dashboard/project/_/settings/api
# Project URL (format: https://xxxxx.supabase.co)
SUPABASE_URL=https://xxxxx.supabase.co
# Project API Key (anon/public)
SUPABASE_KEY=your_supabase_key_here

# ------------------------------------------------------------
# GOOGLE SHEETS
# ------------------------------------------------------------
# Spreadsheet ID (extract from URL)
# URL: https://docs.google.com/spreadsheets/d/[ID_HERE]/edit
SPREADSHEET_ID=your_spreadsheet_id

# Complete JSON from service account (paste entire content in one line)
# Format: {"type":"service_account","project_id":"...","private_key_id":"...",...}
GOOGLE_CREDENTIALS_JSON={"type":"service_account","project_id":"your-project","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"...@....iam.gserviceaccount.com","client_id":"...","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/..."}

# ============================================================
# NOTES:
# - Do not share this file
# - Do not commit this file to Git
# - Use the .env.example file as reference
# ============================================================