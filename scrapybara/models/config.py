from pydantic import BaseModel, Field


class ScrapybaraConfig(BaseModel):
    """
    Configuration for Scrapybara instance

    Args:
        base_url: Base URL for the Scrapybara service (default: http://localhost:8000)
    """

    base_url: str = Field(
        default="https://starfish-app-e63cz.ondigitalocean.app",
        description="Base URL for the Scrapybara service",
    )

    def __init__(self, **data):
        super().__init__(**data)
        self.base_url = self.base_url.rstrip("/")
