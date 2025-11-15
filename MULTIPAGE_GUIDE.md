# Multipage Application Guide

This guide explains the multipage structure of the Azure AD SSO Streamlit application and how to add new protected pages.

---

## 📁 Project Structure

```
Streamlit SSO/
│
├── app.py                          # Home page (login & dashboard)
├── pages/                          # Multipage directory
│   ├── 1_📊_Analytics.py          # Protected analytics page
│   └── 2_⚙️_Settings.py           # Protected settings page
│
├── SSO/                            # Authentication package
│   ├── __init__.py                # Package exports
│   ├── config.py                  # Azure AD configuration
│   ├── auth.py                    # MSAL authentication
│   ├── session.py                 # Session management
│   └── auth_utils.py              # Page protection utilities
│
├── README.md                       # Main documentation
├── MULTIPAGE_GUIDE.md             # This file
└── PRODUCTION_CHECKLIST.md        # Production deployment guide
```

---

## 🔄 How Streamlit Multipage Works

### Automatic Page Discovery

Streamlit automatically discovers pages in the `pages/` directory:

1. **File naming**: Files are sorted alphabetically by default
2. **Prefix numbers**: Use `1_`, `2_`, etc. to control order
3. **Emojis**: Include emojis in filenames for visual navigation
4. **Sidebar**: Pages appear automatically in the sidebar

### Example File Names

| Filename | Appears As | Order |
|----------|------------|-------|
| `1_📊_Analytics.py` | 📊 Analytics | First |
| `2_⚙️_Settings.py` | ⚙️ Settings | Second |
| `3_📁_Documents.py` | 📁 Documents | Third |

---

## 🔒 Authentication Protection

### The `@require_authentication` Decorator

All pages except the home page should be protected with authentication:

```python
from SSO import require_authentication, init_session_state

@require_authentication
def main():
    """Your page logic here."""
    # Initialize session state
    init_session_state()

    # Your page content
    st.title("Protected Page")
    st.write("Only authenticated users see this!")

if __name__ == "__main__":
    main()
```

### What the Decorator Does

1. **Checks authentication**: Verifies `st.session_state.authenticated`
2. **Blocks access**: Shows error if not authenticated
3. **Redirects user**: Tells them to log in via Home page
4. **Stops execution**: Prevents page content from loading

---

## 📄 Current Pages

### 🏠 Home (`app.py`)

**Purpose**: Authentication entry point and dashboard

**Features**:
- Login page for unauthenticated users
- Dashboard with quick stats for authenticated users
- OAuth callback handling
- Navigation guide

**Authentication**: Not required (handles login)

---

### 📊 Analytics (`pages/1_📊_Analytics.py`)

**Purpose**: Data visualization and analytics

**Features**:
- Key performance indicators (KPIs)
- Interactive charts (line, bar)
- Recent activity table
- Date range filters
- Sample data generation

**Authentication**: ✅ Required (`@require_authentication`)

**Key Components**:
```python
# KPI Metrics
st.metric("Total Users", "1,234", delta="12%")

# Charts
st.line_chart(chart_data)
st.bar_chart(traffic_data)

# Data Table
st.dataframe(activity_data)

# Interactive Filters
date_range = st.date_input("Select Date Range")
metric_type = st.selectbox("Metric Type", [...])
```

---

### ⚙️ Settings (`pages/2_⚙️_Settings.py`)

**Purpose**: User preferences and configuration

**Features**:
- User profile display
- Appearance settings (theme, language, density)
- Notification preferences
- Privacy & security settings
- API key management
- Connected services
- Developer options

**Authentication**: ✅ Required (`@require_authentication`)

**Key Components**:
```python
# User Profile
user_name = get_user_name()
user_email = get_user_email()

# Settings Form
theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
email_updates = st.checkbox("Email updates", value=True)

# Save Button
if st.button("Save Settings"):
    st.success("Settings saved!")
```

---

## 🆕 Creating New Pages

### Step 1: Create the File

Create a new file in the `pages/` directory:

```bash
touch "pages/3_📁_Documents.py"
```

**Naming Convention**:
- Start with a number for ordering: `3_`
- Include an emoji for visual appeal: `📁`
- Use descriptive name: `Documents`
- Extension: `.py`

### Step 2: Basic Page Template

