# Workflow Reference

## Stage gates

### Gate A — Content architecture approved
Do not begin full implementation until the page narrative is coherent and source-supported.

### Gate B — Visual baseline approved
Use 3–5 key screens to validate style. Once approved, lock them unless global changes require rework.

### Gate C — Full build complete
All planned screens exist and can be navigated.

### Gate D — QA passed
Every screen has been rendered at the target viewport and the contact sheet has been reviewed.

### Gate E — Release verified
Both modular and standalone outputs reflect the intended revision. A green CI run alone is not sufficient evidence.

## State names
- UNDERSTAND
- CONTENT_ARCH
- VISUAL_BASELINE
- KEY_SCREENS
- FULL_BUILD
- QA
- STANDALONE
- RELEASE

## Completion language
Use exact status language so users know whether a task is truly closed:
- “analysis complete; no files changed yet”
- “modular source updated; release not rebuilt yet”
- “workflow succeeded; artifact verification pending”
- “modular and standalone releases verified”
