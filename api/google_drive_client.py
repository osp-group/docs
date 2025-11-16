#!/usr/bin/env python3
"""
Google Drive Validator API Client - Python SDK

Purpose:
  - Easy-to-use Python client for the Google Drive Validator API
  - Query link status and permissions
  - Validate individual URLs
  - Trigger full validations

Usage:
  from api.google_drive_client import GoogleDriveValidatorClient
  
  # Initialize client
  client = GoogleDriveValidatorClient("http://localhost:5000")
  
  # Get status
  status = client.get_status()
  
  # Get all links
  links = client.get_all_links()
  
  # Get hub links
  vendas_links = client.get_hub_links("VENDAS")
  
  # Validate single URL
  result = client.validate_url("https://docs.google.com/document/d/...")
  
  # Validate all links
  validation_results = client.validate_all()

Installation:
  pip install requests
"""

import requests
from typing import Dict, List, Optional
from urllib.parse import urljoin


class GoogleDriveValidatorClient:
    """Client for Google Drive Validator API."""

    def __init__(self, base_url: str = "http://localhost:5000", timeout: int = 30):
        """
        Initialize the API client.

        Args:
            base_url: Base URL of the API server (default: localhost:5000)
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
    ) -> Dict:
        """
        Make HTTP request to API.

        Args:
            method: HTTP method (GET, POST, etc)
            endpoint: API endpoint (without base URL)
            data: Request body data (for POST requests)

        Returns:
            Response JSON as dictionary

        Raises:
            requests.RequestException: If request fails
        """
        url = urljoin(self.base_url, endpoint)

        try:
            if method.upper() == "GET":
                response = self.session.get(url, timeout=self.timeout)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Cannot connect to API at {self.base_url}")
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Request to {endpoint} timed out after {self.timeout}s")
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"API error: {e.response.status_code} - {e.response.text}")

    def health_check(self) -> Dict:
        """Check if API is healthy and ready."""
        return self._request("GET", "/health")

    def get_status(self) -> Dict:
        """Get overall validation status of all links."""
        return self._request("GET", "/api/v1/status")

    def get_all_links(self) -> Dict:
        """Get all links from all hubs with validation status."""
        return self._request("GET", "/api/v1/links")

    def get_hub_links(self, hub_name: str) -> Dict:
        """
        Get links from a specific hub.

        Args:
            hub_name: Hub name (VENDAS, CONHECIMENTO, DADOS_INTELIGENCIA, MARKETING)

        Returns:
            Dictionary with hub links and validation status
        """
        return self._request("GET", f"/api/v1/links/{hub_name}")

    def get_link_details(self, hub_name: str, doc_id: str) -> Dict:
        """
        Get details for a specific link.

        Args:
            hub_name: Hub name
            doc_id: Google Drive document ID

        Returns:
            Link details including validation and permissions
        """
        return self._request("GET", f"/api/v1/links/{hub_name}/{doc_id}")

    def validate_url(self, url: str) -> Dict:
        """
        Validate a single Google Drive URL.

        Args:
            url: Google Drive URL to validate

        Returns:
            Validation result with accessibility and permissions
        """
        return self._request("POST", "/api/v1/validate", {"url": url})

    def validate_all_links(self) -> Dict:
        """Trigger full validation of all links."""
        return self._request("POST", "/api/v1/validate/all", {})

    def get_permissions_summary(self) -> Dict:
        """Get audit summary of all permissions."""
        return self._request("GET", "/api/v1/permissions")

    def get_accessible_links(self, hub_name: Optional[str] = None) -> List[Dict]:
        """
        Get only accessible links.

        Args:
            hub_name: Optional hub name to filter by

        Returns:
            List of accessible links
        """
        if hub_name:
            data = self.get_hub_links(hub_name)
            links = data.get("links", [])
        else:
            all_data = self.get_all_links()
            links = []
            for hub_links in all_data.get("hubs", {}).values():
                links.extend(hub_links)

        return [link for link in links if link.get("validation", {}).get("accessible")]

    def get_inaccessible_links(self, hub_name: Optional[str] = None) -> List[Dict]:
        """
        Get only inaccessible links.

        Args:
            hub_name: Optional hub name to filter by

        Returns:
            List of inaccessible links
        """
        if hub_name:
            data = self.get_hub_links(hub_name)
            links = data.get("links", [])
        else:
            all_data = self.get_all_links()
            links = []
            for hub_links in all_data.get("hubs", {}).values():
                links.extend(hub_links)

        return [link for link in links if not link.get("validation", {}).get("accessible")]

    def get_not_shared_with_osp_group(self) -> List[Dict]:
        """Get all accessible links NOT shared with @osp-group."""
        all_data = self.get_all_links()
        links = []

        for hub_links in all_data.get("hubs", {}).values():
            for link in hub_links:
                validation = link.get("validation", {})
                if (
                    validation.get("accessible")
                    and not validation.get("shared_with_osp_group")
                ):
                    links.append(link)

        return links

    def get_public_links(self) -> List[Dict]:
        """Get all public links."""
        all_data = self.get_all_links()
        links = []

        for hub_links in all_data.get("hubs", {}).values():
            for link in hub_links:
                validation = link.get("validation", {})
                if validation.get("public"):
                    links.append(link)

        return links


def main():
    """Example usage of the client."""
    # Initialize client
    client = GoogleDriveValidatorClient()

    # Test connection
    try:
        health = client.health_check()
        print(f"✅ API Health: {health['status']}")
    except ConnectionError as e:
        print(f"❌ Connection error: {e}")
        return

    # Get status
    try:
        status = client.get_status()
        print(f"\n📊 Validation Status:")
        print(f"  Total: {status['validation']['total']}")
        print(f"  Accessible: {status['validation']['accessible']}")
        print(f"  Inaccessible: {status['validation']['inaccessible']}")
    except Exception as e:
        print(f"❌ Error getting status: {e}")

    # Get hub links
    try:
        vendas = client.get_hub_links("VENDAS")
        print(f"\n📄 VENDAS Hub:")
        print(f"  Total links: {vendas['total']}")
        print(f"  Accessible: {vendas['accessible']}")
    except Exception as e:
        print(f"❌ Error getting VENDAS links: {e}")

    # Get permission summary
    try:
        permissions = client.get_permissions_summary()
        print(f"\n🔐 Permission Summary:")
        print(f"  Total: {permissions['total']}")
        print(f"  Shared with @osp-group: {permissions['shared_with_osp_group']}")
        print(f"  Public: {permissions['public']}")
    except Exception as e:
        print(f"❌ Error getting permissions: {e}")


if __name__ == "__main__":
    main()
