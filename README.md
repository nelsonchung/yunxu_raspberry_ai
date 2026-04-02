# yunxu_raspberry_ai

使用 Raspberry Pi 4 製作可移動、可收音、可播音、可拍照的 AI 遙控車，主程式直接跑在 Raspberry Pi 上，並可選擇透過同一個 Wi-Fi 內網連到 MacBook 上的 Ollama 模型，完成「聽懂語音任務 -> 找玩具 -> 持續搜尋」的循環。

這個專案現在建議拆成兩個角色：

1. `Raspberry Pi main runtime`
負責相機、麥克風、喇叭、馬達控制、任務狀態、搜尋流程，以及模型呼叫整合。

2. `MacBook operator / optional Ollama host`
負責透過 SSH 連到 Raspberry Pi 啟動主程式，也可選擇在 MacBook 上執行 Ollama，讓 Pi 直接呼叫模型 API。

注意：

- 如果要做「看畫面找玩具」，模型必須是支援影像輸入的 vision model。
- 單純文字模型不能直接看相機畫面。
- 即使沒有 FastAPI server，語音、影像、馬達控制與模型整合仍然建議分模組開發，不要在同一支腳本裡混寫。

建議優先開發順序：

1. 先讓車子可以手動前進、後退、左轉、右轉。
2. 再讓 Raspberry Pi 能穩定拍照，並把畫面送給本機或遠端的 Ollama。
3. 再讓 Raspberry Pi 根據模型結果執行簡單動作，例如 `forward`、`turn_left`、`stop`。
4. 最後再加上語音任務與「持續搜尋玩具」的自主迴圈。

## Repository Layout

```text
.
├── src/
│   └── robot_core/         # Raspberry Pi 主程式核心：相機、音訊、馬達、任務、模型整合
├── config/                 # 預設設定與使用者本地覆寫設定
├── docs/                   # 架構、硬體、API、開發階段文件
├── pyproject.toml          # Python 專案設定
└── scripts/                # SSH 啟動、部署、環境安裝腳本
```

## Docs

- [系統架構](./docs/architecture.md)
- [設定設計](./docs/configuration.md)
- [執行與模組說明](./docs/runtime-usage.md)
- [硬體與供電規劃](./docs/hardware-bom.md)
- [模組整合與命令合約](./docs/api-contract.md)
- [開發階段規劃](./docs/development-phases.md)
- [軟體堆疊建議](./docs/software-stack.md)

## Initial Development Goal

第一個里程碑不是「完全自動找玩具」，而是下面這條最小可行路線：

1. Raspberry Pi 啟動後能連上 Wi-Fi。
2. Raspberry Pi 能拍一張縮圖並送給 Ollama 視覺模型。
3. Raspberry Pi 能把模型輸出轉成一個方向指令。
4. Raspberry Pi 根據指令控制四輪底盤短時間移動。
5. 重複這個循環，形成最基本的 search loop。

## Operation Model

平常開發方式改為：

1. 在 MacBook 上用 SSH 連到 Raspberry Pi。
2. 在 Raspberry Pi 上啟動主程式。
3. 主程式在 Pi 上管理相機、音訊、馬達與任務循環。
4. 若使用 MacBook 上的 Ollama，Pi 直接呼叫模型 API，不再經過自訂 FastAPI server。
