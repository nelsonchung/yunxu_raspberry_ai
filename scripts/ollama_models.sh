#!/usr/bin/env bash

set -euo pipefail

OLLAMA_MODEL_NAMES=()
OLLAMA_MODEL_LABELS=()
OLLAMA_TAGS_TIMEOUT="${OLLAMA_TAGS_TIMEOUT_S:-10}"

load_ollama_models() {
  local raw_output
  local api_url="${OLLAMA_BASE_URL%/}/api/tags"

  OLLAMA_MODEL_NAMES=()
  OLLAMA_MODEL_LABELS=()

  if ! command -v curl >/dev/null 2>&1; then
    echo "[error] 找不到 curl，無法查詢 Ollama 模型清單。" >&2
    return 1
  fi

  if ! raw_output="$(
    curl \
      --silent \
      --show-error \
      --fail \
      --max-time "$OLLAMA_TAGS_TIMEOUT" \
      "$api_url"
  )"; then
    echo "[error] 無法從 ${api_url} 取得 Ollama 模型清單。" >&2
    return 1
  fi

  while IFS=$'\t' read -r name parameter_size family; do
    local label
    [[ -z "$name" ]] && continue

    label="$name"
    if [[ -n "$parameter_size" && "$parameter_size" != "None" ]]; then
      label="${label} [${parameter_size}]"
    fi
    if [[ -n "$family" && "$family" != "None" ]]; then
      label="${label} - ${family}"
    fi

    OLLAMA_MODEL_NAMES+=("$name")
    OLLAMA_MODEL_LABELS+=("$label")
  done < <(
    python3 -c '
import json
import sys

body = json.loads(sys.argv[1])
for model in body.get("models", []):
    details = model.get("details") or {}
    name = model.get("name", "")
    parameter_size = details.get("parameter_size", "")
    family = details.get("family", "")
    print(f"{name}\t{parameter_size}\t{family}")
' "$raw_output"
  )

  if [[ "${#OLLAMA_MODEL_NAMES[@]}" -eq 0 ]]; then
    echo "[error] Ollama 沒有回傳任何可用模型。" >&2
    return 1
  fi
}

default_ollama_model_index() {
  local idx
  for idx in "${!OLLAMA_MODEL_NAMES[@]}"; do
    if [[ "${OLLAMA_MODEL_NAMES[$idx]}" == "$OLLAMA_MODEL" ]]; then
      echo "$idx"
      return 0
    fi
  done
  echo "0"
}

select_ollama_model() {
  local title="$1"
  local default_index choice selected_index idx

  load_ollama_models
  default_index="$(default_ollama_model_index)"

  echo "$title"
  echo
  echo "[info] 使用 API: ${OLLAMA_BASE_URL%/}/api/tags"
  echo "請選擇要測試的 Ollama 模型："
  for idx in "${!OLLAMA_MODEL_LABELS[@]}"; do
    if [[ "$idx" == "$default_index" ]]; then
      echo "$((idx + 1))) ${OLLAMA_MODEL_LABELS[$idx]} [預設]"
    else
      echo "$((idx + 1))) ${OLLAMA_MODEL_LABELS[$idx]}"
    fi
  done
  echo

  read -r -p "輸入選項 (預設 $((default_index + 1))): " choice
  selected_index="${choice:-$((default_index + 1))}"

  if ! [[ "$selected_index" =~ ^[0-9]+$ ]]; then
    echo "[error] 無效選項: $selected_index" >&2
    return 1
  fi

  if (( selected_index < 1 || selected_index > ${#OLLAMA_MODEL_LABELS[@]} )); then
    echo "[error] 無效選項: $selected_index" >&2
    return 1
  fi

  selected_index=$((selected_index - 1))
  OLLAMA_MODEL="${OLLAMA_MODEL_NAMES[$selected_index]}"
  OLLAMA_MODEL_LABEL="${OLLAMA_MODEL_LABELS[$selected_index]}"
}
