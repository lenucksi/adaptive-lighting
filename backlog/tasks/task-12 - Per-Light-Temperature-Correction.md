---
id: TASK-12
title: Per-Light Temperature Correction
status: Done
assignee: []
created_date: 2026-05-30 15:45
updated_date: 2026-05-30 16:38
labels:
  - feature
  - v2
dependencies: []
references:
  - https://github.com/basnijholt/adaptive-lighting/issues/1428
priority: low
ordinal: 12000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Kalibrierungsoffsets pro Lampe um Fertigungsunterschiede in der Farbtemperaturwiedergabe auszugleichen. Zwei Ankerpunkte mit gemessenen Korrekturen und linearer Interpolation dazwischen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 1 Config-Optionen definiert: light_calibration als Dict mit light_entity_id → {anchor_temp, correction_offset}
- [ ] #2 2 Transformationsfunktion implementiert: offset = lerp(anchor_A, anchor_B, current_temp)
- [ ] #3 3 Integration in prepare_adaptation_data() vor dem Senden von color_temp
- [ ] #4 4 Kompatibel mit existierendem manual_control Tracking
- [ ] #5 5 Doku: Anleitung zur Kalibrierung (Referenzgerät + Vergleich)
- [x] #6 6 Prüfen ob Lösung besser in Z2M/ZHA-Ebene gehört (Interop mit ha-calibrated_led)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implementiert: Constants, VALIDATION_TUPLES, light_calibration in _set_changeable_settings, _calibrate_color_temp Methode mit Zwei-Anker-Interpolation, Integration in prepare_adaptation_data. AC 1-5 done. AC 6 (Prüfung Z2M/ZHA-Integration) offen.

AC 6 (Z2M/ZHA calibration interaction): Analyzed. Our Kelvin offsets and Z2M mired range mapping operate in different domains, so calibration composes correctly. No code change needed. (commit 38e4547)
<!-- SECTION:NOTES:END -->