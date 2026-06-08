---
id: TASK-6.4
title: Wire proxy entity lifecycle into AdaptiveLightingManager
status: To Do
assignee: []
created_date: 2026-05-31 21:03
updated_date: 2026-05-31 21:04
labels:
  - architecture
  - refactoring
  - proxy
dependencies:
  - TASK-6.1
  - TASK-6.3
parent_task_id: TASK-6
priority: low
ordinal: 21000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Integrate proxy entity creation/destruction into the AdaptiveLightingManager lifecycle. When a switch is enabled with proxy mode, create AdaptiveLightProxy entities for all managed lights. When the switch is disabled or config changes, destroy the proxies. Handle entity registry changes (lights added/removed). Add configuration option to enable proxy mode instead of intercept.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 AdaptiveLightingManager creates proxy entities for all managed lights on switch start,Proxy entities are removed when switch stops or config changes,Entity registry updates add/remove proxies when lights are added/removed from config,Config option proxy_mode added (opt-in, replaces intercept),proxy_mode and intercept are mutually exclusive,Manager tracks proxy ↔ real entity mappings,Existing lifecycle tests pass with proxy mode disabled,New tests verify proxy creation/removal lifecycle
- [ ] #2 AdaptiveLightingManager creates proxy entities for all managed lights on switch start
- [ ] #3 Proxy entities are removed when switch stops or config changes
- [ ] #4 Entity registry updates add/remove proxies when lights are added/removed from config
- [ ] #5 Config option proxy_mode added (opt-in, replaces intercept)
- [ ] #6 proxy_mode and intercept are mutually exclusive
- [ ] #7 Manager tracks proxy to real entity mappings
- [ ] #8 Existing lifecycle tests pass with proxy mode disabled
- [ ] #9 New tests verify proxy creation and removal lifecycle
- [ ] #10 Manager creates proxy entities for all managed lights on switch start,Proxy entities removed when switch stops or config changes,Entity registry updates add and remove proxies dynamically,proxy_mode config option added (opt-in replaces intercept),proxy_mode and intercept are mutually exclusive,Manager tracks proxy to real entity mappings,Existing lifecycle tests pass with proxy mode disabled,New tests verify proxy creation and removal lifecycle
<!-- AC:END -->





## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add proxy_mode config option to const.py\n2. Add proxy entity creation method to AdaptiveLightingManager\n3. Wire into switch async_turn_on/async_turn_off: create/destroy proxies\n4. Register async_track_entity_registry_updated_event for dynamic light changes\n5. Handle proxy entity cleanup in switch disable\n6. Add validation: proxy_mode and intercept are mutually exclusive\n7. Write lifecycle tests
<!-- SECTION:PLAN:END -->