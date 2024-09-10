# ExecuteScriptResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | The current execution status (e.g., &#39;in_progress&#39;, &#39;completed&#39;, &#39;error&#39;). | 
**status_description** | **str** | Additional details about the current execution status or errors. | 
**result** | **object** | The data extracted by the script. | 
**streaming** | **bool** |  | 

## Example

```python
from scrapybara.models.execute_script_response import ExecuteScriptResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ExecuteScriptResponse from a JSON string
execute_script_response_instance = ExecuteScriptResponse.from_json(json)
# print the JSON string representation of the object
print(ExecuteScriptResponse.to_json())

# convert the object into a dict
execute_script_response_dict = execute_script_response_instance.to_dict()
# create an instance of ExecuteScriptResponse from a dict
execute_script_response_from_dict = ExecuteScriptResponse.from_dict(execute_script_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


