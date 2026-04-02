from __future__ import annotations

import sys

from .camera.file_camera import FileCamera
from .camera.mock_camera import MockCamera
from .camera.pi_camera import PiCamera
from .config import RuntimeConfig
from .describe_runtime import DescribeRuntime
from .model.mock_vision import MockVisionEngine
from .model.ollama_adapter import OllamaVisionEngine
from .motor.mock_motor import MockMotorController
from .runtime import SearchRuntime


def build_camera(config: RuntimeConfig):
    if config.camera_mode == "pi":
        return PiCamera(
            width=config.camera_width,
            height=config.camera_height,
            warmup_s=config.camera_warmup_s,
            jpeg_quality=config.jpeg_quality,
        )
    if config.camera_mode == "file":
        if not config.sample_image_path:
            raise ValueError("--sample-image-path is required when --camera-mode=file")
        return FileCamera(config.sample_image_path)
    return MockCamera()


def build_vision_engine(config: RuntimeConfig):
    if config.model_mode == "ollama":
        return OllamaVisionEngine(
            base_url=config.ollama_base_url,
            model=config.ollama_model,
            timeout_s=config.ollama_timeout_s,
            timing_enabled=config.timing_enabled,
        )
    return MockVisionEngine()


def build_motor_controller(config: RuntimeConfig):
    _ = config
    return MockMotorController()


def main() -> int:
    try:
        config = RuntimeConfig.from_args()
        camera = build_camera(config)
        vision_engine = build_vision_engine(config)
        if config.app_mode == "describe":
            runtime = DescribeRuntime(config, camera, vision_engine)
            return runtime.run()

        motor_controller = build_motor_controller(config)
        runtime = SearchRuntime(config, camera, vision_engine, motor_controller)
        return runtime.run()
    except Exception as exc:
        print(f"[startup-error] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
