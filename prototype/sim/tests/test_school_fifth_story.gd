extends "res://sim/tests/test_base.gd"
const Playground := preload("res://sim/school_playground.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")


func _json(path: String) -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(path)))


func _course(course := 10, waiting := -1):
	var model := Playground.new()
	assert_true(model.start()["supported"])
	if waiting >= 0:
		assert_true(model.execute({"op":"move","kind":"student","member_id":waiting,"target_group":-1,"target_slot":-1})["supported"])
	for command in [{"op":"mode","group":0,"teaching":true},{"op":"course","group":0,"course":course},
			{"op":"grow"},{"op":"confirm"},{"op":"complete"}]:
		assert_true(model.execute(command)["supported"])
	return model


func _restore(model):
	var copy := Playground.new()
	copy.start()
	assert_true(copy.restore_text(JSON.stringify(model.export_save()))["supported"])
	assert_eq(copy.state(),model.state())
	assert_eq(copy.export_save(),model.export_save())
	return copy


func _arrive(course := 10, waiting := -1):
	var model = _course(course,waiting)
	for op in ["story_start","story_skip","week"]:
		assert_true(model.execute({"op":op})["supported"])
	return model


func test_fifth_exit_matches_native_without_repeating_school_or_week() -> void:
	var model = _arrive()
	var school: Dictionary = model._school_state()
	var week: Dictionary = model.state()["week"]
	assert_false(model.execute({"op":"fifth_finish"})["supported"])
	assert_true(model.execute({"op":"fifth_start"})["supported"])
	assert_eq(model.stage(),"fifth_story")
	assert_true(model.execute({"op":"fifth_skip"})["supported"])
	assert_eq(model.stage(),"fifth_completed")
	_restore(model)
	assert_true(model.execute({"op":"fifth_finish"})["supported"])
	assert_eq(model.stage(),"workroom_entry")
	var native: Dictionary = _json("res://data/school_fifth_week_evidence.json")["cases"][0]
	var actual: Dictionary = model.state()["fifth_exit"]
	for field in ["before","after"]:
		var expected: Dictionary = native[field].duplicate(true)
		expected.erase("nonparticipant_character_sha256")
		expected.erase("nonparticipant_package_sha256")
		assert_eq(actual[field],expected,"native fifth-week "+field)
	assert_eq(actual["handoff"]["pending_state"],8)
	assert_false(actual["handoff"]["workroom_body_executed"])
	assert_false(actual["handoff"]["school_initialized"])
	assert_eq(model._school_state(),school)
	assert_eq(model.state()["week"],week)
	var saved: Dictionary = model.export_save()
	assert_true(model.execute({"op":"fifth_finish"})["supported"])
	assert_true(model.execute({"op":"week"})["supported"])
	assert_eq(model.export_save(),saved)
	assert_false(model.execute({"op":"fifth_prev"})["supported"])
	assert_false(model.execute({"op":"grow"})["supported"])
	_restore(model)


func test_fifth_reading_previous_replacement_and_all_pages() -> void:
	var model = _arrive()
	assert_false(model.execute({"op":"fifth_next"})["supported"])
	model.execute({"op":"fifth_start"})
	assert_eq(model.read_fifth_page()["speaker"],"body:9")
	var saved: Dictionary = model.export_save()
	model.execute({"op":"fifth_prev"})
	model.execute({"op":"fifth_start"})
	assert_eq(model.export_save(),saved)
	model.execute({"op":"fifth_next"})
	model.execute({"op":"fifth_prev"})
	for index in range(121):
		assert_true(model.execute({"op":"fifth_next"})["supported"])
	assert_eq(model.read_fifth_page()["speaker"],"portrait:27")
	var copy = _restore(model)
	assert_eq(copy.read_fifth_page(),model.read_fifth_page())
	var exposed: Dictionary = model.read_fifth_page()
	exposed["characters"][0]["id"] = 99
	assert_eq(model.read_fifth_page()["characters"][0]["id"],12)
	var catalog: Dictionary = model.fifth_catalog()
	catalog["actors"]["portrait:27"]["name"] = "changed"
	assert_eq(model.fifth_catalog()["actors"]["portrait:27"]["name"],"娜芙忒卡")
	while model.stage() == "fifth_story":
		assert_true(model.execute({"op":"fifth_next"})["supported"])
	assert_eq(model.state()["fifth_story"]["cursor"],126)
	assert_true(model.read_fifth_page().is_empty())
	_restore(model)


