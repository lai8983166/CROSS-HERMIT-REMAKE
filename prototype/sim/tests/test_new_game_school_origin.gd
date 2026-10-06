extends "res://sim/tests/test_base.gd"

const Origin := preload("res://sim/new_game_school_origin.gd")
const Session := preload("res://sim/new_game_school_session.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")
const Courses := preload("res://sim/school_course_unlocking.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const DATA := "res://data/new_game_school_evidence.json"


func _data() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(DATA)))


func _legacy() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_teacher_group_evidence.json")))


func _authority(result: Dictionary) -> void:
	for key in ["school_initialized","interactive_school_ready","live_witness","authorizes_persistent_write"]:
		assert_false(result[key])


func test_native_initialization_reinitialization_and_all_preparation_phases() -> void:
	var data := _data()
	var saved := data.duplicate(true)
	assert_eq(data["cases"].size(),3)
	for row in data["cases"]:
		var built := Origin.construct(data["origin_rules"])
		assert_true(built["supported"])
		assert_eq(built.get("after"),row["initialized"]["after"],row["name"])
		_authority(built)
		if row.has("reinitialized"):
			built = Origin.construct(data["origin_rules"],0)
			assert_eq(built["after"],row["reinitialized"]["after"])
		var old: Dictionary = built["after"].duplicate(true)
		var unlocked := Courses.unlock_courses(built["after"],data["course_rules"])
		assert_eq(built["after"],old)
		assert_true(unlocked["supported"])
		assert_eq(unlocked.get("after"),row["preparation"][0]["after"])
		var clean := Groups.reconcile(unlocked["after"],Origin.group_rules())
		assert_true(clean["supported"])
		assert_eq(clean.get("after"),row["preparation"][1]["after"])
		var rated := Groups.rate(clean["after"],Origin.group_rules())
		assert_true(rated["supported"])
		assert_eq(rated.get("after"),row["preparation"][2]["after"])
		assert_eq(rated.get("ratings"),row["preparation"][2]["ratings"])
		_authority(unlocked)
		_authority(clean)
		_authority(rated)
	assert_eq(data,saved)


func test_owned_session_phases_revision_and_journal_match_native() -> void:
	var data := _data()
	var row: Dictionary = data["cases"][0]
	var session := Session.new()
	var started := session.initialize(data["origin_rules"],data["course_rules"])
	assert_true(started["supported"])
	assert_eq(started["status"],"initialized_once")
	assert_eq(started["revision"],1)
	assert_false(started["school_data_prepared"])
	assert_eq(started["snapshot"],row["initialized"]["after"])
	var ready := session.prepare_school(1)
	assert_true(ready["supported"])
	assert_eq(ready["status"],"prepared_once")
	assert_eq(ready["revision"],2)
	assert_true(ready["school_data_prepared"])
	assert_eq(ready["snapshot"],row["preparation"][2]["after"])
	assert_eq(ready["ratings"],row["preparation"][2]["ratings"])
	var journal := session.journal()
	assert_eq(journal.size(),4)
	assert_eq(journal[0]["phase"],"initialize")
	assert_eq(journal[0]["after"],row["initialized"]["after"])
	for index in range(3):
		assert_eq(journal[index+1]["phase"],row["preparation"][index]["phase"])
		assert_eq(journal[index+1]["revision"],2)
		assert_eq(journal[index+1]["after"],row["preparation"][index]["after"])
		assert_eq(journal[index+1]["before"],journal[index]["after"])
	_authority(started)
	_authority(ready)


