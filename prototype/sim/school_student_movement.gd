extends RefCounted
## Original student-only 4A4680 operation on isolated prepared school data.
## Immediate drag changes remain separate from explicit later cleanup/rating.

const Group = preload("res://sim/school_teacher_group_replay.gd")
const Sort = preload("res://sim/school_waitlist_sort.gd")
const Week = preload("res://sim/week_settlement_replay.gd")


static func move_student(before: Dictionary, command: Dictionary, profiles: Variant,
		group_rules: Dictionary, sort_rules: Dictionary) -> Dictionary:
	var reason := _validate(before, command, profiles, group_rules, sort_rules)
	if not reason.is_empty():
		return Group._unsupported(reason)
	var after := before.duplicate(true)
	after["task_drag_state"] = 2
	var target := int(command["target_group"])
	var slot := int(command["target_slot"])
	var source := int(command["source_group"])
	var origin := int(command["source_slot"])
	var identity := int(command["student_id"])
	var eligible := target >= 0 and Group._word(after["group_raw_bytes"], target * 28) != -1
	if eligible:
		after["selected_group"] = target
	if not command["released"]:
		return _view(after, "held")
	var waiting: Array = after["idle_student_ids"]
	if eligible:
		var offset := target * 28 + 16 + slot * 2
		var occupant := Group._word(after["group_raw_bytes"], offset)
		Group._put_word(after["group_raw_bytes"], offset, identity)
		if source == -1:
			waiting.remove_at(origin)
			if occupant == -1:
				after["group_raw_bytes"][target * 28 + 14] += 1
			else:
				waiting.append(occupant)
		else:
			Group._put_word(after["group_raw_bytes"], source * 28 + 16 + origin * 2, occupant)
		# Native rates only the target class here; source indices/count can be stale.
		var rated := Group.rate(after, group_rules)
		if not rated["supported"]:
			return rated
		for key in ["derived_teacher_ids", "derived_teacher_indices", "derived_student_ids", "derived_student_indices"]:
			after[key][target] = rated["after"][key][target]
	elif source >= 0:
		waiting.append(identity)
		Group._put_word(after["group_raw_bytes"], source * 28 + 16 + origin * 2, -1)
	if eligible or source >= 0:
		var sorted := Sort.order(profiles, waiting, before["idle_sort_mode"], sort_rules)
		if not sorted["supported"]:
			return sorted
		after["idle_student_ids"] = sorted["idle_student_ids"]
	for key in ["drag_kind", "drag_origin", "drag_group", "drag_slot", "drag_id"]:
		after[key] = -1
	after["task_command"] = 0
	return _view(after, "released")


static func reconcile(before: Dictionary, group_rules: Dictionary) -> Dictionary:
	# 4A5F40 also resets the sort controls owned by this extended snapshot.
	if not Week._bounded(before.get("idle_sort_mode"), 0, 2) \
			or not Week._bounded(before.get("teacher_sort_mode"), 0, 2):
		return Group._unsupported("invalid_movement_sort_control")
	var result := Group.reconcile(before, group_rules)
	if result["supported"]:
		result["after"]["idle_sort_mode"] = 0
		result["after"]["teacher_sort_mode"] = 0
		result["execution_scope"] = "isolated_student_movement_data"
	return result


static func _validate(before: Dictionary, command: Dictionary, profiles: Variant,
		group_rules: Dictionary, sort_rules: Dictionary) -> String:
	var reason := Group._validate(before, group_rules)
	if not reason.is_empty():
		return reason
	for spec in [["idle_sort_mode",0,2], ["teacher_sort_mode",0,2], ["drag_kind",0,0],
			["drag_origin",0,1], ["drag_group",-1,4], ["drag_slot",0,19], ["drag_id",1,12],
			["drag_source_rank",0,7], ["task_drag_state",0,2], ["task_command",0,65535]]:
		if not Week._bounded(before.get(spec[0]), spec[1], spec[2]):
			return "invalid_student_drag_control"
	if command.get("kind") != "student" or not command.get("released") is bool \
			or not Week._bounded(command.get("student_id"),1,12) \
			or not Week._bounded(command.get("source_group"),-1,4) \
			or not Week._bounded(command.get("source_slot"),0,19) \
			or not Week._bounded(command.get("target_group"),-1,4) \
			or not Week._bounded(command.get("target_slot"),-1,3):
		return "invalid_student_move_command"
	var source := int(command["source_group"])
	var origin := int(command["source_slot"])
	var target := int(command["target_group"])
	var slot := int(command["target_slot"])
	var identity := int(command["student_id"])
	if (target == -1 and slot != -1) or (target >= 0 and slot < 0):
		return "invalid_student_move_target"
	if int(before["drag_origin"]) != (0 if source == -1 else 1) \
			or int(before["drag_group"]) != source or int(before["drag_slot"]) != origin \
			or int(before["drag_id"]) != identity:
		return "stale_student_drag_selection"
	if source == -1:
		if origin >= before["idle_student_ids"].size() or before["idle_student_ids"][origin] != identity:
			return "stale_waiting_student_source"
	elif origin >= 4 or Group._word(before["group_raw_bytes"], source * 28 + 16 + origin * 2) != identity:
		return "stale_class_student_source"
	var roster: Array = before["student_ids"].slice(0, int(before["student_count"]))
	var membership: Array = before["idle_student_ids"].duplicate()
	var waiting_teachers: Array = before["teacher_ids"].slice(0, int(before["teacher_count"]))
	for group in range(5):
		var base := group * 28
		var count := 0
		var teacher := Group._word(before["group_raw_bytes"],base)
		if teacher != -1:
			waiting_teachers.erase(teacher)
		for index in range(4):
			var member := Group._word(before["group_raw_bytes"],base + 16 + index * 2)
			if member != -1:
				membership.append(member)
				count += 1
		if int(before["group_raw_bytes"][base + 14]) != count:
			return "pending_student_count_reconciliation"
	membership.sort()
	roster.sort()
	var teacher_wait: Array = before["idle_teacher_ids"].duplicate()
	teacher_wait.sort()
	waiting_teachers.sort()
	if membership != roster or teacher_wait != waiting_teachers:
		return "student_move_membership_mismatch"
	var sorted := Sort.order(profiles, roster, before["idle_sort_mode"], sort_rules)
	if not sorted["supported"]:
		return sorted["reason"]
	if profiles.size() != roster.size():
		return "student_move_profile_roster_mismatch"
	var rated := Group.rate(before, group_rules)
	if not rated["supported"]:
		return rated["reason"]
	for key in ["derived_teacher_ids", "derived_teacher_indices", "derived_student_ids", "derived_student_indices"]:
		if before[key] != rated["after"][key]:
			return "pending_student_index_reconciliation"
	return ""


static func _view(after: Dictionary, status: String) -> Dictionary:
	var result := Group._view(after, status)
	result["execution_scope"] = "isolated_student_movement_data"
	return result
