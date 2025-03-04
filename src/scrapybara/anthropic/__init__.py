from typing import Literal, Optional

from pydantic import Field

from ..types.act import Model


class Anthropic(Model):
    """Model adapter for Anthropic.

    Supported models:
    - claude-3-7-sonnet-20250219 (1x agent credit if no api_key)
    - claude-3-7-sonnet-20250219-thinking (1x agent credit if no api_key)
    - claude-3-5-sonnet-20241022 (1x agent credit if no api_key)

    Args:
        name: Anthropic model name, defaults to "claude-3-7-sonnet-20250219"
        api_key: Optional Anthropic API key

    Returns:
        A Model configuration object
    """

    provider: Literal["anthropic"] = Field(default="anthropic", frozen=True)

    def __init__(
        self,
        name: Optional[str] = "claude-3-7-sonnet-20250219",
        api_key: Optional[str] = None,
    ) -> None:
        super().__init__(provider="anthropic", name=name, api_key=api_key)
