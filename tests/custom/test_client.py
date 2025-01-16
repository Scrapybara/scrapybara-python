from pydantic import BaseModel
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

    class YCStats(BaseModel):
        number_of_startups: int
        combined_valuation: int

    response = client.act(
        model=Anthropic(),
        system=SYSTEM_PROMPT,
        prompt="Go to the YC website and get the number of funded startups and combined valuation",
        tools=[
            ComputerTool(instance),
            BashTool(instance),
            EditTool(instance),
            BrowserTool(instance),
        ],
        schema=YCStats,
    )
    print(response)

    assert response.output is not None
    assert response.output.number_of_startups is not None
    assert response.output.combined_valuation is not None

    instance.browser.stop()
    instance.stop()


if __name__ == "__main__":
    test_client()
