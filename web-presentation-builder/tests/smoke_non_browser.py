from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples' / 'minimal-project'
SCRIPTS = ROOT / 'scripts'


def run(script: str, config: Path):
    proc = subprocess.run([sys.executable, str(SCRIPTS / script), str(config)], capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(f'{script} failed:\n{proc.stdout}\n{proc.stderr}')
    return proc.stdout


def main():
    # Work on a temporary copy so the packaged example remains clean.
    with tempfile.TemporaryDirectory() as td:
        dst = Path(td) / 'project'
        import shutil
        shutil.copytree(EXAMPLE, dst)
        cfg = dst / 'web-presentation.yaml'
        run('audit_source.py', cfg)
        run('validate_assets.py', cfg)
        out = json.loads(run('build_standalone.py', cfg))
        standalone = dst / out['path']
        assert standalone.exists()
        assert out['remaining_local_dependencies'] == []
        assert out['embedded_images']
        print('smoke_non_browser: PASS')


if __name__ == '__main__':
    main()
