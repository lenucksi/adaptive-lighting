---
id: TASK-4
title: Manual Control System stabilisieren
status: Archived
assignee: []
created_date: 2026-05-28 22:07
labels:
  - reliability
  - refactoring
dependencies: []
references:
  - https://github.com/basnijholt/adaptive-lighting/issues/290
  - https://github.com/basnijholt/adaptive-lighting/issues/1471
  - https://github.com/basnijholt/adaptive-lighting/issues/1187
priority: medium
ordinal: 4000
---
## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Manual Control System hat mehrere Fehler: Sleep-Mode feuert manual_control (#1471), set_manual_control mit Light-Gruppen kaputt (#1187), Light-Group Color Temp löst manual_control aus (#1164), autoreset_control_seconds schlägt fehl (#1233).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Sleep-Mode feuert kein falsches manual_control-Event
- [ ] #2 set_manual_control funktioniert mit HA Light-Gruppen
- [ ] #3 autoreset_control_seconds funktioniert korrekt
<!-- AC:END -->