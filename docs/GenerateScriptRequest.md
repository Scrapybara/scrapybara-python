# GenerateScriptRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | The target URL for the script. | 
**command** | **str** | The action to be performed by the script. | 
**steps** | **List[str]** | Optional step-by-step instructions for complex actions. | [optional] 
**input_schema** | **object** | Optional schema defining the structure of input data. | [optional] 
**output_schema** | **object** | Optional schema defining the expected structure of output data. | [optional] 

## Example

```python
from scrapybara.models.generate_script_request import GenerateScriptRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateScriptRequest from a JSON string
generate_script_request_instance = GenerateScriptRequest.from_json(json)
# print the JSON string representation of the object
print(GenerateScriptRequest.to_json())

# convert the object into a dict
generate_script_request_dict = generate_script_request_instance.to_dict()
# create an instance of GenerateScriptRequest from a dict
generate_script_request_from_dict = GenerateScriptRequest.from_dict(generate_script_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


