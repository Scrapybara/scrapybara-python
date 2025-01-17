from datetime import datetime
from typing import (
    Optional,
    Any,
    Dict,
    List,
    Sequence,
    Type,
    TypeVar,
    Union,
    Literal,
    Generator,
    Callable,
    AsyncGenerator,
)
import typing
import os
import asyncio

import httpx
from pydantic import BaseModel, ConfigDict

from scrapybara.core.http_client import AsyncHttpClient, HttpClient
from scrapybara.environment import ScrapybaraEnvironment
from .core.request_options import RequestOptions
from .core.api_error import ApiError
from .types import (
    AuthStateResponse,
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
    SaveBrowserAuthResponse,
    StartBrowserResponse,
    StopBrowserResponse,
    StopInstanceResponse,
)
from .types.act import (
    SingleActRequest,
    SingleActResponse,
    Message,
    Model,
    TextPart,
    Tool,
    ApiTool,
    ToolCallPart,
    ToolMessage,
    ToolResultPart,
    UserMessage,
    AssistantMessage,
    Step,
    ActResponse,
    TokenUsage,
)
from .base_client import BaseClient, AsyncBaseClient
from .instance.types import Action, Command

OMIT = typing.cast(typing.Any, ...)
SchemaT = TypeVar("SchemaT", bound=BaseModel)


