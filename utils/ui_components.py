"""
UI Components for Streamlit Azure AD SSO Application

This module contains all the UI rendering functions for the application,
separated from the main app logic for better maintainability.
"""

import streamlit as st
from SSO import (
    check_env_file,
    get_auth_url,
    get_user_name,
    get_user_email,
    logout,
    get_highest_role,
    render_role_badge
)


def render_config_error(missing_vars):
    """Render configuration error page with helpful instructions."""
    st.error("⚠️ Configuration Error")
    st.write("The following environment variables are missing or not set:")
    for var in missing_vars:
        st.code(var)

    st.divider()

    if not check_env_file():
        st.warning("📝 The `.env` file was not found in the current directory.")
        st.write("**To fix this:**")
        st.write("1. Copy `.env.example` to `.env`:")
        st.code("cp .env.example .env")
        st.write("2. Edit `.env` and add your Azure AD credentials")
    else:
        st.warning("📝 The `.env` file exists but variables are not set correctly.")
        st.write("**To fix this:**")
        st.write("1. Open your `.env` file")
        st.write("2. Make sure these variables are set with your actual Azure AD values:")
        st.code("""AZURE_CLIENT_ID=your_actual_client_id
AZURE_CLIENT_SECRET=your_actual_client_secret
AZURE_TENANT_ID=your_actual_tenant_id
REDIRECT_URI=http://localhost:8501""")

    st.divider()
    st.info("**Need help?** Check the README.md for detailed Azure AD setup instructions.")


def render_login_page():
    """Render the login page for unauthenticated users."""
    st.title("🏠 Welcome to Azure SSO App")
    st.write("This is a multipage Streamlit application with Azure AD authentication.")

    st.divider()

    st.subheader("🔐 Sign In")
    st.write("Please sign in with your Microsoft account to access all features.")

    auth_url = get_auth_url()

    col1, col2 = st.columns([2, 3])
    with col1:
        st.link_button(
            "Sign in with Microsoft",
            auth_url,
            type="primary",
            use_container_width=True
        )

    st.divider()

    st.subheader("✨ Features")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔒 Secure")
        st.write("Azure AD SSO authentication with secure session management")

    with col2:
        st.markdown("### 📄 Multipage")
        st.write("Multiple pages with authentication protection")

    with col3:
        st.markdown("### 🚀 Ready")
        st.write("Production-ready with logging and monitoring")

    with st.expander("🔗 Having trouble with the button?"):
        st.caption("Copy this link if the button doesn't work:")
        st.code(auth_url, language=None)


def render_dashboard():
    """Render the main dashboard for authenticated users."""
    # Header with logout
    col1, col2 = st.columns([5, 1])

    with col1:
        st.title("🏠 Dashboard")
        user_name = get_user_name()
        user_email = get_user_email()

        # Show user name and role badge
        col_name, col_role = st.columns([4, 1])
        with col_name:
            st.write(f"Welcome back, **{user_name}**! 👋")
        with col_role:
            render_role_badge()

        if user_email:
            st.caption(f"📧 {user_email}")

    with col2:
        st.write("")  # Spacing
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            logout()

    st.divider()

    # Success indicator
    st.success("✅ You are successfully logged in!")

    st.write("")

    # Dashboard content
    st.subheader("📊 Quick Stats")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Pages", "3", help="Total pages in this app")

    with col2:
        st.metric("Status", "Active", help="Current session status")

    with col3:
        st.metric("Session", "24h", help="Session duration")

    with col4:
        st.metric("Security", "High", help="Security level")

    st.divider()

    # Navigation guide
    st.subheader("🧭 Navigation")
    st.write("Use the sidebar to navigate between pages:")

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **📄 Page 2 - Analytics**

        View analytics and data visualizations.
        Protected by authentication.
        """)

    with col2:
        st.info("""
        **⚙️ Page 3 - Settings**

        Manage your preferences and settings.
        Protected by authentication.
        """)

    st.divider()

    # User info section
    with st.expander("🔍 View Your Profile Information"):
        if st.session_state.user_info:
            st.json(st.session_state.user_info)
        else:
            st.write("No user information available.")

    # Helpful tips
    st.divider()
    st.caption("💡 **Tip**: Your session will persist for 24 hours or until you log out.")
