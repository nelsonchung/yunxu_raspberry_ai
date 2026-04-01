from __future__ import annotations

import base64
import time

try:
    import cv2
except ImportError as exc:  # pragma: no cover
    cv2 = None
    _CV2_IMPORT_ERROR = exc
else:
    _CV2_IMPORT_ERROR = None

try:
    from picamera2 import Picamera2
except ImportError as exc:  # pragma: no cover
    Picamera2 = None
    _PICAMERA2_IMPORT_ERROR = exc
else:
    _PICAMERA2_IMPORT_ERROR = None

from rpi_client.types import FrameCapture


class PiCamera:
    def __init__(
        self,
        width: int = 640,
        height: int = 480,
        warmup_s: float = 1.5,
        jpeg_quality: int = 85,
    ) -> None:
        if Picamera2 is None:
            raise RuntimeError(
                "picamera2 is not installed. On Raspberry Pi OS, run: "
                "sudo apt install -y python3-picamera2"
            ) from _PICAMERA2_IMPORT_ERROR
        if cv2 is None:
            raise RuntimeError(
                "opencv is not installed. On Raspberry Pi OS, run: "
                "sudo apt install -y python3-opencv"
            ) from _CV2_IMPORT_ERROR

        self._width = width
        self._height = height
        self._jpeg_quality = max(1, min(jpeg_quality, 100))
        self._camera = Picamera2()
        self._camera.configure(
            self._camera.create_preview_configuration(
                main={"size": (width, height), "format": "RGB888"}
            )
        )
        self._camera.start()
        time.sleep(max(0.0, warmup_s))

    def capture(self) -> FrameCapture:
        frame_rgb = self._camera.capture_array()
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        ok, encoded = cv2.imencode(
            ".jpg",
            frame_bgr,
            [int(cv2.IMWRITE_JPEG_QUALITY), self._jpeg_quality],
        )
        if not ok:
            raise RuntimeError("failed to encode camera frame as JPEG")
        image_b64 = base64.b64encode(encoded.tobytes()).decode("utf-8")
        return FrameCapture(
            image_base64=image_b64,
            width=self._width,
            height=self._height,
            source="pi-camera",
            encoded_bytes=len(encoded.tobytes()),
        )

    def close(self) -> None:
        self._camera.close()
