extends "res://sim/tests/test_base.gd"

const Origin = preload("res://sim/new_game_school_origin.gd")
const Group = preload("res://sim/school_teacher_group_replay.gd")
const Student = preload("res://sim/school_student_movement.gd")
const Teacher = preload("res://sim/school_teacher_movement.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _data() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/new_game_school_movement_evidence.json")))


func _profiles(snapshot: Dictionary) -> Array:
	var result := []
	for profile in snapshot["member_profiles"]:
		if profile["member_id"] < 101:
			result.append({"character_id":profile["member_id"],"job":profile["job"],"level_50":profile["level_50"],"attributes":profile["attributes"].duplicate()})
	return result


func _move(row: Dictionary, data: Dictionary) -> Dictionary:
	if row["command"]["kind"] == "teacher":
		return Teacher.move_teacher(row["before"],row["command"],_profiles(row["before"]),Origin.group_rules(),data["sort_rules"],data["work_rules"])
	return Student.move_student(row["before"],row["command"],_profiles(row["before"]),Origin.group_rules(),data["sort_rules"])


func test_continuous_native101_and_source_student_phases() -> void:
	var data := _data()
	var saved := data.duplicate(true)
	assert_eq(data["cases"].size(),20)
	for row in data["cases"]:
		var moved := _move(row,data)
		assert_true(moved["supported"],row["name"] + " " + str(moved.get("reason","")))
		if not moved["supported"]:
			continue
		var expected: Dictionary = row["before"].duplicate(true)
		for key in row["phases"][0]["changed_fields"]:
			expected[key] = row["phases"][0]["changed_fields"][key]
		assert_eq(moved["after"],expected,row["name"] + " move")
		var clean := Teacher.reconcile(moved["after"],Origin.group_rules(),data["work_rules"])
		assert_true(clean["supported"],row["name"] + " cleanup")
		if not clean["supported"]:
			continue
		for key in row["phases"][1]["changed_fields"]:
			expected[key] = row["phases"][1]["changed_fields"][key]
		assert_eq(clean["after"],expected,row["name"] + " cleanup")
		var rated := Group.rate(clean["after"],Origin.group_rules())
		assert_true(rated["supported"])
		for key in row["phases"][2]["changed_fields"]:
			expected[key] = row["phases"][2]["changed_fields"][key]
		assert_eq(rated.get("after"),expected,row["name"] + " rate")
		assert_eq(rated.get("ratings"),row["phases"][2]["ratings"])
		for result in [moved,clean,rated]:
			assert_false(result["authorizes_persistent_write"])
			assert_false(result["live_witness"])
	assert_eq(data,saved)


func test_teacher101_requires_origin_fingerprint_and_static_profile() -> void:
	var data := _data()
	var row: Dictionary = data["cases"][5].duplicate(true)
	for mutation in range(4):
		var rules: Dictionary = data["work_rules"].duplicate(true)
		if mutation == 0:
			rules.erase("origin_fields_sha256")
		elif mutation == 1:
			rules["teacher_profiles"][0]["attributes"][0] = 0
		elif mutation == 2:
			rules["teacher_profiles"][0]["teacher_id"] = 117
		else:
			rules["templates"][0]["sort_key"] += 1
		var before: Dictionary = row["before"].duplicate(true)
		var result := Teacher.move_teacher(before,row["command"],_profiles(before),Origin.group_rules(),data["sort_rules"],rules)
		assert_false(result["supported"])
		assert_false(result.has("after"))
		assert_eq(before,row["before"])


func test_origin_domain_rejects_other_teacher_drag_identity() -> void:
	var data := _data()
	var row: Dictionary = data["cases"][5].duplicate(true)
	row["command"]["teacher_id"] = 117
	row["before"]["drag_id"] = 117
	var result := _move(row,data)
	assert_false(result["supported"])
	assert_eq(result["reason"],"invalid_teacher_drag_control")
