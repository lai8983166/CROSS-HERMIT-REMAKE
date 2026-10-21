# Tasks

## 1. Source scheduler graph and owned-call contract

- [x] 1.1 Verify the original manager/node/worker/callback/cleanup source and pinned empty retained scheduler graph, implement a bounded owned-process source-call contract with source/ABI/ownership refusal tests and documentation, then commit locally.

## 2. Real native scheduler lifetime

- [ ] 2.1 Execute original construct/register/dispatch/worker completion/unlink/destruct paths in an owned initialized original runtime, cover dirty/zero, same/different buckets and disabled-then-enabled nodes, independently verify full buffer/source/IAT/stack and actual thread/event cleanup observations; include tests/docs and commit the functional result.

## 3. Integration and roadmap handoff

- [ ] 3.1 Reproduce native cases and normal original-process teardown, pass affected regressions/strict specs and frozen R1/R2/task-frame/save/checkpoint preservation, update the master spec with the completed scheduler-lifetime prerequisite and remaining retained scene/input/world integration, then locally commit acceptance and archive this completed change without marking R3 complete.