func test_frozen_version2_partial_story_and_arrival_migrate() -> void:
	for case in _json("res://data/school_playground_legacy_v2.json")["cases"]:
		var model := Playground.new()
		model.start()
		assert_eq(case["save"]["version"],2)
		assert_true(model.restore(case["save"])["supported"])
		assert_eq(model._version2_state(),case["state"])
		assert_eq(model.state()["fifth_story"]["cursor"],-1)
		assert_eq(model.export_save()["version"],3)
		assert_eq(model.export_save()["commands"],case["save"]["commands"])
		_restore(model)
		if case["name"] == "arrival":
			assert_true(model.execute({"op":"fifth_start"})["supported"])
		else:
			assert_false(model.execute({"op":"fifth_start"})["supported"])
		var before: Dictionary = model.state()
		var bad: Dictionary = case["save"].duplicate(true)
		bad["commands"].append({"op":"fifth_start"})
		assert_false(model.restore(bad)["supported"])
		assert_eq(model.state(),before)


func test_fifth_corrupt_saves_and_early_commands_are_atomic() -> void:
	var model = _course()
	var initial: Dictionary = model.state()
	assert_false(model.execute({"op":"fifth_start"})["supported"])
	assert_eq(model.state(),initial)
	model = _arrive()
	model.execute({"op":"fifth_start"})
	model.execute({"op":"fifth_next"})
	var before: Dictionary = model.state()
	var saved: Dictionary = model.export_save()
	for command in [{"op":"fifth_finish"},{"op":"fifth_next","cursor":121},{"op":"story_prev"}]:
		var bad: Dictionary = saved.duplicate(true)
		bad["commands"].append(command)
		assert_false(model.restore(bad)["supported"])
		assert_eq(model.state(),before)
	for field in ["fifth","fifth_story"]:
		var bad: Dictionary = saved.duplicate(true)
		bad["rules"][field] = "changed"
		assert_false(model.restore(bad)["supported"])
		assert_eq(model.state(),before)
	var bad: Dictionary = saved.duplicate(true)
	bad["state_sha256"] = "0".repeat(64)
	assert_false(model.restore(bad)["supported"])
	assert_eq(model.state(),before)


func test_fifth_preserves_current_course_waiting_and_mvp() -> void:
	var model = _arrive(12,9)
	var school: Dictionary = model._school_state()
	var week: Dictionary = model.state()["week"]
	for op in ["fifth_start","fifth_skip","fifth_finish"]:
		assert_true(model.execute({"op":op})["supported"])
	assert_eq(model._school_state(),school)
	assert_eq(model.state()["week"],week)
	assert_eq(model.state()["fifth_exit"]["after"]["participants"],week["after"]["participants"])
	assert_eq(model.state()["fifth_exit"]["after"]["availability"],week["after"]["availability"])
	assert_eq(model.state()["fifth_exit"]["after"]["adv_globals"]["0x7e1180"],school["result"]["recipient"])
	_restore(model)


func test_fifth_bad_assets_and_handoff_keep_progress() -> void:
	var model = _arrive()
	model.execute({"op":"fifth_start"})
	model.execute({"op":"fifth_skip"})
	model._week["handoff"]["next_task"] = 9
	var before: Dictionary = model.state()
	assert_false(model.execute({"op":"fifth_finish"})["supported"])
	assert_eq(model.state(),before)
	model._rules["fifth_story"]["outputs_sha256"]["portrait_31.png"] = "changed"
	assert_false(model.start()["supported"])
	assert_eq(model.state(),before)
