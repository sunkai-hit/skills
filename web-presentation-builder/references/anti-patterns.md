# Anti-patterns and Recovery Rules

## Anti-pattern: full build before narrative approval
Consequence: many later changes become structural instead of local.
Recovery: pause production, establish a content baseline, then resume.

## Anti-pattern: decorative image dumping
Consequence: the result looks like pasted slides rather than an integrated web presentation.
Recovery: rebuild the page from layout, typography, shapes, diagrams, and only necessary imagery.

## Anti-pattern: shrinking all secondary text
Consequence: a page fits technically but becomes unreadable on a large screen.
Recovery: simplify content and reflow components before reducing type size.

## Anti-pattern: hub/details too far apart
Consequence: total/sub-part relationships become weak and peripheral cards feel unimportant.
Recovery: pull detail cards inward, enlarge them, shorten connectors, and reduce empty gaps.

## Anti-pattern: CI success treated as business success
Consequence: the workflow may complete while stale inputs are rebuilt.
Recovery: compare source and output dimensions/hashes, then inspect the generated contact sheet and release audit.

## Anti-pattern: a build script restores an old generated asset over a new source asset
Consequence: user replacements silently disappear.
Recovery: source assets must be authoritative. Generated derivatives may be overwritten; source files must not be restored from stale Base64/checkpoint data during normal finalization.

## Anti-pattern: Base64 exists, therefore image is assumed valid
Consequence: broken source bytes are faithfully embedded and still fail to display.
Recovery: decode source image -> encode -> re-decode Data URI -> image verify -> browser render.

## Anti-pattern: reporting completion before repository write/release
Consequence: user believes a revision is published when only analysis or local editing happened.
Recovery: use explicit lifecycle status and include commit/workflow/artifact verification in the definition of done.
