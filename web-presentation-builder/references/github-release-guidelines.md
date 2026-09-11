# GitHub Release Guidelines

## Repository discipline
- Read the current default branch before writing.
- Do not assume your local or remembered SHA is current.
- Keep stable releases under versioned paths.
- Prefer generated release files over manual copy/paste when a build pipeline exists.

## Recommended paths
```text
prototype/full-v0.5/
release/v0.5/
qa/contact-sheet-v0.5.jpg
qa/source-reference-audit-v0.5.json
qa/release-build-audit-v0.5.json
.project/
```

## CI finalization
A finalize workflow should:
1. validate dependencies and images;
2. validate local refs and screen IDs;
3. check JS syntax;
4. build standalone;
5. re-validate embedded images;
6. render all screens;
7. build contact sheet;
8. package ZIP;
9. generate hashes/audits;
10. commit generated outputs when desired.

## Verification after CI
Do not stop at “success”. Verify:
- source image dimensions/hash changed when expected;
- standalone size/hash changed when expected;
- contact sheet generation time changed;
- modular asset exists;
- output paths are current;
- latest main commit contains generated artifacts.
