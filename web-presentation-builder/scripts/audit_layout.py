from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import subprocess
import tempfile
from pathlib import Path

from common import find_chrome, load_config, project_root, resolve_path

AUDIT_SCRIPT = r'''
<script>
(function(){
  const selector = __SCREEN_SELECTOR__;
  const ignore = __IGNORE_SELECTORS__;
  const minFont = __MIN_FONT__;
  function ignored(el){
    return ignore.some(s => { try { return el.matches(s) || !!el.closest(s); } catch(e) { return false; } });
  }
  function audit(){
    const screens = [...document.querySelectorAll(selector)];
    const result = screens.map((screen, idx) => {
      const sr = screen.getBoundingClientRect();
      let outside = [];
      let tiny = [];
      [...screen.querySelectorAll('*')].forEach(el => {
        if (ignored(el)) return;
        const style = getComputedStyle(el);
        if (style.display === 'none' || style.visibility === 'hidden') return;
        const r = el.getBoundingClientRect();
        if (r.width > 1 && r.height > 1) {
          const tol = 2;
          if (r.left < sr.left - tol || r.right > sr.right + tol || r.top < sr.top - tol || r.bottom > sr.bottom + tol) {
            outside.push({tag:el.tagName, cls:el.className || '', l:Math.round(r.left-sr.left), t:Math.round(r.top-sr.top), r:Math.round(r.right-sr.left), b:Math.round(r.bottom-sr.top)});
          }
          const text = (el.innerText || '').trim();
          if (text && el.children.length === 0) {
            const fs = parseFloat(style.fontSize || '0');
            if (fs && fs < minFont) tiny.push({text:text.slice(0,80), font:fs, tag:el.tagName, cls:el.className || ''});
          }
        }
      });
      return {
        index: idx + 1,
        id: screen.getAttribute('data-screen') || screen.id || String(idx+1),
        clientWidth: screen.clientWidth,
        clientHeight: screen.clientHeight,
        scrollWidth: screen.scrollWidth,
        scrollHeight: screen.scrollHeight,
        overflowX: screen.scrollWidth > screen.clientWidth + 2,
        overflowY: screen.scrollHeight > screen.clientHeight + 2,
        outside: outside.slice(0, 100),
        tinyText: tiny.slice(0, 100)
      };
    });
    const pre = document.createElement('pre');
    pre.id = '__wp_audit__';
    pre.textContent = JSON.stringify({screens: result});
    document.body.innerHTML = '';
    document.body.appendChild(pre);
  }
  if (document.readyState === 'complete') setTimeout(audit, 700);
  else window.addEventListener('load', () => setTimeout(audit, 700));
})();
</script>
'''


def audit(config_path: str) -> dict:
    cfg_path, cfg = load_config(config_path)
    root = project_root(cfg_path)
    source = resolve_path(root, cfg['source_dir'])
    entry = source / cfg.get('entry_html', 'index.html')
    qa = resolve_path(root, cfg.get('qa_dir', 'qa'))
    qa.mkdir(parents=True, exist_ok=True)

    scfg = cfg.get('screen', {})
    selector = scfg.get('selector', '.screen')
    ignore = scfg.get('ignore_overflow_selectors', []) or []
    min_font = float(cfg.get('qa', {}).get('min_critical_font_px', 15))
    script = AUDIT_SCRIPT.replace('__SCREEN_SELECTOR__', json.dumps(selector)).replace('__IGNORE_SELECTORS__', json.dumps(ignore)).replace('__MIN_FONT__', str(min_font))

    source_html = entry.read_text(encoding='utf-8')
    if '</body>' in source_html.lower():
        injected = re.sub(r'</body>', script + '\n</body>', source_html, count=1, flags=re.I)
    else:
        injected = source_html + script

    chrome = find_chrome()
    viewport = cfg.get('viewport', {})
    w, h = int(viewport.get('width', 1920)), int(viewport.get('height', 1080))
    budget = int(cfg.get('render', {}).get('virtual_time_budget_ms', 1800)) + 1200

    with tempfile.NamedTemporaryFile('w', suffix='.html', encoding='utf-8', delete=False, dir=source) as f:
        f.write(injected)
        temp = Path(f.name)
    try:
        cmd = [chrome, '--headless=new', '--disable-gpu', '--no-sandbox', f'--window-size={w},{h}', f'--virtual-time-budget={budget}', '--dump-dom', temp.resolve().as_uri()]
        try:
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=int(cfg.get('render', {}).get('chrome_timeout_seconds', 45)))
        except subprocess.TimeoutExpired:
            raise SystemExit('Chrome layout audit timed out. Increase render.chrome_timeout_seconds or use --skip-layout-audit while investigating the page.')
        if proc.returncode != 0:
            raise SystemExit(f'Chrome layout audit failed: {proc.stderr[-1500:]}')
        match = re.search(r'<pre id="__wp_audit__">(.*?)</pre>', proc.stdout, re.S)
        if not match:
            raise SystemExit('Layout audit payload was not produced. Ensure screen DOM is available after load.')
        payload = json.loads(html_lib.unescape(match.group(1)))
    finally:
        temp.unlink(missing_ok=True)

    critical = []
    warnings = []
    for s in payload.get('screens', []):
        if s['overflowX'] or s['overflowY']:
            critical.append({'screen': s['id'], 'type': 'screen-overflow', 'x': s['overflowX'], 'y': s['overflowY']})
        if s['outside']:
            warnings.append({'screen': s['id'], 'type': 'descendant-outside', 'count': len(s['outside']), 'samples': s['outside'][:8]})
        if s['tinyText']:
            warnings.append({'screen': s['id'], 'type': 'tiny-text', 'count': len(s['tinyText']), 'samples': s['tinyText'][:8]})
    report = {'viewport': [w, h], 'critical': critical, 'warnings': warnings, **payload}
    (qa / 'layout-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('config', nargs='?', default='web-presentation.yaml')
    args = ap.parse_args()
    report = audit(args.config)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report['critical']:
        raise SystemExit(3)


if __name__ == '__main__':
    main()
