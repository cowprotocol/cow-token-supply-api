# CoW Protocol Supply API

A Flask-based API service that provides token supply information about CoW Protocol token supply metrics, including:

- Total supply
- Circulating supply
- Breakdown of non-circulating components (treasury, locked/vesting, solver bonds, staked)

## Methodology

Circulating supply is defined as the portion of `totalSupply()` that is freely tradable on the open market. It is computed as:

```
circulating = total - treasury - locked - bonds - staked
```

Where:

- **treasury** — COW held in CoW DAO controlled wallets across all supported chains (currently Ethereum mainnet and Gnosis Chain). Bridged COW on Gnosis Chain is excluded from `total` to avoid double-counting but treasury balances on Gnosis Chain reduce circulating supply.
- **locked** — COW still vesting under the TGE schedules (vCOW + GNO DAO allocation).
- **bonds** — COW posted by solvers as bond collateral. Not slashable on-chain but committed against misbehaviour and therefore not freely tradable.
- **staked** — COW locked under the upcoming staking program. Zero until a staking contract address is added to `STAKING_CONTRACTS` in `src/cfg.py`.

This methodology implements the Core Team update described in [CoW DAO's Path to Value Distribution: Core Team view](https://forum.cow.fi/t/cow-daos-path-to-value-distribution-core-team-view/3454).

## Features

- RESTful API endpoint for supply information
- Support for multiple vesting schedules with different vesting modules
- Supports adding new Treasuries on any chains
- Supports adding new Vesting Models and new Vesting Schedules
- Supports adding solver bond wallets and staking contracts as separate non-circulating buckets

## API Endpoints

### GET /supply

Returns the total and circulating supply of CoW Protocol tokens plus a breakdown of non-circulating components.

Example response:

```json
{
  "total": "1000000000",
  "circulating": "750000000",
  "treasury": "200000000",
  "locked": "40000000",
  "bonds": "10000000",
  "staked": "0"
}
```

The `q` query parameter restricts the response to a single scalar: `total`, `circulating`, `treasury`, `locked`, `bonds`, or `staked`. Example: `GET /supply?q=circulating`.

## Setup

### Prerequisites

- Python 3.11+
- Docker (optional)

### Environment Variables

Create a `.env` file with:

```
ETH_RPC_URL=<your-ethereum-rpc-url>
GNOSIS_RPC_URL=<your-gnosis-chain-rpc-url>
```

### Local Development

1. Clone the repository
2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the development server:

```bash
python src/main.py
```

### Using Docker

Build and run with Docker:

```bash
docker build -t cow-supply-api .
docker run -p 8080:8080 --env-file .env cow-supply-api
```

### Development Container

This project includes VS Code devcontainer configuration for a consistent development environment:

1. Install VS Code and Docker
2. Open the project in VS Code
3. Click "Reopen in Container" when prompted

## Project Structure

- `src/`
  - `main.py` - Flask application and API endpoints
  - `supply_handlers.py` - Supply calculation logic
  - `vesting.py` - Vesting schedule implementations
  - `rpc.py` - Blockchain RPC interaction
  - `cfg.py` - Configuration and constants
  - `models.py` - Data models
