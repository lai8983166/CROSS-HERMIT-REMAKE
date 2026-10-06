extends "res://sim/tests/test_base.gd"

const Session = preload("res://sim/new_game_school_session.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _data() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/new_game_school_movement_evidence.json")))


func _rules() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/new_game_school_rules.json")))


func _new_session() -> Session:
	var rules := _rules()
	var session := Session.new()
	assert_true(session.initialize(rules["origin_rules"],rules["course_rules"],rules)["supported"])
	assert_true(session.prepare_school(1)["supported"])
	return session


func _request(row: Dictionary) -> Dictionary:
	var command: Dictionary = row["command"]
	return {"kind":command["kind"],"member_id":command[command["kind"] + "_id"],
		"target_group":command["target_group"],"target_slot":command.get("target_slot",-1)}


func test_owned_release_sequence_matches_native_and_each_journal_phase() -> void:
	var data := _data()
	var session := _new_session()
	assert_eq(session.read_snapshot(),data["prepared"])
	for row in data["cases"]:
		if not row["command"]["released"]:
			continue
		var before := session.read_snapshot()
		var revision := session.revision()
		var size := session.journal().size()
		var result := session.move_member(_request(row),revision)
		assert_true(result["supported"],row["name"] + " " + str(result.get("reason","")))
		assert_eq(session.read_snapshot(),row["canonical_after"],row["name"])
		if before == row["canonical_after"]:
			assert_eq(result["status"],"duplicate")
			assert_eq(session.revision(),revision)
			assert_eq(session.journal().size(),size)
		else:
			assert_eq(result["revision"],revision + 1)
			var journal := session.journal().slice(size)
			assert_eq(journal.size(),3)
			var expected: Dictionary = row["before"].duplicate(true)
			for index in range(3):
				for key in row["phases"][index]["changed_fields"]:
					expected[key] = row["phases"][index]["changed_fields"][key]
				assert_eq(journal[index]["after"],Session._canonical(expected),row["name"] + " phase%d" % index)
				assert_eq(journal[index]["revision"],revision + 1)
			assert_eq(journal[0]["before"],before)
			assert_eq(journal[1]["before"],journal[0]["after"])
			assert_eq(journal[2]["before"],journal[1]["after"])
		assert_eq(result["ratings"],row["phases"][2]["ratings"])
		assert_false(result["live_witness"])
		assert_false(result["authorizes_persistent_write"])


func test_stale_invalid_missing_and_injected_commands_are_atomic() -> void:
	var session := _new_session()
	var before := session.read_snapshot()
	var journal := session.journal()
	var command := {"kind":"student","member_id":3,"target_group":-1}
	assert_false(session.move_member(command,1)["supported"])
	assert_false(session.move_member(command,2.0)["supported"])
	for bad in [
		{"kind":"student","member_id":5,"target_group":0,"target_slot":0},
		{"kind":"teacher","member_id":117,"target_group":1},
		{"kind":"student","member_id":3,"target_group":0},
		{"kind":"teacher","member_id":101,"target_group":5},
		{"kind":"teacher","member_id":101,"target_group":1,"target_slot":0},
		{"kind":"student","member_id":3,"target_group":-1,"source_group":0},
		{"kind":"student","member_id":3,"target_group":-1,"after":{}},
		{"kind":0,"member_id":3,"target_group":-1}]:
		var result := session.move_member(bad,2)
		assert_false(result["supported"])
		assert_false(result.has("snapshot"))
		assert_false(result.has("after"))
		assert_eq(session.read_snapshot(),before)
		assert_eq(session.revision(),2)
		assert_eq(session.journal(),journal)


func test_ownership_and_repeat_requests_use_current_sources() -> void:
	var rules := _rules()
	var session := Session.new()
	session.initialize(rules["origin_rules"],rules["course_rules"],rules)
	session.prepare_school(1)
	rules["work_rules"]["teacher_profiles"][0]["attributes"][0] = 255
	rules["origin_rules"]["relationships"][0]["value"] = 0
	var request := {"kind":"student","member_id":3,"target_group":-1}
	var result := session.move_member(request,2)
	assert_true(result["supported"])
	var saved := session.read_snapshot()
	request["member_id"] = 9
	result["snapshot"]["idle_student_ids"].clear()
	var copied := session.journal()
	copied[-1]["after"]["group_raw_bytes"].clear()
	assert_eq(session.read_snapshot(),saved)
	assert_eq(session.journal()[-1]["command"]["member_id"],3)
	var repeat := session.move_member({"kind":"student","member_id":3,"target_group":-1},session.revision())
	assert_eq(repeat["status"],"duplicate")
	assert_eq(session.read_snapshot(),saved)
	var joined := session.move_member({"kind":"student","member_id":3,"target_group":0,"target_slot":3},session.revision())
	assert_true(joined["supported"])
	assert_eq(joined["snapshot"]["derived_student_ids"][0],[-1,4,9,3])
	assert_eq(joined["snapshot"]["group_raw_bytes"][22],3)


func test_missing_preparation_or_movement_rules_refuses_without_state() -> void:
	var session := Session.new()
	var request := {"kind":"teacher","member_id":101,"target_group":1}
	assert_false(session.move_member(request,0)["supported"])
	var rules := _rules()
	session.initialize(rules["origin_rules"],rules["course_rules"],rules)
	var before := session.read_snapshot()
	assert_false(session.move_member(request,1)["supported"])
	assert_eq(session.read_snapshot(),before)
	var legacy := Session.new()
	legacy.initialize(rules["origin_rules"],rules["course_rules"])
	legacy.prepare_school(1)
	assert_eq(legacy.move_member(request,2)["reason"],"school_movement_not_prepared")


func test_source_only_rules_ignore_oracles_but_reject_changed_known_fields() -> void:
	var rules := _rules()
	rules["cases"] = [{"after":{"teacher_count":20}}]
	rules["work_rules"]["teacher_profiles"][0]["after"] = {"attributes":[255]}
	var session := Session.new()
	assert_true(session.initialize(rules["origin_rules"],rules["course_rules"],rules)["supported"])
	session.prepare_school(1)
	assert_true(session.move_member({"kind":"teacher","member_id":101,"target_group":1},2)["supported"])
	for bad in ["categories","attributes","fingerprint","missing"]:
		var changed := _rules()
		if bad == "categories":
			changed["sort_rules"]["job_categories"][0] = 1
		elif bad == "attributes":
			changed["work_rules"]["teacher_profiles"][0]["attributes"][0] = 0
		elif bad == "fingerprint":
			changed["work_rules"]["origin_fields_sha256"] = "unknown"
		else:
			changed.erase("work_rules")
		var rejected := Session.new()
		assert_false(rejected.initialize(changed["origin_rules"],changed["course_rules"],changed)["supported"])
		assert_eq(rejected.read_snapshot(),{})
		assert_eq(rejected.revision(),0)
		assert_eq(rejected.journal(),[])
