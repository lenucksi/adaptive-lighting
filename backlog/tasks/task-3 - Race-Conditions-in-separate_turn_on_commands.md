---
id: TASK-3
title: Race Conditions in separate_turn_on_commands
status: To Do
assignee: []
created_date: 2026-05-28 22:07
labels:
  - reliability
  - bug
dependencies: []
references:
  - https://github.com/basnijholt/adaptive-lighting/issues/1473
  - https://github.com/basnijholt/adaptive-lighting/issues/1373
  - https://github.com/basnijholt/adaptive-lighting/issues/802
priority: high
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
separate_turn_on_commands (Workaround für IKEA/Zigbee) erzeugt mehrere Race Conditions: multi-light intercept adaptiert nur 1. Light (#1473), "on at 0%" nach turn_off (#1373), take_over_control kaputt (#802).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 multi_light_intercept + separate_turn_on_commands adaptiert alle Lights korrekt
- [ ] #2 Kein 'on at 0% brightness' nach turn_off
- [ ] #3 take_over_control funktioniert mit separate_turn_on_commands
<!-- AC:END -->