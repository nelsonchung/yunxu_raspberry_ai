from __future__ import annotations

import ast
import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


REPO_ROOT = Path(__file__).resolve().parents[4]
CONFIG_DIR = REPO_ROOT / "config"
DEFAULTS_CONFIG_PATH = CONFIG_DIR / "defaults.toml"
USER_CONFIG_PATH = CONFIG_DIR / "user.toml"


def _parse_bool(raw: Any) -> bool:
    if isinstance(raw, bool):
        return raw
    text = str(raw).strip().lower()
    if text in {"1", "true", "yes", "on"}:
        return True
    if text in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"invalid boolean value: {raw!r}")


def _strip_inline_comment(line: str) -> str:
    in_quote = False
    escaped = False
    result = []
    for char in line:
        if char == '"' and not escaped:
            in_quote = not in_quote
        if char == "#" and not in_quote:
            break
        result.append(char)
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    return "".join(result).strip()


def _parse_toml_value(raw: str) -> Any:
    value = raw.strip()
    if value.startswith('"') and value.endswith('"'):
        return ast.literal_eval(value)
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        if any(token in value for token in [".", "e", "E"]):
            return float(value)
        return int(value)
    except ValueError:
        return value


def _load_simple_toml(path: Path) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    if not path.exists():
        return data

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = _strip_inline_comment(raw_line)
        if not line:
            continue
        if line.startswith("["):
            raise ValueError(
                f"unsupported TOML section in {path} at line {line_number}: {raw_line}"
            )
        if "=" not in line:
            raise ValueError(f"invalid config line in {path} at line {line_number}: {raw_line}")
        key, raw_value = line.split("=", 1)
        data[key.strip()] = _parse_toml_value(raw_value)
    return data


def _base_defaults() -> Dict[str, Any]:
    return {
        "app_mode": "search",
        "goal": "find toy",
        "max_iterations": 8,
        "loop_interval_s": 1.0,
        "camera_mode": "mock",
        "camera_width": 640,
        "camera_height": 480,
        "camera_warmup_s": 1.5,
        "jpeg_quality": 85,
        "sample_image_path": None,
        "model_mode": "mock",
        "ollama_base_url": "http://192.168.8.166:11434",
        "ollama_model": "qwen3.5:2b",
        "ollama_timeout_s": 180.0,
        "describe_prompt": "請用繁體中文解讀這張圖片，描述場景、主要物件，以及你注意到的重要細節。",
        "debug_save_frame_path": None,
        "timing_enabled": False,
        "dry_run": False,
    }


def _normalize_loaded_settings(raw_settings: Dict[str, Any]) -> Dict[str, Any]:
    allowed_keys = set(_base_defaults().keys())
    unknown_keys = sorted(set(raw_settings.keys()) - allowed_keys)
    if unknown_keys:
        raise ValueError(f"unknown config keys: {', '.join(unknown_keys)}")

    normalized = dict(raw_settings)
    for optional_key in ["sample_image_path", "debug_save_frame_path"]:
        if optional_key in normalized and normalized[optional_key] == "":
            normalized[optional_key] = None
    return normalized


def _env_overrides() -> Dict[str, Any]:
    env_map = {
        "app_mode": ("RPI_AI_APP_MODE", str),
        "goal": ("RPI_AI_GOAL", str),
        "max_iterations": ("RPI_AI_MAX_ITERATIONS", int),
        "loop_interval_s": ("RPI_AI_LOOP_INTERVAL", float),
        "camera_mode": ("RPI_AI_CAMERA_MODE", str),
        "camera_width": ("RPI_AI_CAMERA_WIDTH", int),
        "camera_height": ("RPI_AI_CAMERA_HEIGHT", int),
        "camera_warmup_s": ("RPI_AI_CAMERA_WARMUP", float),
        "jpeg_quality": ("RPI_AI_JPEG_QUALITY", int),
        "sample_image_path": ("RPI_AI_SAMPLE_IMAGE_PATH", str),
        "model_mode": ("RPI_AI_MODEL_MODE", str),
        "ollama_base_url": ("OLLAMA_BASE_URL", str),
        "ollama_model": ("OLLAMA_MODEL", str),
        "ollama_timeout_s": ("OLLAMA_TIMEOUT_S", float),
        "describe_prompt": ("RPI_AI_DESCRIBE_PROMPT", str),
        "debug_save_frame_path": ("RPI_AI_DEBUG_SAVE_FRAME_PATH", str),
        "timing_enabled": ("RPI_AI_TIMING", _parse_bool),
        "dry_run": ("RPI_AI_DRY_RUN", _parse_bool),
    }
    overrides: Dict[str, Any] = {}
    for key, (env_name, caster) in env_map.items():
        raw_value = os.getenv(env_name)
        if raw_value is None:
            continue
        overrides[key] = caster(raw_value)

    for optional_key in ["sample_image_path", "debug_save_frame_path"]:
        if overrides.get(optional_key) == "":
            overrides[optional_key] = None
    return overrides


def _resolve_initial_settings(
    defaults_config_path: Path,
    user_config_path: Optional[Path],
) -> Dict[str, Any]:
    settings = _base_defaults()
    settings.update(_normalize_loaded_settings(_load_simple_toml(defaults_config_path)))
    if user_config_path is not None:
        settings.update(_normalize_loaded_settings(_load_simple_toml(user_config_path)))
    settings.update(_env_overrides())
    return settings


