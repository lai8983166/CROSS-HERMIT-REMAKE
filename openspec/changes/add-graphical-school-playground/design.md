## Context

The independent NewGameSchoolSession supports declared April/week-four growth, confirmation and MVP handoff over teacher101 and students3/4/9. The existing panels are research interfaces, and all evidence must retain its original byte content. See proposal.md for motivation.

## Goals / Non-Goals

Provide a persistent graphical slice over this domain. The local save belongs to the remake playground, not the original executable. Chapter completion and new-week progression are outside this change.

## Decisions

- Add a separate controller around the existing session instead of copying growth formulas into presentation. It owns a bounded list of successful commands; duplicates do not lengthen it. Rule loading stays local and deterministic.
- Save commands with source fingerprints and a canonical final-state digest. Rebuild a fresh candidate through existing validated APIs before publishing; arbitrary decoded snapshots are never assigned to a live session. This costs replay time but avoids trusting partially restored internal fields.
- Save via a same-directory temporary file, keep a previous copy, and report failures. Restore a valid backup when the primary is corrupt; do not overwrite corrupt user data merely on launch. Explicit restart confirmation belongs to the UI and is not an agent approval flow.
- Export a small named presentation catalog from existing original image/text resources. Provenance and crop rectangles accompany output. Rendering uses runtime-loaded PNG textures so a fresh checkout does not depend on a Godot editor import pass. Unknown names/portraits fall back to IDs; no made-up rules.
- Use a dedicated responsive Control-based scene with class cards, portrait buttons, a student detail pane and guided course/result steps. Keep the existing main.tscn as the battle/research scene. The launch setting switches only after UI and persistence work.
- Presentation data is JSON and can be edited independently; it is not part of native rule fingerprints. The UI locks plan editing after settlement to make the captured result easy to understand, while the old research interface retains its broader editing behavior.

## Risks / Trade-offs

- Small original portraits look pixelated when enlarged → preserve aspect ratio and use nearest filtering, record their exact original source.
- Native rule files are tightly scoped → display April/week-four slice and pending-story status without false advancement.
- Save replay may become large → cap file bytes and command count; refuse changes at capacity rather than silently dropping save history.
- File replacement can fail on Windows → check each operation and restore the previous path after a failed publication.

## Migration Plan

No original-save or prior research-session migration. Change the default scene at final integration; reverting that project setting restores the previous launch. Evidence and historical UI stay in place.
