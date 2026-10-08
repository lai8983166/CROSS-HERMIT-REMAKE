# Design

## Context

The default playground owns a frozen 4/4 school session plus a separate once-only 4/5 week projection. Version2 saves replay six resource fingerprints. Native continuation stops with CH001 loaded and next8 stored. Chapter018's slots5/6 use MC body atlases while slots7/8/9 use SC portraits; CHARSET replaces the resource identity in the active slot.

## Goals / Non-Goals

Preserve the existing school and arrival state while adding a bounded fifth-week story and state8 entry. Do not relabel a fourth-week school snapshot as an initialized fifth-week school. Movie readiness and presentation APIs remain declared boundaries; chronological campaign simulation and workroom/school task bodies are not part of this slice.

## Decisions

- Extend the existing course/story/week emulator in shared memory. Consume the actual pending6 after state7 through an explicit scheduler boundary, execute native date dispatch and Chapter018 END, and record ready/key/UI/fade-wait outcomes. Use finite additional write guards and source hashes; keep previous reports immutable.
- Keep a separate asset catalog. Parse only Chapter018's known linear presentation instructions, honor background, slot visibility and CHARSET replacements; export both MC and SC resources using their source draw tables. Record the movie source without claiming playback fidelity. A generic all-chapter interpreter would exceed verified scope.
- Add a separate fifth cursor and completion projection to the controller. Fifth completion consumes the 4/5 handoff and applies only audited source writes, then exposes workroom entry. Do not rerun week/course/MVP settlement. Readers receive configurable art root, calendar and command prefix; large body art and up to three small portraits retain distinct layouts.
- Save as version3 with separate new fingerprints. Replay version1/2 against their original resource subsets and their original state hash shapes before publishing migrated state. Capture immutable version2 partial-story and arrival fixtures before changing the controller.

## Risks / Trade-offs

- Resource index is not always the visible speaker's old identity: bind speakers to the current slot resource, including replacements, and assert source text coverage.
- SC portrait geometry differs from MC: use native resource tables, render inspection and separate layout.
- Keyboard focus and overlay navigation can duplicate commands: route story keys once in the parent, retain skip confirmation, and verify cancel and save/load through actual UI events.
- Native completion could silently use a presentation stub for an effectful opcode: verify visited source functions, expected writes and blocked cases; do not trust END alone.

## Migration Plan

Existing source data and version1/2 saves stay readable. New saves use version3; invalid migration leaves memory and files unchanged. Each verified stage is committed locally with no push; final acceptance includes all model suites and relevant sequential UI windows.

Post-commit fingerprint verification found the old Windows Chapter016/017 catalog working copy still used CRLF although the Git blob was LF. Stabilize that exporter at explicit LF and migrate only the corresponding exact known CRLF fingerprint for version2/3 saves when the current catalog matches the verified LF digest. This does not accept arbitrary changed catalogs; keep the frozen old save fixtures unchanged and test both known fingerprints plus tamper rejection.
