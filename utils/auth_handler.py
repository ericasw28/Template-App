"""
Authentication Handler for Streamlit Azure AD SSO Application

This module contains the authentication flow logic and callback handling,
separated from the main app logic for better maintainability.
"""

import streamlit as st
from SSO import handle_auth_callback, get_cookie_controller


def handle_auth_flow():
    """Handle the authentication flow and callback processing."""
    query_params = st.query_params

    if "code" in query_params and not st.session_state.authenticated and not st.session_state.auth_code_processed:
        st.session_state.auth_code_processed = True

        auth_code = query_params["code"]

        with st.spinner("Authenticating..."):
            try:
                cookie_controller = get_cookie_controller()
                if handle_auth_callback(auth_code, cookie_controller):
                    st.query_params.clear()
                    st.rerun()
                else:
                    st.error("❌ Authentication failed. Please try again.")
                    st.session_state.auth_code_processed = False
                    st.stop()
            except Exception as e:
                st.error(f"❌ Authentication error: {str(e)}")
                st.session_state.auth_code_processed = False
                st.stop()
