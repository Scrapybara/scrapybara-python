from scrapybara import Scrapybara


def test_client() -> None:
    client = Scrapybara()
    instance = client.start()
    assert instance.id is not None
    screenshot_response = instance.screenshot()
    assert screenshot_response.base_64_image is not None
    instance.stop()
