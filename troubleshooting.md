# 🔧 Guia de Troubleshooting - Crypto Monitor

## Problema: Variáveis de ambiente não estão sendo carregadas

### ❌ Erro mostrado:
```
❌ BINANCE_API_KEY: NÃO CONFIGURADO
❌ BINANCE_SECRET_KEY: NÃO CONFIGURADO
...
```

### ✅ Soluções:

#### 1. Verifique se o python-dotenv está instalado
```bash
pip install python-dotenv
```

#### 2. Teste a leitura do arquivo .env
```bash
python test_env.py
```

Este script vai mostrar:
- Se o arquivo `.env` existe
- Se as variáveis estão sendo carregadas
- Qual é o problema específico

#### 3. Verifique o formato do arquivo .env

**❌ ERRADO:**
```bash
BINANCE_API_KEY = sua_chave_aqui        # Espaços antes/depois do =
BINANCE_API_KEY='sua_chave_aqui'        # Aspas simples
BINANCE_API_KEY="sua_chave_aqui"        # Aspas duplas (exceto para JSON)
```

**✅ CORRETO:**
```bash
BINANCE_API_KEY=sua_chave_aqui
BINANCE_SECRET_KEY=outra_chave_aqui
```

**✅ CORRETO para JSON (Google Credentials):**
```bash
GOOGLE_CREDENTIALS_JSON={"type":"service_account","project_id":"..."}
```

#### 4. Verifique se o arquivo .env está no diretório correto

O arquivo `.env` deve estar na **raiz do projeto**, junto com o `main.py`:

```
Binance_CI-CD_API_Price/
├── .env                  ← Aqui!
├── main.py
├── check_config.py
├── test_env.py
└── requirements.txt
```

Para verificar:
```bash
pwd  # Mostra o diretório atual
ls -la .env  # Lista o arquivo .env
```

#### 5. Verifique permissões do arquivo

```bash
# Linux/Mac
chmod 600 .env

# Windows (PowerShell)
icacls .env /inheritance:r /grant:r "%USERNAME%:F"
```

#### 6. Recrie o arquivo .env do zero

```bash
# Backup do arquivo atual (se existir)
cp .env .env.backup

# Crie um novo arquivo
cat > .env << 'EOF'
BINANCE_API_KEY=cole_sua_chave_aqui
BINANCE_SECRET_KEY=cole_sua_secret_aqui
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=cole_sua_key_aqui
SPREADSHEET_ID=cole_o_id_aqui
GOOGLE_CREDENTIALS_JSON={"cole":"o","json":"completo"}
EOF
```

#### 7. Teste com valores de exemplo

Para testar se o problema é na leitura ou nos valores, use temporariamente:

```bash
cat > .env << 'EOF'
BINANCE_API_KEY=test123
BINANCE_SECRET_KEY=test456
SUPABASE_URL=https://test.supabase.co
SUPABASE_KEY=test789
SPREADSHEET_ID=test_id
GOOGLE_CREDENTIALS_JSON={"type":"test"}
EOF
```

Execute:
```bash
python test_env.py
```

Se funcionar, o problema está nos valores reais.

---

## Problema: Erro no GitHub Actions

### ❌ Erro mostrado:
```
Error: Process completed with exit code 1
TypeError: Client.__init__() got an unexpected keyword argument 'proxy'
```

### ✅ Soluções:

#### 1. Verifique se os Secrets estão configurados

1. Vá em: **Settings** → **Secrets and variables** → **Actions**
2. Verifique se todos os 6 secrets existem:
   - `BINANCE_API_KEY`
   - `BINANCE_SECRET_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `SPREADSHEET_ID`
   - `GOOGLE_CREDENTIALS_JSON`

#### 2. Verifique o conteúdo do GOOGLE_CREDENTIALS_JSON

O JSON deve ser colado **completo**, incluindo as chaves `{}`:

```json
{"type":"service_account","project_id":"crypto-monitor-123","private_key_id":"abc123","private_key":"-----BEGIN PRIVATE KEY-----\nMII...\n-----END PRIVATE KEY-----\n","client_email":"crypto-sheets@crypto-monitor-123.iam.gserviceaccount.com","client_id":"123456789","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/crypto-sheets%40crypto-monitor-123.iam.gserviceaccount.com"}
```

#### 3. Atualize as dependências

Certifique-se de que o `requirements.txt` tem as versões corretas:

```txt
requests==2.31.0
supabase==2.9.1
gspread==6.1.4
google-auth==2.36.0
python-dotenv==1.0.1
httpx==0.27.2
```

#### 4. Teste localmente antes de fazer commit

```bash
# Execute localmente primeiro
python check_config.py
python main.py

# Se funcionar, então faça commit
git add .
git commit -m "test: verificar se funciona"
git push
```

---

## Problema: Erro ao conectar com Supabase

### ❌ Erro mostrado:
```
❌ Erro ao conectar com Supabase: ...
```

### ✅ Soluções:

#### 1. Verifique as credenciais

1. Acesse seu projeto no [Supabase](https://supabase.com/dashboard)
2. Vá em **Settings** → **API**
3. Copie novamente:
   - **Project URL** (deve começar com `https://` e terminar com `.supabase.co`)
   - **anon/public key** (é uma string longa começando com `eyJ...`)

#### 2. Verifique se a tabela existe

Execute no SQL Editor:

```sql
SELECT * FROM crypto_prices LIMIT 1;
```

Se der erro, recrie a tabela com o SQL fornecido no README.

---

## Problema: Erro ao acessar Google Sheets

### ❌ Erro mostrado:
```
❌ Erro ao configurar Google Sheets: ...
```

### ✅ Soluções:

#### 1. Verifique se compartilhou a planilha

1. Abra a planilha no Google Sheets
2. Clique em **Compartilhar**
3. Verifique se o email da service account está na lista
4. A permissão deve ser **Editor**

#### 2. Verifique o SPREADSHEET_ID

O ID está na URL da planilha:
```
https://docs.google.com/spreadsheets/d/1AbC-2DeF_3GhI/edit
                                      ^^^^^^^^^^^^^^^^
                                      Este é o ID
```

#### 3. Verifique as APIs habilitadas

No [Google Cloud Console](https://console.cloud.google.com):
1. Vá em **APIs & Services** → **Enabled APIs & services**
2. Verifique se estão habilitadas:
   - Google Sheets API
   - Google Drive API

---

## Comandos Úteis para Diagnóstico

```bash
# Verificar versões instaladas
pip list | grep -E "(supabase|gspread|google-auth|requests)"

# Reinstalar todas as dependências
pip install -r requirements.txt --force-reinstall

# Testar conexão com a Binance
curl "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

# Ver variáveis de ambiente (Linux/Mac)
printenv | grep -E "(BINANCE|SUPABASE|SPREADSHEET|GOOGLE)"

# Ver variáveis de ambiente (Windows PowerShell)
Get-ChildItem Env: | Where-Object { $_.Name -match "BINANCE|SUPABASE|SPREADSHEET|GOOGLE" }
```

---

## Ainda com problemas?

1. Execute `python test_env.py` e compartilhe o output
2. Execute `python check_config.py` e compartilhe o output
3. Verifique os logs do GitHub Actions em **Actions** → clique na execução com erro
4. Abra uma issue no repositório com:
   - O erro completo
   - Output dos scripts de teste
   - Sistema operacional
   - Versão do Python (`python --version`)