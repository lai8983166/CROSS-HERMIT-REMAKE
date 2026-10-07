extends "res://sim/tests/test_base.gd"

const Session = preload("res://sim/new_game_school_session.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _rules() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/new_game_school_rules.json")))


func _growth_rules() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_settlement_rules.json")))


func _example() -> Session:
	var rules := _rules()
	var session := Session.new()
	assert_true(session.initialize_course_example(rules["origin_rules"],rules["course_rules"],rules)["supported"])
	return session


func _confirmation_rules() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_confirmation_rules.json")))


func _confirmation_evidence() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_confirmation_evidence_v3.json")))


func _grown(course: int = 10) -> Session:
	var session := _example()
	session.set_class_mode(0,true,session.revision())
	session.assign_course(0,course,session.revision())
	assert_true(session.settle_courses(_growth_rules(),session.revision())["supported"])
	return session


func test_native_owned_confirmation_and_journal() -> void:
	for row in _confirmation_evidence()["cases"].slice(0,5):
		var session := _example()
		var group: int = row["setup"]["group"]
		for identity in row["setup"]["waiting_students"]:
			session.move_member({"kind":"student","member_id":identity,"target_group":-1},session.revision())
		if group == 4:
			session.move_member({"kind":"teacher","member_id":101,"target_group":4},session.revision())
			for slot in range(3):
				session.move_member({"kind":"student","member_id":[3,4,9][slot],"target_group":4,"target_slot":slot},session.revision())
		session.set_class_mode(group,true,session.revision())
		session.assign_course(group,row["setup"]["course_id"],session.revision())
		assert_true(session.settle_courses(_growth_rules(),session.revision())["supported"])
		assert_eq(session.read_snapshot(),row["before"],row["name"]+" native pre-confirm school")
		var revision := session.revision()
		var count := session.journal().size()
		var result := session.confirm_courses(_confirmation_rules(),revision)
		assert_true(result["supported"],row["name"]+str(result.get("reason")))
		assert_eq(session.read_snapshot(),row["rated_after"],row["name"]+" complete native school")
		assert_eq(session.read_confirmation_records(),row["after_records"],row["name"]+" complete career/history")
		assert_eq(session.read_growth_records(),row["after_growth_records"],row["name"]+" refreshed career sums")
		assert_eq(session.read_confirmation()["relationship_calls"],row["relationship_calls"])
		assert_eq(session.revision(),revision+1)
		assert_eq(session.journal().size(),count+2)
		for index in range(2):
			assert_eq(session.journal()[count+index]["revision"],revision+1)
			assert_eq(session.journal()[count+index]["phase"],["course_confirmation_fields","course_confirmation_rate"][index])
		assert_eq(session.journal()[-1]["after"],row["rated_after"])
		assert_false(result["authorizes_persistent_write"])


func test_confirmation_refusals_and_late_failure_are_atomic() -> void:
	var empty := Session.new()
	assert_false(empty.confirm_courses(_confirmation_rules(),0)["supported"])
	var unready := _example()
	assert_false(unready.confirm_courses(_confirmation_rules(),unready.revision())["supported"])
	var session := _grown()
	for kind in ["stale","float","rules","source","records","late_rate"]:
		var rules := _confirmation_rules()
		var revision: Variant = session.revision()
		match kind:
			"stale": revision -= 1
			"float": revision = float(revision)
			"rules": rules["job_categories"][1] += 1
			"source": rules["source_image_sha256"] = "bad"
			"records": rules["initial_records"][0]["character_id"] = 3.0
			"late_rate": session._snapshot["availability"][3] = 0
		var saved := {"school":session.read_snapshot(),"growth":session.read_growth_records(),"journal":session.journal()}
		assert_false(session.confirm_courses(rules,revision)["supported"],kind)
		assert_eq(session.read_snapshot(),saved["school"],kind+" school preserved")
		assert_eq(session.read_growth_records(),saved["growth"],kind+" growth preserved")
		assert_eq(session.journal(),saved["journal"],kind+" journal preserved")
		assert_eq(session.revision(),6)
		assert_eq(session.read_confirmation_records(),[])
		assert_eq(session.read_confirmation(),{})
		session._snapshot["availability"][3] = 1


func test_confirmation_duplicate_and_deep_copies() -> void:
	var session := _grown()
	var rules := _confirmation_rules()
	rules["expected_after"] = {"evil":true}
	var result := session.confirm_courses(rules,session.revision())
	assert_true(result["supported"])
	var saved := {"school":session.read_snapshot(),"records":session.read_confirmation_records(),"journal":session.journal()}
	assert_eq(session.confirm_courses(_confirmation_rules(),7)["status"],"duplicate")
	assert_false(session.confirm_courses(_confirmation_rules(),6)["supported"])
	assert_eq(session.revision(),7)
	assert_eq(session.journal(),saved["journal"])
	result["course_confirmation"]["records"].clear()
	var view := session.view()
	view["course_confirmation"]["settled_school"]["relationships"].clear()
	var records := session.read_confirmation_records()
	records[0]["job_progress"][1] = -1
	var journal := session.journal()
	journal[-2]["confirmation"]["before_records"].clear()
	rules["initial_records"][0]["week_records"][9] = 99
	assert_false(session.confirm_courses(rules,7)["supported"])
	assert_eq(session.read_snapshot(),saved["school"])
	assert_eq(session.read_confirmation_records(),saved["records"])
	assert_eq(session.journal(),saved["journal"])
	assert_false(session._confirmation_rules.has("expected_after"),"oracle removed")


func test_confirmation_uses_settled_roster_and_preserves_other_sessions() -> void:
	var session := _grown()
	session.move_member({"kind":"student","member_id":9,"target_group":-1},session.revision())
	session.assign_course(0,12,session.revision())
	var edited := session.read_snapshot()
	assert_true(session.confirm_courses(_confirmation_rules(),session.revision())["supported"])
	var source: Dictionary = _confirmation_evidence()["cases"][0]
	assert_eq(session.read_confirmation_records(),source["after_records"],"history uses original course10 and participating9")
	assert_eq(session.read_snapshot()["relationships"],source["after"]["relationships"],"relationships use settled roster")
	assert_eq(session.read_snapshot()["group_raw_bytes"],edited["group_raw_bytes"],"current edited plan retained")
	assert_eq(session.read_snapshot()["idle_student_ids"],edited["idle_student_ids"],"current waiting retained")
	var rules := _rules()
	var original := Session.new()
	original.initialize(rules["origin_rules"],rules["course_rules"],rules)
	original.prepare_school(original.revision())
	var before := original.read_snapshot()
	assert_false(original.confirm_courses(_confirmation_rules(),original.revision())["supported"])
	assert_eq(original.read_snapshot(),before)
	assert_eq(original.read_confirmation(),{})
	assert_eq(_example().read_confirmation_records(),[],"new example starts empty")
