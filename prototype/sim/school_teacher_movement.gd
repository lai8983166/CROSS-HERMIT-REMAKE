extends RefCounted
## Isolated original teacher movement and active work-list projection.

const Group = preload("res://sim/school_teacher_group_replay.gd")
const Student = preload("res://sim/school_student_movement.gd")
const Sort = preload("res://sim/school_waitlist_sort.gd")
const Week = preload("res://sim/week_settlement_replay.gd")
const TEMPLATE_HASH := "7206ac045306b139a742d678b52ba1c29d602e73245e90cb06774d6801ac651e"


static func move_teacher(before: Dictionary, command: Dictionary, profiles: Variant,
		group_rules: Dictionary, sort_rules: Dictionary, work_rules: Dictionary) -> Dictionary:
	var reason := _basic(before, group_rules, work_rules)
	if reason.is_empty():
		reason = _move_validation(before, command, profiles, group_rules, sort_rules)
	if not reason.is_empty():
		return Group._unsupported(reason)
	var after := before.duplicate(true)
	after["task_drag_state"] = 2
	if not command["released"]:
		return _view(after, "held")
	var source := int(command["source_group"])
	var origin := int(command["source_slot"])
	var target := int(command["target_group"])
	var identity := int(command["teacher_id"])
	var waiting: Array = after["idle_teacher_ids"]
	var raw: Array = after["group_raw_bytes"]
	if target >= 0:
		var occupant := Group._word(raw, target * 28)
		Group._put_word(raw, target * 28, identity)
		if source == -1:
			waiting.remove_at(origin)
			if occupant != -1:
				waiting.append(occupant)
			elif int(before["adventure_gate"]) != 0:
				raw[target * 28 + 3] = 0
		elif occupant == -1:
			_return_students(after, source)
			Group._put_word(raw, source * 28, -1)
			raw[source * 28 + 3] = 1
			_clear_work(raw, source)
			raw[target * 28 + 3] = 1 if int(before["adventure_gate"]) == 0 else 0
		else:
			Group._put_word(raw, source * 28, occupant)
			_clear_work(raw, source)
		_clear_work(raw, target)
		var selected := select_group(after, target, group_rules, work_rules)
		if not selected["supported"]:
			return selected
		after = selected["after"]
	elif source >= 0:
		waiting.append(identity)
		Group._put_word(raw, source * 28, -1)
		_return_students(after, source)
		raw[source * 28 + 3] = 1
		_clear_work(raw, source)
		var sorted := Sort.order(profiles, after["idle_student_ids"], before["idle_sort_mode"], sort_rules)
		if not sorted["supported"]:
			return sorted
		after["idle_student_ids"] = sorted["idle_student_ids"]
	# Sourced teachers117/118 have identical job, level and attribute sort keys.
	# Native teacher sorting therefore retains the append/removal order in all modes.
	for key in ["drag_kind", "drag_origin", "drag_group", "drag_slot", "drag_id"]:
		after[key] = -1
	after["task_command"] = 0
	return _view(after, "released")


static func select_group(before: Dictionary, selected: Variant,
		group_rules: Dictionary, work_rules: Dictionary) -> Dictionary:
	var reason := _basic(before, group_rules, work_rules)
	if not reason.is_empty():
		return Group._unsupported(reason)
	if not Week._bounded(selected, -1, 4):
		return Group._unsupported("invalid_teacher_work_selection")
	var identity := -1
	if int(selected) >= 0:
		identity = Group._word(before["group_raw_bytes"], int(selected) * 28)
	if identity != -1 and not Group._available(before, identity):
		return Group._unsupported("pending_teacher_work_reconciliation")
	var after := before.duplicate(true)
	after["selected_group"] = int(selected)
	after["work_counts"] = [0,0,0]
	after["work_pages"] = [0,0,0]
	after["work_page_limits"] = [0,0,0]
	after["work_rows"] = [[],[],[]]
	if identity != -1:
		var templates := _templates(work_rules)
		var rows: Array = before["teacher_work_records"][str(identity)].duplicate(true)
		rows.sort_custom(func(a, b): return int(a["slot"]) < int(b["slot"]))
		for row in rows:
			if int(row["enabled"]) == 0 or int(row["blocked"]) != 0:
				continue
			var template: Dictionary = templates[int(row["work_id"])]
			var category := int(template["category"])
			var ordinal := int(after["work_counts"][category])
			after["work_rows"][category].append([int(template["sort_key"]), int(row["work_id"]), ordinal])
			after["work_counts"][category] += 1
		for category in range(3):
			var count := int(after["work_counts"][category])
			if count > 10:
				after["work_page_limits"][category] = int((count - 9) / 2.0)
	return _view(after, "work_selected")


