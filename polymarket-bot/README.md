# polybot

Automated trading bot for Polymarket US (CFTC-regulated, QCX LLC). v1 runs a
YES/NO intra-market arbitrage scanner against the official `polymarket-us`
Python SDK. Phase 0 ships only a connection test.

This is not the international Polymarket. If you find yourself installing
`py-clob-client`, stop.

## Phase 0 checklist

Do each step in order.

### 1. Generate API credentials

1. Finish KYC on polymarket.us if you have not already.
2. Go to https://polymarket.us/developer.
3. Create a new Ed25519 API key pair. You will get a `keyId` (UUID) and a
   `secretKey` (base64-encoded Ed25519 private key).
4. Save both somewhere safe. The secret key is shown once.

### 2. Populate `.env`

From the project root:

```
cp .env.example .env
```

Open `.env` and fill in:

- `POLYMARKET_KEY_ID` = the UUID from step 1
- `POLYMARKET_SECRET_KEY` = the base64 secret key from step 1
- `ANTHROPIC_API_KEY` = your Anthropic key (not used in Phase 0)

The `.env` file is gitignored. Verify:

```
git check-ignore -v .env
```

### 3. Install dependencies

Use a virtualenv. Python 3.11+ required.

```
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Or with the pyproject:

```
pip install -e ".[dev]"
```

### 4. Run the connection test

```
python scripts/test_connection.py
```

### 5. Expected output on success

```
Authenticating to Polymarket US...

--- Account balance ---
<balance object from SDK, should show your USDC>

--- Open positions ---
(none)        # or a list if you have open positions

--- Open orders ---
(none)        # or a list if you have open orders

OK. Connection verified. No trades placed.
```

Non-zero exit means something failed. Read the error and fix before moving on.

### 6. Run the unit tests

```
pytest
```

All tests should pass. These cover fee math, edge math, and risk checks.
No network calls.

## What Phase 0 does not do

- No trading. No orders placed. No orders cancelled.
- No WebSocket subscription. That lands in Phase 1.
- No Anthropic call. That lands in Phase 1's sanity layer.

## Fee math reference

Polymarket US publishes a coefficient-based fee schedule effective 2026-04-03.
Per-contract fee scales with `p * (1 - p)`, which makes fees lowest at price
extremes and highest at $0.50.

```
taker_fee_per_contract  = theta_taker  * p * (1 - p) * 2
maker_rebate_per_contract = theta_maker * p * (1 - p) * 2
```

Current coefficients (see `config/default.toml`):

- `theta_taker = 0.05`
- `theta_maker = 0.0125` (25% of taker)
- Temporary taker rebate = 50% of taker fee, expires 2026-04-30. Set
  `fees.taker_rebate_fraction = 0.0` after that.

At p = 0.50, taker fee per 100 contracts = $1.25. At p = 0.10, it is $0.90.

## Kill switch

Create a file named `STOP` at the project root to halt trading on the next
loop iteration.

```
touch STOP      # halt
rm STOP         # resume
```

The `STOP` file is gitignored. Do not track it.

## Directory layout

```
polymarket-bot/
├── config/default.toml       caps, limits, fee coefficients
├── src/polybot/              package code
├── scripts/test_connection.py  Phase 0 connection check
├── tests/                    unit tests for pure logic
└── data/                     sqlite db (gitignored)
```

## Safety invariants

- `mode.dry_run = true` until Phase 3.
- `mode.autonomous = false` always, until Phase 4 criteria are met.
- Credentials never leave `.env`. Never log them.
- All trades flow through `polybot.risk.check_trade` before execution.
- WebSockets for real-time data. REST only for setup and one-off queries.
  The REST rate limit is 60 requests per minute.
