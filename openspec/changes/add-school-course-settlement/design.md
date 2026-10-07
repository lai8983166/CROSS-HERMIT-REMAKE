# Design

## Context

See proposal.md. Existing planning owns source4/0 and declared4/4 schools separately.4A6A10 prepares class result words from4A95F0.4BD870 initializes the result task and mode0 invokes4C00C0; state4 classes invoke4C0400 and4D3600 for their students.

## Goals / Non-Goals

**Goals:** Reproduce source course packets, caps, random learning, attributes and levels; atomically expose one course settlement in the explicit example.

**Non-Goals:** Original result confirmation/MVP fields, weekly unlock/cleanup, actual calendar/ADV progression or saves. Planning remains the prior separate behavior.

## Decisions

- Freeze native preparation and settlement separately with finite write guards. Use real source tables, native RNG and declared clock seeds; do not infer formulas solely from older notes.
- Pure settlement derives class eligibility and packet coefficients from source ratings. Validate all records/rules/classes before writes; unsupported adventure result inputs or unavailable courses fail without mutation.
- Keep complete owned growth records separate until settlement. Build initial records from the already validated origin pools/statuses, matching source initialization. Update school member attributes/levels and growth records together after all calculations succeed.
- Permit settlement only for the declared4/4 example, once until its explicit restart. Fixed declared seed4660 is visible in evidence/journal. Duplicate delivery returns the same result; stale revisions refuse. Planning/movement can continue afterwards, but cannot reopen or replay the settled example. This avoids claiming a new week.
- Add a visible example settlement button and compact student before/after summary to the course page; preserve normal new-game/returned-campaign behavior and existing window tests.

## Risks / Trade-offs

- [Old growth notes may describe an intended but unused average factor] → Compare executed packets before implementing and record any correction.
- [Skill learning consumes RNG even on rejected attribute requirements] → Compare every native draw/state and source skill order.
- [Repeated button could grow students twice] → Session completion state checked after revision/rules validation; explicit restart is the only reset.
- [Partial data publication] → Calculate growth, school profile projection and ratings on candidates before one revision/journal publication.
