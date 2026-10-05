extends "res://sim/tests/test_base.gd"

const Group = preload("res://sim/school_teacher_group_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const PATH := "res://data/school_teacher_group_evidence.json"


func _data() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(PATH)))


func _case(data: Dictionary, name: String) -> Dictionary:
	for row in data["cases"]:
		if row["name"] == name:
			return row
	return {}


func _authority(result: Dictionary) -> void:
	for key in ["school_initialized", "interactive_school_ready", "live_witness", "authorizes_persistent_write"]:
		assert_false(result[key])


func _reject(snapshot: Dictionary, rules: Dictionary, reason := "") -> void:
	var old := snapshot.duplicate(true)
	var result := Group.reconcile(snapshot, rules)
	assert_false(result["supported"], reason)
	assert_false(result.has("after"))
	assert_eq(snapshot, old)
	_authority(result)


func test_all_26_native_join_cleanup_and_rating_checkpoints_match() -> void:
	var data := _data()
	assert_eq(data["cases"].size(), 26)
	for row in data["cases"]:
		var current: Dictionary = row["before"].duplicate(true)
		var pristine := current.duplicate(true)
		var context: Dictionary = row["join_context"]
		if context["kind"] != "none":
			var joined := Group.register_teacher(current, context, data["rules"])
			assert_true(joined["supported"], row["name"])
			if not joined["supported"]:
				continue
			assert_eq(joined["after"], row["after_join_once"], row["name"] + " join")
			assert_eq(current, pristine)
			_authority(joined)
			current = joined["after"]
			if context["duplicate"]:
				var old := current.duplicate(true)
				joined = Group.register_teacher(current, context, data["rules"])
				assert_true(joined["supported"])
				assert_eq(current, old)
				current = joined["after"]
		assert_eq(current, row["after_join"], row["name"] + " repeated join")
		var old := current.duplicate(true)
		var cleaned := Group.reconcile(current, data["rules"])
		assert_true(cleaned["supported"], row["name"])
		if not cleaned["supported"]:
			continue
		assert_eq(cleaned["after"], row["after_reconcile"], row["name"] + " cleanup")
		assert_eq(current, old)
		_authority(cleaned)
		old = cleaned["after"].duplicate(true)
		var rated := Group.rate(cleaned["after"], data["rules"])
		assert_true(rated["supported"], row["name"])
		if not rated["supported"]:
			continue
		assert_eq(rated["after"], row["after_ratings"], row["name"] + " derived fields")
		assert_eq(cleaned["after"], old)
		assert_eq(rated["ratings"], row["ratings"].map(func(item): return item["defined"]), row["name"] + " ratings")
		_authority(rated)


func test_source_rules_and_join_context_are_bounded() -> void:
	var data := _data()
	var row := _case(data, "chapter012_teacher_duplicate")
	for pair in [["source_image_sha256", "other"], ["chapter_sha256", "other"], ["teacher_id", 118],
			["script_file_offset", 21], ["opcode", 145], ["relationship_thresholds", [16,31,46,61,76,90]]]:
		var bad: Dictionary = data["rules"].duplicate(true)
		bad[pair[0]] = pair[1]
		_reject(row["before"], bad)
		assert_false(Group.register_teacher(row["before"], row["join_context"], bad)["supported"])
		assert_false(Group.rate(row["before"], bad)["supported"])
	for pair in [["kind", "live"], ["teacher_id", 118], ["teacher_id", true], ["group", 5],
			["group", 0.5], ["group", 0], ["slot", 0]]:
		var context: Dictionary = row["join_context"].duplicate(true)
		context[pair[0]] = pair[1]
		var before: Dictionary = row["before"].duplicate(true)
		var pristine := before.duplicate(true)
		var result := Group.register_teacher(before, context, data["rules"])
		assert_false(result["supported"])
		assert_false(result.has("after"))
		assert_eq(before, pristine)
		_authority(result)


func test_registration_does_not_move_available_teacher_or_overwrite_occupied_group() -> void:
	var data := _data()
	var context := {"kind": "direct_helper", "teacher_id": 117, "group": 1, "slot": -1}
	var row := _case(data, "teacher_already_available")
	var result := Group.register_teacher(row["before"], context, data["rules"])
	assert_true(result["supported"])
	assert_eq(result["status"], "already_available")
	assert_eq(result["after"], row["before"])
	row = _case(data, "chapter012_teacher_duplicate")
	var before: Dictionary = row["before"].duplicate(true)
	Group._put_word(before["group_raw_bytes"], 28, 118)
	var old := before.duplicate(true)
	result = Group.register_teacher(before, context, data["rules"])
	assert_false(result["supported"])
	assert_eq(result["reason"], "outside_empty_teacher_placement")
	assert_eq(before, old)


