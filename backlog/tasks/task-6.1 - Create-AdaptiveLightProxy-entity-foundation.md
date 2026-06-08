---
id: TASK-6.1
title: Create AdaptiveLightProxy entity foundation
status: To Do
assignee: []
created_date: 2026-05-31 21:02
updated_date: 2026-05-31 21:04
labels:
  - architecture
  - refactoring
  - proxy
dependencies: []
parent_task_id: TASK-6
priority: low
ordinal: 18000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create the core AdaptiveLightProxy(LightEntity) class that wraps a real light entity. Delegate all state properties (is_on, brightness, color_temp_kelvin, hs_color, supported_color_modes, min/max color temp, effect, effect_list) to the wrapped real entity. Handle entity registration with unique_id, device_info, and name. Implement async_added_to_hass and async_will_remove_from_hass for lifecycle. Basic async_turn_on/async_turn_off pass-through to the real entity.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 AdaptiveLightProxy entity class created inheriting from LightEntity,All state properties delegate to the wrapped real entity (is_on, brightness, color_temp, etc.),unique_id derived from switch name + real entity_id,async_added_to_hass and async_will_remove_from_hass implemented,proxy registers correctly as a HA light entity,Basic async_turn_on/async_turn_off delegate to real entity unchanged,device_info groups proxy under the same device as the switch,Entity registry integration works (unique_id dedup)
- [ ] #2 AdaptiveLightProxy entity class created inheriting from LightEntity
- [ ] #3 All state properties delegate to the wrapped real entity (is_on, brightness, color_temp, etc.)
- [ ] #4 unique_id derived from switch name + real entity_id
- [ ] #5 async_added_to_hass and async_will_remove_from_hass implemented
- [ ] #6 Proxy registers correctly as a HA light entity
- [ ] #7 Basic async_turn_on/async_turn_off delegate to real entity unchanged
- [ ] #8 device_info groups proxy under the same device as the switch
- [ ] #9 Entity registry integration works (unique_id dedup)
- [ ] #10 AdaptiveLightProxy entity class created inheriting from LightEntity,All state properties delegate to wrapped real entity,unique_id derived from switch name + real entity_id,async_added_to_hass and async_will_remove_from_hass implemented,Proxy registers correctly as HA light entity,Basic async_turn_on and async_turn_off delegate to real entity unchanged,device_info groups proxy under same device as switch,Entity registry integration works
<!-- AC:END -->





## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Create AdaptiveLightProxy class in switch.py (or new proxy.py file)\n2. Implement __init__ with wrapped_entity_id, switch reference\n3. Implement all state delegation properties (is_on, brightness, color_temp, etc.)\n4. Implement unique_id, name, device_info\n5. Implement async_added_to_hass lifecycle\n6. Implement async_turn_on/async_turn_off pass-through\n7. Write unit tests for state delegation
<!-- SECTION:PLAN:END -->