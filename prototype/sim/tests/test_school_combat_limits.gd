extends "res://sim/tests/test_base.gd"
const Playground := preload("res://sim/school_playground.gd")
const Limits := preload("res://sim/school_combat_limits.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")


func _json(path: String) -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(path)))


func _rules() -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string(Limits.RULE_PATH))


func _school():
	var model := Playground.new()
	assert_true(model.restore(_json("res://data/school_playground_legacy_v3.json")["cases"][1]["save"])["supported"])
	for op in ["workroom_open","work_start","work_skip","school_enter"]:
		assert_true(model.execute({"op":op})["supported"])
	return model


func test_current_squads_match_native_limits_and_keep_save_state() -> void:
	for case in _json("res://data/school_combat_records_evidence.json")["cases"]:
		var model = _school()
		for command in case["commands"]:
			var move: Dictionary = command.duplicate(true)
			move["op"] = "plan_move"
			assert_true(model.execute(move)["supported"])
		var before: Dictionary = model.state()
		var save: Dictionary = model.export_save()
		var revision: int = model.revision()
		var result: Dictionary = model.adventure_combat_limits()
		assert_true(result["supported"],case["name"])
		assert_eq(result["ready"],case["ready"])
		assert_eq(result["students"],case["combat_records"].map(func(r): return {"input":r["input"],"limits":r["limits"]}))
		assert_eq(model.state(),before)
		assert_eq(model.export_save(),save)
		assert_eq(model.revision(),revision)
		for flag in ["full_combat_records","battle_world_constructed","battle_executed","mandatory_gate_cleared","live_witness","authorizes_persistent_write"]:
			assert_false(result[flag])


func test_clamps_and_fractional_recovery_match_declared_native_probes() -> void:
	for probe in _json("res://data/school_combat_records_evidence.json")["counterfactuals"]:
		var input: Dictionary = probe["declared_counterfactual_input"]
		var before: Dictionary = input.duplicate(true)
		var result := Limits.project(input,_rules())
		assert_true(result["supported"],probe["name"])
		assert_eq(result["limits"],probe["record"]["limits"])
		assert_eq(input,before)


func test_copied_output_restore_and_current_slot_order() -> void:
	var model = _school()
	var before: Dictionary = model.adventure_combat_limits()
	model.adventure_combat_limits()["students"][0]["input"]["attributes"].clear()
	model.adventure_combat_limits()["students"][0]["limits"]["hp"] = 1
	assert_eq(model.adventure_combat_limits(),before)
	var save: Dictionary = model.export_save()
	assert_eq(save["version"],4)
	assert_eq(save["rules"].size(),10)
	var fresh := Playground.new()
	assert_true(fresh.restore_text(JSON.stringify(save))["supported"])
	assert_eq(fresh.adventure_combat_limits(),before)
	assert_eq(fresh.export_save(),save)
	assert_true(model.execute({"op":"plan_move","kind":"student","member_id":9,"target_group":0,"target_slot":0})["supported"])
	assert_true(model.execute({"op":"plan_move","kind":"student","member_id":4,"target_group":-1,"target_slot":-1})["supported"])
	assert_eq(model.adventure_combat_limits()["students"].map(func(s): return s["input"]["character_id"]),[9,3])


func test_source_corruption_is_refused_atomically() -> void:
	var input: Dictionary = _json("res://data/school_combat_records_evidence.json")["cases"][0]["combat_records"][0]["input"]
	for pair in [["half_coefficient",0],["supported_skills",[0,1]],["engagement_minutes",[]],
		["functions",[]],["source_image_sha256","bad"],["authorizes_persistent_write",0]]:
		var bad := _rules()
		bad[pair[0]] = pair[1]
		assert_false(Limits.project(input,bad)["supported"])
	for pair in [["hp_coefficient",99],["mp_coefficient",100.5],["record_hex","00"],["record_sha256","bad"]]:
		var bad := _rules()
		bad["jobs"][0][pair[0]] = pair[1]
		assert_false(Limits.project(input,bad)["supported"])
	var bad := _rules()
	bad["skills"][0]["modifier_callback"] = 1
	assert_false(Limits.project(input,bad)["supported"])


func test_unsupported_roles_and_fractional_bytes_refuse_without_mutation() -> void:
	var input: Dictionary = _json("res://data/school_combat_records_evidence.json")["cases"][0]["combat_records"][0]["input"]
	for pair in [["character_id",101],["job",1],["job",6.5],["level",256],["level",true],
		["attributes",[1,1,1,1,1,1,1.5]],["equipped_items",[1,0,0,0,0,0,0,0]],
		["equipped_skills",[1,0,0,0,0,0,0,0]],["equipped_skills",[]]]:
		var bad: Dictionary = input.duplicate(true)
		bad[pair[0]] = pair[1]
		var before: Dictionary = bad.duplicate(true)
		assert_false(Limits.project(bad,_rules())["supported"])
		assert_eq(bad,before)
	assert_false(Limits.project({},_rules())["supported"])
	var model := Playground.new()
	assert_false(model.adventure_combat_limits()["supported"])
	assert_true(model.start()["supported"])
	assert_false(model.adventure_combat_limits()["supported"])


func test_verified_skills_do_not_read_item_table_as_limit_bonuses() -> void:
	var input: Dictionary = _json("res://data/school_combat_records_evidence.json")["cases"][0]["combat_records"][0]["input"]
	var original := Limits.project(input,_rules())
	input["equipped_skills"] = [0,0,0,0,0,0,0,0]
	assert_eq(Limits.project(input,_rules()),original)
