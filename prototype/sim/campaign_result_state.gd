class_name CampaignResultState
extends RefCounted
## Shared in-memory campaign state for the audited result replay subset.
## Owns calculation and publication; callers cannot submit arbitrary after-images.
## No original process/save authority or completed school interaction is inferred.

const Transaction = preload("res://sim/result_transaction_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const Week = preload("res://sim/week_settlement_replay.gd")

var _snapshot: Dictionary = {}
var _rules: Dictionary = {}
var _sessions: Dictionary = {}
var _active := ""
var _revision := 0
var _journal: Array = []


func initialize(snapshot: Dictionary, rules: Dictionary) -> bool:
	if not _snapshot.is_empty() or not rules.get("role") is Dictionary or not rules.get("week") is Dictionary:
		return false
	if not Roles._validate_snapshot(snapshot).is_empty() or not Roles._validate_rules(rules["role"]).is_empty() \
			or not Week._validate(Transaction._week_input(snapshot), rules["week"]).is_empty():
		return false
	_snapshot = snapshot.duplicate(true)
	_rules = rules.duplicate(true)
	return true


func read_snapshot() -> Dictionary:
	return _snapshot.duplicate(true)


func revision() -> int:
	return _revision


func journal() -> Array:
	return _journal.duplicate(true)


func begin_result(instance_id: String, context: Dictionary) -> Dictionary:
	if _snapshot.is_empty() or instance_id.is_empty():
		return _unsupported("missing_campaign_or_instance")
	if _sessions.has(instance_id):
		if _sessions[instance_id]["context"] != context:
			return _unsupported("instance_input_conflict")
		return _view(_sessions[instance_id], "duplicate")
	if not _active.is_empty():
		return _unsupported("another_result_pending")
	# The calculator validates the entire state12 context and both role/week
	# inputs before it can produce any growth. No source fixture is a commit token.
	var transaction := Transaction.new()
	var result := transaction.begin(instance_id, context, _snapshot, _rules)
	if not result["supported"]:
		return result
	var session := {"context": context.duplicate(true), "transaction": transaction,
		"result": result.duplicate(true), "completed": false}
	_sessions[instance_id] = session
	_active = instance_id
	_publish(instance_id, result["after"], result["phase_log"])
	return _view(session, result["status"])


func finish_result(instance_id: String, confirmed: bool, mvp_ready: bool) -> Dictionary:
	if not _sessions.has(instance_id):
		return _unsupported("missing_result_instance")
	var session: Dictionary = _sessions[instance_id]
	if session["completed"]:
		return _view(session, "duplicate")
	if _active != instance_id:
		return _unsupported("result_is_not_active")
	var result: Dictionary = session["transaction"].finish(instance_id, confirmed, mvp_ready)
	if not result["supported"]:
		return result
	session["result"] = result.duplicate(true)
	if result["completed"]:
		# Publish post fields and optional complete week as one shared snapshot.
		# The phase journal retains their native order and intermediate before/after.
		_publish(instance_id, result["after"], result["phase_log"].slice(1))
		session["completed"] = true
		_active = ""
	return _view(session, result["status"])


func _publish(instance_id: String, after: Dictionary, phases: Array) -> void:
	_snapshot = after.duplicate(true)
	_revision += 1
	for phase in phases:
		var record: Dictionary = phase.duplicate(true)
		record["instance_id"] = instance_id
		record["revision"] = _revision
		_journal.append(record)


func _view(session: Dictionary, status: String) -> Dictionary:
	var result: Dictionary = session["result"].duplicate(true)
	result["status"] = status
	return {"supported": true, "status": status, "result": result,
		"campaign_snapshot": read_snapshot(), "campaign_revision": _revision,
		"execution_scope": "isolated_campaign_replay", "live_witness": false,
		"authorizes_persistent_write": false, "school_initialized": false}


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "live_witness": false,
		"authorizes_persistent_write": false, "school_initialized": false}
