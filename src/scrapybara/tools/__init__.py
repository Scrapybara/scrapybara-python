import base64
import json
from typing import Any, Literal, Optional, Sequence, Tuple, Union
from pydantic import BaseModel, Field
from playwright.sync_api import sync_playwright

from ..types.tool import Tool
from ..client import BaseInstance, UbuntuInstance, BrowserInstance
from ..instance.types import Action, Command


def image_result(base64: str) -> str:
    """Return an image result that is interpretable by the model."""
    return json.dumps(
        {
            "output": "",
            "error": "",
            "base64_image": base64,
            "system": None,
        }
    )


class ComputerToolParameters(BaseModel):
    """Parameters for computer interaction commands."""

    action: Action = Field(description="The computer action to execute")
    coordinate: Optional[Sequence[int]] = Field(
        None, description="Coordinates for mouse actions"
    )
    text: Optional[str] = Field(None, description="Text for keyboard actions")


class ComputerTool(Tool):
    """A computer interaction tool that allows the agent to control mouse and keyboard.

    Available for Ubuntu, Browser, and Windows instances."""

    _instance: BaseInstance

    def __init__(self, instance: BaseInstance) -> None:
        super().__init__(
            name="computer",
            description="Control mouse and keyboard for computer interaction",
            parameters=ComputerToolParameters,
        )
        self._instance = instance

    def __call__(self, **kwargs: Any) -> Any:
        params = ComputerToolParameters.model_validate(kwargs)
        return self._instance.computer(
            action=params.action,
            coordinate=tuple(params.coordinate) if params.coordinate else None,
            text=params.text,
        )


class EditToolParameters(BaseModel):
    """Parameters for file editing commands."""

    command: Command = Field(description="The edit command to execute")
    path: str = Field(description="Path to the file to edit")
    file_text: Optional[str] = Field(
        None, description="File content for create command"
    )
    view_range: Optional[Tuple[int, int]] = Field(
        None, description="Line range for view command"
    )
    old_str: Optional[str] = Field(
        None, description="String to replace for replace command"
    )
    new_str: Optional[str] = Field(None, description="New string for replace command")
    insert_line: Optional[int] = Field(
        None, description="Line number for insert command"
    )


class EditTool(Tool):
    """A filesystem editor tool that allows the agent to view, create, and edit files.

    Available for Ubuntu instances."""

    _instance: UbuntuInstance

    def __init__(self, instance: UbuntuInstance) -> None:
        super().__init__(
            name="str_replace_editor",
            description="View, create, and edit files in the filesystem",
            parameters=EditToolParameters,
        )
        self._instance = instance

    def __call__(self, **kwargs: Any) -> Any:
        params = EditToolParameters.model_validate(kwargs)
        return self._instance.edit(
            command=params.command,
            path=params.path,
            file_text=params.file_text,
            view_range=params.view_range,
            old_str=params.old_str,
            new_str=params.new_str,
            insert_line=params.insert_line,
        )


class BashToolParameters(BaseModel):
    """Parameters for bash command execution."""

    command: str = Field(description="The bash command to execute")
    restart: Optional[bool] = Field(False, description="Whether to restart the shell")


class BashTool(Tool):
    """A shell execution tool that allows the agent to run bash commands.

    Available for Ubuntu instances."""

    _instance: UbuntuInstance

    def __init__(self, instance: UbuntuInstance) -> None:
        super().__init__(
            name="bash",
            description="Execute bash commands in the shell",
            parameters=BashToolParameters,
        )
        self._instance = instance

    def __call__(self, **kwargs: Any) -> Any:
        params = BashToolParameters.model_validate(kwargs)
        return self._instance.bash(command=params.command, restart=params.restart)


