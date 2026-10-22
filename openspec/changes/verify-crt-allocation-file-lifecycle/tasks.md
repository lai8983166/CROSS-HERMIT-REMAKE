# Tasks

## 1. Retained source allocator dependency proof

- [x] 1.1 Pin original allocator/CRT/OS contracts and all six accepted allocation boundaries; trace unchanged retained state to unexecuted lock entry, independently verify whole memory/CPU and missing debug-chain dependencies; add source/provenance corruption tests and documentation, then validate immutable reports.

## 2. Original allocation, file read and free lifecycle

- [x] 2.1 Implement a bounded owned headless Win32 heap/file helper and explicitly separate fresh-input fixtures; run original x86 allocation/debug headers/list/accounting, concurrent unlink/free and complete source file-loader/read/free, independently replay full instructions/writes/memory/CPU and actual API ownership/cleanup; add corruption/ownership tests and docs, and run affected regressions.

## 3. Acceptance and archive

- [ ] 3.1 Run strict specs and full previous evidence/save/checkpoint/resource preservation; update master progress with the unresolved retained CRT gap, commit locally, and archive this completed finite change with exact raw/index/HEAD and archive hashes.
