---
name: web-presentation-builder
description: Create, continue, revise, QA, package, and release professional full-screen Web Presentation projects through a staged workflow. Use for leadership/government/product/pre-sales/project presentations delivered as interactive HTML, including modular source, standalone single-file HTML, screenshots, contact sheets, release packages, and GitHub publishing.
---

# Web Presentation Builder

Create presentation-style websites that behave like slide decks but are implemented as responsive full-screen web pages. Treat each project as a versioned product artifact, not as a one-off HTML mockup.

## Core operating principle

Always work in this order unless the user explicitly asks to skip a gate:

1. Understand source material and audience.
2. Confirm content architecture.
3. Define visual and interaction baseline.
4. Build 3–5 representative key screens.
5. Lock approved key screens.
6. Build the full presentation.
7. Run visual/technical QA.
8. Build both modular and standalone versions.
9. Package and release without overwriting the previous stable version.

Do not jump from source material directly to a final 15–30 screen presentation unless the user explicitly requests a rough first pass.

## Supported modes

### New mode
Use when no stable project baseline exists.

Flow:
`UNDERSTAND -> CONTENT_ARCH -> VISUAL_BASELINE -> KEY_SCREENS -> FULL_BUILD -> QA -> STANDALONE -> RELEASE`

### Continue mode
Use when a prior project state or repository already exists.

Before editing:
1. Read `.project/project-state.yaml` when present.
2. Read the latest `content-baseline`, `visual-baseline`, `page-manifest`, and QA status.
3. Identify the current stable version and locked screens.
4. Continue from the latest unfinished stage instead of restarting.

### Revise mode
Use when the user asks to change specific screens or a stable presentation.

Flow:
`LOAD_BASELINE -> TARGETED_EDIT -> REGRESSION_QA -> STANDALONE_SYNC -> RELEASE_SYNC`

Do not redesign untouched screens unless the requested change has a genuine cross-screen dependency.

## Project state model

Every project should maintain a machine-readable state file at:

`.project/project-state.yaml`

Recommended fields:
- project name
- presentation type
- current version
- current stage
- source status
- content architecture status
- visual baseline status
- key screen IDs
- locked screen IDs
- QA status
- standalone status
- release status
- pending items
- last stable commit

The state file is the primary recovery point after long conversations, tool timeouts, model changes, or work resumption.

## Stage 1 — Understand

Read all available source material before producing page code.

Determine:
- presentation audience
- decision or communication objective
- expected presentation duration
- source hierarchy and authority
- core facts that must remain accurate
- likely narrative arc
- whether external research is needed
- whether public, internal, or confidential material is involved

Output a concise understanding report.

Do not generate full HTML yet.

If source material conflicts, preserve source distinctions and ask for a decision instead of silently reconciling them.

## Stage 2 — Content architecture

Create a page-by-page structure before implementation.

For each screen specify:
- screen number
- title
- communication objective
- core message
- supporting content
- preferred visual structure
- diagrams/charts required
- image requirements
- interaction requirements
- expected information density

Prefer narrative progression over feature dumping.

Typical leadership structure:
1. Why now
2. What problem exists
3. What is proposed
4. How it works
5. What users experience
6. How value is measured
7. How it scales
8. What happens next

Wait for confirmation before full build unless explicitly told to proceed.

## Stage 3 — Visual and interaction baseline

Define a reusable design system before building all screens.

Specify:
- palette
- typography scale
- spacing scale
- card radius
- border/shadow rules
- icon style
- diagram language
- illustration style
- image treatment
- navigation style
- transition style
- hover/click behavior
- background treatment

Default viewport target:
`1920 × 1080`

Default readability guidance for leadership presentations:
- page title: 42–56 px
- section title: 28–34 px
- key number: 32–48 px
- body text: 18–22 px
- secondary text: 16–18 px
- avoid text below 15 px unless decorative/nonessential

Do not solve density problems by shrinking all text.

## Visual composition rules

### One-screen rule
Every screen must fit the target viewport without vertical scrolling.

### Balance rule
Avoid both extremes:
- content packed into the top half
- large dead zones around a small cluster

### Center-and-branches rule
For hub-and-spoke or total/sub structure:
- keep secondary components visually close enough to read as one system
- secondary nodes should not be tiny relative to the center
- connecting lines should not create huge empty gaps

### Card rule
Cards are structural containers, not decoration.
Use fewer larger cards rather than many unreadable micro-cards.

### Image rule
Use images only when they contribute context, authenticity, atmosphere, or explanation.
Prefer:
`layout + data/diagram + UI elements + necessary image`
over:
`large decorative image + small text block`

## Stage 4 — Key screen prototype

Before full production, create 3–5 representative screens.

Recommended types:
- cover
- architecture/system overview
- product/workbench screen
- workflow/process screen
- operations/data screen

Use these to validate:
- information density
- font sizes
- visual hierarchy
- page balance
- color system
- component language
- interaction style
- image treatment

Once approved, record approved screens as locked screens in `project-state.yaml`.

Locked screens may only change when:
- the user explicitly requests it
- a critical global bug affects them
- an asset/reference dependency requires synchronization

