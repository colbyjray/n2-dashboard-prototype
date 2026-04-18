"""Stdlib logging config."""
from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure(level: str, file_path: str | Path) -> None:
    p = Path(file_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    root = logging.getLogger()
    root.setLevel(level.upper())
    root.handlers.clear()

    stream = logging.StreamHandler()
    stream.setFormatter(fmt)
    root.addHandler(stream)

    rotating = RotatingFileHandler(p, maxBytes=5_000_000, backupCount=5)
    rotating.setFormatter(fmt)
    root.addHandler(rotating)
