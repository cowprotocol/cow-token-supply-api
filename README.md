# CoW Protocol Supply API

A Flask-based API service that provides token supply information about CoW Protocol token supply metrics, including:

- Total supply
- Circulating supply

## Features

- RESTful API endpoint for supply information
- Support for multiple vesting schedules with different vesting modules
- Supports adding new Treasuries on any chains
- Supports adding new Vesting Models and new Vesting Schedules

## API Endpoints

### GET /supply

Returns the total and circulating supply of CoW Protocol tokens.

Example response:
json
{
"total": "1000000000000000000000000",
"circulating": "750000000000000000000000"
}

## Setup

### Prerequisites

- Python 3.11+
- Docker (optional)

### Environment Variables

Create a `.env` file with:

```
ETH_RPC_URL=<your-ethereum-rpc-url>
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
