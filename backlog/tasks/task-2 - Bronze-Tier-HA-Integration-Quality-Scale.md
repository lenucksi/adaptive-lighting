---
id: TASK-2
title: Bronze Tier HA Integration Quality Scale
status: Done
assignee:
  - "@opencode-agent"
created_date: 2026-05-28 22:07
updated_date: 2026-05-30 17:25
labels:
  - quality
  - compliance
  - refactoring
dependencies: []
references:
  - https://github.com/basnijholt/adaptive-lighting/issues/1195
priority: high
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Home Assistant Bronze Tier Compliance erreichen. PR #1403 (action-setup) bereits gemergt.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 has_entity_name = True gesetzt
- [ ] #2 entity-unique-id für alle Entities
- [ ] #3 config-flow-test-coverage
- [ ] #4 ConfigEntry.runtime_data migriert
- [ ] #5 common-modules ausgelagert
- [ ] #6 test-before-configure/-setup implementiert
- [ ] #7 docs-Anforderungen erfüllt
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Plan approved. Implement:
1. has_entity_name=True + adjust name/device_info
2. runtime_data migration with backward compat
3. test-before-configure/setup 
4. config-flow-test-coverage
5. quality_scale.yaml
6. unique-config-entry check
Skip AC #5 (common-modules) and AC #2 (unique-id) — both already done.
Important: Keep backward compatibility with hass.data lookups used by _switches_with_lights and _switches_from_service_call.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Bronze Tier compliance: has_entity_name, runtime_data migration (with backward compat via hass.data), config-flow test coverage, test-before-configure/setup, quality_scale.yaml. Commit 3639a4c on tasks/TASK-2-Bronze.
<!-- SECTION:FINAL_SUMMARY:END -->