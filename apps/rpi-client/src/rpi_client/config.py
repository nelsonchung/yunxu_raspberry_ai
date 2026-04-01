from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class RuntimeConfig:
    goal: str
    max_iterations: int
    loop_interval_s: float
    camera_mode: str
    camera_width: int
    camera_height: int
    camera_warmup_s: float
    jpeg_quality: int
    sample_image_path: Optional[str]
    model_mode: str
    ollama_base_url: str
    ollama_model: str
    dry_run: bool

    @classmethod
    def from_args(cls):
        parser = argparse.ArgumentParser(
            description="Run the Raspberry Pi AI car main loop."
        )
        parser.add_argument(
            "--goal",
            default=os.getenv("RPI_AI_GOAL", "find toy"),
            help="Mission goal text.",
        )
        parser.add_argument(
            "--max-iterations",
            type=int,
            default=int(os.getenv("RPI_AI_MAX_ITERATIONS", "8")),
            help="Maximum search iterations before stopping.",
        )
        parser.add_argument(
            "--loop-interval",
            type=float,
            default=float(os.getenv("RPI_AI_LOOP_INTERVAL", "1.0")),
            help="Seconds to wait between iterations.",
        )
        parser.add_argument(
            "--camera-mode",
            choices=["mock", "file", "pi"],
            default=os.getenv("RPI_AI_CAMERA_MODE", "mock"),
            help="Camera provider implementation.",
        )
        parser.add_argument(
            "--camera-width",
            type=int,
            default=int(os.getenv("RPI_AI_CAMERA_WIDTH", "640")),
            help="Capture width for Pi camera mode.",
        )
        parser.add_argument(
            "--camera-height",
            type=int,
            default=int(os.getenv("RPI_AI_CAMERA_HEIGHT", "480")),
            help="Capture height for Pi camera mode.",
        )
        parser.add_argument(
            "--camera-warmup",
            type=float,
            default=float(os.getenv("RPI_AI_CAMERA_WARMUP", "1.5")),
            help="Seconds to wait after starting the Pi camera.",
        )
        parser.add_argument(
            "--jpeg-quality",
            type=int,
            default=int(os.getenv("RPI_AI_JPEG_QUALITY", "85")),
            help="JPEG quality for encoded frames.",
        )
        parser.add_argument(
            "--sample-image-path",
            default=os.getenv("RPI_AI_SAMPLE_IMAGE_PATH"),
            help="Local image path used by file camera mode.",
        )
        parser.add_argument(
            "--model-mode",
            choices=["mock", "ollama"],
            default=os.getenv("RPI_AI_MODEL_MODE", "mock"),
            help="Vision model backend.",
        )
        parser.add_argument(
            "--ollama-base-url",
            default=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            help="Ollama host base URL.",
        )
        parser.add_argument(
            "--ollama-model",
            default=os.getenv("OLLAMA_MODEL", "qwen3-vl"),
            help="Ollama model name.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=os.getenv("RPI_AI_DRY_RUN", "0") == "1",
            help="Log actions without touching real hardware.",
        )
        args = parser.parse_args()
        return cls(
            goal=args.goal,
            max_iterations=args.max_iterations,
            loop_interval_s=args.loop_interval,
            camera_mode=args.camera_mode,
            camera_width=args.camera_width,
            camera_height=args.camera_height,
            camera_warmup_s=args.camera_warmup,
            jpeg_quality=args.jpeg_quality,
            sample_image_path=args.sample_image_path,
            model_mode=args.model_mode,
            ollama_base_url=args.ollama_base_url.rstrip("/"),
            ollama_model=args.ollama_model,
            dry_run=args.dry_run,
        )
