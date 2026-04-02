from __future__ import annotations

import base64
from typing import Any

from .config import RuntimeConfig
from .timing import elapsed_ms, log_timing, now


class DescribeRuntime:
    def __init__(self, config, camera, vision_engine) -> None:
        self._config: RuntimeConfig = config
        self._camera: Any = camera
        self._vision_engine = vision_engine

    def run(self) -> int:
        try:
            total_started_at = now()
            print("[describe] capturing a single frame")
            capture_started_at = now()
            frame = self._camera.capture()
            log_timing(
                self._config.timing_enabled,
                "camera_capture",
                elapsed_ms(capture_started_at),
            )
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
                save_started_at = now()
                image_bytes = base64.b64decode(frame.image_base64)
                with open(self._config.debug_save_frame_path, "wb") as fp:
                    fp.write(image_bytes)
                log_timing(
                    self._config.timing_enabled,
                    "debug_save_frame",
                    elapsed_ms(save_started_at),
                )
                print(
                    "[camera] saved debug frame path=%s bytes=%d"
                    % (self._config.debug_save_frame_path, len(image_bytes))
                )

            print("[describe] prompt=%s" % self._config.describe_prompt)
            if hasattr(self._vision_engine, "describe_frame"):
                describe_started_at = now()
                result = self._vision_engine.describe_frame(
                    frame=frame,
                    prompt=self._config.describe_prompt,
                )
                log_timing(
                    self._config.timing_enabled,
                    "describe_total",
                    elapsed_ms(describe_started_at),
                )
            else:
                result = "目前的模型後端不支援圖片解讀模式。"

            print("[describe] result:")
            print(result)
            log_timing(
                self._config.timing_enabled,
                "describe_run_total",
                elapsed_ms(total_started_at),
            )
            return 0
        finally:
            if hasattr(self._camera, "close"):
                self._camera.close()
