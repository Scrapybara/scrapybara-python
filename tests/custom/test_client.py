from pydantic import BaseModel
from scrapybara import Scrapybara
import os
import pytest

from scrapybara.anthropic import (
    Anthropic,
    UBUNTU_SYSTEM_PROMPT as UBUNTU_SYSTEM_PROMPT_ANTHROPIC,
    BROWSER_SYSTEM_PROMPT as BROWSER_SYSTEM_PROMPT_ANTHROPIC,
    WINDOWS_SYSTEM_PROMPT as WINDOWS_SYSTEM_PROMPT_ANTHROPIC,
)
from scrapybara.openai import (
    OpenAI,
    UBUNTU_SYSTEM_PROMPT as UBUNTU_SYSTEM_PROMPT_OPENAI,
    BROWSER_SYSTEM_PROMPT as BROWSER_SYSTEM_PROMPT_OPENAI,
    WINDOWS_SYSTEM_PROMPT as WINDOWS_SYSTEM_PROMPT_OPENAI,
)
from scrapybara.tools import BashTool, ComputerTool, EditTool


class YCStats(BaseModel):
    number_of_startups: int
    combined_valuation: int


def _check_api_key() -> None:
    if os.getenv("SCRAPYBARA_API_KEY") is None:
        raise ValueError("SCRAPYBARA_API_KEY is not set")


def test_ubuntu() -> None:
    _check_api_key()
    client = Scrapybara()

    ubuntu_instance = client.start_ubuntu()
    print(ubuntu_instance.get_stream_url().stream_url)
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
        system=UBUNTU_SYSTEM_PROMPT_ANTHROPIC,
        prompt="Go to the YC website and get the number of funded startups and combined valuation",
        tools=[
            ComputerTool(ubuntu_instance),
            BashTool(ubuntu_instance),
            EditTool(ubuntu_instance),
        ],
        schema=YCStats,
        on_step=lambda step: print(step.text, step.tool_calls),
    )
    print(response.output)
    assert response.output is not None
    assert response.output.number_of_startups is not None
    assert response.output.combined_valuation is not None
    ubuntu_instance.browser.stop()
    ubuntu_instance.stop()

def test_ubuntu_openai() -> None:
    _check_api_key()
    client = Scrapybara()

    ubuntu_instance = client.start_ubuntu()
    print(ubuntu_instance.get_stream_url().stream_url)
    assert ubuntu_instance.id is not None
    instances = client.get_instances()
    assert len(instances) > 0
    screenshot_response = ubuntu_instance.screenshot()
    assert screenshot_response.base_64_image is not None
    ubuntu_instance.browser.start()
    cdp_url = ubuntu_instance.browser.get_cdp_url()
    assert cdp_url is not None
    response = client.act(
        model=OpenAI(),
        system=UBUNTU_SYSTEM_PROMPT_OPENAI,
        prompt="Go to the YC website and get the number of funded startups and combined valuation",
        tools=[
            ComputerTool(ubuntu_instance),
            BashTool(ubuntu_instance),
            EditTool(ubuntu_instance),
        ],
        schema=YCStats,
        on_step=lambda step: print(step.text, step.tool_calls),
    )
    print(response.output)
    assert response.output is not None
    assert response.output.number_of_startups is not None
    assert response.output.combined_valuation is not None
    ubuntu_instance.browser.stop()
    ubuntu_instance.stop()


def test_browser() -> None:
    _check_api_key()
    client = Scrapybara()

    browser_instance = client.start_browser()
    print(browser_instance.get_stream_url().stream_url)
    assert browser_instance.id is not None
    screenshot_response = browser_instance.screenshot()
    assert screenshot_response.base_64_image is not None
    cdp_url = browser_instance.get_cdp_url()
    assert cdp_url is not None
    response = client.act(
        model=Anthropic(),
        system=BROWSER_SYSTEM_PROMPT_ANTHROPIC,
        prompt="Go to the YC website and get the number of funded startups and combined valuation",
        tools=[
            ComputerTool(browser_instance),
        ],
        schema=YCStats,
        on_step=lambda step: print(step.text, step.tool_calls),
    )
    print(response.output)
    assert response.output is not None
    assert response.output.number_of_startups is not None
    assert response.output.combined_valuation is not None
    browser_instance.stop()

