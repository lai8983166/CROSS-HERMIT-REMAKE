extends "res://sim/tests/test_base.gd"

const Courses := preload("res://sim/school_course_unlocking.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const DATA := "res://data/school_course_unlock_evidence.json"


func _data() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(DATA)))


func _case(data: Dictionary, name: String) -> Dictionary:
	for row in data["cases"]:
		if row["name"] == name:
			return row
	return {}


func _authority(result: Dictionary) -> void:
	for key in ["school_initialized","interactive_school_ready","live_witness","authorizes_persistent_write"]:
		assert_false(result[key])


func _reject(before: Dictionary, rules: Dictionary, reason := "") -> void:
	var saved := before.duplicate(true)
	var saved_rules := rules.duplicate(true)
	var result := Courses.unlock_courses(before,rules)
	assert_false(result["supported"])
	assert_false(result.has("after"))
	if not reason.is_empty():
		assert_eq(result["reason"],reason)
	assert_eq(before,saved)
	assert_eq(rules,saved_rules)
	_authority(result)


func test_all_15_native_cases_and_every_continuous_checkpoint() -> void:
	var data := _data()
	var saved := data.duplicate(true)
	assert_eq(data["cases"].size(),15)
	for row in data["cases"]:
		var expected: Dictionary = row["before"].duplicate(true)
		var actual: Dictionary = expected.duplicate(true)
		for step in row["steps"]:
			if step.has("declared_date"):
				for state in [expected,actual]:
					state["month"] = step["declared_date"][0]
					state["week"] = step["declared_date"][1]
			var old := actual.duplicate(true)
			var result := Courses.unlock_courses(actual,data["rules"])
			assert_true(result["supported"],row["name"])
			assert_eq(actual,old)
			for key in step["changed_fields"]:
				expected[key] = step["changed_fields"][key].duplicate(true)
			assert_eq(result.get("after"),expected,row["name"])
			if result.has("after"):
				actual = result["after"]
			_authority(result)
	assert_eq(data,saved)


func test_exact_capacity_success_and_whole_operation_overflow_refusal() -> void:
	var data := _data()
	var before: Dictionary = _case(data,"capacity_exact_100")["before"].duplicate(true)
	var result := Courses.unlock_courses(before,data["rules"])
	assert_true(result["supported"])
	assert_eq(result["after"]["course_counts"][16],100)
	for count in [98,99,100]:
		before["course_counts"][16] = count
		_reject(before,data["rules"],"course_capacity_exceeded")
	# At a later date, teacher101 would change before teacher117 overflows.
	before["month"] = 5
	before["week"] = 1
	_reject(before,data["rules"],"course_capacity_exceeded")


func test_source_rules_reject_wrong_hash_or_any_template_change() -> void:
	var data := _data()
	var before: Dictionary = data["cases"][0]["before"]
	for kind in ["source","hash","missing","order","id","month","week","metadata","category","key","mask","mask_size","boolean","float"]:
		var rules: Dictionary = data["rules"].duplicate(true)
		match kind:
			"source": rules["source_image_sha256"] = "other"
			"hash": rules["template_fields_sha256"] = "other"
			"missing": rules["templates"].pop_back()
			"order": rules["templates"].reverse()
			"id": rules["templates"][0]["work_id"] = 2
			"mask": rules["templates"][0]["teacher_mask"][0] = 0
			"mask_size": rules["templates"][0]["teacher_mask"].pop_back()
			"boolean": rules["templates"][0]["metadata"] = true
			"float": rules["templates"][0]["metadata"] = 1.0
			_: rules["templates"][0][kind] += 1
		_reject(before,rules,"unsupported_course_rules")


