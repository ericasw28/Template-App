"""
SSO Authentication Package for Streamlit Applications

This package provides Azure AD SSO authentication functionality for Streamlit apps.
"""

from .config import (
    validate_config,
    check_env_file,
    CLIENT_ID,
    CLIENT_SECRET,
    TENANT_ID,
    REDIRECT_URI,
    AUTHORITY,
    SCOPE
)
from .auth import (
    get_msal_app,
    get_auth_url,
    handle_auth_callback
)
from .session import (
    get_cookie_controller,
    init_session_state,
    logout
)
from .auth_utils import (
    require_authentication,
    check_authentication,
    get_user_info,
    get_user_name,
    get_user_email,
    render_authenticated_header,
    show_authentication_warning
)
from .rbac import (
    Role,
    Permission,
    get_user_roles,
    get_highest_role,
    has_role,
    has_any_role,
    has_permission,
    require_role,
    require_permission,
    get_accessible_pages,
    render_role_badge
)

__all__ = [
    'validate_config',
    'check_env_file',
    'CLIENT_ID',
    'CLIENT_SECRET',
    'TENANT_ID',
    'REDIRECT_URI',
    'AUTHORITY',
    'SCOPE',
    'get_msal_app',
    'get_auth_url',
    'handle_auth_callback',
    'get_cookie_controller',
    'init_session_state',
    'logout',
    'require_authentication',
    'check_authentication',
    'get_user_info',
    'get_user_name',
    'get_user_email',
    'render_authenticated_header',
    'show_authentication_warning',
    'Role',
    'Permission',
    'get_user_roles',
    'get_highest_role',
    'has_role',
    'has_any_role',
    'has_permission',
    'require_role',
    'require_permission',
    'get_accessible_pages',
    'render_role_badge'
]
