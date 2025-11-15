"""
Users Management Page - Admin Only

This page allows administrators to manage users and their roles.
Only accessible to users with the Admin role.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from SSO import (
    init_session_state,
    render_authenticated_header,
    Role,
    require_role,
    get_user_roles,
    render_role_badge
)


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
    st.info("🔐 **Admin Access** - This page is only visible to administrators.")

    st.divider()

    # Page description
    st.write("""
    Manage user accounts, roles, and permissions.
    This is a demonstration page showing how role-based access control works.
    """)

    st.divider()

    # User Statistics
    st.subheader("📊 User Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Users",
            "47",
            delta="3 this week",
            help="Total registered users in the system"
        )

    with col2:
        st.metric(
            "Active Users",
            "42",
            delta="89%",
            help="Users active in the last 30 days"
        )

    with col3:
        st.metric(
            "Admins",
            "3",
            help="Users with Admin role"
        )

    with col4:
        st.metric(
            "Pending Invites",
            "5",
            help="Outstanding user invitations"
        )

    st.divider()

    # User Management Section
    st.subheader("👥 User Directory")

    # Add user button
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search_query = st.text_input("🔍 Search users", placeholder="Search by name or email...")

    with col2:
        role_filter = st.selectbox(
            "Filter by Role",
            ["All Roles", "Admin", "Superuser", "User"]
        )

    with col3:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("➕ Add New User", type="primary", use_container_width=True):
            st.info("Add user feature would open a dialog to create/invite a new user")

    st.divider()

    # Sample users data
    users_data = pd.DataFrame({
        'Name': [
            'Alice Johnson',
            'Bob Smith',
            'Carol Williams',
            'David Brown',
            'Eve Davis',
            'Frank Miller',
            'Grace Wilson',
            'Henry Moore'
        ],
        'Email': [
            'alice.johnson@company.com',
            'bob.smith@company.com',
            'carol.williams@company.com',
            'david.brown@company.com',
            'eve.davis@company.com',
            'frank.miller@company.com',
            'grace.wilson@company.com',
            'henry.moore@company.com'
        ],
        'Role': [
            'Admin',
            'Admin',
            'Superuser',
            'Superuser',
            'User',
            'User',
            'User',
            'User'
        ],
        'Last Login': [
            '2 hours ago',
            '5 hours ago',
            '1 day ago',
            '3 days ago',
            '1 week ago',
            '2 weeks ago',
            '3 weeks ago',
            '1 month ago'
        ],
        'Status': [
            'Active',
            'Active',
            'Active',
            'Active',
            'Active',
            'Inactive',
            'Inactive',
            'Active'
        ]
    })

    # Display users in a more interactive way
    for idx, user in users_data.iterrows():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 3, 2, 2, 2])

            with col1:
                st.write(f"**{user['Name']}**")

            with col2:
                st.write(user['Email'])

            with col3:
                # Role badge with color coding
                role_colors = {
                    'Admin': '#FF4B4B',
                    'Superuser': '#FFA500',
                    'User': '#0068C9'
                }
                color = role_colors.get(user['Role'], '#666666')
                st.markdown(f"""
                    <div style="
                        display: inline-block;
                        padding: 4px 12px;
                        background-color: {color};
                        color: white;
                        border-radius: 12px;
                        font-size: 12px;
                        font-weight: bold;
                    ">
                        {user['Role'].upper()}
                    </div>
                """, unsafe_allow_html=True)

            with col4:
                status_icon = "🟢" if user['Status'] == 'Active' else "🔴"
                st.write(f"{status_icon} {user['Status']}")

            with col5:
                if st.button("Edit", key=f"edit_{idx}", use_container_width=True):
                    st.info(f"Edit dialog for {user['Name']} would open here")

            st.caption(f"Last login: {user['Last Login']}")
            st.divider()

    st.divider()

    # Role Management Section
    st.subheader("🎭 Role Management")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Role Definitions**")

        roles_info = {
            "Admin": {
                "description": "Full system access including user management",
                "permissions": ["View Analytics", "View Settings", "Manage Users", "Edit Settings"],
                "count": 3
            },
            "Superuser": {
                "description": "Access to all features except user management",
                "permissions": ["View Analytics", "View Settings", "Edit Settings"],
                "count": 2
            },
            "User": {
                "description": "Standard user with limited access",
                "permissions": ["View Analytics"],
                "count": 42
            }
        }

        for role_name, info in roles_info.items():
            with st.expander(f"{role_name} ({info['count']} users)"):
                st.write(f"**Description:** {info['description']}")
                st.write("**Permissions:**")
                for perm in info['permissions']:
                    st.write(f"- ✅ {perm}")

    with col2:
        st.write("**Quick Actions**")

        if st.button("📊 Generate User Report", use_container_width=True):
            st.success("User report generated! Download link would appear here.")

        if st.button("📧 Send Bulk Invitation", use_container_width=True):
            st.info("Bulk invitation dialog would open here")

        if st.button("🔄 Sync with Azure AD", use_container_width=True):
            with st.spinner("Syncing with Azure AD..."):
                import time
                time.sleep(2)
                st.success("✅ Sync completed! All roles are up to date.")

        if st.button("📜 View Audit Log", use_container_width=True):
            st.info("Audit log viewer would open here")

    st.divider()

    # Recent Activity
    st.subheader("📋 Recent User Activity")

    activity_data = pd.DataFrame({
        'Timestamp': pd.date_range(end=datetime.now(), periods=8, freq='H')[::-1],
        'User': [
            'alice.johnson@company.com',
            'bob.smith@company.com',
            'carol.williams@company.com',
            'alice.johnson@company.com',
            'david.brown@company.com',
            'eve.davis@company.com',
            'bob.smith@company.com',
            'frank.miller@company.com'
        ],
        'Action': [
            'User role changed',
            'Login',
            'Login',
            'New user created',
            'Settings updated',
            'Login',
            'Password reset',
            'Account activated'
        ],
        'Performed By': [
            'alice.johnson@company.com',
            'System',
            'System',
            'alice.johnson@company.com',
            'david.brown@company.com',
            'System',
            'bob.smith@company.com',
            'alice.johnson@company.com'
        ]
    })

    st.dataframe(
        activity_data,
        use_container_width=True,
        hide_index=True
    )

    # Footer
    st.divider()
    st.caption(f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption("💡 **Note**: This is a demonstration page. In production, this would integrate with your actual user management system.")


if __name__ == "__main__":
    main()
