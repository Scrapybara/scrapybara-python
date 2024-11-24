# Scrapybara Python Client

Official Python client for Scrapybara ₍ᐢ•(ܫ)•ᐢ₎

## Installation

```bash
pip install scrapybara
```

## Usage

```python
from scrapybara import Scrapybara

# Initialize the client
client = Scrapybara(api_key="your-api-key")

# Start a new instance and get its ID
instance = client.start()

# Interact with the instance
instance.computer.mouse_move(100, 200)
instance.screenshot()

# Stop the instance
instance.stop()
```

### With Anthropic Computer Use

```python
from scrapybara.anthropic import ComputerTool, EditTool, BashTool

# From https://github.com/anthropics/anthropic-quickstarts/blob/main/computer-use-demo

tool_collection = ToolCollection(
    ComputerTool(instance),
    EditTool(instance),
    BashTool(instance),
)

raw_response = client.beta.messages.with_raw_response.create(
    max_tokens=max_tokens,
    messages=messages,
    model=model,
    system=[system],
    tools=tool_collection.to_params(),
    betas=betas,
)
```

## Requirements

- Python >= 3.8
- `requests` >= 2.25.1
- `anthropic` ^0.39.0
- `pydantic` ^2.0.0

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to submit an issue.
