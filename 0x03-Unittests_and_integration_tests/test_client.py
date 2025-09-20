#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient class.

- Covers org property (with memoization), and
- ensures no real HTTP calls are made using patch.
"""

import unittest
from unittest import TestCase
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized_class


class TestGithubOrgClient(TestCase):
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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that GithubOrgClient.has_license correctly evaluates licenses.

        - Ensure it returns True when repo license matches license_key, and
        - returns False when repo license does not match license_key.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
  
@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": [
            "episodes.dart",
            "cpp-netlib",
            "dagger",
            "ios-webkit-debug-proxy",
            "google.github.io",
            "kratu",
            "build-debian-cloud",
            "traceur-compiler",
            "firmata.py",
        ],
        "apache2_repos": [
            "dagger",
            "kratu",
            "traceur-compiler",
            "firmata.py",
        ],
    }
])
class TestIntegrationGithubOrgClient(TestCase):
    """Integration tests for GithubOrgClient.public_repos with fixtures."""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and set up mock side_effect."""
        # promote instance attrs (from parameterized_class) to class attrs
        dummy = cls()
        cls.org_payload = dummy.org_payload
        cls.repos_payload = dummy.repos_payload
        cls.expected_repos = dummy.expected_repos
        cls.apache2_repos = dummy.apache2_repos

        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Mocked side_effect function for requests.get."""
            mock_response = Mock()
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo names."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos by license works."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos,
        )


if __name__ == "__main__":
    unittest.main()
