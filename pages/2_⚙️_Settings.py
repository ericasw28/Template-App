"""
Settings Page - Protected by Azure AD SSO with RBAC

This page allows users to manage their preferences and application settings.
Only accessible to Admin and Superuser roles (Users are blocked).
"""

import streamlit as st
from SSO import (
    init_session_state,
    render_authenticated_header,
    get_user_name,
    get_user_email,
    get_user_info,
    Role,
    require_role
)


@require_role(Role.ADMIN, Role.SUPERUSER)
def main():
    """Main function for settings page."""
    # Initialize session state FIRST
    init_session_state()

    st.set_page_config(
        page_title="Azure SSO App - Settings",
        page_icon="⚙️",
        layout="wide"
    )

    # Render header with logout button
    render_authenticated_header("⚙️ Settings", show_logout=True)

    st.divider()

    # Page description
    st.write("""
    Manage your preferences and application settings here.
    These settings are demonstration examples and don't persist between sessions.
    """)

    st.divider()

    # User Profile Section
    st.subheader("👤 User Profile")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(
            "https://via.placeholder.com/150",
            caption="Profile Picture",
            width=150
        )
        if st.button("Upload New Photo", use_container_width=True):
            st.info("Photo upload feature coming soon!")

    with col2:
        user_name = get_user_name()
        user_email = get_user_email()

        st.text_input("Display Name", value=user_name, disabled=True)
        st.text_input("Email", value=user_email, disabled=True)

        st.caption("📝 Profile information is managed by your Azure AD account")

    st.divider()

    # Appearance Settings
    st.subheader("🎨 Appearance")

    col1, col2 = st.columns(2)

    with col1:
        theme = st.selectbox(
            "Theme",
            ["Light", "Dark", "Auto"],
            help="Select your preferred theme"
        )

        language = st.selectbox(
            "Language",
            ["English", "French", "Spanish", "German"],
            help="Select your preferred language"
        )

    with col2:
        density = st.radio(
            "Display Density",
            ["Comfortable", "Compact", "Spacious"],
            help="Adjust the spacing of UI elements"
        )

        sidebar_default = st.checkbox(
            "Expand sidebar by default",
            value=True,
            help="Show sidebar expanded on page load"
        )

    st.divider()

    # Notification Settings
    st.subheader("🔔 Notifications")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Email Notifications**")
        email_updates = st.checkbox("Product updates", value=True)
        email_security = st.checkbox("Security alerts", value=True)
        email_newsletter = st.checkbox("Newsletter", value=False)

    with col2:
        st.write("**In-App Notifications**")
        push_mentions = st.checkbox("When someone mentions you", value=True)
        push_updates = st.checkbox("System updates", value=True)
        push_tips = st.checkbox("Tips and tricks", value=False)

    st.divider()

    # Privacy Settings
    st.subheader("🔒 Privacy & Security")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Session Management**")
        st.metric("Current Session", "24 hours", help="Time until automatic logout")

        if st.button("View Active Sessions", use_container_width=True):
            st.info("You are currently logged in from 1 device")

    with col2:
        st.write("**Data Privacy**")
        share_analytics = st.checkbox(
            "Share analytics data",
            value=True,
            help="Help improve the app by sharing anonymous usage data"
        )

        if st.button("Download My Data", use_container_width=True):
            st.info("Data export feature coming soon!")

    st.divider()

    # API & Integration Settings
    st.subheader("🔌 API & Integrations")

    with st.expander("API Access"):
        st.write("**API Key Management**")

        api_key = "sk_live_••••••••••••••••1234"
        col1, col2 = st.columns([3, 1])

        with col1:
            st.code(api_key, language=None)

        with col2:
            if st.button("Regenerate", use_container_width=True):
                st.warning("This will invalidate your current API key!")

        st.caption("🔒 Keep your API key secure. Never share it publicly.")

    with st.expander("Connected Services"):
        st.write("**Third-party Integrations**")

        services = [
            {"name": "Microsoft Teams", "status": "✅ Connected", "color": "green"},
            {"name": "Slack", "status": "❌ Not connected", "color": "red"},
            {"name": "GitHub", "status": "✅ Connected", "color": "green"}
        ]

        for service in services:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{service['name']}**")
            with col2:
                st.write(service['status'])
            with col3:
                button_label = "Disconnect" if service['color'] == "green" else "Connect"
                if st.button(button_label, key=service['name'], use_container_width=True):
                    st.info(f"{button_label} feature for {service['name']} coming soon!")

    st.divider()

    # Advanced Settings
    st.subheader("🔧 Advanced")

    with st.expander("Developer Options"):
        debug_mode = st.checkbox("Enable debug mode", value=False)

        if debug_mode:
            st.warning("⚠️ Debug mode exposes additional information. Use only for development.")

            st.write("**Session State:**")
            st.json({
                "authenticated": st.session_state.get("authenticated", False),
                "user_info_keys": list(get_user_info().keys()) if get_user_info() else []
            })

    with st.expander("Danger Zone"):
        st.error("⚠️ **Danger Zone** - Irreversible Actions")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Clear All Data", type="secondary", use_container_width=True):
                st.warning("This would clear all your app data!")

        with col2:
            if st.button("Delete Account", type="secondary", use_container_width=True):
                st.error("This would permanently delete your account!")

    st.divider()

    # Save Settings Button
    col1, col2, col3 = st.columns([2, 1, 2])

    with col2:
        if st.button("💾 Save Settings", type="primary", use_container_width=True):
            with st.spinner("Saving settings..."):
                import time
                time.sleep(1)
                st.success("✅ Settings saved successfully!")
                st.balloons()

    # Footer
    st.divider()
    st.caption("💡 **Note**: Settings on this page are for demonstration and don't persist between sessions.")
    st.caption("🔒 Your actual profile data is managed through your Azure AD account.")


if __name__ == "__main__":
    main()
