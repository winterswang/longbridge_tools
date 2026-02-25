# Longbridge Tools

A Python toolkit for interacting with the Longbridge OpenAPI, providing simplified skills for market data, trading, and asset management.

## Features

- **QuoteSkill**: Real-time quotes, market depth, broker queues, and historical candlesticks.
- **TradeSkill**: Order placement, cancellation, and order history.
- **AssetSkill**: Account balance, positions, and cash flow history.

## Installation

```bash
pip install -e .
```

## Configuration

You can configure the tools using a `config.yaml` file (Recommended) or environment variables.

### 1. Using Configuration File

Create a `config.yaml` file in your project root:

```yaml
app_key: "your_app_key"
app_secret: "your_app_secret"
access_token: "your_access_token"
# Optional: Override API URLs if needed
# http_url: "https://openapi.lbkrs.com"
```

You can use `config.yaml.example` as a template.

### 2. Using Environment Variables

Set the following environment variables:

```bash
export LONGBRIDGE_APP_KEY="your_app_key"
export LONGBRIDGE_APP_SECRET="your_app_secret"
export LONGBRIDGE_ACCESS_TOKEN="your_access_token"
```

## Usage

```python
from longbridge_tools import QuoteSkill, AppConfig

# Initialize with default config (looks for config.yaml or env vars)
quote_skill = QuoteSkill()

# Or specify a custom config file
quote_skill = QuoteSkill(config=AppConfig.load("my_config.yaml"))

# Get real-time quote
quotes = quote_skill.get_quote(["700.HK"])
print(quotes)
```

For more details, see [Skills Documentation](docs/skills.md) and [API Reference](docs/api_reference.md).
