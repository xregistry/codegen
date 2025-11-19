# Workflow Architecture

## Main Workflow Flow

```mermaid
graph TD
    A[Git Tag Push v*] --> B[test.yml<br/>Run Tests]
    B -->|✅ Success| C{Tests Pass}
    B -->|❌ Fail| D[Stop<br/>No Publishing]
    
    C --> E[build.yml<br/>Create Release]
    C --> F[publish-pypi.yml<br/>PyPI Publish]
    C --> G[publish-vscode.yml<br/>VS Code Publish]
    
    E --> H[✅ GitHub Release<br/>with Artifacts]
    F --> I{PYPI_API_TOKEN<br/>set?}
    G --> J{VSCE_PAT<br/>set?}
    
    I -->|Yes| K[✅ Published to PyPI]
    I -->|No| L[⚠️ Skip PyPI<br/>📦 Artifacts Available]
    
    J -->|Yes| M[✅ Published to<br/>VS Code Marketplace]
    J -->|No| N[⚠️ Skip Marketplace<br/>📦 Artifacts Available]
    
    style B fill:#e1f5ff
    style C fill:#d4edda
    style D fill:#f8d7da
    style E fill:#fff3cd
    style F fill:#fff3cd
    style G fill:#fff3cd
    style K fill:#d4edda
    style M fill:#d4edda
    style L fill:#fff3cd
    style N fill:#fff3cd
```

## Workflow States

### With All Secrets Configured

```mermaid
sequenceDiagram
    participant Tag as v1.2.3 Tag
    participant Test as test.yml
    participant Build as build.yml
    participant PyPI as publish-pypi.yml
    participant VSCode as publish-vscode.yml
    
    Tag->>Test: Trigger
    Test->>Test: Run Tests
    Test-->>Build: ✅ Success
    Test-->>PyPI: ✅ Success
    Test-->>VSCode: ✅ Success
    
    Build->>Build: Create Release
    Build-->>Tag: ✅ GitHub Release<br/>📦 Artifacts
    
    PyPI->>PyPI: Check PYPI_API_TOKEN
    PyPI->>PyPI: Build Package
    PyPI->>PyPI: Publish to PyPI
    PyPI-->>Tag: ✅ Published
    
    VSCode->>VSCode: Check VSCE_PAT
    VSCode->>VSCode: Build Extension
    VSCode->>VSCode: Publish to Marketplace
    VSCode-->>Tag: ✅ Published
```

### Without Secrets (Developer Mode)

```mermaid
sequenceDiagram
    participant Tag as v1.0.0-test Tag
    participant Test as test.yml
    participant Build as build.yml
    participant PyPI as publish-pypi.yml
    participant VSCode as publish-vscode.yml
    
    Tag->>Test: Trigger
    Test->>Test: Run Tests
    Test-->>Build: ✅ Success
    Test-->>PyPI: ✅ Success
    Test-->>VSCode: ✅ Success
    
    Build->>Build: Create Release
    Build-->>Tag: ✅ GitHub Release<br/>📦 Artifacts
    
    PyPI->>PyPI: Check PYPI_API_TOKEN
    PyPI->>PyPI: ⚠️ Not Found
    PyPI->>PyPI: Build Package Only
    PyPI-->>Tag: ⚠️ Skipped Publishing<br/>📦 Artifacts Available<br/>ℹ️ Instructions Shown
    
    VSCode->>VSCode: Check VSCE_PAT
    VSCode->>VSCode: ⚠️ Not Found
    VSCode->>VSCode: Build Extension Only
    VSCode-->>Tag: ⚠️ Skipped Publishing<br/>📦 Artifacts Available<br/>ℹ️ Instructions Shown
```

## Secret Dependency Matrix

| Workflow | Secret Required | Behavior Without Secret | Depends on Tests |
|----------|----------------|------------------------|------------------|
| test.yml | None | ✅ Always runs | N/A (runs first) |
| build.yml | None | ✅ Always creates release | ✅ Yes |
| publish-pypi.yml | `PYPI_API_TOKEN` | ⚠️ Builds but skips PyPI upload | ✅ Yes |
| publish-vscode.yml | `VSCE_PAT` | ⚠️ Builds but skips marketplace publish | ✅ Yes |

## Workflow Triggers

```mermaid
graph LR
    A[Push to Branch] --> B[test.yml]
    C[Pull Request] --> B
    D[Push Tag v*] --> B
    D --> E[build.yml]
    D --> F[publish-pypi.yml]
    D --> G[publish-vscode.yml]
    
    B -->|✅ Success| E
    B -->|✅ Success| F
    B -->|✅ Success| G
    
    H[Manual Dispatch] -.->|Bypasses Tests| F
    H -.->|Bypasses Tests| G
    
    style B fill:#e1f5ff
    style E fill:#fff3cd
    style F fill:#fff3cd
    style G fill:#fff3cd
    style H fill:#f8d7da
```

**Trigger Summary:**

