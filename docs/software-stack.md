# Software Stack

## Raspberry Pi Side

建議用 Python 開發，因為硬體控制、OpenCV、音訊與模型整合都很成熟。

### Recommended Libraries

- `opencv-python`
  - 相機擷取、縮圖、影像壓縮
- `picamera2`
  - Raspberry Pi CSI camera interface 的官方 Python 路線，建議和 OpenCV 一起使用
- `gpiozero` 或 `pigpio`
  - 控制 GPIO 與 PWM
- `httpx` 或 `aiohttp`
  - 若模型跑在遠端主機，用來直接呼叫 Ollama API
- `sounddevice` 或 `pyaudio`
  - 錄音
- `pygame`、`simpleaudio` 或系統播放器
  - 播放提示音 / TTS 音訊
- `faster-whisper` 或 `vosk`
  - 本機 STT

## MacBook Side

MacBook 不再承擔自訂 FastAPI server 的責任，主要是開發操作端。

### Recommended Roles

- SSH 連到 Raspberry Pi
- 編輯設定、啟動主程式、看 log
- 可選擇執行 Ollama，讓 Pi 透過區網直接呼叫
- 可選擇保存訓練樣本、測試圖片與調參紀錄

### Optional MacBook Libraries

- `ollama`
  - 若 MacBook 作為模型主機，可在本機執行模型
- `tmux`
  - 方便長時間透過 SSH 操作 Pi
- `rsync`
  - 同步程式與資料到 Pi

## Functional Split

### On Raspberry Pi

- 硬體控制
- 低延遲安全停車
- 影像前處理
- 音訊收集
- 任務狀態
- 搜尋策略
- 決策驗證
- 模型呼叫整合

### On MacBook

- SSH 操作
- 啟動與部署
- 遠端除錯
- 可選模型主機

## STT Recommendation

如果你的目標是完全由 Pi 主控，語音辨識有兩條路：

- `MVP 路線`
  - 先用 SSH / CLI 文字任務驗證整個 search loop
- `完整語音路線`
  - 再加入 Pi 本地 STT，例如 `faster-whisper tiny` 或 `vosk`

這樣比較容易把問題拆開，不會一開始就同時卡在語音、影像和馬達控制。

## Suggested MVP Tech Choices

如果你要先求穩定，第一版可以這樣選：

- `RPi main`: Python + OpenCV + gpiozero + httpx
- `Model host`: MacBook 上的 Ollama，或之後換成 Pi 本機模型
- `Mission input`: SSH CLI 文字任務，之後再升級本地 STT
- `Image format`: JPEG + base64
- `TTS`: 先用簡單預錄音或本地短句播放

等第一版完成後，再升級：

- 文字任務 -> 本地語音任務
- 單張分析 -> 持續串流
- 規則式搜尋 -> 更完整的任務狀態機
