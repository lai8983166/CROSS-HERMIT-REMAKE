class_name ResultTransactionReplay
extends RefCounted
## One isolated result instance owns role initialization, confirmed fields and
## complete week settlement. State6/CH003 is a request; no school task/save runs.
## next_task_state is requested after ADV completion, not a script entry index.

const Roles = preload("res://sim/all_result_role_replay.gd")
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
	if not rules.get("role") is Dictionary or not rules.get("week") is Dictionary:
		return _unsupported("missing_role_or_week_rules")
	# Validate all week inputs BEFORE letting Roles create an initialized record.
	# Post fields preserve these layouts/owner IDs; no caller can change them later.
	var reason: String = Week._validate(_week_input(before), rules["week"])
	if not reason.is_empty():
		return _unsupported("week_" + reason)
	var role := Roles.new()
	var initialized: Dictionary = role.begin(instance_id, context, before, rules["role"])
	if not initialized["supported"]:
		return initialized
	var entry := {"input": input, "role": role, "week": Week.new(), "role_view": initialized,
		"completed": false, "week_executed": false, "before_week": null,
		"school_script_requests": [], "requested_state": 12,
		"phase_log": [{"phase": "initialized", "before": before.duplicate(true),
			"after": initialized["after"].duplicate(true)}]}
	_instances[instance_id] = entry
	return _view(entry, "initialized_once")


func finish(instance_id: String, confirmed: bool, mvp_ready: bool) -> Dictionary:
	if not _instances.has(instance_id):
		return _unsupported("missing_initialized_instance")
	var entry: Dictionary = _instances[instance_id]
	if entry["completed"]:
		return _view(entry, "duplicate")
	var completed: Dictionary = entry["role"].finish(instance_id, confirmed, mvp_ready)
	if not completed["supported"]:
		return completed
	if completed["status"] in ["waiting_confirmation", "waiting_mvp"]:
		entry["role_view"] = completed
		return _view(entry, completed["status"])
	# Stage candidate output locally. Publish post fields and week together only
	# after week succeeds; retries can reuse Roles' completed stage safely.
	var candidate: Dictionary = completed["after"].duplicate(true)
	var logs: Array = entry["phase_log"].duplicate(true)
	logs.append({"phase": "result_fields" if completed["result_fields_completed"] else "mode1_complete",
		"before": entry["role_view"]["after"].duplicate(true), "after": candidate.duplicate(true)})
	var before_week: Variant = null
	var did_week := false
	var requested: int = completed["requested_state"]
	var scripts := []
	if completed["week_pending"]:
		before_week = candidate.duplicate(true)
		var context: Dictionary = entry["input"]["context"]
		var week_context := {"task_state": 12, "mode": context["mode"],
			"current": context["current"], "total": context["total"],
			"result_fields_completed": completed["result_fields_completed"]}
		var settled: Dictionary = entry["week"].apply_once(instance_id, week_context,
			_week_input(candidate), entry["input"]["rules"]["week"])
		if not settled["supported"]:
			return settled
		if settled.get("status") not in ["projected_once", "duplicate"]:
			return _unsupported("unresolved_week_request")
		candidate = _merge_week(candidate, settled["after"])
		logs.append({"phase": "week_settlement", "before": before_week.duplicate(true),
			"after": candidate.duplicate(true)})
		did_week = true
		requested = 6
		scripts.append({"path": "Data\\Adv\\dat\\CH003.ybc", "next_task_state": 18})
	elif requested == 6:
		scripts.append({"path": "Data\\Adv\\dat\\CH003.ybc", "next_task_state": 7})
	completed["after"] = candidate
	completed["week_pending"] = false
	entry["role_view"] = completed
	entry["before_week"] = before_week
	entry["phase_log"] = logs
	entry["week_executed"] = did_week
	entry["requested_state"] = requested
	entry["school_script_requests"] = scripts
	entry["completed"] = true
	return _view(entry, "completed_once")


static func _week_input(snapshot: Dictionary) -> Dictionary:
	var result := {}
	for key in ["month", "week", "flags", "availability", "item_flags"]:
		if snapshot.has(key):
			result[key] = snapshot[key]
	if snapshot.has("characters"):
		result["participants"] = snapshot["characters"]
	return result.duplicate(true)


static func _merge_week(roles: Dictionary, week: Dictionary) -> Dictionary:
	var after := roles.duplicate(true)
	for key in ["month", "week", "flags", "availability", "item_flags"]:
		after[key] = week[key].duplicate(true) if week[key] is Array or week[key] is Dictionary else week[key]
	var records := {}
	for record in week["participants"]:
		records[int(record["character_id"])] = record
	for record in after["characters"]:
		var source: Dictionary = records[int(record["character_id"])]
		for key in ["attributes", "job_progress", "unlock_flags", "skill_statuses", "equipped_skills", "equipped_items"]:
			record[key] = source[key].duplicate(true)
	return after


static func _view(entry: Dictionary, status: String) -> Dictionary:
	var role: Dictionary = entry["role_view"]
	var result := {"supported": true, "status": status, "school_initialized": false,
		"school_task_executed": false, "authorizes_persistent_write": false, "live_witness": false,
		"completed": entry["completed"], "week_executed": entry["week_executed"],
		"before_week": entry["before_week"], "phase_log": entry["phase_log"],
		"requested_state": entry["requested_state"], "school_script_requests": entry["school_script_requests"]}
	for key in ["after", "branch", "learning_draws", "rand_state", "display_request", "skill_display_needed",
			"result_fields_completed", "week_pending"]:
		result[key] = role[key]
	return result.duplicate(true)


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "authorizes_persistent_write": false}
