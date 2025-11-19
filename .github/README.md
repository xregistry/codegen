# GitHub Workflows & Publishing

This directory contains GitHub Actions workflows and publishing documentation for the xRegistry Code Generation CLI.

## 📚 Documentation

- **[PUBLISHING_GUIDE.md](PUBLISHING_GUIDE.md)** - Complete guide for setting up automated publishing to PyPI and VS Code Marketplace
- **[WORKFLOW_ARCHITECTURE.md](WORKFLOW_ARCHITECTURE.md)** - Visual diagrams and architecture documentation for all workflows
- **[workflows/README.md](workflows/README.md)** - Detailed description of each workflow and their relationships

## 🚀 Quick Start

### Test Workflows (No Setup Needed)

```bash
git tag v0.0.1-test
git push origin v0.0.1-test
```

Workflows will build everything successfully and show what would be published.

### Enable Publishing (Requires 2 Secrets)

1. Add `PYPI_API_TOKEN` - for PyPI publishing
2. Add `VSCE_PAT` - for VS Code Marketplace publishing

**Full instructions:** See [PUBLISHING_GUIDE.md](PUBLISHING_GUIDE.md)

## 📋 Workflows

| Workflow | Trigger | Purpose | Requires Tests |
|----------|---------|---------|----------------|
| `test.yml` | Push, PR, Tags | Run test suite | N/A |
| `build.yml` | Tags (v*) | Create GitHub releases | ✅ Yes |
| `publish-pypi.yml` | Tags (v*) | Publish to PyPI | ✅ Yes |
| `publish-vscode.yml` | Tags (v*) | Publish to VS Code Marketplace | ✅ Yes |

**All publishing and release workflows require tests to pass first.**

## 🎯 Key Features

- **Quality Gate:** Tests must pass before any publishing
- **Fork-Friendly:** Works without secrets in contributor forks
- **Graceful Degradation:** Builds succeed, publishing skips with warnings if secrets missing
- **Complete Documentation:** Step-by-step setup instructions

## 📖 Learn More

- [PUBLISHING_GUIDE.md](PUBLISHING_GUIDE.md) - Complete setup and troubleshooting guide
- [WORKFLOW_ARCHITECTURE.md](WORKFLOW_ARCHITECTURE.md) - Visual workflow diagrams
- [workflows/README.md](workflows/README.md) - Individual workflow documentation
