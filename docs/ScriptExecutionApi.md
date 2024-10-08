# scrapybara.ScriptExecutionApi

All URIs are relative to *https://api.scrapybara.com/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**execute_script**](ScriptExecutionApi.md#execute_script) | **POST** /scripts/execute | Execute script


# **execute_script**
> ExecuteScriptResponse execute_script(execute_script_request)

Execute script

Executes a previously generated script.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import scrapybara
from scrapybara.models.execute_script_request import ExecuteScriptRequest
from scrapybara.models.execute_script_response import ExecuteScriptResponse
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
with scrapybara.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = scrapybara.ScriptExecutionApi(api_client)
    execute_script_request = scrapybara.ExecuteScriptRequest() # ExecuteScriptRequest | 

    try:
        # Execute script
        api_response = api_instance.execute_script(execute_script_request)
        print("The response of ScriptExecutionApi->execute_script:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptExecutionApi->execute_script: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **execute_script_request** | [**ExecuteScriptRequest**](ExecuteScriptRequest.md)|  | 

### Return type

[**ExecuteScriptResponse**](ExecuteScriptResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response with the execution results. |  -  |
**401** | Unauthorized - Invalid or missing API key. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

