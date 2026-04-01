from __future__ import annotations

import json
import urllib.error
import urllib.request

from rpi_client.model.parser import decision_from_text
from rpi_client.types import Action, FrameCapture, Mission, RobotState, VisionDecision


class OllamaVisionEngine:
    def __init__(self, base_url: str, model: str) -> None:
        self._url = f"{base_url}/api/chat"
        self._model = model

    def analyze_frame(
        self,
        frame: FrameCapture,
        mission: Mission,
        state: RobotState,
    ) -> VisionDecision:
        prompt = self._build_prompt(mission=mission, state=state)
        payload = {
            "model": self._model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "images": [frame.image_base64],
                }
            ],
            "stream": False,
        }
        request = urllib.request.Request(
            self._url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            return VisionDecision(
                action=Action.STOP,
                duration_ms=0,
                speed=0.0,
                reason=f"ollama request failed: {exc}",
                raw_text=str(exc),
            )

        content = str(body.get("message", {}).get("content", "")).strip()
        decision = decision_from_text(content)
        decision.raw_payload = body
        return decision

    def _build_prompt(self, mission: Mission, state: RobotState) -> str:
        return (
            "You are controlling a small robot car that is searching for an object.\n"
            f"Mission goal: {mission.goal}\n"
            f"Previous action: {state.last_action.value}\n"
            f"Loop count: {state.loop_count}\n"
            "Look at the image and decide the next safe high-level action.\n"
            "Return only JSON with keys: "
            "action, duration_ms, speed, target_found, reason.\n"
            "Valid actions: forward, backward, turn_left, turn_right, "
            "rotate_search, stop, announce_found."
        )
