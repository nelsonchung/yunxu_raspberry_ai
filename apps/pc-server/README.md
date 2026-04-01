# legacy-macbook-notes

這個目錄目前不再作為主要執行架構的一部分。

目前專案改為由 Raspberry Pi 直接執行主程式，MacBook 主要透過 SSH 操作 Pi，並可選擇只提供 Ollama 模型能力，不再維護自訂 FastAPI server。

## Suggested Use

- 若未來需要存放 MacBook 端的輔助腳本，可把這裡當成操作工具目錄。
- 若決定完全不在 MacBook 放任何專案程式，這個目錄之後可以移除。

## Important Rules

1. 不要再把主控制邏輯放回 MacBook。
2. 若 MacBook 只負責 Ollama，Pi 仍然必須保有最終決策與安全停車權。
