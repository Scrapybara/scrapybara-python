# coding: utf-8

"""
    Scrapybara API

    Scrapybara API provides web automation, capybara-style. It allows users to generate, execute, and manage scripts.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from scrapybara.api.script_execution_api import ScriptExecutionApi


class TestScriptExecutionApi(unittest.TestCase):
    """ScriptExecutionApi unit test stubs"""

    def setUp(self) -> None:
        self.api = ScriptExecutionApi()

    def tearDown(self) -> None:
        pass

    def test_execute_script(self) -> None:
        """Test case for execute_script

        Execute script
        """
        pass


if __name__ == '__main__':
    unittest.main()
