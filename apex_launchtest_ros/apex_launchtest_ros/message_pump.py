# Copyright 2019 Apex.AI, Inc.
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

import threading

import rclpy


class MessagePump:
    """Calls rclpy.spin on a thread so tests don't need to."""

    def __init__(self, node):
        self._node = node
        self._thread = threading.Thread(
            target=self._run,
            name="msg_pump_thread",
        )
        self._run = True

    def start(self):
        self._thread.start()

    def stop(self):
        self._run = False
        self._thread.join(timeout=5.0)
        if self._thread.is_alive():
            raise Exception("Timed out waiting for message pump to stop")

    def _run(self):
        while self._run:
            rclpy.spin_once(self._node, timeout_sec=1.0)
