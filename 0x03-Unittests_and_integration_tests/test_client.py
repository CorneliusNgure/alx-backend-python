#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient class.

- Covers org property (with memoization), and
- ensures no real HTTP calls are made using patch.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the expected value.
        - get_json is called once with the correct URL.
        - The returned org data is exactly what get_json returns.
        """

        expected_url = f"https://api.github.com/orgs/{org_name}"
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, expected_payload)


if __name__ == "__main__":
    unittest.main()
