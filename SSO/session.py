"""
Session and Cookie Management Module

Handles Streamlit session state and cookie operations for authentication persistence.
"""

import json
import logging
import streamlit as st
from streamlit_cookies_controller import CookieController

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_cookie_controller():
    """
    Initialize and return a cookie controller instance.

    Note: Not cached because CookieController internally uses Streamlit widgets
    which cannot be used inside cached functions.

    Returns:
        CookieController: Cookie controller instance
    """
    return CookieController(key="auth_cookies")


def init_session_state():
    """
    Initialize session state, checking cookies first for persistent authentication.

    This function:
    - Cleans up old session-based cookies
    - Initializes session state defaults
    - Attempts to restore authentication from cookies
    """
    cookie_controller = get_cookie_controller()

    # Get all cookies
    cookies = cookie_controller.getAll()

    # Clean up old session-based cookies (from previous implementation)
    if not hasattr(st.session_state, '_cookies_cleaned'):
        for cookie_name in list(cookies.keys()):
            if cookie_name.startswith("session_"):
                cookie_controller.remove(cookie_name)
        st.session_state._cookies_cleaned = True
        logger.info("Cleaned up old session cookies")

    # Initialize defaults if not already done
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
    if "auth_code_processed" not in st.session_state:
        st.session_state.auth_code_processed = False

    # Try to restore from cookies if not already authenticated
    if not st.session_state.authenticated and cookies:
        auth_cookie = cookies.get("authenticated")
        user_info_cookie = cookies.get("user_info")

        if auth_cookie == "true" and user_info_cookie:
            try:
                st.session_state.authenticated = True
                st.session_state.user_info = json.loads(user_info_cookie)
                logger.info("Session restored from secure cookies")
            except (json.JSONDecodeError, TypeError) as e:
                # If cookie data is corrupted, clear everything for security
                logger.warning(f"Failed to restore session from cookies: {e}")
                st.session_state.authenticated = False
                st.session_state.user_info = None
                cookie_controller.remove("authenticated")
                cookie_controller.remove("user_info")


def logout():
    """
    Clear authentication state from both session and cookies, then reload the app.
    """
    cookie_controller = get_cookie_controller()

    # Clear session state
    st.session_state.authenticated = False
    st.session_state.user_info = None
    st.session_state.auth_code_processed = False

    # Remove cookies securely
    cookie_controller.remove("authenticated")
    cookie_controller.remove("user_info")

    logger.info("User logged out - session and cookies cleared")
    st.rerun()
