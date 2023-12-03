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

from ..core.api_error import ApiError


class InternalServerError(ApiError):
    def __init__(self, body: typing.Any):
        super().__init__(status_code=500, body=body)
