#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROMPT="${1:-請用繁體中文解讀這張圖片，描述場景、主要物件，以及你注意到的重要細節。}"

exec "$ROOT_DIR/scripts/start_rpi_client.sh" \
  --app-mode describe \
  --camera-mode pi \
  --camera-width "${RPI_AI_CAMERA_WIDTH:-640}" \
  --camera-height "${RPI_AI_CAMERA_HEIGHT:-480}" \
  --model-mode ollama \
  --ollama-base-url "${OLLAMA_BASE_URL:-http://192.168.8.166:11434}" \
  --ollama-model "${OLLAMA_MODEL:-qwen3.5:2b}" \
  --ollama-timeout "${OLLAMA_TIMEOUT_S:-300}" \
  --debug-save-frame-path "${RPI_AI_DEBUG_SAVE_FRAME_PATH:-/tmp/latest-frame.jpg}" \
  --describe-prompt "$PROMPT"
