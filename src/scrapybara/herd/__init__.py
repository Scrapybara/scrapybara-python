from ..types.act import Model
from typing import Literal
from pydantic import Field


class Herd(Model):
    """Model adapter for Herd (Scrapybara-hosted LLMs).

    Args:
        name: Herd model name

    Returns:
        A Model configuration object
    """

    provider: Literal["herd"] = Field(default="herd", frozen=True)

    def __init__(self, name: str) -> None:
        super().__init__(provider="herd", name=name)
