from __future__ import annotations

from typing import Protocol

from ..types import FrameCapture


class CameraProvider(Protocol):
    def capture(self) -> FrameCapture:
        """Capture a frame for the search loop."""
