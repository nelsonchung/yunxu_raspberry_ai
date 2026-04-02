from __future__ import annotations

from typing import Protocol

from ..types import FrameCapture, Mission, RobotState, VisionDecision


class VisionEngine(Protocol):
    def analyze_frame(
        self,
        frame: FrameCapture,
        mission: Mission,
        state: RobotState,
    ) -> VisionDecision:
        """Analyze a frame and suggest the next action."""