func test_duplicate_initialization_preparation_and_stale_revision_refuse_republication() -> void:
	var data := _data()
	var session := Session.new()
	assert_false(session.prepare_school(0)["supported"])
	session.initialize(data["origin_rules"],data["course_rules"])
	assert_eq(session.initialize(data["origin_rules"],data["course_rules"])["status"],"duplicate")
	assert_eq(session.revision(),1)
	for revision in [0,2,1.0,true,"1",null]:
		var result := session.prepare_school(revision)
		assert_false(result["supported"])
		assert_eq(result["reason"],"stale_school_revision")
		assert_false(result.has("snapshot"))
		assert_eq(session.revision(),1)
		assert_eq(session.journal().size(),1)
		_authority(result)
	session.prepare_school(1)
	var before := session.read_snapshot()
	assert_eq(session.prepare_school(2)["status"],"duplicate")
	assert_false(session.prepare_school(1)["supported"])
	assert_eq(session.initialize(data["origin_rules"],data["course_rules"])["status"],"duplicate")
	assert_eq(session.read_snapshot(),before)
	assert_eq(session.revision(),2)
	assert_eq(session.journal().size(),4)
	var bad: Dictionary = data["origin_rules"].duplicate(true)
	bad["calls"][0]["group"] = 1
	assert_eq(session.initialize(bad,data["course_rules"])["reason"],"school_origin_input_conflict")
	assert_eq(session.read_snapshot(),before)


func test_changed_source_fields_types_or_missing_inputs_refuse_without_state() -> void:
	var data := _data()
	for kind in ["source","hash","initializer","calls","call","group","slot","member","profile","job","level","attributes","storage","template","relations","relation","relation_type","points","statuses","skills","threshold","cost","float","null"]:
		var rules: Dictionary = data["origin_rules"].duplicate(true)
		match kind:
			"source": rules["source_image_sha256"] = "other"
			"hash": rules["origin_fields_sha256"] = "other"
			"initializer": rules["initializer_va"] += 1
			"calls": rules["calls"].pop_back()
			"call": rules["calls"][0]["call_va"] += 1
			"group": rules["calls"][0]["group"] = 1
			"slot": rules["calls"][0]["slot"] = 0
			"member": rules["calls"][0]["member_id"] = 117
			"profile": rules["member_profiles"].reverse()
			"job": rules["member_profiles"][0]["job"] = 2
			"level": rules["member_profiles"][1]["level_50"] = 31
			"attributes": rules["member_profiles"][0]["attributes"][0] = 2
			"storage": rules["member_profiles"][0]["storage_kind"] = "student_record"
			"template": rules["member_profiles"][0]["template_sha256"] = "0".repeat(64)
			"relations": rules["relationships"].pop_back()
			"relation": rules["relationships"][0]["value"] = 60
			"relation_type": rules["relationships"][0]["value"] = 75.0
			"points": rules["student_level_inputs"][0]["growth_pools"][0] += 1
			"statuses": rules["student_level_inputs"][0]["skill_statuses"][0] = 255
			"skills": rules["student_level_inputs"][0]["equipped_skills"][0] = 84
			"threshold": rules["level_thresholds"][0] += 1
			"cost": rules["learned_points"][0] += 1
			"float": rules["member_profiles"][0]["attributes"][0] = 1.0
			"null": rules["student_level_inputs"][0] = null
		var saved := rules.duplicate(true)
		var result := Origin.construct(rules)
		assert_false(result["supported"],kind)
		assert_false(result.has("after"))
		assert_eq(rules,saved)
		var session := Session.new()
		assert_false(session.initialize(rules,data["course_rules"])["supported"],kind)
		assert_eq(session.read_snapshot(),{})
		assert_eq(session.revision(),0)
		assert_eq(session.journal(),[])
		_authority(result)
	for selection in [-2,1,0.0,false,null,"0"]:
		assert_false(Origin.construct(data["origin_rules"],selection)["supported"])
	var bad: Dictionary = data["course_rules"].duplicate(true)
	bad["templates"][0]["teacher_mask"][0] = 0
	var session := Session.new()
	assert_false(session.initialize(data["origin_rules"],bad)["supported"])
	assert_eq(session.revision(),0)
	assert_eq(session.read_snapshot(),{})


