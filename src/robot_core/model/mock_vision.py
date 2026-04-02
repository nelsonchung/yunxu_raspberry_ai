from __future__ import annotations

from ..types import Action, FrameCapture, Mission, RobotState, VisionDecision


class MockVisionEngine:
    def analyze_frame(
        self,
        frame: FrameCapture,
        mission: Mission,
        state: RobotState,
    ) -> VisionDecision:
        if state.loop_count >= 4:
            return VisionDecision(
                action=Action.ANNOUNCE_FOUND,
                duration_ms=0,
                speed=0.0,
                reason=f"mock target found for goal '{mission.goal}'",
                target_found=True,
                raw_text="mock target found",
            )

        sequence = [
            Action.ROTATE_SEARCH,
            Action.TURN_LEFT,
            Action.FORWARD,
            Action.TURN_RIGHT,
        ]
        action = sequence[state.loop_count % len(sequence)]
        return VisionDecision(
            action=action,
            duration_ms=500,
            speed=0.35,
            reason=f"mock step from {frame.source}",
            raw_text=f"mock action: {action.value}",
        )

    def describe_frame(self, frame: FrameCapture, prompt: str) -> str:
        return (
            "這是 mock 圖片解讀模式。"
            f" 目前影像來源是 {frame.source}，解析度為 {frame.width}x{frame.height}。"
            f" 你提供的提示是：{prompt}"
        )
