---
id: TASK-5.2
title: Split manual_control config into brightness and color components
status: To Do
assignee: []
created_date: 2026-05-31 20:41
updated_date: 2026-05-31 20:42
labels:
  - v2
  - config
  - manual_control
dependencies: []
parent_task_id: TASK-5
priority: low
ordinal: 15000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Extend the manual_control config schema to support granular brightness/color control. The set_manual_control service already supports this via LightControlAttributes bitmask (BRIGHTNESS, COLOR, BOTH, NONE), but the YAML/Options config only offers a boolean. Add dict form {\"brightness\": bool, \"color\": bool} while keeping full backward compatibility with plain booleans.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Config schema accepts both bool and dict forms,Dict form supports brightness and color keys,True/False booleans continue to work unchanged (maps to BOTH/NONE),Config flow UI supports granular selection for each component,set_manual_control service behavior unchanged (already works),All existing tests pass
- [ ] #2 Config schema accepts both bool and dict forms
- [ ] #3 Dict form supports brightness and color keys
- [ ] #4 True/False booleans continue to work unchanged (maps to BOTH/NONE)
- [ ] #5 Config flow UI supports granular selection for each component
- [ ] #6 set_manual_control service behavior unchanged (already works)
- [ ] #7 All existing tests pass
<!-- AC:END -->



## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Update CONF_MANUAL_CONTROL schema in const.py to accept vol.Any(bool, dict)\n2. Add LightControlAttributes.from_config() factory to parse bool/dict\n3. Update switch.py init to use new factory\n4. Update config_flow.py options form\n5. Write tests for dict config form\n6. Run full test suite
<!-- SECTION:PLAN:END -->