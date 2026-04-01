from __future__ import annotations

from typing import Protocol

from rpi_client.types import FrameCapture


class CameraProvider(Protocol):
    def capture(self) -> FrameCapture:
        """Capture a frame for the search loop."""
