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
- `rpi_client.describe_runtime`
  - 拍一張照並請模型解讀圖片
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

## Config

專案現在支援分層設定，建議不要直接改腳本內容。

優先順序：

1. CLI 參數
2. 環境變數
3. `config/user.toml`
4. `config/defaults.toml`
5. 程式內建 fallback

建議做法：

1. 先查看 [defaults.toml](/Users/nelsonchung/development/yunxu_raspberry_ai/config/defaults.toml)
2. 複製 [user.toml.example](/Users/nelsonchung/development/yunxu_raspberry_ai/config/user.toml.example) 成 `config/user.toml`
3. 把你常用的解析度、Ollama 位址、模型名稱寫進 `config/user.toml`
4. 需要單次覆寫時，再用 CLI 參數修改

如果要指定不同的設定檔：

```bash
./scripts/start_rpi_client.sh \
  --config-file /absolute/path/to/defaults.toml \
  --user-config-file /absolute/path/to/user.toml
```

如果要忽略使用者設定檔：

```bash
./scripts/start_rpi_client.sh --no-user-config
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
  --ollama-model qwen3.5:2b \
  --ollama-timeout 180 \
  --debug-save-frame-path /tmp/latest-frame.jpg
```

如果你要觀測效能，可加上：

```bash
./scripts/start_rpi_client.sh \
  --camera-mode pi \
  --model-mode ollama \
  --timing
```

會額外輸出像這些資訊：

- `camera_capture`
- `debug_save_frame`
- `ollama_roundtrip`
- `vision_total`
- `motor_execute`
- `loop_0_total`
- `describe_run_total`

如果你要使用「拍一張照，然後請 LLM 解讀圖片」模式：

```bash
./scripts/start_rpi_client.sh \
  --app-mode describe \
  --camera-mode pi \
  --camera-width 640 \
  --camera-height 480 \
  --model-mode ollama \
  --ollama-base-url http://192.168.8.166:11434 \
  --ollama-model qwen3.5:2b \
  --ollama-timeout 180 \
  --debug-save-frame-path /tmp/latest-frame.jpg \
  --describe-prompt "請用繁體中文解讀這張圖片，描述場景、主要物件，以及你注意到的重要細節。"
```

目前專案預設的遠端模型設定也是：

- `OLLAMA_BASE_URL=http://192.168.8.166:11434`
- `OLLAMA_MODEL=qwen3.5:2b`

目前 Ollama prompt 會要求：

- `action` 維持固定英文值，方便程式解析
- `reason` 使用繁體中文，方便直接閱讀模型判斷依據

如果要確認目前到底有沒有拍照成功、是否真的送出圖片到模型，建議加上：

- `--debug-save-frame-path /tmp/latest-frame.jpg`
  - 每次迴圈都把最新影像存成 JPEG
- `--ollama-timeout 180`
  - 避免模型第一次載入時 30 秒內來不及回應

## Important Rules

1. Pi 端是主控制器，但模型輸出仍然要經過本地驗證。
2. Pi 端只允許有限動作命令進入馬達層。
3. 模型逾時或解析失敗時，預設停止。
4. 馬達控制一定要有 timeout。
