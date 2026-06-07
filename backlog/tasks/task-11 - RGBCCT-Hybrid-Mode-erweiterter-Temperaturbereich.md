---
id: TASK-11
title: RGB+CCT Hybrid Mode (erweiterter Temperaturbereich)
status: Done
assignee: []
created_date: 2026-05-30 15:45
updated_date: 2026-05-30 16:38
labels:
  - feature
  - v2
dependencies: []
references:
  - https://github.com/basnijholt/adaptive-lighting/issues/1287
priority: medium
ordinal: 11000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Erweitert AL um einen Hybrid-Modus der RGB-LEDs für sehr warme Farbtemperaturen nutzt (wo CCT nicht niedrig genug dimmen kann) und automatisch zwischen RGB- und CCT-Modus umschaltet basierend auf konfigurierbaren Schwellwerten für Temperatur und Helligkeit
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 1 Config-Optionen definiert: rgb_color_temp_threshold, rgb_brightness_threshold, rgb_max_brightness
- [ ] #2 2 prepare_adaptation_data() erweitert: wenn Ziel-Temp < threshold → RGB-Modus (hs_color/rgb_color statt color_temp)
- [ ] #3 3 RGB→CCT Umschaltung bei Überschreitung des Thresholds (beide Richtungen: wärmer vs. kälter)
- [ ] #4 4 Brightness-Begrenzung für RGB separat (da RGB-LEDs meist schwächer sind)
- [x] #5 5 manual_control Tracking für RGB und CCT getrennt
- [ ] #6 6 Sanfter Übergang zwischen RGB und CCT (Transition/Fade, kein harter Sprung)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implementiert: Constants, VALIDATION_TUPLES, _set_changeable_settings, prepare_adaptation_data (force_rgb + brightness cap). AC 1-4 done. AC 5 (manual_control split) und AC 6 (smooth transition) als Folge-TODO.

AC 5 (manual_control split for force_rgb) complete. Committed in 38e4547.
<!-- SECTION:NOTES:END -->