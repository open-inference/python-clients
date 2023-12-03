# Copyright 2023 The Open Inference Protocol Working Group
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

import httpx

from .core.api_error import ApiError
from .core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .core.jsonable_encoder import jsonable_encoder
from .errors.bad_request_error import BadRequestError
from .errors.internal_server_error import InternalServerError
from .errors.not_found_error import NotFoundError
from .errors.service_unavailable_error import ServiceUnavailableError
from .types.inference_request import InferenceRequest
from .types.inference_response import InferenceResponse
from .types.metadata_model_response import MetadataModelResponse
from .types.metadata_server_response import MetadataServerResponse

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class OpenInferenceClient:
    def __init__(
        self, *, base_url: str, timeout: typing.Optional[float] = 60, httpx_client: typing.Optional[httpx.Client] = None
    ):
        self._client_wrapper = SyncClientWrapper(
            base_url=base_url, httpx_client=httpx.Client(timeout=timeout) if httpx_client is None else httpx_client
        )

    def check_server_liveness(self) -> None:
        """
        The “server live” API indicates if the inference server is able to receive and respond to metadata and inference requests. The “server live” API can be used directly to implement the Kubernetes livenessProbe.

        ---
        from open_inference.client import OpenInferenceClient

        client = OpenInferenceClient(
            base_url="https://yourhost.com/path/to/api",
        )
        client.check_server_liveness()
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "v2/health/live"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return
        if _response.status_code == 500:
            raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def check_server_readiness(self) -> None:
        """
        The “server ready” health API indicates if all the models are ready for inferencing. The “server ready” health API can be used directly to implement the Kubernetes readinessProbe.

        ---
        from open_inference.client import OpenInferenceClient

        client = OpenInferenceClient(
            base_url="https://yourhost.com/path/to/api",
        )
        client.check_server_readiness()
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "v2/health/ready"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return
        if _response.status_code == 503:
            raise ServiceUnavailableError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def check_model_version_readiness(self, model_name: str, model_version: str) -> None:
        """
        The "model ready" health API indicates if a specific model is ready for inferencing. The model name and version must be provided in the URL.

        Parameters:
            - model_name: str.

            - model_version: str.
        ---
        from open_inference.client import OpenInferenceClient

        client = OpenInferenceClient(
            base_url="https://yourhost.com/path/to/api",
        )
        client.check_model_version_readiness(
            model_name="model-name",
            model_version="model-version",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", f"v2/models/{model_name}/versions/{model_version}/ready"
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 503:
            raise ServiceUnavailableError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def check_model_readiness(self, model_name: str) -> None:
        """
        The "model ready" health API indicates if a specific model is ready for inferencing. The model name is provided in the URL. The server may choose a model version based on its own policies.

        Parameters:
            - model_name: str.
        ---
        from open_inference.client import OpenInferenceClient

        client = OpenInferenceClient(
            base_url="https://yourhost.com/path/to/api",
        )
        client.check_model_readiness(
            model_name="model-name",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", f"v2/models/{model_name}/ready"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 503:
            raise ServiceUnavailableError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def read_server_metadata(self) -> MetadataServerResponse:
        """
        The server metadata endpoint provides information about the server. Compliant servers return a [Server Metadata Response JSON Object](#server-metadata-response-json-object) or a [Server Metadata Response JSON Error Object](#server-metadata-response-json-error-object).
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "v2"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(MetadataServerResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def read_model_version_metadata(self, model_name: str, model_version: str) -> MetadataModelResponse:
        """
        The per-model metadata endpoint provides information about a model. Compliant servers return a [Model Metadata Response JSON Object](#model-metadata-response-json-object) or a [Model Metadata Response JSON Error Object](#model-metadata-response-json-error-object). The model name and version must be provided in the URL.

        Parameters:
            - model_name: str.

            - model_version: str.
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", f"v2/models/{model_name}/versions/{model_version}"
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(MetadataModelResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def read_model_metadata(self, model_name: str) -> MetadataModelResponse:
        """
        The per-model metadata endpoint provides information about a model. Compliant servers return a [Model Metadata Response JSON Object](#model-metadata-response-json-object) or a [Model Metadata Response JSON Error Object](#model-metadata-response-json-error-object). The model name is provided in the URL. The server may choose a model version based on its own policies or return an error.

        Parameters:
            - model_name: str.
        """
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", f"v2/models/{model_name}"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(MetadataModelResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def model_version_infer(
        self, model_name: str, model_version: str, *, request: InferenceRequest
    ) -> InferenceResponse:
        """
        Send data to a model for inferencing via an [Inference Request JSON Object](#inference-request-json-object). Compliant servers return an [Inference Response JSON Object](#inference-response-json-object) or an [Inference Response JSON Error Object](#inference-response-json-error-object). The model name and version must be provided in the URL.
        See [Inference Request Examples](#inference-request-examples) for some example HTTP/REST requests and responses.

        Parameters:
            - model_name: str.

            - model_version: str.

            - request: InferenceRequest.
        """
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", f"v2/models/{model_name}/versions/{model_version}/infer"
            ),
            json=jsonable_encoder(request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(InferenceResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def model_infer(self, model_name: str, *, request: InferenceRequest) -> InferenceResponse:
        """
        Send data to a model for inferencing via an [Inference Request JSON Object](#inference-request-json-object). Compliant servers return an [Inference Response JSON Object](#inference-response-json-object) or an [Inference Response JSON Error Object](#inference-response-json-error-object). The model name is provided in the URL. The server may choose a model version based on its own policies or return an error.
        See [Inference Request Examples](#inference-request-examples) for some example HTTP/REST requests and responses.

        Parameters:
            - model_name: str.

            - request: InferenceRequest.
        """
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", f"v2/models/{model_name}/infer"),
            json=jsonable_encoder(request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(InferenceResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncOpenInferenceClient:
    def __init__(
        self,
        *,
        base_url: str,
        timeout: typing.Optional[float] = 60,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
    ):
        self._client_wrapper = AsyncClientWrapper(
            base_url=base_url, httpx_client=httpx.AsyncClient(timeout=timeout) if httpx_client is None else httpx_client
        )

    async def check_server_liveness(self) -> None:
        """
        The “server live” API indicates if the inference server is able to receive and respond to metadata and inference requests. The “server live” API can be used directly to implement the Kubernetes livenessProbe.

        ---
        from open_inference.client import AsyncOpenInferenceClient

        client = AsyncOpenInferenceClient(
            base_url="https://yourhost.com/path/to/api",
        )
        await client.check_server_liveness()
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "v2/health/live"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return
        if _response.status_code == 500:
            raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def check_server_readiness(self) -> None:
        """
        The “server ready” health API indicates if all the models are ready for inferencing. The “server ready” health API can be used directly to implement the Kubernetes readinessProbe.

        ---
        from open_inference.client import AsyncOpenInferenceClient

        client = AsyncOpenInferenceClient(
            base_url="https://yourhost.com/path/to/api",
        )
        await client.check_server_readiness()
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "v2/health/ready"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return
        if _response.status_code == 503:
            raise ServiceUnavailableError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def check_model_version_readiness(self, model_name: str, model_version: str) -> None:
        """
        The "model ready" health API indicates if a specific model is ready for inferencing. The model name and version must be provided in the URL.

        Parameters:
            - model_name: str.

            - model_version: str.
        ---
        from open_inference.client import AsyncOpenInferenceClient

        client = AsyncOpenInferenceClient(
            base_url="https://yourhost.com/path/to/api",
        )
        await client.check_model_version_readiness(
            model_name="model-name",
            model_version="model-version",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", f"v2/models/{model_name}/versions/{model_version}/ready"
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 503:
            raise ServiceUnavailableError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def check_model_readiness(self, model_name: str) -> None:
        """
        The "model ready" health API indicates if a specific model is ready for inferencing. The model name is provided in the URL. The server may choose a model version based on its own policies.

        Parameters:
            - model_name: str.
        ---
        from open_inference.client import AsyncOpenInferenceClient

        client = AsyncOpenInferenceClient(
            base_url="https://yourhost.com/path/to/api",
        )
        await client.check_model_readiness(
            model_name="model-name",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", f"v2/models/{model_name}/ready"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 503:
            raise ServiceUnavailableError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def read_server_metadata(self) -> MetadataServerResponse:
        """
        The server metadata endpoint provides information about the server. Compliant servers return a [Server Metadata Response JSON Object](#server-metadata-response-json-object) or a [Server Metadata Response JSON Error Object](#server-metadata-response-json-error-object).
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "v2"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(MetadataServerResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def read_model_version_metadata(self, model_name: str, model_version: str) -> MetadataModelResponse:
        """
        The per-model metadata endpoint provides information about a model. Compliant servers return a [Model Metadata Response JSON Object](#model-metadata-response-json-object) or a [Model Metadata Response JSON Error Object](#model-metadata-response-json-error-object). The model name and version must be provided in the URL.

        Parameters:
            - model_name: str.

            - model_version: str.
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", f"v2/models/{model_name}/versions/{model_version}"
            ),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(MetadataModelResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def read_model_metadata(self, model_name: str) -> MetadataModelResponse:
        """
        The per-model metadata endpoint provides information about a model. Compliant servers return a [Model Metadata Response JSON Object](#model-metadata-response-json-object) or a [Model Metadata Response JSON Error Object](#model-metadata-response-json-error-object). The model name is provided in the URL. The server may choose a model version based on its own policies or return an error.

        Parameters:
            - model_name: str.
        """
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", f"v2/models/{model_name}"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(MetadataModelResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def model_version_infer(
        self, model_name: str, model_version: str, *, request: InferenceRequest
    ) -> InferenceResponse:
        """
        Send data to a model for inferencing via an [Inference Request JSON Object](#inference-request-json-object). Compliant servers return an [Inference Response JSON Object](#inference-response-json-object) or an [Inference Response JSON Error Object](#inference-response-json-error-object). The model name and version must be provided in the URL.
        See [Inference Request Examples](#inference-request-examples) for some example HTTP/REST requests and responses.

        Parameters:
            - model_name: str.

            - model_version: str.

            - request: InferenceRequest.
        """
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_base_url()}/", f"v2/models/{model_name}/versions/{model_version}/infer"
            ),
            json=jsonable_encoder(request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(InferenceResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def model_infer(self, model_name: str, *, request: InferenceRequest) -> InferenceResponse:
        """
        Send data to a model for inferencing via an [Inference Request JSON Object](#inference-request-json-object). Compliant servers return an [Inference Response JSON Object](#inference-response-json-object) or an [Inference Response JSON Error Object](#inference-response-json-error-object). The model name is provided in the URL. The server may choose a model version based on its own policies or return an error.
        See [Inference Request Examples](#inference-request-examples) for some example HTTP/REST requests and responses.

        Parameters:
            - model_name: str.

            - request: InferenceRequest.
        """
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", f"v2/models/{model_name}/infer"),
            json=jsonable_encoder(request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(InferenceResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)