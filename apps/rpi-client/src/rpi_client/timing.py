from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator


def now() -> float:
    return time.perf_counter()


def elapsed_ms(start: float) -> float:
    return (time.perf_counter() - start) * 1000.0


def format_ms(value: float) -> str:
    return f"{value:.1f} ms"


def log_timing(enabled: bool, label: str, value_ms: float) -> None:
    if enabled:
        print(f"[timing] {label}={format_ms(value_ms)}")


@contextmanager
def timed(enabled: bool, label: str) -> Iterator[None]:
    start = now()
    try:
        yield
    finally:
        log_timing(enabled, label, elapsed_ms(start))
