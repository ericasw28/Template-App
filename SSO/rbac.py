"""
Role-Based Access Control (RBAC) Module

Provides role management and permission checking for Azure AD App Roles.
Integrates with Azure AD to enforce access control based on assigned roles.
"""

import streamlit as st
from functools import wraps
from enum import Enum
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Role(str, Enum):
    """
    Application roles that map to Azure AD App Roles.

    These roles should match exactly with the roles configured in Azure AD.
    """
    ADMIN = "Admin"
    SUPERUSER = "Superuser"
    USER = "User"


class Permission(str, Enum):
    """
    Application permissions that can be granted to roles.
    """
    VIEW_ANALYTICS = "view_analytics"
    VIEW_SETTINGS = "view_settings"
    MANAGE_USERS = "manage_users"
    EDIT_SETTINGS = "edit_settings"


# Role-Permission Mapping
ROLE_PERMISSIONS = {
    Role.ADMIN: [
        Permission.VIEW_ANALYTICS,
        Permission.VIEW_SETTINGS,
        Permission.MANAGE_USERS,
        Permission.EDIT_SETTINGS,
    ],
    Role.SUPERUSER: [
        Permission.VIEW_ANALYTICS,
        Permission.VIEW_SETTINGS,
        Permission.EDIT_SETTINGS,
    ],
    Role.USER: [
        Permission.VIEW_ANALYTICS,
    ],
}


def get_user_roles() -> List[str]:
    """
    Extract user roles from Azure AD token claims stored in session state.

    Azure AD includes roles in the 'roles' claim of the ID token.

    Returns:
        List[str]: List of role names assigned to the user
    """
    user_info = st.session_state.get("user_info", {})

    # Azure AD sends roles as a list in the 'roles' claim
    roles = user_info.get("roles", [])

    # Ensure roles is always a list
    if not isinstance(roles, list):
        roles = [roles] if roles else []

    logger.info(f"User roles extracted: {roles}")
    return roles


def get_highest_role() -> Optional[Role]:
    """
    Get the highest role assigned to the current user.

    Role hierarchy: Admin > Superuser > User

    Returns:
        Role: Highest role, or None if no role assigned
    """
    user_roles = get_user_roles()

    # Check in order of priority
    if Role.ADMIN in user_roles:
        return Role.ADMIN
    elif Role.SUPERUSER in user_roles:
        return Role.SUPERUSER
    elif Role.USER in user_roles:
        return Role.USER

    return None


def has_role(required_role: Role) -> bool:
    """
    Check if the current user has the specified role.

    Args:
        required_role (Role): The role to check for

    Returns:
        bool: True if user has the role, False otherwise
    """
    user_roles = get_user_roles()
    return required_role in user_roles


def has_any_role(required_roles: List[Role]) -> bool:
    """
    Check if the current user has any of the specified roles.

    Args:
        required_roles (List[Role]): List of roles to check

    Returns:
        bool: True if user has at least one of the roles
    """
    user_roles = get_user_roles()
    return any(role in user_roles for role in required_roles)


def has_permission(permission: Permission) -> bool:
    """
    Check if the current user has a specific permission.

    Args:
        permission (Permission): The permission to check

    Returns:
        bool: True if user has the permission through any of their roles
    """
    user_roles = get_user_roles()

    for role_str in user_roles:
        try:
            role = Role(role_str)
            if permission in ROLE_PERMISSIONS.get(role, []):
                return True
        except ValueError:
            logger.warning(f"Unknown role: {role_str}")
            continue

    return False


def require_role(*required_roles: Role):
    """
    Decorator to restrict page access to users with specific roles.

    Usage:
        @require_role(Role.ADMIN, Role.SUPERUSER)
        def main():
            st.write("Admin or Superuser only")

    Args:
        *required_roles: One or more Role values required to access the page
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # First check authentication
            if not st.session_state.get("authenticated", False):
                _show_auth_error()
                st.stop()

            # Then check role
            if not has_any_role(list(required_roles)):
                _show_permission_error(required_roles)
                st.stop()

            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_permission(*required_permissions: Permission):
    """
    Decorator to restrict page access to users with specific permissions.

    Usage:
        @require_permission(Permission.MANAGE_USERS)
        def main():
            st.write("Can manage users")

    Args:
        *required_permissions: One or more Permission values required
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # First check authentication
            if not st.session_state.get("authenticated", False):
                _show_auth_error()
                st.stop()

            # Check if user has all required permissions
            missing_permissions = [
                perm for perm in required_permissions
                if not has_permission(perm)
            ]

            if missing_permissions:
                _show_permission_error_for_permissions(missing_permissions)
                st.stop()

            return func(*args, **kwargs)
        return wrapper
    return decorator


def _show_auth_error():
    """Show authentication error message and hide sidebar pages."""
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] li:nth-child(n+2) {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

    st.error("⚠️ You must be logged in to access this page.")
    st.info("👈 Please log in using the **Home** page from the sidebar.")


def _show_permission_error(required_roles: tuple):
    """Show permission denied error for role-based access."""
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] li:nth-child(n+2) {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

    role_names = " or ".join([role.value for role in required_roles])

    st.error(f"🚫 Access Denied")
    st.warning(f"This page requires **{role_names}** role.")

    user_roles = get_user_roles()
    if user_roles:
        st.info(f"Your current role(s): **{', '.join(user_roles)}**")
    else:
        st.info("You have no roles assigned. Contact your administrator.")

    st.divider()
    st.caption("💡 If you believe this is an error, please contact your system administrator.")


def _show_permission_error_for_permissions(missing_permissions: list):
    """Show permission denied error for permission-based access."""
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] li:nth-child(n+2) {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

    perm_names = ", ".join([perm.value for perm in missing_permissions])

    st.error(f"🚫 Access Denied")
    st.warning(f"This page requires the following permission(s): **{perm_names}**")

    user_role = get_highest_role()
    if user_role:
        st.info(f"Your current role: **{user_role.value}**")
    else:
        st.info("You have no roles assigned. Contact your administrator.")

    st.divider()
    st.caption("💡 If you believe this is an error, please contact your system administrator.")


def get_accessible_pages() -> dict:
    """
    Get a mapping of pages that are accessible to the current user.

    Returns:
        dict: Dictionary with page names as keys and accessibility as boolean values
    """
    return {
        "Home": True,  # Always accessible
        "Analytics": has_permission(Permission.VIEW_ANALYTICS),
        "Settings": has_permission(Permission.VIEW_SETTINGS),
        "Users": has_permission(Permission.MANAGE_USERS),
    }


def render_role_badge():
    """
    Render a badge showing the user's current role in the UI.

    Useful for headers or sidebars to show role at a glance.
    """
    role = get_highest_role()

    if role:
        # Color coding for roles
        colors = {
            Role.ADMIN: "#FF4B4B",      # Red
            Role.SUPERUSER: "#FFA500",  # Orange
            Role.USER: "#0068C9",       # Blue
        }

        color = colors.get(role, "#666666")

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
                {role.value.upper()}
            </div>
        """, unsafe_allow_html=True)