| Event | test.yml | build.yml | publish-pypi.yml | publish-vscode.yml |
|-------|----------|-----------|------------------|-------------------|
| Push to branch | ✅ | ❌ | ❌ | ❌ |
| Pull request | ✅ | ❌ | ❌ | ❌ |
| Push tag (v*) | ✅ | ⏳ Waits for tests | ⏳ Waits for tests | ⏳ Waits for tests |
| Manual dispatch | ❌ | ❌ | ⚠️ Bypasses tests | ⚠️ Bypasses tests |

## Artifact Flow

```mermaid
graph TD
    A[Build Artifacts] --> B[Python Package<br/>.tar.gz + .whl]
    A --> C[VS Code Extension<br/>.vsix]
    A --> D[GitHub Actions<br/>30-day retention]
    
    B --> E{PYPI_API_TOKEN<br/>configured?}
    C --> F{VSCE_PAT<br/>configured?}
    
    E -->|Yes| G[📦 PyPI.org<br/>Permanent]
    E -->|No| H[📦 Manual Upload<br/>from Artifacts]
    
    F -->|Yes| I[📦 VS Code Marketplace<br/>Permanent]
    F -->|No| J[📦 Manual Upload<br/>from Artifacts]
    
    D --> K[💾 Download Available<br/>30 days]
    
    style G fill:#d4edda
    style I fill:#d4edda
    style H fill:#fff3cd
    style J fill:#fff3cd
    style K fill:#e1f5ff
```

## Security Model

```mermaid
graph TD
    A[GitHub Repository] --> B[Public Code<br/>Anyone can read]
    A --> C[Secrets<br/>Repo Admin only]
    
    B --> D[GitHub Actions<br/>Secure Runner]
    C --> D
    
    D --> E[Build Stage<br/>No Secrets]
    D --> F[Publish Stage<br/>PYPI_API_TOKEN]
    D --> G[Publish Stage<br/>VSCE_PAT]
    
    E --> H[✅ Always Works<br/>Fork-Friendly]
    F --> I{Secret<br/>Available?}
    G --> J{Secret<br/>Available?}
    
    I -->|Yes| K[✅ Publish]
    I -->|No| L[⚠️ Skip]
    J -->|Yes| M[✅ Publish]
    J -->|No| N[⚠️ Skip]
    
    style B fill:#e1f5ff
    style C fill:#f8d7da
    style E fill:#d4edda
    style H fill:#d4edda
    style K fill:#d4edda
    style M fill:#d4edda
    style L fill:#fff3cd
    style N fill:#fff3cd
```

## Decision Flow for Publishing

```mermaid
flowchart TD
    A[Start Workflow] --> B{Has version tag?}
    B -->|No| C[Skip Publishing]
    B -->|Yes| D{Tests Passed?}
    D -->|No| E[❌ Stop<br/>No Publishing]
    D -->|Yes| F{Check Secret}
    F -->|Missing| G[⚠️ Build Only<br/>Skip Publishing]
    F -->|Present| H[✅ Build & Publish]
    
    G --> I[Upload Artifacts]
    H --> I
    C --> I
    
    I --> J[Show Status Message]
    
    style E fill:#f8d7da
    style G fill:#fff3cd
    style H fill:#d4edda
    style I fill:#e1f5ff
```

## Monitoring Dashboard View

### Successful Run (All Secrets Configured)

```mermaid
gantt
    title Workflow Runs for tag v1.2.3
    dateFormat mm:ss
    axisFormat %M:%S
    
    section Tests
    Run Tests           :done, test, 00:00, 02:34
    
    section Release
    Create GitHub Release :done, build, 02:34, 01:12
    
    section PyPI
    Publish to PyPI     :done, pypi, 02:34, 00:45
    
    section VS Code
    Publish to Marketplace :done, vscode, 02:34, 01:03
```

**Results:**
- ✅ Tests passed (2m 34s)
- ✅ GitHub Release created (1m 12s)
- ✅ Published to PyPI (45s)
- ✅ Published to VS Code Marketplace (1m 03s)
- 📦 Artifacts available for download

### Run Without Secrets (Developer Mode)

```mermaid
gantt
    title Workflow Runs for tag v1.0.0-test
    dateFormat mm:ss
    axisFormat %M:%S
    
    section Tests
    Run Tests           :done, test, 00:00, 02:34
    
    section Release
    Create GitHub Release :done, build, 02:34, 01:12
    
    section PyPI
    Build Package       :done, pypi, 02:34, 00:30
    Publishing Skipped  :crit, skip1, 03:04, 00:00
    
    section VS Code
    Build Extension     :done, vscode, 02:34, 00:25
    Publishing Skipped  :crit, skip2, 02:59, 00:00
```

**Results:**
- ✅ Tests passed (2m 34s)
- ✅ GitHub Release created (1m 12s)
- ⚠️ PyPI publishing skipped - PYPI_API_TOKEN not configured (30s build only)
- ⚠️ VS Code publishing skipped - VSCE_PAT not configured (25s build only)
- 📦 Artifacts available for manual upload
- ℹ️ Instructions shown for configuring secrets
