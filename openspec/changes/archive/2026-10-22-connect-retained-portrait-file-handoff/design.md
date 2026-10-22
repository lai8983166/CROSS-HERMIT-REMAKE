# Design

## Context

See proposal.md. The accepted name-raster report contains six source continuations at 403BD0 with all original frames and a real 88x24 bitmap. Its native GDI resources have ended. Historical native name-texture evidence has identical raster bytes and exact successful CreateTexture/descriptor/lock/unlock replies.

## Goals / Non-Goals

Connect original name conversion, source cleanup, path construction and read-only image-file open/size to the first unexecuted original allocation request. Independently classify all 21 referenced image containers and pixels. Do not claim new native GPU work, live old handles, source heap allocation, image loading completion or complete R3.

## Decisions

- Pin latest acceptance and obtain full state by read-only observation of its unmodified independent verifier, then continue the CPU/stack without new roots.
- Project the actual observed historical texture/interface replies into fresh typed guest addresses. Retain the inherited device/vtable and IAT; only new platform-response objects/method-boundary pages and lock mirror are mapped. Never execute method-boundary stubs. Validate source arguments and original COM dispatch against recorded metadata.
- Replay historical successful GDI cleanup under the exact original caller and source-owned object roles, with explicit current logical handle rebasing. No expired handle reaches Windows.
- Execute original formatter/concat/accessors from pinned image, not game-function stubs. At natural image loader use actual Win32 read-only source-file open and size. Stop before original 428A40 allocator; close the outstanding file explicitly as probe cleanup, not as original loader success.
- Independently replay instructions, all guest writes/platform outputs, all memory/CPU, natural stack, converted pixels and resource accounting. Validate all 21 files with independent byte readers and per-row/pixel statistics, preserving private-copy identities. Corpus parsing does not establish VM reachability.

## Risks / Trade-offs

- Historical platform replay -> explicit offline-only label and immutable reply pins; no fresh GPU acceptance.
- Pointer/handle rebasing -> typed projection ledger and exact source-call/role checks, never edit existing derived fields to manufacture readiness.
- Next source heap depends on valid CRT lifetime -> preserve exact allocation request as planned boundary, no substitute allocator return.
- File left open at that boundary -> actual owned probe cleanup and invalid-handle recheck; source ReadFile/CloseHandle remain unexecuted.
