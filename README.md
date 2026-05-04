# Mox Buy Me A Coffee

A Vyper smart contract that lets people send ETH as "coffee" donations, with a USD minimum enforced via a Chainlink price feed. Built as part of the [Cyfrin Updraft Intermediate Python and Vyper](https://updraft.cyfrin.io/courses/intermediate-python-vyper-smart-contract-development) course using the [Moccasin](https://github.com/Cyfrin/moccasin) framework.

## What it does

- Accepts ETH donations via a `fund()` function with a minimum of $5 USD
- Converts the incoming ETH to USD using a Chainlink AggregatorV3 price feed
- Tracks each funder and the amount they sent
- Lets the contract owner withdraw the full balance via `withdraw()`
- Resets funder balances on withdrawal

## Tech stack

- **Vyper** `0.4.3` — contract language
- **Moccasin** (`mox`) — Python-based smart contract development framework
- **Titanoboa** — Vyper interpreter and testing engine
- **anvil** — local EVM testnet
- **anvil-zksync** + **zkvyper** — local zkSync Era testnet (optional)
- **uv** — Python project/dependency manager

## Project layout

```
.
├── src/
│   ├── buy_me_a_coffee.vy        # main contract
│   ├── get_price_module.vy       # ETH→USD conversion module
│   ├── interfaces/
│   │   └── AggregatorV3Interface.vyi
│   └── mocks/
│       └── mock_v3_aggregator.vy # local price-feed mock
├── script/
│   ├── deploy.py
│   ├── deploy_mocks.py
│   └── withdraw.py
├── tests/
│   ├── unit/
│   ├── staging/
│   └── conftest.py
└── moccasin.toml
```

## Setup

```bash
# install moccasin via uv
uv tool install moccasin

# install project deps
mox install
```

Make sure `anvil` is on your PATH (`anvil --version`). For zkSync, also install `anvil-zksync` and `zkvyper`.

Create a `.env` with your Sepolia RPC URL if you plan to deploy to testnet:

```
SEPOLIA_RPC_URL=https://...
```

## Common commands

```bash
# run the unit tests on the default pyevm network
mox test

# spin up anvil in a separate terminal, then deploy
anvil
mox run deploy --network anvil

# withdraw from a deployed contract on anvil
mox run withdraw --network anvil

# deploy to sepolia (requires .env + funded account)
mox run deploy --network sepolia
```

## Networks

Configured in `moccasin.toml`:

| Name           | Description                            |
| -------------- | -------------------------------------- |
| `pyevm`        | default in-memory EVM (used for tests) |
| `anvil`        | local foundry anvil node               |
| `sepolia`      | Ethereum Sepolia testnet               |
| `eravm`        | local zkSync Era node (anvil-zksync)   |
| `zksync-local` | alternative local zkSync setup         |

## Known issues

**`mox test --network eravm` may fail** with a `zkvyper` assembler error like `error: identifier expected ... internal_0__get_eth_to_usd_rate_src/interfaces/AggregatorV3Interface.vyi_...`. This is a known compatibility quirk between current `zkvyper` (1.5.x) and Vyper 0.4.x interface imports — the compiler embeds the interface's file path into an internal assembly symbol, and the forward slashes break the assembler. EVM tests are unaffected.

## Course

Part of the [Cyfrin Updraft Vyper Developer Career Path](https://updraft.cyfrin.io). Course repo: [Cyfrin/mox-buy-me-a-coffee-cu](https://github.com/Cyfrin/mox-buy-me-a-coffee-cu).

## Disclaimer

This contract is for learning purposes only. It has not been audited and should not be used with real funds in production.
