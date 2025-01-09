from scrapybara import Scrapybara
import os


def test_client() -> None:
    if os.getenv("SCRAPYBARA_API_KEY") is None:
        raise ValueError("SCRAPYBARA_API_KEY is not set")
    client = Scrapybara()
    instance = client.start()
    assert instance.id is not None
    instances = client.get_instances()
    assert len(instances) > 0
    screenshot_response = instance.screenshot()
    assert screenshot_response.base_64_image is not None
    instance.browser.start()
    cdp_url = instance.browser.get_cdp_url()
    assert cdp_url is not None
    instance.browser.stop()
    instance.stop()
