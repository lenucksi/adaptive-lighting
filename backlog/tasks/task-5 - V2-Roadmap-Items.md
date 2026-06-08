---
id: TASK-5
title: V2 Roadmap Items
status: To Do
assignee: []
created_date: 2026-05-28 22:07
updated_date: 2026-05-31 20:41
labels:
  - v2
  - architecture
dependencies: []
references:
  - https://github.com/basnijholt/adaptive-lighting/issues/739
priority: low
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
V2 Roadmap: transition_until_sleep splitten, manual control splitten, custom locations, defaults überarbeiten.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 transition_until_sleep in Brightness+Color gesplittet
- [ ] #2 manual_control in Brightness+Color gesplittet
- [ ] #3 Custom Locations unterstützt
- [ ] #4 Defaults überarbeitet
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Order (recommended)

AC #4 → AC #2 → AC #1 → AC #3

This order builds from least to most complex, avoiding merge conflicts as each subtask touches different files.

### AC #4 — Revise Defaults (quickest win, ~15 min)
Pure const.py changes. Safe, fast, high visibility.

### AC #2 — Split manual_control config (~30 min)
Service layer already supports granular control via LightControlAttributes bitmask. Only config schema + options flow need extending. Backward-compatible.

### AC #1 — Split transition_until_sleep (~1 hr)
New booleans in const.py → SunLightSettings constructor → get_brightness()/get_color_temp()/get_rgb_color() methods. Includes backward-compat migration for old configs.

### AC #3 — Custom Locations (~1.5 hrs)
Most complex. New location resolution logic in SunEvents. Optional lat/lon/tz/times with fallback to HA defaults. Config flow UI section.

## Reference
- Upstream V2 Roadmap: basnijholt/adaptive-lighting#739
- Upstream PR #1470 (custom location support)
- PR #1462 (related changes)
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Analysis complete. Subtasks created for each AC.
<!-- SECTION:NOTES:END -->