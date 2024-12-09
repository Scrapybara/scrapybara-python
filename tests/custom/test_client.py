from scrapybara import Scrapybara
import os


def test_client() -> None:
    if os.getenv("SCRAPYBARA_API_KEY") is None:
        raise ValueError("SCRAPYBARA_API_KEY is not set")
    client = Scrapybara(api_key=os.getenv("SCRAPYBARA_API_KEY"))
    instance = client.start()
    assert instance.id is not None
    screenshot_response = instance.screenshot()
    assert screenshot_response.base_64_image is not None
    instance.stop()
