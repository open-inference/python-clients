from datetime import date
from textwrap import dedent
import itertools
import os
import pathlib
import subprocess
import sys
import urllib.request

import black

PROTO_URL = os.environ.get(
    "PROTO_URL",
    "https://raw.githubusercontent.com/open-inference/open-inference-protocol/main/specification/protocol/open_inference_rest.yaml",
)


def maybe_download_proto(protopath: pathlib.Path) -> None:
    if (protopath / "open_inference_rest.yaml").exists():
        print(f"> Protocol definition found ({protopath / 'open_inference_rest.yaml'})")
    else:
        print(
            f"> Protocol definition not found ({protopath / 'open_inference_rest.yaml'})"
        )
        print(f"> Downloading protocol definition from {PROTO_URL}")
        urllib.request.urlretrieve(PROTO_URL, protopath / "open_inference_rest.yaml")


def build_client() -> None:
    print("> Running fern")

    result = subprocess.run(["fern", "generate"])

    if result.returncode != 0:
        sys.exit(result.returncode)


def patch_recursive_tensor(outputpath: pathlib.Path) -> None:
    print(
        f"> Replacing recursive tensor type in {outputpath / 'open_inference_rest.py'}"
    )

    (outputpath / "types" / "tensor_data.py").write_text(
        dedent(
            """
            from __future__ import annotations
            import typing

            try:
                import pydantic.v1 as pydantic  # type: ignore
            except ImportError:
                import pydantic  # type: ignore


            class TensorData(pydantic.BaseModel):
                __root__: typing.List[typing.Union[TensorData, float, str, bool]]

            """
        )
    )

    # Remove TensorDataItem, along with its exports
    (outputpath / "types" / "tensor_data_item.py").unlink()
    (outputpath / "types" / "__init__.py").write_text(
        (outputpath / "types" / "__init__.py")
        .read_text()
        .replace("from .tensor_data_item import TensorDataItem\n", "")
        .replace('    "TensorDataItem",\n', "")
    )

    (outputpath / "__init__.py").write_text(
        (outputpath / "__init__.py")
        .read_text()
        .replace("    TensorDataItem,\n", "")
        .replace('    "TensorDataItem",\n', "")
    )


def patch_remove_hardcoded_timeouts(outputpath: pathlib.Path) -> None:
    for path in itertools.chain(
        outputpath.glob("**/*.py"),
        outputpath.glob("**/*.pyi"),
    ):
        if "timeout=60," in path.read_text():
            print(f"> Removing hardcoded timeouts: {path}")
            path.write_text(path.read_text().replace("timeout=60,", ""))


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

    protopath = this_dir / "fern" / "openapi"
    protopath.mkdir(parents=True, exist_ok=True)
    outputpath = this_dir / "generated" / "open_inference" / "openapi"

    maybe_download_proto(protopath)
    build_client()
    patch_recursive_tensor(outputpath)
    patch_remove_hardcoded_timeouts(outputpath)
    prepend_apache_license(outputpath)
    format_generated_files(outputpath)
    add_py_typed(outputpath)
