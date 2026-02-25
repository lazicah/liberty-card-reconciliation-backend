# Quick Reference - Environment Setup

## 🚀 Quick Start

### Local Development (5 minutes)
```bash
# 1. Copy environment template
cp .env.example .env

# 2. Encode your Google credentials
base64 -i streamlit-analytics-488117-db0b145f8c2a.json | pbcopy
# (Output is now on clipboard)

# 3. Edit .env and paste
GOOGLE_CREDENTIALS_BASE64=<paste here>

# 4. Add other variables
OPENAI_API_KEY=your_key
SPREADSHEET_ID=1La0dpzzo2yZQTOe3DJk11uapbgF4kk2fqQ6fblck8TI

# 5. Test setup
python test_setup.py

# 6. Run API
python main.py
```

### Production Deployment on Render (10 minutes)
```bash
# 1. Push to GitHub
git add .
git commit -m "Update API"
git push

# 2. Create service on Render.com
# - New Web Service
# - Connect GitHub repo
# - Build: pip install -r requirements.txt
# - Start: uvicorn main:app --host 0.0.0.0 --port $PORT

# 3. Add environment variables in Render Dashboard
GOOGLE_CREDENTIALS_BASE64=<your_base64_string>
OPENAI_API_KEY=<your_key>
SPREADSHEET_ID=1La0dpzzo2yZQTOe3DJk11uapbgF4kk2fqQ6fblck8TI
API_RELOAD=false

# 4. Deploy and test
curl https://your-render-url.onrender.com/health
```

---

## 📋 Environment Variables Cheat Sheet

### Required (at least one)
| Variable | Value | Best For |
|----------|-------|----------|
| `GOOGLE_CREDENTIALS_BASE64` | Base64 encoded JSON | ⭐ Production |
| `GOOGLE_CREDENTIALS_JSON` | Raw JSON string | Alternative |
| `SERVICE_ACCOUNT_FILE` | File path | Local dev |

### Required (always)
| Variable | Value | Example |
|----------|-------|---------|
| `SPREADSHEET_ID` | Your Google Sheet ID | `1La0dpzzo2yZQTOe3DJk11...` |

### Optional
| Variable | Value | Default |
|----------|-------|---------|
| `OPENAI_API_KEY` | Your OpenAI key | (empty = skipped) |
| `API_HOST` | Server host | `0.0.0.0` |
| `API_PORT` | Server port | `8000` |
| `API_RELOAD` | Auto-reload code | `true` |

---

## 🔐 Encoding Credentials

```bash
# Encode to Base64
base64 -i streamlit-analytics-488117-db0b145f8c2a.json

# To clipboard (macOS)
base64 -i streamlit-analytics-488117-db0b145f8c2a.json | pbcopy

# To clipboard (Linux)
base64 -i streamlit-analytics-488117-db0b145f8c2a.json | xclip -selection clipboard

# Save to file
base64 -i streamlit-analytics-488117-db0b145f8c2a.json > credentials.b64

# Verify encoding
base64 -D < credentials.b64 | python -m json.tool
```

---

## ✅ Verification

```bash
# Test setup
python test_setup.py

# Check health
curl http://localhost:8000/health

# View API docs
http://localhost:8000/docs

# Test reconciliation
curl -X POST http://localhost:8000/reconciliation/run \
  -H "Content-Type: application/json" \
  -d '{"run_date": "2026-02-07"}'
```

---

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| "No Google credentials found" | Set `GOOGLE_CREDENTIALS_BASE64` or another method |
| "Failed to decode Base64" | Verify string is valid: `echo "..." \| base64 -D \| python -m json.tool` |
| "Google Sheets not connected" | Share sheet with service account email |
| Port 8000 in use | Change `API_PORT` in .env or use different port |
| Module not found | Install deps: `pip install -r requirements.txt` |

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| `ENVIRONMENT_SETUP.md` | Complete setup guide (all platforms) |
| `RENDER_DEPLOYMENT.md` | Step-by-step Render guidance |
| `CHANGES.md` | What was modified and why |
| `test_setup.py` | Automated verification script |

---

## 🌐 API Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/` | Root info |
| `GET` | `/health` | Service status |
| `POST` | `/reconciliation/run` | Run reconciliation |
| `GET` | `/metrics/latest` | Latest metrics |
| `GET` | `/metrics/{date}` | Metrics by date |
| `GET` | `/config` | Configuration |

---

## 🚀 Deployment Platforms

### Render
- Guide: `RENDER_DEPLOYMENT.md`
- Recommended for beginners
- Free tier available

### Docker
```bash
docker-compose up -d
# Or
docker run -e GOOGLE_CREDENTIALS_BASE64=... \
  -p 8000:8000 liberty-card-reconciliation
```

### AWS / Heroku / GCP
- See `ENVIRONMENT_SETUP.md` for instructions
- Set environment variables via platform UI

---

## 💡 Pro Tips

1. **Never commit `.env` file** - it's in `.gitignore`
2. **Use Base64 encoding** for all cloud deployments
3. **Test locally first** before pushing to cloud
4. **Rotate credentials** every 6-12 months
5. **Check health endpoint** to verify connectivity
6. **Share spreadsheet** with service account email (project_id@...)

---

## 🔗 Useful Links

- API Docs: `http://localhost:8000/docs`
- Google Cloud Console: https://console.cloud.google.com
- OpenAI API Keys: https://platform.openai.com/api-keys
- Render Dashboard: https://dashboard.render.com
- GitHub: https://github.com/lazicah/liberty-card-reconciliation-backend

---

## 📞 Support

1. Run `python test_setup.py` to identify issues
2. Check relevant documentation file
3. Review error messages in health endpoint
4. Check application logs

---

**Last Updated**: February 2026  
**Version**: 1.0.0  
**Quick Reference v1.0**
