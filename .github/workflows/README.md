# GitHub Actions Workflows

This directory contains the CI/CD workflows for the xRegistry Code Generation CLI project.

## Workflows Overview

### 📦 `publish-pypi.yml` - PyPI Publishing
**Trigger:** Version tags (`v*`), successful test completion  
**Purpose:** Build and publish Python package to PyPI  
**Required Secret:** `PYPI_API_TOKEN`  
**Behavior:**
- 🔒 **Only runs if tests pass** (or triggered by tag/manual dispatch)
- ✅ Always builds the package
- ✅ Publishes to PyPI if secret is configured
- ⚠️ Skips publishing with clear warning if secret is missing
- 📤 Uploads artifacts to GitHub Actions (available for 30 days)

### 🎨 `publish-vscode.yml` - VS Code Marketplace Publishing  
**Trigger:** Version tags (`v*`), successful test completion  
**Purpose:** Build and publish VS Code extension to marketplace  
**Required Secret:** `VSCE_PAT`  
**Behavior:**
- 🔒 **Only runs if tests pass** (or triggered by tag/manual dispatch)
- ✅ Always builds the extension (.vsix)
- ✅ Publishes to VS Code Marketplace if secret is configured
- ⚠️ Skips publishing with clear warning if secret is missing
- 📤 Uploads artifacts to GitHub Actions (available for 30 days)

### 🏷️ `build.yml` - GitHub Release Creation
**Trigger:** Version tags (`v*`)  
**Purpose:** Create GitHub releases with build artifacts  
**Required Secrets:** None  
**Behavior:**
- ✅ Builds Python package
- ✅ Builds VS Code extension
- ✅ Creates GitHub release
- 📎 Attaches all build artifacts to the release

### 🧪 `test.yml` - Continuous Integration Testing
**Trigger:** Push to any branch, pull requests  
**Purpose:** Run test suite to validate changes  
**Required Secrets:** None  
**Behavior:**
- ✅ Runs Python test suite
- ✅ Validates code quality
- ✅ Ensures changes don't break existing functionality

### 🐳 `build-images.yml` - Container Image Building
**Trigger:** Push to main, tags  
**Purpose:** Build and publish Docker container images  
**Required Secrets:** Container registry credentials (if publishing)  
**Behavior:**
- ✅ Builds container images
- 📤 Publishes to container registry if configured

## Workflow Design Philosophy

All workflows follow a "**graceful degradation**" pattern:

1. **Build Always Succeeds:** Packages/extensions are always built successfully
2. **Secrets Optional:** Publishing is skipped if secrets aren't configured
3. **Clear Warnings:** Users get helpful messages explaining missing configuration
4. **Artifact Preservation:** Build outputs are always available for manual publishing
5. **Fork-Friendly:** Contributors can run workflows without needing publishing credentials

## Publishing Workflow

When you want to create a new release:

```bash
# 1. Ensure all changes are committed
git add .
git commit -m "Prepare v1.2.3 release"
git push

# 2. Create and push a version tag
git tag v1.2.3
git push origin v1.2.3

# 3. Workflows automatically:
#    - Run test suite (test.yml)
#    - If tests pass:
#      ├─ Build and publish to PyPI (if PYPI_API_TOKEN is set)
#      ├─ Build and publish to VS Code Marketplace (if VSCE_PAT is set)
#      └─ Create GitHub release with artifacts (build.yml)
#    - If tests fail: All publishing and release creation skipped
```

**Important:** Publishing and release creation only happen if tests pass. This ensures quality control.

## Setting Up Publishing

To enable automatic publishing, you need to configure secrets:

**See:** [../.github/PUBLISHING_GUIDE.md](../PUBLISHING_GUIDE.md) for complete setup instructions.

## Monitoring Workflows

- View workflow runs: Repository → Actions tab
- Check individual steps in workflow logs
- Download artifacts from completed workflow runs
- Review warning messages if publishing is skipped

## Testing Workflows

### Without Secrets (Safe for Development)
```bash
git tag v1.0.0-test
git push origin v1.0.0-test
# Result: Builds succeed, publishing skipped
```

### With Secrets (Actual Release)
```bash
git tag v1.0.0
git push origin v1.0.0
# Result: Builds and publishes to PyPI + VS Code Marketplace
```

## Troubleshooting

### "Skipping PyPI publish: PYPI_API_TOKEN secret is not configured"
This is expected if you haven't set up the secret. The package still builds successfully - check the artifacts.

### "Skipping VS Code Marketplace publish: VSCE_PAT secret is not configured"
This is expected if you haven't set up the secret. The extension still builds successfully - check the artifacts.

### Workflow Doesn't Trigger
- Ensure tag starts with `v` (e.g., `v1.2.3` not `1.2.3`)
- Check that GitHub Actions is enabled (Settings → Actions)

### Publishing Fails
- **PyPI:** Token may be expired or invalid - regenerate on PyPI
- **VS Code:** PAT may be expired (default 90 days) - regenerate in Azure DevOps

## Manual Publishing (Fallback)

If workflows fail or you prefer manual control, you can download artifacts and publish manually:

```bash
# Download artifacts from GitHub Actions
# Then:

# PyPI
pip install twine
twine upload dist/*

# VS Code
vsce publish -p <your-pat>
```

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Publishing Guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/)
- [VS Code Publishing Guide](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
