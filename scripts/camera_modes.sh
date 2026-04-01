#!/usr/bin/env bash

set -euo pipefail

CAMERA_MODE_LABELS=()
CAMERA_MODE_WIDTHS=()
CAMERA_MODE_HEIGHTS=()

find_camera_list_command() {
  if command -v rpicam-hello >/dev/null 2>&1; then
    echo "rpicam-hello"
    return 0
  fi

  if command -v libcamera-hello >/dev/null 2>&1; then
    echo "libcamera-hello"
    return 0
  fi

  return 1
}

load_camera_modes() {
  local cmd raw_output line width height label

  CAMERA_MODE_LABELS=()
  CAMERA_MODE_WIDTHS=()
  CAMERA_MODE_HEIGHTS=()

  if ! cmd="$(find_camera_list_command)"; then
    echo "[error] 找不到 rpicam-hello 或 libcamera-hello，無法讀取攝影機支援模式。" >&2
    return 1
  fi

  raw_output="$("$cmd" --list-cameras)"

  while IFS= read -r line; do
    if [[ "$line" == *"fps"* && "$line" =~ ([0-9]+)x([0-9]+) ]]; then
      width="${BASH_REMATCH[1]}"
      height="${BASH_REMATCH[2]}"
      label="${width}x${height}"
      if [[ "$line" =~ \[([0-9.]+[[:space:]]fps) ]]; then
        label="${label} (${BASH_REMATCH[1]})"
      fi
      if camera_mode_exists "$width" "$height"; then
        continue
      fi
      CAMERA_MODE_WIDTHS+=("$width")
      CAMERA_MODE_HEIGHTS+=("$height")
      CAMERA_MODE_LABELS+=("$label")
    fi
  done <<< "$raw_output"

  if [[ "${#CAMERA_MODE_LABELS[@]}" -eq 0 ]]; then
    echo "[error] 無法從相機資訊中解析出可用解析度。" >&2
    return 1
  fi
}

camera_mode_exists() {
  local width="$1"
  local height="$2"
  local idx
  for idx in "${!CAMERA_MODE_WIDTHS[@]}"; do
    if [[ "${CAMERA_MODE_WIDTHS[$idx]}" == "$width" && "${CAMERA_MODE_HEIGHTS[$idx]}" == "$height" ]]; then
      return 0
    fi
  done
  return 1
}

default_camera_mode_index() {
  local idx
  for idx in "${!CAMERA_MODE_WIDTHS[@]}"; do
    if [[ "${CAMERA_MODE_WIDTHS[$idx]}" == "640" && "${CAMERA_MODE_HEIGHTS[$idx]}" == "480" ]]; then
      echo "$idx"
      return 0
    fi
  done
  echo "0"
}

select_camera_mode() {
  local title="$1"
  local default_index choice selected_index idx

  load_camera_modes
  default_index="$(default_camera_mode_index)"

  echo "$title"
  echo
  echo "請選擇拍照解析度："
  for idx in "${!CAMERA_MODE_LABELS[@]}"; do
    echo "$((idx + 1))) ${CAMERA_MODE_LABELS[$idx]}"
  done
  echo

  read -r -p "輸入選項 (預設 $((default_index + 1))): " choice
  selected_index="${choice:-$((default_index + 1))}"

  if ! [[ "$selected_index" =~ ^[0-9]+$ ]]; then
    echo "[error] 無效選項: $selected_index" >&2
    return 1
  fi

  if (( selected_index < 1 || selected_index > ${#CAMERA_MODE_LABELS[@]} )); then
    echo "[error] 無效選項: $selected_index" >&2
    return 1
  fi

  selected_index=$((selected_index - 1))
  CAMERA_WIDTH="${CAMERA_MODE_WIDTHS[$selected_index]}"
  CAMERA_HEIGHT="${CAMERA_MODE_HEIGHTS[$selected_index]}"
  CAMERA_LABEL="${CAMERA_MODE_LABELS[$selected_index]}"
}
