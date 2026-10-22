# Design

## Context

See proposal.md. Accepted CRT lifecycle evidence is pinned by school-retained-crt-acceptance-v1-20261022.json (4433b1e2299794fa9e11a45003f12838d5cddb97694050f073beb478e688efed). The packed PE has zero raw sizes for original text/data sections, so its initial zero mapping alone does not prove post-unpack CRT defaults.

## Goals / Non-Goals

Observe original post-unpack/pre-CRT data and pre-WinMain initialized allocation graphs in two independent rounds of fresh owned probes (one process tree per target boundary). Use observed cold fields for an explicitly separate source initialization/lifecycle fixture. Do not graft fixture inputs into retained VM state, claim original game normal shutdown from probe termination, or claim full R3/R6/Godot completion.

## Decisions

- The protection parent owns its child debug port and clears debug registers during unpacking. Observe the parent NtWaitForDebugEvent return / NtDebugContinue entry with parent hardware breakpoints; arm an unused child debug slot only once original CRT bytes appear and prior protected debug slots are clear. Capture each desired child breakpoint before the original parent handles it, then terminate that independent probe. No parent debugger reply is rewritten. Native debugger owns each fresh job/process tree and private non-switched desktop. Use execution hardware breakpoints at5713C0 and49DD70, only debug-register context edits; preserve full context before/after instrumentation and source bytes. No WriteProcessMemory, source INT3 patch, general register rewrite or game-return substitute.
- Record bounded debug events, real process image/ABI, full original data section and relevant code/stack. At CRT and WinMain entries collect ledger, native lock/heap state, every linked allocation header/payload, source guards and ownership. Stop before first WinMain instruction and explicitly terminate/reap the probe job; report this separately from original cleanup.
- Independently parse full captured states, verify original bytes/control-boundary/counters/list guards and derive cold input provenance. Original source heap57B9D0, lock576F60 and teardown routines then execute with actual owned headless OS calls, followed by original allocation/file/free; cold source fields replace previous hand-declared empty-ledger values only in a new separate fixture.
- Frozen tools/reports remain unchanged. New crt-init prefixes, mutation/ownership rejection tests, raw/index/HEAD identities, complete historical preservation, strict specs and exact archive mapping.

## Risks / Trade-offs

- Protection/debug behavior may prevent early observations: retain failed raw evidence and diagnose actual exception/source boundaries; never invent cold values or silently bypass protection.
- Native pointers are process-local: inventory while the source process is stopped/live, never pass captured expired tokens to a helper.
- Private desktop is hidden and never switched; no unlock/input required. Probe termination intentionally does not execute game cleanup and cannot satisfy same-lifetime retained integration.
- Bounded source fixture demonstrates observed initialization semantics; native whole-process instruction tracing remains distinct.
