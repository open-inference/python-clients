import importlib.resources
import itertools
import os
import pathlib
import sys
import urllib.request
from textwrap import dedent
from datetime import date

import black
import grpc_tools.protoc

PROTO_URL = os.environ.get(
    "PROTO_URL",
    "https://raw.githubusercontent.com/open-inference/open-inference-protocol/main/specification/protocol/open_inference_grpc.proto",
)


def maybe_download_proto(protopath: pathlib.Path) -> None:
    if (protopath / "open_inference_grpc.proto").exists():
        print(f"> Protocol definition found ({protopath / 'open_inference_grpc.proto'})")
    else:
        print(f"> Protocol definition not found ({protopath / 'open_inference_grpc.proto'})")
        print(f"> Downloading protocol definition from {PROTO_URL}")
        urllib.request.urlretrieve(PROTO_URL, protopath / "open_inference_grpc.proto")


def compile_grpc(protopath: pathlib.Path, outputpath: pathlib.Path) -> None:
    print("> Compiling gRPC stubs")
    proto_include = importlib.resources.files("grpc_tools") / "_proto"

    exit_code = grpc_tools.protoc.main(
        [
            "grpc_tools.protoc",
            f"--proto_path={protopath}",
            f"--proto_path={proto_include}",
            f"--python_out={outputpath}",
            f"--pyi_out={outputpath}",
            f"--grpc_python_out={outputpath}",
            "open_inference_grpc.proto",
        ]
    )

    if exit_code != 0:
        sys.exit(exit_code)


def rename_built_files(outputpath: pathlib.Path) -> None:
    for source, target in {
        outputpath / "open_inference_grpc_pb2_grpc.py": outputpath / "service.py",
        outputpath / "open_inference_grpc_pb2.py": outputpath / "protocol.py",
        outputpath / "open_inference_grpc_pb2.pyi": outputpath / "protocol.pyi",
    }.items():
        print(f"> Moving {source} to {target}")
        os.rename(source, target)


def patch_module_import(outputpath: pathlib.Path) -> None:
    print(f"> Patching import of 'open_inference.grpc' in {outputpath / 'service.py'}")
    service_content = (outputpath / "service.py").read_text()
    service_content = service_content.replace(
        "import open_inference_grpc_pb2",
        "import open_inference.grpc.protocol",
    )
    (outputpath / "service.py").write_text(service_content)


def prepend_apache_license(outputpath: pathlib.Path) -> None:
    for path in itertools.chain(
        outputpath.glob("**/*.py"),
        outputpath.glob("**/*.pyi"),
    ):
        print(f"> Prepending Apache License to {path}")
        path.write_text(
            dedent(
                f"""
                # Copyright {date.today().year} The Open Inference Protocol Working Group
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

                """
            )
            + path.read_text()
        )


def format_generated_files(outputpath: pathlib.Path) -> None:
    for path in itertools.chain(
        outputpath.glob("**/*.py"),
        outputpath.glob("**/*.pyi"),
    ):
        print(f"> Formatting generated code: {path}")
        black.format_file_in_place(
            path,
            fast=False,
            mode=black.FileMode(
                line_length=120,
            ),
            write_back=black.WriteBack.YES,
        )


def add_py_typed(outputpath: pathlib.Path) -> None:
    print(f"> Adding {outputpath / 'py.typed'}")
    (outputpath / "py.typed").touch()


if __name__ == "__main__":
    this_dir = pathlib.Path(__file__).parent

    protopath = this_dir / "proto"
    protopath.mkdir(parents=True, exist_ok=True)
    outputpath = this_dir / "generated" / "open_inference" / "grpc"

    maybe_download_proto(protopath)
    compile_grpc(protopath, outputpath)
    rename_built_files(outputpath)
    patch_module_import(outputpath)
    prepend_apache_license(outputpath)
    format_generated_files(outputpath)
    add_py_typed(outputpath)
