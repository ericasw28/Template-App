# Microsoft Graph API Setup Guide

This guide explains how to configure Microsoft Graph API permissions to enable the read-only Users dashboard.

## What You Get

With Graph API configured, the Users page will:
- ✅ Display real users from your Azure AD
- ✅ Show active/disabled status
- ✅ Search and filter users
- ✅ Provide quick links to Azure AD portal
- ✅ Cache data for performance (5-minute TTL)

**Note**: This is READ-ONLY. Role assignments are still managed in Azure AD portal.

---

## Prerequisites

- ✅ Azure AD App Registration (already set up for SSO)
- ✅ Admin access to grant API permissions
- ✅ Global Administrator or Application Administrator role

---

## Step 1: Add API Permissions

### 1.1 Navigate to API Permissions

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory**
3. Click **App registrations**
4. Select your application
5. Click **API permissions** in the left menu

### 1.2 Add Microsoft Graph Permissions

Click **+ Add a permission**

#### Add User.Read.All

1. Select **Microsoft Graph**
2. Select **Application permissions** (NOT Delegated)
3. Expand **User**
4. Check **User.Read.All**
5. Click **Add permissions**

**What this allows:**
- Read user profiles
- List all users in the directory
- View user account status

#### Add Application.Read.All (Optional)

For enhanced features (role assignments):

1. Click **+ Add a permission** again
2. Select **Microsoft Graph**
3. Select **Application permissions**
4. Expand **Application**
5. Check **Application.Read.All**
6. Click **Add permissions**

**What this allows:**
- Read application role assignments
- View which users have which roles

---

## Step 2: Grant Admin Consent

### 2.1 Why Admin Consent is Required

Application permissions (used for server-to-server calls) require administrator approval for security.

### 2.2 Grant Consent

1. In the **API permissions** page
2. Click **✔ Grant admin consent for [Your Organization]**
3. Click **Yes** to confirm
4. Wait for the status to change to "Granted"

**You should see:**
- ✅ Green checkmark next to each permission
- Status: "Granted for [Your Organization]"

---

## Step 3: Verify Configuration

### 3.1 Check Permissions

In **API permissions** page, you should see:

| Permission | Type | Status |
|------------|------|--------|
| User.Read.All | Application | ✅ Granted |
| Application.Read.All | Application | ✅ Granted (optional) |

### 3.2 Test in Application

1. Login as an **Admin** user
2. Navigate to **Users** page
3. You should see real users from Azure AD
4. If you see "Graph API Not Configured", check:
   - Permissions are granted
   - Admin consent is approved
   - App has been restarted

---

## Step 4: Update Requirements (If Needed)

If you don't have the `requests` library installed:

```bash
pip install requests
```

Or add to your `requirements.txt`:
```
requests>=2.31.0
```

---

## How It Works

### Authentication Flow

```
1. App starts
   ↓
2. Graph API client requests access token
   ↓
3. Azure AD validates client credentials
   ↓
4. Token granted with permissions (User.Read.All)
   ↓
5. App makes API calls to list users
   ↓
6. Data cached for 5 minutes
   ↓
7. Users displayed in dashboard
```

### Client Credentials Flow

The app uses **Client Credentials Flow** (OAuth 2.0):
- Uses `CLIENT_ID` and `CLIENT_SECRET` from your `.env`
- No user interaction required
- Runs server-side only
- Secure for backend operations

---

## Security Considerations

### Permissions Scope

The permissions granted are:
- ✅ **Read-only**: Cannot modify users
- ✅ **Application-level**: Not tied to specific user
- ✅ **Server-side only**: Never exposed to browser
- ✅ **Audited**: All API calls logged by Azure

### Best Practices

1. **Least Privilege**: Only `User.Read.All` is required (minimum)
2. **Secure Credentials**: Keep `CLIENT_SECRET` in `.env`, never commit
3. **Monitor Usage**: Review Azure AD sign-in logs regularly
4. **Rotate Secrets**: Rotate client secret every 6-12 months
5. **Limit Admin Access**: Only grant Admin role to trusted users

