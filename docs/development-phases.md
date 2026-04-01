# Development Phases

## Phase 0: Bring-Up

目標是把每個硬體元件單獨測通。

- Raspberry Pi 開機與 Wi-Fi
- Camera 拍照
- 麥克風錄音
- 喇叭播放
- 四輪馬達控制

完成標準：

- 每個硬體都有自己的測試腳本
- 不需要 AI 也能確認硬體正常

## Phase 1: Remote Control MVP

目標是讓你先有一台可靠的「SSH 啟動的主控車」。

- 透過 SSH 登入 Pi 啟動主程式
- 在 Pi 本機接受鍵盤或簡單 CLI 命令
- Pi 能執行前進、後退、左轉、右轉、停止

完成標準：

- 主程式在 Pi 上可穩定執行
- SSH 中斷或主程式異常時車子會自動停止

## Phase 2: Vision Feedback Loop

目標是讓 Pi 能把畫面送到模型，並根據結果做動作。

- Pi 定時擷取縮圖
- 傳送到 Ollama 或其他 vision model
- Pi 解析模型結果並回傳高階動作到馬達模組

完成標準：

- 能形成最小 search loop
- 即使尚未真的找到玩具，也能做出持續搜尋動作

## Phase 3: Voice Mission

目標是加入語音任務入口。

- 「請找到玩具」
- STT 轉文字
- 本機任務解析
- 啟動搜尋流程

完成標準：

- 使用者不需要碰鍵盤就能啟動任務

## Phase 4: Robust Search

目標是讓搜尋更穩定，不會一直原地亂轉。

- 記錄最近幾次動作
- 防止同一動作無限重複
- 加入 timeout 與 recovery 邏輯
- 加入 target found / lost 狀態切換

完成標準：

- 搜尋路徑有策略
- 找不到目標時會自動改變搜尋模式

## Phase 5: Real-World Reliability

目標是把系統從 demo 拉到可重複展示。

- SSH 啟動腳本
- systemd service
- 日誌輪替
- 電池與硬體狀態監控
- 測試資料回放

完成標準：

- 重開機後可自動啟動
- 有基本除錯資料可追查問題
