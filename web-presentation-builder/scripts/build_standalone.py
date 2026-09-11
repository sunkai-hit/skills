from __future__ import annotations

import argparse
import base64
import html as html_lib
import json
import re
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote, urlparse

from PIL import Image

from common import load_config, mime_for_image, project_root, resolve_path, sha256

LINK_RE = re.compile(r'<link\b[^>]*?rel=["\']stylesheet["\'][^>]*?href=["\']([^"\']+)["\'][^>]*?>', re.I)
SCRIPT_RE = re.compile(r'<script\b[^>]*?src=["\']([^"\']+)["\'][^>]*?>\s*</script>', re.I | re.S)
ATTR_IMAGE_RE = re.compile(r'(?P<prefix>\b(?:src|poster)=["\'])(?P<url>[^"\']+)(?P<suffix>["\'])', re.I)
CSS_URL_RE = re.compile(r'url\((?P<q>["\']?)(?P<url>[^)"\']+)(?P=q)\)', re.I)


def is_external(url: str) -> bool:
    u = url.strip()
    return u.startswith(('data:', 'http://', 'https://', '//', '#', 'mailto:', 'tel:', 'javascript:'))


def local_path(base: Path, url: str) -> Path:
    parsed = urlparse(url)
    clean = unquote(parsed.path)
    return (base / clean).resolve()


def validate_and_data_uri(path: Path) -> tuple[str, dict]:
    raw = path.read_bytes()
    with Image.open(BytesIO(raw)) as im:
        im.load()
        meta = {'format': im.format, 'width': im.width, 'height': im.height, 'mode': im.mode}
    mime = mime_for_image(path)
    encoded = base64.b64encode(raw).decode('ascii')
    decoded = base64.b64decode(encoded, validate=True)
    if decoded != raw:
        raise SystemExit(f'Base64 round-trip mismatch: {path}')
    with Image.open(BytesIO(decoded)) as verify:
        verify.verify()
    meta.update(bytes=len(raw), sha256=sha256(path), mime=mime)
    return f'data:{mime};base64,{encoded}', meta


def replace_css_urls(css: str, css_file: Path, source_dir: Path, audit: list[dict]) -> str:
    def repl(match):
        url = match.group('url').strip()
        if is_external(url):
            return match.group(0)
        asset = local_path(css_file.parent, url)
        if not asset.exists():
            raise SystemExit(f'Missing CSS asset: {url} referenced by {css_file}')
        if asset.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp', '.gif'}:
            return match.group(0)  # do not inline fonts by default
        uri, meta = validate_and_data_uri(asset)
        audit.append({'source': str(asset.relative_to(source_dir.parent)), **meta})
        return f'url("{uri}")'
    return CSS_URL_RE.sub(repl, css)


def build(config_path: str) -> dict:
    cfg_path, cfg = load_config(config_path)
    root = project_root(cfg_path)
    source = resolve_path(root, cfg['source_dir'])
    release = resolve_path(root, cfg['release_dir'])
    entry = source / cfg.get('entry_html', 'index.html')
    standalone_cfg = cfg.get('standalone', {})
    out_name = standalone_cfg.get('filename', 'Web_Presentation_Standalone.html')
    out = release / out_name
    release.mkdir(parents=True, exist_ok=True)

    html = entry.read_text(encoding='utf-8')
    image_audit: list[dict] = []

    # Inline local stylesheets; also inline raster assets referenced from CSS.
    def link_repl(match):
        url = match.group(1)
        if is_external(url):
            return match.group(0)
        css_path = local_path(source, url)
        if not css_path.exists():
            raise SystemExit(f'Missing stylesheet: {url}')
        css = css_path.read_text(encoding='utf-8')
        css = replace_css_urls(css, css_path, source, image_audit)
        return f'<style data-inline-from="{html_lib.escape(url)}">\n{css}\n</style>'

    html = LINK_RE.sub(link_repl, html)

    # Inline local scripts.
    def script_repl(match):
        url = match.group(1)
        if is_external(url):
            return match.group(0)
        js_path = local_path(source, url)
        if not js_path.exists():
            raise SystemExit(f'Missing script: {url}')
        js = js_path.read_text(encoding='utf-8')
        return f'<script data-inline-from="{html_lib.escape(url)}">\n{js}\n</script>'

    html = SCRIPT_RE.sub(script_repl, html)

    # Inline raster src/poster attributes.
    if standalone_cfg.get('inline_local_images', True):
        def image_repl(match):
            url = match.group('url')
            if is_external(url):
                return match.group(0)
            path = local_path(source, url)
            if not path.exists() or path.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp', '.gif'}:
                return match.group(0)
            uri, meta = validate_and_data_uri(path)
            image_audit.append({'source': str(path.relative_to(root)), **meta})
            return f'{match.group("prefix")}{uri}{match.group("suffix")}'
        html = ATTR_IMAGE_RE.sub(image_repl, html)

    # Check for remaining local CSS/JS/image dependencies.
    remaining = []
    for m in re.finditer(r'\b(?:src|href|poster)=["\']([^"\']+)["\']', html, re.I):
        url = m.group(1)
        if is_external(url):
            continue
        suffix = Path(urlparse(url).path).suffix.lower()
        if suffix in {'.css', '.js', '.png', '.jpg', '.jpeg', '.webp', '.gif'}:
            remaining.append(url)
    if remaining:
        raise SystemExit(f'Uninlined local dependencies: {sorted(set(remaining))}')

    out.write_text(html, encoding='utf-8')
    audit = {
        'path': str(out.relative_to(root)),
        'bytes': out.stat().st_size,
        'sha256': sha256(out),
        'embedded_images': image_audit,
        'remaining_local_dependencies': remaining,
    }
    audit_path = release / 'standalone-build-audit.json'
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return audit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('config', nargs='?', default='web-presentation.yaml')
    args = ap.parse_args()
    print(json.dumps(build(args.config), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
