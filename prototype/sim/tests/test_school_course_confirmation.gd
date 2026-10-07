extends "res://sim/tests/test_base.gd"

const Confirmation = preload("res://sim/school_course_confirmation.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func evidence() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_confirmation_evidence_v3.json")))


func test_native_confirmation_records_relations_and_order() -> void:
	var data := evidence()
	for row in data["cases"]:
		var before: Dictionary = row["before"].duplicate(true)
		var records: Array = row["before_records"].duplicate(true)
		var result := Confirmation.apply(before,records,data["rules"])
		assert_true(result["supported"],row["name"]+str(result.get("reason")))
		if not result["supported"]:
			continue
		assert_eq(result["after"],row["after"],row["name"]+" native school")
		assert_eq(result["records"],row["after_records"],row["name"]+" full career/history")
		assert_eq(result["relationship_calls"],row["relationship_calls"],row["name"]+" exact directed calls")
		assert_eq(before,row["before"],"school input retained")
		assert_eq(records,row["before_records"],"record input retained")


func test_source_initial_records_and_boundaries() -> void:
	var data := evidence()
	var runtime: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_confirmation_rules.json")))
	assert_eq(runtime,data["rules"],"source-only runtime rules")
	assert_true(Confirmation.valid_rules(runtime))
	for row in data["cases"]:
		assert_eq(runtime["initial_records"],row["initial_records"],"native initializer cleared history and progress")
	var cap: Dictionary = data["cases"][5]
	assert_eq(cap["after_records"][0]["job_progress"][10],99,"99 remains99")
	assert_eq(cap["after_records"][1]["job_progress"][6],100,"100 remains100")
	assert_eq(cap["after_records"][2]["job_progress"][6],0,"127 wraps signed negative then clamps")
	assert_eq(cap["after_records"][2]["week_records"].slice(9,12),[3,8,9],"waiting only overwrites first byte")


func test_refusals_and_deep_ownership() -> void:
	var data := evidence()
	var row: Dictionary = data["cases"][0]
	for kind in ["source","rules","missing","identity","float","progress","history","date","roster","profile","relation","adventure","unavailable"]:
		var before: Dictionary = row["before"].duplicate(true)
		var records: Array = row["before_records"].duplicate(true)
		var rules: Dictionary = data["rules"].duplicate(true)
		match kind:
			"source": rules["source_image_sha256"] = "bad"
			"rules": rules["job_categories"][1] = 2
			"missing": records.pop_back()
			"identity": records[0]["character_id"] = 4
			"float": records[0]["character_id"] = 3.0
			"progress": records[0]["job_progress"][1] = -1
			"history": records[0]["week_records"].pop_back()
			"date": before["week"] = 5
			"roster": before["student_ids"][2] = 5
			"profile": before["member_profiles"][1]["job"] = 31
			"relation": before["relationships"].pop_back()
			"adventure": before["group_raw_bytes"][3] = 0
			"unavailable": before["group_raw_bytes"][10] = 99
		var saved := {"before":before.duplicate(true),"records":records.duplicate(true)}
		var result := Confirmation.apply(before,records,rules)
		assert_false(result["supported"],kind)
		assert_false(result.has("after"),kind+" no partial result")
		assert_eq(before,saved["before"],kind+" school retained")
		assert_eq(records,saved["records"],kind+" records retained")
	var owned := Confirmation.apply(row["before"],row["before_records"],data["rules"])
	assert_true(owned["supported"])
	if owned["supported"]:
		owned["records"][0]["job_progress"][1] = -1
		owned["after"]["relationships"][0]["value"] = -1
		assert_true(row["before_records"][0]["job_progress"][1] >= 0)
		assert_true(row["before"]["relationships"][0]["value"] >= 0)
