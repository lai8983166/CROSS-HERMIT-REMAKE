class_name WorkroomReturnReplay
extends RefCounted
## Isolated 5/1 workroom/CH002 control projection, backed by native snapshots.
## Completion is a declared input. No VM, school body, or persistent authority.

const Week = preload("res://sim/week_settlement_replay.gd")
var _instances: Dictionary = {}


func begin(instance_id: String, context: Dictionary, before: Dictionary, rules: Dictionary) -> Dictionary:
	if instance_id.is_empty():
		return _unsupported("missing_instance_id")
	var input := {"context": context.duplicate(true), "before": before.duplicate(true), "rules": rules.duplicate(true)}
	if _instances.has(instance_id):
		if _instances[instance_id]["input"] != input:
			return _unsupported("instance_input_conflict")
		return _view(_instances[instance_id], "duplicate")
	if not context.get("adv_completed") is bool:
		return _unsupported("missing_adv_completion_input")
	if not context["adv_completed"]:
		return _unsupported("pending_ch001_completion")
	for pair in [["task_state", 8], ["pending_flag", 1], ["vm_active", 0],
			["next_task_state", 8], ["end_file_offset", 0x1b0], ["opcode", 19]]:
		if not Week._integer(context.get(pair[0])) or int(context[pair[0]]) != pair[1]:
			return _unsupported("pending_ch001_next8_gate")
	if context.get("script_path") != "chapter208.ybc":
		return _unsupported("outside_sourced_ch001_end")
	var reason := _validate(before, rules)
	if not reason.is_empty():
		return _unsupported(reason)
	var entry := {"input": input, "after": before.duplicate(true), "phase": "workroom",
		"requested_state": 8, "pending_flag": 0, "script_requests": [],
		"ch002_completed": false, "ch002_context": {}, "phase_log": ["consume8"]}
	_instances[instance_id] = entry
	return _view(entry, "waiting_continue")


func continue_workroom(instance_id: String, continue_ready: bool) -> Dictionary:
	if not _instances.has(instance_id):
		return _unsupported("missing_workroom_instance")
	var entry: Dictionary = _instances[instance_id]
	if entry["phase"] != "workroom":
		return _view(entry, "duplicate")
	if not continue_ready:
		return _view(entry, "waiting_continue")
	if int(entry["after"]["flags"]["0x7a4e62"]) != 0:
		entry["after"]["flags"]["0x7e11a0"] = 1
		entry["phase"] = "school_requested"
		entry["requested_state"] = 9
	else:
		entry["after"]["flags"]["0x7a4e62"] = 1
		entry["phase"] = "ch002_loaded"
		entry["requested_state"] = 6
		entry["script_requests"] = [{"path": "Data\\Adv\\dat\\CH002.ybc", "next_task_state": 9}]
	entry["pending_flag"] = 1
	entry["phase_log"].append(entry["phase"])
	return _view(entry, "continued_once")


func start_ch002(instance_id: String, context: Dictionary) -> Dictionary:
	if not _instances.has(instance_id):
		return _unsupported("missing_workroom_instance")
	var entry: Dictionary = _instances[instance_id]
	if not entry["ch002_context"].is_empty():
		if entry["ch002_context"] != context:
			return _unsupported("ch002_input_conflict")
		return _view(entry, "duplicate")
	if entry["phase"] != "ch002_loaded":
		return _unsupported("missing_ch002_load")
	for pair in [["state", 6], ["pending_flag", 1], ["next_task_state", 9], ["vm_active", 1], ["vm_pc", 0]]:
		if not Week._integer(context.get(pair[0])) or int(context[pair[0]]) != pair[1]:
			return _unsupported("pending_ch002_gate")
	if context.get("path") != "ch002.ybc":
		return _unsupported("outside_sourced_ch002")
	entry["ch002_context"] = context.duplicate(true)
	# At 5/1 the native script reaches opcode151 BEFORE waiting on its fade.
	entry["after"]["flags"]["0x7a55f6"] = 11
	entry["after"]["flags"]["0x7e11a0"] = 0
	entry["phase"] = "ch002_running"
	entry["pending_flag"] = 0
	entry["phase_log"].append("ch002_opcode151")
	return _view(entry, "waiting_ch002_end")


