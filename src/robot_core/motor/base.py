from __future__ import annotations

from typing import Protocol

from ..types import VisionDecision


class MotorController(Protocol):
    def execute(self, decision: VisionDecision) -> None:
        """Execute a validated decision."""

    def stop(self) -> None:
        """Stop all motors safely."""
