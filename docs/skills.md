# Longbridge Tools Skills

This document describes the available skills for interacting with the Longbridge OpenAPI.
These skills are wrapped around the `longport` SDK to provide simplified, task-oriented interfaces.

## Rate Limits

The following rate limits apply to the Longbridge OpenAPI:

- **Quote API**: Max 10 calls/sec, 5 concurrent requests.
- **Trade API**: Max 30 calls/30 sec.
- **WebSocket**: Max 500 subscriptions per connection.

For detailed API parameter definitions and return values, please refer to the [API Reference](api_reference.md).

## Installation

```bash
cd longbridge_tools
pip install -e .
```

## Configuration

You can configure the tools using a `config.yaml` file or environment variables.

### 1. Using Configuration File (Recommended)

Create a `config.yaml` file in your working directory (or copy from `config.yaml.example`):

```yaml
app_key: "your_app_key"
app_secret: "your_app_secret"
access_token: "your_access_token"
```

Then initialize the skills:

```python
# Automatically loads from config.yaml in current directory
skill = QuoteSkill()

# Or specify a custom path
skill = QuoteSkill(config="path/to/my_config.yaml")
```

### 2. Using Environment Variables

Set the following environment variables:

```bash
export LONGBRIDGE_APP_KEY="your_app_key"
export LONGBRIDGE_APP_SECRET="your_app_secret"
export LONGBRIDGE_ACCESS_TOKEN="your_access_token"
```

## Available Skills

### 1. QuoteSkill

Used for retrieving market data.

**Methods:**

- `get_quote(symbols: List[str]) -> List[Quote]`: Get real-time quotes.
- `get_depth(symbol: str) -> Depth`: Get market depth (L2).
- `get_brokers(symbol: str) -> Brokers`: Get broker queue (HK).
- `get_candlesticks(symbol: str, period: str, count: int, adjust_type: str = "no_adjust") -> List[Candlestick]`: Get historical price data.

**Example:**

```python
from longbridge_tools import QuoteSkill

skill = QuoteSkill()
quotes = skill.get_quote(["700.HK", "AAPL.US"])
for q in quotes:
    print(f"{q.symbol}: {q.last_done}")

history = skill.get_candlesticks("700.HK", "day", 100)
print(f"Historical data count: {len(history)}")
```

### 2. TradeSkill

Used for order management.

**Methods:**

- `submit_order(symbol: str, side: str, order_type: str, quantity: int, price: float = None) -> str`: Place an order. Returns `order_id`.
- `cancel_order(order_id: str)`: Cancel an order.
- `get_orders(symbol: str = None) -> List[Order]`: Get today's orders.
- `get_history_orders(symbol: str = None, start: str, end: str) -> List[Order]`: Get historical orders.

**Example:**

```python
from longbridge_tools import TradeSkill

skill = TradeSkill()

# Place a limit buy order
order_id = skill.submit_order("700.HK", "buy", "lo", 100, 300.0)
print(f"Placed order: {order_id}")

# Cancel it
skill.cancel_order(order_id)
```

### 3. AssetSkill

Used for account information.

**Methods:**

- `get_account_balance(currency: str = None) -> AccountBalance`: Get cash balance.
- `get_stock_positions(symbol: str = None) -> List[Position]`: Get stock holdings.
- `get_cash_flow(start: str, end: str) -> List[CashFlow]`: Get cash flow history.

**Example:**

```python
from longbridge_tools import AssetSkill

skill = AssetSkill()
balance = skill.get_account_balance("HKD")
print(f"Available Cash (HKD): {balance.cash_available}")

positions = skill.get_stock_positions()
for p in positions:
    print(f"{p.symbol}: {p.quantity} shares")
```

### 4. AuthSkill

Used for authentication management, including token refresh.

**Methods:**

- `refresh_token(expired_at: str) -> Dict`: Refresh the access token. `expired_at` must be in ISO8601 format (e.g., "2023-04-14T12:13:57.859Z").
- `update_config_file(new_token: str, config_path: str = "config.yaml")`: Update the configuration file with the new token.

**Example:**

```python
from longbridge_tools import AuthSkill

skill = AuthSkill()

# Refresh token
# You typically get 'expired_at' from your current token info or a previous response
new_token_info = skill.refresh_token("2023-05-14T12:13:57.859Z")
print(f"New Token: {new_token_info['token']}")

# Update config.yaml automatically
skill.update_config_file(new_token_info['token'])
```

## Testing

Run the tests using `pytest`:

```bash
# Run unit tests (mocks)
pytest tests/test_skills.py

# Run integration tests (requires env vars)
pytest tests/integration_test.py
```

## Notes

- **Environment**: Use `AppConfig` to load credentials from environment variables securely.