## Stage 5 — Full build

Build the complete presentation using the approved baseline.

Recommended modular structure:

```text
prototype/full-vX.Y/
├── index.html
├── app.js
├── css/
│   ├── part-1.css
│   ├── part-2.css
│   └── ...
├── screens/
│   ├── screens-01-05.js
│   ├── screens-06-10.js
│   └── ...
└── assets/
```

Use screen IDs consistently, preferably zero-padded:
`01 ... 20`

Each screen should support direct URL hash navigation when practical:
`#01`, `#02`, etc.

Implementation must preserve:
- one-screen fit
- readable body text
- consistent spacing
- consistent component vocabulary
- expected keyboard/mouse navigation

## Stage 6 — QA

QA is mandatory before release.

### Technical QA
Check:
- all local references resolve
- all intended screen IDs exist
- JS syntax is valid
- no broken image paths
- no missing assets
- no unintended external dependency in standalone builds

### Visual QA
Render every screen at the target viewport.

Inspect:
- overflow/clipping
- text too small
- crowded cards
- excessive whitespace
- content too high/low
- hub-and-spoke structures too dispersed
- inconsistent card dimensions
- broken images
- incomplete demo content
- strange alignment
- navigation overlap

Generate a Contact Sheet so the entire presentation can be reviewed as a system.

A successful build is not sufficient evidence that the presentation is visually correct.

## Stage 7 — Standalone build

Produce both:
1. modular multi-file source
2. standalone single-file HTML

Standalone must inline:
- CSS
- JavaScript
- required local images/assets that are needed offline

### Image validation pipeline
Never trust a Base64 string merely because it exists.

Required pipeline:
1. decode/open source image
2. verify file format
3. verify dimensions
4. optionally create a web-compatible PNG/JPEG
5. encode final bytes as Base64
6. decode embedded Base64 again
7. compare decoded bytes with source bytes
8. verify decoded image with an image library
9. render in a browser as final proof

Never keep a build step that silently restores an obsolete image over a newly committed source image.

The current repository asset should be the source of truth unless the project explicitly defines a different immutable source mechanism.

## Stage 8 — Release

Never overwrite an older stable release unless the user explicitly requests replacement.

Recommended structure:

```text
release/vX.Y/
├── Presentation_vX.Y_Standalone.html
├── Presentation_vX.Y.zip
├── README.md
├── HTML-SHA256.txt
└── SHA256SUMS.txt

qa/
├── contact-sheet-vX.Y.jpg
├── source-reference-audit-vX.Y.json
├── release-build-audit-vX.Y.json
└── full-page-qa-vX.Y.md
```

Release only after:
- technical QA passes
- visual QA passes
- standalone build opens correctly
- key assets are verified
- intended source changes are confirmed in generated output

## GitHub publishing workflow

Prefer reproducible builds over manually edited release artifacts.

Typical workflow:
1. commit modular source
2. push to versioned source directory
3. GitHub Actions runs build script
4. validate assets
5. render all screens
6. build Contact Sheet
7. build standalone HTML
8. build ZIP
9. generate SHA256 files
10. commit generated release artifacts back to the same branch

Workflow path filters should target only relevant files.

Avoid infinite CI loops by ensuring generated release paths do not retrigger the source build unless intentional.

## Release verification requirements

After CI says success, independently verify business intent.

Examples:
- if a photo was replaced, confirm generated audit records the new resolution/hash
- if a screen changed, confirm Contact Sheet reflects it
- if standalone was rebuilt, confirm size/hash changed when expected
- confirm generated commit exists on the target branch

Never report “done” based only on a green workflow status.

## Failure recovery

### Long task or timeout
Before continuing:
1. inspect repository state
2. identify last completed commit
3. compare requested work with actual repository contents
4. split remaining work into explicit smaller steps
5. resume from the first incomplete step

### Broken image in standalone
Check in this order:
1. source image opens
2. source image size/dimensions
3. generated compatible image opens
4. Data URI MIME type
5. Base64 validation
6. decoded bytes equal generated asset
7. browser render

### CI succeeds but old content remains
Inspect build scripts for:
- stale hard-coded assets
- restore/copy steps
- cached templates
- old source directories
- release generation based on the wrong branch/version

## Anti-patterns

Do not:
- build all screens before the visual baseline is confirmed
- use tiny text to force content into a screen
- scatter branch cards to page edges around a small center
- insert irrelevant stock imagery to “make the page richer”
- convert whole presentation screens into flat images
- claim completion before browser QA
- overwrite a user-uploaded asset with a hidden legacy source
- maintain two competing build pipelines for the same version
- assume successful CI means the requested content made it into the artifact

## Deliverable quality bar

A completed Web Presentation should be:
- understandable without presenter narration for core points
- readable on a meeting-room display
- visually coherent across all screens
- technically reproducible
- editable through modular source
- distributable through a standalone HTML
- reviewable through screenshots/contact sheet
- recoverable through project state files
- versioned and auditable through GitHub

## Recommended templates and tools

Use accompanying files under:
- `templates/`
- `references/`
- `scripts/`
- `examples/`

The templates are intended to be copied into each project rather than edited in place inside the skill.
