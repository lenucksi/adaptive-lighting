---
id: TASK-13
title: Lux Sensor Integration
status: Done
assignee: []
created_date: 2026-05-30 15:45
updated_date: 2026-05-30 16:16
labels:
  - feature
  - v2
dependencies: []
references:
  - https://github.com/basnijholt/adaptive-lighting/issues/124
priority: medium
ordinal: 13000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Adaptive Lighting soll Lux-Sensor-Entities von Zigbee Helligkeitssensoren lesen können und die Lampenhelligkeit so regeln dass die gemessene + künstliche Beleuchtung eine Zielhelligkeit erreicht. Farbtemperatur bleibt von der Sonnenkurve bestimmt.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 1 Config-Optionen definiert: lux_sensor_entity_id, target_lux, brightness_curve_factor
- [ ] #2 2 Sensor-Werte aus hass.states lesen im _update_cycle
- [ ] #3 3 Regelkreis (P-Regler) für Helligkeit: soll_lux - ist_lux = delta → brightness_anpassung
- [ ] #4 4 Farbtemperatur bleibt von SunLightSettings bestimmt (nur Brightness wird moduliert)
- [ ] #5 5 manual_control detection: wenn User Helligkeit manuell ändert → Regelkreis pausieren
- [ ] #6 6 Fallback: wenn Sensor nicht verfügbar → normaler AL-Modus ohne Lux-Regelung
- [ ] #7 Config-Optionen definiert: lux_sensor_entity_id, target_lux, brightness_curve_factor
- [ ] #8 Sensor-Werte aus hass.states lesen im _update_cycle
- [ ] #9 Regelkreis (P-Regler) für Helligkeit: soll_lux - ist_lux = delta → brightness_anpassung
- [ ] #10 Farbtemperatur bleibt von SunLightSettings bestimmt (nur Brightness moduliert)
- [ ] #11 manual_control detection: wenn User Helligkeit ändert → Regelkreis pausieren
- [ ] #12 Fallback: wenn Sensor nicht verfügbar → normaler AL-Modus ohne Lux-Regelung
<!-- AC:END -->