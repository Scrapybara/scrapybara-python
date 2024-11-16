from typing import Optional, List
from pydantic import BaseModel, model_validator

from .types import Command
from .exceptions import ScrapybaraError


class EditCommand(BaseModel):
    """
    File editing command request model

    Attributes:
        command: Type of edit operation to perform
        path: Path to the target file
        file_text: Content for create command
        view_range: [start_line, end_line] for view command
        old_str: Text to replace for str_replace command
        new_str: New text for str_replace or insert commands
        insert_line: Line number for insert command
    """

    command: Command
    path: str
    file_text: Optional[str] = None
    view_range: Optional[List[int]] = None
    old_str: Optional[str] = None
    new_str: Optional[str] = None
    insert_line: Optional[int] = None

    @model_validator(mode="after")
    def validate_command_params(self) -> "EditCommand":
        """Validate the edit command parameters"""
        if self.command == "view":
            if self.view_range is not None:
                if not isinstance(self.view_range, list) or len(self.view_range) != 2:
                    raise ScrapybaraError("view_range must be a list of length 2")
                if not all(isinstance(i, int) and i >= 0 for i in self.view_range):
                    raise ScrapybaraError(
                        "view_range must be a list of non-negative integers"
                    )

        elif self.command == "create":
            if self.file_text is None:
                raise ScrapybaraError("file_text is required for create command")

        elif self.command == "str_replace":
            if self.old_str is None or self.new_str is None:
                raise ScrapybaraError(
                    "old_str and new_str are required for str_replace command"
                )

        elif self.command == "insert":
            if self.insert_line is None or self.new_str is None:
                raise ScrapybaraError(
                    "insert_line and new_str are required for insert command"
                )
            if not isinstance(self.insert_line, int) or self.insert_line < 0:
                raise ScrapybaraError("insert_line must be a non-negative integer")

        return self
