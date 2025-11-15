"""
Analytics Page - Protected by Azure AD SSO

This page demonstrates data visualization and analytics features.
Only accessible to authenticated users.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from SSO import (
    require_authentication,
    init_session_state,
    render_authenticated_header
)


@require_authentication
def main():
    """Main function for analytics page."""
    # Initialize session state FIRST
    init_session_state()

    st.set_page_config(
        page_title="Azure SSO App - Analytics",
        page_icon="📊",
        layout="wide"
    )

    # Render header with logout button
    render_authenticated_header("📊 Analytics Dashboard", show_logout=True)

    st.divider()

    # Page description
    st.write("""
    This page demonstrates data visualization capabilities with authentication protection.
    All data shown here is randomly generated for demonstration purposes.
    """)

    st.divider()

    # Key Performance Indicators
    st.subheader("📈 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Users",
            "1,234",
            delta="12%",
            help="Total registered users"
        )

    with col2:
        st.metric(
            "Active Sessions",
            "456",
            delta="-5%",
            delta_color="inverse",
            help="Currently active sessions"
        )

    with col3:
        st.metric(
            "Revenue",
            "$45.2K",
            delta="23%",
            help="Monthly revenue"
        )

    with col4:
        st.metric(
            "Conversion Rate",
            "3.2%",
            delta="0.5%",
            help="User conversion rate"
        )

    st.divider()

    # Charts Section
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📉 User Growth Trend")

        # Generate sample data
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=30),
            end=datetime.now(),
            freq='D'
        )
        users = np.cumsum(np.random.randint(10, 50, size=len(dates))) + 1000

        chart_data = pd.DataFrame({
            'Date': dates,
            'Users': users
        })

        st.line_chart(chart_data.set_index('Date'))

    with col2:
        st.subheader("📊 Traffic by Source")

        # Generate sample data
        traffic_data = pd.DataFrame({
            'Source': ['Organic', 'Direct', 'Referral', 'Social', 'Email'],
            'Visitors': [450, 320, 180, 150, 90]
        })

        st.bar_chart(traffic_data.set_index('Source'))

    st.divider()

    # Data Table Section
    st.subheader("📋 Recent Activity")

    # Generate sample activity data
    activity_data = pd.DataFrame({
        'Timestamp': pd.date_range(end=datetime.now(), periods=10, freq='H')[::-1],
        'User': [f'User{i}' for i in range(1, 11)],
        'Action': np.random.choice(['Login', 'View Page', 'Download', 'Update Profile'], 10),
        'Status': np.random.choice(['Success', 'Success', 'Success', 'Failed'], 10)
    })

    st.dataframe(
        activity_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Interactive Filters
    st.subheader("🔍 Interactive Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime.now() - timedelta(days=7), datetime.now()),
            help="Filter data by date range"
        )

    with col2:
        metric_type = st.selectbox(
            "Metric Type",
            ["Users", "Revenue", "Sessions", "Conversions"],
            help="Select metric to analyze"
        )

    with col3:
        aggregation = st.selectbox(
            "Aggregation",
            ["Daily", "Weekly", "Monthly"],
            help="Select aggregation period"
        )

    if st.button("Apply Filters", type="primary"):
        st.success(f"✅ Filters applied: {metric_type} aggregated {aggregation}")

    st.divider()

    # Additional Metrics
    st.subheader("💡 Additional Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **Peak Activity Time**

        🕐 Most users are active between 2 PM - 4 PM

        Consider scheduling updates during off-peak hours.
        """)

    with col2:
        st.warning("""
        **Attention Required**

        ⚠️ Bounce rate increased by 8% this week

        Review landing page optimization.
        """)

    # Footer
    st.divider()
    st.caption(f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption("💡 **Note**: All data on this page is randomly generated for demonstration purposes.")


if __name__ == "__main__":
    main()
