"""
MSAL Authentication Module

Handles Microsoft Authentication Library (MSAL) operations for Azure AD SSO.
"""

import json
import logging
import msal
import streamlit as st
from .config import (
    CLIENT_ID,
    CLIENT_SECRET,
    AUTHORITY,
    SCOPE,
    REDIRECT_URI
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_msal_app():
    """
    Initialize and return MSAL Confidential Client Application.

    Returns:
        msal.ConfidentialClientApplication: Configured MSAL app instance
    """
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
    )


def get_auth_url():
    """
    Generate Azure AD authentication URL for user login.

    Returns:
        str: Authentication URL to redirect users to Microsoft login
    """
    msal_app = get_msal_app()
    auth_url = msal_app.get_authorization_request_url(
        SCOPE,
        redirect_uri=REDIRECT_URI,
    )
    return auth_url


def handle_auth_callback(auth_code, cookie_controller):
    """
    Handle the authentication callback from Azure AD.

    Exchanges the authorization code for an access token and stores
    user information in session state and cookies.

    Args:
        auth_code (str): Authorization code received from Azure AD
        cookie_controller: Streamlit cookie controller instance

    Returns:
        bool: True if authentication successful, False otherwise
    """
    try:
        msal_app = get_msal_app()
        result = msal_app.acquire_token_by_authorization_code(
            auth_code,
            scopes=SCOPE,
            redirect_uri=REDIRECT_URI,
        )

        if "access_token" in result:
            st.session_state.authenticated = True
            st.session_state.user_info = result.get("id_token_claims", {})

            # Store authentication state in cookies with secure settings
            # Production: 24 hours, secure cookies for HTTPS, strict same-site policy
            try:
                cookie_controller.set(
                    "authenticated",
                    "true",
                    max_age=86400,      # 24 hours instead of 7 days
                    secure=True,        # Only transmit over HTTPS
                    samesite="Strict"   # Prevent CSRF attacks
                )
                cookie_controller.set(
                    "user_info",
                    json.dumps(st.session_state.user_info),
                    max_age=86400,      # 24 hours instead of 7 days
                    secure=True,        # Only transmit over HTTPS
                    samesite="Strict"   # Prevent CSRF attacks
                )
                logger.info("Authentication successful - secure cookies set")
            except Exception as e:
                # Production: Use proper logging instead of displaying to user
                logger.error(f"Error setting cookies: {e}")

            return True
        else:
            # Log the error server-side, show user-friendly message
            error = result.get("error", "Unknown error")
            error_description = result.get("error_description", "No description")
            logger.error(f"Authentication failed: {error} - {error_description}")

            st.error("Authentication failed. Please try again or contact support.")
            return False
    except Exception as e:
        # Log full error server-side, show generic message to user
        logger.error(f"Exception during authentication: {str(e)}", exc_info=True)

        st.error("An error occurred during authentication. Please try again later.")
        return False
