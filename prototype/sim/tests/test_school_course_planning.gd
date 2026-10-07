extends "res://sim/tests/test_base.gd"

const Planning = preload("res://sim/school_course_planning.gd")
const Origin = preload("res://sim/new_game_school_origin.gd")
const Group = preload("res://sim/school_teacher_group_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _data() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_planning_evidence_v2.json")))


func _operate(row: Dictionary, rules: Dictionary) -> Dictionary:
	var command: Dictionary = row["command"]
	if command["kind"] == "mode":
		return Planning.set_mode(row["before"],command["group"],command["teaching"],Origin.group_rules(),rules)
	return Planning.select_course(row["before"],command,Origin.group_rules(),rules)


func test_all_native_modes_valid_clicks_hover_categories_and_ratings() -> void:
	var data := _data()
	var saved := data.duplicate(true)
	assert_eq(data["cases"].size(),15)
	for row in data["cases"]:
		if row["name"] in ["empty_category","adventure_click_ignored"]:
			assert_false(_operate(row,data["work_rules"])["supported"])
			assert_false(row["operation"]["changed_fields"].has("group_raw_bytes"))
			continue
		var result := _operate(row,data["work_rules"])
		assert_true(result["supported"],row["name"] + " " + str(result.get("reason","")))
		if not result["supported"]:
			continue
		var expected: Dictionary = row["before"].duplicate(true)
		for key in row["operation"]["changed_fields"]:
			expected[key] = row["operation"]["changed_fields"][key]
		assert_eq(result["after"],expected,row["name"] + " operation")
		var rated := Group.rate(result["after"],Origin.group_rules())
		for key in row["rating"]["changed_fields"]:
			expected[key] = row["rating"]["changed_fields"][key]
		assert_eq(rated.get("after"),expected,row["name"] + " rating")
		assert_eq(rated.get("ratings"),row["rating"]["ratings"])
		assert_false(result["live_witness"])
		assert_false(result["authorizes_persistent_write"])
	assert_eq(data,saved)


func test_stale_rows_controls_view_and_teacherless_refuse_without_mutation() -> void:
	var data := _data()
	for mutation in range(6):
		var row: Dictionary = data["cases"][1].duplicate(true)
		if mutation == 0:
			row["command"]["row"] = 9
		elif mutation == 1:
			row["before"]["course_category"] = 1
		elif mutation == 2:
			row["command"]["page"] = 1
		elif mutation == 3:
			row["before"]["teacher_work_records"]["101"][0]["blocked"] = 1
		elif mutation == 4:
			row["command"]["group"] = 1
			row["before"]["selected_group"] = 1
		else:
			row["command"]["clicked"] = 1
		var saved: Dictionary = row.duplicate(true)
		var result := _operate(row,data["work_rules"])
		assert_false(result["supported"])
		assert_false(result.has("after"))
		assert_eq(row,saved)
	var before: Dictionary = data["cases"][0]["before"]
	assert_false(Planning.set_mode(before,1,true,Origin.group_rules(),data["work_rules"])["supported"])
	assert_false(Planning.set_mode(before,0.0,true,Origin.group_rules(),data["work_rules"])["supported"])


func test_changed_source_rules_and_immediate_operation_ownership() -> void:
	var data := _data()
	var row: Dictionary = data["cases"][1]
	var rules: Dictionary = data["work_rules"].duplicate(true)
	rules["templates"][0]["sort_key"] += 1
	assert_false(_operate(row,rules)["supported"])
	var old: Dictionary = row["before"].duplicate(true)
	var result := _operate(row,data["work_rules"])
	result["after"]["group_raw_bytes"].clear()
	assert_eq(row["before"],old)
