# Design

## Context

See proposal.md.4A3CA0 menu1..5 sets adventure and6..10 sets teaching unless the adventure gate forces adventure.4A2DA0 copies selected category/key/workID/ordinal into group offsets6/8/10/12. Teacher101 first unlocks10/11/12 at4/4;4/0 and4/1 are empty.

## Goals / Non-Goals

**Goals:** Reproduce sourced mode and course selection, expose revision-safe planning and a usable course window.

**Non-Goals:** Course execution/growth, changing the original new-game date, automatic week advance, saves or complete original school menus.

## Decisions

- Execute real4A3CA0 and4A2DA0 with declared menu/mouse/presentation boundaries. Keep assignment and rating separate; source date inputs4/4,6/5,11/5 are declared before unlocks, not chronology.
- Bind pure operations to the same origin/group/work rules. Resolve source course rows from owned teacher buffers; reject missing teachers, adventure mode, blocked/unavailable courses and stale views before writes.
- Session mode/assignment publishes calculations atomically. New course example initialization computes an independent source roster plus explicitly declared4/4 unlock/prepare/selection before publication; original initialize remains unchanged. Never accept an arbitrary after image or user calendar change.
- Add a separate course page to the existing panel and keep independent new-game/example sessions. UI selects a taught class, switches its mode, lists all valid source courses by category and assigns a course. Do not imitate native unsafe clicks past the list end.

## Risks / Trade-offs

- [Example date could be mistaken for progression] → Visible4月第4周课程示例 label and explicit initialization journal phase.
- [Cached work list belongs to another teacher] → Derive and validate the selected teacher view for each operation.
- [Course page reduces space] → Separate page,1024×768 screenshot and actual-input checks.
