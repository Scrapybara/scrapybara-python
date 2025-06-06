# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class ScrollAction(UniversalBaseModel):
    coordinates: typing.Optional[typing.List[int]] = None
    delta_x: typing.Optional[float] = None
    delta_y: typing.Optional[float] = None
    hold_keys: typing.Optional[typing.List[str]] = None
    screenshot: typing.Optional[bool] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
