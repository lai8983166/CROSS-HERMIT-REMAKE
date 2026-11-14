extends "res://sim/tests/test_base.gd"

const Consumer := preload("res://sim/tactics_result_consumer.gd")
const Transition := preload("res://sim/tactics_result_transition.gd")


func test_zero_is_read_only_after_resume_and_stale_resume_is_rejected() -> void:
	var flow := Consumer.new()
	var started := flow.begin_iteration(0)
	assert_false(started["result_consumed"], "453CB0 precedes 453CB5 even for zero")
	assert_eq(started["action"], "wait", "zero still yields before the next loop")
	var resumed := flow.resume_wait(1, 1, 0)
	assert_eq(resumed["action"], "continue_loop", "zero takes 453CE4 -> 4539CD")
	assert_true(resumed["result_consumed"], "completion is consumed on resume")
	assert_false(resumed["function_returned"], "zero does not exit the scene loop")
	flow.begin_iteration(1)
	var before := flow.snapshot()
	assert_false(flow.resume_wait(1, 1, 0)["supported"], "old iteration cannot wake a new wait")
	assert_eq(flow.snapshot(), before, "stale resume does not mutate state")


func test_nonzero_preserves_order_without_interpreting_victory_or_rewards() -> void:
	for completion in [1, 2, 5, -1]:
		var flow := Consumer.new()
		flow.begin_iteration(completion)
		var first := flow.resume_wait(1, 1, 0)
		assert_eq(first["action"], "call_replay_record", "all nonzero values follow the same CMP branch")
		assert_false(first["function_returned"], "first resume is not loop completion")
		assert_false(flow.resume_wait(1, 2, 0)["supported"], "record call must return before wait 2")
		assert_eq(flow.replay_record_returned(1, 0)["wait_ordinal"], 2, "disabled recording return 0 is allowed")
		assert_false(flow.replay_record_returned(1, 0)["supported"], "record callback cannot be consumed twice")
		assert_eq(flow.resume_wait(1, 2, 0)["wait_ordinal"], 3, "two additional distinct waits")
		var final := flow.resume_wait(1, 3, 0)
		assert_eq(final["scene_function_return"], 1, "453CDD returns fixed 1, not outcome selector")
		assert_eq(final["completion_value"], completion & 0xffffffff, "original completion bits preserved")
		assert_false(final.has("winner"), "completion does not invent outcome")
		assert_false(final["authorizes_persistent_write"], "no reward or save authority")
		assert_false(final["native_wait_verified"], "semantic test is not native proof")
		assert_false(flow.resume_wait(1, 3, 0)["supported"], "duplicate final resume cannot repeat exit")


func test_wait_failure_timeout_and_out_of_order_calls_preserve_state() -> void:
	var flow := Consumer.new()
	flow.begin_iteration(1)
	var before := flow.snapshot()
	for status in [0x102, 0xffffffff, 0x80]:
		assert_false(flow.resume_wait(1, 1, status)["supported"], "only successful event wait can resume")
		assert_eq(flow.snapshot(), before, "failure is not a fabricated return")
	assert_false(flow.resume_wait(1, 3, 0)["supported"], "cannot skip waits")
	assert_false(flow.begin_iteration(0)["supported"], "cannot overwrite retained completion")
	assert_false(flow.replay_record_returned(1, 1)["supported"], "record cannot precede first consumption")
	assert_eq(flow.snapshot(), before, "all refusals leave the pending frame intact")
	before["completion_value"] = 0
	assert_eq(flow.snapshot()["completion_value"], 1, "snapshot does not alias the retained frame")


func test_record_return_does_not_replace_retained_completion() -> void:
	for record_return in [0, 1, 123, -1]:
		var flow := Consumer.new()
		flow.begin_iteration(1)
		flow.resume_wait(1, 1, 0)
		flow.replay_record_returned(1, record_return)
		flow.resume_wait(1, 2, 0)
		assert_eq(flow.resume_wait(1, 3, 0)["scene_function_return"], 1, "record EAX is ignored by the caller")


func test_existing_scene5_dispatch_requires_all_three_resumes() -> void:
	var fixture: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(
		"res://data/scene5_task_execution_evidence.json"))
	for example in fixture["cases"]:
		if not example["state11_dispatched_in_emulation"]: continue
		var flow := Consumer.new()
		flow.begin_iteration(int(example["exit_frame"]["transition_function_return"]))
		assert_false(Transition.after_waits(example["exit_frame"], example["dispatch_context"], flow)["supported"], "no early dispatch")
		flow.resume_wait(1, 1, 0)
		flow.replay_record_returned(1, 0)
		flow.resume_wait(1, 2, 0)
		assert_false(Transition.after_waits(example["exit_frame"], example["dispatch_context"], flow)["supported"], "third wait cannot be skipped")
		flow.resume_wait(1, 3, 0)
		var actual := Transition.after_waits(example["exit_frame"], example["dispatch_context"], flow)
		assert_true(actual["supported"], "existing scene-5 subset remains supported")
		assert_eq(actual["requested_state"], int(example["dispatch_events"][0]["state"]), "matches existing original-code isolated fixture")
		assert_false(actual["authorizes_persistent_write"], "dispatch remains separate from rewards")
		assert_true(actual["projection_only"], "given isolated context predicts a request only")
		assert_false(actual["outer_callback_teardown_executed"], "outer tail waits and cleanup remain unexecuted")
		var unsupported: Dictionary = example["dispatch_context"].duplicate(true)
		unsupported["scene_id"] = 45
		assert_false(Transition.after_waits(example["exit_frame"], unsupported, flow)["supported"], "unknown scene routing stays unresolved")
