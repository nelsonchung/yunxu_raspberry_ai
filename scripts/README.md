# scripts

這裡放開發與部署輔助腳本，例如：

- Raspberry Pi 環境安裝
- 啟動 robot core
- 相機解析度 / mode 檢查
- 健康檢查
- 測試資料回放

## Available Scripts

- `./scripts/start_robot_core.sh`
  - 啟動 Raspberry Pi 主程式核心
- `./scripts/demo.sh`
  - 執行時先讀取 Ollama 可用模型與攝影機支援模式，再以互動式選單選擇模型和解析度後執行一次 Ollama 測試，並預設開啟 timing
- `./scripts/describe_image.sh`
  - 執行時先讀取 Ollama 可用模型與攝影機支援模式，再以互動式選單選擇模型和解析度後請 Ollama 以繁體中文解讀圖片，並預設開啟 timing
- `./scripts/capture_photo.sh`
  - 執行時先讀取攝影機支援模式，再以互動式選單選擇解析度後拍一張 JPEG 照片，可指定輸出路徑與 JPEG 品質
- `./scripts/list_camera_resolutions.sh`
  - 列出 Raspberry Pi 相機可用的 camera modes / resolutions
- `./scripts/list_ollama_models.sh`
  - 直接從目前設定的 Ollama host 查詢 `/api/tags` 並列出可用模型

## Config Files

- `config/defaults.toml`
  - 專案預設值，可提交到版本控制
- `config/user.toml`
  - 使用者自己的本地設定，不提交
- `config/user.toml.example`
  - 建議複製成 `config/user.toml` 後再修改
