# Proposal

## Why

The retained portrait loader stops at its original allocator, whose snapshot contains unmapped debug-heap chain nodes and expired OS resources. R3 needs exact dependency evidence and verified original allocation/read/free semantics without manufacturing missing retained objects or requiring an interactive desktop.

## What Changes

- Trace all six accepted retained allocation boundaries to the first unexecuted critical-section API, preserving full source state and identifying missing chain nodes precisely.
- Exercise original x86 allocation, debug headers/list/accounting, read-only file loader and free functions in separate controlled-input fixtures with explicitly empty debug ledgers, fresh owned native Windows heap/critical section and actual file APIs.
- Check two simultaneous allocations/unlinks plus full SC004 read/free, source counters, guards, complete memory/CPU, OS ownership and normal helper cleanup through independent replay and corruption tests.
- Keep retained state untouched by the separate fixture declarations; record that the missing retained CRT context remains unresolved. Preserve old evidence/saves, validate and archive this finite research unit.

## Capabilities

### New Capabilities

None. Research tooling under existing reverse-engineering/completion requirements; skip_specs is explicit.

### Modified Capabilities

None. No requirements, target date or milestone scope changes.

## Impact

New source contracts, owned headless Win32 helper, tools/tests/docs and immutable evidence. No game window, input or GPU. Independent empty-ledger fixtures are controlled test inputs, not a reconstruction of the old process or a bypass for its missing nodes. Game/CRT functions execute original code; only native OS APIs are marshalled. R3/R6 and the retained allocator/read/upload connection remain incomplete unless separately proven later. Godot unchanged.
