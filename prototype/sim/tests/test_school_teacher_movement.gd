extends "res://sim/tests/test_base.gd"

const Teacher = preload("res://sim/school_teacher_movement.gd")
const Group = preload("res://sim/school_teacher_group_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const PATH := "res://data/school_teacher_movement_evidence.json"


func _data() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(PATH)))


func _case(data: Dictionary, name: String, collection := "cases") -> Dictionary:
	for row in data[collection]:
		if row["name"] == name:
			return row
	return {}


func _patch(before: Dictionary, changes: Dictionary) -> Dictionary:
	var result := before.duplicate(true)
	for key in changes:
		result[key] = changes[key].duplicate(true) if changes[key] is Array or changes[key] is Dictionary else changes[key]
	return result


func _move(row: Dictionary, data: Dictionary) -> Dictionary:
	return Teacher.move_teacher(row["before"],row["command"],data["declared_student_profiles"],data["group_rules"],data["sort_rules"],data["work_rules"])


func _authority(result: Dictionary) -> void:
	for key in ["school_initialized","interactive_school_ready","live_witness","authorizes_persistent_write"]:
		assert_false(result[key])


func _reject(row: Dictionary, data: Dictionary) -> Dictionary:
	var saved := row.duplicate(true)
	var inputs := data.duplicate(true)
	var result := _move(row,data)
	assert_false(result["supported"])
	assert_false(result.has("after"))
	assert_eq(row,saved)
	assert_eq(data,inputs)
	_authority(result)
	return result


func test_all_52_native_teacher_movement_cleanup_and_rating_checkpoints() -> void:
	var data := _data()
	var saved := data.duplicate(true)
	assert_eq(data["cases"].size(),52)
	for row in data["cases"]:
		var result := _move(row,data)
		assert_true(result["supported"],row["name"] + " " + str(result.get("reason","")))
		if not result["supported"]:
			continue
		var expected := _patch(row["before"],row["movement"]["changed_fields"])
		assert_eq(result["after"],expected,row["name"] + " immediate")
		_authority(result)
		var old: Dictionary = result["after"].duplicate(true)
		var clean := Teacher.reconcile(result["after"],data["group_rules"],data["work_rules"])
		assert_true(clean["supported"],row["name"] + " cleanup " + str(clean.get("reason","")))
		if not clean["supported"]:
			continue
		assert_eq(result["after"],old)
		expected = _patch(expected,row["reconciliation"]["changed_fields"])
		assert_eq(clean["after"],expected,row["name"] + " cleanup")
		old = clean["after"].duplicate(true)
		var rated := Group.rate(clean["after"],data["group_rules"])
		assert_true(rated["supported"])
		assert_eq(clean["after"],old)
		expected = _patch(expected,row["rating"]["changed_fields"])
		assert_eq(rated["after"],expected,row["name"] + " rating")
		assert_eq(rated["ratings"],row["rating"]["ratings"])
		_authority(clean)
		_authority(rated)
	assert_eq(data,saved)


func test_all_11_work_selection_cases_and_sparse_slot_order() -> void:
	var data := _data()
	assert_eq(data["selections"].size(),11)
	for row in data["selections"]:
		var old: Dictionary = row["before"].duplicate(true)
		var selected := Teacher.select_group(row["before"],row["group"],data["group_rules"],data["work_rules"])
		assert_true(selected["supported"],row["name"])
		assert_eq(selected["after"],_patch(row["before"],row["selection"]["changed_fields"]),row["name"])
		assert_eq(row["before"],old)
		_authority(selected)
	var row := _case(data,"mixed_active","selections")
	var before: Dictionary = row["before"].duplicate(true)
	before["teacher_work_records"]["117"].reverse()
	var selected := Teacher.select_group(before,0,data["group_rules"],data["work_rules"])
	assert_eq(selected["after"]["work_rows"],[[[1,2,0],[0,1,1]],[[6,7,0]],[[8,9,0]]])
	assert_eq(selected["after"]["work_counts"],[2,1,1])


func test_work_source_rules_and_teacher_sort_templates_cannot_be_altered() -> void:
	var data := _data()
	var row := _case(data,"class_exchange_mode0_gate0")
	for kind in ["source","hash","category","key","order","teacher_job","teacher_level","teacher_attribute","teacher_id"]:
		var bad := data.duplicate(true)
		match kind:
			"source": bad["work_rules"]["source_image_sha256"] = "other"
			"hash": bad["work_rules"]["template_fields_sha256"] = "other"
			"category": bad["work_rules"]["templates"][0]["category"] = 1
			"key": bad["work_rules"]["templates"][0]["sort_key"] = 10
			"order": bad["work_rules"]["templates"].reverse()
			"teacher_job": bad["work_rules"]["teacher_profiles"][0]["job"] = 2
			"teacher_level": bad["work_rules"]["teacher_profiles"][0]["level_50"] = 1
			"teacher_attribute": bad["work_rules"]["teacher_profiles"][0]["attributes"][0] = 1
			"teacher_id": bad["work_rules"]["teacher_profiles"][0]["teacher_id"] = 101
		_reject(row,bad)


