from __future__ import annotations

import base64
import time
from typing import Any

from rpi_client.config import RuntimeConfig
from rpi_client.mission.controller import MissionController
from rpi_client.safety.watchdog import SafetyWatchdog
from rpi_client.timing import elapsed_ms, log_timing, now
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
                loop_started_at = now()
                self._state.loop_count = loop_index
                print(f"[camera] capturing frame loop={loop_index}")
                capture_started_at = now()
                frame = self._camera.capture()
                log_timing(
                    self._config.timing_enabled,
                    "camera_capture",
                    elapsed_ms(capture_started_at),
                )
                print(
                    "[camera] captured source=%s size=%dx%d bytes=%s"
                    % (
                        frame.source,
                        frame.width,
                        frame.height,
                        frame.encoded_bytes if frame.encoded_bytes is not None else "unknown",
                    )
                )
                if self._config.debug_save_frame_path:
                    save_started_at = now()
                    image_bytes = base64.b64decode(frame.image_base64)
                    with open(self._config.debug_save_frame_path, "wb") as fp:
                        fp.write(image_bytes)
                    log_timing(
                        self._config.timing_enabled,
                        "debug_save_frame",
                        elapsed_ms(save_started_at),
                    )
                    print(
                        "[camera] saved debug frame path=%s bytes=%d"
                        % (self._config.debug_save_frame_path, len(image_bytes))
                    )
                vision_started_at = now()
                decision = self._vision_engine.analyze_frame(frame, mission, self._state)
                log_timing(
                    self._config.timing_enabled,
                    "vision_total",
                    elapsed_ms(vision_started_at),
                )
                decision = self._watchdog.validate(decision)
                self._mission_controller.record_action(mission, decision.action)
                self._state.last_action = decision.action

                print(
                    "[vision] source=%s action=%s found=%s reason=%s"
                    % (
                        frame.source,
                        decision.action.value,
                        decision.target_found,
                        decision.reason,
                    )
                )
                motor_started_at = now()
                self._motor_controller.execute(decision)
                log_timing(
                    self._config.timing_enabled,
                    "motor_execute",
                    elapsed_ms(motor_started_at),
                )
                log_timing(
                    self._config.timing_enabled,
                    f"loop_{loop_index}_total",
                    elapsed_ms(loop_started_at),
                )

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
