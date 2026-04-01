#!/usr/bin/env bash

set -euo pipefail

print_header() {
  echo "== Raspberry Pi Camera Resolution Helper =="
  echo
}

print_usage() {
  echo "用法:"
  echo "  ./scripts/list_camera_resolutions.sh"
  echo
  echo "這支腳本會列出 Raspberry Pi 相機目前可用的 camera modes / resolutions。"
}

run_with_command() {
  local cmd="$1"
  echo "[info] 使用指令: ${cmd} --list-cameras"
  echo
  "${cmd}" --list-cameras
}

print_hint() {
  echo
  echo "[hint] 輸出中的 mode / size 就是目前感光元件支援的解析度模式。"
  echo "[hint] 例如 640x480、1280x720、2592x1944。"
  echo "[hint] 如果你的程式設定成較低解析度，通常是由 ISP 或軟體做縮放。"
}

main() {
  print_header

  if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    print_usage
    exit 0
  fi

  if command -v rpicam-hello >/dev/null 2>&1; then
    run_with_command "rpicam-hello"
    print_hint
    exit 0
  fi

  if command -v libcamera-hello >/dev/null 2>&1; then
    run_with_command "libcamera-hello"
    print_hint
    exit 0
  fi

  cat <<'EOF'
[error] 找不到 rpicam-hello 或 libcamera-hello。

請先確認：
  1. 你是在 Raspberry Pi OS 上執行
  2. 相機功能已啟用
  3. 已安裝 rpicam-apps 或 libcamera-apps

常見安裝方式：
  sudo apt update
  sudo apt install -y rpicam-apps
EOF
  exit 1
}

main "$@"