static func reconcile(before: Dictionary, group_rules: Dictionary, work_rules: Dictionary) -> Dictionary:
	var reason := _basic(before, group_rules, work_rules)
	if not reason.is_empty():
		return Group._unsupported(reason)
	var result := Student.reconcile(before, group_rules)
	if not result["supported"]:
		return result
	for group in range(5):
		var identity := Group._word(result["after"]["group_raw_bytes"], group * 28)
		if Group._available(result["after"], identity):
			return select_group(result["after"], group, group_rules, work_rules)
	# With no available class, native4A5F40 does not call4A8B50: keep stale work view.
	return _view(result["after"], "reconciled")


static func _clear_work(raw: Array, group: int) -> void:
	Group._put_word(raw, group * 28 + 6, -1)
	Group._put_word(raw, group * 28 + 8, -1)


static func _return_students(snapshot: Dictionary, group: int) -> void:
	for slot in range(4):
		var offset := group * 28 + 16 + slot * 2
		var identity := Group._word(snapshot["group_raw_bytes"], offset)
		if identity != -1:
			snapshot["idle_student_ids"].append(identity)
			Group._put_word(snapshot["group_raw_bytes"], offset, -1)


static func _templates(rules: Dictionary) -> Dictionary:
	var result := {}
	for row in rules["templates"]:
		result[int(row["work_id"])] = row
	return result


static func _basic(before: Dictionary, group_rules: Dictionary, rules: Dictionary) -> String:
	var reason := Group._validate(before, group_rules)
	if not reason.is_empty():
		return reason
	if rules.get("source_image_sha256") != Group.SOURCE_SHA \
			or rules.get("template_fields_sha256") != TEMPLATE_HASH or not rules.get("templates") is Array \
			or not rules.get("teacher_profiles") is Array or rules["teacher_profiles"].size() != 2:
		return "invalid_teacher_work_rules"
	var encoded := ""
	for row in rules["templates"]:
		if not row is Dictionary or not Week._bounded(row.get("work_id"),1,100) \
				or not Week._bounded(row.get("category"),0,2) or not Week._bounded(row.get("sort_key"),0,32766):
			return "invalid_teacher_work_template"
		encoded += "%d:%d:%d;" % [int(row["work_id"]), int(row["category"]), int(row["sort_key"])]
	if encoded.sha256_text() != TEMPLATE_HASH:
		return "teacher_work_template_source_mismatch"
	for index in range(2):
		var row: Variant = rules["teacher_profiles"][index]
		if not row is Dictionary or not Week._bounded(row.get("teacher_id"),117 + index,117 + index) \
				or not Week._bounded(row.get("job"),1,1) or not Week._bounded(row.get("level_50"),0,0) \
				or not Week._vector(row.get("attributes"),7,0,0):
			return "teacher_sort_template_source_mismatch"
	var work: Variant = before.get("teacher_work_records")
	if not work is Dictionary or work.size() != 2:
		return "invalid_teacher_work_records"
	var templates := _templates(rules)
	for identity in [117,118]:
		if not work.get(str(identity)) is Array or work[str(identity)].size() > 100:
			return "invalid_teacher_work_slots"
		var seen := {}
		for row in work[str(identity)]:
			if not row is Dictionary or not Week._bounded(row.get("slot"),0,99) \
					or not Week._bounded(row.get("enabled"),0,1) or not Week._bounded(row.get("blocked"),0,1) \
					or not Week._bounded(row.get("work_id"),0,100) or seen.has(int(row["slot"])):
				return "invalid_or_duplicate_teacher_work_slot"
			seen[int(row["slot"])] = true
			if int(row["enabled"]) != 0 and int(row["blocked"]) == 0 and not templates.has(int(row["work_id"])):
				return "unsupported_active_teacher_work"
	if not Week._vector(before.get("work_counts"),3,0,100) \
			or not Week._vector(before.get("work_pages"),3,0,45) \
			or not Week._vector(before.get("work_page_limits"),3,0,45) \
			or not before.get("work_rows") is Array or before["work_rows"].size() != 3:
		return "invalid_teacher_work_view"
	for category in range(3):
		var count := int(before["work_counts"][category])
		var rows: Variant = before["work_rows"][category]
		var limit := int((count - 9) / 2.0) if count > 10 else 0
		if not rows is Array or rows.size() != count or int(before["work_page_limits"][category]) != limit \
				or before["work_pages"][category] > limit:
			return "inconsistent_teacher_work_view"
		for index in range(count):
			var row: Variant = rows[index]
			if not Week._vector(row,3,0,32767) or not templates.has(int(row[1])) \
					or int(row[2]) != index or int(row[0]) != int(templates[int(row[1])]["sort_key"]) \
					or int(templates[int(row[1])]["category"]) != category:
				return "inconsistent_teacher_work_row"
	return ""


