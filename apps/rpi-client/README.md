# rpi-client

Raspberry Pi 端是整個專案的主執行程式，負責所有硬體互動、本地安全控制、任務狀態，以及模型整合。

## Responsibilities

- 擷取相機畫面
- 收麥克風音訊
- 播放 TTS 或提示音
- 控制 GPIO / PWM 馬達
- 管理 mission / search loop
- 呼叫本機或遠端模型
- 將高階動作轉成底層控制

## Suggested Internal Modules

```text
src/rpi_client/
├── audio/
├── camera/
├── mission/
├── model/
├── motor/
├── network/
└── safety/
```

## Current Bootstrap

目前已經有第一版可執行骨架：

- `rpi_client.main`
  - 主程式入口
- `rpi_client.runtime`
  - search loop
- `rpi_client.camera`
  - `mock`、`file` 與 `pi` 相機來源
- `rpi_client.model`
  - `mock` 與 `ollama` 模型 adapter
- `rpi_client.motor`
  - mock 馬達控制器
- `rpi_client.safety`
  - 基本動作驗證

## Run

在 repo 根目錄可先用 mock 模式驗證流程：

```bash
./scripts/start_rpi_client.sh --goal "find toy"
```

如果要改用本機圖片測試：

```bash
./scripts/start_rpi_client.sh \
  --camera-mode file \
  --sample-image-path /absolute/path/to/image.jpg
```

如果是在 Raspberry Pi 上使用 CSI camera interface 攝影機，建議用 `Picamera2 + OpenCV`：

```bash
sudo apt install -y python3-picamera2 python3-opencv

./scripts/start_rpi_client.sh \
  --camera-mode pi \
  --camera-width 640 \
  --camera-height 480
```

如果 Raspberry Pi 要直接呼叫區網中的 Ollama：

```bash
./scripts/start_rpi_client.sh \
  --model-mode ollama \
  --camera-mode pi \
  --camera-width 640 \
  --camera-height 480 \
  --ollama-base-url http://192.168.8.166:11434 \
  --ollama-model qwen3.5:2b
```

目前專案預設的遠端模型設定也是：

- `OLLAMA_BASE_URL=http://192.168.8.166:11434`
- `OLLAMA_MODEL=qwen3.5:2b`

## Important Rules

1. Pi 端是主控制器，但模型輸出仍然要經過本地驗證。
2. Pi 端只允許有限動作命令進入馬達層。
3. 模型逾時或解析失敗時，預設停止。
4. 馬達控制一定要有 timeout。
