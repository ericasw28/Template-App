# Users Page - Read-Only Dashboard

## Overview

The **Users** page is an **Admin-only**, **read-only dashboard** that displays real user data from Azure AD.

**Key Points:**
- ✅ Shows real users from Azure AD
- ✅ Read-only (no modifications)
- ✅ Role management done in Azure AD portal
- ✅ Cached for performance
- ✅ Only accessible to Admins

---

## Current State

### Without Graph API (Default)

Shows **sample data** with instructions to configure Graph API.

**What you see:**
- Demo users with fake data
- Setup instructions
- Link to configuration guide

### With Graph API (Recommended)

Shows **real users** from your Azure AD tenant.

**What you see:**
- Real user names and emails
- Active/disabled status
- Search and filter
- User statistics
- Quick links to Azure portal

---

## Quick Setup (5 Minutes)

### Step 1: Add API Permissions

1. **Azure Portal** → **App registrations** → **Your App** → **API permissions**
2. Click **+ Add a permission**
3. Select **Microsoft Graph** → **Application permissions**
4. Add **User.Read.All**
5. Click **Add permissions**

### Step 2: Grant Admin Consent

1. Click **✔ Grant admin consent for [Your Organization]**
2. Click **Yes**
3. Verify green checkmark appears

### Step 3: Test

1. Restart Streamlit app
2. Login as Admin
3. Navigate to Users page
4. See real users!

---

## Features

### User Directory

- **List all users** from Azure AD
- **Search** by name or email
- **Filter** active/disabled accounts
- **View details**: name, email, status, Azure AD ID

### Statistics

- Total users count
- Active users count
- Disabled accounts count

### Quick Links

Direct links to:
- Azure AD Enterprise Applications (role management)
- Azure AD Users list
- App Roles configuration

### Role Information

- Role definitions (Admin, Superuser, User)
- Permission breakdown
- Assignment instructions

---

## What You CAN Do

✅ View all users in your Azure AD
✅ Search and filter users
✅ See active/disabled status
✅ View user details (name, email, ID)
✅ Click links to Azure portal
✅ Export data (copy from table)

---

## What You CANNOT Do

❌ Create new users
❌ Delete users
❌ Assign/remove roles
❌ Enable/disable accounts
❌ Modify user properties
❌ Reset passwords

**Why?** Security best practice: keep user management centralized in Azure AD.

---

## Role Management

### How to Assign Roles

All role assignment happens in **Azure AD portal**:

1. Go to **Azure Portal**
2. Navigate to **Azure AD** → **Enterprise applications**
3. Find your application
4. Click **Users and groups**
5. Click **+ Add user/group**
6. Select user and assign role

The Users page provides:
- Instructions for role assignment
- Direct links to Azure portal
- Role definitions and permissions

---

## Performance

### Caching

- User data cached for **5 minutes**
- Reduces API calls
- Improves page load time

### API Limits

- Fetches up to **100 users** by default
- Can be increased if needed
- Well within Microsoft Graph rate limits

### Refresh Data

- **Automatic**: Every 5 minutes
- **Manual**: Refresh browser (Ctrl+R or Cmd+R)

---

## Security

### Read-Only Access

- Uses Microsoft Graph API
- Application permissions (server-side)
- No user modifications possible
- All changes done in Azure portal

### Audit Trail

- All API calls logged by Azure AD
- Track who accessed user data
- Monitor usage patterns

### Permissions Required

- **To view page**: Admin role in app
- **To see data**: Graph API configured with admin consent
- **To manage roles**: Azure AD admin privileges

---

## Troubleshooting

### "Graph API Not Configured"

**Solution**: Follow setup steps in `GRAPH_API_SETUP.md`

### "Failed to fetch users"

**Possible causes:**
- Admin consent not granted
- Permissions not configured
- Network issues

**Solution**:
- Verify permissions in Azure AD
- Check admin consent status
- Review application logs

### Empty user list

**Causes:**
- No users in tenant (unlikely)
- Disabled accounts filter active
- Search query too restrictive

**Solution**:
- Check "Show disabled accounts"
- Clear search filter
- Verify users exist in Azure AD

---

## Next Steps

### Option A: Use Sample Data (No Setup)

- No configuration needed
- Shows demo data
- Good for testing/development
- **Current state** without Graph API

### Option B: Configure Graph API (Recommended)

- Follow `GRAPH_API_SETUP.md`
- 5-minute setup
- Shows real users
- Production-ready

---

## Files

**Implementation:**
- `pages/3_👥_Users.py` - Users page UI
- `SSO/graph_api.py` - Graph API client

**Documentation:**
- `GRAPH_API_SETUP.md` - Full setup guide
- This file - Overview

**Configuration:**
- `requirements.txt` - Updated with `requests` and `pandas`

---

## Summary

The Users page is a **read-only dashboard** that:

1. **Displays** real users from Azure AD
2. **Links** to Azure portal for management
3. **Caches** data for performance
4. **Requires** Admin role to access
5. **Maintains** security with read-only access

**Philosophy**: View data in app, manage users in Azure AD.

This keeps your app simple while leveraging Azure AD's robust user management capabilities!
