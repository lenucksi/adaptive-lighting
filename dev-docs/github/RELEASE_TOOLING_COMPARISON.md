# Release Tooling Comparison: Release-Drafter vs Release-Please

**Date:** 2025-11-23
**Repository:** basnijholt/adaptive-lighting

## Executive Summary

This document compares **release-drafter** (currently in use) with **release-please** for automating releases. **Recommendation: Migrate to release-please** due to better alignment with existing conventional commit workflow and automatic version bumping.

---

## Current Setup (Release-Drafter)

**Files:**
- `.github/workflows/release-drafter.yml`
- `.github/release-drafter.yml`

**Configuration:**
```yaml
# Workflow triggers on main branch pushes and PR events
# Simple template with "What's Changed" section
# No PR label categorization configured
```

**Limitations:**
- No automatic version bumping in `manifest.json`
- No CHANGELOG.md generation
- Relies on PR labels for categorization (not configured)
- Does not leverage existing conventional commit setup

---

## Comparison Matrix

| Feature | Release-Drafter | Release-Please |
|---------|----------------|----------------|
| **Versioning Method** | PR labels | Conventional commits |
| **Output** | Draft GitHub Release | Release PR + GitHub Release |
| **CHANGELOG.md** | ❌ GitHub Release only | ✅ Auto-generates file |
| **Version File Updates** | ❌ Manual | ✅ Auto-bumps manifest.json |
| **Monorepo Support** | Limited | ✅ Excellent |
| **Maintainer** | Community | Google (googleapis) |
| **Commit Style Required** | Any (uses PR labels) | Conventional commits |
| **Release Workflow** | Publish draft manually | Merge release PR |

---

## Release-Drafter

### How It Works
1. PRs are merged to main
2. Draft release is updated with PR titles
3. PR labels determine version bump (major/minor/patch)
4. Maintainer manually publishes draft when ready

### Strengths
- Simple setup
- Works with any commit style
- Draft releases allow review before publishing

### Weaknesses
- Requires manual PR labeling for proper categorization
- No automatic version file updates
- No CHANGELOG.md generation
- Less active maintenance

### Links
- [GitHub Repository](https://github.com/release-drafter/release-drafter)
- [GitHub Marketplace](https://github.com/marketplace/actions/release-drafter)

---

## Release-Please

### How It Works
1. Commits following [Conventional Commits](https://www.conventionalcommits.org/) are pushed
2. Release-please parses commit messages:
   - `fix:` → patch bump
   - `feat:` → minor bump
   - `feat!:` or `BREAKING CHANGE:` → major bump
3. Creates/updates a "Release PR" with:
   - Version bump in configured files
   - CHANGELOG.md updates
4. Merging the Release PR creates the GitHub Release

### Strengths
- Automatic version bumping in `manifest.json`
- Generates proper CHANGELOG.md
- Works seamlessly with conventional commits (already enforced via pre-commit)
- Actively maintained by Google
- Excellent monorepo support
- Clear audit trail of releases

### Weaknesses
- Requires strict conventional commit format
- More initial configuration (config files)
- Learning curve for Release PR workflow

### Links
- [GitHub Repository](https://github.com/googleapis/release-please)
- [GitHub Action](https://github.com/googleapis/release-please-action)
- [Configuration Guide](https://github.com/googleapis/release-please/blob/main/docs/manifest-releaser.md)

---

## Recommendation

**Migrate to release-please** for the following reasons:

### 1. Conventional Commits Already Enforced
The repository already uses `conventional-precommit-linter` in `.pre-commit-config.yaml`, meaning all commits already follow the format release-please expects.

### 2. Single Source of Truth for Version
Release-please can automatically update `custom_components/adaptive_lighting/manifest.json` version field, eliminating manual version management.

### 3. CHANGELOG Generation
Automatic CHANGELOG.md generation provides better documentation than draft releases alone.

### 4. Active Maintenance
Release-please is maintained by Google's team with regular updates. Note: `standard-version` (a similar tool to release-drafter) was deprecated and recommends migration to release-please.

### 5. Better Audit Trail
Release PRs provide a clear, reviewable record of what's included in each release.

---

## Migration Plan

### Phase 1: Setup Release-Please

1. Create `.release-please-manifest.json`:
```json
{
  ".": "1.26.0"
}
```

2. Create `release-please-config.json`:
```json
{
  "packages": {
    ".": {
      "release-type": "python",
      "extra-files": [
        "custom_components/adaptive_lighting/manifest.json"
      ],
      "changelog-path": "CHANGELOG.md"
    }
  }
}
```

3. Create `.github/workflows/release-please.yml`:
```yaml
name: Release Please

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
```

### Phase 2: Disable Release-Drafter

Option A (Recommended): Disable via GitHub UI
1. Go to Actions → Release Drafter → "..." → "Disable workflow"

Option B: Add condition to skip:
```yaml
jobs:
  update_release_draft:
    if: false  # Disabled - migrated to release-please
```

### Phase 3: Cleanup (After Verification)

1. Delete `.github/workflows/release-drafter.yml`
2. Delete `.github/release-drafter.yml`

---

## Disabling GitHub Workflows

To disable a workflow without deleting it:

### Method 1: GitHub UI (Recommended)
1. Navigate to **Actions** tab
2. Select workflow from sidebar
3. Click **"..."** menu → **"Disable workflow"**

### Method 2: Conditional Skip
```yaml
jobs:
  job-name:
    if: false  # Workflow disabled
```

### Method 3: Manual-Only Trigger
```yaml
on:
  workflow_dispatch:  # Only manual runs allowed
```

---

## References

- [Release-Drafter GitHub](https://github.com/release-drafter/release-drafter)
- [Release-Please GitHub](https://github.com/googleapis/release-please)
- [Release-Please Action](https://github.com/googleapis/release-please-action)
- [Conventional Commits Spec](https://www.conventionalcommits.org/)
- [Simplify Releases with Release-Please](https://dev.to/archinmodi/simplify-your-release-process-with-the-release-please-github-action-3l34)
- [Streamline GitHub Releases](https://ferrishall.dev/automating-github-releases-with-release-please)
