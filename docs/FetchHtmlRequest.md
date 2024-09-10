# FetchHtmlRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | The URL of the webpage to fetch HTML content from. | 

## Example

```python
from scrapybara.models.fetch_html_request import FetchHtmlRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FetchHtmlRequest from a JSON string
fetch_html_request_instance = FetchHtmlRequest.from_json(json)
# print the JSON string representation of the object
print(FetchHtmlRequest.to_json())

# convert the object into a dict
fetch_html_request_dict = fetch_html_request_instance.to_dict()
# create an instance of FetchHtmlRequest from a dict
fetch_html_request_from_dict = FetchHtmlRequest.from_dict(fetch_html_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


