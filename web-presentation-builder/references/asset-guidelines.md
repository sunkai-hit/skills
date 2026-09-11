# Asset Guidelines

## Before adding an image
Ask what role the image serves:
- evidence/documentary photo;
- environmental atmosphere;
- product illustration;
- explanatory diagram;
- background texture.

If none applies, omit it.

## Raster validation
For every JPG/PNG/WebP used in a release:
- file exists;
- file size is plausible;
- image decoder can load all pixels;
- dimensions meet intended display size;
- format matches the file extension or is intentionally converted.

## Standalone embedding
When embedding as Data URI:
1. validate source;
2. encode bytes;
3. decode generated Base64;
4. compare bytes/hash when possible;
5. validate decoded image;
6. render the final standalone page.

A syntactically valid Base64 string does not prove the underlying image is valid.

## Resolution
Avoid excessive upscaling. For a large photographic panel, source width should normally be at least comparable to the rendered pixel width, preferably higher for high-density displays.
