# scrapybara.ScriptManagementApi

All URIs are relative to *https://api.scrapybara.com/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_script**](ScriptManagementApi.md#delete_script) | **DELETE** /scripts/{script_id} | Delete script
[**get_script**](ScriptManagementApi.md#get_script) | **GET** /scripts/{script_id} | Get script


# **delete_script**
> delete_script(script_id)

Delete script

Permanently removes a script from the system.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import scrapybara
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
    api_instance = scrapybara.ScriptManagementApi(api_client)
    script_id = 'script_id_example' # str | Unique identifier of the script to be deleted.

    try:
        # Delete script
        api_instance.delete_script(script_id)
    except Exception as e:
        print("Exception when calling ScriptManagementApi->delete_script: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **script_id** | **str**| Unique identifier of the script to be deleted. | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Script deleted successfully. |  -  |
**401** | Unauthorized - Invalid or missing API key. |  -  |
**404** | Script not found - The specified script ID does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_script**
> GetScriptResponse get_script(script_id)

Get script

Retrieves detailed information about a specific script.

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import scrapybara
from scrapybara.models.get_script_response import GetScriptResponse
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
    api_instance = scrapybara.ScriptManagementApi(api_client)
    script_id = 'script_id_example' # str | Unique identifier of the script.

    try:
        # Get script
        api_response = api_instance.get_script(script_id)
        print("The response of ScriptManagementApi->get_script:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScriptManagementApi->get_script: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **script_id** | **str**| Unique identifier of the script. | 

### Return type

[**GetScriptResponse**](GetScriptResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response with script details. |  -  |
**401** | Unauthorized - Invalid or missing API key. |  -  |
**404** | Script not found - The specified script ID does not exist. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