```python
"""
Documents Page - Protected by Azure AD SSO

Description of what this page does.
Only accessible to authenticated users.
"""

import streamlit as st
from SSO import (
    require_authentication,
    init_session_state,
    render_authenticated_header
)


@require_authentication
def main():
    """Main function for documents page."""
    st.set_page_config(
        page_title="Azure SSO App - Documents",
        page_icon="📁",
        layout="wide"
    )

    # Initialize session state
    init_session_state()

    # Render header with logout button
    render_authenticated_header("📁 Documents", show_logout=True)

    st.divider()

    # Your page content here
    st.write("This is a protected page!")

    # Example content
    st.subheader("Document Library")
    st.write("Upload and manage your documents here.")

    # Add your features...


if __name__ == "__main__":
    main()
```

### Step 3: Add Page Features

Use Streamlit components to build your page:

```python
# File uploader
uploaded_file = st.file_uploader("Choose a file")

# Data editor
df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
edited_df = st.data_editor(df)

# Tabs
tab1, tab2 = st.tabs(["View", "Edit"])
with tab1:
    st.write("View mode")
with tab2:
    st.write("Edit mode")

# Forms
with st.form("my_form"):
    name = st.text_input("Name")
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success(f"Hello {name}!")
```

### Step 4: Test the Page

1. Run the app: `streamlit run app.py`
2. Log in via the Home page
3. Navigate to your new page in the sidebar
4. Verify authentication protection works

---

## 🛠️ Available Utilities

### From `SSO.auth_utils`

| Function | Description | Usage |
|----------|-------------|-------|
| `@require_authentication` | Decorator to protect pages | `@require_authentication` |
| `check_authentication()` | Check if user is logged in | `if check_authentication():` |
| `get_user_info()` | Get user profile dict | `user = get_user_info()` |
| `get_user_name()` | Get user's display name | `name = get_user_name()` |
| `get_user_email()` | Get user's email | `email = get_user_email()` |
| `render_authenticated_header()` | Standard page header | `render_authenticated_header("Title")` |
| `show_authentication_warning()` | Show auth required message | `show_authentication_warning()` |

### Examples

```python
# Check authentication manually
if check_authentication():
    st.success("You're logged in!")
else:
    st.error("Please log in")

# Get user information
user_name = get_user_name()  # Returns "User" if not available
user_email = get_user_email()  # Returns "" if not available
user_info = get_user_info()  # Returns full user dict

# Render consistent header
render_authenticated_header(
    page_title="My Custom Page",
    show_logout=True  # Shows logout button
)

# Custom authentication check
from SSO import check_authentication

def main():
    if not check_authentication():
        show_authentication_warning()
        st.stop()

    # Protected content here
    st.write("Secure content")
```

---

## 🎨 Page Design Best Practices

### 1. Consistent Header

Always use the standard header for consistency:

```python
render_authenticated_header("📊 Your Page Title", show_logout=True)
```

### 2. Page Configuration

Set page config at the start:

```python
st.set_page_config(
    page_title="Azure SSO App - Your Page",
    page_icon="🎯",
    layout="wide",  # or "centered"
    initial_sidebar_state="expanded"
)
```

### 3. Use Dividers

Separate sections with dividers:

```python
st.divider()
```

### 4. Descriptive Help Text

Add help text to interactive elements:

```python
st.selectbox(
    "Choose option",
    options=["A", "B", "C"],
    help="This selector does X, Y, Z"
)
```

### 5. Loading States

Show loading indicators for async operations:

```python
with st.spinner("Loading data..."):
    # Your long-running operation
    data = fetch_data()
```

### 6. Error Handling

Gracefully handle errors:

```python
try:
    result = risky_operation()
    st.success("Operation successful!")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    logger.error(f"Error details: {e}", exc_info=True)
```

---

## 🔐 Security Considerations

### 1. Always Protect Sensitive Pages

**❌ Bad** - No protection:
```python
def main():
    st.write("Sensitive data")  # Anyone can access!
```

**✅ Good** - Protected:
```python
@require_authentication
def main():
    st.write("Sensitive data")  # Only authenticated users
```

### 2. Validate User Permissions

If implementing role-based access:

```python
@require_authentication
def main():
    user_info = get_user_info()

    # Check roles (if you've added role claims to Azure AD)
    user_roles = user_info.get("roles", [])

    if "Admin" not in user_roles:
        st.error("Admin access required")
        st.stop()

    # Admin-only content here
```

### 3. Sanitize User Input

```python
import html

user_input = st.text_input("Enter data")
safe_input = html.escape(user_input)  # Prevent XSS
```

### 4. Don't Expose Sensitive Info

