# 🚀 Crypto Monitor

Sistema automatizado de monitoramento de criptomoedas que coleta dados da Binance, armazena no Supabase e atualiza uma planilha do Google Sheets em tempo real.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-green)
![Binance API](https://img.shields.io/badge/Binance-API-yellow)

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração Passo a Passo](#-configuração-passo-a-passo)
  - [1. API da Binance](#1-configuração-da-api-da-binance)
  - [2. Supabase](#2-configuração-do-supabase)
  - [3. Google Sheets](#3-configuração-do-google-sheets)
  - [4. GitHub](#4-configuração-do-github)
- [Instalação Local](#-instalação-local)
- [Uso](#-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Troubleshooting](#-troubleshooting)
- [Próximas Melhorias](#-próximas-melhorias)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

## ✨ Funcionalidades

- 📊 Coleta automática de preços de criptomoedas (BTC, ETH, BNB, ADA, SOL)
- 💾 Armazenamento histórico no Supabase
- 📈 Atualização automática do Google Sheets
- ⏰ Execução automatizada via GitHub Actions (a cada 1 hora)
- 🔄 Dados de variação e volume 24h
- 🎨 Formatação visual da planilha

## 🏗 Arquitetura

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

## 📦 Pré-requisitos

- Conta na [Binance](https://www.binance.com)
- Conta no [Supabase](https://supabase.com)
- Conta no [Google Cloud Platform](https://console.cloud.google.com)
- Conta no [GitHub](https://github.com)
- Python 3.11+ (para testes locais)

## 🛠 Configuração Passo a Passo

### 1. Configuração da API da Binance

#### 1.1 Criar API Keys

1. Faça login na [Binance](https://www.binance.com)
2. Vá em **Perfil** → **API Management**
3. Clique em **Create API**
4. Escolha **System Generated**
5. Dê um nome: `CryptoMonitor`
6. Complete a verificação 2FA
7. **Importante**: Salve a **API Key** e **Secret Key** em local seguro

#### 1.2 Configurar Permissões

- ✅ Enable Reading
- ❌ Enable Spot & Margin Trading (desabilitar por segurança)
- ❌ Enable Futures (desabilitar)
- ❌ Enable Withdrawals (desabilitar)

⚠️ **Importante**: Nunca compartilhe suas chaves de API!

---

### 2. Configuração do Supabase

#### 2.1 Criar Projeto

1. Acesse [supabase.com](https://supabase.com)
2. Clique em **New Project**
3. Preencha:
   - **Name**: `crypto-monitor`
   - **Database Password**: (escolha uma senha forte)
   - **Region**: escolha a mais próxima de você
4. Aguarde a criação (1-2 minutos)

#### 2.2 Criar Tabela no Banco de Dados

1. No painel do Supabase, vá em **SQL Editor**
2. Clique em **New Query**
3. Cole e execute o seguinte SQL:

```sql
CREATE TABLE crypto_prices (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    price DECIMAL(20, 8) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    volume_24h DECIMAL(20, 8),
    price_change_24h DECIMAL(10, 2)
);

-- Índice para buscas mais rápidas
CREATE INDEX idx_symbol_timestamp ON crypto_prices(symbol, timestamp DESC);
```

#### 2.3 Obter Credenciais

1. Vá em **Settings** → **API**
2. Copie e salve:
   - **Project URL** (ex: `https://xxxxx.supabase.co`)
   - **Project API Key** (anon/public)

---

### 3. Configuração do Google Sheets

#### 3.1 Criar Projeto no Google Cloud

1. Acesse [console.cloud.google.com](https://console.cloud.google.com)
2. Clique em **Select a project** → **New Project**
3. Nome do projeto: `crypto-monitor`
4. Clique em **Create**

#### 3.2 Ativar APIs Necessárias

1. No menu lateral, vá em **APIs & Services** → **Enable APIs and Services**
2. Busque e ative:
   - **Google Sheets API**
   - **Google Drive API**

#### 3.3 Criar Service Account

1. Vá em **APIs & Services** → **Credentials**
2. Clique em **Create Credentials** → **Service Account**
3. Preencha:
   - **Service account name**: `crypto-sheets-bot`
   - **Service account ID**: (será gerado automaticamente)
4. Clique em **Create and Continue**
5. Pule as permissões opcionais → **Done**

#### 3.4 Gerar Chave JSON

1. Clique na service account criada
2. Vá na aba **Keys**
3. Clique em **Add Key** → **Create new key**
4. Escolha formato **JSON**
5. Clique em **Create**
6. **Salve o arquivo JSON baixado em local seguro!**

#### 3.5 Criar e Compartilhar Planilha

1. Acesse [sheets.google.com](https://sheets.google.com)
2. Crie uma nova planilha com o nome: `Crypto Monitor`
3. Abra o arquivo JSON da service account e copie o valor do campo `client_email`
4. Na planilha, clique em **Compartilhar**
5. Cole o email da service account
6. Dê permissão de **Editor**
7. Clique em **Enviar**
8. Copie o **ID da planilha** da URL:
   ```
   https://docs.google.com/spreadsheets/d/[ESTE_É_O_ID]/edit
   ```

---

### 4. Configuração do GitHub

#### 4.1 Criar Repositório

1. Acesse [github.com](https://github.com)
2. Clique em **New repository**
3. Nome: `crypto-monitor`
4. Escolha **Private** (recomendado) ou **Public**
5. **NÃO** marque "Add a README file"
6. Clique em **Create repository**

#### 4.2 Configurar Secrets

1. No repositório, vá em **Settings** → **Secrets and variables** → **Actions**
2. Clique em **New repository secret**
3. Adicione os seguintes secrets (um por vez):

| Nome | Descrição | Exemplo |
|------|-----------|---------|
| `BINANCE_API_KEY` | Sua API Key da Binance | `abc123...` |
| `BINANCE_SECRET_KEY` | Sua Secret Key da Binance | `xyz789...` |
| `SUPABASE_URL` | URL do projeto Supabase | `https://xxxxx.supabase.co` |
| `SUPABASE_KEY` | API Key do Supabase | `eyJhbGci...` |
| `SPREADSHEET_ID` | ID da planilha Google Sheets | `1AbC...xyz` |
| `GOOGLE_CREDENTIALS_JSON` | Conteúdo completo do arquivo JSON | `{"type":"service_account",...}` |

⚠️ **Importante**: Para `GOOGLE_CREDENTIALS_JSON`, cole o conteúdo **completo** do arquivo JSON baixado, incluindo as chaves `{}`.

---

## 💻 Instalação Local

### 1. Clone o Repositório

```bash
git clone https://github.com/SEU_USUARIO/crypto-monitor.git
cd crypto-monitor
```

### 2. Crie um Ambiente Virtual

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

2. Edite o arquivo `.env` e adicione suas credenciais

### 5. Execute o Script

```bash
python main.py
```

Se tudo estiver configurado corretamente, você verá:

```
🚀 Iniciando coleta de dados...
📊 Obtidos 5 preços da Binance
✅ 5 registros salvos no Supabase
✅ Google Sheets atualizado com sucesso
✨ Processo concluído!
```

---

## 📖 Uso

### Execução Automática

O GitHub Actions executará o script automaticamente a cada 1 hora. Você pode acompanhar as execuções em:

**Repositório** → **Actions** → **Crypto Monitor**

### Execução Manual

Para executar manualmente via GitHub Actions:

1. Vá em **Actions**
2. Selecione o workflow **Crypto Monitor**
3. Clique em **Run workflow**
4. Selecione a branch `main`
5. Clique em **Run workflow**

### Alterar Frequência de Atualização

Edite o arquivo `.github/workflows/crypto-monitor.yml` e modifique a linha do cron:

```yaml
schedule:
  # A cada 30 minutos
  - cron: '*/30 * * * *'
  
  # A cada 6 horas
  - cron: '0 */6 * * *'
  
  # Uma vez por dia às 9h UTC
  - cron: '0 9 * * *'
```

Use o site [crontab.guru](https://crontab.guru/) para gerar expressões cron.

---

## 📁 Estrutura do Projeto

```
crypto-monitor/
├── .github/
│   └── workflows/
│       └── crypto-monitor.yml    # Configuração do GitHub Actions
├── main.py                       # Script principal
├── requirements.txt              # Dependências Python
├── .env.example                  # Exemplo de variáveis de ambiente
├── .gitignore                    # Arquivos ignorados pelo Git
└── README.md                     # Este arquivo
```

---

## 🔐 Variáveis de Ambiente

| Variável | Descrição | Obrigatória |
|----------|-----------|-------------|
| `BINANCE_API_KEY` | API Key da Binance | ✅ |
| `BINANCE_SECRET_KEY` | Secret Key da Binance | ✅ |
| `SUPABASE_URL` | URL do projeto Supabase | ✅ |
| `SUPABASE_KEY` | API Key do Supabase (anon/public) | ✅ |
| `SPREADSHEET_ID` | ID da planilha Google Sheets | ✅ |
| `GOOGLE_CREDENTIALS_JSON` | JSON da service account do Google | ✅ |

---

## 🔧 Troubleshooting

### Erro: "Invalid API Key"

- Verifique se as credenciais da Binance estão corretas
- Confirme que a API Key tem permissão de leitura habilitada

### Erro: "Authentication failed" (Supabase)

- Verifique se a URL e API Key do Supabase estão corretas
- Confirme que a tabela `crypto_prices` foi criada

### Erro: "Permission denied" (Google Sheets)

- Verifique se compartilhou a planilha com o email da service account
- Confirme que deu permissão de Editor

### Erro: "Workflow failed"

- Vá em **Actions** no GitHub e clique na execução com erro
- Verifique os logs detalhados para identificar o problema
- Confirme que todos os secrets foram adicionados corretamente

### Google Sheets não atualiza

- Verifique se o `SPREADSHEET_ID` está correto
- Confirme que o JSON das credenciais foi colado completamente no secret
- Teste localmente primeiro para verificar se o problema é no GitHub Actions

---

## 🚀 Próximas Melhorias

Funcionalidades planejadas:

- [ ] Alertas de preço via email ou Telegram
- [ ] Gráficos históricos no Google Sheets
- [ ] Notificações de variações bruscas
- [ ] Análise de tendências e médias móveis
- [ ] Dashboard web interativo
- [ ] Suporte a mais exchanges
- [ ] Backup automático dos dados
- [ ] Sistema de alertas personalizados
- [ ] API REST para consultar dados
- [ ] Integração com Discord/Slack

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 📞 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique a seção [Troubleshooting](#-troubleshooting)
2. Abra uma [Issue](https://github.com/SEU_USUARIO/crypto-monitor/issues)
3. Consulte a [documentação oficial da Binance API](https://binance-docs.github.io/apidocs/spot/en/)

---

## ⚠️ Aviso Legal

Este projeto é apenas para fins educacionais e de monitoramento. Não constitui aconselhamento financeiro. Sempre faça sua própria pesquisa antes de investir em criptomoedas.

---

**Desenvolvido com ❤️ usando Python, Binance API, Supabase e Google Sheets**

---

## 📊 Screenshots

### Planilha Google Sheets
A planilha será atualizada automaticamente com os dados mais recentes:

| Criptomoeda | Preço (USDT) | Variação 24h (%) | Volume 24h | Última Atualização |
|-------------|--------------|------------------|------------|--------------------|
| BTC | $43,250.50 | +2.34% | $28,543,000,000 | 20/01/2026 14:30:00 |
| ETH | $2,845.75 | -1.12% | $15,234,000,000 | 20/01/2026 14:30:00 |

### GitHub Actions
O workflow será executado automaticamente e você poderá acompanhar o status:

```
✅ Crypto Monitor - Execução bem-sucedida
```

---

## 🌟 Star o Projeto

Se este projeto foi útil para você, considere dar uma ⭐ no repositório!