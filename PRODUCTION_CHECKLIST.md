# Production Readiness Checklist

This guide will help you prepare this Azure AD SSO template for production use. Follow these steps carefully before deploying to production.

---

## 📋 Table of Contents

1. [Security Configuration](#1-security-configuration)
2. [Code Hardening](#2-code-hardening)
3. [Environment Setup](#3-environment-setup)
4. [Azure AD Production Configuration](#4-azure-ad-production-configuration)
5. [Testing & Validation](#5-testing--validation)
6. [Deployment Options](#6-deployment-options)
7. [Monitoring & Logging](#7-monitoring--logging)
8. [Performance Optimization](#8-performance-optimization)
9. [Documentation](#9-documentation)
10. [Final Pre-Launch Checklist](#10-final-pre-launch-checklist)

---

## 1. Security Configuration

### ✅ Environment Variables

- [ ] **Never commit `.env` file** - Verify it's in `.gitignore`
- [ ] **Create `.env.example`** - Template without sensitive data
- [ ] **Use environment-specific configs** - Separate dev/staging/prod
- [ ] **Rotate secrets regularly** - Set calendar reminders

### ✅ Azure AD Security

- [ ] **Use client certificates** (recommended over secrets for production)
- [ ] **Enable Conditional Access policies**
- [ ] **Set token lifetime policies**
- [ ] **Enable MFA requirements** for users
- [ ] **Review and minimize API permissions** - Only request what you need
- [ ] **Enable admin consent workflow**

### ✅ Application Security

- [ ] **Enable HTTPS only** - Never use HTTP in production
- [ ] **Implement CORS policies** if building API
- [ ] **Add rate limiting** to prevent abuse
- [ ] **Sanitize user inputs** before displaying
- [ ] **Implement CSP headers** (Content Security Policy)
- [ ] **Add security headers** (X-Frame-Options, etc.)

```python
# Add to app.py for security headers
import streamlit as st

def add_security_headers():
    """Add security headers to the application"""
    st.set_page_config(
        page_title="Your App",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    # Note: Streamlit's server configuration should be updated for full header control
```

### ✅ Session Security

- [ ] **Reduce cookie expiration** - Consider shorter than 7 days for sensitive apps
- [ ] **Use secure cookies** - Set `secure=True` and `httponly=True`
- [ ] **Implement session timeout** - Auto-logout after inactivity
- [ ] **Add CSRF protection** if handling forms

**Update `SSO/auth.py` for secure cookies:**

```python
# For production - use secure cookies
cookie_controller.set(
    "authenticated",
    "true",
    max_age=86400,  # 24 hours instead of 7 days
    secure=True,     # Only over HTTPS
    samesite="Strict"  # Prevent CSRF
)
```

---

## 2. Code Hardening

### ✅ Error Handling

- [ ] **Remove debug statements** - Check `SSO/session.py` for debug code
- [ ] **Add proper error logging** - Don't expose stack traces to users
- [ ] **Implement graceful degradation**
- [ ] **Add retry logic** for API calls

**Example error handling in `SSO/auth.py`:**

```python
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_auth_callback(auth_code, cookie_controller):
    try:
        # ... existing code ...
    except Exception as e:
        # Log error server-side
        logger.error(f"Auth failed: {str(e)}", exc_info=True)

        # Show user-friendly message
        st.error("Authentication failed. Please try again or contact support.")
        return False
```

### ✅ Input Validation

- [ ] **Validate all user inputs**
- [ ] **Sanitize data before display**
- [ ] **Check file upload sizes/types** (if applicable)
- [ ] **Validate redirect URIs**

### ✅ Code Quality

- [ ] **Run linting** - Use `pylint` or `flake8`
- [ ] **Format code** - Use `black` for consistent formatting
- [ ] **Add type hints** - Use Python type annotations
- [ ] **Write unit tests** - Test authentication flow
- [ ] **Add integration tests** - Test end-to-end flow
- [ ] **Code review** - Have another developer review

```bash
# Install development tools
pip install pylint black pytest

# Run linting
pylint app.py SSO/

# Format code
black app.py SSO/

# Run tests
pytest tests/
```

---

## 3. Environment Setup

### ✅ Dependency Management

- [ ] **Pin exact versions** in `requirements.txt`
- [ ] **Review security advisories** for dependencies
- [ ] **Use virtual environments**
- [ ] **Document Python version** requirement

**Update `requirements.txt` with exact versions:**

```txt
streamlit==1.31.0
msal==1.26.0
python-dotenv==1.0.1
streamlit-cookies-controller==0.0.2
```

### ✅ Configuration Files

- [ ] **Create `.streamlit/config.toml`** for app configuration
- [ ] **Set server configuration** for production
- [ ] **Configure logging levels**
- [ ] **Set memory limits**

**Create/Update `.streamlit/config.toml`:**

```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200

[browser]
gatherUsageStats = false
serverAddress = "your-domain.com"
serverPort = 443

[theme]
base = "light"
primaryColor = "#0078D4"

[logger]
level = "info"
```

### ✅ Environment Variables

Production environment variables structure:

```bash
# Development
AZURE_CLIENT_ID=dev_client_id
AZURE_CLIENT_SECRET=dev_secret
AZURE_TENANT_ID=dev_tenant_id
REDIRECT_URI=http://localhost:8501
ENVIRONMENT=development

# Production
AZURE_CLIENT_ID=prod_client_id
AZURE_CLIENT_SECRET=prod_secret
AZURE_TENANT_ID=prod_tenant_id
REDIRECT_URI=https://your-domain.com
ENVIRONMENT=production
LOG_LEVEL=INFO
SESSION_TIMEOUT=3600
```

---

## 4. Azure AD Production Configuration

### ✅ App Registration

- [ ] **Create separate app registrations** for dev/staging/prod
- [ ] **Set production redirect URIs** in Azure
- [ ] **Configure token lifetimes**
- [ ] **Enable token encryption**
- [ ] **Set up app roles** if needed

### ✅ Redirect URIs

Add all valid production URIs:

```
https://your-domain.com
https://www.your-domain.com
https://app.your-domain.com
```

### ✅ API Permissions

Review and request only necessary permissions:

| Permission | Required | Justification |
|------------|----------|---------------|
| User.Read | Yes | Basic user profile |
| Mail.Read | Only if needed | Email access |
| Files.Read | Only if needed | File access |

### ✅ Branding

- [ ] **Add company logo** to Azure AD app
- [ ] **Set app name** and description
- [ ] **Configure publisher domain**
- [ ] **Add privacy policy URL**
- [ ] **Add terms of service URL**

### ✅ Certificates (Recommended)

Instead of client secrets, use certificates:

1. Generate certificate:
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

2. Upload to Azure AD app registration
3. Update `SSO/auth.py` to use certificate

---

## 5. Testing & Validation

### ✅ Functional Testing

- [ ] **Test login flow** - Multiple user accounts
- [ ] **Test logout flow** - Verify session clearing
- [ ] **Test session persistence** - Browser refresh
- [ ] **Test cookie expiration** - Wait for timeout
- [ ] **Test error scenarios** - Invalid credentials, network errors
- [ ] **Test concurrent sessions** - Multiple tabs/browsers
- [ ] **Test mobile devices** - Responsive design

### ✅ Security Testing

- [ ] **Penetration testing** - Hire security professional
- [ ] **OWASP Top 10 check** - Common vulnerabilities
- [ ] **SSL/TLS validation** - Proper certificate setup
- [ ] **Session hijacking tests** - Verify secure cookies
- [ ] **CSRF testing** - Cross-site request forgery
- [ ] **XSS testing** - Cross-site scripting

### ✅ Performance Testing

- [ ] **Load testing** - Simulate multiple users
- [ ] **Stress testing** - Find breaking points
- [ ] **Memory leak testing** - Long-running sessions
- [ ] **Network latency testing** - Slow connections

### ✅ Compliance Testing

- [ ] **GDPR compliance** - Data protection (if EU users)
- [ ] **CCPA compliance** - California privacy (if US users)
- [ ] **Data retention policies** - How long to keep user data
- [ ] **Right to deletion** - User data removal process

---

## 6. Deployment Options

### Option A: Streamlit Community Cloud

**Steps:**

1. Push code to GitHub (ensure `.env` is not committed)
2. Connect to Streamlit Cloud
3. Add secrets in app settings
4. Deploy

**Secrets Configuration:**

```toml
# .streamlit/secrets.toml (in Streamlit Cloud only)
AZURE_CLIENT_ID = "your_client_id"
AZURE_CLIENT_SECRET = "your_secret"
AZURE_TENANT_ID = "your_tenant_id"
REDIRECT_URI = "https://your-app.streamlit.app"
```

**Update `SSO/config.py` to support secrets:**

```python
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Support both .env and Streamlit secrets
CLIENT_ID = os.getenv("AZURE_CLIENT_ID") or st.secrets.get("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET") or st.secrets.get("AZURE_CLIENT_SECRET")
TENANT_ID = os.getenv("AZURE_TENANT_ID") or st.secrets.get("AZURE_TENANT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI") or st.secrets.get("REDIRECT_URI", "http://localhost:8501")
```

### Option B: Azure App Service

**Steps:**

1. Create App Service in Azure Portal
2. Configure environment variables
3. Deploy via GitHub Actions or Azure CLI
4. Enable HTTPS

**GitHub Actions deployment:**

```yaml
# .github/workflows/deploy.yml
name: Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: azure/webapps-deploy@v2
        with:
          app-name: your-app-name
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

### Option C: Docker

**Create `Dockerfile`:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Create `docker-compose.yml`:**

```yaml
version: '3.8'

services:
  streamlit-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - AZURE_CLIENT_ID=${AZURE_CLIENT_ID}
      - AZURE_CLIENT_SECRET=${AZURE_CLIENT_SECRET}
      - AZURE_TENANT_ID=${AZURE_TENANT_ID}
      - REDIRECT_URI=${REDIRECT_URI}
    restart: unless-stopped
```

### Option D: Kubernetes

- [ ] **Create Kubernetes manifests**
- [ ] **Set up secrets management** (use Azure Key Vault)
- [ ] **Configure ingress** with TLS
- [ ] **Set up horizontal pod autoscaling**

---

## 7. Monitoring & Logging

### ✅ Application Monitoring

- [ ] **Set up Application Insights** (Azure)
- [ ] **Configure error tracking** (Sentry, Rollbar)
- [ ] **Monitor uptime** (UptimeRobot, Pingdom)
- [ ] **Track user metrics** (Google Analytics, Mixpanel)

**Add logging to `SSO/auth.py`:**

```python
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def handle_auth_callback(auth_code, cookie_controller):
    try:
        logger.info(f"Auth callback initiated at {datetime.utcnow()}")
        # ... existing code ...
        logger.info(f"Auth successful for user: {result.get('id_token_claims', {}).get('email')}")
        return True
    except Exception as e:
        logger.error(f"Auth failed: {str(e)}", exc_info=True)
        return False
```

### ✅ Azure AD Monitoring

- [ ] **Enable sign-in logs** in Azure AD
- [ ] **Set up alerts** for failed logins
- [ ] **Monitor token usage**
- [ ] **Track API permission usage**

### ✅ Performance Monitoring

- [ ] **Track page load times**
- [ ] **Monitor authentication latency**
- [ ] **Watch memory usage**
- [ ] **Monitor active sessions**

---

## 8. Performance Optimization

### ✅ Caching

- [ ] **Cache static content**
- [ ] **Use `@st.cache_data` for data**
- [ ] **Use `@st.cache_resource` for connections**

**Example in `app.py`:**

```python
@st.cache_data(ttl=3600)
def load_user_data(user_id):
    """Cache user data for 1 hour"""
    # Load data
    return data

@st.cache_resource
def get_database_connection():
    """Cache database connection"""
    return connection
```

### ✅ Code Optimization

- [ ] **Lazy load modules** - Import only when needed
- [ ] **Minimize recomputation** - Use session state
- [ ] **Optimize database queries** - Use indexes
- [ ] **Compress responses** - Enable gzip

### ✅ Asset Optimization

- [ ] **Optimize images** - Compress and resize
- [ ] **Minify CSS/JS** if using custom components
- [ ] **Use CDN** for static assets
- [ ] **Enable browser caching**

---

## 9. Documentation

### ✅ User Documentation

- [ ] **Create user guide** - How to use the app
- [ ] **Document features** - What the app does
- [ ] **Add FAQ section** - Common questions
- [ ] **Provide support contact**

### ✅ Developer Documentation

- [ ] **Architecture documentation** - System design
- [ ] **API documentation** - If exposing APIs
- [ ] **Deployment guide** - How to deploy
- [ ] **Troubleshooting guide** - Common issues

### ✅ Operational Documentation

- [ ] **Runbook** - Common operational tasks
- [ ] **Incident response plan** - What to do when things break
- [ ] **Backup/restore procedures**
- [ ] **Disaster recovery plan**

---

## 10. Final Pre-Launch Checklist

### 🔒 Security

- [ ] All secrets removed from code
- [ ] HTTPS enabled and working
- [ ] Security headers configured
- [ ] Authentication tested thoroughly
- [ ] Penetration testing completed
- [ ] Security audit passed

### ⚙️ Configuration

- [ ] Production environment variables set
- [ ] Azure AD production app configured
- [ ] Redirect URIs updated
- [ ] Logging configured
- [ ] Monitoring enabled
- [ ] Backup strategy in place

### 🧪 Testing

- [ ] All functional tests passing
- [ ] Performance tests completed
- [ ] Security tests passed
- [ ] User acceptance testing done
- [ ] Load testing completed
- [ ] Mobile testing verified

### 📚 Documentation

- [ ] README updated
- [ ] User documentation complete
- [ ] API documentation ready
- [ ] Deployment guide written
- [ ] Runbook created

### 🚀 Deployment

- [ ] Deployment pipeline configured
- [ ] Rollback plan ready
- [ ] DNS configured
- [ ] SSL certificate installed
- [ ] Monitoring alerts set up
- [ ] On-call rotation established

### 📊 Post-Launch

- [ ] Monitor error rates
- [ ] Track performance metrics
- [ ] Collect user feedback
- [ ] Plan first update cycle
- [ ] Schedule security reviews

---

## Quick Start Commands

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

### Testing

```bash
# Install test dependencies
pip install pytest pytest-cov pylint black

# Run tests
pytest tests/ --cov=SSO --cov=app

# Lint
pylint app.py SSO/

# Format
black app.py SSO/
```

### Deployment

```bash
# Docker build and run
docker build -t streamlit-sso .
docker run -p 8501:8501 --env-file .env streamlit-sso

# Docker Compose
docker-compose up -d
```

---

## Support & Resources

- **Azure AD Documentation**: https://docs.microsoft.com/azure/active-directory/
- **Streamlit Documentation**: https://docs.streamlit.io/
- **MSAL Python**: https://msal-python.readthedocs.io/
- **OWASP Security**: https://owasp.org/www-project-top-ten/

---

## Version Control

Keep track of major changes:

| Version | Date | Changes | Deployed By |
|---------|------|---------|-------------|
| 1.0.0 | YYYY-MM-DD | Initial production release | Name |
| 1.0.1 | YYYY-MM-DD | Security patch | Name |

---

**Remember**: Security and user experience are paramount. Don't rush to production - take time to properly test and validate everything!
