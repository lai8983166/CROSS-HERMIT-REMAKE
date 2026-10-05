# Design

## Context

See proposal.md. The current source catalog has four students and zero teachers. Native 4A4680 requires a teacher before accepting a student into a group; this change uses commands 0B–0D, which do not have that requirement.

## Goals / Non-Goals

**Goals:** Execute original command and sort consumers, port their ordering semantics, publish through the catalog owner, and expose that operation in the existing window.

**Non-Goals:** Teacher catalog extension, drag/drop grouping, course work tables, teacher sorting, original save/process writes or claiming a complete school screen.

## Decisions

- A bounded emulator executes 4A3CA0 and 4A8BF0 together. Menu hit testing, selected group, audio, visual feedback and debug checks are declared stubs. Source snapshots are explicitly declared starting data, not a continuous native return witness.
- Capture writes outside the emulator stack and require only the waiting ID buffer and sort-mode byte. Capture input profiles and source category bytes; include divergent levels/attribute totals, ties, empty and single-member cases.
- The pure calculator consumes current catalog data and source category rules. Numeric sorting uses the original nested swaps, because stable sorting changes tied results. Category sorting scans categories 0–5, preserving order within each category.
- Add optional `idle_sort_mode` to school control only on a sorting action; existing frozen boot fixtures remain byte-identical. Before an action the selector shows the boot level-order default. No-change operations are suppressed once an explicit mode exists.
- CampaignResultState guards a completed boot and no pending result/preparation/return. It validates before calculation and publishes once when list or explicit mode changes. The adapter loads only the new fixture's rules, never its expected outcomes.
- The UI replaces its roster-order display with waiting-order display and a selector. Selection is keyed by student ID; browsing and duplicate completion events cannot overwrite the sorted catalog.

## Risks / Trade-offs

- [Native category values outside 0–5 leave scratch output undefined] → Reject invalid rule/category inputs before publication.
- [Declared source inputs could be mistaken for live operations] → Record replay boundaries and retain existing false live/save/full-school flags.
- [Adding a selector moves list coordinates] → Update window input tests to use observed item rectangles and verify actual viewport mouse/key input.

## Migration Plan

Add new files and rules without rewriting frozen evidence. Run targeted Python native regeneration checks, all Godot suites, window input verification and strict OpenSpec validation. Commit each verified stage; no push. Reverting these commits restores the browsing-only school page.