@dataclass
class RuntimeConfig:
    app_mode: str
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
    ollama_timeout_s: float
    describe_prompt: str
    debug_save_frame_path: Optional[str]
    timing_enabled: bool
    dry_run: bool

    @classmethod
    def from_args(cls):
        pre_parser = argparse.ArgumentParser(add_help=False)
        pre_parser.add_argument(
            "--config-file",
            default=os.getenv("RPI_AI_CONFIG_FILE", str(DEFAULTS_CONFIG_PATH)),
        )
        pre_parser.add_argument(
            "--user-config-file",
            default=os.getenv("RPI_AI_USER_CONFIG_FILE", str(USER_CONFIG_PATH)),
        )
        pre_parser.add_argument(
            "--no-user-config",
            action="store_true",
            default=_parse_bool(os.getenv("RPI_AI_NO_USER_CONFIG", "false")),
        )
        pre_args, _ = pre_parser.parse_known_args()

        defaults_config_path = Path(pre_args.config_file).expanduser()
        user_config_path = None
        if not pre_args.no_user_config:
            user_config_path = Path(pre_args.user_config_file).expanduser()

        settings = _resolve_initial_settings(
            defaults_config_path=defaults_config_path,
            user_config_path=user_config_path,
        )

        parser = argparse.ArgumentParser(
            description="Run the Raspberry Pi AI car main loop."
        )
        parser.add_argument(
            "--config-file",
            default=str(defaults_config_path),
            help="Path to the project defaults TOML file.",
        )
        parser.add_argument(
            "--user-config-file",
            default=str(user_config_path) if user_config_path is not None else "",
            help="Path to the user override TOML file.",
        )
        parser.add_argument(
            "--no-user-config",
            action="store_true",
            default=pre_args.no_user_config,
            help="Ignore the user override TOML file.",
        )
        parser.add_argument(
            "--app-mode",
            choices=["search", "describe"],
            default=settings["app_mode"],
            help="Application mode.",
        )
        parser.add_argument(
            "--goal",
            default=settings["goal"],
            help="Mission goal text.",
        )
        parser.add_argument(
            "--max-iterations",
            type=int,
            default=settings["max_iterations"],
            help="Maximum search iterations before stopping.",
        )
        parser.add_argument(
            "--loop-interval",
            type=float,
            default=settings["loop_interval_s"],
            help="Seconds to wait between iterations.",
        )
        parser.add_argument(
            "--camera-mode",
            choices=["mock", "file", "pi"],
            default=settings["camera_mode"],
            help="Camera provider implementation.",
        )
        parser.add_argument(
            "--camera-width",
            type=int,
            default=settings["camera_width"],
            help="Capture width for Pi camera mode.",
        )
        parser.add_argument(
            "--camera-height",
            type=int,
            default=settings["camera_height"],
            help="Capture height for Pi camera mode.",
        )
        parser.add_argument(
            "--camera-warmup",
            type=float,
            default=settings["camera_warmup_s"],
            help="Seconds to wait after starting the Pi camera.",
        )
        parser.add_argument(
            "--jpeg-quality",
            type=int,
            default=settings["jpeg_quality"],
            help="JPEG quality for encoded frames.",
        )
        parser.add_argument(
            "--sample-image-path",
            default=settings["sample_image_path"],
            help="Local image path used by file camera mode.",
        )
        parser.add_argument(
            "--model-mode",
            choices=["mock", "ollama"],
            default=settings["model_mode"],
            help="Vision model backend.",
        )
        parser.add_argument(
            "--ollama-base-url",
            default=settings["ollama_base_url"],
            help="Ollama host base URL.",
        )
        parser.add_argument(
            "--ollama-model",
            default=settings["ollama_model"],
            help="Ollama model name.",
        )
        parser.add_argument(
            "--ollama-timeout",
            type=float,
            default=settings["ollama_timeout_s"],
            help="Timeout in seconds for each Ollama request.",
        )
        parser.add_argument(
            "--describe-prompt",
            default=settings["describe_prompt"],
            help="Prompt used by describe mode.",
        )
        parser.add_argument(
            "--debug-save-frame-path",
            default=settings["debug_save_frame_path"],
            help="Optional JPEG path for saving the latest captured frame.",
        )
        parser.add_argument(
            "--timing",
            action="store_true",
            default=settings["timing_enabled"],
            help="Print per-stage timing for performance analysis.",
        )
        parser.add_argument(
            "--no-timing",
            action="store_false",
            dest="timing",
            help="Disable timing output even if enabled in config or env.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=settings["dry_run"],
            help="Log actions without touching real hardware.",
        )
        parser.add_argument(
            "--no-dry-run",
            action="store_false",
            dest="dry_run",
            help="Disable dry-run even if it is enabled in config or env.",
        )
        args = parser.parse_args()
        return cls(
            app_mode=args.app_mode,
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
            ollama_timeout_s=args.ollama_timeout,
            describe_prompt=args.describe_prompt,
            debug_save_frame_path=args.debug_save_frame_path,
            timing_enabled=args.timing,
            dry_run=args.dry_run,
        )
