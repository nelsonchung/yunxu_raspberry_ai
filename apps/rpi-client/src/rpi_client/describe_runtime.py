from __future__ import annotations

import base64
from typing import Any

from rpi_client.config import RuntimeConfig


class DescribeRuntime:
    def __init__(self, config, camera, vision_engine) -> None:
        self._config: RuntimeConfig = config
        self._camera: Any = camera
        self._vision_engine = vision_engine

    def run(self) -> int:
        try:
            print("[describe] capturing a single frame")
            frame = self._camera.capture()
            print(
                "[camera] captured source=%s size=%dx%d bytes=%s"
                % (
                    frame.source,
                    frame.width,
                    frame.height,
                    frame.encoded_bytes if frame.encoded_bytes is not None else "unknown",
                )
            )
            if self._config.debug_save_frame_path:
                image_bytes = base64.b64decode(frame.image_base64)
                with open(self._config.debug_save_frame_path, "wb") as fp:
                    fp.write(image_bytes)
                print(
                    "[camera] saved debug frame path=%s bytes=%d"
                    % (self._config.debug_save_frame_path, len(image_bytes))
                )

            print("[describe] prompt=%s" % self._config.describe_prompt)
            if hasattr(self._vision_engine, "describe_frame"):
                result = self._vision_engine.describe_frame(
                    frame=frame,
                    prompt=self._config.describe_prompt,
                )
            else:
                result = "目前的模型後端不支援圖片解讀模式。"

            print("[describe] result:")
            print(result)
            return 0
        finally:
            if hasattr(self._camera, "close"):
                self._camera.close()
