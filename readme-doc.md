# 🚀 Crypto Monitor

Automated system for monitoring cryptocurrencies that collects data from Binance, stores it in Supabase and updates a Google Sheets spreadsheet in real time.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-green)
![Binance API](https://img.shields.io/badge/Binance-API-yellow)

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Step-by-Step Configuration](#-step-by-step-configuration)
  - [1. Binance API](#1-binance-api-configuration)
  - [2. Supabase](#2-supabase-configuration)
  - [3. Google Sheets](#3-google-sheets-configuration)
  - [4. GitHub](#4-github-configuration)
- [Local Installation](#-local-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Environment Variables](#-environment-variables)
- [Troubleshooting](#-troubleshooting)
- [Next Improvements](#-next-improvements)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- 📊 Automatic collection of cryptocurrency prices (BTC, ETH, BNB, ADA, SOL)
- 💾 Historical storage in Supabase
- 📈 Automatic Google Sheets update
- ⏰ Automated execution via GitHub Actions (every 1 hour)
- 🔄 24h variation and volume data
- 🎨 Visual spreadsheet formatting

## 🏗 Architecture

```
┌─────────────┐
│   Binance   │
│     API     │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌──────────────┐
│   Python    │────▶│   Supabase   │
│   Script    │     │  (PostgreSQL)│
└──────┬──────┘     └──────────────┘
       │
       ▼
┌─────────────┐
│   Google    │
│   Sheets    │
└─────────────┘
       ▲
       │
┌──────┴──────┐
│   GitHub    │
│   Actions   │
│  (Schedule) │
└─────────────┘
```

## 📦 Prerequisites

- Account on [Binance](https://www.binance.com)
- Account on [Supabase](https://supabase.com)
- Account on [Google Cloud Platform](https://console.cloud.google.com)
- Account on [GitHub](https://github.com)
- Python 3.11+ (for local testing)

## 🛠 Step-by-Step Configuration

### 1. Binance API Configuration

#### 1.1 Create API Keys

1. Log in to [Binance](https://www.binance.com)
2. Go to **Profile** → **API Management**
3. Click **Create API**
4. Choose **System Generated**
5. Give it a name: `CryptoMonitor`
6. Complete the 2FA verification
7. **Important**: Save the **API Key** and **Secret Key** in a secure location

#### 1.2 Configure Permissions

- ✅ Enable Reading
- ❌ Enable Spot & Margin Trading (disable for security)
- ❌ Enable Futures (disable)
- ❌ Enable Withdrawals (disable)

⚠️ **Important**: Never share your API keys!

---

### 2. Supabase Configuration

#### 2.1 Create Project

1. Visit [supabase.com](https://supabase.com)
2. Click **New Project**
3. Fill in:
   - **Name**: `crypto-monitor`
   - **Database Password**: (choose a strong password)
   - **Region**: choose the closest one to you
4. Wait for creation (1-2 minutes)

#### 2.2 Create Table in Database

1. In the Supabase panel, go to **SQL Editor**
2. Click **New Query**
3. Paste and execute the following SQL:

```sql
CREATE TABLE crypto_prices (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    price DECIMAL(20, 8) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    volume_24h DECIMAL(20, 8),
    price_change_24h DECIMAL(10, 2)
);

-- Index for faster searches
CREATE INDEX idx_symbol_timestamp ON crypto_prices(symbol, timestamp DESC);
```

#### 2.3 Get Credentials

1. Go to **Settings** → **API**
2. Copy and save:
   - **Project URL** (ex: `https://xxxxx.supabase.co`)
   - **Project API Key** (anon/public)

---

### 3. Google Sheets Configuration

#### 3.1 Create Project on Google Cloud

1. Visit [console.cloud.google.com](https://console.cloud.google.com)
2. Click **Select a project** → **New Project**
3. Project name: `crypto-monitor`
4. Click **Create**

#### 3.2 Enable Necessary APIs

1. In the left menu, go to **APIs & Services** → **Enable APIs and Services**
2. Search and enable:
   - **Google Sheets API**
   - **Google Drive API**

#### 3.3 Create Service Account

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **Service Account**
3. Fill in:
   - **Service account name**: `crypto-sheets-bot`
   - **Service account ID**: (will be generated automatically)
4. Click **Create and Continue**
5. Skip optional permissions → **Done**

#### 3.4 Generate JSON Key

1. Click on the created service account
2. Go to the **Keys** tab
3. Click **Add Key** → **Create new key**
4. Choose **JSON** format
5. Click **Create**
6. **Save the downloaded JSON file in a secure location!**

#### 3.5 Create and Share Spreadsheet

1. Visit [sheets.google.com](https://sheets.google.com)
2. Create a new spreadsheet named: `Crypto Monitor`
3. Open the JSON file of the service account and copy the value of the `client_email` field
4. In the spreadsheet, click **Share**
5. Paste the service account email
6. Give **Editor** permission
7. Click **Send**
8. Copy the **Spreadsheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/[THIS_IS_THE_ID]/edit
   ```

---

### 4. GitHub Configuration

#### 4.1 Create Repository

1. Visit [github.com](https://github.com)
2. Click **New repository**
3. Name: `crypto-monitor`
4. Choose **Private** (recommended) or **Public**
5. **DO NOT** check "Add a README file"
6. Click **Create repository**

#### 4.2 Configure Secrets

1. In the repository, go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add the following secrets (one at a time):

| Name | Description | Example |
|------|-----------|---------|
| `BINANCE_API_KEY` | Your Binance API Key | `abc123...` |
| `BINANCE_SECRET_KEY` | Your Binance Secret Key | `xyz789...` |
| `SUPABASE_URL` | Supabase project URL | `https://xxxxx.supabase.co` |
| `SUPABASE_KEY` | Supabase API Key | `eyJhbGci...` |
| `SPREADSHEET_ID` | Google Sheets ID | `1AbC...xyz` |
| `GOOGLE_CREDENTIALS_JSON` | Complete JSON file content | `{"type":"service_account",...}` |

⚠️ **Important**: For `GOOGLE_CREDENTIALS_JSON`, paste the **complete** content of the downloaded JSON file, including the `{}` braces.

---

## 💻 Local Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USER/crypto-monitor.git
cd crypto-monitor
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit the `.env` file and add your credentials

### 5. Run the Script

```bash
python main.py
```

If everything is configured correctly, you will see:

```
🚀 Starting data collection...
📊 Obtained 5 prices from Binance
✅ 5 records saved to Supabase
✅ Google Sheets updated successfully
✨ Process completed!
```

---

## 📖 Usage

### Automatic Execution

GitHub Actions will run the script automatically every 1 hour. You can track executions at:

**Repository** → **Actions** → **Crypto Monitor**

### Manual Execution

To run manually via GitHub Actions:

1. Go to **Actions**
2. Select the **Crypto Monitor** workflow
3. Click **Run workflow**
4. Select the `main` branch
5. Click **Run workflow**

### Change Update Frequency

Edit the `.github/workflows/crypto-monitor.yml` file and modify the cron line:

```yaml
schedule:
  # Every 30 minutes
  - cron: '*/30 * * * *'
  
  # Every 6 hours
  - cron: '0 */6 * * *'
  
  # Once a day at 9am UTC
  - cron: '0 9 * * *'
```

Use [crontab.guru](https://crontab.guru/) to generate cron expressions.

---

## 📁 Project Structure

```
crypto-monitor/
├── .github/
│   └── workflows/
│       └── crypto-monitor.yml    # GitHub Actions configuration
├── main.py                       # Main script
├── requirements.txt              # Python dependencies
├── .env.example                  # Example environment variables
├── .gitignore                    # Files ignored by Git
└── README.md                     # This file
```

---

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-----------|----------|
| `BINANCE_API_KEY` | Binance API Key | ✅ |
| `BINANCE_SECRET_KEY` | Binance Secret Key | ✅ |
| `SUPABASE_URL` | Supabase project URL | ✅ |
| `SUPABASE_KEY` | Supabase API Key (anon/public) | ✅ |
| `SPREADSHEET_ID` | Google Sheets ID | ✅ |
| `GOOGLE_CREDENTIALS_JSON` | Google service account JSON | ✅ |

---

## 🔧 Troubleshooting

### Error 451: Binance geographically blocked

If you receive a `451 Client Error` when running on GitHub Actions:

```
Error retrieving price for BTCUSDC: 451 Client Error
```

**Cause**: Binance blocks requests from certain countries/regions, including GitHub Actions servers (located in the US).

**Solution**: The code now automatically uses an alternative API (CoinGecko) when Binance is blocked. No additional action is needed.

**Note**: Binance API keys (`BINANCE_API_KEY` and `BINANCE_SECRET_KEY`) are no longer required to collect public prices, but you can keep them configured for future use.

### Error: "Invalid API Key"

- Check if Binance credentials are correct
- Confirm that the API Key has read permission enabled

### Error: "Authentication failed" (Supabase)

- Check if the Supabase URL and API Key are correct
- Confirm that the `crypto_prices` table was created

### Error: "Permission denied" (Google Sheets)

- Check if you shared the spreadsheet with the service account email
- Confirm that you gave Editor permission

### Error: "Workflow failed"

- Go to **Actions** in GitHub and click on the execution with error
- Check the detailed logs to identify the problem
- Confirm that all secrets were added correctly

### Google Sheets does not update

- Check if the `SPREADSHEET_ID` is correct
- Confirm that the JSON credentials were completely pasted in the secret
- Test locally first to verify if the problem is in GitHub Actions

---

## 🚀 Next Improvements

Planned features:

- [ ] Price alerts via email or Telegram
- [ ] Historical charts in Google Sheets
- [ ] Notifications for sudden variations
- [ ] Trend analysis and moving averages
- [ ] Interactive web dashboard
- [ ] Support for more exchanges
- [ ] Automatic data backup
- [ ] Custom alert system
- [ ] REST API to query data
- [ ] Discord/Slack integration

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/MyFeature`)
3. Commit your changes (`git commit -m 'Add MyFeature'`)
4. Push to the branch (`git push origin feature/MyFeature`)
5. Open a Pull Request

---

## 📄 License

This project is under the MIT license. See the `LICENSE` file for details.

---

## 📞 Support

If you encounter problems or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Open an [Issue](https://github.com/YOUR_USER/crypto-monitor/issues)
3. Consult the [official Binance API documentation](https://binance-docs.github.io/apidocs/spot/en/)

---

## ⚠️ Legal Notice

This project is for educational and monitoring purposes only. It does not constitute financial advice. Always do your own research before investing in cryptocurrencies.

---

**Developed with ❤️ using Python, Binance API, Supabase and Google Sheets**

---

## 📊 Screenshots

### Google Sheets Spreadsheet
The spreadsheet will be automatically updated with the latest data:

| Cryptocurrency | Price (USDC) | 24h Change (%) | 24h Volume | Last Updated |
|-------------|--------------|------------------|------------|--------------------|
| BTC | $43,250.50 | +2.34% | $28,543,000,000 | 01/20/2026 14:30:00 |
| ETH | $2,845.75 | -1.12% | $15,234,000,000 | 01/20/2026 14:30:00 |

### GitHub Actions
The workflow will run automatically and you can track the status:

```
✅ Crypto Monitor - Successful execution
```

---

## 🌟 Star the Project

If this project was helpful to you, consider giving it a ⭐ on the repository!
