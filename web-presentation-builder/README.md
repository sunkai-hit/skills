# web-presentation-builder

A reusable, staged workflow skill for designing, implementing, QA-ing, packaging, and releasing professional Web Presentation projects.

## What it standardizes

- guided requirement/content framing;
- page architecture before implementation;
- visual baseline and key-screen approval;
- 1920×1080 full-screen presentation layouts;
- readable typography and compact hub/detail structures;
- modular HTML/CSS/JS source;
- standalone single-file HTML;
- robust image validation before Base64 embedding;
- browser rendering and Contact Sheet QA;
- versioned release packaging;
- GitHub Actions finalization;
- persistent project state for future continuation.

## Recommended usage

Start a new project:

> Use `web-presentation-builder` to turn these materials into a leadership-facing Web Presentation. Start with source understanding and content architecture; do not build all pages yet.

Continue a project:

> Continue this Web Presentation from the repository baseline. Read `.project/project-state.yaml` first and resume from the recorded stage.

Revise selected screens:

> Use revision mode. Update screens 02, 09, 14 and the global small-text size, then run full regression QA and rebuild the standalone release.

## Dependencies for helper scripts

- Python 3.10+
- Pillow
- PyYAML
- Chromium / Google Chrome for rendering and layout audits
- Node.js is optional but recommended for JS syntax checking

Install Python dependencies:

```bash
python -m pip install pillow pyyaml
```

## Project integration

Copy `templates/project-state.yaml` into the target repository as `.project/project-state.yaml`, then adapt `examples/minimal-project/web-presentation.yaml` to the project.

The scripts are intentionally generic and do not contain project-specific business terms, brand names, or content.
