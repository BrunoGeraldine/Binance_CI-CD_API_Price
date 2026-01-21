import os
import json
from datetime import datetime
from typing import List, Dict
import requests
from supabase import create_client, Client
import gspread
from google.oauth2.service_account import Credentials
import time

# Load environment variables from .env file (for local testing)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # GitHub Actions does not need dotenv

# Configuration
BINANCE_API_URL = "https://api.binance.com/api/v3"
SYMBOLS = ["BTCUSDC", "ETHUSDC", "BNBUSDC", "XRPUSDC", "SOLUSDC", "LINKUSDC"]

class CryptoMonitor:
    def __init__(self):
        # Binance
        self.binance_api_key = os.getenv("BINANCE_API_KEY")
        self.binance_secret = os.getenv("BINANCE_SECRET_KEY")
        
        # Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be configured")
        
        try:
            self.supabase: Client = create_client(supabase_url, supabase_key)
            print("✅ Connected to Supabase")
        except Exception as e:
            print(f"❌ Error connecting to Supabase: {e}")
            raise
        
        # Google Sheets
        self.setup_google_sheets()
    
    def setup_google_sheets(self):
        """Setup connection with Google Sheets"""
        try:
            creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
            
            if not creds_json:
                raise ValueError("GOOGLE_CREDENTIALS_JSON not configured")
            
            creds_dict = json.loads(creds_json)
            
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            credentials = Credentials.from_service_account_info(
                creds_dict, 
                scopes=scopes
            )
            
            self.gc = gspread.authorize(credentials)
            spreadsheet_id = os.getenv("SPREADSHEET_ID")
            
            if not spreadsheet_id:
                raise ValueError("SPREADSHEET_ID not configured")
            
            self.sheet = self.gc.open_by_key(spreadsheet_id).sheet1
            print("✅ Connected to Google Sheets")
            
        except json.JSONDecodeError as e:
            print(f"❌ Error decoding Google JSON: {e}")
            raise
        except Exception as e:
            print(f"❌ Error setting up Google Sheets: {e}")
            raise
    
    def _get_all_prices_from_coingecko(self) -> Dict[str, Dict]:
        """Get all prices from CoinGecko in a single request (avoids rate limiting)"""
        try:
            # Map Binance symbols to CoinGecko IDs
            symbol_map = {
                "BTCUSDC": "bitcoin",
                "ETHUSDC": "ethereum",
                "BNBUSDC": "binancecoin",
                "XRPUSDC": "ripple",
                "SOLUSDC": "solana",
                "LINKUSDC": "chainlink"
            }
            
            # Join all IDs in a single comma-separated string
            all_ids = ",".join(symbol_map.values())
            
            # Use CoinGecko API (public, no key needed)
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": all_ids,
                "vs_currencies": "usd",
                "include_24hr_vol": "true",
                "include_24hr_change": "true"
            }
            
            # Retry with exponential backoff to handle rate limiting
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.get(url, params=params, timeout=15)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Convert data to expected format
                    result = {}
                    for symbol, coin_id in symbol_map.items():
                        if coin_id in data:
                            coin_data = data[coin_id]
                            result[symbol] = {
                                "symbol": symbol,
                                "price": float(coin_data["usd"]),
                                "volume_24h": float(coin_data.get("usd_24h_vol", 0)),
                                "price_change_24h": float(coin_data.get("usd_24h_change", 0)),
                                "timestamp": datetime.now().isoformat(),
                                "source": "CoinGecko"
                            }
                            print(f"  ✓ {symbol}: Retrieved from CoinGecko")
                    
                    return result
                    
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429 and attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * 2  # 2s, 4s, 8s
                        print(f"  ⏳ Rate limit reached, waiting {wait_time}s before retrying...")
                        time.sleep(wait_time)
                    else:
                        raise
            
        except Exception as e:
            print(f"  ✗ Error retrieving prices from CoinGecko: {e}")
        
        return {}
    
    def get_binance_prices(self) -> List[Dict]:
        """Get prices from Binance, using CoinGecko as fallback"""
        prices_data = []
        failed_symbols = []
        
        # Headers to prevent blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        # First try to get each symbol from Binance
        for symbol in SYMBOLS:
            try:
                # Use public endpoint without authentication
                ticker_url = f"{BINANCE_API_URL}/ticker/24hr"
                params = {"symbol": symbol}
                
                response = requests.get(
                    ticker_url, 
                    params=params,
                    headers=headers,
                    timeout=10
                )
                
                # If error 451 (geographic blocking), mark for CoinGecko lookup
                if response.status_code == 451:
                    print(f"⚠️  {symbol}: Geographically blocked (error 451)")
                    failed_symbols.append(symbol)
                    continue
                
                response.raise_for_status()
                data = response.json()
                
                prices_data.append({
                    "symbol": symbol,
                    "price": float(data["lastPrice"]),
                    "volume_24h": float(data["volume"]),
                    "price_change_24h": float(data["priceChangePercent"]),
                    "timestamp": datetime.now().isoformat(),
                    "source": "Binance"
                })
                print(f"  ✓ {symbol}: Retrieved from Binance")
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 451:
                    print(f"⚠️  {symbol}: Geographically blocked (error 451)")
                    failed_symbols.append(symbol)
                else:
                    print(f"  ✗ HTTP error retrieving {symbol}: {e}")
                    failed_symbols.append(symbol)
            except Exception as e:
                print(f"  ✗ Error retrieving price for {symbol}: {e}")
                failed_symbols.append(symbol)
        
        # If there are failed symbols, fetch all at once from CoinGecko
        if failed_symbols:
            print(f"\n🔄 Retrieving {len(failed_symbols)} cryptocurrencies from CoinGecko (alternative API)...")
            coingecko_data = self._get_all_prices_from_coingecko()
            
            # Add CoinGecko data for failed symbols
            for symbol in failed_symbols:
                if symbol in coingecko_data:
                    prices_data.append(coingecko_data[symbol])
                else:
                    print(f"  ✗ Could not retrieve price for {symbol}")
        
        return prices_data
    
    def save_to_supabase(self, prices_data: List[Dict]):
        """Save data to Supabase"""
        if not prices_data:
            print("⚠️  No data to save to Supabase")
            return
        
        try:
            saved_count = 0
            for data in prices_data:
                try:
                    result = self.supabase.table("crypto_prices").insert(data).execute()
                    saved_count += 1
                    print(f"  ✓ {data['symbol']}: ${data['price']:.2f} (source: {data['source']})")
                except Exception as e:
                    print(f"  ✗ Error saving {data['symbol']}: {e}")
            
            print(f"✅ {saved_count}/{len(prices_data)} records saved to Supabase")
        except Exception as e:
            print(f"❌ General error saving to Supabase: {e}")
            import traceback
            traceback.print_exc()
    
    def update_google_sheets(self, prices_data: List[Dict]):
        """Update Google Sheets with Source column"""
        if not prices_data:
            print("⚠️  No data to update in Google Sheets")
            return
        
        try:
            print(f"📝 Preparing data for {len(prices_data)} cryptocurrencies...")
            
            # Header - INCLUDING SOURCE COLUMN
            headers = [
                "Cryptocurrency", 
                "Price (USDC)", 
                "24h Change (%)", 
                "24h Volume",
                "Source",  # New column
                "Last Updated"
            ]
            
            # Data
            rows = [headers]
            for data in prices_data:
                rows.append([
                    data["symbol"].replace("USDC", ""),
                    f"${data['price']:,.2f}",
                    f"{data['price_change_24h']:.2f}%",
                    f"${data['volume_24h']:,.0f}",
                    data["source"],  # Data source (Binance or CoinGecko)
                    datetime.fromisoformat(data["timestamp"]).strftime("%m/%d/%Y %H:%M:%S")
                ])
            
            print(f"📤 Sending {len(rows)} rows to Google Sheets...")
            
            # Clear and update the spreadsheet
            self.sheet.clear()
            self.sheet.update(range_name='A1', values=rows)
            
            print(f"🎨 Applying formatting...")
            
            # Format header
            self.sheet.format('A1:F1', {
                "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.2},
                "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
            })
            
            print("✅ Google Sheets updated successfully")
            
        except Exception as e:
            print(f"❌ Error updating Google Sheets: {e}")
            import traceback
            traceback.print_exc()
    
    def run(self):
        """Execute the complete process"""
        print("=" * 60)
        print("🚀 CRYPTO MONITOR - Starting data collection...")
        print("=" * 60)
        print()
        
        # 1. Get prices
        print("1️⃣  Collecting prices from Binance...")
        prices_data = self.get_binance_prices()
        
        if not prices_data:
            print("❌ No data collected. Exiting.")
            return
        
        print(f"\n✅ Retrieved {len(prices_data)}/{len(SYMBOLS)} prices successfully")
        print()
        
        # Show summary of collected data
        print("📊 Summary of collected data:")
        for data in prices_data:
            source_icon = "🟢" if data['source'] == "Binance" else "🔵"
            print(f"  {source_icon} {data['symbol']}: ${data['price']:,.2f} ({data['price_change_24h']:+.2f}%) - {data['source']}")
        print()
        
        # 2. Save to Supabase
        print("2️⃣  Saving to Supabase...")
        self.save_to_supabase(prices_data)
        print()
        
        # 3. Update Google Sheets
        print("3️⃣  Updating Google Sheets...")
        self.update_google_sheets(prices_data)
        print()
        
        print("=" * 60)
        print("✨ PROCESS COMPLETED SUCCESSFULLY!")
        print("=" * 60)

if __name__ == "__main__":
    monitor = CryptoMonitor()
    monitor.run()