func test_origin_teacher_domain_does_not_widen_legacy_or_authorize_registration() -> void:
	var data := _data()
	var legacy := _legacy()
	var before: Dictionary = Origin.construct(data["origin_rules"])["after"]
	assert_eq(Groups.TEACHERS,[117,118])
	assert_false(Groups._domain(101,true))
	assert_false(Groups.reconcile(before,legacy["rules"])["supported"])
	assert_false(Groups.rate(before,legacy["rules"])["supported"])
	var result := Groups.register_teacher(before,{"kind":"direct_helper","teacher_id":117,"group":-1,"slot":-1},Origin.group_rules())
	assert_false(result["supported"])
	for row in legacy["cases"]:
		assert_false(Groups.reconcile(row["before"],Origin.group_rules())["supported"])
	for kind in ["scope","initializer","hash"]:
		var rules := Origin.group_rules()
		match kind:
			"scope": rules["teacher_scope"] = "chapter012"
			"initializer": rules["initializer_va"] = 4843824.0
			"hash": rules["origin_fields_sha256"] = "other"
		assert_false(Groups.reconcile(before,rules)["supported"])
	var bad := before.duplicate(true)
	bad["teacher_ids"][0] = 117
	bad["availability"][101] = 0
	bad["availability"][117] = 1
	assert_false(Groups.reconcile(bad,Origin.group_rules())["supported"])


func test_teacher_profile_owned_static_storage_and_recomputed_student_level() -> void:
	var data := _data()
	var session := Session.new()
	assert_false(session.read_teacher_profile(101)["supported"])
	session.initialize(data["origin_rules"],data["course_rules"])
	var view := session.read_teacher_profile(101)
	assert_true(view["supported"])
	assert_eq(view["profile"]["storage_kind"],"static_teacher_template")
	assert_eq(view["profile"]["attributes"],[1,1,1,1,1,1,1])
	assert_eq(session.read_snapshot()["member_profiles"][1]["level_50"],31)
	for identity in [3,117,118,101.0,true,null]:
		assert_false(session.read_teacher_profile(identity)["supported"])
	view["profile"]["attributes"].clear()
	assert_eq(session.read_teacher_profile(101)["profile"]["attributes"],[1,1,1,1,1,1,1])
	_authority(view)


func test_source_only_inputs_ignore_oracles_and_isolate_all_views() -> void:
	var data := _data()
	var rules: Dictionary = data["origin_rules"].duplicate(true)
	var courses: Dictionary = data["course_rules"].duplicate(true)
	var oracle := {"expected_after":{"teacher_count":20},"fake":[999]}
	rules["expected_after"] = oracle
	rules["member_profiles"][0]["expected_after"] = oracle
	courses["expected_after"] = oracle
	courses["templates"][0]["expected_after"] = oracle
	var session := Session.new()
	var started := session.initialize(rules,courses)
	assert_true(started["supported"])
	assert_eq(started["snapshot"],data["cases"][0]["initialized"]["after"])
	assert_false(session._origin_rules.has("expected_after"))
	assert_false(session._origin_rules["member_profiles"][0].has("expected_after"))
	assert_false(session._course_rules.has("expected_after"))
	assert_false(session._course_rules["templates"][0].has("expected_after"))
	rules["member_profiles"][0]["attributes"].clear()
	courses["templates"].clear()
	started["snapshot"]["member_profiles"].clear()
	started["snapshot"]["group_raw_bytes"].clear()
	assert_eq(session.read_snapshot(),data["cases"][0]["initialized"]["after"])
	var journal := session.journal()
	journal[0]["after"]["student_ids"].clear()
	assert_eq(session.journal()[0]["after"],session.read_snapshot())
	var other := Session.new()
	other.initialize(data["origin_rules"],data["course_rules"])
	session.prepare_school(1)
	assert_eq(other.read_snapshot(),data["cases"][0]["initialized"]["after"])
	assert_eq(other.revision(),1)
	assert_eq(session.revision(),2)


func test_late_preparation_failure_does_not_publish_unlocked_or_reconciled_state() -> void:
	var data := _data()
	var session := Session.new()
	session.initialize(data["origin_rules"],data["course_rules"])
	var good := session.read_snapshot()
	# Simulate an inconsistent internal catalog before a future edit operation.
	session._snapshot["relationships"].pop_back()
	var before := session.read_snapshot()
	var journal := session.journal()
	var result := session.prepare_school(1)
	assert_false(result["supported"])
	assert_eq(result["reason"],"missing_group_relationship")
	assert_eq(session.read_snapshot(),before)
	assert_eq(session.journal(),journal)
	assert_eq(session.revision(),1)
	assert_false(session._prepared)
	assert_eq(session.read_snapshot()["course_unlocked_flags"],Origin._filled(101,0))
	session._snapshot = good
	assert_true(session.prepare_school(1)["supported"])
