from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script: str, config: str, extra: list[str] | None = None):
    cmd = [sys.executable, str(HERE / script), config, *(extra or [])]
    proc = subprocess.run(cmd, text=True)
    if proc.returncode:
        raise SystemExit(proc.returncode)


def main():
    ap = argparse.ArgumentParser(description='Finalize a Web Presentation release using the reusable skill pipeline.')
    ap.add_argument('config', nargs='?', default='web-presentation.yaml')
    ap.add_argument('--skip-layout-audit', action='store_true')
    args = ap.parse_args()

    run('audit_source.py', args.config)
    run('validate_assets.py', args.config)
    if not args.skip_layout_audit:
        run('audit_layout.py', args.config)
    run('build_standalone.py', args.config)

    # Render standalone rather than modular source for final release verification.
    import yaml
    cfg = yaml.safe_load(Path(args.config).read_text(encoding='utf-8'))
    standalone_rel = str(Path(cfg['release_dir']) / cfg.get('standalone', {}).get('filename', 'Web_Presentation_Standalone.html'))
    run('render_pages.py', args.config, ['--html', standalone_rel])
    run('build_contact_sheet.py', args.config)
    run('package_release.py', args.config)
    print(json.dumps({'status': 'success', 'config': args.config}, ensure_ascii=False))


if __name__ == '__main__':
    main()
