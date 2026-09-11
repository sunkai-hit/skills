from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw

from common import load_config, project_root, resolve_path, sha256


def build(config_path: str) -> dict:
    cfg_path, cfg = load_config(config_path)
    root = project_root(cfg_path)
    qa = resolve_path(root, cfg.get('qa_dir', 'qa'))
    shots_dir = qa / 'screenshots'
    shots = sorted(shots_dir.glob('screen-*.png'))
    if not shots:
        raise SystemExit(f'No screenshots found in {shots_dir}')

    ccfg = cfg.get('contact_sheet', {})
    cols = int(ccfg.get('columns', 5))
    tw = int(ccfg.get('thumb_width', 348))
    th = int(ccfg.get('thumb_height', 196))
    gap = int(ccfg.get('gap', 12))
    label_h = 24
    rows = (len(shots) + cols - 1) // cols
    sw = cols * tw + (cols + 1) * gap
    sh = rows * (th + label_h) + (rows + 1) * gap

    sheet = Image.new('RGB', (sw, sh), '#e8ece8')
    draw = ImageDraw.Draw(sheet)
    for idx, shot in enumerate(shots):
        row, col = divmod(idx, cols)
        x = gap + col * (tw + gap)
        y = gap + row * (th + label_h + gap)
        with Image.open(shot) as im:
            thumb = im.convert('RGB').resize((tw, th), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        draw.text((x + 5, y + th + 4), f'SCREEN {idx + 1:02d}', fill='#264d40')

    version = str(cfg.get('release_version', 'V0.1')).replace('V', 'v').replace(' ', '-')
    out = qa / f'contact-sheet-{version}.jpg'
    sheet.save(out, 'JPEG', quality=88, optimize=True)
    report = {'path': str(out.relative_to(root)), 'bytes': out.stat().st_size, 'sha256': sha256(out), 'screens': len(shots)}
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('config', nargs='?', default='web-presentation.yaml')
    args = ap.parse_args()
    print(json.dumps(build(args.config), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
