from scrapybara import Scrapybara


def test_client() -> None:
    client = Scrapybara(api_key="scrapy-8bb02c63-1339-4aeb-bae2-b6beea0485cb")
    instance = client.start()
    assert instance.id is not None
    screenshot_response = instance.screenshot()
    assert screenshot_response.base_64_image is not None
    instance.stop()
