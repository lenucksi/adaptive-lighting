---
id: TASK-7
title: Weitere Bugs und Edge Cases
status: Done
assignee:
  - "@opencode-agent"
created_date: 2026-05-28 22:07
updated_date: 2026-05-30 18:18
labels:
  - bugs
dependencies: []
references:
  - https://github.com/basnijholt/adaptive-lighting/issues/1442
  - https://github.com/basnijholt/adaptive-lighting/issues/1459
  - https://github.com/basnijholt/adaptive-lighting/issues/1421
priority: medium
ordinal: 7000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Sammeltask für kleinere Bugs: color_temp + color_temp_kelvin Konflikt (#1442), Entity-Naming dupliziert (#1459), Tanh/Linear bleibt bei min_brightness (#1421).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 color_temp/color_temp_kelvin Konflikt behoben
- [ ] #2 Entity-Naming-Duplikation behoben
- [ ] #3 Tanh/Linear verhalten sich korrekt bei inverted timescale
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Fixed 3 bugs (#1442 color_temp/kelvin conflict, #1459 entity naming, #1421 tanh/linear inverted brightness) and added test_sunrise.py + test_docs_helpers.py. Commit d9a3dfe on tasks/TASK-7-MinorBugs. Note: Docker tests need to be verified from main repo branch (worktree symlink limitations with Docker bind mounts).
<!-- SECTION:FINAL_SUMMARY:END -->