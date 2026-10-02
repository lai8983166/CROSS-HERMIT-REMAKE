class_name WeekStartReplay
extends RefCounted
## Isolated state7 task. Week runs before fade; CH001/8 is only a request.
## Caller-supplied ADV completion is a declared input, never live authority.

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
	if not Week._integer(context.get("task_state")) or int(context["task_state"]) != 7:
		return _unsupported("pending_state7_gate")
	if not context.get("adv_completed") is bool:
		return _unsupported("missing_adv_completion_input")
	if not context["adv_completed"]:
		return {"supported": true, "status": "waiting_adv", "after": before.duplicate(true),
			"week_executed": false, "requested_state": 6, "script_requests": [],
			"school_initialized": false, "live_witness": false, "authorizes_persistent_write": false}
	if not Week._bounded(before.get("month"), 4, 14):
		return _unsupported("outside_week_start_calendar_subset")
	# Directly project the known 4D3510 body. Do not fabricate a state12 context:
	# state7 unconditionally invokes it, whereas state12 has a special-date gate.
	var settled: Dictionary = Week.project(before, rules)
	if not settled["supported"]:
		return settled
	var entry := {"input": input, "after": settled["after"].duplicate(true),
		"completed": false, "requested_state": 7, "script_requests": [],
		"phase_log": [{"phase": "week_settlement", "before": before.duplicate(true),
			"after": settled["after"].duplicate(true)}]}
	_instances[instance_id] = entry
	return _view(entry, "week_applied_once")


func finish(instance_id: String, fade_ready: bool) -> Dictionary:
	if not _instances.has(instance_id):
		return _unsupported("missing_week_start_instance")
	var entry: Dictionary = _instances[instance_id]
	if entry["completed"]:
		return _view(entry, "duplicate")
	if not fade_ready:
		return _view(entry, "waiting_fade")
	entry["completed"] = true
	entry["requested_state"] = 6
	entry["script_requests"] = [{"path": "Data\\Adv\\dat\\CH001.ybc", "next_task_state": 8}]
	entry["phase_log"].append({"phase": "fade_completed", "requested_state": 6,
		"script_requests": entry["script_requests"].duplicate(true)})
	return _view(entry, "completed_once")


static func _view(entry: Dictionary, status: String) -> Dictionary:
	return {"supported": true, "status": status, "after": entry["after"].duplicate(true),
		"week_executed": true, "completed": entry["completed"], "fade_frames": 90,
		"requested_state": entry["requested_state"], "script_requests": entry["script_requests"].duplicate(true),
		"phase_log": entry["phase_log"].duplicate(true), "school_initialized": false,
		"live_witness": false, "authorizes_persistent_write": false}


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "authorizes_persistent_write": false}
