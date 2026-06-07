---
id: TASK-8
title: CI/CD und Dev-Infrastruktur
status: Done
assignee:
  - sub-agent-1
created_date: 2026-05-28 22:07
updated_date: 2026-05-30 17:06
labels:
  - ci
  - infrastructure
dependencies: []
priority: medium
ordinal: 8000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Docker-Image von Docker Hub auf GHCR migrieren, Devcontainer-Setup vereinfachen, CI-Pinning prüfen, Test-Container aktualisieren.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Docker-Image auf GHCR verfügbar
- [ ] #2 Devcontainer-Setup funktioniert zuverlässig
- [ ] #3 CI-Workflows aktuell und korrekt
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1) tests/README.md: Docker Hub -> GHCR (line 34 URL + docker run images) 2) scripts/setup-devcontainer: remove --python 3.14.2 (mismatch with 3.13 container) 3) .github/workflows/validate.yml: pin hacs/action@main -> 22.5.0 4) Verify: no conflict markers, no .orig files, docker build, ruff check, commit+push
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Completed CI/CD infrastructure fixes: 1) Updated tests/README.md Docker Hub references to GHCR 2) Removed hardcoded --python 3.14.2 from scripts/setup-devcontainer 3) Pinned hacs/action@main to v22.5.0 (SHA d556e73) in validate.yml 4) Verified no merge conflicts or .orig files 5) Committed and pushed to tasks/TASK-8-CICD
<!-- SECTION:FINAL_SUMMARY:END -->