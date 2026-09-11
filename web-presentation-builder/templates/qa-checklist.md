# Web Presentation QA Checklist

## Content
- [ ] All planned screens exist.
- [ ] No unintended placeholders or empty operational cards.
- [ ] Demo data is labeled.
- [ ] Source terminology is preserved.

## Layout
- [ ] Each screen fits one target viewport.
- [ ] No critical child is clipped.
- [ ] No accidental horizontal overflow.
- [ ] Content is not visibly too high/low.
- [ ] Whitespace is balanced.
- [ ] No dense card collisions.
- [ ] Hub/detail structures are visually compact.

## Typography
- [ ] Body text is generally 18–22px for leadership contexts.
- [ ] Critical supporting text is >=16px.
- [ ] No critical text is <15px.
- [ ] Text hierarchy is consistent.

## Assets
- [ ] Raster images decode successfully.
- [ ] Dimensions are suitable for display size.
- [ ] No corrupted source is converted to Base64.
- [ ] Standalone embedded images re-decode successfully.
- [ ] Image crop/focus is correct.

## Technical
- [ ] CSS references resolve.
- [ ] JS references resolve.
- [ ] JS syntax checks pass.
- [ ] Browser render has no fatal console errors.
- [ ] Standalone has no unintended local dependencies.

## Release
- [ ] Full-screen screenshots rendered.
- [ ] Contact Sheet reviewed.
- [ ] Modular source updated.
- [ ] Standalone rebuilt after modular source.
- [ ] ZIP validated.
- [ ] SHA256 generated.
- [ ] Previous stable release not overwritten.
- [ ] GitHub workflow status checked.
- [ ] Generated artifacts verified, not merely workflow status.
