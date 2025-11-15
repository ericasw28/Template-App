"""
Streamlit Multipage Application with Azure AD SSO

Home page that handles authentication and serves as the dashboard.
Navigate to other pages using the sidebar after logging in.
"""

import streamlit as st
from SSO import validate_config, init_session_state, has_permission, Permission
from utils.ui_components import render_config_error, render_login_page, render_dashboard
from utils.auth_handler import handle_auth_flow


def main():
    """Main application entry point."""
    # Initialize session state FIRST (before set_page_config)
    init_session_state()

    # Dynamically set which pages are visible based on authentication
    if st.session_state.authenticated:
        # Show all pages when authenticated
        page_config = {
            "page_title": "Azure SSO App - Home",
            "page_icon": "🏠",
            "layout": "wide",
            "initial_sidebar_state": "expanded"
        }
    else:
        # Hide protected pages when not authenticated
        page_config = {
            "page_title": "Azure SSO App - Home",
            "page_icon": "🏠",
            "layout": "wide",
            "initial_sidebar_state": "collapsed"
        }

    st.set_page_config(**page_config)

    # Rename "app" to "🏠 Home" in sidebar and apply role-based visibility
    if not st.session_state.authenticated:
        st.markdown("""
            <style>
                /* Hide protected pages when not authenticated */
                [data-testid="stSidebarNav"] li:nth-child(n+2) {
                    display: none;
                }
                /* Rename the home page from 'app' to '🏠 Home' */
                [data-testid="stSidebarNav"] li:first-child a span {
                    display: none;
                }
                [data-testid="stSidebarNav"] li:first-child a::after {
                    content: "🏠 Home";
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        # Apply role-based page visibility when authenticated
        hide_settings = not has_permission(Permission.VIEW_SETTINGS)
        hide_users = not has_permission(Permission.MANAGE_USERS)

        # Build CSS to hide pages based on permissions
        # Page order: Home (1), Analytics (2), Settings (3), Users (4)
        hide_css = ""

        if hide_settings and hide_users:
            # Hide both Settings and Users (pages 3 and 4)
            hide_css = """
                [data-testid="stSidebarNav"] li:nth-child(3),
                [data-testid="stSidebarNav"] li:nth-child(4) {
                    display: none;
                }
            """
        elif hide_settings:
            # Hide only Settings (page 3)
            hide_css = """
                [data-testid="stSidebarNav"] li:nth-child(3) {
                    display: none;
                }
            """
        elif hide_users:
            # Hide only Users (page 4)
            hide_css = """
                [data-testid="stSidebarNav"] li:nth-child(4) {
                    display: none;
                }
            """

        st.markdown(f"""
            <style>
                /* Rename the home page from 'app' to '🏠 Home' */
                [data-testid="stSidebarNav"] li:first-child a span {{
                    display: none;
                }}
                [data-testid="stSidebarNav"] li:first-child a::after {{
                    content: "🏠 Home";
                }}
                {hide_css}
            </style>
        """, unsafe_allow_html=True)

    # Validate configuration
    config_valid, missing_vars = validate_config()

    if not config_valid:
        render_config_error(missing_vars)
        st.stop()

    # Handle authentication flow
    handle_auth_flow()

    # Render appropriate page based on authentication status
    if not st.session_state.authenticated:
        render_login_page()
    else:
        render_dashboard()


if __name__ == "__main__":
    main()
