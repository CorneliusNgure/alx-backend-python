#!/usr/bin/env python3
"""
Unit tests for the utils module.

This module covers:
- access_nested_map
- get_json
- memoize

It demonstrates testing patterns such as mocking, parametrization,
and memoization checks.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the utils.access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the expected value
        when provided with valid nested maps and paths.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(
        self, nested_map, path, expected_message
    ):
        """
        Test that access_nested_map raises a KeyError when
        provided with invalid paths, and that the exception
        message matches the expected value.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_message)


class TestGetJson(unittest.TestCase):
    """Unit tests for the utils.get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that get_json retrieves JSON content from the
        provided URL using a mocked requests.get call.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Unit tests for the utils.memoize decorator."""

    def test_memoize(self):
        """
        Test that the memoize decorator caches the result of
        a method so that it is only called once for multiple
        accesses.
        """

        class TestClass:
            """Helper class to test the memoize decorator."""

            def a_method(self):
                """Return a fixed integer value."""
                return 42

            @memoize
            def a_property(self):
                """Call a_method and return its result, memoized."""
                return self.a_method()

        with patch.object(
            TestClass, "a_method", return_value=42
        ) as mock_method:
            obj = TestClass()

            result1 = obj.a_property
            result2 = obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
