from datetime import date
from textwrap import dedent
import itertools
import os
import pathlib
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
    print("> Run fern, waiting...")

    input("Press Enter to continue...")


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
    
    
    prepend_apache_license(outputpath)
    format_generated_files(outputpath)
    add_py_typed(outputpath)
