# Render Deployment Guide

Quick guide for deploying Liberty Card Reconciliation API to Render.

## Prerequisites

- GitHub account with your repository pushed
- Render account (register at render.com)
- Google credentials JSON file
- OpenAI API key (optional, for AI summaries)
- Google Spreadsheet and its ID

## Step-by-Step Deployment

### 1. Prepare Your Google Credentials

```bash
# Encode credentials to Base64
base64 -i streamlit-analytics-488117-db0b145f8c2a.json | pbcopy

# Your encoded credentials are now copied to clipboard
# Save them somewhere safe for the next step
```

### 2. Create Render Service

1. Visit [render.com](https://render.com)
2. Click **+ New** → **Web Service**
3. Select **Build and deploy from a Git repository**
4. Click **Connect** to connect your GitHub repository
5. Select the `liberty-card-reconciliation-backend` repository

### 3. Configure Service Settings

Fill in the following:

| Field | Value |
|-------|-------|
| Name | `liberty-card-reconciliation` |
| Environment | `Python 3` |
| Region | (Choose closest to you) |
| Branch | `main` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

### 4. Add Environment Variables

Click **Add Environment Variable** for each:

| Key | Value | Source |
|-----|-------|--------|
| `GOOGLE_CREDENTIALS_BASE64` | Paste your Base64 string | Base64 encoded JSON |
| `OPENAI_API_KEY` | Your OpenAI API key | OpenAI dashboard |
| `SPREADSHEET_ID` | `1La0dpzzo2yZQTOe3DJk11uapbgF4kk2fqQ6fblck8TI` | Google Sheets URL |
| `API_RELOAD` | `false` | (for production) |

### 5. Deploy

1. Click **Create Web Service**
2. Render will start building and deploying
3. Wait for the build to complete (usually 2-3 minutes)
4. You'll see a green ✓ when deployment is successful
5. Your API will be available at: `https://liberty-card-reconciliation.onrender.com`

## Verify Deployment

Test your API is working:

```bash
# Check health
curl https://liberty-card-reconciliation.onrender.com/health

# View API docs
https://liberty-card-reconciliation.onrender.com/docs
```

### Expected Health Response

```json
{
  "status": "healthy",
  "message": "Service is running",
  "google_sheets_connected": true,
  "openai_configured": true
}
```

## Common Issues & Solutions

### Issue: "No Google credentials found"

**Cause**: `GOOGLE_CREDENTIALS_BASE64` environment variable not set

**Solutions**:
1. Go to Service Settings → Environment
2. Add the variable with your Base64 string
3. Click "Save" and wait for redeploy

### Issue: "Google Sheets not connected"

**Cause**: Service account doesn't have access to spreadsheet

**Solutions**:
1. Get service account email from your JSON file (look for `client_email`)
2. Share spreadsheet with that email address
3. Wait a few minutes for permissions to update
4. Manually trigger redeploy in Render

### Issue: "Failed to decode GOOGLE_CREDENTIALS_BASE64"

**Cause**: Base64 string is corrupted or invalid

**Solutions**:
```bash
# Test your Base64 locally
echo "your_base64_string" | base64 -d | python -m json.tool

# If it fails, re-encode
base64 -i streamlit-analytics-488117-db0b145f8c2a.json
# Copy and paste entire output carefully
```

### Issue: Deployment stuck in building

**Causes**: Long build time or Python dependency installation issues

**Solutions**:
- Wait up to 15 minutes
- Check build logs for specific errors
- Try updating `requirements.txt`
- Delete and recreate service if stuck

## Updating Your API

### Option A: Automatic (Recommended)

```bash
# Make changes locally
git add .
git commit -m "Update API"
git push origin main

# Render automatically rebuilds and deploys
# Monitor progress in Render dashboard
```

### Option B: Manual Redeploy

1. Go to your Service in Render
2. Click **Manual Deploy** → **Deploy latest commit**
3. Wait for build to complete

### Option C: Update Environment Variables Only

1. Go to Service Settings → Environment
2. Edit variable values
3. Click "Save"
4. Service automatically redeploys with new vars

## Monitoring

### View Logs

```
In Render dashboard:
1. Select your service
2. Click "Logs" tab
3. View real-time logs as requests come in
```

### Enable More Verbose Logging

Set environment variable:
```
LOG_LEVEL=DEBUG
```

Then restart service.

## Database & File Storage

Render services are **stateless** - files don't persist across deployments.

For persistent storage:
1. **For metrics files**: Use Google Sheets (already integrated)
2. **For logs**: Use Render's log service (built-in)
3. **For persistent DB**: Add PostgreSQL service to your render.yaml

Current setup: All critical data is saved to Google Sheets automatically.

## Performance & Scaling

Render pricing is based on:
- **Compute time**: How long your API runs
- **Paid tier**: Optional for better performance

For this API:
- **Free tier**: Good for small usage
- **Starter plan**: ₦2/hour for production use

## Backup Plan

If something breaks in production:

```bash
# 1. Check logs
curl https://liberty-card-reconciliation.onrender.com/health

# 2. View detailed logs in Render dashboard
# 3. Check environment variables are correct
# 4. Manually trigger redeploy
# 5. If needed, delete and recreate service
```

All important data is in Google Sheets, so you can recreate the service anytime.

## Cost Estimation

| Component | Cost | Notes |
|-----------|------|-------|
| Render API | Free/Starter | ~₦2/hour when active |
| Google Sheets | Free | Unlimited with Google account |
| OpenAI API | Variable | Only if using AI summaries |
| Domain | Optional | Custom domain is paid |

## Security Best Practices

1. ✅ Never share `GOOGLE_CREDENTIALS_BASE64` value
2. ✅ Rotate credentials every 6-12 months
3. ✅ Use different credentials for dev/prod
4. ✅ Enable logging for audit trail
5. ✅ Keep dependencies updated

## Next Steps

1. ✅ Deploy API
2. ✅ Test `/health` endpoint
3. ✅ Run test reconciliation
4. ✅ Build web interface (see WEB_INTERFACE_PROMPT.md)
5. ✅ Set up monitoring and alerts

## Support

- Render docs: [render.com/docs](https://render.com/docs)
- API docs: `https://your-service-url.onrender.com/docs`
- Issues: Check logs and error messages

## Useful Links

- Service Status: https://render.com/status
- Pricing: https://render.com/pricing
- Documentation: https://render.com/docs