class BrowserToolParameters(BaseModel):
    """Parameters for browser interaction commands."""

    command: Literal[
        "go_to",  # Navigate to a URL
        "get_html",  # Get current page HTML
        "evaluate",  # Run JavaScript code
        "click",  # Click on an element
        "type",  # Type into an element
        "screenshot",  # Take a screenshot
        "get_text",  # Get text content of element
        "get_attribute",  # Get attribute of element
    ] = Field(
        description="The browser command to execute. Required parameters per command:\n"
        "- go_to: requires 'url'\n"
        "- evaluate: requires 'code'\n"
        "- click: requires 'selector'\n"
        "- type: requires 'selector' and 'text'\n"
        "- get_text: requires 'selector'\n"
        "- get_attribute: requires 'selector' and 'attribute'\n"
        "- get_html: no additional parameters\n"
        "- screenshot: no additional parameters"
    )
    url: Optional[str] = Field(
        None, description="URL for go_to command (required for go_to)"
    )
    selector: Optional[str] = Field(
        None,
        description="CSS selector for element operations (required for click, type, get_text, get_attribute)",
    )
    code: Optional[str] = Field(
        None, description="JavaScript code for evaluate command (required for evaluate)"
    )
    text: Optional[str] = Field(
        None, description="Text to type for type command (required for type)"
    )
    timeout: Optional[int] = Field(
        30000, description="Timeout in milliseconds for operations"
    )
    attribute: Optional[str] = Field(
        None,
        description="Attribute name for get_attribute command (required for get_attribute)",
    )


class BrowserTool(Tool):
    """A browser interaction tool that allows the agent to interact with a browser.

    Available for Ubuntu and Browser instances."""

    _instance: Union[UbuntuInstance, BrowserInstance]

    def __init__(self, instance: Union[UbuntuInstance, BrowserInstance]) -> None:
        super().__init__(
            name="browser",
            description="Interact with a browser for web scraping and automation",
            parameters=BrowserToolParameters,
        )
        self._instance = instance

    def __call__(self, **kwargs: Any) -> Any:
        params = BrowserToolParameters.model_validate(kwargs)
        command = params.command
        url = params.url
        selector = params.selector
        code = params.code
        text = params.text
        timeout = params.timeout or 30000
        attribute = params.attribute

        # Get CDP URL based on instance type
        if isinstance(self._instance, UbuntuInstance):
            cdp_url = self._instance.browser.get_cdp_url().cdp_url
        else:
            cdp_url = self._instance.get_cdp_url().cdp_url

        if cdp_url is None:
            raise ValueError("CDP URL is not available, start the browser first")

        with sync_playwright() as playwright:
            browser = playwright.chromium.connect_over_cdp(cdp_url)
            context = browser.contexts[0]
            if not context.pages:
                page = context.new_page()
            else:
                page = context.pages[0]

            try:
                if command == "go_to":
                    if not url:
                        raise ValueError("URL is required for go_to command")
                    page.goto(url, timeout=timeout)
                    return True

                elif command == "get_html":
                    try:
                        return page.evaluate("() => document.documentElement.outerHTML")
                    except Exception:
                        # If page is navigating, just return what we can get
                        return page.evaluate("() => document.documentElement.innerHTML")

                elif command == "evaluate":
                    if not code:
                        raise ValueError("Code is required for evaluate command")
                    return page.evaluate(code)

                elif command == "click":
                    if not selector:
                        raise ValueError("Selector is required for click command")
                    page.click(selector, timeout=timeout)
                    return True

                elif command == "type":
                    if not selector:
                        raise ValueError("Selector is required for type command")
                    if not text:
                        raise ValueError("Text is required for type command")
                    page.type(selector, text, timeout=timeout)
                    return True

                elif command == "screenshot":
                    return image_result(
                        base64.b64encode(page.screenshot(type="png")).decode("utf-8")
                    )

                elif command == "get_text":
                    if not selector:
                        raise ValueError("Selector is required for get_text command")
                    element = page.wait_for_selector(selector, timeout=timeout)
                    if element is None:
                        raise ValueError(f"Element not found: {selector}")
                    return element.text_content()

                elif command == "get_attribute":
                    if not selector:
                        raise ValueError(
                            "Selector is required for get_attribute command"
                        )
                    if not attribute:
                        raise ValueError(
                            "Attribute is required for get_attribute command"
                        )
                    element = page.wait_for_selector(selector, timeout=timeout)
                    if element is None:
                        raise ValueError(f"Element not found: {selector}")
                    return element.get_attribute(attribute)

                else:
                    raise ValueError(f"Unknown command: {command}")

            except Exception as e:
                raise ValueError(f"Browser command failed: {str(e)}")

            finally:
                browser.close()
