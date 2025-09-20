#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient class.

- Covers org property (with memoization), and
- ensures no real HTTP calls are made using patch.
"""

import unittest
from unittest.mock import patch, PropertyMock
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

    def test_public_repos_url(self):
        """
        Test that GithubOrgClient._public_repos_url returns the expected value.

        - Ensure value comes from the "repos_url" in the mocked org payload.
        """

        expected_url = "https://api.github.com/orgs/test/repos"
        payload = {"repos_url": expected_url}

        with patch.object(
                GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("test")
            result = client._public_repos_url

            self.assertEqual(result, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Ensure GithubOrgClient.public_repos returns the expected list.

        - Ensure GithubOrgClient._public_repos_url is used,
        - get_json is called once with the mocked URL, and
        - the list of repo names matches the mocked payload.
        """

        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mock_repos_payload

        expected_url = "https://api.github.com/orgs/test/repos"

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value=expected_url,
        ) as mock_repos_url:
            client = GithubOrgClient("test")
            result = client.public_repos()

            # Assert
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(expected_url)


if __name__ == "__main__":
    unittest.main()
