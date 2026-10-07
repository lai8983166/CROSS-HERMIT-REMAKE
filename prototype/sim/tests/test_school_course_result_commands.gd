extends "res://sim/tests/test_base.gd"

const Session := preload("res://sim/new_game_school_session.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")


func rules(name: String) -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/"+name+".json")))


func confirmed(waiting: bool = false) -> Session:
	var input := rules("new_game_school_rules")
	var session := Session.new()
	assert_true(session.initialize_course_example(input["origin_rules"],input["course_rules"],input)["supported"])
	if waiting:
		assert_true(session.move_member({"kind":"student","member_id":3,"target_group":-1},session.revision())["supported"])
	session.set_class_mode(0,true,session.revision())
	session.assign_course(0,10,session.revision())
	assert_true(session.settle_courses(rules("school_course_settlement_rules"),session.revision())["supported"])
	assert_true(session.confirm_courses(rules("school_course_confirmation_rules"),session.revision())["supported"])
	return session


func test_owned_mvp_count_handoff_and_atomic_journal() -> void:
	var evidence := rules("school_course_result_handoff_evidence_v1")
	for index in range(2):
		var session := confirmed(index == 1)
		var row: Dictionary = evidence["cases"][index]
		var snapshot := session.read_snapshot()
		var growth := session.read_growth_records()
		var records := session.read_confirmation_records()
		var revision := session.revision()
		var journal_size := session.journal().size()
		var result := session.complete_course_result(rules("school_course_result_handoff_rules"),revision)
		assert_true(result["supported"])
		assert_eq(session.read_mvp_counts(),row["after_result"]["counts"],"native recipient count")
		assert_eq(session.read_result_handoff()["recipient"],row["growth_checkpoint"]["recipient"])
		assert_eq(session.read_result_handoff()["adv_request"]["chapter"],row["loads"][-1]["path"])
		assert_eq(session.read_snapshot(),snapshot,"result handoff leaves school fields/date")
		assert_eq(session.read_growth_records(),growth,"growth not repeated")
		assert_eq(session.read_confirmation_records(),records,"career/history not repeated")
		assert_eq(session.revision(),revision+1)
		assert_eq(session.journal().size(),journal_size+2)
		assert_eq(session.journal()[-2]["phase"],"course_mvp_count")
		assert_eq(session.journal()[-1]["phase"],"course_adv_request")
		for row_j in session.journal().slice(-2):
			assert_eq(row_j["revision"],revision+1)
			assert_eq(row_j["after"],snapshot)
		assert_eq(session.view()["course_result_handoff"],session.read_result_handoff())
		assert_false(result["authorizes_persistent_write"])


func test_duplicate_stale_invalid_and_deep_copy() -> void:
	var session := confirmed()
	var input := rules("school_course_result_handoff_rules")
	input["recipient"] = 9
	input["expected_after"] = {"count":99}
	assert_true(session.complete_course_result(input,session.revision())["supported"])
	var saved := [session.read_snapshot(),session.read_mvp_counts(),session.read_result_handoff(),session.journal(),session.revision()]
	assert_eq(session.complete_course_result(input,session.revision())["status"],"duplicate")
	for kind in ["stale","float","source","count","script"]:
		var altered := input.duplicate(true)
		var revision: Variant = session.revision()
		match kind:
			"stale": revision -= 1
			"float": revision = float(revision)
			"source": altered["source_image_sha256"] = "bad"
			"count": altered["initial_counts"][0]["count"] = 1
			"script": altered["script_sha256"]["adv/dat/ch003.ybc"] = "bad"
		assert_false(session.complete_course_result(altered,revision)["supported"],kind)
	var view := session.view()
	view["course_result_handoff"]["counts"].clear()
	var result := session.read_result_handoff()
	result["adv_request"]["chapter"] = "evil"
	var counts := session.read_mvp_counts()
	counts[0]["count"] = 99
	var journal := session.journal()
	journal[-1]["adv_request"].clear()
	input["initial_counts"].clear()
	assert_eq([session.read_snapshot(),session.read_mvp_counts(),session.read_result_handoff(),session.journal(),session.revision()],saved)
	assert_false(session._result_rules.has("expected_after"))
	assert_false(session._result_rules.has("recipient"))


func test_later_planning_cannot_change_frozen_mvp() -> void:
	var session := confirmed()
	var expected: Dictionary = rules("school_course_result_handoff_evidence_v1")["cases"][0]
	session.move_member({"kind":"student","member_id":3,"target_group":-1},session.revision())
	session.assign_course(0,12,session.revision())
	var snapshot := session.read_snapshot()
	assert_true(session.complete_course_result(rules("school_course_result_handoff_rules"),session.revision())["supported"])
	assert_eq(session.read_result_handoff()["recipient"],expected["growth_checkpoint"]["recipient"])
	assert_eq(session.read_mvp_counts(),expected["after_result"]["counts"])
	assert_eq(session.read_snapshot(),snapshot)
	var count := session.journal().size()
	session.move_member({"kind":"student","member_id":4,"target_group":-1},session.revision())
	assert_eq(session.complete_course_result(rules("school_course_result_handoff_rules"),session.revision())["status"],"duplicate")
	assert_eq(session.journal().size(),count+3,"only movement stages added")
	assert_eq(session.read_mvp_counts(),expected["after_result"]["counts"])


func test_unconfirmed_source_and_late_refusal_leave_no_partial_result() -> void:
	var empty := Session.new()
	assert_false(empty.complete_course_result(rules("school_course_result_handoff_rules"),0)["supported"])
	var input := rules("new_game_school_rules")
	var source := Session.new()
	source.initialize(input["origin_rules"],input["course_rules"],input)
	source.prepare_school(source.revision())
	var snapshot := source.read_snapshot()
	assert_false(source.complete_course_result(rules("school_course_result_handoff_rules"),source.revision())["supported"])
	assert_eq(source.read_snapshot(),snapshot)
	assert_eq(source.read_result_handoff(),{})
	var session := confirmed()
	for kind in ["confirmation","zero","missing"]:
		var confirmation := session._confirmation.duplicate(true)
		var growth: Array = session._settlement["records"].duplicate(true)
		match kind:
			"confirmation": session._confirmation = {}
			"zero":
				for row in session._settlement["records"]:
					row["staged_total"] = 0
			"missing": session._settlement["records"].pop_back()
		var journal := session.journal()
		assert_false(session.complete_course_result(rules("school_course_result_handoff_rules"),session.revision())["supported"],kind)
		assert_eq(session.journal(),journal)
		assert_eq(session.read_mvp_counts(),[])
		assert_eq(session.read_result_handoff(),{})
		assert_eq(session.revision(),7)
		session._confirmation = confirmation
		session._settlement["records"] = growth
