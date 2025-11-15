"""
Authentication Utilities for Multipage Apps

Provides helper functions and decorators for protecting pages with authentication.
"""

import streamlit as st
from functools import wraps


def require_authentication(func):
    """
    Decorator to protect pages that require authentication.

    Usage:
        @require_authentication
        def main():
            st.write("Protected content")

    If user is not authenticated, shows error message and hides other protected pages.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not st.session_state.get("authenticated", False):
            # Hide all pages except Home when blocked
            st.markdown("""
                <style>
                    [data-testid="stSidebarNav"] li:nth-child(n+2) {
                        display: none;
                    }
                </style>
            """, unsafe_allow_html=True)

            st.error("⚠️ You must be logged in to access this page.")
            st.info("👈 Please log in using the **Home** page from the sidebar.")
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def check_authentication():
    """
    Check if user is authenticated.

    Returns:
        bool: True if authenticated, False otherwise
    """
    return st.session_state.get("authenticated", False)


def get_user_info():
    """
    Get current user information from session state.

    Returns:
        dict: User information or None if not authenticated
    """
    if check_authentication():
        return st.session_state.get("user_info", {})
    return None


def get_user_name():
    """
    Get the current user's display name.

    Returns:
        str: User's name or "User" if not available
    """
    user_info = get_user_info()
    if user_info:
        return user_info.get("name", "User")
    return "User"


def get_user_email():
    """
    Get the current user's email.

    Returns:
        str: User's email or empty string if not available
    """
    user_info = get_user_info()
    if user_info:
        return user_info.get("preferred_username", "")
    return ""


def render_authenticated_header(page_title=None, show_logout=True):
    """
    Render a standard header for authenticated pages.

    Args:
        page_title (str, optional): Custom page title. If None, uses generic welcome
        show_logout (bool): Whether to show logout button. Default True.
    """
    col1, col2 = st.columns([5, 1])

    with col1:
        if page_title:
            st.title(page_title)
        user_name = get_user_name()
        st.write(f"👋 Welcome, **{user_name}**!")

    with col2:
        if show_logout:
            from .session import logout
            st.write("")  # Spacing
            if st.button("🚪 Logout", type="secondary", use_container_width=True):
                logout()


def show_authentication_warning():
    """
    Display a warning message for unauthenticated users trying to access protected pages.
    """
    st.warning("🔒 Authentication Required")
    st.write("This page requires authentication. Please log in to continue.")
    st.info("💡 Navigate to the **Home** page using the sidebar to log in.")
