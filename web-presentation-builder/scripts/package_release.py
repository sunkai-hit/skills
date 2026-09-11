from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

from common import load_config, project_root, resolve_path, sha256


def package(config_path: str) -> dict:
    cfg_path, cfg = load_config(config_path)
    root = project_root(cfg_path)
    release = resolve_path(root, cfg['release_dir'])
    qa = resolve_path(root, cfg.get('qa_dir', 'qa'))
    standalone_name = cfg.get('standalone', {}).get('filename', 'Web_Presentation_Standalone.html')
    standalone = release / standalone_name
    if not standalone.exists():
        raise SystemExit(f'Standalone file does not exist: {standalone}')

    html_hash = sha256(standalone)
    (release / 'HTML-SHA256.txt').write_text(f'{html_hash}  {standalone.name}\n', encoding='utf-8')

    zip_name = cfg.get('release', {}).get('zip_filename', 'Web_Presentation.zip')
    zip_path = release / zip_name
    readme = release / 'README.md'
    if not readme.exists():
        readme.write_text(f'# {cfg.get("project_name", "Web Presentation")}\n\nRelease {cfg.get("release_version", "")}\n', encoding='utf-8')

    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.write(standalone, standalone.name)
        z.write(readme, 'README.md')
        z.write(release / 'HTML-SHA256.txt', 'HTML-SHA256.txt')

    version = str(cfg.get('release_version', 'V0.1')).replace('V', 'v').replace(' ', '-')
    contact = qa / f'contact-sheet-{version}.jpg'
    checks = [
        (standalone, standalone.name),
        (zip_path, zip_path.name),
    ]
    if contact.exists():
        checks.append((contact, str(contact.relative_to(root))))
    checksum_text = ''.join(f'{sha256(p)}  {label}\n' for p, label in checks)
    (release / 'SHA256SUMS.txt').write_text(checksum_text, encoding='utf-8')

    report = {
        'standalone': {'path': str(standalone.relative_to(root)), 'bytes': standalone.stat().st_size, 'sha256': sha256(standalone)},
        'zip': {'path': str(zip_path.relative_to(root)), 'bytes': zip_path.stat().st_size, 'sha256': sha256(zip_path)},
        'contact_sheet': str(contact.relative_to(root)) if contact.exists() else None,
    }
    (qa / 'release-build-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('config', nargs='?', default='web-presentation.yaml')
    args = ap.parse_args()
    print(json.dumps(package(args.config), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
