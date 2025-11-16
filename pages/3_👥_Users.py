"""
Users Management Page - Admin Only (Read-Only Dashboard)

This page displays users and their roles from Azure AD.
Role management is done in Azure AD portal (Enterprise Applications).
Only accessible to users with the Admin role.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from SSO import (
    init_session_state,
    render_authenticated_header,
    Role,
    require_role
)
from SSO.graph_api import get_cached_users, is_graph_api_configured


@require_role(Role.ADMIN)
def main():
    """Main function for users management page."""
    # Initialize session state FIRST
    init_session_state()

    st.set_page_config(
        page_title="Azure SSO App - Users",
        page_icon="👥",
        layout="wide"
    )

    # Render header with logout button
    render_authenticated_header("👥 Users Management", show_logout=True)

    st.divider()

    # Admin notice
    st.info("🔐 **Admin Access** - This page displays users from Azure AD. Role management is done in Azure AD portal.")

    st.divider()

    # Check if Graph API is configured
    if not is_graph_api_configured():
        st.warning("⚠️ **Graph API Not Configured**")
        st.write("""
        To display real user data, you need to configure Microsoft Graph API permissions.

        **Setup Steps:**
        1. Go to Azure AD → App registrations → Your App → API permissions
        2. Add permissions: `User.Read.All` and `Application.Read.All`
        3. Grant admin consent for your organization

        For now, showing sample data.
        """)
        display_sample_data()
        return

    # Fetch real users from Azure AD
    with st.spinner("Loading users from Azure AD..."):
        users = get_cached_users(top=100)

    if not users:
        st.error("❌ Failed to fetch users from Azure AD")
        st.write("Possible reasons:")
        st.write("- Graph API permissions not granted")
        st.write("- Admin consent not provided")
        st.write("- Network connectivity issues")
        st.divider()
        st.write("**Showing sample data instead:**")
        display_sample_data()
        return

    # Display real user data
    display_real_users(users)


def display_real_users(users):
    """Display real users from Azure AD."""

    # User Statistics
    st.subheader("📊 User Statistics")

    col1, col2, col3, col4 = st.columns(4)

    active_users = [u for u in users if u.get("accountEnabled", False)]

    with col1:
        st.metric(
            "Total Users",
            len(users),
            help="Total users in Azure AD"
        )

    with col2:
        st.metric(
            "Active Users",
            len(active_users),
            delta=f"{int(len(active_users)/len(users)*100)}%",
            help="Users with enabled accounts"
        )

    with col3:
        st.metric(
            "Disabled",
            len(users) - len(active_users),
            help="Users with disabled accounts"
        )

    with col4:
        # Link to Azure AD
        if st.button("🔗 Open Azure AD Portal", use_container_width=True):
            st.link_button(
                "Go to Enterprise Applications",
                "https://portal.azure.com/#view/Microsoft_AAD_IAM/StartboardApplicationsMenuBlade/~/AppAppsPreview",
                use_container_width=True
            )

    st.divider()

    # User Directory
    st.subheader("👥 User Directory")

    # Search and filter
    col1, col2 = st.columns([3, 1])

    with col1:
        search_query = st.text_input("🔍 Search users", placeholder="Search by name or email...")

    with col2:
        show_disabled = st.checkbox("Show disabled accounts", value=False)

    st.divider()

    # Filter users
    filtered_users = users

    if not show_disabled:
        filtered_users = [u for u in filtered_users if u.get("accountEnabled", False)]

    if search_query:
        search_lower = search_query.lower()
        filtered_users = [
            u for u in filtered_users
            if search_lower in u.get("displayName", "").lower()
            or search_lower in u.get("mail", "").lower()
            or search_lower in u.get("userPrincipalName", "").lower()
        ]

    # Display users in table format
    if filtered_users:
        # Create DataFrame
        users_df = pd.DataFrame([
            {
                "Display Name": u.get("displayName", "N/A"),
                "Email": u.get("mail") or u.get("userPrincipalName", "N/A"),
                "Status": "✅ Active" if u.get("accountEnabled") else "❌ Disabled",
                "User ID": u.get("id", "N/A")
            }
            for u in filtered_users
        ])

        st.dataframe(
            users_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Display Name": st.column_config.TextColumn("Name", width="medium"),
                "Email": st.column_config.TextColumn("Email", width="large"),
                "Status": st.column_config.TextColumn("Status", width="small"),
                "User ID": st.column_config.TextColumn("Azure AD ID", width="medium"),
            }
        )

        st.caption(f"Showing {len(filtered_users)} of {len(users)} users")
    else:
        st.info("No users match your search criteria")

    st.divider()

    # Role Management Section
    st.subheader("🎭 Role Management")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**How to Assign Roles**")

        st.write("""
        1. Go to [Azure Portal](https://portal.azure.com)
        2. Navigate to **Azure AD** → **Enterprise applications**
        3. Find and select your application
        4. Click **Users and groups**
        5. Click **+ Add user/group**
        6. Select user and assign role (Admin, Superuser, or User)
        """)

        if st.button("📖 View Full Documentation", use_container_width=True):
            st.info("See AZURE_AD_RBAC_SETUP.md for detailed instructions")

    with col2:
        st.write("**Role Definitions**")

        roles_info = {
            "🔴 Admin": {
                "permissions": ["View Analytics", "View Settings", "Manage Users", "Edit Settings"],
                "description": "Full system access"
            },
            "🟠 Superuser": {
                "permissions": ["View Analytics", "View Settings", "Edit Settings"],
                "description": "All features except user management"
            },
            "🔵 User": {
                "permissions": ["View Analytics"],
                "description": "Limited access"
            }
        }

        for role_name, info in roles_info.items():
            with st.expander(role_name):
                st.write(f"**{info['description']}**")
                st.write("**Permissions:**")
                for perm in info['permissions']:
                    st.write(f"- ✅ {perm}")

    st.divider()

    # Quick Actions
    st.subheader("🔗 Quick Links")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.link_button(
            "🏢 Enterprise Applications",
            "https://portal.azure.com/#view/Microsoft_AAD_IAM/StartboardApplicationsMenuBlade/~/AppAppsPreview",
            use_container_width=True,
            help="Manage app role assignments"
        )

    with col2:
        st.link_button(
            "👥 Azure AD Users",
            "https://portal.azure.com/#view/Microsoft_AAD_UsersAndTenants/UserManagementMenuBlade/~/AllUsers",
            use_container_width=True,
            help="View all Azure AD users"
        )

    with col3:
        st.link_button(
            "📊 App Roles",
            "https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationMenuBlade/~/AppRoles",
            use_container_width=True,
            help="Manage app role definitions"
        )

    # Footer
    st.divider()
    st.caption(f"📅 Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption("💡 **Note**: User data is cached for 5 minutes. Click browser refresh to update.")
    st.caption("🔒 **Security**: This page only displays data. All role assignments must be done in Azure AD portal.")


def display_sample_data():
    """Display sample data when Graph API is not configured."""

    st.subheader("📊 Sample Data")
    st.caption("This is demonstration data. Configure Graph API to see real users.")

    # Sample users
    sample_users = pd.DataFrame({
        'Display Name': [
            'Alice Johnson',
            'Bob Smith',
            'Carol Williams',
            'David Brown',
            'Eve Davis'
        ],
        'Email': [
            'alice.johnson@company.com',
            'bob.smith@company.com',
            'carol.williams@company.com',
            'david.brown@company.com',
            'eve.davis@company.com'
        ],
        'Role': [
            '🔴 Admin',
            '🔴 Admin',
            '🟠 Superuser',
            '🟠 Superuser',
            '🔵 User'
        ],
        'Status': [
            '✅ Active',
            '✅ Active',
            '✅ Active',
            '✅ Active',
            '✅ Active'
        ]
    })

    st.dataframe(
        sample_users,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.info("""
    **To see real data:**

    1. Configure Graph API permissions in Azure AD
    2. Add `User.Read.All` permission
    3. Grant admin consent
    4. Restart the app

    See `GRAPH_API_SETUP.md` for detailed instructions.
    """)


if __name__ == "__main__":
    main()
