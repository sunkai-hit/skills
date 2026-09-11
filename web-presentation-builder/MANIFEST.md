# Package Manifest

## Core
- `SKILL.md` — skill behavior, triggers, stage gates, modes, release definition of done.
- `README.md` — usage and dependency overview.
- `CHANGELOG.md` — skill version history.
- `requirements.txt` — Python helper dependencies.

## Templates
Reusable project memory, content, design, QA, revision, and release templates.

## References
Reusable rules for workflow, guided dialogue, layout, typography, visualization, interaction, assets, QA, GitHub release, and known anti-patterns.

## Scripts
- `audit_source.py` — missing local refs, screen ID coverage, JS syntax.
- `validate_assets.py` — full raster decode validation, dimensions, hashes.
- `audit_layout.py` — browser-based overflow and tiny-text audit.
- `build_standalone.py` — inline CSS/JS/images and revalidate embedded image bytes.
- `render_pages.py` — 1920×1080 (configurable) browser screenshots.
- `build_contact_sheet.py` — whole-deck visual review sheet.
- `package_release.py` — ZIP, hashes, release audit.
- `finalize_release.py` — orchestration pipeline.

## GitHub
Reusable Actions workflow template with recursive-bot-trigger protection.

## Example
A neutral 3-screen example used to verify the non-browser build pipeline. It contains no project-specific business content.
