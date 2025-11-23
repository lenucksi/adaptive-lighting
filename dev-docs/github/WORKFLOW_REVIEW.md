# GitHub Workflows Review - Adaptive Lighting

**Date:** 2025-11-23
**Repository:** basnijholt/adaptive-lighting

## Executive Summary

The repository has **10 workflow files** and **1 reusable action**. While well-structured overall, there is a **critical branch inconsistency**: workflows reference both `master` and `main` branches, creating race conditions and broken functionality.

**Overall Health:** Good with critical issues to address

---

## 1. Workflow Inventory

| Workflow | Trigger | Purpose | Branch Issue |
|----------|---------|---------|--------------|
| deploy-webapp.yml | main | Deploy WebAssembly webapp to GitHub Pages | Correct |
| docker-build.yml | main | Build/push Docker images | **BROKEN** |
| hassfest.yaml | master | Validate HA manifest | Inconsistent |
| pytest.yaml | master | Run test suite | Inconsistent |
| pre-commit.yaml | master | Run pre-commit hooks | Inconsistent |
| validate.yml | master | HACS validation | Inconsistent |
| toc.yaml | all | Auto-generate README TOC | No filter |
| release-drafter.yml | main | Draft release notes | Correct |
| update-readme.yml | master | Update README/strings/services | Inconsistent |
| main-to-master-sync.yml | main→master | Sync branches | Intentional |

---

## 2. Critical Issues

### Issue 1: Docker Build Never Pushes (CRITICAL)

**File:** `.github/workflows/docker-build.yml`

```yaml
on:
  push:
    branches: ["main"]

# ... later ...
push: ${{ github.ref == 'refs/heads/master' }}
```

**Problem:** Triggers on `main` but only pushes when branch is `master` (never true).

**Impact:** Docker images are built but never published to Docker Hub.

**Fix:** Change condition to `github.ref == 'refs/heads/main'`

-> HUMAN Docker Hub can probably be skipped. Either push to quay for sbom scanning or just GitHub registry.

### Issue 2: Branch Inconsistency (CRITICAL)

| Workflows triggering on `main` | Workflows triggering on `master` |
|-------------------------------|----------------------------------|
| deploy-webapp.yml | hassfest.yaml |
| docker-build.yml | pytest.yaml |
| release-drafter.yml | pre-commit.yaml |
| main-to-master-sync.yml | validate.yml |
| | update-readme.yml |

**Impact:** CI behavior differs between branches; PRs may not get proper validation.

**Fix:** Migrate all workflows to trigger on `main` only.

### Issue 3: Unstable Action References (HIGH)

| Workflow | Action | Issue | Resolution |
|----------|--------|-------|------------|
| hassfest.yaml | `home-assistant/actions/hassfest@master` | Branch reference | **Keep @master** - only tag is v1.0.0 from 2020, outdated |
| validate.yml | `hacs/action@main` | Branch reference | Pin to `@v22.5.0` |
| update-readme.yml | `ad-m/github-push-action@master` | Branch reference | Pin to `@v1.0.0` |

**Risk:** Branch references can change without notice.

**Note:** `home-assistant/actions/hassfest` should use `@master` as recommended by Home Assistant.
The only available tag (v1.0.0) is from April 2020 and incompatible with current HA Core.

---

## 3. Medium Priority Issues

### Issue 4: Path Filter Typo

**File:** `.github/workflows/update-readme.yml`

```yaml
paths:
  - "github/workflows/update-readme.yml"  # Missing leading dot!
```

**Fix:** Change to `.github/workflows/update-readme.yml`

### Issue 5: TOC Generator on All Branches

**File:** `.github/workflows/toc.yaml`

```yaml
on: push  # No branch filter!
```

**Impact:** Wastes CI resources, auto-commits to feature branches.

**Fix:** Add `branches: [main]`

### Issue 6: Bug Template Label Error

