# 🔑 Guia para Recriar os Secrets do GitHub Actions

## ⚠️ Problema Identificado

O código funciona **perfeitamente** localmente, mas **falha** no GitHub Actions. Isso indica que o problema está nos **Secrets** do GitHub.

## 📋 Checklist de Verificação

Antes de recriar, verifique:

- [ ] O código funciona localmente (`python main.py`)
- [ ] Todas as variáveis estão no arquivo `.env`
- [ ] O arquivo `.env` não tem espaços antes/depois do `=`
- [ ] O JSON do Google está em uma linha única
- [ ] A planilha foi compartilhada com o service account

## 🔧 Passo a Passo para Recriar os Secrets

### 1. Valide suas credenciais localmente

```bash
# Execute estes scripts para garantir que tudo está OK
python validate_google_json.py
python test_connections.py
python main.py
```

Se TODOS passarem, suas credenciais locais estão corretas.

### 2. Exporte os valores do .env

```bash
# No terminal, no diretório do projeto
cat .env
```

Copie cada valor. Você vai precisar deles.

### 3. Acesse os Secrets do GitHub

1. Vá no seu repositório no GitHub
2. Clique em **Settings** (⚙️)
3. No menu lateral, clique em **Secrets and variables** → **Actions**
4. Você verá a lista de secrets

### 4. Delete TODOS os secrets antigos

Para cada secret:
1. Clique no secret
2. Clique em **Remove secret**
3. Confirme

Delete na seguinte ordem:
- BINANCE_API_KEY
- BINANCE_SECRET_KEY
- SUPABASE_URL
- SUPABASE_KEY
- SPREADSHEET_ID
- GOOGLE_CREDENTIALS_JSON

### 5. Recrie os secrets (na ordem)

#### 5.1 BINANCE_API_KEY

1. Clique em **New repository secret**
2. Name: `BINANCE_API_KEY`
3. Secret: Cole o valor do seu `.env` (só o valor, sem aspas)
4. Clique em **Add secret**

**Formato correto:**
```
WMSt5PUw2AblahblahblahCbXUqugc
```

**❌ ERRADO:**
```
BINANCE_API_KEY=WMSt5PUw2A...
"WMSt5PUw2A..."
'WMSt5PUw2A...'
```

#### 5.2 BINANCE_SECRET_KEY

1. **New repository secret**
2. Name: `BINANCE_SECRET_KEY`
3. Secret: Cole o valor do `.env`
4. **Add secret**

#### 5.3 SUPABASE_URL

1. **New repository secret**
2. Name: `SUPABASE_URL`
3. Secret: Cole a URL completa (deve começar com `https://` e terminar com `.supabase.co`)
4. **Add secret**

**Exemplo:**
```
https://qsnkdjfhskjfh.supabase.co
```

#### 5.4 SUPABASE_KEY

1. **New repository secret**
2. Name: `SUPABASE_KEY`
3. Secret: Cole a chave **anon/public** (deve começar com `eyJ`)
4. **Add secret**

**⚠️ IMPORTANTE:** Use a chave **anon/public**, NÃO a service_role!

No Supabase:
- Settings → API → Project API keys → **anon/public** ✅
- Settings → API → Project API keys → ~~service_role~~ ❌

#### 5.5 SPREADSHEET_ID

1. **New repository secret**
2. Name: `SPREADSHEET_ID`
3. Secret: Cole apenas o ID (da URL da planilha)
4. **Add secret**

**Como obter:**
```
URL: https://docs.google.com/spreadsheets/d/1BgEEZObNjblahblahUhutvtyw/edit
                                              ^^^^^^^^^^^^^^^^^^^^
                                              Cole apenas esta parte
```

#### 5.6 GOOGLE_CREDENTIALS_JSON (CRÍTICO!)

Este é o mais complicado e onde geralmente está o erro.

**Método 1: Copiar do .env (Recomendado)**

1. Abra o arquivo `.env` no seu editor
2. Localize a linha `GOOGLE_CREDENTIALS_JSON=`
3. Copie TUDO que está depois do `=`, incluindo as chaves `{}`
4. Cole no GitHub Secret

**Método 2: Copiar do arquivo JSON original**

