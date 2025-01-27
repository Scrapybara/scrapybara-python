from pydantic import BaseModel
from scrapybara import Scrapybara
import os

from scrapybara.anthropic import Anthropic
from scrapybara.prompts import (
    BROWSER_SYSTEM_PROMPT,
    UBUNTU_SYSTEM_PROMPT,
    WINDOWS_SYSTEM_PROMPT,
)
from scrapybara.tools import BashTool, ComputerTool, EditTool


class YCStats(BaseModel):
    number_of_startups: int
    combined_valuation: int


def test_client() -> None:
    if os.getenv("SCRAPYBARA_API_KEY") is None:
        raise ValueError("SCRAPYBARA_API_KEY is not set")
    client = Scrapybara(
        base_url="https://scrapybara-api-alpha-47247185186.us-central1.run.app"
    )

    # Ubuntu test
    ubuntu_instance = client.start_ubuntu()
    assert ubuntu_instance.id is not None
    instances = client.get_instances()
    assert len(instances) > 0
    screenshot_response = ubuntu_instance.screenshot()
    assert screenshot_response.base_64_image is not None
    ubuntu_instance.browser.start()
    cdp_url = ubuntu_instance.browser.get_cdp_url()
    assert cdp_url is not None
    response = client.act(
        model=Anthropic(),
        system=UBUNTU_SYSTEM_PROMPT,
        prompt="Go to the YC website and get the number of funded startups and combined valuation",
        tools=[
            ComputerTool(ubuntu_instance),
            BashTool(ubuntu_instance),
            EditTool(ubuntu_instance),
        ],
        schema=YCStats,
    )
    print(response)
    assert response.output is not None
    assert response.output.number_of_startups is not None
    assert response.output.combined_valuation is not None
    ubuntu_instance.browser.stop()
    ubuntu_instance.stop()

    # Browser test
    browser_instance = client.start_browser()
    assert browser_instance.id is not None
    screenshot_response = browser_instance.screenshot()
    assert screenshot_response.base_64_image is not None
    cdp_url = browser_instance.get_cdp_url()
    assert cdp_url is not None
    response = client.act(
        model=Anthropic(),
        system=BROWSER_SYSTEM_PROMPT,
        prompt="Go to the YC website and get the number of funded startups and combined valuation",
        tools=[
            ComputerTool(browser_instance),
        ],
    )
    print(response)
    assert response.output is not None
    assert response.output.number_of_startups is not None
    assert response.output.combined_valuation is not None
    browser_instance.stop()

    # Windows test
    windows_instance = client.start_windows()
    assert windows_instance.id is not None
    screenshot_response = windows_instance.screenshot()
    assert screenshot_response.base_64_image is not None
    response = client.act(
        model=Anthropic(),
        system=WINDOWS_SYSTEM_PROMPT,
        prompt="Go to the YC website and get the number of funded startups and combined valuation",
        tools=[
            ComputerTool(windows_instance),
        ],
    )
    print(response)
    assert response.output is not None
    assert response.output.number_of_startups is not None
    assert response.output.combined_valuation is not None
    windows_instance.stop()


if __name__ == "__main__":
    test_client()
