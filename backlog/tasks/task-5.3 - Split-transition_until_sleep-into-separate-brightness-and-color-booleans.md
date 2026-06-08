---
id: TASK-5.3
title: Split transition_until_sleep into separate brightness and color booleans
status: To Do
assignee: []
created_date: 2026-05-31 20:41
updated_date: 2026-05-31 20:42
labels:
  - v2
  - architecture
  - config
  - breaking
dependencies:
  - TASK-5.1
  - TASK-5.2
parent_task_id: TASK-5
priority: low
ordinal: 16000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Replace the single boolean transition_until_sleep (CONF_ADAPT_UNTIL_SLEEP) with two independent booleans: adapt_until_sleep_brightness and adapt_until_sleep_color. Allows users to independently control whether brightness and/or color transition toward sleep settings after sunset. Includes backward-compat migration reading old key.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 New CONF_ADAPT_UNTIL_SLEEP_BRIGHTNESS and CONF_ADAPT_UNTIL_SLEEP_COLOR keys defined in const.py,Old CONF_ADAPT_UNTIL_SLEEP key accepted with backward-compat mapping to both new keys,SunLightSettings uses separate booleans for brightness and color,get_brightness() respects adapt_until_sleep_brightness only,get_color_temp() and get_rgb_color() respect adapt_until_sleep_color only,Config flow UI shows two separate toggles,All existing tests pass,New tests verify independent brightness/color sleep behavior
- [ ] #2 New CONF_ADAPT_UNTIL_SLEEP_BRIGHTNESS and CONF_ADAPT_UNTIL_SLEEP_COLOR keys defined in const.py
- [ ] #3 Old CONF_ADAPT_UNTIL_SLEEP key accepted with backward-compat mapping to both new keys
- [ ] #4 SunLightSettings uses separate booleans for brightness and color
- [ ] #5 get_brightness() respects adapt_until_sleep_brightness only
- [ ] #6 get_color_temp() and get_rgb_color() respect adapt_until_sleep_color only
- [ ] #7 Config flow UI shows two separate toggles
- [ ] #8 All existing tests pass
- [ ] #9 New tests verify independent brightness/color sleep behavior
<!-- AC:END -->



## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add new constants CONF_ADAPT_UNTIL_SLEEP_BRIGHTNESS + CONF_ADAPT_UNTIL_SLEEP_COLOR in const.py\n2. Add backward-compat migration in schema handling (read old key if new absent)\n3. Update SunLightSettings.__init__ in color_and_brightness.py to accept two booleans\n4. Update get_brightness() to use brightness boolean\n5. Update get_color_temp()/get_rgb_color() to use color boolean\n6. Update switch.py to pass both booleans\n7. Update config_flow.py for two toggles\n8. Write migration + split tests
<!-- SECTION:PLAN:END -->