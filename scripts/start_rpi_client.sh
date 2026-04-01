#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="$ROOT_DIR/apps/rpi-client"

export PYTHONPATH="$APP_DIR/src${PYTHONPATH:+:$PYTHONPATH}"

cd "$APP_DIR"
exec python3 -m rpi_client.main "$@"
