# Design

## Context

See proposal.md. Existing origin session owns the initialized subset. Student movement already consumes scoped group rules; teacher movement only validates117/118. Native dragging temporarily leaves counts and indices stale, so explicit reconciliation and rating are required before another command.

## Goals / Non-Goals

**Goals:** Prove101 and actual source student movement, publish coherent owned state and expose point-and-click grouping in the main window.

**Non-Goals:** Save loading/writing, full original menu chronology, course assignment, new teacher joins and migration of the old returned campaign.

## Decisions

- Extend the new-game emulator with existing finite drag bodies and declared pointer/button/presentation boundaries. Execute a continuous source-initialized command sequence; export immediate, cleanup and rated checkpoints separately, without modifying historical fixtures.
- Bind teacher101 rules to the initializer fingerprint and exact static profile. Keep legacy117/118 validation intact; the one-teacher domain cannot require teacher exchange branches.
- Keep ephemeral drag controls in a derived command working copy, then strip them before publishing the canonical school snapshot. Derive current source cells and rating from owned state. No caller-provided after image, profiles or course records are accepted.
- Publish movement/reconcile/rate atomically at one new revision; refusal leaves snapshot, revision and journal unchanged. Reconcile work selection as in native teacher cleanup.
- Use a separate panel on the same main scene. Click a member then an appropriate class cell or waiting area; Escape cancels selection. Navigation preserves the new session, explicit restart replaces it. Block battle ticking and shortcuts while school is open.

## Risks / Trade-offs

- [Original UI inputs are declared] → Label evidence as isolated source execution; verify prototype mouse/keyboard through real viewport events.
- [Intermediate counts differ] → Compare each native phase and publish only the rated checkpoint.
- [Window layouts can overflow] → Capture and inspect1024×768 rendering before acceptance.
