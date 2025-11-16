"""
Microsoft Graph API Client

Provides read-only access to Azure AD user and role information.
Used by admin pages to display real user data.
"""

import requests
import logging
from typing import List, Dict, Optional
import streamlit as st
from .config import CLIENT_ID, CLIENT_SECRET, TENANT_ID

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphAPIClient:
    """Client for Microsoft Graph API operations."""

    def __init__(self):
        self.tenant_id = TENANT_ID
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.graph_url = "https://graph.microsoft.com/v1.0"
        self._access_token = None

    def _get_access_token(self) -> Optional[str]:
        """
        Get access token for Microsoft Graph API using client credentials flow.

        Returns:
            str: Access token or None if failed
        """
        if self._access_token:
            return self._access_token

        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials"
        }

        try:
            response = requests.post(token_url, data=data, timeout=10)
            response.raise_for_status()
            self._access_token = response.json().get("access_token")
            logger.info("Successfully obtained Graph API access token")
            return self._access_token
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get Graph API token: {e}")
            return None

    def _make_request(self, endpoint: str) -> Optional[Dict]:
        """
        Make authenticated request to Graph API.

        Args:
            endpoint (str): API endpoint (e.g., "/users")

        Returns:
            dict: Response data or None if failed
        """
        token = self._get_access_token()
        if not token:
            return None

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        url = f"{self.graph_url}{endpoint}"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Graph API request failed: {e}")
            return None

    def get_users(self, top: int = 50) -> List[Dict]:
        """
        Get list of users from Azure AD.

        Args:
            top (int): Maximum number of users to retrieve

        Returns:
            List[Dict]: List of user objects
        """
        endpoint = f"/users?$top={top}&$select=id,displayName,mail,userPrincipalName,accountEnabled"

        result = self._make_request(endpoint)

        if result and "value" in result:
            logger.info(f"Retrieved {len(result['value'])} users from Azure AD")
            return result["value"]

        logger.warning("No users retrieved from Azure AD")
        return []

    def get_user_app_role_assignments(self, user_id: str) -> List[str]:
        """
        Get app role assignments for a specific user.

        Args:
            user_id (str): User's object ID

        Returns:
            List[str]: List of role names assigned to user
        """
        # This would require additional Graph API calls and app-specific logic
        # For now, returning empty list as placeholder
        # In production, you'd query the enterprise app role assignments
        return []

    def get_application_users(self, app_id: str) -> List[Dict]:
        """
        Get users assigned to the application with their roles.

        Args:
            app_id (str): Application (Service Principal) object ID

        Returns:
            List[Dict]: List of users with role assignments
        """
        endpoint = f"/servicePrincipals/{app_id}/appRoleAssignedTo"

        result = self._make_request(endpoint)

        if result and "value" in result:
            return result["value"]

        return []


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_cached_users(top: int = 50) -> List[Dict]:
    """
    Get users with caching to reduce API calls.

    Args:
        top (int): Maximum number of users

    Returns:
        List[Dict]: List of user objects
    """
    try:
        client = GraphAPIClient()
        return client.get_users(top)
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return []


@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_cached_app_users(app_id: str) -> List[Dict]:
    """
    Get application role assignments with caching.

    Args:
        app_id (str): Application ID

    Returns:
        List[Dict]: List of role assignments
    """
    try:
        client = GraphAPIClient()
        return client.get_application_users(app_id)
    except Exception as e:
        logger.error(f"Error fetching app users: {e}")
        return []


def is_graph_api_configured() -> bool:
    """
    Check if Graph API credentials are configured.

    Returns:
        bool: True if configured, False otherwise
    """
    return bool(TENANT_ID and CLIENT_ID and CLIENT_SECRET)