```python
# ❌ Bad
st.write(f"API Key: {secret_key}")

# ✅ Good
st.write(f"API Key: {'*' * 20}{secret_key[-4:]}")
```

---

## 📊 Session State Management

### Accessing Session State

```python
# Check authentication
if st.session_state.get("authenticated", False):
    st.write("Logged in!")

# Get user info
user_info = st.session_state.get("user_info", {})
user_name = user_info.get("name", "User")
```

### Storing Page-Specific Data

```python
# Initialize page-specific state
if "my_page_data" not in st.session_state:
    st.session_state.my_page_data = []

# Add data
if st.button("Add Item"):
    st.session_state.my_page_data.append("New Item")

# Display data
st.write(st.session_state.my_page_data)
```

### Clearing State on Logout

The `logout()` function automatically clears authentication state. Add custom cleanup if needed:

```python
from SSO import logout

def custom_logout():
    # Clear custom state
    if "my_custom_data" in st.session_state:
        del st.session_state.my_custom_data

    # Call standard logout
    logout()
```

---

## 🧪 Testing New Pages

### 1. Test Authentication

- [ ] Try accessing the page without logging in
- [ ] Verify error message appears
- [ ] Confirm redirection guidance is shown
- [ ] Log in and verify page loads

### 2. Test Functionality

- [ ] All buttons work
- [ ] Forms submit correctly
- [ ] Data persists as expected
- [ ] Error handling works

### 3. Test UI/UX

- [ ] Page renders correctly on desktop
- [ ] Page renders correctly on mobile
- [ ] All text is readable
- [ ] Navigation works smoothly

### 4. Test Performance

- [ ] Page loads quickly (<2 seconds)
- [ ] No unnecessary reruns
- [ ] Data caching works (if implemented)

---

## 🚀 Deployment

### File Requirements

When deploying, ensure all files are included:

```
├── app.py              ✅ Required
├── pages/              ✅ Required (entire directory)
├── SSO/                ✅ Required (entire package)
├── requirements.txt    ✅ Required
├── .env               ⚠️ Never commit!
└── .streamlit/         ✅ Optional (config)
```

### Update Requirements

If you add new dependencies, update `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Or manually add:

```txt
streamlit==1.31.0
msal==1.26.0
python-dotenv==1.0.1
streamlit-cookies-controller==0.0.2
pandas>=1.5.0        # If using pandas
plotly>=5.0.0        # If using plotly
```

---

## 📚 Examples & Templates

### Example: Data Table Page

```python
@require_authentication
def main():
    init_session_state()
    render_authenticated_header("📋 Data Table")

    # Sample data
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['NYC', 'LA', 'Chicago']
    })

    # Editable table
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",  # Allow adding rows
        use_container_width=True
    )

    # Export button
    if st.button("Export to CSV"):
        csv = edited_df.to_csv(index=False)
        st.download_button(
            "Download CSV",
            csv,
            "data.csv",
            "text/csv"
        )
```

### Example: Form Page

```python
@require_authentication
def main():
    init_session_state()
    render_authenticated_header("📝 Submit Form")

    with st.form("feedback_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        rating = st.slider("Rating", 1, 5)
        comments = st.text_area("Comments")

        submitted = st.form_submit_button("Submit")

        if submitted:
            # Process form
            st.success("Thank you for your feedback!")
            st.balloons()
```

---

## 🆘 Troubleshooting

### Page Not Appearing in Sidebar

**Cause**: Filename format or location issue

**Fix**:
- Ensure file is in `pages/` directory
- Check filename starts with number: `1_`
- Verify `.py` extension

### Authentication Not Working

**Cause**: Decorator not applied or session not initialized

**Fix**:
```python
# Make sure you have:
@require_authentication  # This line!
def main():
    init_session_state()  # And this!
```

### Page Shows Blank After Login

**Cause**: Error in page code

**Fix**:
- Check terminal for error messages
- Add try-except blocks
- Test page in isolation

### User Info Not Available

**Cause**: Accessing before initialization

**Fix**:
```python
# Always initialize first
init_session_state()

# Then access
user_name = get_user_name()
```

---

## 📖 Additional Resources

- **Streamlit Multipage Docs**: https://docs.streamlit.io/library/get-started/multipage-apps
- **Streamlit Components**: https://docs.streamlit.io/library/api-reference
- **Main README**: [README.md](README.md)
- **Production Guide**: [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)

---

**Happy Building! 🚀**
