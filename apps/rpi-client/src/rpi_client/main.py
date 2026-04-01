from __future__ import annotations

import sys

from rpi_client.camera.file_camera import FileCamera
from rpi_client.camera.mock_camera import MockCamera
from rpi_client.camera.pi_camera import PiCamera
from rpi_client.config import RuntimeConfig
from rpi_client.model.mock_vision import MockVisionEngine
from rpi_client.model.ollama_adapter import OllamaVisionEngine
from rpi_client.motor.mock_motor import MockMotorController
from rpi_client.runtime import SearchRuntime


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
        motor_controller = build_motor_controller(config)
        runtime = SearchRuntime(config, camera, vision_engine, motor_controller)
        return runtime.run()
    except Exception as exc:
        print(f"[startup-error] {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
