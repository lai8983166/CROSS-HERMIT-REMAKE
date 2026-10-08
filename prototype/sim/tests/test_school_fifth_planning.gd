extends "res://sim/tests/test_base.gd"
const Playground := preload("res://sim/school_playground.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")


func _json(path: String) -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(path)))


func _exit():
	var model := Playground.new()
	assert_true(model.restore(_json("res://data/school_playground_legacy_v3.json")["cases"][1]["save"])["supported"])
	return model


func _enter(model):
	for op in ["workroom_open","work_start","work_skip","school_enter"]:
		assert_true(model.execute({"op":op})["supported"],op)
	return model


func _round_trip(model):
	var fresh := Playground.new()
	assert_true(fresh.restore_text(JSON.stringify(model.export_save()))["supported"])
	assert_eq(fresh.state(),model.state())
	assert_eq(fresh.export_save(),model.export_save())
	return fresh


func test_actual_native_school_prefix_and_earned_records() -> void:
	var model = _exit()
	var original: Dictionary = model._school_state()
	var week: Dictionary = model.state()["week"]
	_enter(model)
	assert_eq(model.stage(),"fifth_planning")
	var native: Dictionary = _json("res://data/school_fifth_planning_evidence.json")["cases"][0]
	assert_eq(model.fifth_session.read_snapshot(),native["after"]["school"],"same CPU native school preparation")
	var expected: Dictionary = native["after"]["roles"].duplicate(true)
	expected.erase("nonparticipant_character_sha256")
	expected.erase("nonparticipant_package_sha256")
	assert_eq(model.state()["school_entry"]["after"],expected)
	assert_eq(model._school_state(),original)
	assert_eq(model.state()["week"],week)
	assert_eq(model.fifth_session.school_context(),"source_fifth_week_planning_4_5")
	assert_false(model.fifth_session.settle_courses(model._rules["growth"],model.fifth_session.revision())["supported"])
	_round_trip(model)


func test_frozen_v3_partial_and_exit_migrate_without_entry() -> void:
	for case in _json("res://data/school_playground_legacy_v3.json")["cases"]:
		var model := Playground.new()
		assert_true(model.restore(case["save"])["supported"])
		assert_eq(model._version3_state(),case["state"])
		assert_eq(model.state()["work_story"]["cursor"],-1)
		assert_eq(model.state()["workroom"],{})
		assert_eq(model.state()["fifth_school"],{})
		assert_eq(model.export_save()["version"],4)
		_round_trip(model)
		var payload: Dictionary = case["save"].duplicate(true)
		payload["rules"]["story"] = Playground.LEGACY_STORY_CRLF_SHA
		assert_true(model.restore(payload)["supported"],"genuine v3 exact CRLF alias")
		payload["commands"].append({"op":"workroom_open"})
		var before: Dictionary = model.state()
		assert_false(model.restore(payload)["supported"],"v3 cannot smuggle new entry commands")
		assert_eq(model.state(),before)


func test_read_all_workroom_pages_previous_and_deep_copy() -> void:
	var model = _exit()
	model.execute({"op":"workroom_open"})
	assert_eq(model.stage(),"workroom")
	_round_trip(model)
	model.execute({"op":"work_start"})
	assert_eq(model.read_work_page()["speaker"],"narrator")
	var saved: Dictionary = model.export_save()
	model.execute({"op":"work_prev"})
	model.execute({"op":"work_start"})
	assert_eq(model.export_save(),saved)
	model.execute({"op":"work_next"})
	assert_eq(model.read_work_page()["speaker"],"portrait:117")
	model.execute({"op":"work_prev"})
	var page: Dictionary = model.read_work_page()
	page["text"] = "tampered"
	assert_true(model.read_work_page()["text"] != page["text"])
	for index in range(32):
		assert_true(model.execute({"op":"work_next"})["supported"])
	assert_eq(model.stage(),"work_completed")
	assert_eq(model.state()["work_story"]["cursor"],32)
	_round_trip(model)
	assert_true(model.execute({"op":"school_enter"})["supported"])
	_round_trip(model)


