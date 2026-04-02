#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT_DIR/scripts/ollama_models.sh"

OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://192.168.8.166:11434}"
OLLAMA_MODEL="${OLLAMA_MODEL:-qwen3.5:2b}"

print_header() {
  echo "== Ollama Model Helper =="
  echo
}

print_usage() {
  echo "用法:"
  echo "  ./scripts/list_ollama_models.sh"
  echo
  echo "這支腳本會從目前設定的 Ollama host 讀取可用模型清單。"
}

main() {
  local idx

  print_header

  if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    print_usage
    exit 0
  fi

  load_ollama_models

  echo "[info] 使用 API: ${OLLAMA_BASE_URL%/}/api/tags"
  echo

  for idx in "${!OLLAMA_MODEL_LABELS[@]}"; do
    if [[ "${OLLAMA_MODEL_NAMES[$idx]}" == "$OLLAMA_MODEL" ]]; then
      echo "$((idx + 1))) ${OLLAMA_MODEL_LABELS[$idx]} [預設]"
    else
      echo "$((idx + 1))) ${OLLAMA_MODEL_LABELS[$idx]}"
    fi
  done
}

main "$@"
