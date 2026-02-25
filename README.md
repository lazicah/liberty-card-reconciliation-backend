# Liberty Card Reconciliation API

A FastAPI-based service for automated card transaction reconciliation, settlement analysis, and financial reporting.

## Features

- **Automated Reconciliation**: Processes card transactions from multiple channels (NIBSS, Interswitch, Parallex)
- **Settlement Analysis**: Matches transactions with settlement reports
- **Bank Statement Processing**: Analyzes bank statements and identifies discrepancies
- **AI-Powered Summaries**: Generates intelligent summaries using OpenAI
- **Google Sheets Integration**: Reads from and writes to Google Sheets
- **RESTful API**: Easy-to-use HTTP endpoints for all operations
- **Docker Support**: Containerized for easy deployment

## Architecture

```
liberty-card-reconciliation-backend/
├── main.py                          # FastAPI application entry point
├── config.py                        # Configuration settings
├── utils.py                         # Utility functions
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker configuration
├── docker-compose.yml              # Docker Compose configuration
├── models/
│   ├── __init__.py
│   └── schemas.py                  # Pydantic models
├── services/
│   ├── __init__.py
│   ├── google_sheets_service.py   # Google Sheets integration
│   ├── reconciliation_service.py  # Core business logic
│   └── ai_service.py              # OpenAI integration
└── outputs/
    └── metrics/                    # Generated metrics files
```

## Prerequisites

- Python 3.11+
- Google Cloud Service Account with Sheets API access
- OpenAI API key (optional, for AI summaries)
- Google Sheets with the following tabs:
  - CardTransaction
  - NIBSS SETT FROM NIBSS
  - ISW SETT REPORT
  - LIBERTYPAY_Pos_Acquired_Detail_
  - BANK STMT UNITY
  - BANK STMT PARALLEX

## Installation

### Option 1: Local Setup

1. **Clone the repository**
```bash
cd /Users/user/Documents/Personal\ Projects/liberty-card-reconciliation-backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your credentials
```

5. **Add Google Service Account JSON**
Place your `streamlit-analytics-488117-db0b145f8c2a.json` file in the project root.

6. **Run the application**
```bash
python main.py
# Or use uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Docker Setup

1. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your credentials
```

2. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

3. **View logs**
```bash
docker-compose logs -f
```

## API Documentation

Once the server is running, access:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Endpoints

### Health Check
```http
GET /health
```
Checks service status and dependency connections.

**Response:**
```json
{
  "status": "healthy",
  "message": "Service is running",
  "google_sheets_connected": true,
  "openai_configured": true
}
```

### Run Reconciliation
```http
POST /reconciliation/run
```
Executes the complete reconciliation process.

**Request Body:**
```json
{
  "run_date": "2026-02-07",  // Optional: YYYY-MM-DD format
  "days_offset": 18           // Optional: defaults to 18
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Reconciliation completed successfully",
  "run_date": "2026-02-07",
  "metrics": {
    "run_date": "2026-02-07",
    "total_revenue": 125000.50,
    "total_settlement": 120000.00,
    "total_settlement_charge_back": 500.00,
    "total_settlement_unsettled_claims": 4500.50,
    "total_bank_isw_unsettled_claims": 200.00,
    "total_bank_isw_charge_back": 100.00,
    "channels": {
      "NIBSS": {...},
      "INTERSWITCH": {...},
      "PARALLEX": {...},
      "ISW Bank": {...}
    }
  },
  "ai_summary": "Financial analysis summary...",
  "metrics_file_path": "outputs/metrics/metrics_2026-02-07.json"
}
```

### Get Metrics by Date
```http
GET /metrics/{run_date}
```
Retrieves metrics for a specific date.

**Example:**
```http
GET /metrics/2026-02-07
```

### Get Latest Metrics
```http
GET /metrics/latest
```
Retrieves the most recently generated metrics.

### Get Configuration
```http
GET /config
```
Returns current API configuration (non-sensitive values).

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google Sheets Configuration
SERVICE_ACCOUNT_FILE=streamlit-analytics-488117-db0b145f8c2a.json
SPREADSHEET_ID=1La0dpzzo2yZQTOe3DJk11uapbgF4kk2fqQ6fblck8TI

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
```

### Merchant IDs

The following merchant IDs are configured in `config.py`:
- **Interswitch Unity**: `2LBP87654321988`
- **NIBSS Unity**: `2215LA525653900`
- **NIBSS Parallex**: `210000000000000.0`

## Usage Examples

### Using cURL

**Run reconciliation for today - 18 days:**
```bash
curl -X POST http://localhost:8000/reconciliation/run \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Run reconciliation for specific date:**
```bash
curl -X POST http://localhost:8000/reconciliation/run \
  -H "Content-Type: application/json" \
  -d '{
    "run_date": "2026-02-07"
  }'
```

