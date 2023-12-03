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


class ApiError(Exception):
    status_code: typing.Optional[int]
    body: typing.Any

    def __init__(self, *, status_code: typing.Optional[int] = None, body: typing.Any = None):
        self.status_code = status_code
        self.body = body

    def __str__(self) -> str:
        return f"status_code: {self.status_code}, body: {self.body}"