func test_bad_teacher_commands_stale_sources_and_catalogs_refuse_without_mutation() -> void:
	var data := _data()
	var original := _case(data,"class_exchange_mode0_gate0")
	for pair in [["kind","student"],["teacher_id",101],["released",1],["source_group",5],
			["source_group",-1],["source_slot",0],["target_group",5],["target_group",0.5],["teacher_id",118]]:
		var row := original.duplicate(true)
		row["command"][pair[0]] = pair[1]
		_reject(row,data)
	for kind in ["drag","count","derived","student_wait","teacher_wait","available","teacher","sort"]:
		var row := original.duplicate(true)
		match kind:
			"drag": row["before"]["drag_kind"] = 0
			"count": row["before"]["group_raw_bytes"][14] = 3
			"derived": row["before"]["derived_teacher_ids"][0] = 118
			"student_wait": row["before"]["idle_student_ids"].append(3)
			"teacher_wait": row["before"]["idle_teacher_ids"].append(117)
			"available": row["before"]["availability"][117] = 0
			"teacher": Group._put_word(row["before"]["group_raw_bytes"],0,118)
			"sort": row["before"]["teacher_sort_mode"] = 3
		_reject(row,data)
	var row := _case(data,"waiting_replace_mode0_gate0").duplicate(true)
	row["before"]["idle_teacher_ids"] = [117]
	assert_eq(_reject(row,data)["reason"],"stale_waiting_teacher_source")
	var bad := data.duplicate(true)
	bad["declared_student_profiles"].pop_back()
	_reject(original,bad)


func test_invalid_work_records_and_view_buffers_refuse_all_operations() -> void:
	var data := _data()
	var original := _case(data,"class_exchange_mode0_gate0")
	for kind in ["missing","duplicate","slot","enabled","blocked","unknown","inactive_template","counts","pages","rows","ordinal","key"]:
		var row := original.duplicate(true)
		match kind:
			"missing": row["before"]["teacher_work_records"].erase("118")
			"duplicate": row["before"]["teacher_work_records"]["117"].append(row["before"]["teacher_work_records"]["117"][0].duplicate())
			"slot": row["before"]["teacher_work_records"]["117"][0]["slot"] = 100
			"enabled": row["before"]["teacher_work_records"]["117"][0]["enabled"] = true
			"blocked": row["before"]["teacher_work_records"]["117"][0]["blocked"] = 2
			"unknown": row["before"]["teacher_work_records"]["117"][0]["work_id"] = 0
			"inactive_template": row["before"]["teacher_work_records"]["117"][0]["work_id"] = 32
			"counts": row["before"]["work_counts"][0] = 101
			"pages": row["before"]["work_pages"][0] = 1
			"rows": row["before"]["work_rows"][0].clear()
			"ordinal": row["before"]["work_rows"][0][0][2] = 1
			"key": row["before"]["work_rows"][0][0][0] = 20
		_reject(row,data)
		var old: Dictionary = row["before"].duplicate(true)
		assert_false(Teacher.select_group(row["before"],0,data["group_rules"],data["work_rules"])["supported"])
		assert_false(Teacher.reconcile(row["before"],data["group_rules"],data["work_rules"])["supported"])
		assert_eq(row["before"],old)
	for group in [-2,5,true,0.5,"0",null]:
		assert_false(Teacher.select_group(original["before"],group,data["group_rules"],data["work_rules"])["supported"])


func test_teacher_student_return_and_stale_work_view_are_not_implicitly_repaired() -> void:
	var data := _data()
	var row := _case(data,"class_empty_mode2_gate0")
	var result := _move(row,data)
	assert_eq(result["after"]["idle_student_ids"],[9,5,3,4])
	assert_eq(result["after"]["group_raw_bytes"][14],2)
	assert_eq(result["after"]["derived_student_ids"][0],row["before"]["derived_student_ids"][0])
	row = _case(data,"class_outside_no_teacher_mode0_gate0")
	result = _move(row,data)
	var clean := Teacher.reconcile(result["after"],data["group_rules"],data["work_rules"])
	assert_eq(clean["after"]["selected_group"],row["before"]["selected_group"])
	assert_eq(clean["after"]["work_rows"],row["before"]["work_rows"])
	var cleared := Teacher.select_group(clean["after"],-1,data["group_rules"],data["work_rules"])
	assert_eq(cleared["after"]["work_rows"],[[],[],[]])
	assert_eq(cleared["after"]["work_counts"],[0,0,0])


func test_held_to_release_and_independent_metadata_views() -> void:
	var data := _data()
	var row := _case(data,"class_exchange_held").duplicate(true)
	row["before"]["opaque"] = {"nested":[1.25,"untouched"]}
	var saved := row.duplicate(true)
	var held := _move(row,data)
	assert_eq(held["status"],"held")
	assert_eq(held["after"]["selected_group"],row["before"]["selected_group"])
	var command: Dictionary = row["command"].duplicate()
	command["released"] = true
	var result := Teacher.move_teacher(held["after"],command,data["declared_student_profiles"],data["group_rules"],data["sort_rules"],data["work_rules"])
	assert_true(result["supported"])
	assert_eq(result["after"]["opaque"],row["before"]["opaque"])
	for key in ["month","week","global_total_511c","student_record_sha256","teacher_work_record_sha256","relationships"]:
		assert_eq(result["after"][key],row["before"][key])
	result["after"]["opaque"]["nested"].clear()
	result["after"]["teacher_work_records"]["117"].clear()
	result["after"]["work_rows"][0].clear()
	assert_eq(row,saved)
	assert_eq(held["after"]["opaque"],saved["before"]["opaque"])
