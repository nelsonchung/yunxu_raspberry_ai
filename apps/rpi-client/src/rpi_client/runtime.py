from __future__ import annotations

import time
from typing import Any

from rpi_client.config import RuntimeConfig
from rpi_client.mission.controller import MissionController
from rpi_client.safety.watchdog import SafetyWatchdog
from rpi_client.types import Action, RobotState


class SearchRuntime:
    def __init__(self, config, camera, vision_engine, motor_controller) -> None:
        self._config: RuntimeConfig = config
        self._camera: Any = camera
        self._vision_engine = vision_engine
        self._motor_controller = motor_controller
        self._mission_controller = MissionController()
        self._watchdog = SafetyWatchdog()
        self._state = RobotState()

    def run(self) -> int:
        mission = self._mission_controller.start_mission(self._config.goal)
        print(f"[mission] started {mission.mission_id} goal={mission.goal!r}")

        try:
            for loop_index in range(self._config.max_iterations):
                self._state.loop_count = loop_index
                frame = self._camera.capture()
                decision = self._vision_engine.analyze_frame(frame, mission, self._state)
                decision = self._watchdog.validate(decision)
                self._mission_controller.record_action(mission, decision.action)
                self._state.last_action = decision.action

                print(
                    "[vision] source=%s action=%s found=%s"
                    % (frame.source, decision.action.value, decision.target_found)
                )
                self._motor_controller.execute(decision)

                if decision.target_found or decision.action == Action.ANNOUNCE_FOUND:
                    self._mission_controller.mark_found(mission)
                    print(f"[mission] target found for {mission.goal!r}")
                    return 0

                time.sleep(self._config.loop_interval_s)

            self._mission_controller.mark_failed(mission)
            print(f"[mission] max iterations reached for {mission.goal!r}")
            return 0
        finally:
            self._motor_controller.stop()
            if hasattr(self._camera, "close"):
                self._camera.close()
