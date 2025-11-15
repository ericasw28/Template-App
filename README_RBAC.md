# Role-Based Access Control (RBAC) - Azure AD Integration

## What Is This?

This Streamlit app now includes **Role-Based Access Control (RBAC)** using Azure AD App Roles. Different users see different pages based on their assigned role.

---

## Three Role Levels

### 🔴 Admin
**Full Access** - Can do everything
- ✅ View Analytics
- ✅ Manage Settings
- ✅ Manage Users
- ✅ All administrative functions

### 🟠 Superuser
**Power User** - All features except user management
- ✅ View Analytics
- ✅ Manage Settings
- ❌ Cannot manage users

### 🔵 User
**Standard Access** - Limited features
- ✅ View Analytics
- ❌ Cannot access Settings
- ❌ Cannot manage users

---

## How It Works

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  1. Admin assigns role to user in Azure AD                  │
│     (one-time setup)                                         │
│                                                              │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  2. User logs in via Azure AD SSO                           │
│                                                              │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  3. Azure AD returns JWT token with role(s)                 │
│     Example: { "roles": ["Admin"] }                         │
│                                                              │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  4. Streamlit app reads role from token                     │
│     - Shows role badge                                       │
│     - Hides unauthorized pages                              │
│     - Blocks unauthorized access                            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Page Access Matrix

| Page          | Icon | Admin | Superuser | User |
|---------------|------|-------|-----------|------|
| Home          | 🏠   | ✅    | ✅        | ✅   |
| Analytics     | 📊   | ✅    | ✅        | ✅   |
| Settings      | ⚙️   | ✅    | ✅        | ❌   |
| Users (CRUD)  | 👥   | ✅    | ❌        | ❌   |

---

## Getting Started

### For Users

**Just log in!** Your administrator will assign you the appropriate role.

Your role badge appears on the dashboard after login.

### For Administrators

Follow the setup guide to configure roles:

1. **Quick Setup**: Read `RBAC_QUICK_START.md` (5 minutes)
2. **Detailed Guide**: Read `AZURE_AD_RBAC_SETUP.md` (complete instructions)
3. **Technical Details**: Read `RBAC_IMPLEMENTATION_SUMMARY.md`

---

## What You Need

### Azure AD Requirements

- ✅ Azure AD tenant (Free tier works!)
- ✅ App registration (already set up for SSO)
- ✅ Permission to assign roles

### No Additional Infrastructure

- ❌ No PostgreSQL needed
- ❌ No user database
- ❌ No additional services
- ❌ No extra costs

**Everything is managed through Azure AD!**

---

## Quick Configuration (Admins Only)

### Step 1: Create Roles (Azure Portal)

Navigate to: **Azure AD** → **App registrations** → **Your App** → **App roles**

Create these three roles:

| Display Name | Value       | Allowed Members |
|-------------|-------------|-----------------|
| Admin       | `Admin`     | Users/Groups    |
| Superuser   | `Superuser` | Users/Groups    |
| User        | `User`      | Users/Groups    |

### Step 2: Assign Roles to Users

Navigate to: **Azure AD** → **Enterprise applications** → **Your App** → **Users and groups**

1. Click **+ Add user/group**
2. Select user(s)
3. Select role
4. Click **Assign**

### Step 3: Enable Roles in Token

Navigate to: **Azure AD** → **App registrations** → **Your App** → **Token configuration**

Add "roles" claim if not present:
- Token type: **ID**
- Claim: **roles**

### Done!

Users need to re-login to get their new role.

---

## Example Scenarios

### Scenario 1: New Employee

**Goal**: Give standard access

**Steps**:
1. Assign "User" role in Azure AD
2. User logs in
3. User sees: Home + Analytics only

### Scenario 2: Promote to Manager

**Goal**: Give access to settings

**Steps**:
1. Change role from "User" to "Superuser" in Azure AD
2. User logs out and back in
3. User now sees: Home + Analytics + Settings

### Scenario 3: New Admin

**Goal**: Give full access

**Steps**:
1. Assign "Admin" role in Azure AD
2. Admin logs in
3. Admin sees: All pages including Users management

---

## Security Features

### ✅ Defense in Depth

