# Design

## Context

See proposal.md. Teachers use external IDs101–120, separate availability entries and roster; relationship coordinates for these IDs are ID−55. Current CampaignSchoolLayout/Week snapshots remain student-only. A sourced teacher join cannot be inserted into an unrelated campaign checkpoint.

## Goals / Non-Goals

**Goals:** Produce independently captured teacher and group outputs and a reusable pure data module with explicit validation. Execute the actual Chapter012 opcode144 at file0x14 and the native registration, reconciliation and rating helpers.

**Non-Goals:** Campaign-wide teacher migration, playing Chapter012 from the current demo, teacher growth/profile projection, drag/drop4A4680, work-table selection, full menu or saves.

## Decisions

- Keep an isolated school input layout with availability121, both20-slot rosters, five28-byte raw group records and explicit directed relationships. Preserve calendar/reward and student-record hashes as opaque observed fields.
- Audit registration and group layout separately. Execute4D3E90/4D4730 via real VM prefix, or label direct placement calls. Execute4A5F40 cleanup, then4A95F0 for all groups;4D45C0/4D46E0/4D3A20 execute natively.4A2980 is a declared teacher-work/presentation boundary.
- Capture stages before, after join, after reconciliation and after ratings on the same CPU. Replay input placement is declared, not a mouse event. Do not use this evidence to enable current demo grouping.
- Ignore undefined rating output words. The source initializes state/mean/rank but work words are meaningful only in states2/4; keep their four source words without guessing user-facing labels.
- The pure module clones inputs and offers teacher registration, reconciliation and rating functions. Validate roster/availability agreement and identity domains before any change. Permit stale unavailable raw references for cleanup; reject duplicate teachers because the native cleanup does not deduplicate them.
- Native cases cover teacher registration/no-op/direct placement; cleanup with unavailable or duplicate student slots; lecture/adventure branches; asymmetric means and threshold edges16/31/46/61/76/91. Tests compare observed outputs, not another port's expectations.

## Risks / Trade-offs

- [Teacher IDs are not student profile indices] → Keep teacher metadata separate and do not expand existing growth/result rules.
- [Stack-marker words could become claimed work data] → Normalize only branch-defined fields; retain raw words in the audit.
- [A valid helper output could be mistaken for completed story/menu] → Keep isolation/live/full-school/save flags explicit and retain the current demo unchanged.

## Migration Plan

Land verified source evidence first, then the pure module and tests. Run targeted native regeneration, full Godot regression and unchanged demo window checks. Update docs and commit each verified stage. Campaign integration requires a separate change with teacher provenance and operation ownership.