def test_browser_openai() -> None:
    _check_api_key()
    client = Scrapybara()

    browser_instance = client.start_browser()
    print(browser_instance.get_stream_url().stream_url)
    assert browser_instance.id is not None
    screenshot_response = browser_instance.screenshot()
    assert screenshot_response.base_64_image is not None
    cdp_url = browser_instance.get_cdp_url()
    assert cdp_url is not None
    response = client.act(
        model=OpenAI(),
        system=BROWSER_SYSTEM_PROMPT_OPENAI,
        prompt="Go to the YC website and get the number of funded startups and combined valuation",
        tools=[
            ComputerTool(browser_instance),
        ],
        schema=YCStats,
        on_step=lambda step: print(step.text, step.tool_calls),
    )
    print(response.output)
    assert response.output is not None
    assert response.output.number_of_startups is not None
    assert response.output.combined_valuation is not None
    browser_instance.stop()


@pytest.mark.skip()
def test_windows() -> None:
    _check_api_key()
    client = Scrapybara()

    windows_instance = client.start_windows()
    print(windows_instance.get_stream_url().stream_url)
    assert windows_instance.id is not None
    screenshot_response = windows_instance.screenshot()
    assert screenshot_response.base_64_image is not None
    response = client.act(
        model=Anthropic(),
        system=WINDOWS_SYSTEM_PROMPT_ANTHROPIC,
        prompt="Go to the YC website and get the number of funded startups and combined valuation",
        tools=[
            ComputerTool(windows_instance),
        ],
        schema=YCStats,
        on_step=lambda step: print(step.text, step.tool_calls),
    )
    print(response.output)
    assert response.output is not None
    assert response.output.number_of_startups is not None
    assert response.output.combined_valuation is not None
    windows_instance.stop()


@pytest.mark.skip()
def test_ubuntu_thinking() -> None:
    _check_api_key()
    client = Scrapybara()

    ubuntu_instance = client.start_ubuntu()
    print(ubuntu_instance.get_stream_url().stream_url)
    assert ubuntu_instance.id is not None
    instances = client.get_instances()
    assert len(instances) > 0
    screenshot_response = ubuntu_instance.screenshot()
    assert screenshot_response.base_64_image is not None
    ubuntu_instance.browser.start()
    cdp_url = ubuntu_instance.browser.get_cdp_url()
    assert cdp_url is not None
    response = client.act(
        model=Anthropic(name="claude-3-7-sonnet-20250219-thinking"),
        system=UBUNTU_SYSTEM_PROMPT_ANTHROPIC,
        prompt="Go to the YC website and get the number of funded startups and combined valuation",
        tools=[
            ComputerTool(ubuntu_instance),
            BashTool(ubuntu_instance),
            EditTool(ubuntu_instance),
        ],
        schema=YCStats,
        on_step=lambda step: print(step.text, step.tool_calls, step.reasoning_parts),
    )
    print(response.output)
    assert response.output is not None
    assert response.output.number_of_startups is not None
    assert response.output.combined_valuation is not None
    ubuntu_instance.browser.stop()
    ubuntu_instance.stop()


@pytest.mark.skip()
def test_browser_thinking() -> None:
    _check_api_key()
    client = Scrapybara()

    browser_instance = client.start_browser()
    print(browser_instance.get_stream_url().stream_url)
    assert browser_instance.id is not None
    screenshot_response = browser_instance.screenshot()
    assert screenshot_response.base_64_image is not None
    cdp_url = browser_instance.get_cdp_url()
    assert cdp_url is not None
    response = client.act(
        model=Anthropic(name="claude-3-7-sonnet-20250219-thinking"),
        system=BROWSER_SYSTEM_PROMPT_ANTHROPIC,
        prompt="Go to the YC website and get the number of funded startups and combined valuation",
        tools=[
            ComputerTool(browser_instance),
        ],
        schema=YCStats,
        on_step=lambda step: print(step.text, step.tool_calls, step.reasoning_parts),
    )
    print(response.output)
    assert response.output is not None
    assert response.output.number_of_startups is not None
    assert response.output.combined_valuation is not None
    browser_instance.stop()


if __name__ == "__main__":
    test_ubuntu()
    test_browser()
    test_ubuntu_openai()
    test_browser_openai()
    # test_ubuntu_thinking()
    # test_browser_thinking()
    # test_windows()
