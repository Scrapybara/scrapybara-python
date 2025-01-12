# This file was auto-generated by Fern from our API Definition.

import typing
from .environment import ScrapybaraEnvironment
import os
import httpx
from .core.api_error import ApiError
from .core.client_wrapper import SyncClientWrapper
from .instance.client import InstanceClient
from .browser.client import BrowserClient
from .code.client import CodeClient
from .notebook.client import NotebookClient
from .file.client import FileClient
from .env.client import EnvClient
from .types.deployment_config_instance_type import DeploymentConfigInstanceType
from .core.request_options import RequestOptions
from .types.get_instance_response import GetInstanceResponse
from .core.pydantic_utilities import parse_obj_as
from .errors.unprocessable_entity_error import UnprocessableEntityError
from .types.http_validation_error import HttpValidationError
from json.decoder import JSONDecodeError
from .core.jsonable_encoder import jsonable_encoder
from .types.auth_state_response import AuthStateResponse
from .core.client_wrapper import AsyncClientWrapper
from .instance.client import AsyncInstanceClient
from .browser.client import AsyncBrowserClient
from .code.client import AsyncCodeClient
from .notebook.client import AsyncNotebookClient
from .file.client import AsyncFileClient
from .env.client import AsyncEnvClient

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class BaseClient:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : ScrapybaraEnvironment
        The environment to use for requests from the client. from .environment import ScrapybaraEnvironment



        Defaults to ScrapybaraEnvironment.PRODUCTION



    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 600 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from scrapybara import Scrapybara

    client = Scrapybara(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: ScrapybaraEnvironment = ScrapybaraEnvironment.PRODUCTION,
        api_key: typing.Optional[str] = os.getenv("SCRAPYBARA_API_KEY"),
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 600 if httpx_client is None else None
        if api_key is None:
            raise ApiError(
                body="The client must be instantiated be either passing in api_key or setting SCRAPYBARA_API_KEY"
            )
        self._client_wrapper = SyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.Client(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.Client(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.instance = InstanceClient(client_wrapper=self._client_wrapper)
        self.browser = BrowserClient(client_wrapper=self._client_wrapper)
        self.code = CodeClient(client_wrapper=self._client_wrapper)
        self.notebook = NotebookClient(client_wrapper=self._client_wrapper)
        self.file = FileClient(client_wrapper=self._client_wrapper)
        self.env = EnvClient(client_wrapper=self._client_wrapper)

    def start(
        self,
        *,
        instance_type: typing.Optional[DeploymentConfigInstanceType] = OMIT,
        timeout_hours: typing.Optional[float] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> GetInstanceResponse:
        """
        Parameters
        ----------
        instance_type : typing.Optional[DeploymentConfigInstanceType]

        timeout_hours : typing.Optional[float]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GetInstanceResponse
            Successful Response

        Examples
        --------
        from scrapybara import Scrapybara

        client = Scrapybara(
            api_key="YOUR_API_KEY",
        )
        client.start()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/start",
            method="POST",
            json={
                "instance_type": instance_type,
                "timeout_hours": timeout_hours,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    GetInstanceResponse,
                    parse_obj_as(
                        type_=GetInstanceResponse,  # type: ignore
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

    def get(self, instance_id: str, *, request_options: typing.Optional[RequestOptions] = None) -> GetInstanceResponse:
        """
        Parameters
        ----------
        instance_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GetInstanceResponse
            Successful Response

        Examples
        --------
        from scrapybara import Scrapybara

        client = Scrapybara(
            api_key="YOUR_API_KEY",
        )
        client.get(
            instance_id="instance_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/instance/{jsonable_encoder(instance_id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    GetInstanceResponse,
                    parse_obj_as(
                        type_=GetInstanceResponse,  # type: ignore
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

    def get_instances(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[GetInstanceResponse]:
        """
        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[GetInstanceResponse]
            Successful Response

        Examples
        --------
        from scrapybara import Scrapybara

        client = Scrapybara(
            api_key="YOUR_API_KEY",
        )
        client.get_instances()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/instances",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.List[GetInstanceResponse],
                    parse_obj_as(
                        type_=typing.List[GetInstanceResponse],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_auth_states(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[AuthStateResponse]:
        """
        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[AuthStateResponse]
            Successful Response

        Examples
        --------
        from scrapybara import Scrapybara

        client = Scrapybara(
            api_key="YOUR_API_KEY",
        )
        client.get_auth_states()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/auth_states",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.List[AuthStateResponse],
                    parse_obj_as(
                        type_=typing.List[AuthStateResponse],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncBaseClient:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : ScrapybaraEnvironment
        The environment to use for requests from the client. from .environment import ScrapybaraEnvironment



        Defaults to ScrapybaraEnvironment.PRODUCTION



    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 600 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from scrapybara import AsyncScrapybara

    client = AsyncScrapybara(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: ScrapybaraEnvironment = ScrapybaraEnvironment.PRODUCTION,
        api_key: typing.Optional[str] = os.getenv("SCRAPYBARA_API_KEY"),
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 600 if httpx_client is None else None
        if api_key is None:
            raise ApiError(
                body="The client must be instantiated be either passing in api_key or setting SCRAPYBARA_API_KEY"
            )
        self._client_wrapper = AsyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.instance = AsyncInstanceClient(client_wrapper=self._client_wrapper)
        self.browser = AsyncBrowserClient(client_wrapper=self._client_wrapper)
        self.code = AsyncCodeClient(client_wrapper=self._client_wrapper)
        self.notebook = AsyncNotebookClient(client_wrapper=self._client_wrapper)
        self.file = AsyncFileClient(client_wrapper=self._client_wrapper)
        self.env = AsyncEnvClient(client_wrapper=self._client_wrapper)

    async def start(
        self,
        *,
        instance_type: typing.Optional[DeploymentConfigInstanceType] = OMIT,
        timeout_hours: typing.Optional[float] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> GetInstanceResponse:
        """
        Parameters
        ----------
        instance_type : typing.Optional[DeploymentConfigInstanceType]

        timeout_hours : typing.Optional[float]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GetInstanceResponse
            Successful Response

        Examples
        --------
        import asyncio

        from scrapybara import AsyncScrapybara

        client = AsyncScrapybara(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.start()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/start",
            method="POST",
            json={
                "instance_type": instance_type,
                "timeout_hours": timeout_hours,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    GetInstanceResponse,
                    parse_obj_as(
                        type_=GetInstanceResponse,  # type: ignore
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

    async def get(
        self, instance_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> GetInstanceResponse:
        """
        Parameters
        ----------
        instance_id : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GetInstanceResponse
            Successful Response

        Examples
        --------
        import asyncio

        from scrapybara import AsyncScrapybara

        client = AsyncScrapybara(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.get(
                instance_id="instance_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/instance/{jsonable_encoder(instance_id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    GetInstanceResponse,
                    parse_obj_as(
                        type_=GetInstanceResponse,  # type: ignore
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

    async def get_instances(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[GetInstanceResponse]:
        """
        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[GetInstanceResponse]
            Successful Response

        Examples
        --------
        import asyncio

        from scrapybara import AsyncScrapybara

        client = AsyncScrapybara(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.get_instances()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/instances",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.List[GetInstanceResponse],
                    parse_obj_as(
                        type_=typing.List[GetInstanceResponse],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_auth_states(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[AuthStateResponse]:
        """
        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[AuthStateResponse]
            Successful Response

        Examples
        --------
        import asyncio

        from scrapybara import AsyncScrapybara

        client = AsyncScrapybara(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.get_auth_states()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/auth_states",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    typing.List[AuthStateResponse],
                    parse_obj_as(
                        type_=typing.List[AuthStateResponse],  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


def _get_base_url(*, base_url: typing.Optional[str] = None, environment: ScrapybaraEnvironment) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Please pass in either base_url or environment to construct the client")
