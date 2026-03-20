# IMC Prosperity 4 Backtester

A local backtester for [IMC Prosperity 4](https://prosperity.imc.com/) trading algorithms. Test your algo against real historical market data before submitting.

Forked from [jmerle/imc-prosperity-3-backtester](https://github.com/jmerle/imc-prosperity-3-backtester) by [Jasper van Merle](https://github.com/jmerle). Credit to him for the original design and implementation.

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```sh
git clone <this repo>
cd imc-prosperity-4-backtester
uv venv && source .venv/bin/activate
uv sync
```

## Usage

```sh
# Backtest on all days from round 0
python -m prosperity4bt <path to algorithm file> 0

# Backtest on round 0 day -1
python -m prosperity4bt <path to algorithm file> 0--1

# Backtest on round 0 day -2 and day -1
python -m prosperity4bt <path to algorithm file> 0--2 0--1
```

### Options

```sh
# Merge profit and loss across days (cumulative P&L)
python -m prosperity4bt algo.py 0 --merge-pnl

# Write output log to a specific file (default: backtests/<timestamp>.log)
python -m prosperity4bt algo.py 0 --out my_run.log

# Skip saving the output log entirely
python -m prosperity4bt algo.py 0 --no-out

# Print trader output to stdout in real time (useful for debugging)
python -m prosperity4bt algo.py 0 --print

# Use a custom data directory instead of the bundled data
python -m prosperity4bt algo.py 0 --data path/to/data

# Suppress progress bars
python -m prosperity4bt algo.py 0 --no-progress

# Preserve original timestamps across days instead of normalizing them
python -m prosperity4bt algo.py 0 --original-timestamps

# Control how orders are matched against market trades (default: all)
python -m prosperity4bt algo.py 0 --match-trades all    # match trades at prices equal to or worse than your quotes
python -m prosperity4bt algo.py 0 --match-trades worse  # match trades only at prices strictly worse than your quotes
python -m prosperity4bt algo.py 0 --match-trades none   # do not match market trades against orders
```

Output logs are saved to `backtests/<timestamp>.log` by default.

## Algorithm Interface

Your algorithm file must expose a `Trader` class with a `run` method:

```python
from prosperity4bt.datamodel import TradingState, Order

class Trader:
    def run(self, state: TradingState):
        orders = {}  # dict[str, list[Order]]
        conversions = 0
        trader_data = ""
        return orders, conversions, trader_data
```

## Order Matching

Orders are matched first against the order book, then against market trades (if any volume remains).

- **Order depth matching**: your order fills against resting liquidity at prices equal to or better than yours.
- **Market trade matching**: the backtester assumes each market trade's counterparty is willing to trade with you at the trade's price and volume. Your order fills at *your* quoted price, not the market trade price (e.g. a sell order at 9 fills at 9 even if the market trade was at 10).

Position limits are enforced before matching. If filling all your orders for a product would breach its limit, all orders for that product are canceled.

## Data

| Round | Days | Products |
|-------|------|----------|
| 0 | -2, -1 | EMERALDS, TOMATOES |

More rounds will be added as data becomes available.

### Custom Data

Pass `--data <directory>` to use your own data. The directory must follow this structure:

```
data/
└── round0/
    ├── prices_round_0_day_-1.csv
    └── trades_round_0_day_-1.csv
```

Prices and trades CSVs are semicolon-delimited. Observations CSVs (for products that require them) are comma-delimited. See `prosperity4bt/resources/` for examples.

## Environment Variables

During a backtest, two environment variables are set:
- `prosperity4bt_ROUND` — the round number
- `prosperity4bt_DAY` — the day number

These do not exist in the official submission environment, so make sure your submitted code does not depend on them.
