from __future__ import annotations

import hashlib
import mimetypes
import shutil
from pathlib import Path
from typing import Any

import yaml

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}


def load_config(path: str | Path) -> tuple[Path, dict[str, Any]]:
    config_path = Path(path).resolve()
    data = yaml.safe_load(config_path.read_text(encoding='utf-8')) or {}
    return config_path, data


def project_root(config_path: Path) -> Path:
    return config_path.parent.resolve()


def resolve_path(root: Path, value: str | Path) -> Path:
    p = Path(value)
    return p if p.is_absolute() else (root / p).resolve()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def find_chrome() -> str:
    for name in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'):
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit('Chrome/Chromium is required but was not found in PATH.')


def mime_for_image(path: Path) -> str:
    ext = path.suffix.lower()
    explicit = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.webp': 'image/webp',
        '.gif': 'image/gif',
    }
    return explicit.get(ext) or mimetypes.guess_type(path.name)[0] or 'application/octet-stream'


def iter_images(source_dir: Path):
    for p in source_dir.rglob('*'):
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS:
            yield p
