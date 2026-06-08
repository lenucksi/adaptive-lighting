---
id: TASK-5.1
title: Revise default configuration values for V2
status: To Do
assignee: []
created_date: 2026-05-31 20:41
updated_date: 2026-05-31 20:42
labels:
  - v2
  - config
  - defaults
dependencies: []
parent_task_id: TASK-5
priority: low
ordinal: 14000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update default values for transition, separate_turn_on_commands, sleep settings, and other config options to improve the out-of-box experience. Pure const.py changes — safe, fast, high visibility.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 transition default changed from 45 to 30,separate_turn_on_commands default changed from False to True,sleep_transition default changed from 1 to 30,sleep_brightness default changed from 1 to 5,sleep_color_temp default changed from 4000 to 3500,send_split_delay default changed from 0 to 100,adapt_delay default changed from 0 to 100,All updated defaults pass existing tests
- [ ] #2 transition default changed from 45 to 30
- [ ] #3 separate_turn_on_commands default changed from False to True
- [ ] #4 sleep_transition default changed from 1 to 30
- [ ] #5 sleep_brightness default changed from 1 to 5
- [ ] #6 sleep_color_temp default changed from 4000 to 3500
- [ ] #7 send_split_delay default changed from 0 to 100
- [ ] #8 adapt_delay default changed from 0 to 100
- [ ] #9 All updated defaults pass existing tests
<!-- AC:END -->



## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Update all DEFAULT_* constants in const.py\n2. Run tests to verify no regressions\n3. Update changelog
<!-- SECTION:PLAN:END -->