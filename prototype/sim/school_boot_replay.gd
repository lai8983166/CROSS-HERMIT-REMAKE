class_name SchoolBootReplay
extends RefCounted
## Projects captured boot data after BOTH state9 task constructors.
## Fresh audited 5/1 roster only; no teacher work tables, menu or resource readiness.

const Week = preload("res://sim/week_settlement_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const Entry = preload("res://sim/school_entry_replay.gd")
var _instances: Dictionary = {}


func initialize_once(instance_id: String, context: Dictionary, before: Dictionary,
		role_rules: Dictionary, boot_rules: Dictionary) -> Dictionary:
	if instance_id.is_empty():
		return _unsupported("missing_instance_id")
	var reason := _validate(context, before, role_rules, boot_rules)
	if not reason.is_empty():
		return _unsupported(reason)
	# Preserve opaque metadata exactly, including fractional presentation values.
	var input := {"context": context.duplicate(true), "before": before.duplicate(true),
		"role_rules": role_rules.duplicate(true), "boot_rules": boot_rules.duplicate(true)}
	if _instances.has(instance_id):
		if _instances[instance_id]["input"] != input:
			return _unsupported("instance_input_conflict")
		return _view(_instances[instance_id], "duplicate")
	var after: Dictionary = input["before"].duplicate(true)
	_project_captured_fields(after, Roles._integers(input["boot_rules"]))
	var entry := {"input": input, "after": after}
	_instances[instance_id] = entry
	return _view(entry, "projected_once")


static func _project_captured_fields(after: Dictionary, rules: Dictionary) -> void:
	var control: Dictionary = after["school_control"]
	var roster: Array = Roles._integers(after["student_ids"].slice(0, int(after["student_count"])))
	var records := {}
	for record in after["participants"]:
		records[int(record["character_id"])] = record
	# 4A9AB0 ranks in roster order, using strictly greater counts (ties share rank).
	var values: Array = []
	for identity in roster:
		var row: Array = Roles._integers(records[identity]["attributes"])
		var total := 0
		for value in row:
			total += value
		row.append(total)
		values.append(row)
	control["group_rankings"] = []
	for row in values:
		var ranks: Array = []
		for column in range(8):
			var rank := 1
			for other in values:
				if other[column] > row[column]:
					rank += 1
			ranks.append(rank)
		control["group_rankings"].append(ranks)
	# 4A5F40: no teachers in this supported input. Clear students from classes,
	# preserving their global records and all other raw group bytes.
	for group in range(5):
		control["group_raw_bytes"][group * 28 + 3] = 1
		control["group_raw_bytes"][group * 28 + 14] = 0
		for slot in range(4):
			after["group_student_ids"][group][slot] = -1
			after["group_student_indices"][group][slot] = -1
			control["group_raw_bytes"][group * 28 + 16 + slot * 2] = 255
			control["group_raw_bytes"][group * 28 + 17 + slot * 2] = 255
	# Reproduce 4A8BF0's descending swap sort; do not assume stable ties.
	var idle := roster.duplicate()
	for i in range(idle.size()):
		for j in range(i + 1, idle.size()):
			if records[idle[i]]["level_50"] < records[idle[j]]["level_50"]:
				var old: int = idle[i]
				idle[i] = idle[j]
				idle[j] = old
	control["idle_student_ids"] = idle
	control["idle_teacher_ids"] = []
	control["selected_group"] = -1
	control["lecture_counts"] = [0, 0, 0]
	# 4A17B0/4A9D90 prepend newly dated records, then 4A1C70 categorizes.
	var work: Array = []
	for rule in rules["adventures"]:
		if rule["present"] != 0 and rule["gate"] != 0 and rule["kind"] != 0 \
				and rule["month"] == after["month"] and rule["week"] == after["week"]:
			var duration: int = -1 if rule["duration"] == 99 else rule["duration"]
			var category := 0 if rule["kind"] == 4 else (1 if duration == -1 else 2)
			work.push_front([category, (rule["kind"] - 1) & 255,
				(rule["subkind"] - 1) & 255, rule["id"], duration])
			control["adventure_unlock_flags"][rule["id"] - 1] = 1
	control["adventure_entries"] = [[], [], []]
	control["adventure_counts"] = [0, 0, 0]
	after["flags"]["0x7a55fa"] = 0
	for index in range(work.size()):
		var record: Array = work[index]
		control["adventure_entries"][record[0]].append([record[1], record[2], record[3], record[4], index])
		control["adventure_counts"][record[0]] += 1
		if record[0] == 0:
			after["flags"]["0x7a55fa"] = 1
	# 4A2BA0 uses month*6+week, without an extra present or teacher-count gate.
	for rule in rules["lectures"]:
		if rule["month"] * 6 + rule["week"] <= after["month"] * 6 + after["week"] \
				and rule["kind"] != 0 and rule["subkind"] != 0:
			control["lecture_unlock_flags"][rule["id"] - 1] = 1
	after["flags"]["0x7a4e62"] = 1
	# 4A5A60 + 4AB7A0 before menu, then 4B8D50's phase0 idle branch.
	control["group_task_controls"] = [0, 1, 1, 2, 0]
	control["person_phase"] = 0
	control["person_ready"] = 1
	control["person_selection"] = -1


static func _validate(context: Dictionary, before: Dictionary, role_rules: Dictionary, rules: Dictionary) -> String:
	for pair in [["task_state", 9], ["pending_flag", 0]]:
		if not Week._integer(context.get(pair[0])) or int(context[pair[0]]) != pair[1]:
			return "pending_both_school_constructors"
	if not context.get("school_constructed") is bool or not context["school_constructed"] \
			or not context.get("tasks") is Array or context["tasks"].size() != 2:
		return "missing_or_wrong_school_tasks"
	for task in context["tasks"]:
		if not task is Dictionary or not Week._integer(task.get("size")) or not Week._integer(task.get("active")):
			return "invalid_school_task_fields"
	if Roles._integers(context["tasks"]) != Entry.TASKS:
		return "missing_or_wrong_school_tasks"
	var reason := Week._validate(before, role_rules)
	if not reason.is_empty():
		return reason
	if int(before["month"]) != 5 or int(before["week"]) != 1 \
			or int(before["flags"]["0x7a4e62"]) != 1 or int(before["flags"]["0x7a55fa"]) != 0 \
			or not [int(before["flags"]["0x7a55f6"]), int(before["flags"]["0x7e11a0"])] in [[11, 0], [9, 1]]:
		return "outside_sourced_school_boot"
	if not Week._integer(before.get("student_count")) or int(before["student_count"]) != 4 \
			or not Week._integer(before.get("teacher_count")) or int(before["teacher_count"]) != 0 \
			or not Week._vector(before.get("student_ids"), 20, -1, 44) \
			or not Week._vector(before.get("teacher_ids"), 20, -1, -1):
		return "outside_sourced_roster"
	var roster: Array = Roles._integers(before["student_ids"].slice(0, 4))
	var sorted := roster.duplicate()
	sorted.sort()
	if sorted != [3, 4, 5, 9] or not Week._vector(before["student_ids"].slice(4), 16, -1, -1) \
			or before["participants"].size() != 4:
		return "outside_sourced_roster"
	for identity in range(1, 45):
		if int(before["availability"][identity]) != (1 if roster.has(identity) else 0):
			return "roster_availability_mismatch"
	for record in before["participants"]:
		if not roster.has(int(record["character_id"])) or not Week._bounded(record.get("level_50"), 0, 255):
			return "missing_student_level_or_id"
	if not before.get("school_control") is Dictionary:
		return "missing_school_control"
	var control: Dictionary = before["school_control"]
	for key in ["selected_group", "person_phase", "person_ready", "person_selection"]:
		if not Week._bounded(control.get(key), 0, 0):
			return "outside_fresh_school_control"
	for spec in [["idle_student_ids", 0], ["idle_teacher_ids", 0], ["adventure_counts", 3],
			["lecture_counts", 3], ["adventure_unlock_flags", 100], ["lecture_unlock_flags", 100], ["group_task_controls", 5]]:
		if not Week._vector(control.get(spec[0]), spec[1], 0, 0):
			return "outside_fresh_" + spec[0]
	if not _matrix(control.get("adventure_entries"), 3, 0, 0, 0) \
			or not _matrix(control.get("group_rankings"), 4, 8, 0, 0) \
			or not Week._vector(control.get("group_raw_bytes"), 140, 0, 255) \
			or not _matrix(before.get("group_student_ids"), 5, 4, -1, 44) \
			or not _matrix(before.get("group_student_indices"), 5, 4, -1, 3):
		return "invalid_captured_group_layout"
	for group in range(5):
		var raw: Array = control["group_raw_bytes"]
		if int(raw[group * 28]) != 255 or int(raw[group * 28 + 1]) != 255:
			return "outside_teacherless_classes"
		for slot in range(4):
			var identity := int(before["group_student_ids"][group][slot])
			var packed := int(raw[group * 28 + 16 + slot * 2]) | (int(raw[group * 28 + 17 + slot * 2]) << 8)
			if packed != (identity & 65535) or (identity != -1 and not roster.has(identity)) \
					or int(before["group_student_indices"][group][slot]) != roster.find(identity):
				return "inconsistent_class_student_fields"
	for category in ["adventures", "lectures"]:
		if not rules.get(category) is Array or rules[category].size() != 100:
			return "missing_school_template_rules"
		for index in range(100):
			var rule: Variant = rules[category][index]
			if not rule is Dictionary or not Week._bounded(rule.get("id"), index + 1, index + 1):
				return "invalid_school_template_id"
			var specs := [["month", 0, 255], ["week", 0, 255], ["kind", -32768, 32767], ["subkind", -32768, 32767]]
			if category == "adventures":
				specs = [["month", 0, 255], ["week", 0, 255], ["present", 0, 255], ["duration", 0, 255],
					["kind", 0, 255], ["subkind", -128, 127], ["gate", 0, 255]]
			for spec in specs:
				if not Week._bounded(rule.get(spec[0]), spec[1], spec[2]):
					return "invalid_school_template_" + spec[0]
	return ""


static func _matrix(value: Variant, rows: int, columns: int, minimum: int, maximum: int) -> bool:
	if not value is Array or value.size() != rows:
		return false
	for row in value:
		if not Week._vector(row, columns, minimum, maximum):
			return false
	return true


static func _view(entry: Dictionary, status: String) -> Dictionary:
	return {"supported": true, "status": status, "after": entry["after"].duplicate(true),
		"projection": "captured_school_boot_fields", "school_boot_data_projected": true,
		"pending_state": 9, "pending_flag": 0, "week_executed": false,
		"school_initialized": false, "interactive_school_ready": false,
		"live_witness": false, "authorizes_persistent_write": false}


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "school_boot_data_projected": false,
		"school_initialized": false, "interactive_school_ready": false,
		"live_witness": false, "authorizes_persistent_write": false}
