# scrapybara.ScriptGenerationApi

All URIs are relative to *https://api.scrapybara.com/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**generate_script**](ScriptGenerationApi.md#generate_script) | **POST** /scripts/generate | Generate script


# **generate_script**
> GenerateScriptResponse generate_script(generate_script_request)

Generate script

Auto-generates a new script. Use 'streaming' to get real-time updates on the script generation process.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import scrapybara
from scrapybara.models.generate_script_request import GenerateScriptRequest
from scrapybara.models.generate_script_response import GenerateScriptResponse
from scrapybara.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.scrapybara.com/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = scrapybara.Configuration(
    host = "https://api.scrapybara.com/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
async with scrapybara.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = scrapybara.ScriptGenerationApi(api_client)
    generate_script_request = scrapybara.GenerateScriptRequest() # GenerateScriptRequest | 

    try:
        # Generate script
        api_response = await api_instance.generate_script(generate_script_request)
        print("The response of ScriptGenerationApi->generate_script:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptGenerationApi->generate_script: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **generate_script_request** | [**GenerateScriptRequest**](GenerateScriptRequest.md)|  | 

### Return type

[**GenerateScriptResponse**](GenerateScriptResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response with the generated script ID. |  -  |
**401** | Unauthorized - Invalid or missing API key. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

