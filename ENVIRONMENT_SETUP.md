# Setup Guide - Environment Variables

This guide explains how to configure the Liberty Card Reconciliation API using environment variables for both local development and cloud deployment.

## Quick Start

### 1. Local Development (Using .env file)

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your credentials
# You can use any of the three methods below
```

### 2. Production Deployment (Using environment variables)

No `.env` file needed. Set environment variables directly in your platform.

---

## Three Methods to Configure Google Credentials

### Method 1: Base64 Encoded JSON (⭐ RECOMMENDED)

**Best for**: Production, Render, Docker, cloud deployments

**Steps**:

1. **Encode your JSON credentials**:
   ```bash
   # On macOS/Linux
   base64 -i streamlit-analytics-488117-db0b145f8c2a.json
   
   # Or copy to clipboard
   base64 -i streamlit-analytics-488117-db0b145f8c2a.json | pbcopy
   ```

2. **For local development** - Add to `.env`:
   ```bash
   GOOGLE_CREDENTIALS_BASE64=JXsidHlwZSI6InNlcnZpY2VfYWNjb3VudCIsInByb2plY3RfaWQi...
   ```

3. **For Render/cloud** - Add environment variable in service settings:
   ```
   Key: GOOGLE_CREDENTIALS_BASE64
   Value: JXsidHlwZSI6InNlcnZpY2VfYWNjb3VudCIsInByb2plY3RfaWQi...
   ```

**Why it's best**:
- ✅ Doesn't commit sensitive files to git
- ✅ Easy to rotate credentials
- ✅ Works with CI/CD pipelines
- ✅ Portable across platforms

---

### Method 2: JSON String (Alternative)

**Best for**: Simple setups, testing

**Steps**:

1. **Copy your JSON file content**:
   ```bash
   cat streamlit-analytics-488117-db0b145f8c2a.json | tr -d '\n'
   ```

2. **Add to `.env`**:
   ```bash
   GOOGLE_CREDENTIALS_JSON={"type":"service_account","project_id":"...","key_id":"..."}
   ```

**Note**: This is harder to read and manage for large JSON files.

---

### Method 3: File Path (Development Only)

**Best for**: Local development only

**Steps**:

1. **Place JSON file in project root**:
   ```bash
   cp streamlit-analytics-488117-db0b145f8c2a.json ./
   ```

2. **Add to `.env`**:
   ```bash
   SERVICE_ACCOUNT_FILE=streamlit-analytics-488117-db0b145f8c2a.json
   ```

**Important**: 
- ⚠️ DO NOT use this in production
- ⚠️ File is git-ignored (won't commit)
- ⚠️ Won't work on Render/cloud platforms without the file

---

## Setup Instructions by Platform

### Local Development (macOS/Linux/Windows)

1. **Create .env file**:
   ```bash
   cp .env.example .env
   ```

2. **Choose a method and add credentials**:
   ```bash
   # Method 1 (Base64) - RECOMMENDED
   GOOGLE_CREDENTIALS_BASE64=your_base64_string_here
   
   # Method 2 (JSON string) - Alternative
   # GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
   
   # Method 3 (File path) - Local only
   # SERVICE_ACCOUNT_FILE=streamlit-analytics-488117-db0b145f8c2a.json
   ```

3. **Add other variables**:
   ```bash
   OPENAI_API_KEY=your_api_key_here
   SPREADSHEET_ID=1La0dpzzo2yZQTOe3DJk11uapbgF4kk2fqQ6fblck8TI
   API_HOST=0.0.0.0
   API_PORT=8000
   API_RELOAD=true
   ```

4. **Run the API**:
   ```bash
   python main.py
   # Or
   ./start.sh
   ```

---

### Render Deployment

**Step 1: Prepare Your GitHub Repository**

```bash
# Make sure sensitive files are ignored
git add .env.example
git add .gitignore
git commit -m "Add environment configuration template"
git push
```

**Step 2: Encode Your Credentials**

```bash
# On your local machine
base64 -i streamlit-analytics-488117-db0b145f8c2a.json | pbcopy
# Output is now in clipboard
```

**Step 3: Create Service on Render**

1. Go to [render.com](https://render.com)
2. Create new "Web Service"
3. Connect your GitHub repository
4. Choose:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Step 4: Add Environment Variables**

1. In Render service settings, click "Environment"
2. Add these variables:

| Key | Value |
|-----|-------|
| `GOOGLE_CREDENTIALS_BASE64` | (paste your base64 string) |
| `OPENAI_API_KEY` | (your OpenAI API key) |
| `SPREADSHEET_ID` | `1La0dpzzo2yZQTOe3DJk11uapbgF4kk2fqQ6fblck8TI` |
| `API_RELOAD` | `false` |

**Step 5: Deploy**

1. Render will automatically deploy when you push to GitHub
2. Check deployment logs for errors
3. Test health endpoint: `https://your-render-url.onrender.com/health`

---

### Docker / Docker Compose

**Using Method 1 (Base64 - Recommended)**:

```bash
# 1. Create .env file with Base64 credentials
cp .env.example .env
# Edit .env and add GOOGLE_CREDENTIALS_BASE64

# 2. Run Docker Compose
docker-compose up -d

# 3. Check logs
docker-compose logs -f
```

**Using environment variables directly**:

