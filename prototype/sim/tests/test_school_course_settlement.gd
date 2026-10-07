extends "res://sim/tests/test_base.gd"

const Settlement = preload("res://sim/school_course_settlement.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func evidence() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_settlement_evidence_v1.json")))


func work_rules() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/new_game_school_rules.json")))["work_rules"]


func test_native_packets_records_and_rng() -> void:
	var data := evidence()
	for row in data["cases"]:
		var before: Dictionary = row["before"].duplicate(true)
		var records: Array = row["before_records"].duplicate(true)
		var result := Settlement.settle(before,records,data["rules"],work_rules(),row["declared_clock_seed"])
		assert_true(result["supported"],row["name"] + " supported " + str(result.get("reason")))
		if not result["supported"]:
			continue
		for key in ["packets","learning_draws","rand_state","bonus","skill_display_needed"]:
			assert_eq(result[key],row[key],row["name"] + " " + key)
		assert_eq(result["records"],row["after_records"],row["name"] + " complete records")
		assert_eq(result["global_total_511c"],row["after"]["global_total_511c"],row["name"] + " global bonus")
		assert_eq(before,row["before"],"pure school input")
		assert_eq(records,row["before_records"],"pure growth input")


func test_origin_records_and_runtime_rules() -> void:
	var source: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/new_game_school_rules.json")))
	var rules: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_settlement_rules.json")))
	var initial := Settlement.initial_records(source["origin_rules"],rules)
	assert_true(initial["supported"])
	assert_eq(initial["records"],evidence()["cases"][0]["before_records"],"origin-derived source growth records")
	assert_eq(Settlement.source_subset(rules),evidence()["rules"],"runtime contains only source rules")
	assert_true(Settlement.valid_rules(rules))


func test_refusals_are_atomic_and_results_owned() -> void:
	var data := evidence()
	var row: Dictionary = data["cases"][0]
	for kind in ["rules","shape","missing","pool","identity","profile","adventure","unavailable","seed","buffers"]:
		var before: Dictionary = row["before"].duplicate(true)
		var records: Array = row["before_records"].duplicate(true)
		var rules: Dictionary = data["rules"].duplicate(true)
		var seed: Variant = 4660
		match kind:
			"rules": rules["training"][12]["package"][0] += 1
			"shape": rules["training"][12]["renamed"] = rules["training"][12]["package"]; rules["training"][12].erase("package")
			"missing": records.pop_back()
			"pool": records[0]["growth_pools"][0] = -1
			"identity": records[0]["character_id"] = 4
			"profile": before["member_profiles"][1]["attributes"][0] += 1
			"adventure": before["group_raw_bytes"][3] = 0
			"unavailable": before["course_buffers"][0].clear()
			"seed": seed = 4660.0
			"buffers": before["course_buffers"][0][0] = []
		var original := {"before":before.duplicate(true),"records":records.duplicate(true)}
		var result := Settlement.settle(before,records,rules,work_rules(),seed)
		assert_false(result["supported"],kind)
		assert_false(result.has("records"),kind + " no partial result")
		assert_eq(before,original["before"],kind + " preserves school")
		assert_eq(records,original["records"],kind + " preserves growth")
	var owned := Settlement.settle(row["before"],row["before_records"],data["rules"],work_rules())
	assert_true(owned["supported"])
	if owned["supported"]:
		owned["records"][0]["growth_pools"][0] = -1
		assert_true(row["before_records"][0]["growth_pools"][0] >= 0,"output is deep-owned")
