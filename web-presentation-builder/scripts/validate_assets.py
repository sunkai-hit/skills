from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

from common import iter_images, load_config, project_root, resolve_path, sha256


def validate(config_path: str) -> dict:
    cfg_path, cfg = load_config(config_path)
    root = project_root(cfg_path)
    source = resolve_path(root, cfg['source_dir'])
    asset_cfg = cfg.get('assets', {})
    min_w = int(asset_cfg.get('min_width', 1))
    min_h = int(asset_cfg.get('min_height', 1))
    min_bytes = int(asset_cfg.get('min_bytes', 1))

    results = []
    errors = []
    warnings = []

    for path in iter_images(source):
        item = {
            'path': str(path.relative_to(root)),
            'bytes': path.stat().st_size,
            'sha256': sha256(path),
        }
        try:
            with Image.open(path) as im:
                im.load()  # detect truncated/broken streams, not just headers
                item.update(format=im.format, width=im.width, height=im.height, mode=im.mode)
                if im.width < min_w or im.height < min_h:
                    warnings.append(f'Low-resolution image: {item["path"]} ({im.width}x{im.height})')
            if path.stat().st_size < min_bytes:
                warnings.append(f'Suspiciously small image file: {item["path"]} ({path.stat().st_size} bytes)')
        except Exception as exc:
            item['error'] = str(exc)
            errors.append(f'Invalid image: {item["path"]}: {exc}')
        results.append(item)

    return {
        'source_dir': str(source),
        'images': results,
        'errors': errors,
        'warnings': warnings,
        'ok': not errors,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('config', nargs='?', default='web-presentation.yaml')
    ap.add_argument('--output')
    args = ap.parse_args()
    report = validate(args.config)
    text = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        Path(args.output).write_text(text, encoding='utf-8')
    print(text, end='')
    if not report['ok']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
