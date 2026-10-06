extends "res://sim/tests/test_base.gd"

const Move = preload("res://sim/school_student_movement.gd")
const Group = preload("res://sim/school_teacher_group_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const PATH := "res://data/school_student_movement_evidence.json"


func _data() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(PATH)))


func _case(data: Dictionary, name: String) -> Dictionary:
	for row in data["cases"]:
		if row["name"] == name:
			return row
	return {}


func _patched(before: Dictionary, changes: Dictionary) -> Dictionary:
	var after := before.duplicate(true)
	for key in changes:
		after[key] = changes[key].duplicate(true) if changes[key] is Array or changes[key] is Dictionary else changes[key]
	return after


func _authority(result: Dictionary) -> void:
	for key in ["school_initialized", "interactive_school_ready", "live_witness", "authorizes_persistent_write"]:
		assert_false(result[key])


func _move(row: Dictionary, data: Dictionary) -> Dictionary:
	return Move.move_student(row["before"], row["command"], data["declared_profiles"], data["group_rules"], data["sort_rules"])


func _reject(row: Dictionary, data: Dictionary) -> Dictionary:
	var saved := row.duplicate(true)
	var inputs := data.duplicate(true)
	var result := _move(row, data)
	assert_false(result["supported"])
	assert_false(result.has("after"))
	assert_eq(row, saved)
	assert_eq(data, inputs)
	_authority(result)
	return result


func test_all_37_native_immediate_cleanup_and_rating_checkpoints_match() -> void:
	var data := _data()
	var saved := data.duplicate(true)
	assert_eq(data["cases"].size(), 37)
	for row in data["cases"]:
		var result := _move(row, data)
		assert_true(result["supported"], row["name"] + " " + str(result.get("reason", "")))
		if not result["supported"]:
			continue
		var expected := _patched(row["before"], row["movement"]["changed_fields"])
		assert_eq(result["after"], expected, row["name"] + " immediate")
		_authority(result)
		var old: Dictionary = result["after"].duplicate(true)
		var clean := Move.reconcile(result["after"], data["group_rules"])
		assert_true(clean["supported"])
		assert_eq(result["after"], old)
		expected = _patched(expected, row["reconciliation"]["changed_fields"])
		assert_eq(clean["after"], expected, row["name"] + " cleanup")
		old = clean["after"].duplicate(true)
		var rated := Group.rate(clean["after"], data["group_rules"])
		assert_true(rated["supported"])
		assert_eq(clean["after"], old)
		expected = _patched(expected, row["rating"]["changed_fields"])
		assert_eq(rated["after"], expected, row["name"] + " rating")
		assert_eq(rated["ratings"], row["rating"]["ratings"])
		_authority(clean)
		_authority(rated)
	assert_eq(data, saved)


func test_teacherless_drop_preserves_original_outside_release_behavior() -> void:
	var data := _data()
	for mode in range(3):
		var outside := _move(_case(data, "class_outside_mode%d" % mode), data)
		var teacherless := _move(_case(data, "class_teacherless_mode%d" % mode), data)
		assert_eq(teacherless["after"], outside["after"])
		assert_true(teacherless["after"]["idle_student_ids"].has(3))
		for kind in ["waiting_outside", "waiting_teacherless"]:
			var row := _case(data, "%s_mode%d" % [kind, mode])
			var result := _move(row, data)
			assert_eq(result["after"]["idle_student_ids"], row["before"]["idle_student_ids"])
			assert_eq(result["after"]["group_raw_bytes"], row["before"]["group_raw_bytes"])


func test_stale_counts_and_source_indices_are_repaired_only_by_explicit_cleanup() -> void:
	var data := _data()
	var row := _case(data, "class_empty_mode2")
	var result := _move(row, data)
	assert_eq(result["after"]["group_raw_bytes"][14], 2)
	assert_eq(result["after"]["group_raw_bytes"][42], 1)
	assert_eq(result["after"]["derived_student_ids"][0], row["before"]["derived_student_ids"][0])
	assert_eq(result["after"]["derived_student_ids"][1], [9,-1,-1,3])
	assert_eq(result["after"]["idle_sort_mode"], 2)
	var repeated := Move.move_student(result["after"], row["command"], data["declared_profiles"], data["group_rules"], data["sort_rules"])
	assert_false(repeated["supported"])
	var clean := Move.reconcile(result["after"], data["group_rules"])
	assert_eq(clean["after"]["group_raw_bytes"][14], 1)
	assert_eq(clean["after"]["group_raw_bytes"][42], 2)
	assert_eq(clean["after"]["idle_sort_mode"], 0)
	assert_eq(Group.rate(clean["after"], data["group_rules"])["after"]["derived_student_ids"][0], [-1,4,-1,-1])


