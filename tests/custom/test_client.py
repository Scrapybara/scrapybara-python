from pydantic import BaseModel
from scrapybara import Scrapybara
import os
import pytest
import tempfile
import uuid

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


def test_upload_download() -> None:
    _check_api_key()
    client = Scrapybara()

    # Start Ubuntu instance
    ubuntu_instance = client.start_ubuntu()
    assert ubuntu_instance.id is not None
    
    try:
        # Create a temporary file with test content
        test_content = f"Test content {uuid.uuid4()}"
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_path = temp_file.name
        
        # Upload the file to the instance
        remote_path = f"test_file_{uuid.uuid4()}"
        with open(temp_path, 'rb') as f:
            upload_response = ubuntu_instance.upload(file=f, path=remote_path)
        assert upload_response is not None
        
        # Verify file exists on remote and content matches
        file_check = ubuntu_instance.bash(command=f"cat {remote_path}")
        assert file_check is not None
        assert test_content in str(file_check)
        
        # Call the download method to at least test the API call
        # Note: In a real application you would need to handle the response
        # and save the content to a local file
        # ubuntu_instance.download(path=remote_path)
        
        # Clean up local files
        os.unlink(temp_path)
            
    finally:
        # Always stop the instance
        ubuntu_instance.stop()


def test_beta_vm_management() -> None:
    _check_api_key()
    client = Scrapybara()

    # Start a rodent instance
    instance = client.start_ubuntu(backend="rodent")
    assert instance.id is not None
    
    try:
        # Take a snapshot
        snapshot_response = client.beta.take_snapshot(instance_id=instance.id)
        assert snapshot_response is not None
        assert snapshot_response.snapshot_id is not None
        snapshot_id = snapshot_response.snapshot_id
        print(f"Created snapshot with ID: {snapshot_id}")
        
        # Warmup the snapshot
        warmup_response = client.beta.warmup_snapshot(snapshot_id=snapshot_id)
        assert warmup_response is not None
        assert warmup_response.success is True
        
        # Delete the snapshot
        delete_response = client.beta.delete_snapshot(snapshot_id=snapshot_id)
        assert delete_response is not None
        assert delete_response.success is True
        
    finally:
        instance.stop()


def test_restore_from_snapshot() -> None:
    _check_api_key()
    client = Scrapybara()

    # Start original instance
    original_instance = client.start_ubuntu(backend="rodent")
    assert original_instance.id is not None
    print(f"Started original instance: {original_instance.id}")
    
    snapshot_id = None
    restored_instance = None
    
    try:
        # Create a file to verify restoration later
        test_marker = f"test-marker-{uuid.uuid4()}"
        original_instance.bash(command=f"echo '{test_marker}' > /tmp/snapshot-test-file")
        
        # Take a snapshot
        snapshot_response = client.beta.take_snapshot(instance_id=original_instance.id)
        assert snapshot_response is not None
        assert snapshot_response.snapshot_id is not None
        
        snapshot_id = snapshot_response.snapshot_id
        print(f"Created snapshot with ID: {snapshot_id}")
        
        # Warmup the snapshot (optional but recommended)
        client.beta.warmup_snapshot(snapshot_id=snapshot_id)
        
        # Stop the original instance
        original_instance.stop()
        
        # Start a new instance from the snapshot
        restored_instance = client.start_ubuntu(snapshot_id=snapshot_id, backend="rodent")
        assert restored_instance.id is not None
        print(f"Started restored instance: {restored_instance.id}")
        
        # Verify the test file exists with our marker
        file_content = restored_instance.bash(command="cat /tmp/snapshot-test-file")
        assert test_marker in str(file_content)
        print("Successfully verified snapshot restoration!")
        
    finally:
        # Clean up resources
        if original_instance:
            try:
                original_instance.stop()
            except:
                pass
                
        if restored_instance:
            try:
                restored_instance.stop()
            except:
                pass
                
        if snapshot_id:
            try:
                client.beta.delete_snapshot(snapshot_id=snapshot_id)
            except:
                pass


if __name__ == "__main__":
    test_ubuntu()
    test_browser()
    test_ubuntu_openai()
    test_browser_openai()
    test_upload_download()
    test_beta_vm_management()
    test_restore_from_snapshot()
    # test_ubuntu_thinking()
    # test_browser_thinking()
    # test_windows()
