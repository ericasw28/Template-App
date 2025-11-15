# Azure AD App Roles Configuration Guide

This guide explains how to configure Role-Based Access Control (RBAC) for your Streamlit SSO application using Azure AD App Roles.

## Overview

The application supports three role tiers:
- **Admin**: Full access including user management
- **Superuser**: Access to all features except user management
- **User**: Limited access (Analytics only, no Settings or Users pages)

## Architecture

### How It Works

1. **Azure AD Configuration**: You define app roles in Azure AD portal
2. **Role Assignment**: Assign roles to users/groups in Azure AD
3. **Token Claims**: Azure AD includes assigned roles in the JWT token
4. **Application Logic**: The app reads roles from token claims and enforces permissions

### No Database Required

This solution leverages Azure AD's built-in role management, so you don't need:
- PostgreSQL or any database
- User management tables
- Role assignment UI (handled by Azure AD)

---

## Step 1: Configure App Roles in Azure AD

### 1.1 Navigate to App Registrations

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory**
3. Click **App registrations**
4. Select your application (the one you created for SSO)

### 1.2 Create App Roles

1. In your app registration, click **App roles** in the left menu
2. Click **+ Create app role**

#### Create "User" Role

- **Display name**: `User`
- **Allowed member types**: `Users/Groups`
- **Value**: `User` (must match exactly)
- **Description**: `Standard user with limited access to analytics`
- **Do you want to enable this app role?**: ✅ Checked

Click **Apply**

#### Create "Superuser" Role

- **Display name**: `Superuser`
- **Allowed member types**: `Users/Groups`
- **Value**: `Superuser` (must match exactly)
- **Description**: `Power user with access to all features except user management`
- **Do you want to enable this app role?**: ✅ Checked

Click **Apply**

#### Create "Admin" Role

- **Display name**: `Admin`
- **Allowed member types**: `Users/Groups`
- **Value**: `Admin` (must match exactly)
- **Description**: `Administrator with full system access including user management`
- **Do you want to enable this app role?**: ✅ Checked

Click **Apply**

### 1.3 Verify Role Creation

You should now see all three roles listed under **App roles**. The **Value** field is critical - it must match the role names defined in the code.

---

## Step 2: Assign Roles to Users

### 2.1 Navigate to Enterprise Applications

1. In Azure Portal, go to **Azure Active Directory**
2. Click **Enterprise applications**
3. Find and select your application
   - Tip: Search by the same name as your App Registration

### 2.2 Assign Users to Roles

1. Click **Users and groups** in the left menu
2. Click **+ Add user/group**
3. Click **Users** - Select the user(s) you want to assign
4. Click **Select role**
5. Choose the appropriate role (Admin, Superuser, or User)
6. Click **Select**, then **Assign**

### 2.3 Best Practices for Role Assignment

**For Individuals:**
- Assign roles directly to individual users
- Use the least privilege principle (start with User role)

**For Groups (Recommended for Enterprise):**
- Create Azure AD groups (e.g., "App Admins", "App Superusers", "App Users")
- Assign roles to groups instead of individuals
- Manage membership in groups (easier than reassigning roles)

### 2.4 Multiple Roles

Users can have multiple roles assigned, but the app uses the highest role:
- Priority: Admin > Superuser > User

---

## Step 3: Update App Configuration (If Needed)

### 3.1 Verify Token Configuration

Your app should already be configured to receive role claims. To verify:

1. In your **App registration**, go to **Token configuration**
2. Check if "roles" claim is listed
3. If not, click **+ Add optional claim**:
   - Token type: **ID**
   - Claim: Select **roles**
   - Click **Add**

### 3.2 API Permissions

Ensure your app has these permissions:
- `User.Read` (should already be configured)
- `openid` (should already be configured)
- `profile` (should already be configured)

No additional permissions are needed for roles.

---

## Step 4: Test the Implementation

### 4.1 Testing Without Roles

1. Login with a user that has NO role assigned
2. Expected behavior:
   - User can authenticate
   - No pages visible in sidebar except Home
   - If user navigates to a protected page, they see "Access Denied"

### 4.2 Testing with User Role

1. Assign "User" role to a test account
2. Login
3. Expected behavior:
   - ✅ Home page accessible
   - ✅ Analytics page accessible
   - ❌ Settings page hidden in sidebar
   - ❌ Users page hidden in sidebar

### 4.3 Testing with Superuser Role

1. Assign "Superuser" role to a test account
2. Login
3. Expected behavior:
   - ✅ Home page accessible
   - ✅ Analytics page accessible
   - ✅ Settings page accessible
   - ❌ Users page hidden in sidebar

### 4.4 Testing with Admin Role

1. Assign "Admin" role to a test account
2. Login
3. Expected behavior:
   - ✅ Home page accessible
   - ✅ Analytics page accessible
   - ✅ Settings page accessible
   - ✅ Users page accessible
   - ✅ Can see all user management features

---

## Step 5: Debugging Role Issues

### Check User Token Claims

Add this debug code temporarily to see what roles are being received:

```python
# In app.py, after authentication
if st.session_state.authenticated:
    st.write("Debug - User Roles:", st.session_state.user_info.get("roles", []))
```

### Common Issues

#### Issue: No roles showing up in token

**Solution:**
1. Verify roles are assigned in Enterprise Applications → Users and groups
2. Check Token configuration includes "roles" claim
3. User needs to logout and re-login to get new token with roles

