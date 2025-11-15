# Quick Start: Production Deployment

This is a condensed guide to get your app production-ready quickly. For detailed information, see [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md).

---

## 🚀 Essential Steps (30 minutes)

### 1. Security Basics (10 min)

**Update `SSO/auth.py` for secure cookies:**

```python
# Find this line (around line 71-74):
cookie_controller.set("authenticated", "true", max_age=604800)

# Replace with:
cookie_controller.set(
    "authenticated",
    "true",
    max_age=86400,  # 24 hours for production
    secure=True,    # HTTPS only
    samesite="Strict"
)

# Do the same for the user_info cookie
```

**Remove debug code from `SSO/session.py`:**

```python
# Delete or comment out these lines (around line 37-39):
# st.sidebar.write("Debug - Cookies:", cookies)
# st.sidebar.write("Debug - Session State Auth:", st.session_state.get("authenticated"))
```

### 2. Azure AD Configuration (10 min)

1. **Create production app registration** in Azure Portal
   - Separate from development
   - Add production redirect URI: `https://your-domain.com`

2. **Set up production environment variables:**

```bash
# Create .env for production (never commit this!)
AZURE_CLIENT_ID=your_prod_client_id
AZURE_CLIENT_SECRET=your_prod_secret
AZURE_TENANT_ID=your_prod_tenant_id
REDIRECT_URI=https://your-domain.com
ENVIRONMENT=production
```

3. **Minimize permissions** in Azure AD
   - Only keep `User.Read` unless you need more

### 3. Code Updates (10 min)

**Update `SSO/config.py` to support Streamlit Cloud secrets:**

```python
import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Support both .env and Streamlit secrets
try:
    CLIENT_ID = os.getenv("AZURE_CLIENT_ID") or st.secrets["AZURE_CLIENT_ID"]
    CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET") or st.secrets["AZURE_CLIENT_SECRET"]
    TENANT_ID = os.getenv("AZURE_TENANT_ID") or st.secrets["AZURE_TENANT_ID"]
    REDIRECT_URI = os.getenv("REDIRECT_URI") or st.secrets.get("REDIRECT_URI", "http://localhost:8501")
except (KeyError, FileNotFoundError):
    # Fallback to environment variables only
    CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
    TENANT_ID = os.getenv("AZURE_TENANT_ID")
    REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8501")

# Azure AD Authority and Scope
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["User.Read"]
```

**Pin dependency versions in `requirements.txt`:**

```txt
streamlit==1.31.0
msal==1.26.0
python-dotenv==1.0.1
streamlit-cookies-controller==0.0.2
```

---

## 📦 Deployment Options

### Option 1: Streamlit Community Cloud (Easiest)

**Steps:**

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets in app settings:

```toml
AZURE_CLIENT_ID = "your_client_id"
AZURE_CLIENT_SECRET = "your_secret"
AZURE_TENANT_ID = "your_tenant_id"
REDIRECT_URI = "https://your-app.streamlit.app"
```

5. Update Azure AD redirect URI to match your Streamlit Cloud URL
6. Deploy!

**Pros:** Free, easy, no infrastructure management
**Cons:** Limited resources, public repository required

---

### Option 2: Docker (Most Flexible)

**Build and run:**

```bash
# Build image
docker build -t streamlit-sso .

# Run container
docker run -p 8501:8501 --env-file .env streamlit-sso

# Or use Docker Compose
docker-compose up -d
```

**Deploy to cloud:**
- Azure Container Instances
- AWS ECS
- Google Cloud Run
- DigitalOcean Apps

**Pros:** Full control, portable, scalable
**Cons:** Requires infrastructure knowledge

---

### Option 3: Azure App Service

**Steps:**

1. Create App Service in Azure Portal
2. Set environment variables in Configuration
3. Deploy via:
   - GitHub Actions (recommended)
   - Azure CLI
   - VS Code extension

**Pros:** Integrated with Azure AD, auto-scaling
**Cons:** Cost, Azure-specific

---

## ✅ Pre-Launch Checklist

### Critical (Must Do)

- [ ] Remove all debug/print statements
- [ ] Enable HTTPS (never use HTTP in production)
- [ ] Set secure cookies (secure=True, samesite="Strict")
- [ ] Configure production Azure AD app with correct redirect URI
- [ ] Set environment variables securely (never commit .env)
- [ ] Test authentication flow end-to-end
- [ ] Reduce session timeout to 24 hours or less
- [ ] Verify `.env` is in `.gitignore`

