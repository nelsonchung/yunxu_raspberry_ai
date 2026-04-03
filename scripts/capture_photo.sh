#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT_DIR/scripts/camera_modes.sh"

OUTPUT_PATH="${RPI_AI_CAPTURE_OUTPUT:-/tmp/my-photo.jpg}"
JPEG_QUALITY="${RPI_AI_JPEG_QUALITY:-95}"
CAPTURE_TIMEOUT_MS="${RPI_AI_CAPTURE_TIMEOUT_MS:-1000}"

print_header() {
  echo "== Raspberry Pi Photo Capture =="
  echo
}

print_usage() {
  cat <<EOF
用法:
  ./scripts/capture_photo.sh [--output PATH] [--quality 1-100] [--timeout-ms N]

功能:
  1. 讀取 Raspberry Pi 相機目前支援的解析度
  2. 以互動式選單選擇拍照解析度
  3. 拍一張 JPEG 照片並輸出到指定路徑

參數:
  --output PATH     輸出檔案路徑
                    預設: ${OUTPUT_PATH}
  --quality N       JPEG 品質 1-100
                    預設: ${JPEG_QUALITY}
  --timeout-ms N    拍照前等待毫秒數，讓自動曝光稍微穩定
                    預設: ${CAPTURE_TIMEOUT_MS}
  -h, --help        顯示這份說明

環境變數:
  RPI_AI_CAPTURE_OUTPUT
  RPI_AI_JPEG_QUALITY
  RPI_AI_CAPTURE_TIMEOUT_MS
EOF
}

find_capture_command() {
  if command -v rpicam-still >/dev/null 2>&1; then
    echo "rpicam-still"
    return 0
  fi

  if command -v libcamera-still >/dev/null 2>&1; then
    echo "libcamera-still"
    return 0
  fi

  if command -v rpicam-jpeg >/dev/null 2>&1; then
    echo "rpicam-jpeg"
    return 0
  fi

  if command -v libcamera-jpeg >/dev/null 2>&1; then
    echo "libcamera-jpeg"
    return 0
  fi

  return 1
}

validate_integer() {
  local value="$1"
  local name="$2"
  if ! [[ "$value" =~ ^[0-9]+$ ]]; then
    echo "[error] ${name} 必須是整數，收到: ${value}" >&2
    exit 1
  fi
}

validate_quality() {
  validate_integer "$JPEG_QUALITY" "JPEG quality"
  if (( JPEG_QUALITY < 1 || JPEG_QUALITY > 100 )); then
    echo "[error] JPEG quality 必須介於 1 到 100，收到: ${JPEG_QUALITY}" >&2
    exit 1
  fi
}

validate_timeout() {
  validate_integer "$CAPTURE_TIMEOUT_MS" "timeout-ms"
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --output)
        if [[ $# -lt 2 ]]; then
          echo "[error] --output 需要一個路徑參數。" >&2
          exit 1
        fi
        OUTPUT_PATH="$2"
        shift 2
        ;;
      --quality)
        if [[ $# -lt 2 ]]; then
          echo "[error] --quality 需要一個數字參數。" >&2
          exit 1
        fi
        JPEG_QUALITY="$2"
        shift 2
        ;;
      --timeout-ms)
        if [[ $# -lt 2 ]]; then
          echo "[error] --timeout-ms 需要一個整數參數。" >&2
          exit 1
        fi
        CAPTURE_TIMEOUT_MS="$2"
        shift 2
        ;;
      -h|--help)
        print_usage
        exit 0
        ;;
      *)
        echo "[error] 不支援的參數: $1" >&2
        echo >&2
        print_usage >&2
        exit 1
        ;;
    esac
  done
}

print_install_hint() {
  cat <<'EOF'
[error] 找不到 rpicam-still / libcamera-still / rpicam-jpeg / libcamera-jpeg。

請先確認：
  1. 你是在 Raspberry Pi OS 上執行
  2. 相機功能已啟用
  3. 已安裝 rpicam-apps 或 libcamera-apps

常見安裝方式：
  sudo apt update
  sudo apt install -y rpicam-apps
EOF
}

capture_photo() {
  local cmd="$1"

  mkdir -p "$(dirname "$OUTPUT_PATH")"

  echo "[info] 使用指令: ${cmd}"
  echo "[info] 解析度: ${CAMERA_LABEL}"
  echo "[info] JPEG 品質: ${JPEG_QUALITY}"
  echo "[info] 輸出路徑: ${OUTPUT_PATH}"
  echo

  "$cmd" \
    -n \
    --width "$CAMERA_WIDTH" \
    --height "$CAMERA_HEIGHT" \
    --quality "$JPEG_QUALITY" \
    --timeout "$CAPTURE_TIMEOUT_MS" \
    --output "$OUTPUT_PATH"

  echo
  echo "[done] 照片已儲存到: ${OUTPUT_PATH}"
}

main() {
  local capture_cmd

  print_header
  parse_args "$@"
  validate_quality
  validate_timeout

  if ! capture_cmd="$(find_capture_command)"; then
    print_install_hint
    exit 1
  fi

  select_camera_mode "請根據目前攝影機支援模式選擇拍照解析度："
  capture_photo "$capture_cmd"
}

main "$@"
