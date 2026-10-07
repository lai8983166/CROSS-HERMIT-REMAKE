extends "res://sim/tests/test_base.gd"

const Session = preload("res://sim/new_game_school_session.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const Group = preload("res://sim/school_teacher_group_replay.gd")


func _rules() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/new_game_school_rules.json")))


func _data() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_planning_evidence_v2.json")))


func _example() -> Session:
	var rules := _rules()
	var session := Session.new()
	assert_true(session.initialize_course_example(rules["origin_rules"],rules["course_rules"],rules)["supported"])
	return session


func test_example_origin_and_explicit_date_match_native_checkpoint() -> void:
	var rules := _rules()
	var session := _example()
	var expected := Session._canonical(_data()["date_checkpoints"][0]["after"])
	assert_eq(session.read_snapshot(),expected)
	assert_eq(session.revision(),3)
	assert_eq(session.school_context(),"declared_course_example_4_4")
	assert_eq(session.journal().size(),5)
	assert_eq(session.journal()[0]["after"],_data()["initialized"])
	assert_eq(session.journal()[1]["phase"],"declared_course_example_date")
	assert_eq(session.journal()[1]["declared_date"],[4,4])
	assert_false(session.view()["live_witness"])
	var before := session.read_snapshot()
	assert_eq(session.initialize_course_example(rules["origin_rules"],rules["course_rules"],rules)["status"],"duplicate")
	assert_eq(session.read_snapshot(),before)
	assert_eq(session.revision(),3)
	assert_false(session.initialize(rules["origin_rules"],rules["course_rules"],rules)["supported"])


func test_owned_mode_and_course_sequence_matches_original_without_hover_writes() -> void:
	var session := _example()
	var data := _data()
	for row in data["cases"].slice(0,10):
		var command: Dictionary = row["command"]
		var before := session.read_snapshot()
		var revision := session.revision()
		var journal := session.journal()
		var result: Dictionary
		if command["kind"] == "mode":
			result = session.set_class_mode(0,command["teaching"],revision)
		elif row["name"] in ["hover_only","empty_category"]:
			result = session.list_courses(0)
			assert_true(result["supported"])
			assert_eq(session.read_snapshot(),before)
			assert_eq(session.revision(),revision)
			continue
		elif row["name"] == "adventure_click_ignored":
			result = session.assign_course(0,11,revision)
			assert_false(result["supported"])
			assert_eq(session.read_snapshot(),before)
			assert_eq(session.journal(),journal)
			continue
		else:
			var source: Array = row["before"]["work_rows"][command["category"]][command["row"]]
			result = session.assign_course(0,source[1],revision)
		assert_true(result["supported"],row["name"] + " " + str(result.get("reason","")))
		assert_eq(session.read_snapshot(),row["canonical_after"],row["name"])
		assert_eq(result.get("ratings"),row["rating"]["ratings"])
		assert_eq(session.revision(),revision if before == row["canonical_after"] else revision + 1)
		if before != row["canonical_after"]:
			assert_eq(session.journal()[-1]["revision"],revision + 1)
			assert_eq(session.journal()[-1]["phase"],"planning_rate")
			assert_eq(session.journal()[-1]["after"],row["canonical_after"])
			var operation: Dictionary = row["before"].duplicate(true)
			for key in row["operation"]["changed_fields"]:
				operation[key] = row["operation"]["changed_fields"][key]
			assert_eq(session.journal()[-2]["after"],Session._canonical(operation))


func test_invalid_stale_unavailable_and_teacherless_requests_are_atomic() -> void:
	var session := _example()
	var before := session.read_snapshot()
	var journal := session.journal()
	for args in [[0,12,2],[0,12,3.0],[0,9,3],[1,12,3],[0,0,3],[5,12,3],[0.0,12,3]]:
		assert_false(session.assign_course(args[0],args[1],args[2])["supported"])
		assert_eq(session.read_snapshot(),before)
		assert_eq(session.journal(),journal)
	for args in [[0,true,2],[0,1,3],[1,true,3]]:
		assert_false(session.set_class_mode(args[0],args[1],args[2])["supported"])
		assert_eq(session.read_snapshot(),before)
		assert_eq(session.journal(),journal)
	assert_false(session.assign_course(0,12,3)["supported"],"adventure class cannot assign")
	assert_false(session.list_courses(1)["supported"])
	assert_eq(session.revision(),3)


func test_example_and_original_ownership_and_registration_are_independent() -> void:
	var rules := _rules()
	var original := Session.new()
	original.initialize(rules["origin_rules"],rules["course_rules"],rules)
	original.prepare_school(1)
	var original_state := original.read_snapshot()
	var example := _example()
	assert_true(example.set_class_mode(0,true,3)["supported"])
	assert_true(example.assign_course(0,12,4)["supported"])
	var state := example.read_snapshot()
	var journal := example.journal()
	var listed := example.list_courses(0)
	listed["courses"][0].clear()
	assert_eq(example.read_snapshot(),state)
	assert_eq(example.journal(),journal)
	assert_eq(example.list_courses(0)["courses"][0].size(),3)
	assert_eq(original.read_snapshot(),original_state)
	assert_eq(original_state["week"],0)
	assert_eq(original.list_courses(0)["courses"],[[],[],[]])
	assert_false(original.initialize_course_example(rules["origin_rules"],rules["course_rules"],rules)["supported"])
	assert_eq(original.read_snapshot(),original_state)
	var moved := example.move_member({"kind":"teacher","member_id":101,"target_group":1},5)
	assert_true(moved["supported"])
	assert_eq(Group._word(moved["snapshot"]["group_raw_bytes"],6),-1)
	assert_eq(Group._word(moved["snapshot"]["group_raw_bytes"],8),-1)
	assert_eq(example.list_courses(1)["courses"][0].size(),3)
	assert_false(example.assign_course(0,12,6)["supported"])


func test_example_bad_rules_refuse_before_any_publication() -> void:
	var rules := _rules()
	for mutation in range(3):
		var input := rules.duplicate(true)
		if mutation == 0:
			input["work_rules"]["teacher_profiles"][0]["attributes"][0] = 255
		elif mutation == 1:
			input["course_rules"]["templates"][0]["month"] = 4
		else:
			input["sort_rules"]["job_categories"][0] = 1
		var session := Session.new()
		assert_false(session.initialize_course_example(input["origin_rules"],input["course_rules"],input)["supported"])
		assert_eq(session.read_snapshot(),{})
		assert_eq(session.journal(),[])
		assert_eq(session.revision(),0)
	var missing := Session.new()
	assert_false(missing.initialize_course_example(rules["origin_rules"],rules["course_rules"],{})["supported"])
	assert_eq(missing.read_snapshot(),{})
