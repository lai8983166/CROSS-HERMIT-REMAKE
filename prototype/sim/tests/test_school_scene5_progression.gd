extends "res://sim/tests/test_base.gd"

const Progression = preload("res://sim/school_scene5_progression.gd")


func _snapshot() -> Dictionary:
	return {"scene_id": 5, "own_side": 0, "event20_seen": false,
		"enemy2": {"used": true, "side": 0, "state": 1},
		"enemy3": {"used": true, "side": 7, "state": 1},
		"enemy11": {"used": true, "side": 5, "state": 0},
		"own_casualties": 0, "remaining_ticks": 600, "own_playable_unavailable": false}


func test_event20_precedes_all_terminal_conditions_without_mutating_input() -> void:
	var state := _snapshot()
	state.enemy3.side = 0
	state.enemy11.state = 4
	state.remaining_ticks = 0
	state.own_playable_unavailable = true
	var before := state.duplicate(true)
	var result := Progression.choose_terminal(state)
	assert_eq(result.action, "event20")
	assert_eq(result.script_sub, 20)
	assert_eq(result.exit_flag, 0)
	assert_eq(result.event20_bit_write, 1)
	assert_false(result.authorizes_persistent_write)
	assert_eq(state, before)
	state.event20_seen = true
	assert_eq(Progression.choose_terminal(state).selector_arg, 2)


func test_objective_requires_native_removed_state_and_both_owned_records() -> void:
	var state := _snapshot()
	state.event20_seen = true
	state.enemy3.side = 0
	state.enemy11.hp = 0
	for native_state in [0, 1, 2, 3, 5]:
		state.enemy11.state = native_state
		assert_eq(Progression.choose_terminal(state).action, "continue")
	state.enemy11.state = 4
	state.enemy11.hp = 999
	assert_eq(Progression.choose_terminal(state).tactical_result_selector, 1)
	state.own_casualties = 1
	assert_eq(Progression.choose_terminal(state).selector_arg, 5)
	assert_eq(Progression.choose_terminal(state).tactical_result_selector, 2)
	state.enemy2.used = false
	assert_eq(Progression.choose_terminal(state).action, "continue")
	state.enemy2.used = true
	state.enemy2.side = 1
	assert_eq(Progression.choose_terminal(state).action, "continue")


func test_timer_priority_and_distinct_script_and_result_selectors() -> void:
	var state := _snapshot()
	state.remaining_ticks = 0
	state.own_playable_unavailable = true
	var result := Progression.choose_terminal(state)
	assert_eq([result.selector_arg, result.script_sub, result.tactical_result_selector], [11, 11, 4])
	state.event20_seen = true
	result = Progression.choose_terminal(state)
	assert_eq([result.selector_arg, result.script_sub, result.tactical_result_selector], [8, 8, 3])
	state.remaining_ticks = -1
	result = Progression.choose_terminal(state)
	assert_eq([result.selector_arg, result.script_sub, result.tactical_result_selector], [14, 8, 5])
	state.event20_seen = false
	result = Progression.choose_terminal(state)
	assert_eq([result.selector_arg, result.script_sub, result.tactical_result_selector], [14, 14, 5])
	state.own_playable_unavailable = false
	assert_eq(Progression.choose_terminal(state).action, "continue")
	state.remaining_ticks = -2147483648
	assert_true(Progression.choose_terminal(state).supported)


func test_missing_or_invalid_inputs_never_default_to_success() -> void:
	for key in _snapshot():
		var state := _snapshot()
		state.erase(key)
		assert_false(Progression.choose_terminal(state).supported, "missing " + key)
	for pair in [["scene_id", 4], ["own_side", 4], ["remaining_ticks", 2147483648],
			["own_casualties", -1], ["event20_seen", 1], ["own_playable_unavailable", 0]]:
		var state := _snapshot()
		state[pair[0]] = pair[1]
		assert_false(Progression.choose_terminal(state).supported)
	var state := _snapshot()
	state.enemy11.used = false
	assert_false(Progression.choose_terminal(state).supported)
	state = _snapshot()
	state.enemy3.state = 1.0
	assert_false(Progression.choose_terminal(state).supported)


func test_capture_descending_ties_owner_protection_and_signed_byte_counts() -> void:
	var counts: Array = []
	counts.resize(16)
	counts.fill(0)
	assert_eq(Progression.capture_candidate(7, counts), -1)
	counts[2] = 3
	counts[5] = 3
	assert_eq(Progression.capture_candidate(7, counts), 5)
	assert_eq(Progression.capture_candidate(2, counts), -1)
	counts[5] = 4
	assert_eq(Progression.capture_candidate(2, counts), 5)
	counts[15] = 128
	assert_eq(Progression.capture_candidate(7, counts), 5)
	counts[7] = 1
	assert_eq(Progression.capture_candidate(7, counts), -2)
	counts[7] = 0
	counts[0] = 1.0
	assert_eq(Progression.capture_candidate(7, counts), -2)
	assert_eq(Progression.capture_candidate(16, []), -2)


func test_activation_request_order_and_copy_isolation() -> void:
	var requests := Progression.activation_requests()
	assert_eq(requests.size(), 6)
	var centers := [Vector2i(3, 58), Vector2i(4, 90), Vector2i(42, 48), Vector2i(52, 39), Vector2i(28, 41)]
	for index in range(5):
		assert_eq(requests[index].kind, "group")
		assert_eq(requests[index].group, index + 2)
		assert_eq(requests[index].center, centers[index])
		assert_eq(requests[index].radius, 3)
	assert_eq(requests[5].kind, "unit")
	assert_eq(requests[5].enemy_number, 11)
	assert_eq(requests[5].work_index, 239)
	assert_eq(requests[5].center, Vector2i(16, 40))
	assert_eq(requests[5].radius, 10)
	requests[0].group = 99
	assert_eq(Progression.activation_requests()[0].group, 2)


func test_capture_counter_constants_are_not_elapsed_seconds() -> void:
	assert_eq(Progression.capture_hold_limit(0), 900)
	assert_eq(Progression.capture_hold_limit(3), 900)
	assert_eq(Progression.capture_hold_limit(4), 600)
	assert_eq(Progression.capture_hold_limit(7), 600)
	assert_eq(Progression.capture_hold_limit(16), -1)
	assert_eq(Progression.capture_transition_ticks(387), 72)
	assert_eq(Progression.capture_transition_ticks(393), 37)
	assert_eq(Progression.capture_transition_ticks(399), 72)
	assert_eq(Progression.capture_transition_ticks(405), 62)
	assert_eq(Progression.capture_transition_ticks(406), 62)
	assert_eq(Progression.capture_transition_ticks(452), -1)