static func _move_validation(before: Dictionary, command: Dictionary, profiles: Variant,
		group_rules: Dictionary, sort_rules: Dictionary) -> String:
	for spec in [["idle_sort_mode",0,2], ["teacher_sort_mode",0,2], ["drag_kind",1,1],
			["drag_origin",0,1], ["drag_group",-1,4], ["drag_slot",-1,19], ["drag_id",117,118],
			["drag_source_rank",0,7], ["task_drag_state",0,2], ["task_command",0,65535]]:
		if not Week._bounded(before.get(spec[0]), spec[1], spec[2]):
			return "invalid_teacher_drag_control"
	if command.get("kind") != "teacher" or not command.get("released") is bool \
			or not Week._bounded(command.get("teacher_id"),117,118) \
			or not Week._bounded(command.get("source_group"),-1,4) \
			or not Week._bounded(command.get("source_slot"),-1,19) \
			or not Week._bounded(command.get("target_group"),-1,4):
		return "invalid_teacher_move_command"
	var source := int(command["source_group"])
	var origin := int(command["source_slot"])
	var identity := int(command["teacher_id"])
	if int(before["drag_origin"]) != (0 if source == -1 else 1) or int(before["drag_group"]) != source \
			or int(before["drag_slot"]) != origin or int(before["drag_id"]) != identity:
		return "stale_teacher_drag_selection"
	if source == -1:
		if origin < 0 or origin >= before["idle_teacher_ids"].size() or before["idle_teacher_ids"][origin] != identity:
			return "stale_waiting_teacher_source"
	elif origin != -1 or Group._word(before["group_raw_bytes"], source * 28) != identity:
		return "stale_class_teacher_source"
	var roster: Array = before["student_ids"].slice(0,int(before["student_count"]))
	var members: Array = before["idle_student_ids"].duplicate()
	var teachers: Array = before["teacher_ids"].slice(0,int(before["teacher_count"]))
	for group in range(5):
		var base := group * 28
		teachers.erase(Group._word(before["group_raw_bytes"],base))
		var count := 0
		for slot in range(4):
			var student := Group._word(before["group_raw_bytes"],base + 16 + slot * 2)
			if student != -1:
				members.append(student)
				count += 1
		if count != int(before["group_raw_bytes"][base + 14]):
			return "pending_teacher_student_count_reconciliation"
	var waiting: Array = before["idle_teacher_ids"].duplicate()
	for array in [roster,members,teachers,waiting]:
		array.sort()
	if roster != members or teachers != waiting:
		return "teacher_move_membership_mismatch"
	var sorted := Sort.order(profiles,roster,before["idle_sort_mode"],sort_rules)
	if not sorted["supported"]:
		return sorted["reason"]
	if profiles.size() != roster.size():
		return "teacher_move_profile_roster_mismatch"
	var rated := Group.rate(before,group_rules)
	if not rated["supported"]:
		return rated["reason"]
	for key in ["derived_teacher_ids", "derived_teacher_indices", "derived_student_ids", "derived_student_indices"]:
		if rated["after"][key] != before[key]:
			return "pending_teacher_index_reconciliation"
	return ""


static func _view(after: Dictionary, status: String) -> Dictionary:
	var result := Group._view(after,status)
	result["execution_scope"] = "isolated_teacher_movement_and_work_data"
	return result
