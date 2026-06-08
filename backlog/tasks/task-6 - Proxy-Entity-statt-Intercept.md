---
id: TASK-6
title: Proxy Entity statt Intercept
status: To Do
assignee: []
created_date: 2026-05-28 22:07
updated_date: 2026-05-31 21:02
labels:
  - architecture
  - refactoring
dependencies: []
references:
  - https://github.com/basnijholt/adaptive-lighting/issues/947
priority: low
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Statt fragilen Intercept-Hack einen echten HA Proxy-Light-Entity anbieten. Grundlegende Architekturänderung.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Proxy-Light-Entity implementiert
- [ ] #2 Intercept-Mechanismus ersetzt
- [ ] #3 Abwärtskompatibilität gewahrt
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Architecture Overview

Current approach: A service-call interceptor (hass_utils.py) that replaces light.turn_on/light.toggle handlers with a proxy. Fragile because it accesses hass.services._services (private API), creates a global bottleneck, has inherent race conditions, and uses fragile context ID hashing (:al: marker).

Target approach: An AdaptiveLightProxy(LightEntity) per managed light. Instead of intercepting ALL light.turn_on calls globally, each proxy wraps one real light. When async_turn_on is called on the proxy, it merges adaptation data and delegates to the real light's service. This uses HA's first-class entity model.

## What the proxy entity replaces

| Current (Interceptor) | New (Proxy Entity) |
|---|---|
| hass_utils.py — service registry hack | Standard LightEntity subclass |
| _service_interceptor_turn_on_handler — global dispatcher | Per-entity async_turn_on override |
| _separate_entity_ids — entity→switch mapping | Proxy IS the mapping |
| _correct_for_multi_light_intercept — multi-light guard | Each entity handles itself |
| Context hashing (:al:) + proactive tracking | Natural entity-level lifecycle |
| _proactively_adapting_contexts dict | No longer needed |

## What stays the same
- prepare_adaptation_data() — sun position computation engine
- _execute_adaptation_calls() — split command execution
- SunLightSettings — color/brightness calculation
- Manual control logic (LightControlAttributes, takeover detection)
- Sleep mode handling

## Key challenge
Proxy entities have DIFFERENT entity_ids than the real lights. Automation targeting real lights bypass the proxy. Migration strategy needed: offer proxy as opt-in alternative first, deprecate intercept later.

## Implementation Order

Phase 1 (Foundation) → Phase 2 (Core Logic) → Phase 3 (Features) → Phase 4 (Migration)

### Phase 1 — Proxy Entity Foundation (~2-3 hrs)
Create the LightEntity subclass. Delegate is_on, brightness, color_temp, supported_color_modes to the wrapped entity. Handle entity registration with unique_id derived from switch name + real entity_id.

### Phase 2 — Core Adaptation Logic (~2-3 hrs)
Implement async_turn_on to call prepare_adaptation_data(), merge brightness/color_temp into kwargs, then call the real light's turn_on. Support separate_turn_on_commands (split into brightness+color calls with delay).

### Phase 3 — Feature Integration (~2-3 hrs)
Wire manual control detection, sleep mode, adapt_only_on_bare_turn_on, detect_non_ha_changes into the proxy. Handle state reconciliation between proxy and real light.

### Phase 4 — Interceptor Removal (~2-3 hrs)
Remove hass_utils.py, all dispatch methods, context hashing. Add config migration from intercept→proxy. Update docs.

## Reference
- Upstream discussion: basnijholt/adaptive-lighting#947
- HA template light (reference proxy pattern): homeassistant/components/template/light.py
- HA light entity base: LightEntity in homeassistant/components/light/__init__.py
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Analysis complete. 5 subtasks created mapping to 3 ACs.
<!-- SECTION:NOTES:END -->