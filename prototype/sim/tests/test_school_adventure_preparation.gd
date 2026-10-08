extends "res://sim/tests/test_base.gd"
const Playground := preload("res://sim/school_playground.gd")
const Preparation := preload("res://sim/school_adventure_preparation.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")


func _json(path: String) -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(path)))


func _school():
	var model := Playground.new()
	assert_true(model.restore(_json("res://data/school_playground_legacy_v3.json")["cases"][1]["save"])["supported"])
	for op in ["workroom_open","work_start","work_skip","school_enter"]:
		assert_true(model.execute({"op":op})["supported"])
	return model


func test_same_cpu_current_squads_and_teacher_refusals() -> void:
	var model = _school()
	for case in _json("res://data/school_adventure_preparation_evidence.json")["cases"]:
		for command in case["commands"]:
			var move: Dictionary = command.duplicate(true)
			move["op"] = "plan_move"
			assert_true(model.execute(move)["supported"])
		assert_eq(model.fifth_session.read_snapshot(),case["before"]["school"],case["name"]+" current native school")
		var before: Dictionary = model.state()
		var save: Dictionary = model.export_save()
		var revision: int = model.revision()
		var result: Dictionary = model.adventure_preparation()
		assert_true(result["supported"])
		assert_eq(result["ready"],case["ready"])
		assert_eq(result["class_ratings"],case["class_ratings"])
		assert_eq(result["prepared"],case["prepared"],case["name"]+" source defined output")
		assert_eq(model.state(),before)
		assert_eq(model.export_save(),save)
		assert_eq(model.revision(),revision)


func test_preparation_is_repeatable_and_output_is_detached() -> void:
	var model = _school()
	var original: Dictionary = model.adventure_preparation()
	var altered: Dictionary = model.adventure_preparation()
	altered["prepared"]["rounds"][0]["student_ids"].clear()
	altered["class_ratings"][0]["work_fields"][2] = 99
	assert_eq(model.adventure_preparation(),original)
	assert_false(original["battle_executed"])
	assert_false(original["mandatory_gate_cleared"])
	assert_eq(model.fifth_session.read_snapshot()["adventure_gate"],1)


func test_v4_save_and_earned_records_survive_preparation() -> void:
	var model = _school()
	var saved: Dictionary = model.export_save()
	assert_eq(saved["version"],4)
	assert_eq(saved["rules"].size(),10)
	var fresh := Playground.new()
	assert_true(fresh.restore_text(JSON.stringify(saved))["supported"])
	assert_eq(fresh.adventure_preparation(),model.adventure_preparation())
	assert_eq(fresh.export_save(),saved)
	assert_eq(fresh._school_state(),model._school_state())
	assert_eq(fresh.fifth_session.read_snapshot()["member_profiles"],model.session.read_snapshot()["member_profiles"])


func test_premature_query_has_no_effect() -> void:
	var model := Playground.new()
	assert_false(model.adventure_preparation()["supported"])
	assert_true(model.start()["supported"])
	var before: Dictionary = model.state()
	assert_false(model.adventure_preparation()["supported"])
	assert_eq(model.state(),before)


func test_invalid_source_rules_are_refused_without_mutation() -> void:
	var school: Dictionary = _school().fifth_session.read_snapshot()
	var rules := _json(Preparation.RULE_PATH)
	var prior: Dictionary = school.duplicate(true)
	for pair in [["source_image_sha256","bad"],["record_sha256","bad"],["round_specs",[{"scene_id":1,"selection_word":1}]],
		["required_work_fields",[3,4,6,0]],["adventure_id",6],["functions",{}]]:
		var invalid: Dictionary = rules.duplicate(true)
		invalid[pair[0]] = pair[1]
		assert_false(Preparation.project(school,invalid)["supported"])
	assert_false(Preparation.project(school,{})["supported"])
	assert_eq(school,prior)


func test_invalid_school_inputs_never_prepare_or_unlock() -> void:
	var school: Dictionary = _school().fifth_session.read_snapshot()
	var rules := _json(Preparation.RULE_PATH)
	for pair in [["week",4],["adventure_gate",0],["lecture_active",0],["lecture_work_fields",[3,4,6,0]],
		["group_raw_bytes",[]],["relationships",[]]]:
		var invalid: Dictionary = school.duplicate(true)
		invalid[pair[0]] = pair[1]
		var before: Dictionary = invalid.duplicate(true)
		assert_false(Preparation.project(invalid,rules)["supported"])
		assert_eq(invalid,before)
