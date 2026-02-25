# Configuration Changes Summary

This document outlines all changes made to support loading Google credentials from environment variables instead of files.

## Problem Statement

Previously, the application required the Google credentials JSON file (`streamlit-analytics-488117-db0b145f8c2a.json`) to be:
1. Stored in the project root
2. Tracked in some environments
3. Manually copied to deployed servers

This approach has security and deployment issues:
- ❌ Risk of accidentally committing sensitive files
- ❌ File must exist in working directory for deployment
- ❌ Difficult to rotate credentials
- ❌ Doesn't work well with containerized/serverless deployments

## Solution

Updated the entire codebase to load Google credentials from environment variables with three priority options:

1. **GOOGLE_CREDENTIALS_BASE64** (Base64 encoded JSON) - Recommended
2. **GOOGLE_CREDENTIALS_JSON** (Raw JSON string) - Alternative
3. **SERVICE_ACCOUNT_FILE** (File path) - Local development fallback

## Files Modified

### 1. `config.py`
**Status**: ✅ Updated

**Changes**:
- Added imports: `json`, `base64`, `Path`
- Added three new configuration variables:
  - `google_credentials_base64`
  - `google_credentials_json`
  - `service_account_file` (changed from required to optional)
- Added new method `get_google_credentials()`:
  - Checks credentials in priority order
  - Decodes Base64 if needed
  - Parses JSON strings
  - Falls back to file path
  - Raises `RuntimeError` with helpful message if none found

**Before**:
```python
service_account_file: str = os.getenv("SERVICE_ACCOUNT_FILE", "streamlit-analytics-488117-db0b145f8c2a.json")
```

**After**:
```python
google_credentials_base64: str = os.getenv("GOOGLE_CREDENTIALS_BASE64", "")
google_credentials_json: str = os.getenv("GOOGLE_CREDENTIALS_JSON", "")
service_account_file: str = os.getenv("SERVICE_ACCOUNT_FILE", "")

def get_google_credentials(self) -> dict:
    """Load Google credentials from environment variables..."""
```

### 2. `services/google_sheets_service.py`
**Status**: ✅ Updated

**Changes**:
- Modified `__init__()` method:
  - Changed from `Credentials.from_service_account_file()` to `Credentials.from_service_account_info()`
  - Now calls `settings.get_google_credentials()` to get credentials dict
  - Added try-except with helpful error messages

**Before**:
```python
self.creds = Credentials.from_service_account_file(
    settings.service_account_file,
    scopes=settings.google_scopes
)
```

**After**:
```python
credentials_dict = settings.get_google_credentials()
self.creds = Credentials.from_service_account_info(
    credentials_dict,
    scopes=settings.google_scopes
)
```

### 3. `.env.example`
**Status**: ✅ Updated

**Changes**:
- Removed sensitive data (actual API keys)
- Added clear instructions for all three methods
- Added helpful comments about deployment
- Removed the actual OPENAI_API_KEY value
- Added guidance for Render and other platforms

**Before**:
```
OPENAI_API_KEY=sk-svcacct-7BXVMHErgcxhITkoSyrpZx73Hs-...
SERVICE_ACCOUNT_FILE=streamlit-analytics-488117-db0b145f8c2a.json
SPREADSHEET_ID=1La0dpzzo2yZQTOe3DJk11uapbgF4kk2fqQ6fblck8TI
```

**After**:
```
# Three methods to provide credentials:
GOOGLE_CREDENTIALS_BASE64=  # Recommended for production
# GOOGLE_CREDENTIALS_JSON={"type":"service_account"...}
# SERVICE_ACCOUNT_FILE=streamlit-analytics-488117-db0b145f8c2a.json
```

### 4. `main.py`
**Status**: ✅ Updated (Health Check)

**Changes**:
- Enhanced `/health` endpoint error handling
- Now captures and returns error messages
- Provides better feedback about credential status
- Shows specific error if Google Sheets connection fails

**Before**:
```python
except Exception as e:
    pass  # Silent failure
```

**After**:
```python
except Exception as e:
    google_sheets_error = str(e)  # Capture error message
    message = f"Google Sheets not connected: {google_sheets_error}"
```

## New Documentation Files

### 1. `ENVIRONMENT_SETUP.md`
Complete guide covering:
- Three credential methods with examples
- Setup for local development
- Setup for each cloud platform:
  - Render
  - Docker/Docker Compose
  - AWS (ECS/Fargate)
  - Heroku
- Troubleshooting guide
- Security checklist
- Testing procedures

