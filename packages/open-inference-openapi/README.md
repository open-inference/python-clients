# Open Inference Protocol OpenAPI Client

<p>
<a href="https://pypi.org/project/open-inference-openapi/">
    <img src="https://badge.fury.io/py/open-inference-openapi.svg" alt="Package version">
</a>
</p>

`open-inference-openapi` is a generated client library based on the OpenAPI protocol definition tracked in the [open-inference/open-inference-protocol/](https://github.com/open-inference/open-inference-protocol/blob/main/specification/protocol/open_inference_rest.yaml) repository.

---

## Installation

This package requires Python 3.8 or greater.

Install with your favorite tool from pypi.org/project/open-inference-openapi/

```console
$ pip install open-inference-openapi
$ poetry add open-inference-openapi
```

> A gRPC-based python client ([`open-inference-grpc`](https://pypi.org/project/open-inference-grpc)) also exists for the Open Inference Protocol, and can be installed alongside this gRPC client, as both are distributed as [namespace packages](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/#packaging-namespace-packages).

## Example

```python
from open_inference.openapi.client import OpenInferenceClient, InferenceRequest

client = OpenInferenceClient(base_url='http://localhost:5002')

# Check that the server is live, and it has the iris model loaded
client.check_server_readiness()
client.read_model_metadata('mlflow-model')

# Make an inference request with two examples
pred = client.model_infer(
    "mlflow-model",
    request=InferenceRequest(
        inputs=[
            {
                "name": "input",
                "shape": [2, 4],
                "datatype": "FP64",
                "data": [
                    [5.0, 3.3, 1.4, 0.2],
                    [7.0, 3.2, 4.7, 1.4],
                ],
            }
        ]
    ),
)

print(repr(pred))
# InferenceResponse(
#     model_name="mlflow-model",
#     model_version=None,
#     id="580c30e3-f835-418f-bb17-a3074d42ad21",
#     parameters={"content_type": "np", "headers": None},
#     outputs=[
#         ResponseOutput(
#             name="output-1",
#             shape=[2, 1],
#             datatype="INT64",
#             parameters={"content_type": "np", "headers": None},
#             data=TensorData(__root__=[0.0, 1.0]),
#         )
#     ],
# )
```

<details><summary>Async versions of the same APIs are also available. Import <code>AsyncOpenInfereClient</code> instead, then <code>await</code> and requests made.</summary>

```py
from open_inference.openapi.client import AsyncOpenInferenceClient

client = AsyncOpenInferenceClient(base_url="http://localhost:5002")
await client.check_server_readiness()
```

</details>

## Dependencies

The `open-inference-openapi` python package relies on:

- [`pydantic`](https://github.com/pydantic/pydantic) - Message formatting, structure, and validation.
- [`httpx`](https://github.com/encode/httpx/) - Implementation of the underlying HTTP transport.

## Contribute

This client is largely generated automatically by [`fern`](https://github.com/fern-api/fern), with a small amount of build post-processing in [build.py](https://github.com/open-inference/python-clients/blob/main/packages/open-inference-grpc/build.py).

> Run `python build.py` to build this package, it will:
>
> 1. If `fern/openapi/open_inference_rest.yaml` is not found, download it from [open-inference/open-inference-protocol/](https://github.com/open-inference/open-inference-protocol/blob/main/specification/protocol/open_inference_rest.yaml)
> 1. Run `fern generate` to create the python client (fern-api must be installed `npm install --global fern-api`)
> 1. Postprocess to correctly implement the recursive TensorData model.
> 1. Prepend the Apache 2.0 License preamble
> 1. Format with [black](https://github.com/psf/black)

If you want to contribute to the open-inference-protocol itself, please create an issue or PR in the [open-inference/open-inference-protocol](https://github.com/open-inference/open-inference-protocol) repository.

## License

By contributing to Open Inference Protocol Python client repository, you agree that your contributions will be licensed under its Apache 2.0 License.
