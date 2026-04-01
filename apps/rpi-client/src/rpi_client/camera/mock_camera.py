from __future__ import annotations

from rpi_client.types import FrameCapture


# Tiny transparent PNG for dry-run bootstrapping.
_MOCK_IMAGE_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8"
    "/w8AAgMBgN6iQ0sAAAAASUVORK5CYII="
)


class MockCamera:
    def capture(self) -> FrameCapture:
        return FrameCapture(
            image_base64=_MOCK_IMAGE_B64,
            width=1,
            height=1,
            source="mock-camera",
        )
