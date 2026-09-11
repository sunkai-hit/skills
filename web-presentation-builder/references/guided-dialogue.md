# Guided Dialogue Pattern

The skill should feel like a project workflow, not a form questionnaire.

## General behavior
- Infer what is already clear from the user's materials.
- Ask only for information that materially changes the presentation.
- Ask no more than 2–3 high-value questions at a stage when clarification is necessary.
- Do not repeatedly ask the user to reconfirm facts already accepted as baseline.
- At every stage, state the current stage and the next gate in one compact paragraph.

## New project opening
Recommended pattern:

> I’ll start in **Stage 1: source understanding**. I’ll first extract the audience, objective, narrative priorities, confirmed facts, and asset needs. I won’t build the full HTML yet. After that I’ll give you a page architecture for confirmation.

## After content confirmation

> The content architecture is now the baseline. Next I’ll define the visual/interaction system and select 3–5 key screens for prototyping. Full production waits until those screens are approved.

## Before full build

> The key screens are approved and will be treated as locked visual baselines. I’ll now build the remaining screens against the same system, then render the whole deck for regression QA.

## Revision mode

> I’ll treat this as a targeted revision. I’ll separate screen-specific changes from global typography/layout changes, update the modular source first, run full regression rendering, and only then rebuild the standalone release.

## Completion reporting
Do not use “done” too early. Prefer:
- “source changes committed; CI is still running”;
- “CI succeeded; I’m verifying the generated artifacts”;
- “modular and standalone artifacts both reflect the revision; release is closed.”
