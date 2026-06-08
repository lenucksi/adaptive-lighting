---
id: TASK-6.3
title: Integrate manual control and feature detection with proxy
status: To Do
assignee: []
created_date: 2026-05-31 21:03
updated_date: 2026-05-31 21:04
labels:
  - architecture
  - refactoring
  - proxy
dependencies:
  - TASK-6.2
parent_task_id: TASK-6
priority: low
ordinal: 20000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Wire all existing feature flags into the proxy entity: manual control detection via take_over_control, adapt_only_on_bare_turn_on logic (mark as manual when turn_on includes brightness/color params), detect_non_ha_changes state reconciliation, sleep mode interaction, and autoreset of manual control timers. The proxy must track whether its wrapped light is manually controlled and skip adaptation accordingly.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 take_over_control detects non-AL changes to the wrapped light (via state_changed events),adapt_only_on_bare_turn_on marks proxy turn_on with explicit params as manual control,detect_non_ha_changes reconciles proxy state with real light state,sleep mode toggles correctly affect proxy adaptation behavior,auto_reset_manual_control works with proxy entity,LightControlAttributes bitmask respected by proxy turn_on,Manual control state persists across HA restarts via RestoreEntity,All existing manual control tests pass
- [ ] #2 take_over_control detects non-AL changes to the wrapped light via state_changed events
- [ ] #3 adapt_only_on_bare_turn_on marks proxy turn_on with explicit params as manual control
- [ ] #4 detect_non_ha_changes reconciles proxy state with real light state
- [ ] #5 sleep mode toggles correctly affect proxy adaptation behavior
- [ ] #6 auto_reset_manual_control works with proxy entity
- [ ] #7 LightControlAttributes bitmask respected by proxy turn_on
- [ ] #8 Manual control state persists across HA restarts via RestoreEntity
- [ ] #9 All existing manual control tests pass
- [ ] #10 take_over_control detects non-AL changes via state_changed events,adapt_only_on_bare_turn_on marks proxy turn_on with explicit params as manual control,detect_non_ha_changes reconciles proxy state with real light state,sleep mode toggles correctly affect proxy adaptation,auto_reset_manual_control works with proxy entity,LightControlAttributes bitmask respected by proxy turn_on,Manual control state persists across HA restarts via RestoreEntity,All existing manual control tests pass
<!-- AC:END -->





## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Wire take_over_control detection into proxy lifecycle\n2. Implement adapt_only_on_bare_turn_on logic in async_turn_on\n3. Hook into state_changed_event_listener for non-HA change detection\n4. Wire sleep mode interaction with proxy (adapt_until_sleep, sleep settings)\n5. Implement auto_reset_manual_control integration\n6. Add RestoreEntity for manual control state persistence\n7. Write integration tests for manual control via proxy
<!-- SECTION:PLAN:END -->