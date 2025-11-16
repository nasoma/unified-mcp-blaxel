# UnifiedMCP - Upwork Payment & Airtime Transfer Assistant

A Model Context Protocol (MCP) server designed to assist with Upwork payment calculations and airtime transfers in Kenya. This server provides tools for currency conversion, payment planning, and direct airtime loading via Africa's Talking API.

## Features

- **Upwork Payment Conversion**: Convert USD payments to Kenyan Shillings (KES) accounting for Upwork fees and exchange rates
- **Gross Payment Calculation**: Calculate the gross USD amount needed to achieve a target KES amount
- **Airtime Transfer**: Send airtime directly to Kenyan phone numbers via Africa's Talking
- **Account Balance Check**: Check your airtime account balance
- **Email Notifications**: Send HTML emails using AWS SES

## Technology Stack

- **Python**: 3.12+
- **Blaxel**: Framework for MCP (Multi-Client Protocol) server functionality
- **Africa's Talking API**: For airtime transfers and account management
- **AWS SES**: For sending emails
- **Boto3**: AWS SDK for Python

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd unified-mcp-blaxel/server
   ```

2. Install dependencies using uv (recommended) or pip:
   ```bash
   # Using uv (as specified in pyproject.toml)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. Set up environment variables as described in the Configuration section.

## Configuration

Create a `.env` file in the server directory with the following environment variables:

```env
# Upwork Configuration
EXCHANGE_RATE=120.0        # KES to USD exchange rate (e.g., 1 USD = 120 KES)
UPWORK_FEE=0.99           # Upwork fee amount (default: 0.99)
UPWORK_RATE=0.884         # Upwork rate after fees (default: 0.884)
currency_code=KES         # Default currency (default: KES)
country=kenya             # Default country (default: kenya)

# Africa's Talking Configuration
username=your_at_username
api_key=your_at_api_key
SENDER=your_email@example.com
SENDER_NAME=Your Name

# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
REGION=your_aws_region    # e.g., us-east-1

# Server Configuration
BL_SERVER_HOST=0.0.0.0
BL_SERVER_PORT=80
```

## Available Tools

### 1. Convert to KES (`convert_to_kes`)
Convert Upwork payment amounts from USD to Kenyan Shillings, accounting for Upwork fees and exchange rates.

- **Input**: Payment amount(s) in USD (single or comma-separated)
- **Output**: Formatted conversion showing USD payout and equivalent KES amount

### 2. Calculate Gross Needed (`calculate_gross_needed`)
Calculate the gross USD payment needed to receive a target KES amount.

- **Input**: Target amount in KES (e.g., "9000", "9,000", "I need 9,000")
- **Output**: Gross USD payment needed from Upwork to achieve target KES

### 3. Send Email (`send_email`)
Send HTML emails using AWS SES.

- **Input**: recipient (email address), subject (email subject), body_html (HTML content)
- **Output**: Confirmation of email sent or error message

### 4. Check Balance (`check_balance`)
Check your Africa's Talking account balance.

- **Input**: None
- **Output**: Account balance information

### 5. Load Airtime (`load_airtime`)
Send airtime to a Kenyan phone number.

- **Input**: phone_number, amount (5-10,000 KES), currency_code (KES)
- **Output**: Confirmation of airtime sent or error message

### 6. Airtime Transfer Assistant (`airtime_transfer_assistant`)
Provides guidance on planning airtime transfers, best practices, and troubleshooting.

## Configuration Files

### blaxel.toml
This project is configured as a Blaxel function:

```toml
type = "function"
name = "unifiedMCP-on-Blaxel"

[runtime]
transport = "http-stream"

[entrypoint]
prod = ".venv/bin/python3 src/server.py"
dev = "npx nodemon --exec uv run python src/server.py"
```

### pyproject.toml
Defines project dependencies and metadata:

```toml
[project]
name = "unified-mcp"
version = "0.1.0"
description = ""
requires-python = ">=3.12"
dependencies = [
  "africastalking>=2.0.1",
  "blaxel[core,telemetry]==0.2.23",
  "boto3>=1.40.74",
  "mcp[cli]>=1.21.1",
  "python-dotenv>=1.1.0",
  "pytz>=2025.2",
]
```

## Usage

The server runs as an MCP (Multi-Client Protocol) server. To start the server:

```bash
# Using uv (recommended)
uv run python src/server.py

# Or using the development configuration
npx nodemon --exec uv run python src/server.py
```

The server will start on the configured host and port (default: 0.0.0.0:80).

## Development

This project uses uv as the package manager. To work on this project:

1. Install uv if you haven't already:
   ```bash
   pip install uv
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run the server in development mode:
   ```bash
   uv run python src/server.py
   ```

## Dependencies

- **africastalking**: 2.0.1 - Africa's Talking Python SDK
- **blaxel**: 0.2.23 - Blaxel framework with core and telemetry features
- **boto3**: 1.40.74 - AWS SDK for Python
- **mcp**: 1.21.1 - Multi-Client Protocol CLI tools
- **python-dotenv**: 1.1.0 - Environment variable management
- **pytz**: 2025.2 - Timezone handling

## License

This project is licensed under the terms specified in the LICENSE file.