### 2. `RENDER_DEPLOYMENT.md`
Step-by-step guide for Render deployment:
- Encoding credentials to Base64
- Creating Render service
- Setting environment variables
- Verification steps
- Common issues and solutions
- Monitoring and logging
- Cost information

### 3. `test_setup.py`
Automated verification script that:
- Tests Python imports
- Verifies OpenAI configuration
- Checks Google Sheets ID
- Validates Google credentials (all three methods)
- Tests API configuration
- Tests config module initialization
- Provides clear pass/fail messages
- Suggests fixes for failures

**Usage**:
```bash
python test_setup.py
```

## Backward Compatibility

The changes maintain backward compatibility:

✅ **Local development with file** still works:
```bash
SERVICE_ACCOUNT_FILE=streamlit-analytics-488117-db0b145f8c2a.json
# File will be loaded automatically
```

✅ **No .env file needed** for cloud deployment:
```bash
GOOGLE_CREDENTIALS_BASE64=your_base64_string
# Environment variable is read directly
```

## Security Improvements

### Before ❌
- Credentials file at risk of accidental commit
- Hard to rotate credentials
- Credentials visible in plaintext
- No standard way to handle sensitive data

### After ✅
- Credentials in environment variables (never committed)
- Base64 encoding obscures sensitive data
- Easy credential rotation via environment
- Follows 12-factor app principles
- Standard practice for cloud deployments

## Migration Path for Existing Users

1. **No action required** - existing setup still works
2. **Optional - Upgrade to Base64 method**:
   ```bash
   # Encode existing credentials
   base64 -i streamlit-analytics-488117-db0b145f8c2a.json | pbcopy
   
   # Update .env
   GOOGLE_CREDENTIALS_BASE64=<paste>
   
   # Remove file reference
   # SERVICE_ACCOUNT_FILE=  # Delete or empty this line
   ```
3. **For cloud deployment** - use GOOGLE_CREDENTIALS_BASE64 method

## Testing

Run the included test script to verify everything works:

```bash
./test_setup.py
# or
python test_setup.py
```

Expected output if configured correctly:
```
✅ PASS - Python Imports
✅ PASS - OpenAI Config
✅ PASS - Spreadsheet ID
✅ PASS - Google Credentials
✅ PASS - API Configuration
✅ PASS - Config Module

6/6 tests passed
🎉 All tests passed! Your setup is ready.
```

## Environment Variable Priority

The application checks in this order:

```
1. GOOGLE_CREDENTIALS_BASE64  (if set, use this)
   ↓ (if not set)
2. GOOGLE_CREDENTIALS_JSON    (if set, use this)
   ↓ (if not set)
3. SERVICE_ACCOUNT_FILE       (if set and file exists, use this)
   ↓ (if none of above)
4. Error: No credentials found
```

## Deployment Checklist

Before deploying to Render or other cloud platforms:

- [ ] Read ENVIRONMENT_SETUP.md
- [ ] Encode credentials: `base64 -i your_file.json | pbcopy`
- [ ] Create service on Render
- [ ] Add GOOGLE_CREDENTIALS_BASE64 environment variable
- [ ] Add OPENAI_API_KEY environment variable
- [ ] Add SPREADSHEET_ID environment variable
- [ ] Set API_RELOAD=false
- [ ] Test `/health` endpoint
- [ ] Run test reconciliation
- [ ] Monitor logs

## Troubleshooting

### Error: "No Google credentials found"

**Solution**: Set ONE of these environment variables:
```bash
GOOGLE_CREDENTIALS_BASE64=...  # Recommended
# OR
GOOGLE_CREDENTIALS_JSON=...
# OR
SERVICE_ACCOUNT_FILE=/path/to/file
```

### Error: "Failed to decode GOOGLE_CREDENTIALS_BASE64"

**Solution**: Verify Base64 string is valid:
```bash
echo "your_string" | base64 -d | python -m json.tool
```

### Error: "Google Sheets not connected"

**Possible causes**:
1. Service account doesn't have access to spreadsheet
2. Spreadsheet ID is wrong
3. Credentials are for wrong Google project

**Solutions**:
- Share spreadsheet with service account email
- Verify SPREADSHEET_ID is correct
- Test credentials locally first

## Summary

✅ **All code updated** to load from environment variables  
✅ **Three flexible methods** to provide credentials  
✅ **Backward compatible** - existing setups still work  
✅ **Improved security** - no sensitive files needed  
✅ **Better for deployment** - works with Render, Docker, et al.  
✅ **Comprehensive documentation** - ENVIRONMENT_SETUP.md and RENDER_DEPLOYMENT.md  
✅ **Automated testing** - test_setup.py validates configuration  

The application is now ready for production deployment to cloud platforms!
