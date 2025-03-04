# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ...core.pydantic_utilities import UniversalBaseModel
import typing
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
from ...types.button import Button
from ...types.click_mouse_action_click_type import ClickMouseActionClickType


class Request_MoveMouse(UniversalBaseModel):
    action: typing.Literal["move_mouse"] = "move_mouse"
    coordinates: typing.List[int]
    hold_keys: typing.Optional[typing.List[str]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class Request_ClickMouse(UniversalBaseModel):
    action: typing.Literal["click_mouse"] = "click_mouse"
    button: Button
    click_type: typing.Optional[ClickMouseActionClickType] = None
    coordinates: typing.Optional[typing.List[int]] = None
    num_clicks: typing.Optional[int] = None
    hold_keys: typing.Optional[typing.List[str]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class Request_DragMouse(UniversalBaseModel):
    action: typing.Literal["drag_mouse"] = "drag_mouse"
    path: typing.List[typing.List[int]]
    hold_keys: typing.Optional[typing.List[str]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class Request_Scroll(UniversalBaseModel):
    action: typing.Literal["scroll"] = "scroll"
    coordinates: typing.List[int]
    delta_x: typing.Optional[float] = None
    delta_y: typing.Optional[float] = None
    hold_keys: typing.Optional[typing.List[str]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class Request_PressKey(UniversalBaseModel):
    action: typing.Literal["press_key"] = "press_key"
    keys: typing.List[str]
    duration: typing.Optional[float] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class Request_TypeText(UniversalBaseModel):
    action: typing.Literal["type_text"] = "type_text"
    text: str
    hold_keys: typing.Optional[typing.List[str]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class Request_Wait(UniversalBaseModel):
    action: typing.Literal["wait"] = "wait"
    duration: float

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class Request_TakeScreenshot(UniversalBaseModel):
    action: typing.Literal["take_screenshot"] = "take_screenshot"

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


class Request_GetCursorPosition(UniversalBaseModel):
    action: typing.Literal["get_cursor_position"] = "get_cursor_position"

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


Request = typing.Union[
    Request_MoveMouse,
    Request_ClickMouse,
    Request_DragMouse,
    Request_Scroll,
    Request_PressKey,
    Request_TypeText,
    Request_Wait,
    Request_TakeScreenshot,
    Request_GetCursorPosition,
]
