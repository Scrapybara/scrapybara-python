# GenerateScriptNonStreamingResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier for the generated script. | 
**streaming** | **bool** |  | 

## Example

```python
from scrapybara.models.generate_script_non_streaming_response import GenerateScriptNonStreamingResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateScriptNonStreamingResponse from a JSON string
generate_script_non_streaming_response_instance = GenerateScriptNonStreamingResponse.from_json(json)
# print the JSON string representation of the object
print(GenerateScriptNonStreamingResponse.to_json())

# convert the object into a dict
generate_script_non_streaming_response_dict = generate_script_non_streaming_response_instance.to_dict()
# create an instance of GenerateScriptNonStreamingResponse from a dict
generate_script_non_streaming_response_from_dict = GenerateScriptNonStreamingResponse.from_dict(generate_script_non_streaming_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


