# Configuration Design

## Why This Exists

這個專案的設定來源比較多，因為它同時要兼顧：

- 專案級預設值
- 每台 Raspberry Pi 的本地差異
- 單次測試時的臨時覆寫
- 不同啟動腳本之間的共用設定

如果沒有明確的設定層級，常見問題會是：

- 使用者直接修改腳本內容，之後難以維護
- `README` 範例值、程式內建值、環境變數彼此不一致
- 不知道最後到底是哪個值生效

因此目前採用「分層設定」設計，而不是把所有設定硬寫在腳本裡。

## Configuration Sources

目前主程式會從以下來源讀取設定：

1. `config/defaults.toml`
2. `config/user.toml`
3. 環境變數
4. CLI 參數

另外程式內部仍保留最後一層 built-in fallback，避免設定檔缺失時直接崩潰。

## Priority Order

真正生效的優先順序如下：

1. `CLI 參數`
2. `環境變數`
3. `config/user.toml`
4. `config/defaults.toml`
5. `程式內建 fallback`

意思是：

- 如果你在命令列上明確帶了 `--camera-width 1296`，那這次執行就以 `1296` 為準。
- 如果 CLI 沒有帶，才會往下看環境變數。
- 如果環境變數也沒有，才會讀 `config/user.toml`。
- 如果 `config/user.toml` 沒有該欄位，才會回到 `config/defaults.toml`。

## What Each Layer Is For

### `config/defaults.toml`

用途：

- 放專案共同預設值
- 可以提交到版本控制
- 提供團隊一致的起始設定

適合放：

- 預設模型名稱
- 預設 timeout
- 預設 app mode
- 預設 prompt

### `config/user.toml`

用途：

- 放每位使用者或每台 Raspberry Pi 的本地設定
- 不提交到版本控制
- 讓使用者不用每次都改 CLI

適合放：

- 你的常用解析度
- 你的相機模式
- 你的 Ollama host
- 你的 debug 圖片儲存路徑

### 環境變數

用途：

- 放 shell session 或部署環境相關值
- 適合在 SSH session、systemd、CI 或部署腳本中設定

適合放：

- `OLLAMA_BASE_URL`
- `OLLAMA_MODEL`
- `OLLAMA_TIMEOUT_S`
- `RPI_AI_DEBUG_SAVE_FRAME_PATH`

### CLI 參數

用途：

- 單次執行的臨時覆寫
- 優先權最高

例如：

```bash
./scripts/start_rpi_client.sh \
  --app-mode describe \
  --camera-width 1296 \
  --camera-height 972 \
  --ollama-timeout 180
```

上面這些值只影響這一次執行。

## Recommended Usage

建議使用方式：

1. 不要直接修改腳本內容
2. 專案共用預設值放在 `config/defaults.toml`
3. 個人或設備差異寫在 `config/user.toml`
4. 單次測試時再用 CLI 覆寫

## First-Time Setup

### Step 1. Inspect Project Defaults

先看專案預設值：

- [defaults.toml](/Users/nelsonchung/development/yunxu_raspberry_ai/config/defaults.toml)

### Step 2. Create Your Local Override File

複製範本：

```bash
cp config/user.toml.example config/user.toml
```

之後修改：

- `config/user.toml`

### Step 3. Put Your Common Local Values There

例如：

```toml
app_mode = "describe"
camera_mode = "pi"
camera_width = 1296
camera_height = 972
model_mode = "ollama"
ollama_base_url = "http://192.168.8.166:11434"
ollama_model = "qwen3.5:2b"
ollama_timeout_s = 180.0
debug_save_frame_path = "/tmp/latest-frame.jpg"
```

## Example Scenarios

### Scenario 1. Daily Use On Your Raspberry Pi

把常用值寫進 `config/user.toml` 後，平常只要執行：

```bash
./scripts/start_rpi_client.sh
```

### Scenario 2. Temporary One-Off Override

如果今天只想改成高解析度測試一次：

```bash
./scripts/start_rpi_client.sh \
  --camera-width 2592 \
  --camera-height 1944
```

這不會改掉你的 `config/user.toml`。

### Scenario 3. Temporarily Use Another Ollama Host

```bash
OLLAMA_BASE_URL=http://192.168.8.200:11434 ./scripts/describe_image.sh
```

### Scenario 4. Ignore Local User Config

如果你想確認專案預設值是否正常：

```bash
./scripts/start_rpi_client.sh --no-user-config
```

## File Map

目前和這套設定設計直接相關的檔案有：

- [config/defaults.toml](/Users/nelsonchung/development/yunxu_raspberry_ai/config/defaults.toml)
- [config/user.toml.example](/Users/nelsonchung/development/yunxu_raspberry_ai/config/user.toml.example)
- [config.py](/Users/nelsonchung/development/yunxu_raspberry_ai/apps/rpi-client/src/rpi_client/config.py)
- [.gitignore](/Users/nelsonchung/development/yunxu_raspberry_ai/.gitignore)

## Design Notes

這個設計的重點不是追求最多設定方式，而是讓「穩定預設、個人差異、單次測試」三種需求可以同時成立。

最重要的原則只有兩個：

1. 常用值放設定檔，不要把腳本改成每台機器各一份
2. 單次覆寫走 CLI，避免把暫時測試值寫回長期設定
