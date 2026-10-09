extends "res://sim/tests/test_base.gd"
const Playground := preload("res://sim/school_playground.gd")
const Handoff := preload("res://sim/school_adventure_handoff.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")


func _json(path: String) -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(path)))


func _school():
	var model := Playground.new()
	assert_true(model.restore(_json("res://data/school_playground_legacy_v3.json")["cases"][1]["save"])["supported"])
	for op in ["workroom_open","work_start","work_skip","school_enter"]:
		assert_true(model.execute({"op":op})["supported"])
	return model


func _configuration_from_native(record: String) -> Dictionary:
	var raw := PackedByteArray()
	for i in range(record.length()/2):
		raw.append(record.substr(i*2,2).hex_to_int())
	return {"scene_id":raw.decode_u16(0),"field_448a":raw.decode_u16(2),
		"flags_448c_4491":Array(raw.slice(4,10)),
		"fields_4492_44a0":range(8).map(func(i): return raw.decode_u16(10+i*2)),
		"fields_44a2_44a4":Array(raw.slice(26,29)),
		"time_limits":range(4).map(func(i): return raw.decode_u32(32+i*4)),
		"flags_44b8_44bd":Array(raw.slice(48,54)),"objective_slots":Array(raw.slice(54,70))}


func test_current_squads_match_native_commit_round_and_configuration() -> void:
	for case in _json("res://data/school_adventure_handoff_evidence.json")["cases"]:
		var model = _school()
		for command in case["commands"]:
			var move: Dictionary = command.duplicate(true)
			move["op"] = "plan_move"
			assert_true(model.execute(move)["supported"])
		assert_eq(model.fifth_session.read_snapshot(),case["before"]["school"],case["name"]+" current school")
		var before: Dictionary = model.state()
		var save: Dictionary = model.export_save()
		var revision: int = model.revision()
		var result: Dictionary = model.adventure_handoff()
		assert_true(result["supported"],case["name"])
		assert_eq(result["ready"],case["ready"])
		assert_eq(result["prepared"],case["prepared"])
		assert_eq(result["ledger_after"],case["ledger_after"])
		assert_eq(result["requested_states"],case["requested_states"])
		if case["ready"]:
			var expected: Dictionary = case["round_after"].duplicate(true)
			expected.erase("configuration_bytes")
			assert_eq(result["round_after"],expected)
			assert_eq(result["configuration"],_configuration_from_native(case["round_after"]["configuration_bytes"]))
		else:
			assert_eq(result["round_after"],null)
			assert_eq(result["configuration"],null)
		assert_eq(model.state(),before)
		assert_eq(model.export_save(),save)
		assert_eq(model.revision(),revision)
		for key in ["combat_units_ready","resources_resolved","battle_executed","mandatory_gate_cleared",
				"live_witness","authorizes_persistent_write"]:
			assert_false(result[key])


func test_pure_output_cannot_consume_the_current_ledger_or_change_saved_progress() -> void:
	var model = _school()
	var original: Dictionary = model.adventure_handoff()
	var altered: Dictionary = model.adventure_handoff()
	altered["prepared"]["rounds"][0]["student_ids"].clear()
	altered["round_after"]["temp_roster"].clear()
	altered["configuration"]["objective_slots"].clear()
	model.adventure_ledger()["ledger"]["entries"].clear()
	assert_eq(model.adventure_handoff(),original)
	assert_eq(model.adventure_ledger()["ledger"]["entries"].size(),1)
	var save: Dictionary = model.export_save()
	assert_eq(save["version"],4)
	assert_eq(save["rules"].size(),10)
	var fresh := Playground.new()
	assert_true(fresh.restore_text(JSON.stringify(save))["supported"])
	assert_eq(fresh.adventure_handoff(),original)
	assert_eq(fresh.export_save(),save)


func test_invalid_rules_and_ledger_are_atomic_refusals() -> void:
	var model = _school()
	var school: Dictionary = model.fifth_session.read_snapshot()
	var ledger: Dictionary = model.adventure_ledger()["ledger"]
	var rules := _json(Handoff.RULE_PATH)
	for pair in [["configuration_id",1],["configuration_record_hex","00"],["configuration_record_sha256","bad"],
			["configuration_stride",41],["functions",{}],["unresolved_functions",[]],["departure",{}]]:
		var invalid: Dictionary = rules.duplicate(true)
		invalid[pair[0]] = pair[1]
		assert_false(Handoff.project(school,ledger,invalid)["supported"])
	for pair in [["id",6],["busy",1],["limit",1.5],["duration",1],["elapsed",1],["metadata",[]]]:
		var invalid: Dictionary = ledger.duplicate(true)
		invalid["entries"][0][pair[0]] = pair[1]
		var before: Dictionary = invalid.duplicate(true)
		assert_false(Handoff.project(school,invalid,rules)["supported"])
		assert_eq(invalid,before)
	assert_false(Handoff.project(school,{},rules)["supported"])
	assert_false(Handoff.project(school,{"entries":[]},rules)["supported"])
	assert_eq(model.adventure_ledger()["ledger"],ledger)
	assert_eq(model.fifth_session.read_snapshot(),school)


func test_initial_ledger_requires_the_source_template() -> void:
	var template: Dictionary = _json("res://data/school_fifth_planning_rules.json")["adventure_template"]
	assert_eq(Handoff.initial_ledger(template)["ledger"],_school().adventure_ledger()["ledger"])
	for pair in [["metadata",1],["limit",2],["record_sha256","bad"],["id",6],["kind",3]]:
		var invalid: Dictionary = template.duplicate(true)
		invalid[pair[0]] = pair[1]
		assert_false(Handoff.initial_ledger(invalid)["supported"])


func test_premature_or_invalid_school_cannot_handoff() -> void:
	var model := Playground.new()
	assert_false(model.adventure_handoff()["supported"])
	assert_false(model.adventure_ledger()["supported"])
	assert_true(model.start()["supported"])
	var before: Dictionary = model.state()
	assert_false(model.adventure_handoff()["supported"])
	assert_eq(model.state(),before)
	var school: Dictionary = _school().fifth_session.read_snapshot()
	var rules := _json(Handoff.RULE_PATH)
	var ledger: Dictionary = _school().adventure_ledger()["ledger"]
	for pair in [["week",4],["adventure_gate",0],["group_raw_bytes",[]],["relationships",[]]]:
		var invalid: Dictionary = school.duplicate(true)
		invalid[pair[0]] = pair[1]
		var prior: Dictionary = invalid.duplicate(true)
		assert_false(Handoff.project(invalid,ledger,rules)["supported"])
		assert_eq(invalid,prior)


func test_slot_order_is_current_and_not_copied_from_a_fixture() -> void:
	var model = _school()
	assert_true(model.execute({"op":"plan_move","kind":"student","member_id":9,"target_group":0,"target_slot":0})["supported"])
	assert_true(model.execute({"op":"plan_move","kind":"student","member_id":4,"target_group":-1,"target_slot":-1})["supported"])
	var result: Dictionary = model.adventure_handoff()
	assert_true(result["supported"])
	var ids: Array = result["prepared"]["rounds"][0]["student_ids"]
	assert_eq(ids,[9,3])
	assert_eq(result["round_after"]["temp_roster"].slice(0,2),ids)
	assert_eq(result["round_after"]["combat_count"],2)
