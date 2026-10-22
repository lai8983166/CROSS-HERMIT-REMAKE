# Tasks

## 1. Original pre-CRT and pre-WinMain capture

- [x] 1.1 Implement bounded job-owned native hardware-breakpoint capture on a private unshown desktop; preserve two independent original pre-CRT/pre-WinMain source/data/CPU/stack and complete CRT debug allocation graph, independently verify boundaries/ownership/list/guards/accounting and instrumentation scope; add corruption tests/documentation and validate immutable evidence.

## 2. Source-derived CRT initialization and function lifecycle

- [x] 2.1 Use verified observed cold fields in a separate fixture and execute original heap/lock initialization, original allocation/file/free lifecycle and source CRT teardown through owned headless OS interfaces; independently replay all instructions/writes/full CPU/memory/native replies, reject provenance/ownership corruption, document scope and run affected regressions.

## 3. Acceptance and archive

- [x] 3.1 Run full related regressions, strict specs and prior evidence/save/checkpoint/resource preservation; update the master roadmap with exact provenance and remaining retained integration gap, commit coherent units locally and archive this completed change with exact raw/index/HEAD and archive hashes.
