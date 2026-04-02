from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class Action(str, Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    ROTATE_SEARCH = "rotate_search"
    STOP = "stop"
    ANNOUNCE_FOUND = "announce_found"


class MissionStatus(str, Enum):
    IDLE = "idle"
    SEARCHING = "searching"
    FOUND = "found"
    FAILED = "failed"


@dataclass
class RobotState:
    battery: float = 0.0
    last_action: Action = Action.STOP
    loop_count: int = 0


@dataclass
class Mission:
    mission_id: str
    goal: str
    status: MissionStatus = MissionStatus.IDLE
    history: list[Action] = field(default_factory=list)


@dataclass
class FrameCapture:
    image_base64: str
    width: int
    height: int
    source: str
    encoded_bytes: Optional[int] = None


@dataclass
class VisionDecision:
    action: Action
    duration_ms: int
    speed: float
    reason: str
    target_found: bool = False
    raw_text: str = ""
    raw_payload: Optional[dict[str, Any]] = None
