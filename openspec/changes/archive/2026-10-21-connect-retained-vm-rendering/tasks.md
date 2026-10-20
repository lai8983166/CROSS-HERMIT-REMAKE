# Tasks

## 1. Initialized retained-scene reconstruction

- [x] 1.1 Reuse original startup with declared fresh inputs and checkpoint-compatible ownership, reconstruct retained scene logic with valid renderer resources in one lifetime, verify original initialization writes plus complete CPU/stack/logical-state retention, and include tests/documentation before a local commit.

## 2. Original VM drawing and real output

- [x] 2.1 Continue original retained rectangle and text paths through queues and real device drawing, inspect source-derived commands/vertices and nonblank output, verify required error/resource lifetime paths, and land evidence/tests/documentation with the functional local commit.

## 3. Integrated R2 acceptance

- [x] 3.1 Reproduce integrated rendering across representative retained cases, run affected regressions/strict specs/historical-save-checkpoint preservation, record R3 handoff, and only after all R2 criteria pass update the master spec, commit acceptance and archive this completed change locally.
