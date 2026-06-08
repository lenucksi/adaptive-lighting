---
id: TASK-6.2
title: Implement core adaptation merging in proxy async_turn_on
status: To Do
assignee: []
created_date: 2026-05-31 21:02
updated_date: 2026-05-31 21:04
labels:
  - architecture
  - refactoring
  - proxy
dependencies:
  - TASK-6.1
parent_task_id: TASK-6
priority: low
ordinal: 19000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement the core feature of the proxy entity: override async_turn_on to compute sun-position-based brightness and color temperature via prepare_adaptation_data(), merge these into the caller's kwargs, then delegate to the real light entity. Support separate_turn_on_commands (split brightness and color into sequential calls with send_split_delay). Handle transition times from config.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 async_turn_on computes adaptation data via prepare_adaptation_data(),Brightness from adaptation merged into turn_on kwargs when not overridden by caller,Color temperature merged into turn_on kwargs when not overridden,separate_turn_on_commands splits brightnes and color into sequential service calls with delay,Transition duration from config applied to the delegated turn_on call,Sleep mode settings respected when sleep mode is active,All existing tests for adaptation computation still pass,New tests verify proxy turn_on produces correct service calls
- [ ] #2 async_turn_on computes adaptation data via prepare_adaptation_data()
- [ ] #3 Brightness from adaptation merged into turn_on kwargs when not overridden by caller
- [ ] #4 Color temperature merged into turn_on kwargs when not overridden
- [ ] #5 separate_turn_on_commands splits brightness and color into sequential calls with delay
- [ ] #6 Transition duration from config applied to the delegated turn_on call
- [ ] #7 Sleep mode settings respected when sleep mode is active
- [ ] #8 All existing tests for adaptation computation still pass
- [ ] #9 New tests verify proxy turn_on produces correct service calls
- [ ] #10 async_turn_on computes adaptation data via prepare_adaptation_data,Brightness from adaptation merged into turn_on kwargs when not overridden by caller,Color temperature merged into turn_on kwargs when not overridden,separate_turn_on_commands splits brightness and color into sequential calls with delay,Transition duration from config applied to delegated turn_on call,Sleep mode settings respected when sleep mode is active,All existing tests for adaptation computation still pass,New tests verify proxy turn_on produces correct service calls
<!-- AC:END -->





## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Override async_turn_on in AdaptiveLightProxy\n2. Call switch.prepare_adaptation_data() for the wrapped entity\n3. Merge brightness/color_temp into kwargs (caller params take precedence)\n4. For separate_turn_on_commands: use _execute_adaptation_calls pattern\n5. Handle sleep mode setting selection\n6. Call real light via hass.services.async_call or wrapped entity's turn_on\n7. Write tests for merged calls and split commands
<!-- SECTION:PLAN:END -->