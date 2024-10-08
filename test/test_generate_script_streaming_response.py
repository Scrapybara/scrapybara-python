# coding: utf-8

"""
    Scrapybara API

    Scrapybara API provides web automation, capybara-style. It allows users to generate, execute, and manage scripts.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from scrapybara.models.generate_script_streaming_response import GenerateScriptStreamingResponse

class TestGenerateScriptStreamingResponse(unittest.TestCase):
    """GenerateScriptStreamingResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GenerateScriptStreamingResponse:
        """Test GenerateScriptStreamingResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GenerateScriptStreamingResponse`
        """
        model = GenerateScriptStreamingResponse()
        if include_optional:
            return GenerateScriptStreamingResponse(
                script_id = '',
                status = '',
                status_description = '',
                current_script = '',
                current_script_execution_result = '',
                reasoning = '',
                streaming = True
            )
        else:
            return GenerateScriptStreamingResponse(
                script_id = '',
                status = '',
                status_description = '',
                streaming = True,
        )
        """

    def testGenerateScriptStreamingResponse(self):
        """Test GenerateScriptStreamingResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
