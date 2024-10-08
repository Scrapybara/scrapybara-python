# coding: utf-8

"""
    Scrapybara API

    Scrapybara API provides web automation, capybara-style. It allows users to generate, execute, and manage scripts.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class GetScriptResponse(BaseModel):
    """
    GetScriptResponse
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="Unique identifier of the script.")
    url: Optional[StrictStr] = Field(default=None, description="The target URL for the script.")
    command: Optional[StrictStr] = Field(default=None, description="The original action or instructions.")
    steps: Optional[Dict[str, Any]] = Field(default=None, description="Detailed steps for the action.")
    content: Optional[StrictStr] = Field(default=None, description="The actual code content of the script.")
    status: Optional[StrictStr] = Field(default=None, description="Current status of the script (e.g., 'pending', 'completed', 'error').")
    status_description: Optional[StrictStr] = Field(default=None, description="Additional details about the script's status.")
    __properties: ClassVar[List[str]] = ["id", "url", "command", "steps", "content", "status", "status_description"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of GetScriptResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GetScriptResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "url": obj.get("url"),
            "command": obj.get("command"),
            "steps": obj.get("steps"),
            "content": obj.get("content"),
            "status": obj.get("status"),
            "status_description": obj.get("status_description")
        })
        return _obj


