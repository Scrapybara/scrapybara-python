# GenerateScriptResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier for the generated script. | 

## Example

```python
from scrapybara.models.generate_script_response import GenerateScriptResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateScriptResponse from a JSON string
generate_script_response_instance = GenerateScriptResponse.from_json(json)
# print the JSON string representation of the object
print(GenerateScriptResponse.to_json())

# convert the object into a dict
generate_script_response_dict = generate_script_response_instance.to_dict()
# create an instance of GenerateScriptResponse from a dict
generate_script_response_from_dict = GenerateScriptResponse.from_dict(generate_script_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