**File:** `.github/ISSUE_TEMPLATE/bug-report.md`

```yaml
labels: kind/bug, kind/feature, need/triage  # Bug has feature label?
```

**Fix:** Remove `kind/feature`

---

## 4. Test Matrix

The pytest workflow covers an excellent range of Home Assistant versions:

| Python | Home Assistant |
|--------|----------------|
| 3.12 | 2024.12.5 |
| 3.12 | 2025.1.4 |
| 3.13 | 2025.2.5 |
| 3.13 | 2025.3.4 |
| 3.13 | 2025.4.4 |
| 3.13 | 2025.5.3 |
| 3.13 | 2025.6.1 |
| 3.13 | dev |

-> Muss das ergänzt werden um more recent zeug?

---

## 5. Action Version Status

| Action | Version | Status |
|--------|---------|--------|
| actions/checkout | v4 | Current |
| actions/setup-python | v5 | Current |
| docker/build-push-action | v6 | Current |
| release-drafter/release-drafter | v6 | Current |
| pre-commit/action | v3.0.1 | Current |
| astral-sh/setup-uv | v6 | Current |
| home-assistant/actions/hassfest | @master | **Unstable** |
| hacs/action | @main | **Unstable** |
| ad-m/github-push-action | @master | **Unstable** |

-> is hassfest + hacs/action available with versions?
-> why is there a uv action? I can't find any uv usage in the project?

---

## 6. Renovate Configuration

**File:** `.github/renovate.json`

**Key Settings:**
- Dependency dashboard enabled
- GitHub Actions: pinned and auto-merged (minor/patch)
- Emoji commit prefix (⬆️)
- Extends recommended config

**Status:** Well configured

-> what does the dependency dashboard of renovate do in GitHub

---

## 7. Recommendations

### Immediate (This Week)

1. **Fix docker-build.yml condition** - Change to check for `main` branch
2. **Update hassfest.yaml** - Use release tag instead of `@master`
3. **Update validate.yml** - Use release tag instead of `@main`
4. **Fix path typo** in update-readme.yml

### Short Term (2 Weeks)

5. **Migrate all workflows to `main` branch**
6. **Add branch filter** to toc.yaml
7. **Fix bug template labels**
8. **Update ad-m/github-push-action** to release tag

### Medium Term (1 Month)

9. **Deprecate master branch**
10. **Remove main-to-master-sync workflow**
11. **Enhance release-drafter template** with PR categories
12. **Consider adding CodeQL** security scanning

---

## 8. Workflow Dependency Graph

```
Git Push to main:
├── deploy-webapp.yml → GitHub Pages
├── docker-build.yml → (broken - doesn't push)
├── release-drafter.yml → Draft release
├── main-to-master-sync.yml → Syncs to master
└── toc.yaml → Updates README

Git Push to master:
├── hassfest.yaml → HA validation
├── pytest.yaml → Test suite
├── pre-commit.yaml → Linting
├── validate.yml → HACS validation
└── update-readme.yml → Content updates

Pull Request:
├── hassfest.yaml
├── pytest.yaml
├── pre-commit.yaml
├── validate.yml
└── release-drafter.yml
```

---

## 9. Secrets Used

| Secret | Used In | Required |
|--------|---------|----------|
| DOCKERHUB_USERNAME | docker-build.yml | Yes |
| DOCKERHUB_TOKEN | docker-build.yml | Yes |
| GITHUB_TOKEN | release-drafter.yml, update-readme.yml | Auto-provided |

---

## Summary

**Strengths:**
- Comprehensive test matrix (8 HA versions)
- Good action version management via Renovate
- Well-configured issue templates
- Proper permission scoping

**Weaknesses:**
- Critical branch inconsistency affecting multiple workflows
- Docker push condition is broken
- Three workflows use unstable branch references
- TOC generator runs on all branches unnecessarily

**Priority:** Fix the Docker build condition and branch inconsistencies first.
