# QA Guidelines

## Visual QA loop
1. Render every screen at target viewport.
2. Create a contact sheet.
3. Review the whole deck for rhythm and consistency.
4. Inspect flagged screens individually.
5. Patch modular source.
6. Re-run full regression render after global CSS changes.
7. Build standalone only after modular QA passes.

## Automatic warnings
Flag when possible:
- screen scrollWidth > clientWidth;
- screen scrollHeight > clientHeight;
- critical descendants exceed screen bounds;
- critical text is below configured minimum;
- image natural size is smaller than rendered size by a large factor;
- empty text-bearing cards;
- missing local refs.

## Contact Sheet review
Look for:
- pages visually too high/low;
- density spikes;
- repeated layouts becoming monotonous;
- one page using different card language;
- unreadable small text;
- oversized whitespace;
- broken or missing imagery.
