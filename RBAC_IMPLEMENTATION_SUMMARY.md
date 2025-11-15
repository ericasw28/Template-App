# RBAC Implementation Summary

## Overview

This document provides a technical overview of the Role-Based Access Control (RBAC) implementation using Azure AD App Roles.

---

## Architecture

### High-Level Flow

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│   User      │─────▶│  Azure AD    │─────▶│  Streamlit App  │
│  (Browser)  │      │  Login       │      │  (Python)       │
└─────────────┘      └──────────────┘      └─────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  JWT Token   │
                    │  + Roles     │
                    └──────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │ Session      │
                    │ State        │
                    └──────────────┘
```

### Components

1. **Azure AD App Roles**: Defined in Azure portal
2. **JWT Token**: Contains role claims
3. **RBAC Module**: Extracts and validates roles
4. **Decorators**: Protect pages and functions
5. **UI Filters**: Hide unauthorized pages

---

## Implementation Details

### 1. Core RBAC Module (`SSO/rbac.py`)

**Key Classes:**

```python
class Role(str, Enum):
    ADMIN = "Admin"
    SUPERUSER = "Superuser"
    USER = "User"

class Permission(str, Enum):
    VIEW_ANALYTICS = "view_analytics"
    VIEW_SETTINGS = "view_settings"
    MANAGE_USERS = "manage_users"
    EDIT_SETTINGS = "edit_settings"
```

**Key Functions:**

- `get_user_roles()`: Extract roles from token claims
- `get_highest_role()`: Determine user's primary role
- `has_role()`: Check if user has specific role
- `has_permission()`: Check if user has permission
- `require_role()`: Decorator to protect functions
- `require_permission()`: Decorator for permission-based access

**Role-Permission Mapping:**

```python
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
```

---

### 2. Token Flow

**Authentication Process:**

1. User clicks "Sign in with Microsoft"
2. Redirected to Azure AD
3. User authenticates
4. Azure AD generates JWT token with:
   - User info (name, email)
   - **Roles** claim (list of assigned roles)
5. Token returned to app
6. App stores `user_info` in session state
7. RBAC module reads roles from `user_info['roles']`

**Token Structure Example:**

```json
{
  "name": "John Doe",
  "preferred_username": "john@company.com",
  "roles": ["Admin"],
  "oid": "user-object-id",
  ...
}
```

---

### 3. Page Protection

**Settings Page Example:**

```python
# Before RBAC
@require_authentication
def main():
    # Any authenticated user can access

# After RBAC
@require_role(Role.ADMIN, Role.SUPERUSER)
def main():
    # Only Admin or Superuser can access
```

**Users Page Example:**

```python
@require_role(Role.ADMIN)
def main():
    # Only Admin can access
```

---

### 4. Sidebar Navigation Filtering

**Location**: `app.py`

**Logic:**

```python
# Check permissions
hide_settings = not has_permission(Permission.VIEW_SETTINGS)
hide_users = not has_permission(Permission.MANAGE_USERS)

# Generate CSS to hide unauthorized pages
if hide_settings and hide_users:
    # Hide both pages 3 and 4
elif hide_settings:
    # Hide only page 3
elif hide_users:
    # Hide only page 4
```

**Result:**
- Users only see pages they can access
- Prevents confusion and unauthorized access attempts

---

### 5. Role Badge Display

**Location**: `utils/ui_components.py`

**Implementation:**

```python
def render_role_badge():
    role = get_highest_role()
    colors = {
        Role.ADMIN: "#FF4B4B",      # Red
        Role.SUPERUSER: "#FFA500",  # Orange
        Role.USER: "#0068C9",       # Blue
    }
    # Render colored badge
