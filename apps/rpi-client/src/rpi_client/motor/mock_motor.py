from __future__ import annotations

from rpi_client.types import VisionDecision


class MockMotorController:
    def execute(self, decision: VisionDecision) -> None:
        print(
            "[motor] action=%s speed=%.2f duration_ms=%d reason=%s"
            % (
                decision.action.value,
                decision.speed,
                decision.duration_ms,
                decision.reason,
            )
        )

    def stop(self) -> None:
        print("[motor] stop")