func test_malformed_state_dates_flags_counts_and_buffers_refuse() -> void:
	var data := _data()
	var original: Dictionary = _case(data,"existing_progress_and_physical_opaque")["before"]
	for kind in ["missing","month","week","float","boolean","flags_size","flag","flag_bool","counts_size","count","count_float","buffers_size","buffer","row_size","slot","duplicate","order","byte","word","opaque","zero"]:
		var before := original.duplicate(true)
		match kind:
			"missing": before.erase("course_buffers")
			"month": before["month"] = -1
			"week": before["week"] = 6
			"float": before["month"] = 4.0
			"boolean": before["week"] = true
			"flags_size": before["course_unlocked_flags"].pop_back()
			"flag": before["course_unlocked_flags"][1] = 256
			"flag_bool": before["course_unlocked_flags"][1] = false
			"counts_size": before["course_counts"].pop_back()
			"count": before["course_counts"][0] = 101
			"count_float": before["course_counts"][0] = 0.0
			"buffers_size": before["course_buffers"].pop_back()
			"buffer": before["course_buffers"][0] = {}
			"row_size": before["course_buffers"][16][0].pop_back()
			"slot": before["course_buffers"][16][0][0] = 100
			"duplicate": before["course_buffers"][16].append(before["course_buffers"][16][0].duplicate())
			"order": before["course_buffers"][16].reverse()
			"byte": before["course_buffers"][16][0][1] = -1
			"word": before["course_buffers"][16][0][5] = 32768
			"opaque": before["course_buffers"][16][0][7] = true
			"zero": before["course_buffers"][0] = [[0,0,0,0,0,0,0,0]]
		_reject(before,data["rules"],"invalid_course_state")


func test_physical_opaque_tail_progress_and_nonboolean_record_flags() -> void:
	var data := _data()
	var before: Dictionary = _case(data,"existing_progress_and_physical_opaque")["before"]
	var result := Courses.unlock_courses(before,data["rules"])
	var rows: Array = result["after"]["course_buffers"][16]
	assert_eq(rows[3].slice(1,6),[2,3,22,-7,123])
	assert_eq(rows[4].slice(1,6),[1,0,13,9,45])
	for slot in range(6):
		assert_eq(rows[slot].slice(6),[70+slot,90+slot])
	assert_eq(rows[5].slice(1,6),[0,0,0,0,0])


func test_unavailable_teachers_empty_masks_and_nonzero_flags() -> void:
	var data := _data()
	var result := Courses.unlock_courses(_case(data,"date_0_0")["before"],data["rules"])
	assert_eq(result["after"]["course_counts"],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
	assert_true(result["unlocked_work_ids"].has(100))
	assert_false(result["unlocked_work_ids"].has(32))
	result = Courses.unlock_courses(_case(data,"nonzero_flags_skip")["before"],data["rules"])
	assert_false(result["unlocked_work_ids"].has(1))
	assert_false(result["unlocked_work_ids"].has(2))
	assert_false(result["unlocked_work_ids"].has(14))
	assert_eq(result["after"]["teacher_count"],0)
	assert_eq(result["after"]["course_counts"][16],2)


func test_input_rule_output_isolation_metadata_and_repeat_status() -> void:
	var data := _data()
	var before: Dictionary = _case(data,"date_5_1")["before"].duplicate(true)
	before["opaque_metadata"] = {"nested":[1.25,"keep"]}
	before["work_rows"] = [[[5,99,0]],[],[]]
	var saved := before.duplicate(true)
	var saved_rules: Dictionary = data["rules"].duplicate(true)
	var result := Courses.unlock_courses(before,data["rules"])
	assert_true(result["supported"])
	assert_eq(result["after"]["opaque_metadata"],before["opaque_metadata"])
	assert_eq(result["after"]["work_rows"],before["work_rows"])
	assert_eq(result["after"]["month"],5)
	assert_eq(result["after"]["week"],1)
	var repeated := Courses.unlock_courses(result["after"],data["rules"])
	assert_eq(repeated["reason"],"unchanged")
	assert_eq(repeated["unlocked_work_ids"],[])
	assert_eq(repeated["after"],result["after"])
	result["after"]["opaque_metadata"]["nested"].clear()
	result["after"]["course_buffers"][0].clear()
	result["after"]["work_rows"].clear()
	result["unlocked_work_ids"].clear()
	assert_eq(before,saved)
	assert_eq(data["rules"],saved_rules)
	assert_false(repeated["after"]["course_buffers"][0].is_empty())
