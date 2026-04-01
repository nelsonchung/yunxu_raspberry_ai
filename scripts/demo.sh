#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
START_SCRIPT="$ROOT_DIR/scripts/start_rpi_client.sh"
OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://192.168.8.166:11434}"
OLLAMA_MODEL="${OLLAMA_MODEL:-qwen3.5:2b}"
OLLAMA_TIMEOUT="${OLLAMA_TIMEOUT_S:-300}"
DEBUG_FRAME_PATH="${RPI_AI_DEBUG_SAVE_FRAME_PATH:-/tmp/latest-frame.jpg}"
MAX_ITERATIONS="${RPI_AI_MAX_ITERATIONS:-1}"

print_header() {
  echo "== Raspberry Pi AI Car Demo =="
  echo
  echo "請選擇拍照解析度："
  echo "1) 320x240"
  echo "2) 640x480"
  echo "3) 1296x972"
  echo "4) 1920x1080"
  echo "5) 2592x1944"
  echo
}

select_resolution() {
  local choice
  read -r -p "輸入選項 (預設 2): " choice
  choice="${choice:-2}"

  case "$choice" in
    1)
      CAMERA_WIDTH=320
      CAMERA_HEIGHT=240
      ;;
    2)
      CAMERA_WIDTH=640
      CAMERA_HEIGHT=480
      ;;
    3)
      CAMERA_WIDTH=1296
      CAMERA_HEIGHT=972
      ;;
    4)
      CAMERA_WIDTH=1920
      CAMERA_HEIGHT=1080
      ;;
    5)
      CAMERA_WIDTH=2592
      CAMERA_HEIGHT=1944
      ;;
    *)
      echo "[error] 無效選項: $choice" >&2
      exit 1
      ;;
  esac
}

run_demo() {
  echo
  echo "[info] 使用解析度 ${CAMERA_WIDTH}x${CAMERA_HEIGHT}"
  echo "[info] Ollama: ${OLLAMA_BASE_URL} (${OLLAMA_MODEL})"
  echo "[info] Debug image: ${DEBUG_FRAME_PATH}"
  echo

  exec "$START_SCRIPT" \
    --camera-mode pi \
    --camera-width "$CAMERA_WIDTH" \
    --camera-height "$CAMERA_HEIGHT" \
    --model-mode ollama \
    --ollama-base-url "$OLLAMA_BASE_URL" \
    --ollama-model "$OLLAMA_MODEL" \
    --ollama-timeout "$OLLAMA_TIMEOUT" \
    --debug-save-frame-path "$DEBUG_FRAME_PATH" \
    --max-iterations "$MAX_ITERATIONS"
}

print_header
select_resolution
run_demo
