## Context

See proposal.md for motivation. The playground owns a validated command log for a declared 4/4 example; the source school session intentionally ends at course results. Existing native audits stop before Chapter016. Existing week projection already implements source calendar, job unlocks, equipment and skill cleanup.

## Goals / Non-Goals

Continue the same course state through the two original scenes and one verified week handoff. Preserve the old source session contract and all historical evidence. Full Chapter018 onward, fifth-week school initialization, audio fidelity and original UI timing remain outside this bounded continuation.

## Decisions

- Extend the course native emulator in a separate tool, consuming the actual state7 request after Chapter017 END. Reuse finite source instruction/write guards and the existing week projection. Do not substitute an earlier synthetic week snapshot.
- Export text from the matching Chinese resource and visual references from board/background commands. Track text speaker by board slot and TEXTACTIVE; text-pool parameters are not speaker IDs. Reject unknown control changes rather than interpreting a full VM.
- Own story cursor and next-week result in the playground controller, leaving the frozen 4/4 session APIs intact. Assemble week inputs from current growth/confirmation plus native initial equipment/flags; compare a reference run with native after-week data.
- Version2 saves retain exact rule/asset fingerprints, validate replay and state hash. Version1 saves are accepted only under their original four fingerprints and original state hash, then migrate on the next save.
- Display dialogue in an overlay with original imagery and explicit click navigation. Previous navigation re-reads text without replaying side effects. Skip requires an in-game confirmation. A completed story unlocks a once-only next-week transition, and arrival accurately identifies the remaining school setup boundary.

## Risks / Trade-offs

- Chinese source strings can contain Japanese fullwidth-space bytes → handle that documented byte sequence before strict decoding and retain raw source hashes.
- Native presentation and scheduler construction are stubbed → declare those boundaries in evidence and docs; never label the run a live witness.
- Save schema changes could discard earlier progress → test fixed legacy payloads, staged saves, malformed commands, partial story, completed story and week arrival.
- Dialogue length or controls may overflow → render and inspect both scenes, transition and restored views at 1024×768.

## Migration Plan

Keep the default entry and save path. Read valid version1 commands atomically, preserve old backup behavior, write version2 on subsequent save. Local Git commits isolate source evidence, exported presentation, controller, reader, arrival/navigation and final acceptance.
