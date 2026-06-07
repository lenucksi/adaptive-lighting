---
id: TASK-9
title: Upstream-PRs reviewen und mergen
status: Done
assignee: []
created_date: 2026-05-28 22:07
updated_date: 2026-05-30 17:09
labels:
  - ci
  - upstream
dependencies: []
references:
  - https://github.com/basnijholt/adaptive-lighting/pull/1472
  - https://github.com/basnijholt/adaptive-lighting/pull/1470
  - https://github.com/basnijholt/adaptive-lighting/pull/1462
priority: medium
ordinal: 9000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Offene Upstream-PRs prüfen und mergen: Pre-Sleep RGB (#1472), instant context-based manual control (#1470), expand_light_groups (#1462).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Alle mergbaren PRs identifiziert und gemergt
- [ ] #2 Report über nicht-mergbare PRs mit Begründung
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TASK-9 Report: Upstream PR Review

### #1472 — feat: add pre-sleep-rgb-mode
- **Status**: Open, mergeable, no reviews
- **Changes**: +314/-3, 10 files (switch.py, const.py, color_and_brightness.py, services.yaml, strings.json, docs, tests)
- **Assessment**: NOT RECOMMENDED for cherry-pick. Heavy overlap with switch.py and const.py which were significantly modified in TASK-10/11/12/13. Would cause merge conflicts. Also overlaps with planned TASK-5 (split transition_until_sleep). Better to implement as part of TASK-5.

### #1470 — feat: instant context-based manual-control marking (DRAFT)
- **Status**: Draft, mergeable, no reviews. Author seeks design feedback.
- **Changes**: +57, 1 file (switch.py only)
- **Assessment**: HIGHLY RELEVANT for TASK-3 (race conditions) and TASK-4 (manual control). The approach — marking manual_control immediately in state_changed_event_listener when a non-AL context changes brightness/color — directly addresses race conditions. Should be incorporated into TASK-3/TASK-4 implementation rather than cherry-picked as-is (draft may change).

### #1462 — feat: add expand_light_groups option
- **Status**: Open, mergeable, no reviews
- **Changes**: +101, 6 files (const.py, switch.py, config_flow.py, strings.json, tests)
- **Assessment**: RECOMMENDED for cherry-pick. Clean, self-contained feature. No overlap with existing changes (config option for light group handling). Can be implemented independently.

### Bottom Line
- **Mergeable as-is**: #1462 (expand_light_groups) — clean cherry-pick
- **Incorporate approach**: #1470 (context-based manual control) — TASK-3/TASK-4
- **Defer**: #1472 (pre-sleep RGB) — conflicts with our changes, better for TASK-5
<!-- SECTION:FINAL_SUMMARY:END -->