#### Issue: Access denied even with correct role

**Solution:**
1. Verify the role **Value** in App roles matches exactly (case-sensitive):
   - `Admin` not `admin` or `ADMIN`
2. Check the role-permission mapping in `SSO/rbac.py`
3. Clear browser cookies and re-login

#### Issue: Multiple roles conflict

**Solution:**
- The app automatically uses the highest priority role
- If you want different behavior, modify `get_highest_role()` in `SSO/rbac.py`

---

## Role Permissions Matrix

| Page      | Admin | Superuser | User |
|-----------|-------|-----------|------|
| Home      | ✅    | ✅        | ✅   |
| Analytics | ✅    | ✅        | ✅   |
| Settings  | ✅    | ✅        | ❌   |
| Users     | ✅    | ❌        | ❌   |

---

## Customizing Roles

### Adding New Roles

1. **In Azure AD**: Create new app role following Step 1.2
2. **In Code**: Update `SSO/rbac.py`:

```python
class Role(str, Enum):
    ADMIN = "Admin"
    SUPERUSER = "Superuser"
    USER = "User"
    VIEWER = "Viewer"  # New role
```

3. **Define Permissions**: Add to `ROLE_PERMISSIONS`:

```python
ROLE_PERMISSIONS = {
    Role.ADMIN: [...],
    Role.SUPERUSER: [...],
    Role.USER: [...],
    Role.VIEWER: [Permission.VIEW_ANALYTICS],  # New
}
```

### Adding New Permissions

1. **Define Permission**: In `SSO/rbac.py`:

```python
class Permission(str, Enum):
    VIEW_ANALYTICS = "view_analytics"
    VIEW_SETTINGS = "view_settings"
    MANAGE_USERS = "manage_users"
    EDIT_SETTINGS = "edit_settings"
    EXPORT_DATA = "export_data"  # New
```

2. **Assign to Roles**: Update `ROLE_PERMISSIONS`

3. **Protect Pages**: Use decorators:

```python
from SSO import require_permission, Permission

@require_permission(Permission.EXPORT_DATA)
def main():
    st.write("Export page")
```

---

## Security Best Practices

### 1. Principle of Least Privilege
- Start users with the lowest role needed
- Promote only when necessary
- Regularly audit role assignments

### 2. Use Groups for Role Management
- Create AD groups for each role
- Assign roles to groups, not individuals
- Manage access via group membership

### 3. Regular Audits
- Review role assignments quarterly
- Remove roles from inactive users
- Check the audit log in Users page

### 4. Separation of Duties
- Don't give Admin role to service accounts
- Have multiple admins (no single point of failure)
- Document who has Admin access

### 5. Monitoring
- Monitor failed access attempts
- Alert on role changes
- Log all administrative actions

---

## Production Checklist

Before deploying to production:

- [ ] All app roles created in Azure AD
- [ ] Roles assigned to appropriate users/groups
- [ ] Token configuration includes "roles" claim
- [ ] Tested all three role levels
- [ ] Removed debug code showing token claims
- [ ] Documented who has Admin access
- [ ] Set up audit logging
- [ ] Configured alerts for security events
- [ ] Backup plan if admin loses access

---

## Troubleshooting

### Get Help

If you encounter issues:

1. **Check Azure AD Audit Logs**:
   - Azure Portal → Azure AD → Audit logs
   - Filter by "Assign role to user"

2. **Verify Token Contents**:
   - Use [jwt.ms](https://jwt.ms) to decode your JWT token
   - Check if "roles" claim is present

3. **Review Application Logs**:
   ```bash
   # The app logs role information
   tail -f logs/app.log | grep "role"
   ```

4. **Common Error Messages**:
   - "You have no roles assigned" → Assign role in Enterprise Applications
   - "Access Denied" → User has wrong role for that page
   - "Unknown role: X" → Role value doesn't match code definition

---

## Migration Guide

### From Existing Auth (No RBAC) to RBAC

If you're upgrading an existing app:

1. **Assign Default Roles**: Assign all current users the "User" role
2. **Identify Admins**: Promote administrators to "Admin" role
3. **Identify Power Users**: Promote to "Superuser" as needed
4. **Deploy Code**: Update application code with RBAC changes
5. **Communicate**: Inform users about new role structure
6. **Monitor**: Watch for access issues in first week

### From Database Roles to Azure AD Roles

If migrating from a database-based role system:

1. Export current role assignments
2. Create corresponding Azure AD app roles
3. Assign users in Azure AD based on database
4. Deploy new code
5. Deprecate old database tables
6. Clean up

---

## Cost Considerations

**Azure AD App Roles are FREE** with:
- Azure AD Free tier
- Azure AD Premium P1
- Azure AD Premium P2
- Microsoft 365 (includes Azure AD)

No additional costs for implementing this RBAC solution!

---

## Additional Resources

- [Azure AD App Roles Documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-add-app-roles-in-azure-ad-apps)
- [Azure AD Token Claims](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-optional-claims)
- [RBAC Best Practices](https://docs.microsoft.com/en-us/azure/role-based-access-control/best-practices)

---

## Support

For issues with this implementation:
1. Check this guide's Troubleshooting section
2. Review the code comments in `SSO/rbac.py`
3. Consult Azure AD documentation
4. Contact your Azure administrator
