# Design

## Context

Accepted portrait evidence pins six logical continuations at the first CreateFontA instruction with all five original frames intact. All historical native resources have expired. See proposal.md for motivation and the master completion spec for R3/R6 requirements.

## Goals / Non-Goals

Goals: a reproducible offscreen resource reconstruction, complete source execution through the name raster, independent replay and corpus font evidence. Non-goals: live GPU, same original process lifetime, image loading, Godot or full milestone acceptance.

## Decisions

- Pin the preceding acceptance/report and obtain full memory/CPU via read-only observation of its unmodified verifier. Continue the current CPU/stack; introduce no new game root, guest code/IAT binding or derived-state write.
- Retain the logical historical measurement DC returned by original 414440; translate this single token only at GDI API calls to a newly owned CreateCompatibleDC(NULL). Never pass the historical token to Windows. This deliberately reconstructs measurement context and is reported as such. Font, raster DC, stock selections and DIB are fresh process-owned objects.
- Map a fresh bounded guest raster allocation only when actual CreateDIBSection supplies its native bits. Record all platform args, outputs and cleanup. Execute original CRT, string formatting and accessors from pinned code; any unsupported platform request fails closed.
- Replay API records in an independent verifier without new OS calls. Check API order, caller/arguments, memory outputs, source instruction/writes, full CPU/maps, raster geometry and nonempty glyph pixels. Do not use recorded guest-function results.
- Separately exercise every catalogued raw Big5 name through actual offscreen GDI using the original font arguments. Record ACP and actual selected face; do not silently convert ANSI source text to Unicode or claim garbling fixed.

## Risks / Trade-offs

- Historical DC state differs from a fresh memory DC -> explicit reconstruction boundary, no same-lifetime claim, fixed source-selected font and owned state checks.
- ANSI decoding uses host ACP -> record exact raw bytes/ACP/face and leave encoding issue open.
- Expensive parent reconstruction -> cache bounded snapshots within a process; independently validate every retained branch and protect all immutable evidence.
- Cleanup or platform failure -> finally release all owned objects and preserve fresh diagnostic outputs; never fall back to input/window/GPU.
