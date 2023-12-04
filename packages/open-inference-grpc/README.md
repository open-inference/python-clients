# Open Inference Protocol gRPC Client

<p>
<a href="https://pypi.org/project/open-inference-grpc/">
    <img src="https://badge.fury.io/py/open-inference-grpc.svg" alt="Package version">
</a>
</p>

`open-inference-grpc` is a generated client library based on the gRPC protocol definition tracked in the [open-inference/open-inference-protocol/](https://github.com/open-inference/open-inference-protocol/blob/main/specification/protocol/open_inference_grpc.proto) repository.

---

## Installation

This package requires Python 3.8 or greater.

Install with your favorite tool from pypi.org/project/open-inference-grpc/

```console
$ pip install open-inference-grpc
$ poetry add open-inference-grpc
```

> A REST-based python client ([`open-inference-openapi`](https://pypi.org/project/open-inference-openapi)) also exists for the Open Inference Protocol, and can be installed alongside this gRPC client, as both are distributed as [namespace packages](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/#packaging-namespace-packages).

## Example

```python
# These dependencies are installed by open-inference-grpc
import grpc
from google.protobuf.json_format import MessageToDict

from open_inference.grpc.service import GRPCInferenceServiceStub
from open_inference.grpc.protocol import (
    ServerReadyRequest,
    ModelReadyRequest,
    ModelMetadataRequest,
    ModelInferRequest,
)


with grpc.insecure_channel("localhost:8081") as channel:
    client = GRPCInferenceServiceStub(channel)

    # Check that the server is live, and it has the iris model loaded
    client.ServerReady(ServerReadyRequest())
    client.ModelReady(ModelReadyRequest(name="iris-model"))

    # Make an inference request
    pred = client.ModelInfer(
        ModelInferRequest(
            model_name="iris-model",
            inputs=[
                {
                    "name": "input-0",
                    "datatype": "FP64",
                    "shape": [1, 4],
                    "contents": {"fp64_contents": [5.3, 3.7, 1.5, 0.2]},
                }
            ],
        )
    )

print(MessageToDict(pred))
# {
#     "modelName": "iris-model",
#     "parameters": {"content_type": {"stringParam": "np"}},
#     "outputs": [
#         {
#             "name": "output-1",
#             "datatype": "INT64",
#             "shape": ["1", "1"],
#             "parameters": {"content_type": {"stringParam": "np"}},
#             "contents": {"int64Contents": ["0"]},
#         }
#     ],
# }
```

<details><summary>Async versions of the same APIs are also available, use <code>grpc.aio</code> instead to create a channel then <code>await</code> and requests made.</summary>

```py
async with grpc.aio.insecure_channel('localhost:8081') as channel:
    stub = GRPCInferenceServiceStub(channel)
    await stub.ServerReady(ServerReadyRequest())
```

</details>

## Dependencies

The `open-inference-grpc` python package relies only on [`grpcio`](https://github.com/grpc/grpc), the underlying transport implementation of gRPC.

## Contribute

This client is largely generated automatically by [`grpc-tools`](https://grpc.io/docs/languages/python/quickstart/#generate-grpc-code), with a small amount of build post-processing in [build.py](https://github.com/open-inference/python-clients/blob/main/packages/open-inference-grpc/build.py).

> Run `python build.py` to build this package, it will:
>
> 1. If `proto/open_inference_grpc.proto` is not found, download it from [open-inference/open-inference-protocol/](https://github.com/open-inference/open-inference-protocol/blob/main/specification/protocol/open_inference_grpc.proto)
> 1. Run grpcio_tools.protoc to create the python client
> 1. Postprocess filenames and imports
> 1. Prepend the Apache 2.0 License preamble
> 1. Format with [black](https://github.com/psf/black)

If you want to contribute to the open-inference-protocol itself, please create an issue or PR in the [open-inference/open-inference-protocol](https://github.com/open-inference/open-inference-protocol) repository.

## License

By contributing to Open Inference Protocol Python client repository, you agree that your contributions will be licensed under its Apache 2.0 License.
