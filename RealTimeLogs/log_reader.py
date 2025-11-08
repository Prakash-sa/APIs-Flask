"""Utility helpers for reading and appending to large log files."""

from __future__ import annotations

import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Tuple

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_FILE = LOG_DIR / "sample.log"
_LOCK = threading.Lock()


def _ensure_file() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE.touch(exist_ok=True)


def append_log_entry(message: str) -> None:
    """Append a timestamped message to the shared log file."""
    _ensure_file()
    timestamp = datetime.utcnow().isoformat(timespec="seconds")
    line = f"{timestamp} | {message.strip()}\n"
    with _LOCK:
        with LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(line)


def read_latest_lines(max_lines: int = 100) -> List[str]:
    """Return the last `max_lines` log entries."""
    _ensure_file()
    with _LOCK:
        with LOG_FILE.open("r", encoding="utf-8") as handle:
            lines = handle.readlines()
    return [line.rstrip("\n") for line in lines[-max_lines:]]


def read_new_lines(last_position: int = 0) -> Tuple[List[str], int]:
    """Read log entries written after `last_position`."""
    _ensure_file()
    with _LOCK:
        with LOG_FILE.open("r", encoding="utf-8") as handle:
            handle.seek(last_position)
            data = handle.read()
            new_position = handle.tell()
    lines = [line for line in data.splitlines() if line]
    return lines, new_position


def follow_log(start_at_end: bool = True, poll_interval: float = 1.0) -> Iterable[str]:
    """Yield log lines as they are appended, similar to `tail -f`."""
    _ensure_file()
    position = LOG_FILE.stat().st_size if start_at_end else 0
    while True:
        lines, position = read_new_lines(position)
        if lines:
            for line in lines:
                yield line
        else:
            time.sleep(poll_interval)
