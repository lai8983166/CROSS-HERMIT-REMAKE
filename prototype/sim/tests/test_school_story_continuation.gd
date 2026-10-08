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
	var candidate := Playground.new()
	assert_true(candidate.start()["supported"])
	assert_true(candidate.restore_text(JSON.stringify(model.export_save()))["supported"])
	assert_eq(candidate.state(),model.state())
	assert_eq(candidate.export_save(),model.export_save())
	return candidate


func test_exact_native_week_inputs_and_outputs_and_once_only() -> void:
	var native: Dictionary = _json("res://data/school_story_week_evidence_v1.json")["cases"][0]
	var model = _course()
	var counts: Array = model.state()["counts"]
	assert_false(model.execute({"op":"week"})["supported"])
	assert_true(model.execute({"op":"story_start"})["supported"])
	assert_true(model.execute({"op":"story_skip"})["supported"])
	assert_eq(model.stage(),"story_completed")
	assert_true(model.execute({"op":"week"})["supported"])
	assert_eq(model.stage(),"arrival")
	var actual: Dictionary = model.state()["week"]
	for field in ["before","after"]:
		var expected: Dictionary = native[field+"_week"].duplicate(true)
		expected.erase("nonparticipant_character_sha256")
		expected.erase("nonparticipant_package_sha256")
		assert_eq(actual[field],expected,field+" is native same-CPU result")
	assert_eq(model.state()["counts"],counts)
	assert_false(actual["handoff"]["school_initialized"])
	assert_eq(actual["handoff"]["next_task"],8)
	var saved: Dictionary = model.export_save()
	assert_true(model.execute({"op":"week"})["supported"])
	assert_eq(model.export_save(),saved,"a consumed week cannot repeat")
	assert_false(model.execute({"op":"story_prev"})["supported"])
	assert_false(model.execute({"op":"grow"})["supported"])
	_restore(model)


func test_reading_forward_previous_and_partial_second_scene_replay() -> void:
	var model = _course()
	var school: Dictionary = model._school_state()
	assert_false(model.execute({"op":"story_next"})["supported"])
	assert_true(model.execute({"op":"story_start"})["supported"])
	assert_eq(model.read_story_page()["speaker"],4)
	var save: Dictionary = model.export_save()
	assert_true(model.execute({"op":"story_prev"})["supported"])
	assert_true(model.execute({"op":"story_start"})["supported"])
	assert_eq(model.export_save(),save,"duplicate start/previous does not consume log")
	assert_true(model.execute({"op":"story_next"})["supported"])
	assert_eq(model.read_story_page()["speaker"],101)
	assert_true(model.execute({"op":"story_prev"})["supported"])
	for index in range(68):
		assert_true(model.execute({"op":"story_next"})["supported"])
	assert_eq(model.read_story_page()["chapter"],17)
	assert_eq(model.state()["story"]["cursor"],68)
	var copy = _restore(model)
	assert_eq(copy.read_story_page(),model.read_story_page())
	assert_eq(model._school_state(),school,"reading never changes growth, MVP or school revisions")
	var exposed: Dictionary = copy.read_story_page()
	exposed["text"] = "changed"
	assert_false(copy.read_story_page()["text"] == "changed")
	while model.stage() == "story":
		assert_true(model.execute({"op":"story_next"})["supported"])
	assert_eq(model.state()["story"]["cursor"],109)
	assert_eq(model.stage(),"story_completed")
	var complete: Dictionary = model.export_save()
	assert_true(model.execute({"op":"story_next"})["supported"])
	assert_true(model.execute({"op":"story_skip"})["supported"])
	assert_eq(model.export_save(),complete)
	_restore(model)


func test_legacy_v1_restores_and_migrates_without_losing_result() -> void:
	var legacy := _json("res://data/school_playground_legacy_v1.json")
	assert_eq(legacy["version"],1)
	var model := Playground.new()
	model.start()
	assert_true(model.restore(legacy)["supported"])
	assert_eq(model.stage(),"completed")
	assert_eq(model._school_state(),_course()._school_state())
	assert_eq(model.state()["story"]["cursor"],-1)
	assert_eq(model.export_save()["version"],4)
	assert_eq(model.export_save()["commands"],legacy["commands"])
	assert_true(model.execute({"op":"story_start"})["supported"])
	_restore(model)
	var before: Dictionary = model.state()
	var bad: Dictionary = legacy.duplicate(true)
	bad["commands"].append({"op":"story_start"})
	assert_false(model.restore(bad)["supported"])
	assert_eq(model.state(),before)
	bad = legacy.duplicate(true)
	bad["rules"]["result"] = "changed"
	assert_false(model.restore(bad)["supported"])
	assert_eq(model.state(),before)


func test_corrupt_continuation_restore_is_atomic() -> void:
	var model = _course()
	model.execute({"op":"story_start"})
	model.execute({"op":"story_next"})
	var before: Dictionary = model.state()
	var saved: Dictionary = model.export_save()
	for command in [{"op":"week"},{"op":"story_next","cursor":100},{"op":"move","kind":"student","member_id":3,"target_group":-1,"target_slot":-1}]:
		var bad: Dictionary = saved.duplicate(true)
		bad["commands"].append(command)
		assert_false(model.restore(bad)["supported"])
		assert_eq(model.state(),before)
	var bad: Dictionary = saved.duplicate(true)
	bad["rules"]["story"] = "changed"
	assert_false(model.restore(bad)["supported"])
	assert_eq(model.state(),before)
	bad = saved.duplicate(true)
	bad["state_sha256"] = "0".repeat(64)
	assert_false(model.restore(bad)["supported"])
	assert_eq(model.state(),before)
	var owned: Dictionary = model.state()
	owned["story"]["cursor"] = 100
	assert_eq(model.state(),before)


func test_other_course_and_waiting_inputs_preserved_through_week() -> void:
	var model = _course(12,9)
	model.execute({"op":"story_start"})
	model.execute({"op":"story_skip"})
	var before: Dictionary = model._school_state()
	assert_true(model.execute({"op":"week"})["supported"])
	var week: Dictionary = model.state()["week"]
	for index in range(3):
		assert_eq(week["before"]["participants"][index]["attributes"],before["growth"][index]["attributes"])
		assert_eq(week["after"]["participants"][index]["attributes"],before["growth"][index]["attributes"])
	assert_eq(week["after"]["availability"][9],1,"waiting students remain enrolled")
	assert_eq(week["after"]["week"],5)
	assert_eq(model._school_state(),before)
	_restore(model)


func test_corrupt_art_is_refused_before_resetting_existing_progress() -> void:
	var model = _course()
	model.execute({"op":"story_start"})
	var before: Dictionary = model.state()
	var saved: Dictionary = model.export_save()
	model._rules["story"]["outputs_sha256"]["actor_4.png"] = "changed"
	assert_false(model.start()["supported"])
	assert_eq(model.state(),before)
	assert_eq(model.export_save(),saved)
