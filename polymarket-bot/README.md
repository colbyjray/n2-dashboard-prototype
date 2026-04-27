# polybot

Automated trading bot for Polymarket US (CFTC-regulated, QCX LLC). v1 runs a
YES/NO intra-market arbitrage scanner against the official `polymarket-us`
Python SDK. Phase 0 ships a local web dashboard for setup, status, and
control. The bot's strategy code lands in Phase 1.

This is not the international Polymarket. If you find yourself installing
`py-clob-client`, stop.

## Quickstart (the only steps you need)

### 1. Generate API credentials

1. Finish KYC on polymarket.us if you have not already.
2. Visit https://polymarket.us/developer.
3. Create a new Ed25519 API key pair. Copy the `keyId` (UUID) and the
   `secretKey` (base64 Ed25519 private key). The secret is shown once.

### 2. Install dependencies

In a terminal, in this folder:

```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Launch the dashboard

```
python scripts/dashboard.py
```

The terminal prints a URL like:

```
http://127.0.0.1:8765/?token=AbCd...
```

Click it once. Your browser stores the token. From then on you can use
`http://127.0.0.1:8765` directly.

### 4. Save your keys in the dashboard

Open the **Setup** page. Paste your Polymarket `keyId`, `secretKey`, and
your Anthropic API key. Click **Save to keychain**. Click **Test**.

If you see your account balance appear, you're done with setup.

### 5. Verify the unit tests

```
pytest
```

All 18 tests should pass.

## Where do my keys live?

In your operating system's secure credential store, via the `keyring`
library:

- macOS: login Keychain (Keychain Access app)
- Linux: Secret Service / GNOME Keyring
- Windows: Credential Manager

Keys are never written to a file in this project. There is no `.env` step.
The `.env.example` file in the repo is left as a fallback option for users
who prefer environment-variable-based config; the dashboard does not use it.

## What the dashboard shows

- **Setup**: paste keys, test connection, clear keys.
- **Status**: live balance, open positions, open orders. Big kill switch.
  Auto-refreshes every 5 seconds.
- **Markets** (Phase 1): top-N markets by liquidity with computed arb edge.
- **Decisions** (Phase 1): every arb candidate the scanner logged with
  edge, sanity verdict, and outcome.
- **P&L** (Phase 2): realized and unrealized profit, daily breakdown, fee
  drag, distance to daily-loss cap.
- **Logs**: recent log lines from `logs/polybot.log`.

The dashboard binds to `127.0.0.1:8765` only. It cannot be reached from your
network or the public internet.

## Kill switch

Click **Engage** on the Status page, or run:

```
touch STOP
```

Either creates a `STOP` file at the project root. The bot halts on its next
loop iteration. Click **Release** or `rm STOP` to resume.

## Fee math reference

Polymarket US publishes a coefficient-based fee schedule effective
2026-04-03. Per-contract fee scales with `p * (1 - p)`.

```
taker_fee_per_contract  = theta_taker  * p * (1 - p)
maker_rebate_per_contract = theta_maker * p * (1 - p)
```

Current coefficients (see `config/default.toml`):

- `theta_taker = 0.05`
- `theta_maker = 0.0125` (25% of taker)
- Temporary taker rebate = 50% of taker fee, expires 2026-04-30. Set
  `fees.taker_rebate_fraction = 0.0` after that.

At p = 0.50, taker fee per 100 contracts = $1.25. At p = 0.10, it is $0.45.

## Directory layout

```
polymarket-bot/
├── config/default.toml            caps, limits, fee coefficients
├── src/polybot/
│   ├── secrets.py                 keychain-backed secret storage
│   ├── client.py                  thin wrapper around polymarket-us SDK
│   ├── fees.py, edge.py, risk.py  pure logic (unit tested)
│   ├── storage.py, journal.py     SQLite schema + writers
│   ├── strategies/arb.py          Phase 1 scanner
│   └── dashboard/                 FastAPI app, templates, static
├── scripts/
│   ├── dashboard.py               main entry point
│   └── test_connection.py         CLI fallback (no dashboard)
├── tests/                         unit tests for pure logic
└── data/                          sqlite db (gitignored)
```

## Safety invariants

- `mode.dry_run = true` until Phase 3.
- `mode.autonomous = false` always, until Phase 4 criteria are met.
- Keys live only in your OS keychain. Never logged, never written to disk.
- Every trade flows through `polybot.risk.check_trade` before execution.
- WebSockets for real-time data. REST only for setup and one-off queries.
  The REST rate limit is 60 requests per minute.
- Dashboard binds to `127.0.0.1` only. Token auth required.
