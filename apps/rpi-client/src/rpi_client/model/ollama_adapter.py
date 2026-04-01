from __future__ import annotations

import json
import socket
import urllib.error
import urllib.request

from rpi_client.model.parser import decision_from_text
from rpi_client.types import Action, FrameCapture, Mission, RobotState, VisionDecision


class OllamaVisionEngine:
    def __init__(self, base_url: str, model: str, timeout_s: float = 90.0) -> None:
        self._url = f"{base_url}/api/chat"
        self._model = model
        self._timeout_s = timeout_s

    def analyze_frame(
        self,
        frame: FrameCapture,
        mission: Mission,
        state: RobotState,
    ) -> VisionDecision:
        prompt = self._build_search_prompt(mission=mission, state=state)
        try:
            content, body = self._chat_with_image(frame=frame, prompt=prompt)
        except (TimeoutError, socket.timeout) as exc:
            return VisionDecision(
                action=Action.STOP,
                duration_ms=0,
                speed=0.0,
                reason=f"ollama request timed out after {self._timeout_s:.0f}s: {exc}",
                raw_text=str(exc),
            )
        except urllib.error.URLError as exc:
            return VisionDecision(
                action=Action.STOP,
                duration_ms=0,
                speed=0.0,
                reason=f"ollama request failed: {exc}",
                raw_text=str(exc),
            )
        decision = decision_from_text(content)
        decision.raw_payload = body
        return decision

    def describe_frame(self, frame: FrameCapture, prompt: str) -> str:
        content, _ = self._chat_with_image(frame=frame, prompt=prompt)
        return content

    def _chat_with_image(self, frame: FrameCapture, prompt: str):
        print(
            "[ollama] sending request url=%s model=%s image=%dx%d bytes=%s"
            % (
                self._url,
                self._model,
                frame.width,
                frame.height,
                frame.encoded_bytes if frame.encoded_bytes is not None else "unknown",
            )
        )
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
        with urllib.request.urlopen(request, timeout=self._timeout_s) as response:
            body = json.loads(response.read().decode("utf-8"))
        content = str(body.get("message", {}).get("content", "")).strip()
        print("[ollama] response received chars=%d" % len(content))
        return content, body

    def _build_search_prompt(self, mission: Mission, state: RobotState) -> str:
        return (
            "你正在控制一台小型機器車搜尋目標物。\n"
            f"任務目標: {mission.goal}\n"
            f"上一個動作: {state.last_action.value}\n"
            f"迴圈次數: {state.loop_count}\n"
            "請根據圖片判斷下一個安全的高階動作。\n"
            "請只回傳 JSON，不要加任何額外說明、Markdown 或程式碼區塊。\n"
            "JSON 必須包含以下欄位: "
            "action, duration_ms, speed, target_found, reason。\n"
            "action 必須只能使用以下英文值之一: "
            "forward, backward, turn_left, turn_right, rotate_search, stop, announce_found。\n"
            "duration_ms 必須是整數，speed 必須是 0 到 1 之間的小數，"
            "target_found 必須是 true 或 false。\n"
            "reason 必須使用繁體中文，簡短說明你為什麼選這個動作。"
        )
