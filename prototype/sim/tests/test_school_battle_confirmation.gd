extends "res://sim/tests/test_base.gd"

const Confirmation := preload("res://sim/school_battle_confirmation.gd")
const Preparation := preload("res://sim/school_adventure_preparation.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")


func _json(path: String) -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(path)))


func _input(case_index := 0) -> Dictionary:
	var evidence := _json("res://data/school_adventure_preparation_evidence.json")
	var source: Dictionary = evidence["cases"][case_index]
	var school: Dictionary = source["before"]["school"].duplicate(true)
	var growth := []
	for identity in source["prepared"]["rounds"][0]["student_ids"]:
		var profile: Dictionary = school["member_profiles"].filter(func(p): return p["member_id"]==identity)[0]
		growth.append({"character_id":identity,"attributes":profile["attributes"].duplicate(),
			"level_50":profile["level_50"],"staged_total":100})
	return {"school":school,"records":_json("res://data/school_course_confirmation_rules.json")["initial_records"],
		"growth":growth,"counts":[{"character_id":3,"count":0},{"character_id":4,"count":0},{"character_id":9,"count":0}],
		"preparation":source["prepared"].duplicate(true),"grade":0}


func _apply(input: Dictionary) -> Dictionary:
	return Confirmation.apply(input["school"],input["records"],input["growth"],input["counts"],input["preparation"],input["grade"])


func _relation(school: Dictionary, a: int, b: int) -> int:
	return school["relationships"].filter(func(row): return row["from"]==a and row["to"]==b)[0]["value"]


func test_full_squad_teacher_and_support_both_apply_in_native_order() -> void:
	var input := _input()
	var before := input.duplicate(true)
	var result := _apply(input)
	assert_true(result["supported"],str(result.get("reason")))
	if not result["supported"]: return
	assert_eq(result["round_support_ids"],[101],"source4A6A10 support slots, not assumed from display teacher")
	assert_eq(result["relationship_calls"].size(),24)
	for row in input["school"]["relationships"]:
		assert_eq(_relation(result["after"],row["from"],row["to"]),clampi(row["value"]+4,1,100))
	assert_eq(result["relationship_calls"].slice(6,8),[{"from":3,"to":101,"delta":1},{"from":101,"to":3,"delta":1}])
	assert_eq(result["relationship_calls"].slice(18,20),[{"from":3,"to":101,"delta":3},{"from":101,"to":3,"delta":3}])
	assert_eq(result["recipient"],3,"strict greater tie keeps first group/slot")
	assert_eq(result["counts"][0]["count"],1)
	for row in result["records"]:
		assert_eq(row["week_records"].slice(12,15),[2,3,4])
	assert_eq(result["after"]["month"],4); assert_eq(result["after"]["week"],5)
	assert_eq(result["adv_request"]["state"],6); assert_eq(result["adv_request"]["next_task"],7)
	assert_eq(result["adv_request"]["chapter"],"adv/dat/chapter020.ybc")
	assert_false(result["adv_request"]["chapter_completed"]); assert_false(result["adv_request"]["week_advanced"])
	assert_eq(input,before,"pure inputs retained")
	assert_eq(_apply(input),result,"same inputs remain repeatable, caller owns once-only commit")


func test_each_relationship_call_clamps_before_the_negative_grade_call() -> void:
	var input := _input()
	for row in input["school"]["relationships"]: row["value"] = 100
	# Rating depends on relationships, so bind the new actual prepared snapshot.
	input["preparation"] = Preparation.project(input["school"],_json(Preparation.RULE_PATH))["prepared"]
	input["grade"] = 4
	var result := _apply(input)
	assert_true(result["supported"],str(result.get("reason")))
	if not result["supported"]: return
	for row in result["after"]["relationships"]: assert_eq(row["value"],99,"+1 clamps100 before -1")


func test_waiting_record_history_and_directed_relationships_remain_distinct() -> void:
	var input := _input(1)
	input["records"][2]["week_records"][13] = 8
	input["records"][2]["week_records"][14] = 9
	var result := _apply(input)
	assert_true(result["supported"],str(result.get("reason")))
	if not result["supported"]: return
	assert_eq(result["records"][2]["week_records"].slice(12,15),[3,8,9])
	assert_eq(_relation(result["after"],9,3),clampi(_relation(input["school"],9,3)-1,1,100))
	assert_eq(_relation(result["after"],3,9),_relation(input["school"],3,9))
	assert_eq(_relation(result["after"],9,101),_relation(input["school"],9,101))
	assert_eq(result["after"]["member_profiles"][3],input["school"]["member_profiles"][3],"waiting profile retained")
	assert_eq(result["relationship_calls"].size(),14)
	assert_eq(result["relationship_calls"][0],{"from":9,"to":3,"delta":-1})


func test_fifth_class_and_reordered_growth_preserve_group_identity() -> void:
	var input := _input(2)
	input["growth"][1]["staged_total"] = 200
	input["growth"][1]["attributes"][0] += 1
	input["growth"][1]["level_50"] = 10
	input["counts"][1]["count"] = 5
	var result := _apply(input)
	assert_true(result["supported"],str(result.get("reason")))
	if not result["supported"]: return
	assert_eq(result["recipient"],4); assert_eq(result["counts"][1]["count"],5)
	assert_eq(result["after"]["member_profiles"][2]["level_50"],10)
	input["growth"].reverse()
	assert_eq(_apply(input),result,"growth matched by ID rather than array position")
	result["after"]["relationships"][0]["value"] = -1
	result["records"][0]["job_progress"][1] = -1
	assert_true(input["school"]["relationships"][0]["value"] >= 0)
	assert_true(input["records"][0]["job_progress"][1] >= 0)


func test_native_byte_job_counter_wrap_and_sentinel() -> void:
	var input := _input()
	for index in range(3):
		var job: int = input["school"]["member_profiles"][index+1]["job"]
		input["records"][index]["job_progress"][job] = [99,100,127][index]
	var result := _apply(input)
	assert_true(result["supported"],str(result.get("reason")))
	if not result["supported"]: return
	for index in range(3):
		var job: int = input["school"]["member_profiles"][index+1]["job"]
		assert_eq(result["records"][index]["job_progress"][job],[99,100,0][index])


func test_incomplete_or_conflicting_inputs_produce_no_partial_publication() -> void:
	for kind in ["date","teacher","support","roster","relation_missing","relation_duplicate","record","growth","npc","zero_mvp","count","grade"]:
		var input := _input()
		match kind:
			"date": input["school"]["week"] = 4
			"teacher": input["school"]["teacher_ids"][0] = 102
			"support": input["preparation"]["rounds"][0]["teacher_ids"] = []
			"roster": input["preparation"]["rounds"][0]["student_ids"] = [3,4]
			"relation_missing": input["school"]["relationships"].pop_back()
			"relation_duplicate": input["school"]["relationships"][1] = input["school"]["relationships"][0].duplicate()
			"record": input["records"][0]["week_records"].pop_back()
			"growth": input["growth"].pop_back()
			"npc": input["growth"][0]["character_id"] = 5
			"zero_mvp":
				for row in input["growth"]: row["staged_total"] = 0
			"count": input["counts"][0]["count"] = 6
			"grade": input["grade"] = 5
		var before := input.duplicate(true)
		var result := _apply(input)
		assert_false(result["supported"],kind)
		assert_false(result.has("after"),kind+" no partial after")
		assert_eq(input,before,kind+" input preserved")