func test_dynamic_current_class_relationships_and_growth_are_carried() -> void:
	var model := Playground.new()
	model.start()
	for command in [{"op":"move","kind":"student","member_id":9,"target_group":-1,"target_slot":-1},
			{"op":"mode","group":0,"teaching":true},{"op":"course","group":0,"course":12},
			{"op":"grow"},{"op":"confirm"},{"op":"complete"},{"op":"story_start"},{"op":"story_skip"},
			{"op":"week"},{"op":"fifth_start"},{"op":"fifth_skip"},{"op":"fifth_finish"}]:
		assert_true(model.execute(command)["supported"])
	var before: Dictionary = model.session.read_snapshot()
	_enter(model)
	var after: Dictionary = model.fifth_session.read_snapshot()
	for field in ["member_profiles","relationships","global_total_511c","student_ids","teacher_ids","course_buffers"]:
		assert_eq(after[field],before[field],field)
	assert_eq(after["idle_student_ids"],[9])
	assert_eq(Groups._word(after["group_raw_bytes"],10),12)
	assert_eq(after["group_raw_bytes"][3],0,"native default adventure mode")
	_round_trip(model)


func test_fifth_moves_preserve_fourth_week_and_mandatory_adventure_locks_courses() -> void:
	var model = _enter(_exit())
	var original: Dictionary = model._school_state()
	for command in [{"op":"plan_move","kind":"teacher","member_id":101,"target_group":4,"target_slot":-1},
			{"op":"plan_move","kind":"student","member_id":3,"target_group":4,"target_slot":0},
			{"op":"plan_move","kind":"student","member_id":4,"target_group":4,"target_slot":1}]:
		assert_true(model.execute(command)["supported"])
	var saved: Dictionary = model.export_save()
	assert_false(model.execute({"op":"plan_mode","group":4,"teaching":true})["supported"])
	assert_false(model.execute({"op":"plan_course","group":4,"course":11})["supported"])
	assert_eq(model.export_save(),saved,"mandatory source adventure cannot be bypassed")
	var plan: Dictionary = model.fifth_session.read_snapshot()
	assert_eq(Groups._word(plan["group_raw_bytes"],4*28),101)
	assert_eq(plan["group_raw_bytes"][4*28+3],0)
	assert_eq(plan["idle_student_ids"],[9])
	assert_eq(model._school_state(),original)
	_round_trip(model)
	var detached: Dictionary = model.state()
	detached["fifth_school"]["snapshot"]["group_raw_bytes"][0] = 13
	assert_true(model.state() != detached)


func test_early_invalid_and_duplicate_commands_are_atomic() -> void:
	var model := Playground.new()
	model.start()
	for command in [{"op":"workroom_open"},{"op":"school_enter"},{"op":"work_next"},
			{"op":"plan_mode","group":0,"teaching":true}]:
		var before: Dictionary = model.export_save()
		assert_false(model.execute(command)["supported"])
		assert_eq(model.export_save(),before)
	model = _exit()
	var saved: Dictionary = model.export_save()
	assert_false(model.execute({"op":"work_start"})["supported"])
	assert_eq(model.export_save(),saved)
	_enter(model)
	saved = model.export_save()
	for op in ["workroom_open","school_enter","fifth_finish","week"]:
		assert_true(model.execute({"op":op})["supported"])
		assert_eq(model.export_save(),saved)
	for command in [{"op":"grow"},{"op":"work_prev"},{"op":"plan_course","group":0,"course":99},
			{"op":"plan_mode","group":2,"teaching":true},{"op":"school_enter","extra":1}]:
		assert_false(model.execute(command)["supported"])
		assert_eq(model.export_save(),saved)


func test_v4_tamper_and_source_or_art_refusal_leave_memory_intact() -> void:
	var model = _enter(_exit())
	var original: Dictionary = model.state()
	for key in ["state_sha256","rules","commands"]:
		var payload: Dictionary = model.export_save()
		if key == "state_sha256":
			payload[key] = "a".repeat(64)
		elif key == "rules":
			payload[key]["planning"] = "b".repeat(64)
		else:
			payload[key].append({"op":"school_enter"})
		assert_false(model.restore(payload)["supported"])
		assert_eq(model.state(),original)
	model = _exit()
	model.execute({"op":"workroom_open"})
	model.execute({"op":"work_start"})
	model.execute({"op":"work_skip"})
	var saved: Dictionary = model.export_save()
	model._rules["planning"]["adventure_template"]["ordinal"] = 6
	assert_false(model.execute({"op":"school_enter"})["supported"])
	assert_eq(model.export_save(),saved)
	model._rules["workroom"]["outputs_sha256"]["background.png"] = "c".repeat(64)
	assert_false(model.start()["supported"])
	assert_eq(model.export_save(),saved)
