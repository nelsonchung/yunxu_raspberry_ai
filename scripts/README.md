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
  - 互動式選單，選擇拍照解析度後執行一次 Ollama 測試
- `./scripts/list_camera_resolutions.sh`
  - 列出 Raspberry Pi 相機可用的 camera modes / resolutions
- `./scripts/320240.sh`
  - 舊的固定 320x240 快捷測試腳本