### Important (Should Do)

- [ ] Pin exact dependency versions
- [ ] Enable XSRF protection in `.streamlit/config.toml`
- [ ] Set up monitoring (Application Insights, Sentry)
- [ ] Create separate Azure AD apps for dev/prod
- [ ] Test on multiple browsers and devices
- [ ] Add error logging
- [ ] Set up backups if storing data
- [ ] Document deployment process

### Nice to Have

- [ ] Add rate limiting
- [ ] Implement session timeout warning
- [ ] Add user analytics
- [ ] Set up CI/CD pipeline
- [ ] Create staging environment
- [ ] Add automated tests

---

## 🔍 Quick Security Check

Run these commands before deploying:

```bash
# 1. Check for exposed secrets
grep -r "AZURE_CLIENT" . --exclude-dir=venv --exclude-dir=.git --exclude=".env.example"

# 2. Verify .gitignore
cat .gitignore | grep ".env"

# 3. Check dependencies for vulnerabilities
pip install safety
safety check -r requirements.txt

# 4. Lint code
pip install pylint
pylint app.py SSO/
```

---

## 🐛 Common Gotchas

### 1. Redirect URI Mismatch

**Error:** `AADSTS50011: The reply URL specified in the request does not match`

**Fix:**
- Exact match required (no trailing slash difference)
- Both HTTP/HTTPS matter
- Add URL to Azure AD app registration

### 2. Cookies Not Working

**Problem:** Session not persisting

**Fix:**
- Enable cookies in browser
- Use `secure=True` only with HTTPS
- Check `samesite` attribute
- Verify domain matches

### 3. Import Errors

**Error:** `ModuleNotFoundError: No module named 'SSO'`

**Fix:**
- Ensure `SSO/__init__.py` exists
- Check directory structure
- Verify deployment includes all files

### 4. Environment Variables Not Loading

**Problem:** Configuration error on deployment

**Fix:**
- Check variable names exactly match
- Streamlit Cloud: use secrets, not .env
- Docker: use --env-file or docker-compose
- Azure: set in Application Settings

---

## 📊 Post-Deployment Monitoring

### First 24 Hours

Monitor these metrics:

- [ ] Successful login rate (should be >95%)
- [ ] Error logs (check for exceptions)
- [ ] Response times (login should be <3 seconds)
- [ ] Session persistence (cookies working?)
- [ ] Mobile compatibility

### Use Azure AD Logs

1. Go to Azure Portal → Azure AD → Sign-in logs
2. Filter by your application
3. Look for failed sign-ins
4. Check error codes and fix issues

### Set Up Alerts

Configure alerts for:
- High error rate (>5%)
- Failed authentication attempts (>10/hour)
- Slow response times (>5 seconds)
- High memory usage (>80%)

---

## 🆘 Emergency Rollback

If something goes wrong:

### Streamlit Cloud
1. Go to app settings
2. Click "Reboot app" or "Revert to previous deployment"

### Docker
```bash
# Stop container
docker-compose down

# Revert to previous image
docker run previous-image-tag

# Or redeploy old code
git checkout previous-commit
docker-compose up -d
```

### Azure App Service
1. Go to Deployment Center
2. Select previous deployment
3. Click "Redeploy"

---

## 📞 Support Resources

- **Azure AD Issues:** [Microsoft Q&A](https://docs.microsoft.com/answers/)
- **Streamlit Issues:** [Community Forum](https://discuss.streamlit.io/)
- **Security Concerns:** [OWASP Guidelines](https://owasp.org/)

---

## 🎯 Success Criteria

Your app is production-ready when:

✅ All authentication flows work smoothly
✅ No secrets in code or repository
✅ HTTPS enabled and enforced
✅ Error handling in place
✅ Monitoring/logging configured
✅ Tested on multiple devices
✅ Documentation complete
✅ Rollback plan ready

---

**Next Steps:**

1. Review [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) for detailed guidance
2. Test thoroughly in staging environment
3. Deploy to production
4. Monitor for 24-48 hours
5. Gather user feedback
6. Iterate and improve

**Good luck with your deployment! 🚀**
