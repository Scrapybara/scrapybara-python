# Scrapybara Python Client

Official Python client for Scrapybara ₍ᐢ•(ܫ)•ᐢ₎

## Documentation

[Scrapybara API Documentation](https://docs.scrapybara.com/api-reference)

## Installation

```bash
pip install scrapybara
```

## Usage

```python
from scrapybara import ScrapybaraClient

client = ScrapybaraClient("your-api-key")

response = client.generate_script(
    {
        "url": "https://news.ycombinator.com",
        "command": "Scrape all posts"
    }
)
```
