extends "res://sim/tests/test_base.gd"

const Session = preload("res://sim/new_game_school_session.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const Settlement = preload("res://sim/school_course_settlement.gd")


func _rules() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/new_game_school_rules.json")))


func _growth_rules() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_settlement_rules.json")))


func _evidence() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_settlement_evidence_v1.json")))


func _example() -> Session:
	var rules := _rules()
	var session := Session.new()
	assert_true(session.initialize_course_example(rules["origin_rules"],rules["course_rules"],rules)["supported"])
	return session


func test_three_source_courses_and_atomic_journal() -> void:
	for row in _evidence()["cases"].slice(0,3):
		var session := _example()
		assert_true(session.set_class_mode(0,true,session.revision())["supported"])
		assert_true(session.assign_course(0,row["setup"]["course_id"],session.revision())["supported"])
		assert_eq(session.read_snapshot(),row["before"],row["name"] + " source before")
		var revision := session.revision()
		var count := session.journal().size()
		var result := session.settle_courses(_growth_rules(),revision)
		assert_true(result["supported"],row["name"] + " " + str(result.get("reason")))
		assert_eq(session.read_snapshot(),row["after"],row["name"] + " source school after")
		assert_eq(session.read_growth_records(),row["after_records"],row["name"] + " owned records")
		assert_eq(session.revision(),revision+1)
		assert_eq(session.journal().size(),count+3)
		for index in range(3):
			assert_eq(session.journal()[count+index]["revision"],revision+1)
			assert_eq(session.journal()[count+index]["phase"],["course_result_prepare","course_growth","course_growth_rate"][index])
		assert_eq(session.journal()[-1]["after"],row["after"])
		assert_eq(session.journal()[-2]["growth"]["before_records"],row["before_records"])
		for key in ["packets","learning_draws","rand_state","bonus","skill_display_needed"]:
			assert_eq(session.read_settlement()[key],row[key],row["name"] + " " + key)
		assert_eq(session.read_settlement()["declared_clock_seed"],4660)
		assert_false(result["authorizes_persistent_write"])


func test_waiting_student_and_fifth_class_match_source() -> void:
	for index in [4,5]:
		var row: Dictionary = _evidence()["cases"][index]
		var session := _example()
		var group: int = row["setup"]["group"]
		if index == 4:
			assert_true(session.move_member({"kind":"student","member_id":9,"target_group":-1},session.revision())["supported"])
		else:
			assert_true(session.move_member({"kind":"teacher","member_id":101,"target_group":4},session.revision())["supported"])
			for slot in range(3):
				assert_true(session.move_member({"kind":"student","member_id":[3,4,9][slot],"target_group":4,"target_slot":slot},session.revision())["supported"])
		assert_true(session.set_class_mode(group,true,session.revision())["supported"])
		assert_true(session.assign_course(group,10,session.revision())["supported"])
		assert_true(session.settle_courses(_growth_rules(),session.revision())["supported"])
		assert_eq(session.read_snapshot(),row["after"])
		assert_eq(session.read_growth_records(),row["after_records"])


func test_refusals_preserve_all_owned_state() -> void:
	var empty := Session.new()
	assert_false(empty.settle_courses(_growth_rules(),0)["supported"])
	var session := _example()
	for kind in ["no_course","stale","float","rules","origin","origin_float"]:
		var rules := _growth_rules()
		var revision: Variant = session.revision()
		match kind:
			"stale": revision -= 1
			"float": revision = float(revision)
			"rules": rules["training"][12]["package"][0] += 1
			"origin": rules["initial_job_sums"][0]["job_sums"][0] += 1
			"origin_float": rules["initial_job_sums"][0]["character_id"] = 3.0
		var snapshot := session.read_snapshot()
		var journal := session.journal()
		assert_false(session.settle_courses(rules,revision)["supported"],kind)
		assert_eq(session.read_snapshot(),snapshot)
		assert_eq(session.journal(),journal)
		assert_eq(session.revision(),3)
		assert_eq(session.read_growth_records(),[])
		assert_eq(session.read_settlement(),{})
	assert_true(session.set_class_mode(0,true,session.revision())["supported"])
	assert_true(session.assign_course(0,12,session.revision())["supported"])
	assert_true(session.set_class_mode(0,false,session.revision())["supported"])
	var before := session.read_snapshot()
	assert_false(session.settle_courses(_growth_rules(),session.revision())["supported"])
	assert_eq(session.read_snapshot(),before)


func test_duplicate_completion_and_deep_ownership() -> void:
	var session := _example()
	session.set_class_mode(0,true,session.revision())
	session.assign_course(0,10,session.revision())
	var rules := _growth_rules()
	var result := session.settle_courses(rules,session.revision())
	assert_true(result["supported"])
	var before := session.read_snapshot()
	var revision := session.revision()
	var journal := session.journal()
	var growth := session.read_growth_records()
	assert_eq(session.settle_courses(rules,revision)["status"],"duplicate")
	assert_false(session.settle_courses(rules,revision-1)["supported"])
	assert_eq(session.read_snapshot(),before)
	assert_eq(session.revision(),revision)
	assert_eq(session.journal(),journal)
	result["course_settlement"]["records"][0]["growth_pools"][0] = -1
	rules["training"][10]["package"][0] = -1
	var view := session.view()
	view["course_settlement"]["before_records"].clear()
	var copied := session.read_growth_records()
	copied[0]["attributes"][0] = -1
	assert_eq(session.read_growth_records(),growth)
	assert_eq(session.read_snapshot(),before)
	assert_false(session.settle_courses(rules,revision)["supported"])
	assert_eq(session.revision(),revision)
	# Changing plans afterwards cannot reopen this completed date example.
	assert_true(session.assign_course(0,12,revision)["supported"])
	assert_true(session.move_member({"kind":"student","member_id":9,"target_group":-1},session.revision())["supported"])
	var current := session.revision()
	assert_eq(session.settle_courses(_growth_rules(),current)["status"],"duplicate")
	assert_eq(session.revision(),current)
	assert_eq(session.read_growth_records(),growth)


func test_source_example_and_reinitialization_are_independent() -> void:
	var rules := _rules()
	var source := Session.new()
	assert_true(source.initialize(rules["origin_rules"],rules["course_rules"],rules)["supported"])
	assert_true(source.prepare_school(source.revision())["supported"])
	var original := source.read_snapshot()
	var session := _example()
	session.set_class_mode(0,true,session.revision())
	session.assign_course(0,10,session.revision())
	assert_true(session.settle_courses(_growth_rules(),session.revision())["supported"])
	assert_false(source.settle_courses(_growth_rules(),source.revision())["supported"])
	assert_eq(source.read_snapshot(),original)
	assert_eq(source.revision(),2)
	assert_eq(source.read_growth_records(),[])
	assert_eq(source.read_settlement(),{})
	var grown := session.read_growth_records()
	assert_eq(session.initialize_course_example(rules["origin_rules"],rules["course_rules"],rules)["status"],"duplicate")
	assert_eq(session.read_growth_records(),grown)
	assert_eq(_example().read_growth_records(),[],"fresh example has no completed growth")