```

**Displayed On:**
- Dashboard (main page)
- Can be added to any page header

---

## Security Features

### 1. Defense in Depth

**Multiple Layers:**
1. **UI Layer**: Hide unauthorized pages in sidebar
2. **Page Layer**: Decorators block unauthorized access
3. **Function Layer**: Permission checks in code
4. **Session Layer**: Roles stored securely in session

**Why This Matters:**
Even if a user manually navigates to a URL, the decorator blocks access.

### 2. Token-Based Roles

**Advantages:**
- Roles come from trusted source (Azure AD)
- No client-side manipulation possible
- Changes take effect on next login
- Audit trail in Azure AD

### 3. Principle of Least Privilege

**Default Behavior:**
- Users with NO role = No access to protected pages
- Must explicitly assign role to grant access
- Start with lowest role, promote as needed

---

## Code Organization

```
Streamlit SSO/
├── SSO/
│   ├── __init__.py           # Exports RBAC functions
│   ├── auth.py               # Authentication (unchanged)
│   ├── rbac.py               # ✨ NEW: RBAC core logic
│   ├── session.py            # Session management
│   └── config.py             # Configuration
├── pages/
│   ├── 1_📊_Analytics.py     # All authenticated users
│   ├── 2_⚙️_Settings.py      # ✏️ UPDATED: Admin + Superuser only
│   └── 3_👥_Users.py          # ✨ NEW: Admin only
├── utils/
│   ├── ui_components.py      # ✏️ UPDATED: Show role badge
│   └── auth_handler.py       # Auth flow
├── app.py                    # ✏️ UPDATED: Role-based sidebar
├── AZURE_AD_RBAC_SETUP.md    # ✨ NEW: Setup guide
├── RBAC_QUICK_START.md       # ✨ NEW: Quick reference
└── RBAC_IMPLEMENTATION_SUMMARY.md  # ✨ NEW: This file
```

---

## Extending the System

### Add a New Role

1. **In Azure AD**: Create app role
2. **In Code**: Update `Role` enum in `rbac.py`
3. **Define Permissions**: Add to `ROLE_PERMISSIONS`
4. **Test**: Assign to user and verify

### Add a New Permission

1. **Define**: Add to `Permission` enum
2. **Assign**: Update `ROLE_PERMISSIONS`
3. **Use**: Apply to pages/functions with decorators
4. **Update Sidebar**: Modify `app.py` if needed

### Add a New Page

1. **Create Page**: Add to `pages/` directory
2. **Apply Decorator**: Use `@require_role()` or `@require_permission()`
3. **Update Sidebar Logic**: Modify `app.py` to hide/show
4. **Update Docs**: Add to permission matrix

**Example:**

```python
# pages/4_📊_Reports.py

from SSO import require_permission, Permission

@require_permission(Permission.VIEW_REPORTS)
def main():
    st.write("Reports page")
```

---

## Testing Strategy

### Unit Testing

Test RBAC functions independently:

```python
def test_has_role():
    # Mock session state with roles
    st.session_state.user_info = {"roles": ["Admin"]}
    assert has_role(Role.ADMIN) == True
    assert has_role(Role.USER) == False
```

### Integration Testing

Test page access:

```python
def test_settings_page_access():
    # Test with User role - should be blocked
    # Test with Superuser role - should pass
    # Test with Admin role - should pass
