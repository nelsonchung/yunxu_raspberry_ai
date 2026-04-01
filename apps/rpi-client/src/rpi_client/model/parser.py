from __future__ import annotations

import json

from rpi_client.types import Action, VisionDecision


def decision_from_text(raw_text: str) -> VisionDecision:
    cleaned = raw_text.strip()

    try:
        payload = json.loads(cleaned)
        action = Action(payload.get("action", Action.STOP.value))
        return VisionDecision(
            action=action,
            duration_ms=int(payload.get("duration_ms", 500)),
            speed=float(payload.get("speed", 0.4)),
            reason=str(payload.get("reason", "json output parsed")),
            target_found=bool(payload.get("target_found", False)),
            raw_text=raw_text,
            raw_payload=payload,
        )
    except (json.JSONDecodeError, ValueError, TypeError):
        pass

    lowered = cleaned.lower()
    action = Action.STOP
    if "turn_left" in lowered or "turn left" in lowered or "left" in lowered:
        action = Action.TURN_LEFT
    elif "turn_right" in lowered or "turn right" in lowered or "right" in lowered:
        action = Action.TURN_RIGHT
    elif "forward" in lowered or "ahead" in lowered:
        action = Action.FORWARD
    elif "backward" in lowered or "reverse" in lowered:
        action = Action.BACKWARD
    elif "rotate" in lowered or "scan" in lowered or "search" in lowered:
        action = Action.ROTATE_SEARCH
    elif "stop" in lowered:
        action = Action.STOP
    elif "左轉" in cleaned or "向左" in cleaned:
        action = Action.TURN_LEFT
    elif "右轉" in cleaned or "向右" in cleaned:
        action = Action.TURN_RIGHT
    elif "前進" in cleaned or "往前" in cleaned or "直走" in cleaned:
        action = Action.FORWARD
    elif "後退" in cleaned or "倒退" in cleaned:
        action = Action.BACKWARD
    elif "旋轉搜尋" in cleaned or "搜尋" in cleaned or "掃描" in cleaned:
        action = Action.ROTATE_SEARCH
    elif "停止" in cleaned:
        action = Action.STOP

    target_found = (
        "found" in lowered
        or "target_found" in lowered
        or "找到" in cleaned
        or "已發現" in cleaned
    )
    return VisionDecision(
        action=action,
        duration_ms=500,
        speed=0.4,
        reason="由自由格式模型文字解析",
        target_found=target_found,
        raw_text=raw_text,
    )
