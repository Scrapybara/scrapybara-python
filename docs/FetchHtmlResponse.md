# FetchHtmlResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**html** | **str** | The raw HTML content of the requested URL. | [optional] 

## Example

```python
from scrapybara.models.fetch_html_response import FetchHtmlResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FetchHtmlResponse from a JSON string
fetch_html_response_instance = FetchHtmlResponse.from_json(json)
# print the JSON string representation of the object
print(FetchHtmlResponse.to_json())

# convert the object into a dict
fetch_html_response_dict = fetch_html_response_instance.to_dict()
# create an instance of FetchHtmlResponse from a dict
fetch_html_response_from_dict = FetchHtmlResponse.from_dict(fetch_html_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


