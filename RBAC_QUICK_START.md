# RBAC Quick Start Guide

Quick reference for setting up Role-Based Access Control with Azure AD App Roles.

## 5-Minute Setup

### 1. Create App Roles in Azure Portal (2 minutes)

**Azure Portal** → **Azure AD** → **App registrations** → **Your App** → **App roles**

Create three roles with these **exact** values:

| Display Name | Value       | Description                          |
|-------------|-------------|--------------------------------------|
| Admin       | `Admin`     | Full access including user mgmt      |
| Superuser   | `Superuser` | All features except user mgmt        |
| User        | `User`      | Analytics only, no Settings/Users    |

⚠️ **Important**: The "Value" field must match exactly (case-sensitive).

---

### 2. Assign Roles to Users (2 minutes)

**Azure Portal** → **Azure AD** → **Enterprise applications** → **Your App** → **Users and groups**

1. Click **+ Add user/group**
2. Select user(s)
3. Select role
4. Click **Assign**

---

### 3. Add Token Claim (1 minute)

**Azure Portal** → **Azure AD** → **App registrations** → **Your App** → **Token configuration**

If "roles" is not listed:
1. Click **+ Add optional claim**
2. Token type: **ID**
3. Select: **roles**
4. Click **Add**

---

### 4. Test (30 seconds)

Login and verify:
- **User**: Sees Home + Analytics only
- **Superuser**: Sees Home + Analytics + Settings
- **Admin**: Sees all pages including Users

---

## Role Permissions

```
┌─────────────┬───────┬───────────┬──────┐
│ Page        │ Admin │ Superuser │ User │
├─────────────┼───────┼───────────┼──────┤
│ Home        │   ✅  │     ✅    │  ✅  │
│ Analytics   │   ✅  │     ✅    │  ✅  │
│ Settings    │   ✅  │     ✅    │  ❌  │
│ Users       │   ✅  │     ❌    │  ❌  │
└─────────────┴───────┴───────────┴──────┘
```

---

## Code Usage Examples

### Protect a Page by Role

```python
from SSO import require_role, Role

@require_role(Role.ADMIN)
def main():
    st.write("Admin only page")
```

### Protect by Permission

```python
from SSO import require_permission, Permission

@require_permission(Permission.MANAGE_USERS)
def main():
    st.write("Can manage users")
```

### Check Role in Code

```python
from SSO import has_role, Role

if has_role(Role.ADMIN):
    st.write("You are an admin")
```

### Show Role Badge

```python
from SSO import render_role_badge

render_role_badge()  # Shows colored role badge
```

---

## Troubleshooting

### "You have no roles assigned"
→ Assign role in Enterprise Applications → Users and groups

### "Access Denied"
→ User has wrong role. Check role assignment.

### Roles not showing up
→ User needs to logout and re-login to get new token

### Role value mismatch
→ Check role "Value" in Azure AD matches code exactly (case-sensitive)

---

## Files Modified

The RBAC implementation added/modified these files:

**New Files:**
- `SSO/rbac.py` - Core RBAC logic
- `pages/3_👥_Users.py` - Admin-only user management page
- `AZURE_AD_RBAC_SETUP.md` - Detailed setup guide
- `RBAC_QUICK_START.md` - This file

**Modified Files:**
- `SSO/__init__.py` - Export RBAC functions
- `app.py` - Role-based sidebar filtering
- `pages/2_⚙️_Settings.py` - Now requires Admin/Superuser role
- `utils/ui_components.py` - Show role badge on dashboard

---

## No Database Required!

This solution uses Azure AD for role management:
- ✅ No PostgreSQL needed
- ✅ No user tables
- ✅ No role assignment UI to build
- ✅ Free with Azure AD
- ✅ Centralized management

---

## Next Steps

1. ✅ Complete the 5-minute setup above
2. 📖 Read `AZURE_AD_RBAC_SETUP.md` for details
3. 🧪 Test with different roles
4. 🚀 Deploy to production

For detailed information, see **AZURE_AD_RBAC_SETUP.md**.