---

## Troubleshooting

### Issue: "Failed to fetch users from Azure AD"

**Possible Causes:**
1. Admin consent not granted
2. Permissions not configured
3. Network connectivity issues
4. Invalid credentials

**Debug Steps:**

1. **Check Permissions**:
   - Azure Portal → App registrations → Your App → API permissions
   - Verify `User.Read.All` is granted with admin consent

2. **Verify Credentials**:
   - Check `.env` file has correct values:
     - `AZURE_CLIENT_ID`
     - `AZURE_CLIENT_SECRET`
     - `AZURE_TENANT_ID`

3. **Test Token Request**:
   ```bash
   curl -X POST \
     https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/token \
     -d client_id=YOUR_CLIENT_ID \
     -d client_secret=YOUR_CLIENT_SECRET \
     -d scope=https://graph.microsoft.com/.default \
     -d grant_type=client_credentials
   ```

4. **Check Application Logs**:
   - Look for Graph API errors in console/logs

### Issue: "Graph API Not Configured"

**Cause**: Missing environment variables

**Solution**:
- Ensure `.env` has all required variables
- Restart the Streamlit app

### Issue: "Insufficient privileges"

**Cause**: Admin consent not granted or insufficient permissions

**Solution**:
1. Verify admin consent was granted (green checkmark)
2. Ensure you're using **Application permissions**, not Delegated
3. Try revoking and re-granting consent

### Issue: Empty user list

**Cause**: No users in Azure AD tenant or filter issue

**Solution**:
- Verify users exist in Azure AD → Users
- Check if "Show disabled accounts" is unchecked
- Clear search filter

---

## API Rate Limits

Microsoft Graph API has rate limits:

- **Per App**: 2,000 requests per second
- **Per Tenant**: 10,000 requests per second

**Our Implementation**:
- ✅ Caches results for 5 minutes
- ✅ Limits to 100 users per request
- ✅ Single API call per page load

**You're unlikely to hit limits** unless you have:
- Hundreds of concurrent users
- Very frequent page refreshes

---

## Advanced Configuration

### Increase User Limit

By default, we fetch up to 100 users. To increase:

In `pages/3_👥_Users.py`, change:

```python
users = get_cached_users(top=100)  # Change to 500
```

**Note**: Larger values may slow down initial load.

### Adjust Cache Duration

Default cache is 5 minutes. To change:

In `SSO/graph_api.py`:

```python
@st.cache_data(ttl=300)  # Change to 600 (10 minutes)
```

### Add More User Fields

To fetch additional user properties:

In `SSO/graph_api.py`, modify the `$select` parameter:

```python
endpoint = f"/users?$top={top}&$select=id,displayName,mail,userPrincipalName,accountEnabled,jobTitle,department"
```

Then update the Users page to display new fields.

---

## Production Checklist

Before going live:

- [ ] Graph API permissions configured
- [ ] Admin consent granted
- [ ] Tested with real users
- [ ] Client secret stored securely (not committed to git)
- [ ] Rate limiting understood
- [ ] Monitoring/logging enabled
- [ ] Secret rotation schedule defined
- [ ] Backup admin accounts exist

---

## Costs

**Microsoft Graph API is FREE** for:
- Azure AD Free
- Azure AD Premium P1
- Azure AD Premium P2
- Microsoft 365 (includes Azure AD)

**No additional costs** for using Graph API with your existing Azure AD!

---

## Additional Resources

- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/overview)
- [User Resource Type](https://docs.microsoft.com/en-us/graph/api/resources/user)
- [Application Permissions](https://docs.microsoft.com/en-us/graph/permissions-reference)
- [Client Credentials Flow](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow)

---

## Summary

With Graph API configured:

1. **Admin users** see real user data from Azure AD
2. **Search and filter** works on live data
3. **Role management** links directly to Azure portal
4. **Performance** optimized with caching
5. **Security** maintained with read-only access

The Users page becomes a powerful **dashboard** while keeping role management in Azure AD where it belongs!
