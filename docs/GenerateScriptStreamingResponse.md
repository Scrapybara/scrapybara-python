# GenerateScriptStreamingResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**script_id** | **str** | Unique identifier for the generated script. | 
**status** | **str** | The current status of script generation (e.g., &#39;in_progress&#39;, &#39;completed&#39;, &#39;error&#39;). | 
**status_description** | **str** | Additional details about the generation status or errors. | 
**current_script** | **str** | The current version of the generated script. | [optional] 
**current_script_execution_result** | **str** | The result of executing the current version of the script. | [optional] 
**reasoning** | **str** | Explanation of the reasoning behind the current script version. | [optional] 
**streaming** | **bool** |  | 

## Example

```python
from scrapybara.models.generate_script_streaming_response import GenerateScriptStreamingResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateScriptStreamingResponse from a JSON string
generate_script_streaming_response_instance = GenerateScriptStreamingResponse.from_json(json)
# print the JSON string representation of the object
print(GenerateScriptStreamingResponse.to_json())

# convert the object into a dict
generate_script_streaming_response_dict = generate_script_streaming_response_instance.to_dict()
# create an instance of GenerateScriptStreamingResponse from a dict
generate_script_streaming_response_from_dict = GenerateScriptStreamingResponse.from_dict(generate_script_streaming_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