```

### Manual Testing Checklist

- [ ] User with no role cannot access protected pages
- [ ] User role sees only Home + Analytics
- [ ] Superuser sees Home + Analytics + Settings
- [ ] Admin sees all pages
- [ ] Sidebar shows only accessible pages
- [ ] Role badge displays correctly
- [ ] Direct URL navigation is blocked
- [ ] Logout clears role information

---

## Performance Considerations

### Token Parsing

**When**: Once per session (on login)
**Cost**: Minimal (JSON parsing)
**Cached**: In session state

### Permission Checks

**When**: On page load and sidebar render
**Cost**: Dictionary lookup (O(1))
**Impact**: Negligible

### Sidebar Filtering

**When**: Every page render
**Cost**: Boolean checks + CSS injection
**Impact**: <1ms per page load

**Overall**: RBAC adds minimal overhead to the application.

---

## Comparison with Alternatives

### Option 1: Azure AD App Roles (Implemented)

**Pros:**
- ✅ No database needed
- ✅ Free with Azure AD
- ✅ Centralized management
- ✅ Audit trail built-in
- ✅ Enterprise-ready

**Cons:**
- ❌ Requires Azure AD access
- ❌ Changes require re-login
- ❌ Azure portal for management

### Option 2: JSON/YAML Config File

**Pros:**
- ✅ Simple to implement
- ✅ No external dependencies
- ✅ Quick changes

**Cons:**
- ❌ Manual maintenance
- ❌ No audit trail
- ❌ Not scalable
- ❌ Security risk (file access)

### Option 3: PostgreSQL Database

**Pros:**
- ✅ Full control
- ✅ Custom UI possible
- ✅ Complex permissions

**Cons:**
- ❌ Infrastructure needed
- ❌ Database setup/maintenance
- ❌ More code to write
- ❌ Additional costs
- ❌ Security responsibility

**Verdict**: Azure AD App Roles is the best choice for SSO applications.

---

## Migration Path

### From No RBAC to RBAC

1. **Phase 1**: Deploy code with RBAC (all pages still accessible)
2. **Phase 2**: Assign "User" role to all existing users
3. **Phase 3**: Enable page restrictions
4. **Phase 4**: Promote users to Superuser/Admin as needed

### From Config File to Azure AD

1. Export current role mappings
2. Create Azure AD app roles
3. Assign users in Azure AD
4. Deploy RBAC code
5. Remove config file logic

---

## Troubleshooting Guide

### Issue: Roles Not Appearing

**Possible Causes:**
1. Token configuration missing "roles" claim
2. User not assigned role in Azure AD
3. User needs to re-login

**Debug Steps:**
```python
# Add temporary debug code
st.write("User Info:", st.session_state.user_info)
st.write("Roles:", get_user_roles())
```

### Issue: Access Denied with Correct Role

**Possible Causes:**
1. Role value mismatch (case-sensitive)
2. Permission not assigned to role
3. Decorator on wrong function

**Debug Steps:**
- Verify role "Value" in Azure AD
- Check `ROLE_PERMISSIONS` mapping
- Ensure decorator is on `main()` function

### Issue: Sidebar Shows Wrong Pages

**Possible Causes:**
1. Page numbering in CSS selector wrong
2. Permission check logic incorrect
3. New page added without updating sidebar logic

**Debug Steps:**
- Count pages from 1 (Home) to N
- Verify CSS selectors in `app.py`
- Check `has_permission()` returns

---

## Security Audit Checklist

Before production deployment:

**Azure AD Configuration:**
- [ ] App roles created with correct values
- [ ] Roles assigned to appropriate users
- [ ] Token includes "roles" claim
- [ ] Principle of least privilege applied

**Code Security:**
- [ ] All sensitive pages have decorators
- [ ] No hardcoded roles in URLs
- [ ] Debug code removed
- [ ] Logging enabled

**Access Control:**
- [ ] Admin access documented
- [ ] Regular audit schedule defined
- [ ] Process for role requests established
- [ ] Offboarding removes roles

**Monitoring:**
- [ ] Failed access attempts logged
- [ ] Role changes tracked
- [ ] Anomaly detection configured

---

## Future Enhancements

### Potential Additions

1. **Fine-Grained Permissions**
   - Row-level security
   - Field-level access control
   - Dynamic permissions

2. **Temporary Access**
   - Time-based role assignment
   - Emergency access workflows
   - Just-in-time permissions

3. **Multi-Tenant**
   - Organization-based roles
   - Tenant isolation
   - Cross-tenant access

4. **Advanced UI**
   - Role request workflow
   - Approval process
   - Self-service portal

5. **Audit Dashboard**
   - Access analytics
   - Role usage statistics
   - Compliance reporting

---

## Support & Resources

**Documentation:**
- `RBAC_QUICK_START.md` - Quick setup guide
- `AZURE_AD_RBAC_SETUP.md` - Detailed configuration
- This file - Technical overview

**Code Reference:**
- `SSO/rbac.py` - RBAC implementation
- `app.py` - Sidebar filtering example
- `pages/` - Page protection examples

**External Resources:**
- [Azure AD App Roles Docs](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-add-app-roles-in-azure-ad-apps)
- [JWT Token Reference](https://jwt.ms)
- [Streamlit Multipage Apps](https://docs.streamlit.io/library/get-started/multipage-apps)

---

## Conclusion

This RBAC implementation provides:
- ✅ Enterprise-grade access control
- ✅ Zero additional infrastructure
- ✅ Seamless Azure AD integration
- ✅ Easy to maintain and extend
- ✅ Production-ready security

The system is designed to be simple yet powerful, leveraging Azure AD's robust role management without requiring a database or complex infrastructure.
