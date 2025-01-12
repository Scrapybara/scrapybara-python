from typing import Any, Dict, Optional
from playwright.sync_api import sync_playwright
from pydantic import BaseModel

from ..client import Instance


class Tool(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

    def __call__(self, **kwargs: Any) -> Any:
        raise NotImplementedError("Tool.__call__ must be implemented by subclasses")


class ComputerTool(Tool):
    """A computer interaction tool that allows the agent to control mouse and keyboard."""

    _instance: Instance

    def __init__(self, instance: Instance) -> None:
        super().__init__(
            name="computer",
        )
        self._instance = instance

    def __call__(self, **kwargs: Any) -> Any:
        action = kwargs.pop("action")
        coordinate = kwargs.pop("coordinate", None)
        text = kwargs.pop("text", None)

        return self._instance.computer(
            action=action,
            coordinate=tuple(coordinate) if coordinate else None,
            text=text,
        )


class EditTool(Tool):
    """A filesystem editor tool that allows the agent to view, create, and edit files."""

    _instance: Instance

    def __init__(self, instance: Instance) -> None:
        super().__init__(
            name="str_replace_editor",
        )
        self._instance = instance

    def __call__(self, **kwargs: Any) -> Any:
        command = kwargs.pop("command")
        path = kwargs.pop("path")
        file_text = kwargs.pop("file_text", None)
        view_range = kwargs.pop("view_range", None)
        old_str = kwargs.pop("old_str", None)
        new_str = kwargs.pop("new_str", None)
        insert_line = kwargs.pop("insert_line", None)

        return self._instance.edit(
            command=command,
            path=path,
            file_text=file_text,
            view_range=view_range,
            old_str=old_str,
            new_str=new_str,
            insert_line=insert_line,
        )


class BashTool(Tool):
    """A shell execution tool that allows the agent to run bash commands."""

    _instance: Instance

    def __init__(self, instance: Instance) -> None:
        super().__init__(
            name="bash",
        )
        self._instance = instance

    def __call__(self, **kwargs: Any) -> Any:
        command = kwargs.pop("command")
        restart = kwargs.pop("restart", False)

        return self._instance.bash(command=command, restart=restart)


class BrowserTool(Tool):
    """A browser interaction tool that allows the agent to interact with a browser."""

    _instance: Instance

    def __init__(self, instance: Instance) -> None:
        super().__init__(
            name="browser",
            description="Interact with a browser for web scraping and automation",
            parameters={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "enum": [
                            "go_to",  # Navigate to a URL
                            "get_html",  # Get current page HTML
                            "evaluate",  # Run JavaScript code
                            "click",  # Click on an element
                            "type",  # Type into an element
                            "screenshot",  # Take a screenshot
                            "get_text",  # Get text content of element
                            "get_attribute",  # Get attribute of element
                        ],
                        "description": "The browser command to execute. Required parameters per command:\n- go_to: requires 'url'\n- evaluate: requires 'code'\n- click: requires 'selector'\n- type: requires 'selector' and 'text'\n- get_text: requires 'selector'\n- get_attribute: requires 'selector' and 'attribute'\n- get_html: no additional parameters\n- screenshot: no additional parameters",
                    },
                    "url": {
                        "type": "string",
                        "description": "URL for go_to command (required for go_to)",
                    },
                    "selector": {
                        "type": "string",
                        "description": "CSS selector for element operations (required for click, type, get_text, get_attribute)",
                    },
                    "code": {
                        "type": "string",
                        "description": "JavaScript code for evaluate command (required for evaluate)",
                    },
                    "text": {
                        "type": "string",
                        "description": "Text to type for type command (required for type)",
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Timeout in milliseconds for operations",
                        "default": 30000,
                    },
                    "attribute": {
                        "type": "string",
                        "description": "Attribute name for get_attribute command (required for get_attribute)",
                    },
                },
                "required": ["command"],
            },
        )
        self._instance = instance

    def __call__(self, **kwargs: Any) -> Any:
        command = kwargs.pop("command")
        url = kwargs.pop("url", None)
        selector = kwargs.pop("selector", None)
        code = kwargs.pop("code", None)
        text = kwargs.pop("text", None)
        timeout = kwargs.pop("timeout", 30000)
        attribute = kwargs.pop("attribute", None)

        cdp_url = self._instance.browser.get_cdp_url().cdp_url
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
                    page.goto(url, timeout=timeout)
                    return True

                elif command == "get_html":
                    try:
                        return page.evaluate("() => document.documentElement.outerHTML")
                    except Exception:
                        # If page is navigating, just return what we can get
                        return page.evaluate("() => document.documentElement.innerHTML")

                elif command == "evaluate":
                    return page.evaluate(code)

                elif command == "click":
                    page.click(selector, timeout=timeout)
                    return True

                elif command == "type":
                    page.type(selector, text, timeout=timeout)
                    return True

                elif command == "screenshot":
                    return page.screenshot(type="png")

                elif command == "get_text":
                    element = page.wait_for_selector(selector, timeout=timeout)
                    if element is None:
                        raise ValueError(f"Element not found: {selector}")
                    return element.text_content()

                elif command == "get_attribute":
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
