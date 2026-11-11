# Independent review: context-filtered owned WOW64 wait

The retained v9 observation supports the narrow CPU0 exported endpoint and same-run instruction effects, with CPU0/CPU1 CR2 continuity. The executed v2 offline verifier has validation gaps that must be closed in a new version before claiming the strengthened evidence contract is complete. No additional native capture is indicated by these findings: the existing authenticated observation contains the missing checks' inputs.

Reviewed the actual backend, sparse build and dependency audit, observer, verifier v2 and its complete-schema/instruction/CR2 dependencies, plus the completed native observation, fixture result and VM exit report. This is independent review of the main agent's observer/verifier and native evidence; the reviewer implemented the context backend, so backend self-review is not presented as independent backend acceptance.

Evidence identity:

- Observation: .venv-audit/native-worker/tcg-wait-native-v9/observation.json, 840355 bytes, SHA-256 326e61eb38927e835ae2c0af4892233cd88bb67e2093da217176a59ea570818c.
- Plan SHA-256: 32bf3272cfa3c64157ecd7ad6c39178353dcd56432b4ce19365d662060d7d308.
- Runtime SHA-256: ea3fef746e5fa1cbc497b51836f4e4041bad1f1af25ca25248672b8a9e573ad5.
- Reproduction: devtools/terminal_tcg_context_review_mutations_v1.py. Mutation record: analysis/terminal-wait-tcg-context-review-mutations-v1-20261111.json.

The observation has 12 ordered points and 10 steps, all actual step stop replies identifying CPU0. Observer errors are empty and elapsed time is 24.33356956 seconds. The CR2 window lasts 1.248744398 seconds and contains 17 chained events. Context filter output ends disabled and unpoisoned, with 6 accepted and 88 rejected match attempts. These are diagnostic checks, not retired-instruction counts or a count of unique foreign threads.

Strict raw64 schemas and exact state comparisons cover six PXOR effects, the R9 load and interrupt-shadow clearing, MOV SS predecessor, SYSCALL-linked return fields, and RET12 consumption. Every named point records matching current TEB PID/TID, CR3 and R13; the ledger checks both CPUs' full exported start/end states and CR2 writer chains. This is useful same-wait evidence, without claiming uninterrupted execution of every intervening instruction or whole-machine replay.

Completed fixture results report returns [0,0,0,258], no fixture/cleanup errors, both counter workers entered, workers stopped, handles closed, buffers released, affinities restored, watchdog disarmed and fixture process exit. The VM report confirms process exit, no errors and unchanged parent size/mtime. A nonzero timeout argument and successful first return do not independently prove the first wait actually spent time blocked. These are owned test-fixture calls, not original game calls.

Independent mutations confirm rejection of an altered return RAX, point TEB owner, PXOR opcode, duplicate point, CR2 digest and filter poison. The v2 verifier incorrectly accepts the following altered evidence:

- SYSCALL or RET12 stop reply changed to CPU1.
- Removed selector13 point or reversed point chronology.
- Corrupted kernel-entry signature.
- Negative filter rejection count or empty active filter address set.

Recommended new verifier version: require the exact ordered point and step sets; require every step reply to identify CPU0; bind the CALL PC/opcode, selector13 PC/saved return and kernel-entry signature to the authenticated plan and kernel file; validate filter schema, integer counters, budgets, monotonicity, active lifetime and exact expected configured address sets. Re-run both the existing mutations and the newly demonstrated misses on the same original observation. Do not edit the executed v2 verifier, normalize CPU/checkpoint fields, or reinterpret a consistent JSON digest as provenance authentication.

Formal status remains 2/8. This review does not approve general Windows admission, original-game wait integration, complete RAM/device replay, two fresh original-game lifetimes or final resource/ABI acceptance. No native process was started, no host input was sent, no existing evidence was changed, and no files were staged or committed during this review.

Post-review correction: the main agent requested implementation of a new v3 wrapper. It checks the recommended contracts against the unchanged capsule and pinned local kernel. The original observation passes 63 new wrapper checks plus frozen v2 checks; all 26 explicit evidence mutations reject, as does untrusted plan-path replacement. See analysis/terminal-wait-tcg-context-proof-v3-20261111.json and devtools/tests/test_terminal_tcg_context_wait.py. Parent independent review of this new wrapper remains required; this reviewer cannot independently accept their own correction.

Original-game integration remains blocked on platform qualification: native_input_isolation.validate_machine and isolated_vm_preflight.verify require VMware-specific evidence. The current TCG guest has no equivalent same-boot console/input/D3D8 qualification. No game launch was performed or justified by the owned wait proof.

Independent saved-consumer review: reviewed main-owned devtools/terminal_tcg_context_consume_v1.py and its imported PUSHFD/PUSHAD/FXSAVE32 comparison functions against the exact capsule result. All 15 checks pass (the actual report contains 15, not 16). PUSHAD saved ESP correctly reflects the preceding PUSHFD push; clearing VM/RF is confined to the architectural PUSHFD image, without changing the raw endpoint. FXSAVE32 comparisons map logical ST through TOP and compare XMM0..7 and defined scalar fields, excluding reserved bytes and MXCSR_MASK as stated. Patched 214-byte helper bytes and source identities, same ready record, record count, prior empty first-record region and cleanup receipts are checked.

Five independent mutations all reject: saved EAX, saved flags, saved XMM0, result TID and handles_closed=false. Two unittest methods pass in the new frozen devtools/tests/test_terminal_tcg_context_consume_review_v1.py; detailed results are in analysis/terminal-wait-tcg-context-consumption-review-v1-20261111.json. No blocking defect was found for this narrow composition with the separately verified v3 endpoint trace. The saved-record consumer alone does not validate the observer's complete trace contract, and its result must not replace that prerequisite. Only the first owned helper result record is connected to observed CPU state; the remaining three returns remain fixture receipts. This does not establish original-game consumption, platform qualification, full replay or formal milestone advancement.
