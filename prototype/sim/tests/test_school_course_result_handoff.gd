extends "res://sim/tests/test_base.gd"

const Handoff := preload("res://sim/school_course_result_handoff.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")


func data() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_result_handoff_evidence_v1.json")))


func test_native_result_recipient_counts_and_destination() -> void:
	var evidence := data()
	assert_true(Handoff.valid_rules(evidence["rules"]))
	for row in evidence["cases"]:
		if not row["result_completed"]:
			assert_eq(row["result_requests"],[],"pending result has no ADV request")
			assert_eq(row["after_result"]["counts"],row["growth_checkpoint"]["counts"],"pending count unchanged")
			continue
		var growth: Dictionary = row["growth_checkpoint"]
		var result := Handoff.apply(growth["school"],growth["records"],growth["counts"],evidence["rules"])
		assert_true(result["supported"],row["name"]+str(result.get("reason")))
		if not result["supported"]:
			continue
		assert_eq(result["recipient"],growth["recipient"],row["name"]+" actual native selector")
		assert_eq(result["old_count"],growth["old_count"])
		assert_eq(result["counts"],row["after_result"]["counts"],"native short count clamp")
		assert_eq(result["adv_request"]["state"],row["result_requests"][0])
		assert_eq(result["adv_request"]["next_task"],row["after_result"]["stored_next_task"])
		assert_eq(result["adv_request"]["chapter"],row["loads"][-1]["path"])
		assert_eq(row["stop_reason"],"chapter016_entry_boundary")
		assert_eq(result["date"],[row["after_result"]["school"]["month"],row["after_result"]["school"]["week"]])
		assert_false(result["adv_request"]["chapter_completed"])
		assert_false(result["adv_request"]["week_advanced"])


func test_native_selection_ties_zero_and_later_higher() -> void:
	var evidence := data()
	for row in evidence["selection_probes"]:
		var result := Handoff.apply(row["before"],row["records"],row["counts"],evidence["rules"])
		if row["recipient"] == -1:
			assert_false(result["supported"])
			assert_eq(result["reason"],"missing_positive_mvp_recipient")
		else:
			assert_true(result["supported"],row["name"])
			assert_eq(result["recipient"],row["recipient"],row["name"])
			assert_eq(result["staged_total"],row["best"])


func test_refusals_and_input_ownership() -> void:
	var evidence := data()
	var row: Dictionary = evidence["cases"][0]["growth_checkpoint"]
	for kind in ["rules","script","initial_count","date","identity","float","total","counts","class","missing"]:
		var school: Dictionary = row["school"].duplicate(true)
		var records: Array = row["records"].duplicate(true)
		var counts: Array = row["counts"].duplicate(true)
		var rules: Dictionary = evidence["rules"].duplicate(true)
		match kind:
			"rules": rules["next_task"] = 8
			"script": rules["script_sha256"]["adv/dat/ch003.ybc"] = "bad"
			"initial_count": rules["initial_counts"][0]["count"] = 1
			"date": school["week"] = 5
			"identity": records[0]["character_id"] = 4
			"float": records[0]["staged_total"] = 3.0
			"total": records[0]["staged_total"] = -1
			"counts": counts[0]["count"] = 6
			"class": school["group_raw_bytes"][3] = 0
			"missing": records.pop_back()
		var saved := [school.duplicate(true),records.duplicate(true),counts.duplicate(true)]
		var result := Handoff.apply(school,records,counts,rules)
		assert_false(result["supported"],kind)
		assert_false(result.has("counts"),kind+" no partial output")
		assert_eq([school,records,counts],saved,kind+" input retained")
	var result := Handoff.apply(row["school"],row["records"],row["counts"],evidence["rules"])
	assert_true(result["supported"])
	result["counts"][0]["count"] = -1
	result["before_counts"].clear()
	assert_eq(row["counts"][0]["count"],0,"output does not alias counts")
