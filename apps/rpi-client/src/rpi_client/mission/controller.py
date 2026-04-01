from __future__ import annotations

from dataclasses import dataclass
from itertools import count

from rpi_client.types import Action, Mission, MissionStatus


@dataclass
class MissionController:
    _counter: count = count(1)

    def start_mission(self, goal: str) -> Mission:
        mission = Mission(
            mission_id=f"mission-{next(self._counter):03d}",
            goal=goal,
            status=MissionStatus.SEARCHING,
        )
        return mission

    def record_action(self, mission: Mission, action: Action) -> None:
        mission.history.append(action)

    def mark_found(self, mission: Mission) -> None:
        mission.status = MissionStatus.FOUND

    def mark_failed(self, mission: Mission) -> None:
        mission.status = MissionStatus.FAILED
