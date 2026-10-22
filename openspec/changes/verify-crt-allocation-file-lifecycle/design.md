# Design

## Context

See proposal.md. The pinned source snapshot has CRT flag1, heap mode1, lock9 at80A4B0, heap token04D60000 and missing debug first/last nodes04D605B8/04D68FA0. Original 428A40 calls56E810/56E860/577040 before allocation. The existing retained state cannot be repaired merely by replacing a heap handle.

## Goals / Non-Goals

Prove the baseline gap for six retained branches and original allocator/file/free behavior under explicit separate fixture inputs. No claim of restoring retained debug-chain history, native full-process startup, same-lifetime game integration, GPU/image upload or R3 completion.

## Decisions

- Pin the previous acceptance; observe its unchanged verifier to reconstruct full retained boundaries. Stop before EnterCriticalSection, with no actual OS calls or rewritten object state in those branches.
- Separate fresh fixtures start from original code/data plus a declared empty debug ledger (head/tail and byte counters zero, request counter1), fresh owned OS critical-section bytes and explicit source heap-token translation. These are independent function-test inputs, never inserted into retained memory/checkpoints. Keep debug tracking enabled and source heap mode1; document other CRT modes as untested.
- Use an x86 headless C# helper owning HeapCreate/InitializeCriticalSection resources, typed pointer translation and bounded actual HeapAlloc/Validate/Free and file APIs. Commit source-written guest allocation bytes into corresponding native owned buffers before native consumers; read back actual output and validate all ownership/bounds. Original CRT functions are never stubbed.
- Exercise source allocation of262168/88 concurrently, unlink/free both, and the complete original42AE20 read-only SC004 loader/free. Normal helper shutdown releases outstanding owned objects/files and destroys the heap; forced termination is failure evidence.
- Independent replay checks source instruction/write hashes, full CPU/maps, original debug headers/FD guards/CD fill, linked-list transitions/counters, actual file bytes and cleanup. Preserve the retained baseline restriction in all acceptance output.

## Risks / Trade-offs

- Snapshot pointers cannot be native handles -> strict domain translation and explicit fixture declarations, no expired native pointers.
- Function fixtures resemble reconstructed state -> report isolated test inputs and unresolved retained gap prominently; never use fixture success as R3 integration acceptance.
- Header corruption or ownership mismatch -> fail before native API, preserve diagnostics, do not disable debug tracking.
- Helper errors -> finally cleanup owned resources and retain nonzero/forced exits as failures.
