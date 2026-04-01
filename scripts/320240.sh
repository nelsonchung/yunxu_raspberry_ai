./scripts/start_rpi_client.sh \
  --camera-mode pi \
  --camera-width 320 \
  --camera-height 240 \
  --model-mode ollama \
  --ollama-base-url http://192.168.8.166:11434 \
  --ollama-model qwen3.5:2b \
  --ollama-timeout 300 \
  --debug-save-frame-path /tmp/latest-frame.jpg \
  --max-iterations 1