func test_bad_commands_or_changed_drag_sources_refuse_without_mutation() -> void:
	var data := _data()
	var original := _case(data, "class_exchange_mode0")
	for pair in [["kind", "teacher"], ["released", 1], ["student_id", 117], ["source_group", 5],
			["source_slot", 4], ["target_group", -2], ["target_slot", 4], ["target_slot", -1],
			["source_group", -1], ["source_slot", 1], ["student_id", 4]]:
		var row := original.duplicate(true)
		row["command"][pair[0]] = pair[1]
		_reject(row, data)
	for pair in [["drag_kind",1], ["drag_origin",0], ["drag_id",4], ["drag_slot",1],
			["drag_group",1], ["task_drag_state",3], ["drag_source_rank",8], ["idle_sort_mode",3], ["teacher_sort_mode",3]]:
		var row := original.duplicate(true)
		row["before"][pair[0]] = pair[1]
		_reject(row, data)
	var row := _case(data, "waiting_empty_mode0").duplicate(true)
	row["before"]["idle_student_ids"].reverse()
	assert_eq(_reject(row, data)["reason"], "stale_waiting_student_source")
	row = original.duplicate(true)
	Group._put_word(row["before"]["group_raw_bytes"],16,4)
	assert_eq(_reject(row, data)["reason"], "stale_class_student_source")


func test_malformed_memberships_counts_profiles_and_rules_refuse() -> void:
	var data := _data()
	var original := _case(data, "class_exchange_mode0")
	for kind in ["duplicate_wait", "missing_wait", "teacher_wait", "count", "indices", "unavailable", "teacher", "buffer"]:
		var row := original.duplicate(true)
		match kind:
			"duplicate_wait": row["before"]["idle_student_ids"].append(5)
			"missing_wait": row["before"]["idle_student_ids"].clear()
			"teacher_wait": row["before"]["idle_teacher_ids"].append(117)
			"count": row["before"]["group_raw_bytes"][14] = 3
			"indices": row["before"]["derived_student_indices"][0][0] = -1
			"unavailable": row["before"]["availability"][3] = 0
			"teacher": Group._put_word(row["before"]["group_raw_bytes"],0,-1)
			"buffer": row["before"]["group_raw_bytes"].clear()
		_reject(row, data)
	for kind in ["missing_profile", "extra_profile", "attribute", "category", "source", "group_source", "thresholds"]:
		var bad := data.duplicate(true)
		match kind:
			"missing_profile": bad["declared_profiles"].pop_back()
			"extra_profile": bad["declared_profiles"].append({"character_id":6,"job":1,"level_50":1,"attributes":[1,1,1,1,1,1,1]})
			"attribute": bad["declared_profiles"][0]["attributes"][0] = 256
			"category": bad["sort_rules"]["job_categories"][1] = 6
			"source": bad["sort_rules"]["source_image_sha256"] = "other"
			"group_source": bad["group_rules"]["chapter_sha256"] = "other"
			"thresholds": bad["group_rules"]["relationship_thresholds"][0] = 15
		_reject(original, bad)


func test_missing_new_target_relationship_refuses_before_publishing() -> void:
	var data := _data()
	var row := _case(data, "class_exchange_mode0").duplicate(true)
	row["before"]["relationships"] = row["before"]["relationships"].filter(func(pair): return not (pair["from"] == 3 and pair["to"] == 118))
	# The old classes still rate; the prospective target cannot.
	assert_true(Group.rate(row["before"], data["group_rules"])["supported"])
	assert_eq(_reject(row, data)["reason"], "missing_group_relationship")


func test_held_release_sequence_isolated_views_and_opaque_metadata() -> void:
	var data := _data()
	var row := _case(data, "class_exchange_held").duplicate(true)
	row["before"]["opaque"] = {"nested":[1.25, "unchanged"]}
	var saved := row.duplicate(true)
	var held := _move(row, data)
	assert_eq(held["status"], "held")
	assert_eq(held["after"]["selected_group"],1)
	var release: Dictionary = row["command"].duplicate()
	release["released"] = true
	var result := Move.move_student(held["after"], release, data["declared_profiles"], data["group_rules"], data["sort_rules"])
	assert_true(result["supported"])
	assert_eq(result["after"]["opaque"], row["before"]["opaque"])
	for key in ["month", "week", "global_total_511c", "student_record_sha256", "relationships"]:
		assert_eq(result["after"][key], row["before"][key])
	result["after"]["opaque"]["nested"].clear()
	result["after"]["group_raw_bytes"].clear()
	assert_eq(row, saved)
	assert_eq(held["after"]["opaque"], saved["before"]["opaque"])
	var invalid: Dictionary = held["after"].duplicate(true)
	invalid["idle_sort_mode"] = 3
	assert_false(Move.reconcile(invalid, data["group_rules"])["supported"])
