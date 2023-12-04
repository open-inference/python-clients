# Open Inference Protocol Client Libraries

<p>
<a href="https://pypi.org/project/open-inference-openapi/"><img src="https://badge.fury.io/py/open-inference-openapi.svg" alt="Package version"></a>
<a href="https://pypi.org/project/open-inference-grpc/"><img src="https://badge.fury.io/py/open-inference-grpc.svg" alt="Package version"></a>
</p>

Generated Python client libraries for the Open Inference Protocol using protocol definitions tracked in the [open-inference/open-inference-protocol/](https://github.com/open-inference/open-inference-protocol) repository.

---

This repository contains generated Python source code and build scripts for Open Inference Protocol client code as two separate [PEP-420 namespace packages](https://peps.python.org/pep-0420/). The Open Inference Protocol has OpenAPI and gRPC specifications, and are installable independently of each other - choose the preferred transport mechanism for your application.

## OpenAPI implementation `open_inference.openapi`

```shell
pip install open-inference-openapi
```

<details>
<summary>Install from GitHub</summary>

```shell
pip install 'open-inference-openapi @ git+https://git@github.com/open-inference/python-clients@openapi/v2.0.0#subdirectory=packages/open-inference-openapi'
```

</details>

See [packages/open-inference-openapi](./packages/open-inference-openapi/README.md)

## gRPC Implementation `open_inference.grpc`

```shell
pip install open-inference-grpc
```

<details>
<summary>Install from GitHub</summary>

```shell
pip install 'open-inference-grpc @ git+https://git@github.com/open-inference/python-clients@grpc/v2.0.0#subdirectory=packages/open-inference-grpc'
```

</details>

See [packages/open-inference-grpc](./packages/open-inference-grpc/README.md)
