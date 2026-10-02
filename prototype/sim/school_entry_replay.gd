class_name SchoolEntryReplay
extends RefCounted
## Source state9 consumes one request and creates TWO school task descriptors.
## No task bodies, school initialization, or live/persistent store authority.

const Week = preload("res://sim/week_settlement_replay.gd")
const TASKS = [
	{"size": 0x1419c, "vtable": "0x5a0a40", "active": 1,
		"source_wrapper_va": "0x4aba70", "source_constructor_va": "0x4ab570"},
	{"size": 0x3a5e4, "vtable": "0x5a0c18", "active": 1,
		"source_wrapper_va": "0x4b89a0", "source_constructor_va": "0x4b8a90"}]
var _instances: Dictionary = {}


func dispatch_once(instance_id: String, context: Dictionary, before: Dictionary, rules: Dictionary) -> Dictionary:
	if instance_id.is_empty():
		return _unsupported("missing_instance_id")
	var input := {"context": context.duplicate(true), "before": before.duplicate(true), "rules": rules.duplicate(true)}
	if _instances.has(instance_id):
		if _instances[instance_id]["input"] != input:
			return _unsupported("instance_input_conflict")
		return _view(_instances[instance_id], "duplicate")
	for pair in [["task_state", 9], ["pending_flag", 1], ["adv_active", 0]]:
		if not Week._integer(context.get(pair[0])) or int(context[pair[0]]) != pair[1]:
			return _unsupported("pending_school_request9")
	if context.get("source_request_va") != "0x439e30":
		return _unsupported("missing_native_request_source")
	var reason := Week._validate(before, rules)
	if not reason.is_empty():
		return _unsupported(reason)
	if int(before["month"]) != 5 or int(before["week"]) != 1 \
			or int(before["flags"]["0x7a4e62"]) != 1 \
			or not [int(before["flags"]["0x7a55f6"]), int(before["flags"]["0x7e11a0"])] in [[11, 0], [9, 1]]:
		return _unsupported("outside_sourced_school_entry")
	var entry := {"input": input, "after": before.duplicate(true), "tasks": TASKS.duplicate(true)}
	_instances[instance_id] = entry
	return _view(entry, "dispatched_once")


static func _view(entry: Dictionary, status: String) -> Dictionary:
	return {"supported": true, "status": status, "after": entry["after"].duplicate(true),
		"tasks": entry["tasks"].duplicate(true), "pending_state": 9, "pending_flag": 0,
		"school_constructed": true, "school_initialized": false, "week_executed": false,
		"live_witness": false, "authorizes_persistent_write": false}


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "school_constructed": false,
		"school_initialized": false, "live_witness": false, "authorizes_persistent_write": false}
