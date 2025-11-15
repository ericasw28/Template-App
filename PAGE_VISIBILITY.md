# Page Visibility Feature

This document explains how protected pages are hidden from unauthenticated users in the sidebar navigation.

---

## 🔒 How It Works

### Before Login
- **Sidebar**: Only shows "🏠 Home" page
- **Protected pages**: Hidden from navigation
- **Sidebar state**: Collapsed by default

### After Login
- **Sidebar**: Shows all pages (Home, Analytics, Settings)
- **Protected pages**: Visible and accessible
- **Sidebar state**: Expanded by default

---

## 🛠️ Implementation

### In `app.py`

The home page dynamically hides protected pages using CSS:

```python
def main():
    # Initialize session state FIRST
    init_session_state()

    # Hide pages in sidebar if not authenticated
    if not st.session_state.authenticated:
        st.markdown("""
            <style>
                [data-testid="stSidebarNav"] li:nth-child(n+2) {
                    display: none;
                }
            </style>
        """, unsafe_allow_html=True)
```

**What this does:**
- Targets all sidebar navigation items except the first one (Home)
- Uses CSS to hide them with `display: none`
- Only applies when user is not authenticated

### How It Works

1. **User visits app** → Session state initialized
2. **Check authentication** → `st.session_state.authenticated` is checked
3. **If not logged in** → CSS injected to hide pages 2+
4. **Sidebar shows** → Only "🏠 Home" visible
5. **User logs in** → Page reloads, CSS not injected
6. **Sidebar shows** → All pages visible

---

## 🎯 Benefits

### Security
✅ **Visual clarity** - Users only see what they can access
✅ **Reduced confusion** - No clicking on blocked pages
✅ **Better UX** - Clean navigation when logged out

### User Experience
✅ **Clear state** - Obvious when logged in vs. logged out
✅ **Progressive disclosure** - Features revealed after authentication
✅ **Professional appearance** - Polished navigation

---

## 🔐 Security Note

**Important**: Hiding pages in the sidebar is a **UX feature**, not a security feature.

- ✅ Pages are still protected by `@require_authentication`
- ✅ Direct URL access is still blocked
- ✅ Authentication is enforced server-side
- ℹ️ Hiding is purely cosmetic for better UX

**The actual security** comes from:
1. `@require_authentication` decorator
2. Session state validation
3. Cookie verification
4. OAuth token validation

---

## 🧪 Testing

### Test 1: Logged Out State

1. Clear cookies/open in incognito
2. Navigate to app
3. Check sidebar → Should only show "🏠 Home"
4. Try navigating to `/Analytics` directly → Should be blocked

### Test 2: Logged In State

1. Log in via Home page
2. Check sidebar → Should show all pages
3. Navigate between pages → Should work
4. Refresh page → Pages should remain visible

### Test 3: Direct URL Access

1. While logged out, try visiting:
   - `http://localhost:8501/Analytics`
   - `http://localhost:8501/Settings`
2. Should see authentication error
3. Pages should not render

---

## 🎨 Customization

### Adjust Which Pages Are Hidden

The CSS selector `nth-child(n+2)` means "all children from 2nd onwards".

To customize:

```python
# Hide only 2nd and 3rd pages (keep 4th visible)
li:nth-child(2), li:nth-child(3) {
    display: none;
}

# Hide everything except first page (current behavior)
li:nth-child(n+2) {
    display: none;
}

# Hide only 2nd page
li:nth-child(2) {
    display: none;
}
```

### Change Sidebar Behavior

Currently:
- **Logged out**: Sidebar collapsed, pages hidden
- **Logged in**: Sidebar expanded, pages visible

To change:

```python
if st.session_state.authenticated:
    page_config = {
        "initial_sidebar_state": "collapsed"  # Keep collapsed when logged in
    }
else:
    page_config = {
        "initial_sidebar_state": "expanded"   # Expand when logged out
    }
```

---

## 🐛 Troubleshooting

### Issue: Pages still visible when logged out

**Cause**: CSS not being applied or cached

**Solution**:
1. Hard refresh (Ctrl+Shift+R / Cmd+Shift+R)
2. Clear browser cache
3. Check if `st.session_state.authenticated` is False
4. Verify CSS is in `app.py` main function

### Issue: Pages hidden even when logged in

**Cause**: Session state not set correctly

**Solution**:
1. Check login flow completed successfully
2. Verify `st.session_state.authenticated = True` is set
3. Look for errors in console/logs
4. Try logging out and back in

### Issue: CSS affecting other elements

**Cause**: CSS selector too broad

**Solution**:
- Use more specific selector
- Test in browser dev tools
- Inspect element to find correct `data-testid`

---

## 📖 Alternative Approaches

### Approach 1: Using st.Page (Streamlit 1.30+)

If using Streamlit 1.30+, you can use the newer `st.Page` API:

```python
import streamlit as st

# Define pages
home = st.Page("app.py", title="Home", icon="🏠")
analytics = st.Page("pages/analytics.py", title="Analytics", icon="📊")
settings = st.Page("pages/settings.py", title="Settings", icon="⚙️")

# Show different pages based on auth
if st.session_state.authenticated:
    pg = st.navigation([home, analytics, settings])
else:
    pg = st.navigation([home])

pg.run()
```

**Note**: Requires Streamlit 1.30+ and restructuring of pages.

### Approach 2: JavaScript-based Hiding

More robust but complex:

```python
st.components.v1.html("""
<script>
    const items = parent.document.querySelectorAll('[data-testid="stSidebarNav"] li');
    for(let i = 1; i < items.length; i++) {
        items[i].style.display = 'none';
    }
</script>
""", height=0)
```

**Note**: May have timing issues with Streamlit's rendering.

---

## 📚 Related Documentation

- [MULTIPAGE_GUIDE.md](MULTIPAGE_GUIDE.md) - Complete multipage guide
- [README.md](README.md) - Main documentation
- [SSO/auth_utils.py](SSO/auth_utils.py) - Authentication utilities

---

## ✅ Summary

**Current Implementation:**
- ✅ CSS-based hiding (simple, effective)
- ✅ Sidebar collapsed when logged out
- ✅ Pages revealed after login
- ✅ Works with existing authentication system
- ✅ No additional dependencies

**Result:**
- Clean UX for unauthenticated users
- Full navigation for authenticated users
- Maintains security with `@require_authentication`
- Professional appearance

**Remember**: This is a UX enhancement. Security is handled by the authentication decorator on each page!
