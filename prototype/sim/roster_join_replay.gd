class_name RosterJoinReplay
extends RefCounted
## Isolated Chapter020 opcode144 projection; no chapter/school completion.

const Week = preload("res://sim/week_settlement_replay.gd")
var _instances: Dictionary = {}


func apply_once(instance_id: String, context: Dictionary, before: Dictionary, rules: Dictionary) -> Dictionary:
	if instance_id.is_empty():
		return _unsupported("missing_instance_id")
	if _instances.has(instance_id):
		var cached: Dictionary = _instances[instance_id]
		if cached["context"] != context or cached["before"] != before or cached["rules"] != rules:
			return _unsupported("instance_input_conflict")
		return cached["result"].duplicate(true)
	var reason := _validate(context, before, rules)
	if not reason.is_empty():
		return _unsupported(reason)
	var after := before.duplicate(true)
	var status := "already_available"
	if int(before["availability"][5]) == 0:
		status = "joined_once"
		after["student_ids"][int(before["student_count"])] = 5
		after["student_count"] = int(before["student_count"]) + 1
		var candidate: Dictionary
		for record in after["participants"]:
			if int(record["character_id"]) == 5:
				candidate = record
		candidate["unlock_flags"].fill(0)
		candidate["unlock_reserved_bytes"].fill(0)
		candidate["unlock_flags"][int(candidate["job"]) - 1] = 1
		for slot in range(8):
			var item := int(candidate["equipped_items"][slot])
			if item == 0:
				continue
			var flags := int(after["item_flags"][item - 1])
			if (flags & 1) != 0:
				candidate["equipped_items"][slot] = 0
			else:
				after["item_flags"][item - 1] = ((flags | 1) & 0xf001) | 0x300 | (5 << 1)
		for slot in range(8):
			var skill := int(candidate["equipped_skills"][slot])
			if skill == 0:
				continue
			if int(context["difficulty"]) == 0:
				candidate["skill_statuses"][skill - 1] = 6
			else:
				candidate["equipped_skills"][slot] = 0
		var total := 0
		for pool in candidate["growth_pools"]:
			total += int(pool)
		for skill in range(84):
			if int(candidate["skill_statuses"][skill]) in [3, 5, 6]:
				total += int(rules["learned_points"][skill])
		var level := 2
		while level < 51 and int(rules["level_thresholds"][level - 1]) <= total:
			level += 1
		candidate["level_50"] = level - 1
		Week.apply_unlocks(candidate, int(before["month"]), int(before["week"]), rules["week"])
		after["availability"][5] = 1
	var result := {"supported": true, "status": status, "after": after,
		"character_id": 5, "chapter_completed": false, "school_initialized": false,
		"live_witness": false, "authorizes_persistent_write": false}
	_instances[instance_id] = {"context": context.duplicate(true), "before": before.duplicate(true),
		"rules": rules.duplicate(true), "result": result.duplicate(true)}
	return result


static func _validate(context: Dictionary, before: Dictionary, rules: Dictionary) -> String:
	for key in ["task_state", "script_file_offset", "opcode", "character_id", "group", "slot", "difficulty"]:
		if not context.has(key) or not Week._integer(context[key]):
			return "missing_or_invalid_context_" + key
	if int(context["task_state"]) != 6 or context.get("script_path") != "DATA/ADV/DAT/Chapter020.ybc" \
			or int(context["script_file_offset"]) != 20 or int(context["opcode"]) != 144 \
			or int(context["character_id"]) != 5 or int(context["group"]) != -1 or int(context["slot"]) != -1 \
			or not int(context["difficulty"]) in [0, 2]:
		return "outside_sourced_join_subset"
	if not rules.get("week") is Dictionary:
		return "missing_week_rules"
	var reason := Week._validate(before, rules["week"])
	if not reason.is_empty():
		return reason
	if int(before["month"]) != 4 or int(before["week"]) != 5:
		return "outside_chapter020_date"
	if not Week._vector(rules.get("level_thresholds"), 50, 0, 2147483647) \
			or not Week._vector(rules.get("learned_points"), 84, 0, 2147483647):
		return "invalid_level_rules"
	for index in range(1, 50):
		if int(rules["level_thresholds"][index]) < int(rules["level_thresholds"][index - 1]):
			return "unordered_level_thresholds"
	var ids := {}
	var candidate: Dictionary
	for record in before["participants"]:
		ids[int(record["character_id"])] = true
		if not Week._bounded(record.get("job"), 1, 30) or not Week._bounded(record.get("level_50"), 1, 50) \
				or not Week._vector(record.get("growth_pools"), 7, 0, 2147483647) \
				or not Week._vector(record.get("unlock_reserved_bytes"), 2, 0, 255):
			return "invalid_join_character_fields"
		if int(record["character_id"]) == 5:
			candidate = record
	if candidate.is_empty():
		return "missing_join_candidate"
	var maximum_total := 0
	for pool in candidate["growth_pools"]:
		maximum_total += int(pool)
	for points in rules["learned_points"]:
		maximum_total += int(points)
	if maximum_total > 2147483647:
		return "outside_stat_sum_bounds"
	if not Week._bounded(before.get("student_count"), 0, 20) \
			or not Week._vector(before.get("student_ids"), 20, -1, 44) \
			or not Week._bounded(before.get("teacher_count"), 0, 0) \
			or not Week._vector(before.get("teacher_ids"), 20, -1, -1):
		return "outside_student_roster_subset"
	var students := {}
	for index in range(20):
		var id := int(before["student_ids"][index])
		if index >= int(before["student_count"]):
			if id != -1:
				return "invalid_roster_tail"
		elif id < 1 or students.has(id) or not ids.has(id) or int(before["availability"][id]) != 1:
			return "invalid_student_membership"
		else:
			students[id] = true
	for id in range(1, 45):
		if int(before["availability"][id]) == 1 and not students.has(id):
			return "missing_available_student"
	if int(before["availability"][5]) == 0 and int(before["student_count"]) >= 20:
		return "student_roster_full"
	for key in ["group_student_ids", "group_student_indices"]:
		if not before.get(key) is Array or before[key].size() != 5:
			return "invalid_group_matrix"
	for group in range(5):
		if not Week._vector(before["group_student_ids"][group], 4, -1, 44) \
				or not Week._vector(before["group_student_indices"][group], 4, -1, 19):
			return "invalid_group_slots"
		for slot in range(4):
			var id := int(before["group_student_ids"][group][slot])
			var index := int(before["group_student_indices"][group][slot])
			if (id == -1 and index != -1) or (id != -1 and (index < 0 \
					or index >= int(before["student_count"]) or int(before["student_ids"][index]) != id)):
				return "mismatched_group_student"
	return ""


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "chapter_completed": false,
		"school_initialized": false, "live_witness": false, "authorizes_persistent_write": false}
