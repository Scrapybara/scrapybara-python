# This file was auto-generated by Fern from our API Definition.

from ..core.client_wrapper import SyncClientWrapper
import typing
from ..core.request_options import RequestOptions
from ..types.start_browser_response import StartBrowserResponse
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import parse_obj_as
from ..errors.unprocessable_entity_error import UnprocessableEntityError
from ..types.http_validation_error import HttpValidationError
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..types.browser_get_cdp_url_response import BrowserGetCdpUrlResponse
from ..types.browser_authenticate_response import BrowserAuthenticateResponse
from ..types.stop_browser_response import StopBrowserResponse
from ..core.client_wrapper import AsyncClientWrapper


class BrowserClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def start(
        self, instance_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> StartBrowserResponse:
        """
        Parameters
        ----------
        instance_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        StartBrowserResponse
            Successful Response

        Examples
        --------
        from scrapybara import Scrapybara

        client = Scrapybara(
            api_key="YOUR_API_KEY",
        )
        client.browser.start(
            instance_id="instance_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/instance/{jsonable_encoder(instance_id)}/browser/start",
            method="POST",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    StartBrowserResponse,
                    parse_obj_as(
                        type_=StartBrowserResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_cdp_url(
        self, instance_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> BrowserGetCdpUrlResponse:
        """
        Parameters
        ----------
        instance_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BrowserGetCdpUrlResponse
            Successful Response

        Examples
        --------
        from scrapybara import Scrapybara

        client = Scrapybara(
            api_key="YOUR_API_KEY",
        )
        client.browser.get_cdp_url(
            instance_id="instance_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/instance/{jsonable_encoder(instance_id)}/browser/cdp_url",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    BrowserGetCdpUrlResponse,
                    parse_obj_as(
                        type_=BrowserGetCdpUrlResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def authenticate(
        self, instance_id: str, *, context_id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> BrowserAuthenticateResponse:
        """
        Authenticate browser with Anon for all available apps

        Parameters
        ----------
        instance_id : str

        context_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BrowserAuthenticateResponse
            Successful Response

        Examples
        --------
        from scrapybara import Scrapybara

        client = Scrapybara(
            api_key="YOUR_API_KEY",
        )
        client.browser.authenticate(
            instance_id="instance_id",
            context_id="context_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/instance/{jsonable_encoder(instance_id)}/browser/authenticate",
            method="POST",
            params={
                "context_id": context_id,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    BrowserAuthenticateResponse,
                    parse_obj_as(
                        type_=BrowserAuthenticateResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def stop(self, instance_id: str, *, request_options: typing.Optional[RequestOptions] = None) -> StopBrowserResponse:
        """
        Parameters
        ----------
        instance_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        StopBrowserResponse
            Successful Response

        Examples
        --------
        from scrapybara import Scrapybara

        client = Scrapybara(
            api_key="YOUR_API_KEY",
        )
        client.browser.stop(
            instance_id="instance_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/instance/{jsonable_encoder(instance_id)}/browser/stop",
            method="POST",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    StopBrowserResponse,
                    parse_obj_as(
                        type_=StopBrowserResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncBrowserClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def start(
        self, instance_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> StartBrowserResponse:
        """
        Parameters
        ----------
        instance_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        StartBrowserResponse
            Successful Response

        Examples
        --------
        import asyncio

        from scrapybara import AsyncScrapybara

        client = AsyncScrapybara(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.browser.start(
                instance_id="instance_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/instance/{jsonable_encoder(instance_id)}/browser/start",
            method="POST",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    StartBrowserResponse,
                    parse_obj_as(
                        type_=StartBrowserResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_cdp_url(
        self, instance_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> BrowserGetCdpUrlResponse:
        """
        Parameters
        ----------
        instance_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BrowserGetCdpUrlResponse
            Successful Response

        Examples
        --------
        import asyncio

        from scrapybara import AsyncScrapybara

        client = AsyncScrapybara(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.browser.get_cdp_url(
                instance_id="instance_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/instance/{jsonable_encoder(instance_id)}/browser/cdp_url",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    BrowserGetCdpUrlResponse,
                    parse_obj_as(
                        type_=BrowserGetCdpUrlResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def authenticate(
        self, instance_id: str, *, context_id: str, request_options: typing.Optional[RequestOptions] = None
    ) -> BrowserAuthenticateResponse:
        """
        Authenticate browser with Anon for all available apps

        Parameters
        ----------
        instance_id : str

        context_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BrowserAuthenticateResponse
            Successful Response

        Examples
        --------
        import asyncio

        from scrapybara import AsyncScrapybara

        client = AsyncScrapybara(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.browser.authenticate(
                instance_id="instance_id",
                context_id="context_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/instance/{jsonable_encoder(instance_id)}/browser/authenticate",
            method="POST",
            params={
                "context_id": context_id,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    BrowserAuthenticateResponse,
                    parse_obj_as(
                        type_=BrowserAuthenticateResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def stop(
        self, instance_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> StopBrowserResponse:
        """
        Parameters
        ----------
        instance_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        StopBrowserResponse
            Successful Response

        Examples
        --------
        import asyncio

        from scrapybara import AsyncScrapybara

        client = AsyncScrapybara(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.browser.stop(
                instance_id="instance_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/instance/{jsonable_encoder(instance_id)}/browser/stop",
            method="POST",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    StopBrowserResponse,
                    parse_obj_as(
                        type_=StopBrowserResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(
                        HttpValidationError,
                        parse_obj_as(
                            type_=HttpValidationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)