# scripts

這裡放開發與部署輔助腳本，例如：

- Raspberry Pi 環境安裝
- 啟動 client
- 相機解析度 / mode 檢查
- 健康檢查
- 測試資料回放

## Available Scripts

- `./scripts/start_rpi_client.sh`
  - 啟動 Raspberry Pi 主程式
- `./scripts/demo.sh`
  - 執行時先讀取攝影機支援模式，再以互動式選單選擇解析度後執行一次 Ollama 測試
- `./scripts/describe_image.sh`
  - 執行時先讀取攝影機支援模式，再以互動式選單選擇解析度後請 Ollama 以繁體中文解讀圖片
- `./scripts/list_camera_resolutions.sh`
  - 列出 Raspberry Pi 相機可用的 camera modes / resolutions

## Config Files

- `config/defaults.toml`
  - 專案預設值，可提交到版本控制
- `config/user.toml`
  - 使用者自己的本地設定，不提交
- `config/user.toml.example`
  - 建議複製成 `config/user.toml` 後再修改
