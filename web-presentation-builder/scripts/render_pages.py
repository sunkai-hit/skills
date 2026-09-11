from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from common import find_chrome, load_config, project_root, resolve_path


def render(config_path: str, html_path: str | None = None) -> dict:
    cfg_path, cfg = load_config(config_path)
    root = project_root(cfg_path)
    source = resolve_path(root, cfg['source_dir'])
    qa = resolve_path(root, cfg.get('qa_dir', 'qa'))
    entry = resolve_path(root, html_path) if html_path else source / cfg.get('entry_html', 'index.html')
    shots_dir = qa / 'screenshots'
    if shots_dir.exists():
        shutil.rmtree(shots_dir)
    shots_dir.mkdir(parents=True, exist_ok=True)

    viewport = cfg.get('viewport', {})
    width, height = int(viewport.get('width', 1920)), int(viewport.get('height', 1080))
    screen_cfg = cfg.get('screen', {})
    count = int(screen_cfg.get('expected_count', 1))
    render_cfg = cfg.get('render', {})
    use_hash = bool(render_cfg.get('hash_navigation', True))
    fmt = render_cfg.get('hash_format', '{screen:02d}')
    budget = int(render_cfg.get('virtual_time_budget_ms', 1800))
    chrome = find_chrome()

    outputs = []
    base_uri = entry.resolve().as_uri()
    for i in range(1, count + 1):
        shot = shots_dir / f'screen-{i:02d}.png'
        target = f'{base_uri}#{fmt.format(screen=i)}' if use_hash else base_uri
        cmd = [
            chrome, '--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
            f'--window-size={width},{height}', '--force-device-scale-factor=1',
            f'--virtual-time-budget={budget}', f'--screenshot={shot}', target,
        ]
        try:
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=int(render_cfg.get('chrome_timeout_seconds', 45)))
        except subprocess.TimeoutExpired:
            raise SystemExit(f'Chrome render timed out for screen {i:02d}. Increase render.chrome_timeout_seconds or inspect page load loops.')
        if proc.returncode != 0 or not shot.exists():
            raise SystemExit(f'Chrome render failed for screen {i:02d}: {proc.stderr[-1500:]}')
        outputs.append(str(shot.relative_to(root)))

    report = {'html': str(entry.relative_to(root)), 'viewport': [width, height], 'screenshots': outputs}
    (qa / 'render-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('config', nargs='?', default='web-presentation.yaml')
    ap.add_argument('--html', help='Optional HTML path relative to project root; defaults to modular entry.')
    args = ap.parse_args()
    print(json.dumps(render(args.config, args.html), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
