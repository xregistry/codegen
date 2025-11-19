# Publishing Guide for xRegistry Code Generation CLI

Complete guide for setting up and managing automated publishing to PyPI and VS Code Marketplace.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Workflow Overview](#workflow-overview)
- [Setting Up Publishing](#setting-up-publishing)
  - [Prerequisites](#prerequisites)
  - [1. PyPI Token Setup](#1-pypi-token-setup)
  - [2. VS Code Marketplace Token Setup](#2-vs-code-marketplace-token-setup)
- [Publishing Checklist](#publishing-checklist)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Maintenance](#maintenance)

---

## Quick Start

### Test Without Secrets (Recommended First Step)

The workflows work without any configuration - they'll build everything and show you what would be published:

```bash
git tag v0.0.1-test
git push origin v0.0.1-test
```

**What happens:**
- ✅ Tests run
- ✅ Packages built successfully
- ⚠️ Publishing skipped with helpful warnings
- 📦 Artifacts available for download (30 days)

### Production Publishing (Requires 2 Secrets)

Once you add the two required secrets, publishing happens automatically:

1. **`PYPI_API_TOKEN`** - Publishes Python package to PyPI
2. **`VSCE_PAT`** - Publishes VS Code extension to Marketplace

---

## Workflow Overview

### How It Works

When you push a version tag (e.g., `v1.2.3`):

```
1. test.yml runs
   ↓
   ✅ Tests PASS
   ↓
   ├─→ build.yml creates GitHub release with artifacts
   ├─→ publish-pypi.yml publishes to PyPI (if PYPI_API_TOKEN set)
   └─→ publish-vscode.yml publishes to VS Code Marketplace (if VSCE_PAT set)

   ❌ Tests FAIL
   └─→ Nothing publishes (quality gate)
```

### Key Features

- **Test-dependent:** All publishing blocked if tests fail
- **Fork-friendly:** Works without secrets in contributor forks
- **Graceful degradation:** Builds succeed, publishing skips with warnings
- **Manual override:** Can trigger publishing manually via GitHub Actions UI

---

## Setting Up Publishing

### Prerequisites

- GitHub repository with admin access
- PyPI account (create at https://pypi.org/account/register/)
- Azure DevOps account (create at https://dev.azure.com)

### 1. PyPI Token Setup

#### Step 1: Create API Token on PyPI

1. Go to https://pypi.org/manage/account/token/
2. Log in to your PyPI account
3. Click **"Add API token"**
4. Configure the token:
   - **Name:** `xregistry-codegen-github-actions`
   - **Scope:** Select "Entire account" or limit to "Project: xregistry" (if project exists)
5. Click **"Add token"**
6. **⚠️ Copy the token immediately** (starts with `pypi-`) - it won't be shown again

#### Step 2: Add Token to GitHub

1. Navigate to your repository on GitHub
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Configure the secret:
   - **Name:** `PYPI_API_TOKEN` (must match exactly)
   - **Value:** Paste the token from PyPI
5. Click **"Add secret"**

#### Step 3: Verify

- ✅ Secret appears in secrets list (value hidden)
- ✅ Name is exactly `PYPI_API_TOKEN` (case-sensitive)

### 2. VS Code Marketplace Token Setup

#### Step 1: Create Azure DevOps Account

1. Go to https://dev.azure.com
2. Sign in with your Microsoft account
3. Create a new organization (if needed) or use existing

#### Step 2: Create Personal Access Token (PAT)

1. In Azure DevOps, click your **profile icon** → **"Personal access tokens"**
2. Click **"New Token"**
3. Configure the token:
   - **Name:** `VS Code Extension Publishing`
   - **Organization:** Select "All accessible organizations"
   - **Expiration:** Set to 90 days or custom (max 1 year)
   - **Scopes:** Click "Show all scopes"
   - Expand **"Marketplace"** section
   - Check **"Manage"** permission
4. Click **"Create"**
5. **⚠️ Copy the token immediately** - it won't be shown again

#### Step 3: Set Up VS Code Publisher (if needed)

1. Go to https://marketplace.visualstudio.com/manage
2. Sign in with the same Microsoft account
3. If you don't have a publisher:
   - Click **"Create publisher"**
   - Use publisher ID: `xregistry-cg` (must match `package.json`)
4. Verify publisher exists and is active

#### Step 4: Add Token to GitHub

1. Navigate to your repository on GitHub
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Configure the secret:
   - **Name:** `VSCE_PAT` (must match exactly)
   - **Value:** Paste the PAT from Azure DevOps
5. Click **"Add secret"**

#### Step 5: Verify

- ✅ Secret appears in secrets list (value hidden)
- ✅ Name is exactly `VSCE_PAT` (case-sensitive)
- ✅ PAT has "Marketplace (Manage)" scope
- ✅ Publisher ID matches extension's `package.json`

---

## Publishing Checklist

### First-Time Setup

- [ ] **Test without secrets**
  - [ ] Create test tag: `git tag v0.0.1-test && git push origin v0.0.1-test`
  - [ ] Verify workflows run successfully
  - [ ] Check warnings about missing secrets
  - [ ] Download and inspect build artifacts

- [ ] **Set up PyPI publishing**
  - [ ] Create PyPI API token at https://pypi.org/manage/account/token/
  - [ ] Add `PYPI_API_TOKEN` secret to GitHub repository
  - [ ] Verify secret name is correct (case-sensitive)

- [ ] **Set up VS Code Marketplace publishing**
  - [ ] Create Azure DevOps account at https://dev.azure.com
  - [ ] Generate PAT with "Marketplace (Manage)" scope
  - [ ] Verify publisher ID matches package.json: `xregistry-cg`
  - [ ] Add `VSCE_PAT` secret to GitHub repository
  - [ ] Verify secret name is correct (case-sensitive)

- [ ] **Test publishing with secrets**
  - [ ] Create pre-release tag: `git tag v0.0.1-beta.1 && git push origin v0.0.1-beta.1`
  - [ ] Monitor workflows in Actions tab
  - [ ] Verify test.yml passes
  - [ ] Verify build.yml creates GitHub release
  - [ ] Verify publish-pypi.yml publishes to PyPI
  - [ ] Verify publish-vscode.yml publishes to Marketplace

- [ ] **Verify published packages**
  - [ ] Check PyPI: https://pypi.org/project/xregistry/
  - [ ] Check VS Code Marketplace: Search "xregistry-vscode"
  - [ ] Test install: `pip install xregistry==0.0.1-beta.1`
  - [ ] Test VS Code extension installation

### Before Each Release

- [ ] Run tests locally: `pytest`
- [ ] Update CHANGELOG.md with release notes
- [ ] Commit all changes
- [ ] Create version tag: `git tag vX.Y.Z`
- [ ] Push tag: `git push origin vX.Y.Z`
- [ ] Monitor workflows in Actions tab
- [ ] Verify all workflows complete successfully
- [ ] Test installed packages

---

## Testing

### Test Workflow Behavior

#### Without Secrets (Safe Testing)

```bash
# Create a test tag
git tag v0.0.1-test
git push origin v0.0.1-test

# Expected behavior:
# ✅ test.yml runs and passes
# ✅ build.yml creates GitHub release
# ⚠️ publish-pypi.yml builds package but skips PyPI upload
# ⚠️ publish-vscode.yml builds extension but skips marketplace publish
# 📦 All artifacts available for download
```

#### With Secrets (Real Publishing)

```bash
# Create a release tag
git tag v1.0.0
git push origin v1.0.0

# Expected behavior:
# ✅ test.yml runs and passes
# ✅ build.yml creates GitHub release
# ✅ publish-pypi.yml publishes to PyPI
# ✅ publish-vscode.yml publishes to VS Code Marketplace
```

#### Testing Test Failure Behavior

To verify that failed tests block publishing:

1. Create a failing test temporarily:
   ```python
   def test_intentional_failure():
       assert False, "Testing workflow behavior"
   ```

2. Push with a tag:
   ```bash
   git tag v0.0.1-test-fail
   git push origin v0.0.1-test-fail
   ```

3. Verify in Actions tab:
   - ❌ test.yml fails
   - ⏭️ build.yml does NOT run
   - ⏭️ publish-pypi.yml does NOT run
   - ⏭️ publish-vscode.yml does NOT run

4. Revert the test and push

### Manual Workflow Triggering

You can trigger publishing workflows manually (bypasses test requirement):

1. Go to repository **Actions** tab
2. Select workflow (e.g., "Publish to PyPI")
3. Click **"Run workflow"**
4. Fill in parameters if needed
5. Click **"Run workflow"**

⚠️ **Use with caution:** This bypasses the quality gate.

---

## Troubleshooting

### Common Issues

#### "Skipping PyPI publish: PYPI_API_TOKEN secret is not configured"

**Cause:** The `PYPI_API_TOKEN` secret is not set or named incorrectly.

**Solution:**
1. Verify secret exists: Settings → Secrets and variables → Actions
2. Check spelling: Must be exactly `PYPI_API_TOKEN` (case-sensitive)
3. Regenerate token if expired: https://pypi.org/manage/account/token/
4. Re-add secret to GitHub

#### "Skipping VS Code Marketplace publish: VSCE_PAT secret is not configured"

**Cause:** The `VSCE_PAT` secret is not set or named incorrectly.

**Solution:**
1. Verify secret exists: Settings → Secrets and variables → Actions
2. Check spelling: Must be exactly `VSCE_PAT` (case-sensitive)
3. Regenerate PAT if expired: Azure DevOps → Personal access tokens
4. Verify PAT has "Marketplace (Manage)" scope
5. Re-add secret to GitHub

#### Workflow Doesn't Trigger

**Cause:** Tag format incorrect or GitHub Actions disabled.

**Solution:**
1. Ensure tag starts with `v`: Use `v1.2.3`, not `1.2.3`
2. Verify GitHub Actions is enabled: Settings → Actions
3. Check repository permissions allow workflow runs

#### Publishing Fails with "401 Unauthorized"

**PyPI:**
1. Token may be expired - regenerate on PyPI
2. Token may not have correct permissions
3. Token may have been revoked

**VS Code Marketplace:**
1. PAT may be expired - check Azure DevOps
2. PAT may not have "Marketplace (Manage)" scope
3. Publisher ID may not match extension's package.json

#### Publishing Fails with "Conflict" or "Version Already Exists"

**Cause:** The version number has already been published.

**Solution:**
1. You cannot republish the same version to PyPI or VS Code Marketplace
2. Increment the version number
3. Create a new tag with the new version
4. Delete the old tag if needed: `git tag -d vX.Y.Z && git push origin :refs/tags/vX.Y.Z`

#### Tests Pass But Publishing Doesn't Run

**Cause:** Workflows waiting for test.yml to complete.

**Solution:**
1. Check Actions tab - publishing workflows should show as "Waiting"
2. Once test.yml completes, publishing workflows will start
3. If stuck, check workflow_run trigger configuration

---

## Maintenance

### Token Renewal

Both tokens expire and need periodic renewal:

#### PyPI Token

- **Expiration:** Optional (can be set during creation)
- **Renewal:**
  1. Generate new token at https://pypi.org/manage/account/token/
  2. Update `PYPI_API_TOKEN` secret in GitHub
  3. Test with a patch release

#### VS Code PAT

- **Expiration:** Required (default 90 days, max 1 year)
- **Renewal:**
  1. Azure DevOps → Profile → Personal access tokens
  2. Regenerate or create new token
  3. Update `VSCE_PAT` secret in GitHub
  4. Test with a patch release

**⚠️ Set calendar reminders** 7-14 days before token expiration to avoid publishing disruptions.

### Quarterly Review

Every 3 months, review:

- [ ] Token expiration dates
- [ ] Recent workflow runs for failures
- [ ] Dependency updates in workflows
- [ ] Documentation accuracy
- [ ] Test complete publishing flow

### Emergency Procedures

#### Lost PyPI Access

1. Recover PyPI account access via email reset
2. Generate new API token
3. Update `PYPI_API_TOKEN` secret in GitHub
4. Test with patch release

#### Lost Azure DevOps Access

1. Recover Azure DevOps account via Microsoft account
2. Generate new PAT
3. Update `VSCE_PAT` secret in GitHub
4. Test with patch release

#### Compromised Token

**Immediate actions:**
1. **Revoke token immediately** (PyPI or Azure DevOps)
2. Generate new token
3. Update GitHub secret
4. Review recent workflow runs for unauthorized activity
5. Consider creating new release to ensure package integrity
6. Document incident for security records

---

## Support Resources

- **PyPI Help:** https://pypi.org/help/
- **VS Code Publishing Docs:** https://code.visualstudio.com/api/working-with-extensions/publishing-extension
- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Azure DevOps PAT Docs:** https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate

---

## Workflow Architecture

For detailed workflow architecture and dependencies, see:
- `.github/workflows/README.md` - Complete workflow documentation
- `.github/WORKFLOW_ARCHITECTURE.md` - Visual diagrams and flow charts

---

**Last Updated:** November 19, 2025
