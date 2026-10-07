extends RefCounted
## Source4A3CA0 class modes and4A2DA0 valid course clicks; no settlement.

const Group = preload("res://sim/school_teacher_group_replay.gd")
const Teacher = preload("res://sim/school_teacher_movement.gd")
const Week = preload("res://sim/week_settlement_replay.gd")
const Courses = preload("res://sim/school_course_unlocking.gd")


static func set_mode(before: Dictionary, group: Variant, teaching: Variant,
		group_rules: Dictionary, work_rules: Dictionary) -> Dictionary:
	var reason := Teacher._basic(before,group_rules,work_rules)
	if not reason.is_empty():
		return Group._unsupported(reason)
	if not Courses._integer(group,0,4) or not teaching is bool:
		return Group._unsupported("invalid_class_mode_command")
	if Group._word(before["group_raw_bytes"],int(group) * 28) == -1:
		return Group._unsupported("class_has_no_teacher")
	var after := before.duplicate(true)
	after["group_raw_bytes"][int(group) * 28 + 3] = 1 if teaching and before["adventure_gate"] == 0 else 0
	return _view(after,"mode_set")


static func select_course(before: Dictionary, command: Dictionary,
		group_rules: Dictionary, work_rules: Dictionary) -> Dictionary:
	var reason := Teacher._basic(before,group_rules,work_rules)
	if not reason.is_empty():
		return Group._unsupported(reason)
	for spec in [["group",0,4],["category",0,2],["row",0,9],["page",0,45]]:
		if not Courses._integer(command.get(spec[0]),spec[1],spec[2]):
			return Group._unsupported("invalid_course_selection_command")
	if not command.get("clicked") is bool:
		return Group._unsupported("invalid_course_selection_command")
	for spec in [["course_category",0,2],["detail_work_id",-1,100],["detail_previous_work_id",-1,100]]:
		if not Week._bounded(before.get(spec[0]),spec[1],spec[2]):
			return Group._unsupported("invalid_course_selection_control")
	var group := int(command["group"])
	var category := int(command["category"])
	if before["selected_group"] != group or before["course_category"] != category \
			or before["work_pages"][category] != command["page"]:
		return Group._unsupported("stale_course_selection")
	if Group._word(before["group_raw_bytes"],group * 28) == -1:
		return Group._unsupported("class_has_no_teacher")
	if before["group_raw_bytes"][group * 28 + 3] == 0:
		return Group._unsupported("course_requires_teaching_mode")
	var projected := Teacher.select_group(before,group,group_rules,work_rules)
	if not projected["supported"]:
		return projected
	for key in ["work_counts","work_rows","work_page_limits"]:
		if projected["after"][key] != before[key]:
			return Group._unsupported("stale_teacher_course_view")
	var index := int(command["page"]) * 2 + int(command["row"])
	if index >= int(before["work_counts"][category]) or command["page"] > before["work_page_limits"][category]:
		return Group._unsupported("course_row_unavailable")
	var after := before.duplicate(true)
	if command["clicked"]:
		var row: Array = before["work_rows"][category][index]
		for pair in [[6,category],[8,row[0]],[10,row[1]],[12,row[2]]]:
			Group._put_word(after["group_raw_bytes"],group * 28 + int(pair[0]),int(pair[1]))
	var selected := Group._word(after["group_raw_bytes"],group * 28 + 10)
	after["detail_work_id"] = selected
	if selected not in [-1,0] and before["detail_previous_work_id"] != selected:
		var templates := Teacher._templates(work_rules)
		if not templates.has(selected):
			return Group._unsupported("unsupported_selected_course_details")
		after["course_category"] = templates[selected]["category"]
		after["detail_previous_work_id"] = selected
	return _view(after,"course_selected" if command["clicked"] else "course_hover")


static func _view(after: Dictionary, status: String) -> Dictionary:
	var result := Group._view(after,status)
	result["execution_scope"] = "isolated_source_class_course_planning"
	return result
