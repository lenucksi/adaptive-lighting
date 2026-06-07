---
id: TASK-10
title: Sunrise-Simulation Feature
status: Done
assignee: []
created_date: 2026-05-30 15:45
updated_date: 2026-05-30 16:38
labels:
  - feature
  - v2
dependencies: []
references:
  - https://github.com/moag1000/beurer_daylight_lamps/blob/main/blueprints/automation/beurer_daylight_lamps/morning_light_therapy.yaml
priority: medium
ordinal: 10000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Sonnenaufgangs-Simulation für Adaptive Lighting: Eine Sequenz die Lampen über einen konfigurierbaren Zeitraum von Rot/Orange (über RGB) durch die Farben eines Sonnenaufgangs fährt, zur CCT wechselt, auf volle Helligkeit hochdimmt, dort hält und dann ausschaltet
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 1 Blueprint erstellt das AL-Service/Entity triggert (Scheduling+Firing outsourced)
- [ ] #2 2 AL Service/Entity definiert das sunrise_sequence mit Parametern: lights, start_time, duration, hold_time, max_brightness, min_color_temp, max_color_temp, rgb_color_temp_threshold
- [ ] #3 3 Phase 1 implementiert: RGB warm (rot→orange) mit niedriger Brightness, langsam steigend
- [ ] #4 4 Phase 2 implementiert: Übergang RGB→CCT am Schwellwert mit konfigurierbarem Threshold
- [ ] #5 5 Phase 3 implementiert: CCT von warm→kalt + Brightness 1%→100%
- [ ] #6 6 Phase 4 implementiert: Hold für X Minuten auf Max-Brightness + Target-Color-Temp
- [ ] #7 7 Phase 5 implementiert: Graceful Shutdown (sanftes Dimmen + Ausschalten)
- [x] #8 8 Interrupt-Handling: Benutzereingriff bricht Sequenz ab (ähnlich manual_control)
- [x] #9 9 Integration mit ALs bestehenden Config-Optionen (min/max brightness, color_temp_range, adapt_* switches)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implementation complete: ACs 1-7 done (sunrise.py, service, blueprint, services.yaml). AC 8 (interrupt-handling via manual_control tracking) und AC 9 (AL Switch Config-Integration) als Folge-TODO markiert.

AC 8 (interrupt handling during sunrise) and AC 9 (Integration mit AL Config-Optionen) complete. Committed in 38e4547.
<!-- SECTION:NOTES:END -->