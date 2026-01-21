# 🔑 Guide to Recreating GitHub Actions Secrets

## ⚠️ Problem Identified

The code works **perfectly** locally, but **fails** on GitHub Actions. This indicates that the problem is in the GitHub **Secrets**.

## 📋 Verification Checklist

Before recreating, verify:

- [ ] The code works locally (`python main.py`)
- [ ] All variables are in the `.env` file
- [ ] The `.env` file has no spaces before/after the `=`
- [ ] The Google JSON is on a single line
- [ ] The spreadsheet was shared with the service account

## 🔧 Step-by-Step to Recreate Secrets

### 1. Validate your credentials locally

```bash
# Run these scripts to make sure everything is OK
python validate_google_json.py
python test_connections.py
python main.py
```

If ALL pass, your local credentials are correct.

### 2. Export the .env values

```bash
# In the terminal, in the project directory
cat .env
```

Copy each value. You will need them.

### 3. Access GitHub Secrets

1. Go to your repository on GitHub
2. Click **Settings** (⚙️)
3. In the left menu, click **Secrets and variables** → **Actions**
4. You will see the list of secrets

### 4. Delete ALL old secrets

For each secret:
1. Click on the secret
2. Click **Remove secret**
3. Confirm

Delete in the following order:
- BINANCE_API_KEY
- BINANCE_SECRET_KEY
- SUPABASE_URL
- SUPABASE_KEY
- SPREADSHEET_ID
- GOOGLE_CREDENTIALS_JSON

### 5. Recreate the secrets (in order)

#### 5.1 BINANCE_API_KEY

1. Click **New repository secret**
2. Name: `BINANCE_API_KEY`
3. Secret: Paste the value from your `.env` (just the value, without quotes)
4. Click **Add secret**

**Correct format:**
```
WMSt5PUw2AblahblahblahCbXUqugc
```

**❌ WRONG:**
```
BINANCE_API_KEY=WMSt5PUw2A...
"WMSt5PUw2A..."
'WMSt5PUw2A...'
```

#### 5.2 BINANCE_SECRET_KEY

1. **New repository secret**
2. Name: `BINANCE_SECRET_KEY`
3. Secret: Paste the value from `.env`
4. **Add secret**

#### 5.3 SUPABASE_URL

1. **New repository secret**
2. Name: `SUPABASE_URL`
3. Secret: Paste the complete URL (must start with `https://` and end with `.supabase.co`)
4. **Add secret**

**Example:**
```
https://qsnkdjfhskjfh.supabase.co
```

#### 5.4 SUPABASE_KEY

1. **New repository secret**
2. Name: `SUPABASE_KEY`
3. Secret: Paste the **anon/public** key (must start with `eyJ`)
4. **Add secret**

**⚠️ IMPORTANT:** Use the **anon/public** key, NOT the service_role!

In Supabase:
- Settings → API → Project API keys → **anon/public** ✅
- Settings → API → Project API keys → ~~service_role~~ ❌

#### 5.5 SPREADSHEET_ID

1. **New repository secret**
2. Name: `SPREADSHEET_ID`
3. Secret: Paste only the ID (from the spreadsheet URL)
4. **Add secret**

**How to get it:**
```
URL: https://docs.google.com/spreadsheets/d/1BgEEZObNjblahblahUhutvtyw/edit
                                              ^^^^^^^^^^^^^^^^^^^^
                                              Paste only this part
```

#### 5.6 GOOGLE_CREDENTIALS_JSON (CRITICAL!)

This is the most complicated and where the error usually happens.

**Method 1: Copy from .env (Recommended)**

1. Open the `.env` file in your editor
2. Locate the line `GOOGLE_CREDENTIALS_JSON=`
3. Copy EVERYTHING after the `=`, including the `{}` braces
4. Paste in the GitHub Secret

**Method 2: Copy from the original JSON file**

1. Open the `.json` file downloaded from Google Cloud
2. Copy ALL the content
3. **IMPORTANT:** Remove ALL line breaks
4. Must be in ONE SINGLE LINE

**Correct example (all in one line):**
```json
{"type":"service_account","project_id":"crypto-monitor-123456","private_key_id":"abc123def456","private_key":"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0B...\n-----END PRIVATE KEY-----\n","client_email":"crypto-sheets@crypto-monitor-123456.iam.gserviceaccount.com","client_id":"123456789","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/crypto-sheets%40crypto-monitor-123456.iam.gserviceaccount.com"}
```

**❌ WRONG (with line breaks):**
```json
{
  "type": "service_account",
  "project_id": "crypto-monitor-123456",
  ...
}
```

**How to convert from multiple lines to one:**

```bash
# Linux/Mac
cat google-credentials.json | jq -c . | pbcopy

# Or manually in the editor:
# 1. Select all
# 2. Find and replace: \n with nothing (empty)
# 3. Make sure there are no extra spaces
```

### 6. Validate the JSON before adding

```bash
# Copy the JSON to a temporary file
echo 'PASTE_THE_JSON_HERE' > /tmp/test.json

# Validate
python3 -c "import json; print('✅ Valid JSON' if json.load(open('/tmp/test.json')) else '❌ Invalid JSON')"

# Clean up
rm /tmp/test.json
```

### 7. Verify the created secrets

After creating all, you should see:

```
✅ BINANCE_API_KEY
✅ BINANCE_SECRET_KEY
✅ SUPABASE_URL
✅ SUPABASE_KEY
✅ SPREADSHEET_ID
✅ GOOGLE_CREDENTIALS_JSON
```

### 8. Test with Debug Workflow

1. Go to **Actions**
2. Select **Crypto Monitor (Debug Mode)**
3. Click **Run workflow**
4. Select `main`
5. **Run workflow**

This workflow will show:
- ✅ Size of each secret
- ✅ If formats are correct
- ✅ If it can connect to each service
- ✅ Detailed logs of each step

### 9. Analyze the Logs

Go to the execution and check the logs. Look for:

**If Supabase error:**
```
❌ Error connecting to Supabase: ...
```
→ Problem: SUPABASE_URL or SUPABASE_KEY incorrect

**If Google Sheets error:**
```
❌ Error setting up Google Sheets: ...
```
→ Problem: GOOGLE_CREDENTIALS_JSON or SPREADSHEET_ID incorrect

**If JSON is broken:**
```
❌ Error decoding Google JSON: ...
```
→ Problem: JSON with line breaks or incorrect format

## 🎯 Final Checklist

After recreating all secrets:

- [ ] Run the debug workflow
- [ ] Check if all checks passed (✅)
- [ ] Check if Supabase was updated
- [ ] Check if Google Sheets was updated
- [ ] If everything is OK, the normal workflow will work

## 🆘 Still not working?

If even after recreating the secrets it doesn't work:

1. **Compare the values:**
   ```bash
   # Local (works)
   cat .env
   
   # GitHub (compare with the secrets)
   ```

2. **Check character by character:**
   - Cannot have extra spaces
   - Cannot have quotes
   - Cannot have line breaks (except in the private_key of the JSON)

3. **Check the spreadsheet:**
   - Is it shared with the service account?
   - Does it have Editor permission?
   - Is the ID correct?

## 💡 Pro Tip

To ensure the JSON is correct, use this command to generate a "minified" version:

```bash
# Takes the JSON from .env and minifies it
grep GOOGLE_CREDENTIALS_JSON .env | cut -d'=' -f2- | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin)))"
```

Paste the result directly into the GitHub Secret.
