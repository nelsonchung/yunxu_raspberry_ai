#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
START_SCRIPT="$ROOT_DIR/scripts/start_robot_core.sh"
source "$ROOT_DIR/scripts/camera_modes.sh"
source "$ROOT_DIR/scripts/ollama_models.sh"
OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://192.168.8.166:11434}"
OLLAMA_MODEL="${OLLAMA_MODEL:-qwen3.5:2b}"
OLLAMA_TIMEOUT="${OLLAMA_TIMEOUT_S:-300}"
DEBUG_FRAME_PATH="${RPI_AI_DEBUG_SAVE_FRAME_PATH:-/tmp/latest-frame.jpg}"
MAX_ITERATIONS="${RPI_AI_MAX_ITERATIONS:-1}"

print_header() {
  echo "== Raspberry Pi AI Car Demo =="
}

run_demo() {
  echo
  echo "[info] 使用解析度 ${CAMERA_LABEL}"
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
    --timing \
    --max-iterations "$MAX_ITERATIONS"
}

print_header
select_ollama_model "請根據目前 Ollama 主機支援模型選擇測試模型："
select_camera_mode "請根據目前攝影機支援模式選擇解析度："
run_demo