```bash
docker run -d \
  -p 8000:8000 \
  -e GOOGLE_CREDENTIALS_BASE64="your_base64_string" \
  -e OPENAI_API_KEY="your_key" \
  -e SPREADSHEET_ID="your_sheet_id" \
  liberty-card-reconciliation:latest
```

---

### AWS / ECS / Fargate

Use AWS Secrets Manager for sensitive data:

```bash
# Store Base64 credentials in Secrets Manager
aws secretsmanager create-secret \
  --name liberty-google-credentials \
  --secret-string "your_base64_string"

# Reference in ECS task definition
{
  "environment": [
    {
      "name": "GOOGLE_CREDENTIALS_BASE64",
      "valueFrom": "arn:aws:secretsmanager:region:account:secret:liberty-google-credentials"
    }
  ]
}
```

---

### Heroku

```bash
# Set environment variables
heroku config:set -a your-app-name \
  GOOGLE_CREDENTIALS_BASE64="your_base64_string" \
  OPENAI_API_KEY="your_key"

# Verify
heroku config -a your-app-name
```

---

## Credential Priority Order

The application checks credentials in this order:

1. **GOOGLE_CREDENTIALS_BASE64** (highest priority)
   - Used first if set
   - Best for production

2. **GOOGLE_CREDENTIALS_JSON**
   - Used if BASE64 is not set
   - Good for simple cases

3. **SERVICE_ACCOUNT_FILE** (lowest priority)
   - Used if neither BASE64 nor JSON set
   - Local development only
   - Requires file to exist

If none are set, you'll get an error:
```
RuntimeError: No Google credentials found. Set one of: 
GOOGLE_CREDENTIALS_BASE64, GOOGLE_CREDENTIALS_JSON, or SERVICE_ACCOUNT_FILE
```

---

## Testing Your Setup

### Check which credentials method is being used

```bash
curl http://localhost:8000/health
```

**Response if configured correctly**:
```json
{
  "status": "healthy",
  "message": "Service is running",
  "google_sheets_connected": true,
  "openai_configured": true
}
```

**Response if missing credentials**:
```json
{
  "status": "degraded",
  "message": "Google Sheets not connected: No Google credentials found...",
  "google_sheets_connected": false,
  "openai_configured": false
}
```

### Run a test reconciliation

```bash
curl -X POST http://localhost:8000/reconciliation/run \
  -H "Content-Type: application/json" \
  -d '{"run_date": "2026-02-07"}'
```

---

## Troubleshooting

### "No Google credentials found" error

**Solution**: Ensure ONE of these is set:
- `GOOGLE_CREDENTIALS_BASE64` (recommended)
- `GOOGLE_CREDENTIALS_JSON`
- `SERVICE_ACCOUNT_FILE` + file exists

Check what's set:
```bash
# Bash/Zsh
echo $GOOGLE_CREDENTIALS_BASE64
echo $GOOGLE_CREDENTIALS_JSON
echo $SERVICE_ACCOUNT_FILE

# Or see all relevant vars
env | grep GOOGLE
```

### Base64 decoding fails

**Symptoms**: "Failed to decode GOOGLE_CREDENTIALS_BASE64"

**Solution**:
```bash
# Test your Base64 string locally
echo "your_base64_string" | base64 -d | jq .

# If it fails, re-encode:
base64 -i streamlit-analytics-488117-db0b145f8c2a.json > /tmp/creds.b64
cat /tmp/creds.b64  # Copy this entire output
```

### Google Sheets connection fails after deployment

**Symptoms**: `"google_sheets_connected": false` even with credentials set

**Possible causes**:
1. Spreadsheet ID is wrong
2. Service account doesn't have access to sheet
3. Credentials are for wrong GCP project

**Solution**:
```bash
# Verify Spreadsheet ID
echo $SPREADSHEET_ID

# Check if service account has access
# (Share the spreadsheet with the service account email)

# Test credentials locally first
python -c "from config import settings; print(settings.get_google_credentials())"
```

### Port conflict on localhost:8000

**Solution**:
```bash
# Change PORT in .env
API_PORT=8001

# Or kill the process using port 8000
lsof -i :8000
kill -9 <PID>
```

---

## Security Checklist

- ✅ Never commit `.env` file (it's in .gitignore)
- ✅ Never commit JSON credential files
- ✅ Use Base64 encoding for cloud deployment
- ✅ Rotate credentials regularly
- ✅ Use secret management tools (Render secrets, AWS Secrets Manager, etc.)
- ✅ Don't share Base64 strings in chat or emails
- ✅ Use environment variables instead of hardcoding credentials
- ✅ Review `.env.example` - it should never have real values

---

## Summary Table

| Method | Local Dev | Cloud Deploy | Security | Ease | Priority |
|--------|-----------|--------------|----------|------|----------|
| Base64 | ✅ | ✅ | ⭐⭐⭐ | ⭐⭐⭐ | 1 |
| JSON String | ✅ | ⚠️ | ⭐⭐ | ⭐⭐ | 2 |
| File Path | ✅ | ❌ | ⭐⭐ | ⭐⭐⭐ | 3 |

**Recommendation**: Use **Method 1 (Base64)** for production and **Method 3 (File Path)** for local development.

---

## Need Help?

1. Check health endpoint: `GET /health`
2. Review error messages in logs
3. Test credentials locally before deploying
4. Ensure spreadsheet ID is correct
5. Verify service account has access to spreadsheet
