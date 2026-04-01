# Integration Contract

## Purpose

這份文件不再描述自訂的 client/server API，而是定義 Raspberry Pi 主程式內部各模組之間，以及 Pi 與 Ollama 之間應遵守的資料邊界。

## Main Boundaries

### 1. Mission Input

任務來源可以是：

- 麥克風語音
- SSH 登入後由 CLI 輸入文字
- 預設啟動任務

### 2. Vision Request

Pi 會把縮圖與任務提示送到模型層。模型層可以是：

- Raspberry Pi 本機模型
- MacBook 上的 Ollama
- 未來替換成其他模型主機

### 3. Action Command

不論模型回傳什麼自由文字，真正交給馬達控制器的都必須是受限命令。

## Core Entities

### Mission

```json
{
  "mission_id": "mission-001",
  "goal": "find toy",
  "status": "searching"
}
```

### Frame Analysis Request

```json
{
  "mission_id": "mission-001",
  "timestamp": "2026-04-01T12:00:00+08:00",
  "image_base64": "<base64-jpeg>",
  "robot_state": {
    "battery": 7.6,
    "last_action": "turn_left"
  },
  "goal": "find toy"
}
```

### Model Output

模型原始輸出可以先保留文字格式，讓 adapter 做解析：

```json
{
  "raw_text": "I do not see the toy clearly. Turn left slightly and continue scanning."
}
```

### Parsed Action

```json
{
  "mission_id": "mission-001",
  "action": "turn_left",
  "duration_ms": 500,
  "speed": 0.45,
  "reason": "continue scanning left",
  "target_found": false
}
```

### Motor Command

```json
{
  "action": "turn_left",
  "left_pwm": 0.2,
  "right_pwm": 0.45,
  "duration_ms": 500
}
```

## Suggested Actions

請把決策層的輸出限制在固定集合：

- `forward`
- `backward`
- `turn_left`
- `turn_right`
- `rotate_search`
- `stop`
- `announce_found`

這樣馬達層只要做 deterministic control，不需要相信模型的自由文字。

## Suggested Internal Interfaces

### Mission Controller

```python
mission = controller.start_mission(goal="find toy")
```

### Vision Engine

```python
result = vision_engine.analyze_frame(
    image_base64=frame_b64,
    goal="find toy",
    robot_state=state,
)
```

### Action Mapper

```python
action = action_mapper.from_model_output(result)
```

### Motor Controller

```python
motor_controller.execute(action)
```

## Validation Rules

模型輸出一定要經過本地驗證層：

1. 檢查 action 是否在允許集合內
2. 檢查 speed / duration 是否在安全範圍
3. 驗證失敗時回傳 `stop`
4. 模型逾時時回傳 `stop`

## SSH-Based Development Workflow

平常開發與操作流程：

1. 使用 MacBook 透過 SSH 連到 Raspberry Pi
2. 在 Pi 上啟動主程式
3. 觀察本地日誌、影像結果與馬達反應
4. 需要時修改設定，例如模型位址、相機解析度、搜尋模式

## Logging

每次決策至少記錄：

- 收到的 mission
- 使用的圖片檔名或摘要
- 模型原始輸出
- 解析後動作
- 最終執行結果

這會非常有助於之後調 prompt 與追查誤判。