**Get metrics:**
```bash
curl http://localhost:8000/metrics/2026-02-07
```

### Using Python

```python
import requests

# Run reconciliation
response = requests.post(
    "http://localhost:8000/reconciliation/run",
    json={"run_date": "2026-02-07"}
)
result = response.json()
print(result["metrics"])

# Get latest metrics
response = requests.get("http://localhost:8000/metrics/latest")
metrics = response.json()
print(metrics)
```

## Reconciliation Process

The service performs the following operations:

1. **Data Loading**: Fetches all required sheets from Google Sheets
2. **Data Preparation**: Converts dates and filters by run date
3. **Transaction Processing**:
   - Filters successful transactions (host_resp_code = 0)
   - Separates by merchant ID (PAYBOX, Interswitch, NIBSS Unity, NIBSS Parallex)
   - Calculates fees, costs, and gross profit
4. **Settlement Reconciliation**:
   - Matches transactions with settlement reports
   - Identifies unsettled claims
   - Flags chargebacks
5. **Bank Statement Analysis**:
   - Processes Unity and Parallex bank statements
   - Extracts transaction details
   - Identifies discrepancies
6. **Metrics Generation**: Creates comprehensive financial metrics
7. **AI Summary**: Generates intelligent summary using OpenAI
8. **Data Export**: Saves results to Google Sheets and local JSON

## Output

### Metrics File
Metrics are saved to `outputs/metrics/metrics_YYYY-MM-DD.json` with the following structure:

```json
{
  "run_date": "2026-02-07",
  "total_revenue": 125000.50,
  "total_settlement": 120000.00,
  "channels": {
    "NIBSS": {
      "revenue": 50000.00,
      "settlement": 49500.00,
      "charge_back": 200.00,
      "unsettled_claim": 300.00
    },
    ...
  }
}
```

### Google Sheets Output
The following sheets are created/updated:
- `paybox_trans_df`: Aggregated PAYBOX transactions
- `nibss_parallex`: NIBSS Parallex reconciliation
- `nibss_unity`: NIBSS Unity reconciliation
- `nibss_reconciliation`: NIBSS discrepancies
- `isw_reconciliation`: Interswitch discrepancies
- `parallex_reconciliation`: Parallex discrepancies
- `isw_bank_reconciliation`: ISW bank discrepancies
- `nerf_nibss_b_credit`: NERF NIBSS bank credits
- `being_nibss_summary`: BEING NIBSS summary
- `cb`: Chargebacks
- `tof_df`: Terminal owner fees
- `ds`: Daily sweeps
- `AI Summary`: AI-generated summaries

## Deployment

### Production Deployment

1. **Update environment variables** for production
2. **Disable debug mode**: Set `API_RELOAD=false`
3. **Use production WSGI server**: Already configured with Uvicorn
4. **Set up reverse proxy** (e.g., Nginx) for SSL/TLS
5. **Configure monitoring** and logging

### Docker Deployment

```bash
# Build image
docker build -t liberty-card-reconciliation:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/streamlit-analytics-488117-db0b145f8c2a.json:/app/streamlit-analytics-488117-db0b145f8c2a.json \
  --name liberty-card-api \
  liberty-card-reconciliation:latest
```

### Cloud Deployment

**Google Cloud Run:**
```bash
gcloud run deploy liberty-card-reconciliation \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

**AWS ECS / Fargate / Heroku:**
Follow respective platform documentation for containerized applications.

## Troubleshooting

### Common Issues

**Google Sheets Connection Failed**
- Verify service account JSON file exists
- Check spreadsheet ID in `.env`
- Ensure service account has access to the spreadsheet

**OpenAI API Errors**
- Verify API key is correct
- Check API quota/limits
- Ensure billing is set up

**Date Parsing Errors**
- Use YYYY-MM-DD format for dates
- Ensure Google Sheets have proper date formatting

**Empty DataFrames**
- Check if data exists for the specified date
- Verify merchant IDs match data in sheets

## Development

### Running Tests
```bash
# Install dev dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Formatting
```bash
pip install black flake8
black .
flake8 .
```

## License

This project is proprietary to Liberty Card Services.

## Support

For issues or questions, please contact the development team.

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request
4. Ensure all tests pass

---

**Version**: 1.0.0  
**Last Updated**: February 2026
