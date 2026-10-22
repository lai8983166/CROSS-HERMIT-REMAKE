# Proposal

## Why

The retained CRT debug heap points at missing historical blocks. The previous accepted original allocation/file/free fixture uses explicit empty-ledger inputs, which do not establish how the original executable initializes that ledger. Obtain actual pre-CRT and pre-WinMain provenance without depending on the active input desktop.

## What Changes

- Capture an owned original process tree at hardware execution breakpoints before original CRT startup and before WinMain, on a private unshown desktop; preserve complete relevant source/data/stack and CRT allocation graph.
- Independently verify original initialization inputs, source identity, native heap/debug list ownership and request/accounting invariants. Execute original heap/lock initialization and allocation/file/free using observed cold inputs in an explicitly separate owned headless fixture.
- Freeze prior evidence/saves/checkpoints, run related regressions and strict specs, record the remaining retained integration gap in the master roadmap, commit coherent units and archive this finite research change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. Existing reverse-engineering/completion provenance requirements apply; skip_specs is explicit because this adds research evidence and tooling, not product behavior.

## Impact

New bounded x86 debugger/Win32 helper and Python source replay/verifiers/tests/documentation. The installed executable and saves remain read-only. Hardware debug registers are instrumentation; no source code, general register return, game input or derived CRT ledger is patched. Probe termination is explicit and never counted as normal original game cleanup. No active desktop switch or OS input. R3/R6 and Godot remain incomplete unless their separate integration requirements are actually met.
