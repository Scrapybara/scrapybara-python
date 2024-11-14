import pytest
import pytest_asyncio
from unittest.mock import Mock, patch

from scrapybara import Scrapybara, ScrapybaraConfig
from scrapybara.anthropic import ComputerTool, EditTool, BashTool
from scrapybara.anthropic.base import CLIResult, ToolError

# Mark all test functions in this module as async
pytestmark = pytest.mark.asyncio


# Use pytest_asyncio fixtures
@pytest_asyncio.fixture
async def mock_scrapybara():
    return Mock(spec=Scrapybara)


@pytest_asyncio.fixture
async def instance_id():
    return "instance_id"


@pytest_asyncio.fixture
async def computer_tool(mock_scrapybara, instance_id):
    return ComputerTool(mock_scrapybara, instance_id)


@pytest_asyncio.fixture
async def edit_tool(mock_scrapybara, instance_id):
    return EditTool(mock_scrapybara, instance_id)


@pytest_asyncio.fixture
async def bash_tool(mock_scrapybara, instance_id):
    return BashTool(mock_scrapybara, instance_id)


class TestComputerTool:
    async def test_computer_action_success(self, computer_tool, mock_scrapybara):
        # Setup
        mock_scrapybara.computer.return_value = {"status": "success"}

        # Execute
        result = await computer_tool(
            instance_id="instance_id",
            action="mouse_move",
            coordinate=[100, 200],
            text=None,
        )

        # Verify
        assert isinstance(result, CLIResult)
        assert result.output == "{'status': 'success'}"
        mock_scrapybara.computer.assert_called_once_with(
            instance_id="instance_id",
            action="mouse_move",
            coordinate=(100, 200),
            text=None,
        )

    async def test_computer_action_failure(self, computer_tool, mock_scrapybara):
        # Setup
        mock_scrapybara.computer.side_effect = Exception("Computer action failed")

        # Execute and verify
        with pytest.raises(ToolError) as exc_info:
            await computer_tool(instance_id="instance_id", action="key", text="hello")

        assert str(exc_info.value) == "Computer action failed"
        mock_scrapybara.computer.assert_called_once_with(
            instance_id="instance_id", action="key", coordinate=None, text="hello"
        )


class TestEditTool:
    async def test_edit_create_success(self, edit_tool, mock_scrapybara):
        # Setup
        mock_scrapybara.edit.return_value = {"status": "created"}

        # Execute
        result = await edit_tool(
            instance_id="instance_id",
            command="create",
            path="/path/to/file.txt",
            file_text="Hello, World!",
        )

        # Verify
        assert isinstance(result, CLIResult)
        assert result.output == "{'status': 'created'}"
        mock_scrapybara.edit.assert_called_once_with(
            instance_id="instance_id",
            command="create",
            path="/path/to/file.txt",
            content="Hello, World!",
            view_range=None,
            old_text=None,
            new_text=None,
            line_number=None,
        )

    async def test_edit_failure(self, edit_tool, mock_scrapybara):
        # Setup
        mock_scrapybara.edit.side_effect = Exception("Edit failed")

        # Execute and verify
        with pytest.raises(ToolError) as exc_info:
            await edit_tool(
                instance_id="instance_id", command="view", path="/path/to/file.txt"
            )

        assert str(exc_info.value) == "Edit failed"
        mock_scrapybara.edit.assert_called_once_with(
            instance_id="instance_id",
            command="view",
            path="/path/to/file.txt",
            content=None,
            view_range=None,
            old_text=None,
            new_text=None,
            line_number=None,
        )


class TestBashTool:
    async def test_bash_command_success(self, bash_tool, mock_scrapybara):
        # Setup
        mock_scrapybara.bash.return_value = {"output": "command output"}

        # Execute
        result = await bash_tool(instance_id="instance_id", command="ls -l")

        # Verify
        assert isinstance(result, CLIResult)
        assert result.output == "{'output': 'command output'}"
        mock_scrapybara.bash.assert_called_once_with(
            instance_id="instance_id", command="ls -l", restart=False
        )

    async def test_bash_restart_success(self, bash_tool, mock_scrapybara):
        # Setup
        mock_scrapybara.bash.return_value = {"status": "restarted"}

        # Execute
        result = await bash_tool(instance_id="instance_id", command=None, restart=True)

        # Verify
        assert isinstance(result, CLIResult)
        assert result.output == "{'status': 'restarted'}"
        mock_scrapybara.bash.assert_called_once_with(
            instance_id="instance_id", command=None, restart=True
        )

    async def test_bash_failure(self, bash_tool, mock_scrapybara):
        # Setup
        mock_scrapybara.bash.side_effect = Exception("Bash command failed")

        # Execute and verify
        with pytest.raises(ToolError) as exc_info:
            await bash_tool(instance_id="instance_id", command="invalid-command")

        assert str(exc_info.value) == "Bash command failed"
        mock_scrapybara.bash.assert_called_once_with(
            instance_id="instance_id", command="invalid-command", restart=False
        )
