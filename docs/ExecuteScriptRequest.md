# ExecuteScriptRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**script_id** | **str** | Unique identifier of the script to be executed. | 
**streaming** | **bool** | If true, the execution results will be streamed as they&#39;re generated. | [optional] [default to False]
**magic** | **bool** | If true, applies advanced processing to improve data extraction results. | [optional] [default to False]
**url** | **str** | Optional URL to override the script&#39;s default target URL. | [optional] 

## Example

```python
from scrapybara.models.execute_script_request import ExecuteScriptRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExecuteScriptRequest from a JSON string
execute_script_request_instance = ExecuteScriptRequest.from_json(json)
# print the JSON string representation of the object
print(ExecuteScriptRequest.to_json())

# convert the object into a dict
execute_script_request_dict = execute_script_request_instance.to_dict()
# create an instance of ExecuteScriptRequest from a dict
execute_script_request_from_dict = ExecuteScriptRequest.from_dict(execute_script_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