func finish_ch002(instance_id: String, end_ready: bool) -> Dictionary:
	if not _instances.has(instance_id):
		return _unsupported("missing_workroom_instance")
	var entry: Dictionary = _instances[instance_id]
	if entry["ch002_completed"]:
		return _view(entry, "duplicate")
	if entry["phase"] != "ch002_running":
		return _unsupported("missing_ch002_execution")
	if not end_ready:
		return _view(entry, "waiting_ch002_end")
	entry["phase"] = "school_requested"
	entry["requested_state"] = 9
	entry["pending_flag"] = 1
	entry["ch002_completed"] = true
	entry["phase_log"].append("ch002_end_request9")
	return _view(entry, "completed_once")


static func _validate(before: Dictionary, rules: Dictionary) -> String:
	var reason := Week._validate(before, rules)
	if not reason.is_empty():
		return reason
	if int(before["month"]) != 5 or int(before["week"]) != 1:
		return "outside_sourced_ch002_date"
	if int(before["flags"]["0x7a55f6"]) != 9 or int(before["flags"]["0x7e11a0"]) != 1 \
			or not Week._bounded(before["flags"]["0x7a4e62"], 0, 1):
		return "outside_ch001_workroom_flags"
	if not before.get("adv_globals") is Dictionary:
		return "missing_adv_globals"
	for pair in [["0x7a5292", 8], ["0x7e1182", 0]]:
		if not Week._integer(before["adv_globals"].get(pair[0])) or int(before["adv_globals"][pair[0]]) != pair[1]:
			return "outside_ch001_background_subset"
	# CH001 does not clear the result-recipient alias. The original standalone
	# ADV probe began at0; the same-CPU result continuation retains recipient4.
	if not Week._integer(before["adv_globals"].get("0x7e1180")) \
			or not int(before["adv_globals"]["0x7e1180"]) in [0, 4]:
		return "outside_ch001_background_subset"
	if not Week._bounded(before.get("student_count"), 4, 4) \
			or not Week._vector(before.get("student_ids"), 20, -1, 44) \
			or not Week._bounded(before.get("teacher_count"), 0, 0) \
			or not Week._vector(before.get("teacher_ids"), 20, -1, -1):
		return "outside_sourced_roster"
	var students := {}
	for index in range(20):
		var id := int(before["student_ids"][index])
		if index >= 4:
			if id != -1:
				return "invalid_roster_tail"
		elif not id in [3, 4, 5, 9] or students.has(id) or int(before["availability"][id]) != 1:
			return "invalid_student_membership"
		else:
			students[id] = true
	for id in range(1, 45):
		if int(before["availability"][id]) == 1 and not students.has(id):
			return "missing_available_student"
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
			if (id == -1 and index != -1) or (id != -1 and (index < 0 or index >= 4 \
					or int(before["student_ids"][index]) != id)):
				return "mismatched_group_student"
	return ""


static func _view(entry: Dictionary, status: String) -> Dictionary:
	return {"supported": true, "status": status, "after": entry["after"].duplicate(true),
		"phase": entry["phase"], "requested_state": entry["requested_state"], "pending_flag": entry["pending_flag"],
		"script_requests": entry["script_requests"].duplicate(true), "ch002_completed": entry["ch002_completed"],
		"phase_log": entry["phase_log"].duplicate(true), "week_executed": false,
		"school_initialized": false, "live_witness": false, "authorizes_persistent_write": false}


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "school_initialized": false,
		"live_witness": false, "authorizes_persistent_write": false}
