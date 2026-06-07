---
id: TASK-1
title: Deprecated Constants ersetzen
status: Done
assignee: []
created_date: 2026-05-28 22:07
updated_date: 2026-05-30 17:10
labels:
  - tech-debt
  - compatibility
dependencies: []
references:
  - https://github.com/basnijholt/adaptive-lighting/issues/1182
priority: high
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Adaptive Lighting nutzt HA-Deprecated-Konstanten (COLOR_MODE_XY, SUPPORT_BRIGHTNESS, SUPPORT_COLOR, SUPPORT_COLOR_TEMP, SUPPORT_TRANSITION), die in HA Core 2026.1 entfernt werden.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Alle deprecated Constants durch aktuelle HA-Äquivalente ersetzt
- [ ] #2 Tests grün
- [ ] #3 Keine Deprecation-Warnings mehr im Log
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TASK-1 Assessment: Already Complete

The deprecated HA constants (COLOR_MODE_XY, SUPPORT_BRIGHTNESS, SUPPORT_COLOR, SUPPORT_COLOR_TEMP, SUPPORT_TRANSITION) are **not used anywhere** in our custom_components codebase.

### Modern equivalents already in use:
- ColorMode.XY, ColorMode.RGB, ColorMode.COLOR_TEMP, ColorMode.BRIGHTNESS (via )
- LightEntityFeature (via )  
- ATTR_SUPPORTED_COLOR_MODES (via )
- ATTR_SUPPORTED_FEATURES (via )

All imports reference the modern HA enums/attributes. No code changes needed.
<!-- SECTION:FINAL_SUMMARY:END -->