class StructuredOutputTool(Tool):
    """A tool that allows the agent to output structured data."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    _model: Type[BaseModel]

    def __init__(self, model: Type[BaseModel]):
        super().__init__(
            name="structured_output",
            description="Output structured data according to the provided schema parameters. Only use this tool at the end of your task. The output data is final and will be passed directly back to the user.",
            parameters=model,
        )
        self._model = model

    def __call__(self, **kwargs: Any) -> Dict[str, Any]:
        validated = self._model.model_validate(kwargs)
        return validated.model_dump()


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

    def save_auth(
        self,
        *,
        name: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> SaveBrowserAuthResponse:
        return self._client.browser.save_auth(
            self.instance_id, name=name, request_options=request_options
        )

    def authenticate(
        self, *, auth_state_id: str, request_options: Optional[RequestOptions] = None
    ) -> BrowserAuthenticateResponse:
        return self._client.browser.authenticate(
            self.instance_id,
            auth_state_id=auth_state_id,
            request_options=request_options,
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

    async def save_auth(
        self,
        *,
        name: Optional[str] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> SaveBrowserAuthResponse:
        return await self._client.browser.save_auth(
            self.instance_id, name=name, request_options=request_options
        )

    async def authenticate(
        self, *, auth_state_id: str, request_options: Optional[RequestOptions] = None
    ) -> BrowserAuthenticateResponse:
        return await self._client.browser.authenticate(
            self.instance_id,
            auth_state_id=auth_state_id,
            request_options=request_options,
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

    @property
    def httpx_client(self) -> HttpClient:
        return self._base_client._client_wrapper.httpx_client

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

    def get_instances(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List[Instance]:
        response = self._base_client.get_instances(request_options=request_options)
        return [
            Instance(
                instance.id,
                instance.launch_time,
                instance.instance_type,
                instance.status,
                self._base_client,
            )
            for instance in response
        ]

    def get_auth_states(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List[AuthStateResponse]:
        response = self._base_client.get_auth_states(request_options=request_options)
        return [AuthStateResponse(id=state.id, name=state.name) for state in response]

    def act(
        self,
        *,
        model: Model,
        tools: Optional[List[Tool]] = None,
        system: Optional[str] = None,
        prompt: Optional[str] = None,
        messages: Optional[List[Message]] = None,
        schema: Optional[Type[SchemaT]] = None,
        on_step: Optional[Callable[[Step], None]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ActResponse[SchemaT]:
        """
        Run an agent loop with the given tools and model, returning all messages at the end.

        Args:
            model: The model to use for generating responses
            tools: List of tools available to the agent
            system: System prompt for the agent
            prompt: Initial user prompt
            messages: List of messages to start with
            schema: Optional Pydantic model class to structure the final output
            on_step: Callback for each step of the conversation
            temperature: Optional temperature parameter for the model
            max_tokens: Optional max tokens parameter for the model
            request_options: Optional request configuration

        Returns:
            ActResponse containing all messages, steps, text, output (if schema is provided), and token usage
        """
        result_messages: List[Message] = []
        steps: List[Step] = []
        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_tokens = 0

        if messages:
            result_messages.extend(messages)

        for step in self.act_stream(
            model=model,
            tools=tools,
            system=system,
            prompt=prompt,
            messages=messages,
            schema=schema,
            on_step=on_step,
            temperature=temperature,
            max_tokens=max_tokens,
            request_options=request_options,
        ):
            steps.append(step)
            assistant_msg = AssistantMessage(
                content=[TextPart(text=step.text)] + (step.tool_calls or [])
            )
            result_messages.append(assistant_msg)
            if step.tool_results:
                tool_msg = ToolMessage(content=step.tool_results)
                result_messages.append(tool_msg)

            if step.usage:
                total_prompt_tokens += step.usage.prompt_tokens
                total_completion_tokens += step.usage.completion_tokens
                total_tokens += step.usage.total_tokens

        text = steps[-1].text if steps else None
        if schema:
            output = (
                steps[-1].tool_results[-1].result if steps[-1].tool_results else None
            )
            output = schema.model_validate(output)

        usage = None
        if total_tokens > 0:
            usage = TokenUsage(
                prompt_tokens=total_prompt_tokens,
                completion_tokens=total_completion_tokens,
                total_tokens=total_tokens,
            )

        return ActResponse(
            messages=result_messages, steps=steps, text=text, output=output, usage=usage
        )

    def act_stream(
        self,
        *,
        model: Model,
        tools: Optional[List[Tool]] = None,
        system: Optional[str] = None,
        prompt: Optional[str] = None,
        messages: Optional[List[Message]] = None,
        schema: Optional[Type[BaseModel]] = None,
        on_step: Optional[Callable[[Step], None]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> Generator[Step, None, None]:
        """
        Run an interactive agent loop with the given tools and model.

        Args:
            model: The model to use for generating responses
            tools: List of tools available to the agent
            system: System prompt for the agent
            prompt: Initial user prompt
            messages: List of messages to start with
            schema: Optional Pydantic model class to structure the final output
            on_step: Callback for each step of the conversation
            temperature: Optional temperature parameter for the model
            max_tokens: Optional max tokens parameter for the model
            request_options: Optional request configuration

        Yields:
            Steps from the conversation, including tool results
        """
        current_messages: List[Message] = []
        if messages is None:
            if prompt is None:
                raise ValueError("prompt or messages must be provided")
            current_messages = [UserMessage(content=[TextPart(text=prompt)])]
        else:
            current_messages = list(messages)

        current_tools = [] if tools is None else list(tools)

        if schema:
            current_tools.append(StructuredOutputTool(schema))

        while True:
            # Convert tools to ApiTools
            api_tools = [ApiTool.from_tool(tool) for tool in current_tools]

            request = SingleActRequest(
                model=model,
                system=system,
                messages=current_messages,
                tools=api_tools,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            response = self.httpx_client.request(
                "v1/act",
                method="POST",
                json=request.model_dump(exclude_none=True),
                headers={"content-type": "application/json"},
                request_options=request_options,
            )

            if not 200 <= response.status_code < 300:
                raise ApiError(status_code=response.status_code, body=response.json())

            act_response = SingleActResponse.model_validate(response.json())
            current_messages.append(act_response.message)

            # Extract text from assistant message
            text = "\n".join(
                part.text
                for part in act_response.message.content
                if isinstance(part, TextPart)
            )

            # Extract tool calls
            tool_calls = [
                part
                for part in act_response.message.content
                if isinstance(part, ToolCallPart)
            ]

            # Create initial step
            step = Step(
                text=text,
                tool_calls=tool_calls if tool_calls else None,
                finish_reason=act_response.finish_reason,
                usage=act_response.usage,
            )

            # Check if there are tool calls
            has_tool_calls = bool(tool_calls)
            has_structured_output = False

            if has_tool_calls:
                tool_results: List[ToolResultPart] = []
                for part in tool_calls:
                    tool = next(t for t in current_tools if t.name == part.tool_name)
                    try:
                        if tool.name == "structured_output" and schema:
                            has_structured_output = True
                        result = tool(**part.args)
                        tool_results.append(
                            ToolResultPart(
                                tool_call_id=part.tool_call_id,
                                tool_name=part.tool_name,
                                result=result,
                            )
                        )
                    except Exception as e:
                        tool_results.append(
                            ToolResultPart(
                                tool_call_id=part.tool_call_id,
                                tool_name=part.tool_name,
                                result=str(e),
                                is_error=True,
                            )
                        )
                step.tool_results = tool_results
                tool_message = ToolMessage(content=tool_results)
                current_messages.append(tool_message)

            if on_step:
                on_step(step)
            yield step

            if not has_tool_calls or has_structured_output:
                break


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

    @property
    def httpx_client(self) -> AsyncHttpClient:
        return self._base_client._client_wrapper.httpx_client

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

    async def get_instances(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List[AsyncInstance]:
        response = await self._base_client.get_instances(
            request_options=request_options
        )
        return [
            AsyncInstance(
                instance.id,
                instance.launch_time,
                instance.instance_type,
                instance.status,
                self._base_client,
            )
            for instance in response
        ]

    async def get_auth_states(
        self,
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> List[AuthStateResponse]:
        response = await self._base_client.get_auth_states(
            request_options=request_options
        )
        return [AuthStateResponse(id=state.id, name=state.name) for state in response]

    async def act(
        self,
        *,
        tools: Optional[List[Tool]] = None,
        model: Model,
        system: Optional[str] = None,
        prompt: Optional[str] = None,
        messages: Optional[List[Message]] = None,
        schema: Optional[Type[SchemaT]] = None,
        on_step: Optional[Callable[[Step], None]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> ActResponse[SchemaT]:
        """
        Run an agent loop with the given tools and model, returning all messages at the end.

        Args:
            tools: List of tools available to the agent
            model: The model to use for generating responses
            system: System prompt for the agent
            prompt: Initial user prompt
            messages: List of messages to start with
            schema: Optional Pydantic model class to structure the final output
            on_step: Callback for each step of the conversation
            temperature: Optional temperature parameter for the model
            max_tokens: Optional max tokens parameter for the model
            request_options: Optional request configuration

        Returns:
            ActResponse containing all messages, steps, text, output (if schema is provided), and token usage
        """
        result_messages: List[Message] = []
        steps: List[Step] = []
        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_tokens = 0

        if messages:
            result_messages.extend(messages)

        async for step in self.act_stream(
            tools=tools,
            model=model,
            system=system,
            prompt=prompt,
            messages=messages,
            schema=schema,
            temperature=temperature,
            max_tokens=max_tokens,
            on_step=on_step,
            request_options=request_options,
        ):
            steps.append(step)
            assistant_msg = AssistantMessage(
                content=[TextPart(text=step.text)] + (step.tool_calls or [])
            )
            result_messages.append(assistant_msg)
            if step.tool_results:
                tool_msg = ToolMessage(content=step.tool_results)
                result_messages.append(tool_msg)

            if step.usage:
                total_prompt_tokens += step.usage.prompt_tokens
                total_completion_tokens += step.usage.completion_tokens
                total_tokens += step.usage.total_tokens

        text = steps[-1].text if steps else None
        if schema:
            output = (
                steps[-1].tool_results[-1].result if steps[-1].tool_results else None
            )
            output = schema.model_validate(output)

        usage = None
        if total_tokens > 0:
            usage = TokenUsage(
                prompt_tokens=total_prompt_tokens,
                completion_tokens=total_completion_tokens,
                total_tokens=total_tokens,
            )

        return ActResponse(
            messages=result_messages, steps=steps, text=text, output=output, usage=usage
        )

    async def act_stream(
        self,
        *,
        model: Model,
        tools: Optional[List[Tool]] = None,
        system: Optional[str] = None,
        prompt: Optional[str] = None,
        messages: Optional[List[Message]] = None,
        schema: Optional[Type[SchemaT]] = None,
        on_step: Optional[Callable[[Step], None]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        request_options: Optional[RequestOptions] = None,
    ) -> AsyncGenerator[Step, None]:
        """
        Run an interactive agent loop with the given tools and model.

        Args:
            model: The model to use for generating responses
            tools: List of tools available to the agent
            system: System prompt for the agent
            prompt: Initial user prompt
            messages: List of messages to start with
            schema: Optional Pydantic model class to structure the final output
            on_step: Callback for each step of the conversation
            temperature: Optional temperature parameter for the model
            max_tokens: Optional max tokens parameter for the model
            request_options: Optional request configuration

        Yields:
            Steps from the conversation, including tool results
        """
        current_messages: List[Message] = []
        if messages is None:
            if prompt is None:
                raise ValueError("prompt or messages must be provided")
            current_messages = [UserMessage(content=[TextPart(text=prompt)])]
        else:
            current_messages = list(messages)

        current_tools = [] if tools is None else list(tools)

        if schema:
            current_tools.append(StructuredOutputTool(schema))

        while True:
            # Convert tools to ApiTools
            api_tools = [ApiTool.from_tool(tool) for tool in current_tools]

            request = SingleActRequest(
                model=model,
                system=system,
                messages=current_messages,
                tools=api_tools,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            response = await self.httpx_client.request(
                "v1/act",
                method="POST",
                json=request.model_dump(exclude_none=True),
                headers={"content-type": "application/json"},
                request_options=request_options,
            )

            if not 200 <= response.status_code < 300:
                raise ApiError(status_code=response.status_code, body=response.json())

            act_response = SingleActResponse.model_validate(response.json())
            current_messages.append(act_response.message)

            # Extract text from assistant message
            text = "\n".join(
                part.text
                for part in act_response.message.content
                if isinstance(part, TextPart)
            )

            # Extract tool calls
            tool_calls = [
                part
                for part in act_response.message.content
                if isinstance(part, ToolCallPart)
            ]

            # Create initial step
            step = Step(
                text=text,
                tool_calls=tool_calls if tool_calls else None,
                finish_reason=act_response.finish_reason,
                usage=act_response.usage,
            )

            # Check if there are tool calls
            has_tool_calls = bool(tool_calls)
            has_structured_output = False

            if has_tool_calls:
                tool_results: List[ToolResultPart] = []
                for part in tool_calls:
                    tool = next(t for t in current_tools if t.name == part.tool_name)
                    try:
                        if tool.name == "structured_output" and schema:
                            has_structured_output = True
                        loop = asyncio.get_event_loop()
                        result = await loop.run_in_executor(
                            None, lambda: tool(**part.args)
                        )
                        tool_results.append(
                            ToolResultPart(
                                tool_call_id=part.tool_call_id,
                                tool_name=part.tool_name,
                                result=result,
                            )
                        )
                    except Exception as e:
                        tool_results.append(
                            ToolResultPart(
                                tool_call_id=part.tool_call_id,
                                tool_name=part.tool_name,
                                result=str(e),
                                is_error=True,
                            )
                        )
                step.tool_results = tool_results
                tool_message = ToolMessage(content=tool_results)
                current_messages.append(tool_message)

            if on_step:
                on_step(step)
            yield step

            if not has_tool_calls or has_structured_output:
                break
