from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from common import load_config, project_root, resolve_path

REF_RE = re.compile(r'\b(?:src|href|poster)=["\']([^"\']+)["\']', re.I)
SCREEN_PATTERNS = [
    re.compile(r'data-screen\s*=\s*["\'](\d{1,3})["\']'),
    re.compile(r'data-screen\\?=[\\"\']+(\d{1,3})'),
]


def is_external(url: str) -> bool:
    return url.startswith(('http://', 'https://', '//', 'data:', '#', 'mailto:', 'tel:', 'javascript:'))


def audit(config_path: str) -> dict:
    cfg_path, cfg = load_config(config_path)
    root = project_root(cfg_path)
    source = resolve_path(root, cfg['source_dir'])
    qa = resolve_path(root, cfg.get('qa_dir', 'qa'))
    qa.mkdir(parents=True, exist_ok=True)
    entry = source / cfg.get('entry_html', 'index.html')
    if not entry.exists():
        raise SystemExit(f'Entry HTML not found: {entry}')

    html = entry.read_text(encoding='utf-8')
    refs = []
    missing = []
    for url in REF_RE.findall(html):
        if is_external(url):
            continue
        clean = urlparse(url).path
        if not clean:
            continue
        refs.append(clean)
        p = (source / clean).resolve()
        if not p.exists():
            missing.append(clean)

    text_sources = [entry]
    text_sources.extend(sorted(source.rglob('*.js')))
    screen_ids = set()
    for p in text_sources:
        try:
            text = p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        for pat in SCREEN_PATTERNS:
            screen_ids.update(pat.findall(text))

    expected_count = int(cfg.get('screen', {}).get('expected_count', 0) or 0)
    normalized = sorted({str(int(x)).zfill(2) for x in screen_ids}, key=int)
    expected = [str(i).zfill(2) for i in range(1, expected_count + 1)] if expected_count else []
    screen_ok = not expected or normalized == expected

    node = shutil.which('node')
    js_syntax = {}
    js_errors = []
    for p in sorted(source.rglob('*.js')):
        rel = str(p.relative_to(root))
        if not node:
            js_syntax[rel] = None
            continue
        proc = subprocess.run([node, '--check', str(p)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        ok = proc.returncode == 0
        js_syntax[rel] = ok
        if not ok:
            js_errors.append({'path': rel, 'error': proc.stderr.strip()[-1200:]})

    report = {
        'entry_html': str(entry.relative_to(root)),
        'local_refs': sorted(set(refs)),
        'missing_refs': sorted(set(missing)),
        'screen_ids': normalized,
        'expected_screen_ids': expected,
        'screen_ids_ok': screen_ok,
        'js_syntax': js_syntax,
        'js_errors': js_errors,
        'ok': not missing and screen_ok and not js_errors,
    }
    (qa / 'source-reference-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('config', nargs='?', default='web-presentation.yaml')
    args = ap.parse_args()
    report = audit(args.config)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report['ok']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
