---
id: TASK-6.5
title: Remove interceptor mechanism and ensure backwards compatibility
status: To Do
assignee: []
created_date: 2026-05-31 21:03
updated_date: 2026-05-31 21:04
labels:
  - architecture
  - refactoring
  - proxy
dependencies:
  - TASK-6.4
parent_task_id: TASK-6
priority: low
ordinal: 22000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Remove the fragile service-call interceptor now that the proxy entity approach is proven. Delete hass_utils.py entirely. Remove _service_interceptor_turn_on_handler, _service_interceptor_turn_on_single_light_handler, _separate_entity_ids, _correct_for_multi_light_intercept, _get_entity_list. Remove context hashing (is_our_context, :al: marker). Remove _proactively_adapting_contexts tracking. Add config migration from intercept → proxy_mode. Ensure all adaptation still works for proxy_mode users.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 hass_utils.py removed entirely,_service_interceptor_turn_on_handler and related dispatch methods removed,Context hashing (is_our_context, :al: marker) removed,_proactively_adapting_contexts tracking removed,Config migration from intercept=true to proxy_mode=true for existing configs,All adaptation still functions correctly via proxy entities,Backwards compat: intercept=false users continue to work via event-reactive path,All existing tests pass after removal,Config flow updated to reflect proxy_mode option
- [ ] #2 hass_utils.py removed entirely
- [ ] #3 _service_interceptor_turn_on_handler and related dispatch methods removed
- [ ] #4 Context hashing (is_our_context, :al: marker) removed
- [ ] #5 _proactively_adapting_contexts tracking removed
- [ ] #6 Config migration from intercept to proxy_mode for existing configs
- [ ] #7 All adaptation still functions correctly via proxy entities
- [ ] #8 Backward compat: intercept=false users continue via event-reactive path
- [ ] #9 All existing tests pass after removal
- [ ] #10 Config flow updated to reflect proxy_mode option
- [ ] #11 hass_utils.py removed entirely,Interceptor dispatch methods removed,Context hashing is_our_context removed,_proactively_adapting_contexts tracking removed,Config migration from intercept to proxy_mode for existing configs,All adaptation works via proxy entities,Backward compat intercept=false users work via event-reactive path,All existing tests pass after removal,Config flow updated for proxy_mode option
<!-- AC:END -->





## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Remove hass_utils.py and all references\n2. Remove _service_interceptor_turn_on_handler and related dispatch\n3. Remove _separate_entity_ids, _correct_for_multi_light_intercept, _get_entity_list\n4. Remove context hashing (is_our_context, is_our_context_id, :al: marker)\n5. Remove _proactively_adapting_contexts tracking\n6. Add config migration logic intercept→proxy_mode\n7. Add config flow migration for existing entries\n8. Update documentation\n9. Run full test suite
<!-- SECTION:PLAN:END -->