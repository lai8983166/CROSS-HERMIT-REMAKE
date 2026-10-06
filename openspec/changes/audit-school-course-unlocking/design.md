# Design

## Context

See proposal.md. 4A2BA0 scans100 source96-byte templates; 4A24A0 inserts into20 teacher buffers of100 records,10 bytes each. Current movement modules cover teachers117/118 with declared course flags. Current returned campaign roster has zero teachers.

## Goals / Non-Goals

**Goals:** Execute both unlock functions independently with finite write guards, export source rules and compare a pure module at each checkpoint.

**Non-Goals:** Full new-game initialization, chronological Chapter012 execution, teacher registration migration, course selection/execution, current UI or original save writes.

## Decisions

- Add a dedicated ExitEmulator subclass allowing only the two native functions and debug check. Avoid reusing drag initialization that would conflate roster presence with course availability.
- Snapshot global101 flags,20 signed counts and sparse nonzero physical records with all10 bytes. Absent slots default zero. Native write guard allows flags1..100, counts, and only record offsets0..7; offsets8/9 are immutable physical data.
- Export all100 templates including category-zero hole32 and valid empty masks. Pin their ordered numeric encoding with SHA-256; do not derive rules from expected cases.
- Use date month0..255/week0..5, a bounded subset that preserves native signed stamp arithmetic without overflow. Model flags as bytes (any nonzero means already unlocked) and record fields as byte/signed-short data.
- Preflight all teacher counts before mutation; native capacity overflow is unsafe and is not executed. The model returns a refusal rather than reproducing out-of-buffer writes.
- Teacher101 initialization is verified at original call bytes; existing Chapter012117 evidence remains a prefix. Neither constitutes a full initialized campaign or permits rewriting the zero-teacher frozen return.

## Risks / Trade-offs

- [Opaque bytes are not shifted with logical records] → Compare every sparse physical record including distinctive sentinel bytes and inactive destination tails.
- [Global unlock can occur for absent teachers and empty masks] → Include zero-roster and empty-mask cases; preserve ownership metadata unchanged.
- [Runtime activation could imply unsupported teacher provenance] → Keep module standalone and report source initialization and current replay as different evidence boundaries.
