from datetime import datetime
from typing import Optional, Any, Dict, List, Sequence, Union, Literal
import typing
import httpx
import os

import typing
from pydantic import BaseModel, ValidationError
from scrapybara.agent.types.model import Model
from scrapybara.environment import ScrapybaraEnvironment
from .core.request_options import RequestOptions
from .types import (
    ActResponse,
    BrowserAuthenticateResponse,
    BrowserGetCdpUrlResponse,
    CellType,
    DeploymentConfigInstanceType,
    EnvGetResponse,
    EnvResponse,
    FileDownloadResponse,
    FileReadResponse,
    GetInstanceResponse,
    InstanceGetStreamUrlResponse,
    InstanceScreenshotResponse,
    KernelInfo,
    Notebook as NotebookType,
    NotebookCell,
    ScrapeResponse,
    StartBrowserResponse,
    StopBrowserResponse,
    StopInstanceResponse,
)
from .base_client import BaseClient, AsyncBaseClient
from .instance.types import Action, Command

OMIT = typing.cast(typing.Any, ...)

PydanticModelT = typing.TypeVar("PydanticModelT", bound=BaseModel)


class Agent:
    def __init__(self, instance_id: str, client: BaseClient):
        self.instance_id = instance_id
        self._client = client

    def act(
        self,
        *,
        cmd: str,
        include_screenshot: Optional[bool] = OMIT,
        model: Optional[Model] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> ActResponse:
        return self._client.agent.act(
            self.instance_id,
            cmd=cmd,
            include_screenshot=include_screenshot,
            model=model,
            request_options=request_options,
        )

    def scrape(
        self,
        *,
        cmd: str,
        schema: Optional[Dict[str, Optional[Any]]] = OMIT,
        include_screenshot: Optional[bool] = OMIT,
        model: Optional[Model] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> ScrapeResponse:
        return self._client.agent.scrape(
            self.instance_id,
            cmd=cmd,
            schema=schema,
            include_screenshot=include_screenshot,
            model=model,
            request_options=request_options,
        )

    def scrape_to_pydantic(
        self,
        *,
        cmd: str,
        schema: PydanticModelT,
        model: typing.Optional[Model] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> PydanticModelT:
        response = self._client.agent.scrape(
            self.instance_id,
            cmd=cmd,
            schema=schema.model_json_schema(),
            model=model,
            request_options=request_options,
        )

        try:
            return schema.model_validate(response.data)
        except ValidationError as e:
            raise ValidationError(f"Validation error at client side: {e}") from e


class AsyncAgent:
    def __init__(self, instance_id: str, client: AsyncBaseClient):
        self.instance_id = instance_id
        self._client = client

    async def act(
        self,
        *,
        cmd: str,
        include_screenshot: Optional[bool] = OMIT,
        model: Optional[Model] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> ActResponse:
        return await self._client.agent.act(
            self.instance_id,
            cmd=cmd,
            include_screenshot=include_screenshot,
            model=model,
            request_options=request_options,
        )

    async def scrape(
        self,
        *,
        cmd: str,
        schema: Optional[Dict[str, Optional[Any]]] = OMIT,
        include_screenshot: Optional[bool] = OMIT,
        model: Optional[Model] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> ScrapeResponse:
        return await self._client.agent.scrape(
            self.instance_id,
            cmd=cmd,
            schema=schema,
            include_screenshot=include_screenshot,
            model=model,
            request_options=request_options,
        )

    async def scrape_to_pydantic(
        self,
        *,
        cmd: str,
        schema: PydanticModelT,
        model: typing.Optional[Model] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> PydanticModelT:
        response = await self._client.agent.scrape(
            self.instance_id,
            cmd=cmd,
            schema=schema.model_json_schema(),
            model=model,
            request_options=request_options,
        )

        try:
            return schema.model_validate(response.data)
        except ValidationError as e:
            raise ValidationError(f"Validation error at client side: {e}") from e


class Browser:
    def __init__(self, instance_id: str, client: BaseClient):
        self.instance_id = instance_id
        self._client = client

    def start(
        self, request_options: Optional[RequestOptions] = None
    ) -> StartBrowserResponse:
        return self._client.browser.start(
            self.instance_id, request_options=request_options
        )

    def get_cdp_url(
        self, request_options: Optional[RequestOptions] = None
    ) -> BrowserGetCdpUrlResponse:
        return self._client.browser.get_cdp_url(
            self.instance_id, request_options=request_options
        )

    def authenticate(
        self, *, context_id: str, request_options: Optional[RequestOptions] = None
    ) -> BrowserAuthenticateResponse:
        return self._client.browser.authenticate(
            self.instance_id, context_id=context_id, request_options=request_options
        )

    def stop(
        self, request_options: Optional[RequestOptions] = None
    ) -> StopBrowserResponse:
        return self._client.browser.stop(
            self.instance_id, request_options=request_options
        )


class AsyncBrowser:
    def __init__(self, instance_id: str, client: AsyncBaseClient):
        self.instance_id = instance_id
        self._client = client

    async def start(
        self, request_options: Optional[RequestOptions] = None
    ) -> StartBrowserResponse:
        return await self._client.browser.start(
            self.instance_id, request_options=request_options
        )

    async def get_cdp_url(
        self, request_options: Optional[RequestOptions] = None
    ) -> BrowserGetCdpUrlResponse:
        return await self._client.browser.get_cdp_url(
            self.instance_id, request_options=request_options
        )

    async def authenticate(
        self, *, context_id: str, request_options: Optional[RequestOptions] = None
    ) -> BrowserAuthenticateResponse:
        return await self._client.browser.authenticate(
            self.instance_id, context_id=context_id, request_options=request_options
        )

    async def stop(
        self, request_options: Optional[RequestOptions] = None
    ) -> StopBrowserResponse:
        return await self._client.browser.stop(
            self.instance_id, request_options=request_options
        )


class Code:
    def __init__(self, instance_id: str, client: BaseClient):
        self.instance_id = instance_id
        self._client = client

    def execute(
        self,
        *,
        code: str,
        kernel_name: Optional[str] = OMIT,
        timeout: Optional[int] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> Optional[Any]:
        return self._client.code.execute(
            self.instance_id,
            code=code,
            kernel_name=kernel_name,
            timeout=timeout,
            request_options=request_options,
        )


class AsyncCode:
    def __init__(self, instance_id: str, client: AsyncBaseClient):
        self.instance_id = instance_id
        self._client = client

    async def execute(
        self,
        *,
        code: str,
        kernel_name: Optional[str] = OMIT,
        timeout: Optional[int] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> Optional[Any]:
        return await self._client.code.execute(
            self.instance_id,
            code=code,
            kernel_name=kernel_name,
            timeout=timeout,
            request_options=request_options,
        )


class Notebook:
    def __init__(self, instance_id: str, client: BaseClient):
        self.instance_id = instance_id
        self._client = client

    def list_kernels(
        self, request_options: Optional[RequestOptions] = None
    ) -> List[KernelInfo]:
        return self._client.notebook.list_kernels(
            self.instance_id, request_options=request_options
        )

    def create(
        self,
        *,
        name: str,
        kernel_name: str,
        request_options: Optional[RequestOptions] = None,
    ) -> NotebookType:
        return self._client.notebook.create(
            self.instance_id,
            name=name,
            kernel_name=kernel_name,
            request_options=request_options,
        )

    def get(
        self, notebook_id: str, request_options: Optional[RequestOptions] = None
    ) -> NotebookType:
        return self._client.notebook.get(
            self.instance_id, notebook_id, request_options=request_options
        )

    def delete(
        self, notebook_id: str, request_options: Optional[RequestOptions] = None
    ) -> None:
        self._client.notebook.delete(
            self.instance_id, notebook_id, request_options=request_options
        )

    def add_cell(
        self,
        notebook_id: str,
        *,
        type: CellType,
        content: str,
        metadata: Optional[Dict[str, Optional[Any]]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> NotebookCell:
        return self._client.notebook.add_cell(
            self.instance_id,
            notebook_id,
            type=type,
            content=content,
            metadata=metadata,
            request_options=request_options,
        )

    def execute_cell(
        self,
        notebook_id: str,
        cell_id: str,
        *,
        timeout: Optional[int] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> NotebookCell:
        return self._client.notebook.execute_cell(
            self.instance_id,
            notebook_id,
            cell_id,
            timeout=timeout,
            request_options=request_options,
        )

    def execute(
        self,
        notebook_id: str,
        *,
        timeout: Optional[int] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> List[NotebookCell]:
        return self._client.notebook.execute(
            self.instance_id,
            notebook_id,
            timeout=timeout,
            request_options=request_options,
        )


class AsyncNotebook:
    def __init__(self, instance_id: str, client: AsyncBaseClient):
        self.instance_id = instance_id
        self._client = client

    async def list_kernels(
        self, request_options: Optional[RequestOptions] = None
    ) -> List[KernelInfo]:
        return await self._client.notebook.list_kernels(
            self.instance_id, request_options=request_options
        )

    async def create(
        self,
        *,
        name: str,
        kernel_name: str,
        request_options: Optional[RequestOptions] = None,
    ) -> NotebookType:
        return await self._client.notebook.create(
            self.instance_id,
            name=name,
            kernel_name=kernel_name,
            request_options=request_options,
        )

    async def get(
        self, notebook_id: str, request_options: Optional[RequestOptions] = None
    ) -> NotebookType:
        return await self._client.notebook.get(
            self.instance_id, notebook_id, request_options=request_options
        )

    async def delete(
        self, notebook_id: str, request_options: Optional[RequestOptions] = None
    ) -> None:
        await self._client.notebook.delete(
            self.instance_id, notebook_id, request_options=request_options
        )

    async def add_cell(
        self,
        notebook_id: str,
        *,
        type: CellType,
        content: str,
        metadata: Optional[Dict[str, Optional[Any]]] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> NotebookCell:
        return await self._client.notebook.add_cell(
            self.instance_id,
            notebook_id,
            type=type,
            content=content,
            metadata=metadata,
            request_options=request_options,
        )

    async def execute_cell(
        self,
        notebook_id: str,
        cell_id: str,
        *,
        timeout: Optional[int] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> NotebookCell:
        return await self._client.notebook.execute_cell(
            self.instance_id,
            notebook_id,
            cell_id,
            timeout=timeout,
            request_options=request_options,
        )

    async def execute(
        self,
        notebook_id: str,
        *,
        timeout: Optional[int] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> List[NotebookCell]:
        return await self._client.notebook.execute(
            self.instance_id,
            notebook_id,
            timeout=timeout,
            request_options=request_options,
        )


class File:
    def __init__(self, instance_id: str, client: BaseClient):
        self.instance_id = instance_id
        self._client = client

    def read(
        self,
        *,
        path: str,
        encoding: Optional[str] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> FileReadResponse:
        return self._client.file.read(
            self.instance_id,
            path=path,
            encoding=encoding,
            request_options=request_options,
        )

    def write(
        self,
        *,
        path: str,
        content: str,
        encoding: Optional[str] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Optional[Any]]:
        return self._client.file.write(
            self.instance_id,
            path=path,
            content=content,
            encoding=encoding,
            request_options=request_options,
        )

    def upload(
        self,
        *,
        path: str,
        content: str,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Optional[Any]]:
        return self._client.file.upload(
            self.instance_id,
            path=path,
            content=content,
            request_options=request_options,
        )

    def download(
        self, *, path: str, request_options: Optional[RequestOptions] = None
    ) -> FileDownloadResponse:
        return self._client.file.download(
            self.instance_id, path=path, request_options=request_options
        )


class AsyncFile:
    def __init__(self, instance_id: str, client: AsyncBaseClient):
        self.instance_id = instance_id
        self._client = client

    async def read(
        self,
        *,
        path: str,
        encoding: Optional[str] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> FileReadResponse:
        return await self._client.file.read(
            self.instance_id,
            path=path,
            encoding=encoding,
            request_options=request_options,
        )

    async def write(
        self,
        *,
        path: str,
        content: str,
        encoding: Optional[str] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Optional[Any]]:
        return await self._client.file.write(
            self.instance_id,
            path=path,
            content=content,
            encoding=encoding,
            request_options=request_options,
        )

    async def upload(
        self,
        *,
        path: str,
        content: str,
        request_options: Optional[RequestOptions] = None,
    ) -> Dict[str, Optional[Any]]:
        return await self._client.file.upload(
            self.instance_id,
            path=path,
            content=content,
            request_options=request_options,
        )

    async def download(
        self, *, path: str, request_options: Optional[RequestOptions] = None
    ) -> FileDownloadResponse:
        return await self._client.file.download(
            self.instance_id, path=path, request_options=request_options
        )


class Env:
    def __init__(self, instance_id: str, client: BaseClient):
        self.instance_id = instance_id
        self._client = client

    def set(
        self,
        *,
        variables: Dict[str, str],
        request_options: Optional[RequestOptions] = None,
    ) -> EnvResponse:
        return self._client.env.set(
            self.instance_id, variables=variables, request_options=request_options
        )

    def get(self, request_options: Optional[RequestOptions] = None) -> EnvGetResponse:
        return self._client.env.get(self.instance_id, request_options=request_options)

    def delete(
        self, *, keys: Sequence[str], request_options: Optional[RequestOptions] = None
    ) -> EnvResponse:
        return self._client.env.delete(
            self.instance_id, keys=keys, request_options=request_options
        )


class AsyncEnv:
    def __init__(self, instance_id: str, client: AsyncBaseClient):
        self.instance_id = instance_id
        self._client = client

    async def set(
        self,
        *,
        variables: Dict[str, str],
        request_options: Optional[RequestOptions] = None,
    ) -> EnvResponse:
        return await self._client.env.set(
            self.instance_id, variables=variables, request_options=request_options
        )

    async def get(
        self, request_options: Optional[RequestOptions] = None
    ) -> EnvGetResponse:
        return await self._client.env.get(
            self.instance_id, request_options=request_options
        )

    async def delete(
        self, *, keys: Sequence[str], request_options: Optional[RequestOptions] = None
    ) -> EnvResponse:
        return await self._client.env.delete(
            self.instance_id, keys=keys, request_options=request_options
        )


class Instance:
    def __init__(
        self,
        id: str,
        launch_time: datetime,
        instance_type: str,
        status: str,
        client: BaseClient,
    ):
        self.id = id
        self.launch_time = launch_time
        self.instance_type = instance_type
        self.status = status
        self._client = client
        self.agent = Agent(self.id, self._client)
        self.browser = Browser(self.id, self._client)
        self.code = Code(self.id, self._client)
        self.notebook = Notebook(self.id, self._client)
        self.file = File(self.id, self._client)
        self.env = Env(self.id, self._client)

    def screenshot(
        self, request_options: Optional[RequestOptions] = None
    ) -> InstanceScreenshotResponse:
        return self._client.instance.screenshot(
            self.id, request_options=request_options
        )

    def get_stream_url(
        self, request_options: Optional[RequestOptions] = None
    ) -> InstanceGetStreamUrlResponse:
        return self._client.instance.get_stream_url(
            self.id, request_options=request_options
        )

    def computer(
        self,
        *,
        action: Action,
        coordinate: Optional[Sequence[int]] = OMIT,
        text: Optional[str] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> Optional[Any]:
        return self._client.instance.computer(
            self.id,
            action=action,
            coordinate=coordinate,
            text=text,
            request_options=request_options,
        )

    def bash(
        self,
        *,
        command: Optional[str] = OMIT,
        restart: Optional[bool] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> Optional[Any]:
        return self._client.instance.bash(
            self.id, command=command, restart=restart, request_options=request_options
        )

    def edit(
        self,
        *,
        command: Command,
        path: str,
        file_text: Optional[str] = OMIT,
        view_range: Optional[Sequence[int]] = OMIT,
        old_str: Optional[str] = OMIT,
        new_str: Optional[str] = OMIT,
        insert_line: Optional[int] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> Optional[Any]:
        return self._client.instance.edit(
            self.id,
            command=command,
            path=path,
            file_text=file_text,
            view_range=view_range,
            old_str=old_str,
            new_str=new_str,
            insert_line=insert_line,
            request_options=request_options,
        )

    def stop(
        self, request_options: Optional[RequestOptions] = None
    ) -> StopInstanceResponse:
        return self._client.instance.stop(self.id, request_options=request_options)

    def pause(
        self, request_options: Optional[RequestOptions] = None
    ) -> StopInstanceResponse:
        return self._client.instance.pause(self.id, request_options=request_options)

    def resume(
        self,
        *,
        timeout_hours: Optional[float] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> GetInstanceResponse:
        return self._client.instance.resume(
            self.id,
            timeout_hours=timeout_hours,
            request_options=request_options,
        )


class AsyncInstance:
    def __init__(
        self,
        id: str,
        launch_time: datetime,
        instance_type: str,
        status: str,
        client: AsyncBaseClient,
    ):
        self.id = id
        self.launch_time = launch_time
        self.instance_type = instance_type
        self.status = status
        self._client = client
        self.agent = AsyncAgent(self.id, self._client)
        self.browser = AsyncBrowser(self.id, self._client)
        self.code = AsyncCode(self.id, self._client)
        self.notebook = AsyncNotebook(self.id, self._client)
        self.file = AsyncFile(self.id, self._client)
        self.env = AsyncEnv(self.id, self._client)

    async def screenshot(
        self, request_options: Optional[RequestOptions] = None
    ) -> InstanceScreenshotResponse:
        return await self._client.instance.screenshot(
            self.id, request_options=request_options
        )

    async def get_stream_url(
        self, request_options: Optional[RequestOptions] = None
    ) -> InstanceGetStreamUrlResponse:
        return await self._client.instance.get_stream_url(
            self.id, request_options=request_options
        )

    async def computer(
        self,
        *,
        action: Action,
        coordinate: Optional[Sequence[int]] = OMIT,
        text: Optional[str] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> Optional[Any]:
        return await self._client.instance.computer(
            self.id,
            action=action,
            coordinate=coordinate,
            text=text,
            request_options=request_options,
        )

    async def bash(
        self,
        *,
        command: Optional[str] = OMIT,
        restart: Optional[bool] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> Optional[Any]:
        return await self._client.instance.bash(
            self.id, command=command, restart=restart, request_options=request_options
        )

    async def edit(
        self,
        *,
        command: Command,
        path: str,
        file_text: Optional[str] = OMIT,
        view_range: Optional[Sequence[int]] = OMIT,
        old_str: Optional[str] = OMIT,
        new_str: Optional[str] = OMIT,
        insert_line: Optional[int] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> Optional[Any]:
        return await self._client.instance.edit(
            self.id,
            command=command,
            path=path,
            file_text=file_text,
            view_range=view_range,
            old_str=old_str,
            new_str=new_str,
            insert_line=insert_line,
            request_options=request_options,
        )

    async def stop(
        self, request_options: Optional[RequestOptions] = None
    ) -> StopInstanceResponse:
        return await self._client.instance.stop(
            self.id, request_options=request_options
        )

    async def pause(
        self, request_options: Optional[RequestOptions] = None
    ) -> StopInstanceResponse:
        return await self._client.instance.pause(
            self.id, request_options=request_options
        )

    async def resume(
        self,
        *,
        timeout_hours: Optional[float] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> GetInstanceResponse:
        return await self._client.instance.resume(
            self.id,
            timeout_hours=timeout_hours,
            request_options=request_options,
        )


class Scrapybara:
    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        environment: ScrapybaraEnvironment = ScrapybaraEnvironment.PRODUCTION,
        api_key: Optional[str] = os.getenv("SCRAPYBARA_API_KEY"),
        timeout: Optional[float] = None,
        follow_redirects: Optional[bool] = True,
        httpx_client: Optional[httpx.Client] = None,
    ):
        self._base_client = BaseClient(
            base_url=base_url,
            environment=environment,
            api_key=api_key,
            timeout=timeout,
            follow_redirects=follow_redirects,
            httpx_client=httpx_client,
        )

    def start(
        self,
        *,
        instance_type: Optional[
            Union[DeploymentConfigInstanceType, Literal["small", "medium", "large"]]
        ] = OMIT,
        timeout_hours: Optional[float] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> Instance:
        response = self._base_client.start(
            instance_type=instance_type,
            timeout_hours=timeout_hours,
            request_options=request_options,
        )
        return Instance(
            response.id,
            response.launch_time,
            response.instance_type,
            response.status,
            self._base_client,
        )

    def get(
        self, instance_id: str, *, request_options: Optional[RequestOptions] = None
    ) -> Instance:
        response = self._base_client.get(instance_id, request_options=request_options)
        return Instance(
            response.id,
            response.launch_time,
            response.instance_type,
            response.status,
            self._base_client,
        )


class AsyncScrapybara:
    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        environment: ScrapybaraEnvironment = ScrapybaraEnvironment.PRODUCTION,
        api_key: Optional[str] = os.getenv("SCRAPYBARA_API_KEY"),
        timeout: Optional[float] = None,
        follow_redirects: Optional[bool] = True,
        httpx_client: Optional[httpx.AsyncClient] = None,
    ):
        self._base_client = AsyncBaseClient(
            base_url=base_url,
            environment=environment,
            api_key=api_key,
            timeout=timeout,
            follow_redirects=follow_redirects,
            httpx_client=httpx_client,
        )

    async def start(
        self,
        *,
        instance_type: Optional[
            Union[DeploymentConfigInstanceType, Literal["small", "medium", "large"]]
        ] = OMIT,
        timeout_hours: Optional[float] = OMIT,
        request_options: Optional[RequestOptions] = None,
    ) -> AsyncInstance:
        response = await self._base_client.start(
            instance_type=instance_type,
            timeout_hours=timeout_hours,
            request_options=request_options,
        )
        return AsyncInstance(
            response.id,
            response.launch_time,
            response.instance_type,
            response.status,
            self._base_client,
        )

    async def get(
        self, instance_id: str, *, request_options: Optional[RequestOptions] = None
    ) -> AsyncInstance:
        response = await self._base_client.get(
            instance_id, request_options=request_options
        )
        return AsyncInstance(
            response.id,
            response.launch_time,
            response.instance_type,
            response.status,
            self._base_client,
        )
