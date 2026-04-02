from __future__ import annotations

import base64
from pathlib import Path

from ..types import FrameCapture


class FileCamera:
    def __init__(self, image_path: str) -> None:
        self._path = Path(image_path)
        if not self._path.exists():
            raise FileNotFoundError(f"Sample image not found: {self._path}")

    def capture(self) -> FrameCapture:
        image_bytes = self._path.read_bytes()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        return FrameCapture(
            image_base64=image_b64,
            width=640,
            height=480,
            source=str(self._path),
            encoded_bytes=len(image_bytes),
        )
