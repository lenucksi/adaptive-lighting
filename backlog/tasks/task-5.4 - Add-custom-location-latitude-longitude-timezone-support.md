---
id: TASK-5.4
title: Add custom location (latitude/longitude/timezone) support
status: To Do
assignee: []
created_date: 2026-05-31 20:41
updated_date: 2026-05-31 20:42
labels:
  - v2
  - feature
  - location
dependencies:
  - TASK-5.3
parent_task_id: TASK-5
priority: low
ordinal: 17000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add optional per-switch location overrides for latitude, longitude, timezone, sunrise_time, and sunset_time. When not set, default to HA config location. Allows users to simulate lighting for a different geographic location or manually override sunrise/sunset times.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 New config options: latitude, longitude, timezone (all optional, default to HA config),New config options: sunrise_time, sunset_time (optional, override sun position calculation),SunEvents constructor accepts optional location overrides,Falls back to hass.config defaults when not specified,Config flow UI shows optional location override section,All existing tests pass with default (no-override) behavior,New tests verify custom location and time overrides
- [ ] #2 New config options: latitude, longitude, timezone (optional, default to HA config)
- [ ] #3 New config options: sunrise_time, sunset_time (optional, override sun position)
- [ ] #4 SunEvents constructor accepts optional location overrides
- [ ] #5 Falls back to hass.config defaults when not specified
- [ ] #6 Config flow UI shows optional location override section
- [ ] #7 All existing tests pass with default (no-override) behavior
- [ ] #8 New tests verify custom location and time overrides
<!-- AC:END -->



## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add new CONF_LATITUDE, CONF_LONGITUDE, CONF_TIMEZONE, CONF_SUNRISE_TIME, CONF_SUNSET_TIME to const.py\n2. Update SunEvents in color_and_brightness.py to accept optional location overrides\n3. Add conditional astral.Location creation only when coords differ from HA config default\n4. Integrate sunrise_time/sunset_time into get_sunrise_sunset logic\n5. Update switch.py to pass location params from config to SunEvents\n6. Update config_flow.py with optional location override section\n7. Review upstream PR #1470 for reference pattern\n8. Write tests for custom location behavior
<!-- SECTION:PLAN:END -->