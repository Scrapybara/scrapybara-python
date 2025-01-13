from scrapybara import Scrapybara
import os

from scrapybara.anthropic import Anthropic
from scrapybara.prompts import SYSTEM_PROMPT
from scrapybara.tools import BashTool, BrowserTool, ComputerTool, EditTool


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

    messages = client.act(
        model=Anthropic(),
        system=SYSTEM_PROMPT,
        prompt="Go to the YC website and fetch the HTML",
        tools=[
            ComputerTool(instance),
            BashTool(instance),
            EditTool(instance),
            BrowserTool(instance),
        ],
        on_step=lambda step: print(f"{step}\n"),
    )
    assert len(messages) > 0

    instance.browser.stop()
    instance.stop()


if __name__ == "__main__":
    test_client()
