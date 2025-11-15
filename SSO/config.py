"""
Azure AD Configuration Module

Handles loading and validating Azure AD configuration from environment variables
and Streamlit Cloud secrets.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try to import streamlit for secrets support (for Streamlit Cloud deployment)
try:
    import streamlit as st
    _streamlit_available = True
except ImportError:
    _streamlit_available = False

# Azure AD Configuration
# Support both environment variables (.env) and Streamlit secrets
def _get_config(key, default=None):
    """Get configuration from environment or Streamlit secrets."""
    # First try environment variables
    value = os.getenv(key)

    # If not found and Streamlit is available, try secrets
    if value is None and _streamlit_available:
        try:
            value = st.secrets.get(key, default)
        except (AttributeError, FileNotFoundError):
            value = default

    return value if value else default

CLIENT_ID = _get_config("AZURE_CLIENT_ID")
CLIENT_SECRET = _get_config("AZURE_CLIENT_SECRET")
TENANT_ID = _get_config("AZURE_TENANT_ID")
REDIRECT_URI = _get_config("REDIRECT_URI", "http://localhost:8501")

# Azure AD Authority and Scope
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["User.Read"]


def validate_config():
    """
    Check if all required environment variables are set.

    Returns:
        tuple: (bool, list) - (is_valid, missing_variables)
    """
    missing_vars = []

    if not CLIENT_ID:
        missing_vars.append("AZURE_CLIENT_ID")
    if not CLIENT_SECRET:
        missing_vars.append("AZURE_CLIENT_SECRET")
    if not TENANT_ID:
        missing_vars.append("AZURE_TENANT_ID")

    if missing_vars:
        return False, missing_vars
    return True, []


def check_env_file():
    """
    Check if .env file exists in the current directory.

    Returns:
        bool: True if .env file exists, False otherwise
    """
    env_path = Path(".env")
    return env_path.exists()
