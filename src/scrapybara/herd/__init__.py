from ..types.act import Model
from typing import Literal, Optional
from pydantic import Field


class Herd(Model):
    """Model adapter for Herd (Scrapybara-hosted LLMs).

    Supported models:
    - ui-tars-72b (0.5x agent credit)

    Args:
        name: Herd model name, defaults to "ui-tars-72b"

    Returns:
        A Model configuration object
    """

    provider: Literal["herd"] = Field(default="herd", frozen=True)

    def __init__(self, name: Optional[str] = "ui-tars-72b") -> None:
        super().__init__(provider="herd", name=name)
