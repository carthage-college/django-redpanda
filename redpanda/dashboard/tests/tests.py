# -*- coding: utf-8 -*-

from django.test import TestCase


class YourTestClass(TestCase):
    """Tests for this module."""

    def setUp(self):
        """Setup run before every test method."""
        print("setUp: Run once for every test method to setup clean data.")

    def tearDown(self):
        """Clean up run after every test method."""
        print("tearDown: Run once for every test method to clean up.")

    def test_something_that_will_pass(self):
        """Pass a test."""
        self.assertFalse(False)

    def test_something_that_will_fail(self):
        """Fail a test."""
        self.assertTrue(False)
