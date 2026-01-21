# 🌐 APIs Alternativas para Preços de Criptomoedas

## 🚨 Problema: Erro 451 da Binance

A Binance retorna erro **451 (Unavailable For Legal Reasons)** quando detecta requisições de regiões bloqueadas, incluindo:
- Servidores do GitHub Actions (principalmente EUA)
- Alguns provedores de cloud
- VPNs e proxies conhecidos

## ✅ Solução Implementada

O código agora usa um **sistema de fallback automático**:

1. 🥇 **Binance API** (primária)
   - Tenta primeiro a Binance
   - Melhor precisão e volume de dados
   
2. 🥈 **CoinGecko API** (fallback)
   - Se Binance falhar (erro 451), usa CoinGecko
   - API pública, sem necessidade de chave
   - Boa cobertura de moedas

## 📊 Comparação das APIs

### Binance API

**Prós:**
- ✅ Dados em tempo real
- ✅ Volume preciso
- ✅ Múltiplos endpoints

**Contras:**
- ❌ Bloqueada em algumas regiões
- ❌ Requer chave de API (para alguns endpoints)
- ❌ Rate limits mais rigorosos

**Endpoint usado:**
```
https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDC
```

### CoinGecko API

**Prós:**
- ✅ Funciona globalmente
- ✅ Não requer chave de API
- ✅ Rate limits generosos (50 req/min)
- ✅ Dados de múltiplas exchanges

**Contras:**
- ❌ Dados agregados (média de várias exchanges)
- ❌ Latência um pouco maior
- ❌ Volume em USD (não em BTC/ETH)

**Endpoint usado:**
```
https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_vol=true&include_24hr_change=true
```

## 🔧 Como Funciona o Fallback

```python
# 1. Tenta Binance
try:
    response = requests.get("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDC")
    if response.status_code == 451:
        # 2. Se bloqueado, usa CoinGecko
        alternative_data = get_from_coingecko("bitcoin")
except:
    # 3. Em caso de erro, também tenta alternativa
    alternative_data = get_from_coingecko("bitcoin")
```

## 🎯 Mapeamento de Símbolos

| Binance | CoinGecko ID | Nome |
|---------|-------------|------|
| BTCUSDC | bitcoin | Bitcoin |
| ETHUSDC | ethereum | Ethereum |
| BNBUSDC | binancecoin | BNB |
| ADAUSDC | cardano | Cardano |
| SOLUSDC | solana | Solana |

## 📝 Outras Alternativas Possíveis

Se quiser adicionar mais fallbacks, considere:

### 1. CoinCap
```python
url = "https://api.coincap.io/v2/assets/bitcoin"
# Sem necessidade de chave
# Rate limit: ~200 req/min
```

### 2. CryptoCompare
```python
url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"
# Requer chave de API (gratuita)
# Rate limit: 100,000 req/mês
```

### 3. Binance US
```python
url = "https://api.binance.us/api/v3/ticker/24hr?symbol=BTCUSDC"
# Alternativa da Binance para EUA
# Pode estar acessível de servidores GitHub
```

### 4. Kraken
```python
url = "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
# API pública
# Nomenclatura diferente (XBT = BTC)
```

## 🚀 Para Desenvolvedores

### Adicionar Nova API Alternativa

1. Crie uma função no `main.py`:
```python
def _get_price_from_kraken(self, symbol: str) -> Dict:
    # Mapeamento de símbolos
    symbol_map = {
        "BTCUSDC": "XBTUSD",
        "ETHUSDC": "ETHUSD",
        # ...
    }
    
    kraken_symbol = symbol_map.get(symbol)
    url = f"https://api.kraken.com/0/public/Ticker?pair={kraken_symbol}"
    
    response = requests.get(url)
    data = response.json()
    
    # Processar resposta específica da Kraken
    # ...
    
    return processed_data
```

2. Adicione no fallback:
```python
# Se CoinGecko falhar
if not alt_response:
    alt_response = self._get_price_from_kraken(symbol)
```

## 📊 Monitoramento de APIs

Para monitorar qual API está sendo usada, o código imprime:

```
✓ BTCUSDC: $89,261.45  # Binance funcionou
✓ ETHUSDC: Obtido de CoinGecko  # Binance falhou, usou CoinGecko
```

## ⚡ Performance

| API | Latência Média | Disponibilidade |
|-----|---------------|-----------------|
| Binance | ~100ms | ~95% (bloqueios geográficos) |
| CoinGecko | ~300ms | ~99.9% |
| CoinCap | ~200ms | ~99% |

## 🔐 Segurança

**Binance:**
- Chaves de API não são mais necessárias para preços públicos
- Mantenha as chaves salvas apenas se precisar de endpoints privados

**CoinGecko:**
- API totalmente pública
- Sem necessidade de autenticação
- Rate limit por IP

## 📚 Documentação das APIs

- **Binance:** https://binance-docs.github.io/apidocs/spot/en/
- **CoinGecko:** https://www.coingecko.com/en/api/documentation
- **CoinCap:** https://docs.coincap.io/
- **CryptoCompare:** https://min-api.cryptocompare.com/documentation

## 💡 Dicas

1. **Para produção séria**: Considere usar múltiplas APIs e calcular média
2. **Para alta frequência**: Use WebSockets ao invés de REST
3. **Para histórico**: APIs como CoinGecko oferecem dados históricos gratuitos
4. **Para alertas**: Configure webhooks em serviços especializados