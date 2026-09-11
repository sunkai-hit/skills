# GitHub Actions Integration

1. Copy `scripts/` into the project repository, for example as `tools/web-presentation/`.
2. Copy `finalize-web-presentation.yml` to `.github/workflows/finalize-web-presentation.yml`.
3. Put `web-presentation.yaml` at the repository root.
4. Adjust watched paths if your source structure differs.
5. Push to `main` or run the workflow manually.

The job ignores commits authored by `github-actions[bot]` to prevent release commits from recursively re-triggering the finalizer.

After a successful run, verify the generated audit files. Do not rely on CI status alone.