func test_malformed_rosters_buffers_and_controls_refuse_before_mutation() -> void:
	var data := _data()
	var row := _case(data, "teacher_only")
	for pair in [["availability", []], ["group_raw_bytes", []], ["student_count", 13], ["teacher_count", 3],
			["student_ids", []], ["reset_groups", 2], ["adventure_gate", -1], ["lecture_active", true],
			["selected_group", 5], ["lecture_work_fields", [1,2,3]], ["derived_student_ids", []],
			["derived_teacher_ids", [101,-1,-1,-1,-1]], ["idle_teacher_ids", [120]], ["relationships", null]]:
		var bad: Dictionary = row["before"].duplicate(true)
		bad[pair[0]] = pair[1]
		_reject(bad, data["rules"], str(pair[0]))
	for kind in ["tail", "duplicate", "unsupported_teacher", "availability", "raw_teacher", "raw_student", "mode", "byte"]:
		var bad: Dictionary = row["before"].duplicate(true)
		match kind:
			"tail": bad["student_ids"][19] = 3
			"duplicate": bad["student_ids"][1] = bad["student_ids"][0]
			"unsupported_teacher": bad["teacher_ids"][0] = 101
			"availability": bad["availability"][3] = 0
			"raw_teacher": Group._put_word(bad["group_raw_bytes"], 28, 117)
			"raw_student": Group._put_word(bad["group_raw_bytes"], 16, 13)
			"mode": bad["group_raw_bytes"][3] = 2
			"byte": bad["group_raw_bytes"][2] = 256
		_reject(bad, data["rules"], kind)


func test_rating_requires_reconciled_members_and_complete_directed_relationships() -> void:
	var data := _data()
	for name in ["unavailable_teacher_clears_group", "teacherless_students_clear", "unavailable_student_clears", "duplicate_student_first_wins"]:
		var row := _case(data, name)
		var before: Dictionary = row["before"].duplicate(true)
		var old := before.duplicate(true)
		var result := Group.rate(before, data["rules"])
		assert_false(result["supported"], name)
		assert_eq(result["reason"], "pending_group_reconciliation")
		assert_eq(before, old)
	var row := _case(data, "asymmetric_relationship_mean")
	var bad: Dictionary = row["after_reconcile"].duplicate(true)
	bad["relationships"] = bad["relationships"].filter(func(pair): return not (pair["from"] == 117 and pair["to"] == 3))
	var old := bad.duplicate(true)
	var result := Group.rate(bad, data["rules"])
	assert_false(result["supported"])
	assert_eq(result["reason"], "missing_group_relationship")
	assert_eq(bad, old)
	for kind in ["duplicate", "range", "self", "unknown"]:
		bad = row["after_reconcile"].duplicate(true)
		match kind:
			"duplicate": bad["relationships"].append(bad["relationships"][0].duplicate())
			"range": bad["relationships"][0]["value"] = 101
			"self": bad["relationships"][0]["to"] = bad["relationships"][0]["from"]
			"unknown": bad["relationships"][0]["from"] = 120
		_reject(bad, data["rules"])
		assert_false(Group.rate(bad, data["rules"])["supported"])


func test_undefined_work_words_are_excluded_and_directional_average_is_used() -> void:
	var data := _data()
	var seen := {}
	for row in data["cases"]:
		var result := Group.rate(row["after_reconcile"], data["rules"])
		for rating in result["ratings"]:
			seen[rating["state"]] = true
			assert_eq(rating["work_fields"].size(), 4 if rating["state"] in [2,4] else 0)
	assert_eq(seen.size(), 6)
	var row := _case(data, "asymmetric_relationship_mean")
	var result := Group.rate(row["after_reconcile"], data["rules"])
	assert_eq(result["ratings"][0]["relationship_mean"], 50)
	assert_eq(result["ratings"][0]["relationship_rank"], 4)
	assert_eq(Group._pair(117, 3), 62 * 68 + 3)
	assert_eq(Group._pair(3, 117), 3 * 68 + 62)


func test_opaque_metadata_and_work_bytes_survive_and_views_are_independent() -> void:
	var data := _data()
	var row := _case(data, "reset_groups_clears_work")
	var before: Dictionary = row["before"].duplicate(true)
	before["opaque"] = {"nested": [{"fraction": 1.25, "label": "untouched"}]}
	var pristine := before.duplicate(true)
	var cleaned := Group.reconcile(before, data["rules"])
	var rated := Group.rate(cleaned["after"], data["rules"])
	assert_eq(before, pristine)
	assert_eq(rated["after"]["opaque"], pristine["opaque"])
	for key in ["month", "week", "global_total_511c", "student_record_sha256", "relationships", "student_ids"]:
		assert_eq(rated["after"][key], pristine[key], key)
	for group in range(5):
		for offset in [2, 5, 10, 11, 12, 13, 15, 24, 25, 26, 27]:
			assert_eq(rated["after"]["group_raw_bytes"][group * 28 + offset], pristine["group_raw_bytes"][group * 28 + offset])
	rated["after"]["opaque"]["nested"][0]["label"] = "changed"
	rated["after"]["student_ids"].clear()
	assert_eq(before, pristine)
	assert_eq(cleaned["after"]["opaque"], pristine["opaque"])