1. Abra o arquivo `.json` baixado do Google Cloud
2. Copie TODO o conteúdo
3. **IMPORTANTE:** Remova TODAS as quebras de linha
4. Deve ficar em UMA ÚNICA LINHA

**Exemplo correto (tudo em uma linha):**
```json
{"type":"service_account","project_id":"crypto-monitor-123456","private_key_id":"abc123def456","private_key":"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0B...\n-----END PRIVATE KEY-----\n","client_email":"crypto-sheets@crypto-monitor-123456.iam.gserviceaccount.com","client_id":"123456789","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/crypto-sheets%40crypto-monitor-123456.iam.gserviceaccount.com"}
```

**❌ ERRADO (com quebras de linha):**
```json
{
  "type": "service_account",
  "project_id": "crypto-monitor-123456",
  ...
}
```

**Como converter de várias linhas para uma:**

```bash
# Linux/Mac
cat google-credentials.json | jq -c . | pbcopy

# Ou manualmente no editor:
# 1. Selecione tudo
# 2. Procure e substitua: \n por nada (vazio)
# 3. Certifique-se de que não há espaços extras
```

### 6. Valide o JSON antes de adicionar

```bash
# Copie o JSON para um arquivo temporário
echo 'COLE_O_JSON_AQUI' > /tmp/test.json

# Valide
python3 -c "import json; print('✅ JSON válido' if json.load(open('/tmp/test.json')) else '❌ JSON inválido')"

# Limpe
rm /tmp/test.json
```

### 7. Verifique os Secrets criados

Após criar todos, você deve ver:

```
✅ BINANCE_API_KEY
✅ BINANCE_SECRET_KEY
✅ SUPABASE_URL
✅ SUPABASE_KEY
✅ SPREADSHEET_ID
✅ GOOGLE_CREDENTIALS_JSON
```

### 8. Teste com o Workflow de Debug

1. Vá em **Actions**
2. Selecione **Crypto Monitor (Debug Mode)**
3. Clique em **Run workflow**
4. Selecione `main`
5. **Run workflow**

Este workflow vai mostrar:
- ✅ Tamanho de cada secret
- ✅ Se os formatos estão corretos
- ✅ Se consegue conectar em cada serviço
- ✅ Logs detalhados de cada etapa

### 9. Analise os Logs

Vá para a execução e veja os logs. Procure por:

**Se der erro no Supabase:**
```
❌ Erro ao conectar com Supabase: ...
```
→ Problema: SUPABASE_URL ou SUPABASE_KEY incorretos

**Se der erro no Google Sheets:**
```
❌ Erro ao configurar Google Sheets: ...
```
→ Problema: GOOGLE_CREDENTIALS_JSON ou SPREADSHEET_ID incorretos

**Se o JSON estiver quebrado:**
```
❌ Erro ao decodificar JSON do Google: ...
```
→ Problema: JSON com quebras de linha ou formato incorreto

## 🎯 Checklist Final

Depois de recriar todos os secrets:

- [ ] Execute o workflow de debug
- [ ] Verifique se todos os checks passaram (✅)
- [ ] Verifique se o Supabase foi atualizado
- [ ] Verifique se o Google Sheets foi atualizado
- [ ] Se tudo estiver OK, o workflow normal funcionará

## 🆘 Ainda não funciona?

Se mesmo depois de recriar os secrets não funcionar:

1. **Compare os valores:**
   ```bash
   # Local (funciona)
   cat .env
   
   # GitHub (compare com os secrets)
   ```

2. **Verifique caracter por caracter:**
   - Não pode ter espaços extras
   - Não pode ter aspas
   - Não pode ter quebras de linha (exceto no private_key do JSON)

3. **Teste o JSON separadamente:**
   ```bash
   python validate_google_json.py
   ```

4. **Verifique a planilha:**
   - Está compartilhada com o service account?
   - Tem permissão de Editor?
   - O ID está correto?

## 💡 Dica Pro

Para garantir que o JSON está correto, use este comando para gerar uma versão "minificada":

```bash
# Pega o JSON do .env e minifica
grep GOOGLE_CREDENTIALS_JSON .env | cut -d'=' -f2- | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin)))"
```

Cole o resultado diretamente no GitHub Secret.