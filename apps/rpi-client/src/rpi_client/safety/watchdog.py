from __future__ import annotations

from rpi_client.types import Action, VisionDecision


class SafetyWatchdog:
    def validate(self, decision: VisionDecision) -> VisionDecision:
        if decision.speed < 0:
            decision.speed = 0.0
        if decision.speed > 1.0:
            decision.speed = 1.0
        if decision.duration_ms < 0:
            decision.duration_ms = 0
        if decision.duration_ms > 3_000:
            decision.duration_ms = 3_000
        if decision.action == Action.ANNOUNCE_FOUND:
            decision.speed = 0.0
            decision.duration_ms = 0
        return decision