1. **UI Level**: Unauthorized pages hidden in sidebar
2. **Page Level**: Decorators block direct URL access
3. **Function Level**: Permission checks in code
4. **Token Level**: Roles verified from Azure AD

### ✅ Zero Trust

- Every page checks authentication AND authorization
- No client-side role manipulation possible
- Roles come from trusted source (Azure AD)

### ✅ Audit Trail

- All role assignments logged in Azure AD
- Access attempts logged in application
- Easy to track who has what access

---

## Troubleshooting

### "You have no roles assigned"

**Cause**: No role assigned in Azure AD
**Solution**: Admin needs to assign a role

### "Access Denied" on a page

**Cause**: Your role doesn't have permission
**Solution**: Contact admin if you need different access

### Role badge not showing

**Cause**: You logged in before role was assigned
**Solution**: Logout and login again

### Changes not taking effect

**Cause**: Old token cached
**Solution**: Logout and login to get new token

---

## For Developers

### Protect a New Page

```python
from SSO import require_role, Role

@require_role(Role.ADMIN, Role.SUPERUSER)
def main():
    st.write("Protected page")
```

### Check Permission in Code

```python
from SSO import has_permission, Permission

if has_permission(Permission.EDIT_SETTINGS):
    st.button("Edit Settings")
else:
    st.info("Contact admin for edit access")
```

### Show User's Role

```python
from SSO import render_role_badge, get_highest_role

render_role_badge()  # Shows colored badge

role = get_highest_role()
st.write(f"Your role: {role.value}")
```

---

## Files & Documentation

### User Documentation
- **This file** - Overview and quick reference
- `RBAC_QUICK_START.md` - 5-minute setup guide

### Administrator Documentation
- `AZURE_AD_RBAC_SETUP.md` - Complete setup guide
- Step-by-step Azure AD configuration
- Troubleshooting and best practices

### Developer Documentation
- `RBAC_IMPLEMENTATION_SUMMARY.md` - Technical details
- Architecture and code organization
- Extending the system

### Code
- `SSO/rbac.py` - RBAC implementation
- `pages/3_👥_Users.py` - User management (Admin only)
- Other pages updated with role protection

---

## Benefits

### For Users
- ✅ Clear visibility of your role
- ✅ Only see pages you can access
- ✅ No confusion about permissions

### For Administrators
- ✅ Centralized role management in Azure AD
- ✅ No database to maintain
- ✅ Audit trail built-in
- ✅ Easy to add/remove access

### For Developers
- ✅ Clean, simple API
- ✅ Reusable decorators
- ✅ Easy to extend
- ✅ Production-ready

---

## FAQs

**Q: Do I need a database for this?**
A: No! Roles are managed entirely in Azure AD.

**Q: Does this cost extra?**
A: No! App Roles are free with Azure AD (including free tier).

**Q: Can a user have multiple roles?**
A: Yes, but the app uses the highest priority role.

**Q: How do I change someone's role?**
A: In Azure AD → Enterprise applications → Your App → Users and groups

**Q: Can I add custom roles?**
A: Yes! See `RBAC_IMPLEMENTATION_SUMMARY.md` for instructions.

**Q: What if I don't use Azure AD?**
A: This implementation is specifically for Azure AD. For other providers, you'd need to adapt the code.

**Q: Is this production-ready?**
A: Yes! The implementation follows security best practices.

---

## Next Steps

**For First-Time Setup**:
1. Read `RBAC_QUICK_START.md`
2. Configure roles in Azure AD (5 minutes)
3. Assign roles to test users
4. Login and test

**For Production Deployment**:
1. Read `AZURE_AD_RBAC_SETUP.md` completely
2. Plan role assignments
3. Complete security checklist
4. Test thoroughly
5. Deploy

**For Customization**:
1. Read `RBAC_IMPLEMENTATION_SUMMARY.md`
2. Understand the architecture
3. Make modifications
4. Test changes

---

## Support

**Questions about**:
- **Setup**: See `AZURE_AD_RBAC_SETUP.md`
- **Quick Start**: See `RBAC_QUICK_START.md`
- **Technical Details**: See `RBAC_IMPLEMENTATION_SUMMARY.md`
- **Azure AD**: Check [Azure AD Documentation](https://docs.microsoft.com/en-us/azure/active-directory/)

---

**Happy Role-Based Access Controlling! 🔐**
