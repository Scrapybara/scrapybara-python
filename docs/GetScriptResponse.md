# GetScriptResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of the script. | [optional] 
**url** | **str** | The target URL for the script. | [optional] 
**command** | **str** | The original action or instructions. | [optional] 
**steps** | **object** | Detailed steps for the action. | [optional] 
**content** | **str** | The actual code content of the script. | [optional] 
**status** | **str** | Current status of the script (e.g., &#39;pending&#39;, &#39;completed&#39;, &#39;error&#39;). | [optional] 
**status_description** | **str** | Additional details about the script&#39;s status. | [optional] 

## Example

```python
from scrapybara.models.get_script_response import GetScriptResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetScriptResponse from a JSON string
get_script_response_instance = GetScriptResponse.from_json(json)
# print the JSON string representation of the object
print(GetScriptResponse.to_json())

# convert the object into a dict
get_script_response_dict = get_script_response_instance.to_dict()
# create an instance of GetScriptResponse from a dict
get_script_response_from_dict = GetScriptResponse.from_dict(get_script_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


