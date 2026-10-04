class_name CampaignResultState
extends RefCounted
## Shared in-memory campaign state for the audited result replay subset.
## Owns calculation and publication; callers cannot submit arbitrary after-images.
## No original process/save authority or completed school interaction is inferred.

const Transaction = preload("res://sim/result_transaction_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const Week = preload("res://sim/week_settlement_replay.gd")
const Layout = preload("res://sim/campaign_school_layout.gd")
const Join = preload("res://sim/roster_join_replay.gd")
const Continuation = preload("res://sim/school_return_continuation.gd")

var _snapshot: Dictionary = {}
var _rules: Dictionary = {}
var _sessions: Dictionary = {}
var _probes: Dictionary = {}
var _returns: Dictionary = {}
var _active := ""
var _active_return := ""
var _revision := 0
var _journal: Array = []


func initialize(snapshot: Dictionary, rules: Dictionary) -> bool:
	if not _snapshot.is_empty() or not rules.get("role") is Dictionary or not rules.get("week") is Dictionary:
		return false
	if not Roles._validate_snapshot(snapshot).is_empty() or not Roles._validate_rules(rules["role"]).is_empty() \
			or not Week._validate(Transaction._week_input(snapshot), rules["week"]).is_empty():
		return false
	if snapshot.has("school") and not Layout.validate(snapshot, rules["week"]).is_empty():
		return false
	_snapshot = snapshot.duplicate(true)
	_rules = rules.duplicate(true)
	return true


func read_snapshot() -> Dictionary:
	return _snapshot.duplicate(true)


func read_school_snapshot() -> Dictionary:
	if not _snapshot.has("school"):
		return _unsupported("missing_school_layout")
	return Layout.school_view(_snapshot, _rules["week"])


func revision() -> int:
	return _revision


func journal() -> Array:
	return _journal.duplicate(true)


func begin_result(instance_id: String, context: Dictionary, source_inputs: Dictionary = {}) -> Dictionary:
	if _snapshot.is_empty() or instance_id.is_empty():
		return _unsupported("missing_campaign_or_instance")
	if _probes.has(instance_id) or _returns.has(instance_id):
		return _unsupported("instance_belongs_to_school_probe")
	if _sessions.has(instance_id):
		if _sessions[instance_id]["context"] != context or _sessions[instance_id]["source_inputs"] != source_inputs:
			return _unsupported("instance_input_conflict")
		return _view(_sessions[instance_id], "duplicate")
	if not _active.is_empty() or not _active_return.is_empty():
		return _unsupported("another_result_pending")
	# The calculator validates the entire state12 context and both role/week
	# inputs before it can produce any growth. No source fixture is a commit token.
	var before := _snapshot.duplicate(true)
	if _snapshot.has("school"):
		var projected := Layout.result_view(_snapshot, context.get("participant_ids"), _rules["week"])
		if not projected["supported"]:
			return projected
		before = projected["snapshot"]
	var transaction := Transaction.new()
	var result := transaction.begin(instance_id, context, before, _rules)
	if not result["supported"]:
		return result
	var staged := _stage_result_publication(result["after"], result["phase_log"])
	if not staged["supported"]:
		return staged
	var session := {"context": context.duplicate(true), "source_inputs": source_inputs.duplicate(true), "transaction": transaction,
		"result": result.duplicate(true), "completed": false, "completed_revision": 0}
	_sessions[instance_id] = session
	_active = instance_id
	_publish(instance_id, staged["after"], staged["phases"], session["source_inputs"])
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
	if result["completed"]:
		# Publish post fields and optional complete week as one shared snapshot.
		# The phase journal retains their native order and intermediate before/after.
		var staged := _stage_result_publication(result["after"], result["phase_log"].slice(1))
		if not staged["supported"]:
			return staged
		_publish(instance_id, staged["after"], staged["phases"], session["source_inputs"])
		session["completed"] = true
		session["completed_revision"] = _revision
		_active = ""
	session["result"] = result.duplicate(true)
	return _view(session, result["status"])


# These methods deliberately model the direct calls in the same-CPU layout
# evidence. They do not consume state6/7, run ADV END, or dispatch school tasks.
func probe_school_join(instance_id: String, result_instance: String, context: Dictionary) -> Dictionary:
	var input := {"kind": "join", "parent": result_instance, "context": context.duplicate(true)}
	var cached := _probe_guard(instance_id, input)
	if not cached.is_empty():
		return cached
	if not _active.is_empty() or not _active_return.is_empty() or not _sessions.has(result_instance):
		return _unsupported("pending_or_missing_result_parent")
	var parent: Dictionary = _sessions[result_instance]
	if not parent["completed"] or parent["completed_revision"] != _revision \
			or int(parent["result"]["requested_state"]) != 6 \
			or int(parent["result"]["branch"]) != 0 or parent["result"]["week_executed"]:
		return _unsupported("outside_completed_ordinary_result_probe")
	var view := read_school_snapshot()
	if not view["supported"]:
		return view
	var join_rules := {"week": _rules["week"].duplicate(true),
		"level_thresholds": _rules["role"]["level_thresholds"].duplicate(true),
		"learned_points": _rules["role"]["skills"].map(func(skill): return skill["learned_points"])}
	var result := Join.new().apply_once(instance_id, context, view["snapshot"], join_rules)
	if not result["supported"]:
		return result
	var merged := Layout.merge_school(_snapshot, result["after"], _rules["week"])
	if not merged["supported"]:
		return merged
	var sources := {"direct_source_call": "Chapter020 opcode144", "result_instance": result_instance,
		"result_context": parent["context"].duplicate(true),
		"result_source_inputs": parent["source_inputs"].duplicate(true), "join_context": context.duplicate(true)}
	_publish_probe(instance_id, input, result, merged["snapshot"], "direct_join_probe", sources)
	return _probe_view(_probes[instance_id], result["status"])


func probe_school_week(instance_id: String, join_instance: String) -> Dictionary:
	var input := {"kind": "week", "parent": join_instance}
	var cached := _probe_guard(instance_id, input)
	if not cached.is_empty():
		return cached
	if not _active.is_empty() or not _active_return.is_empty() or not _probes.has(join_instance) \
			or _probes[join_instance]["input"]["kind"] != "join" \
			or _probes[join_instance]["revision"] != _revision:
		return _unsupported("pending_missing_or_stale_join_parent")
	var view := read_school_snapshot()
	if not view["supported"]:
		return view
	var result := Week.project(view["snapshot"], _rules["week"])
	if not result["supported"]:
		return result
	var merged := Layout.merge_school(_snapshot, result["after"], _rules["week"])
	if not merged["supported"]:
		return merged
	result["status"] = "projected_once"
	var sources := {"direct_source_call": "0x4d3510", "join_instance": join_instance,
		"join_source_inputs": _probes[join_instance]["source_inputs"].duplicate(true)}
	_publish_probe(instance_id, input, result, merged["snapshot"], "direct_week_probe", sources)
	return _probe_view(_probes[instance_id], result["status"])


func begin_school_return(instance_id: String, result_instance: String) -> Dictionary:
	if _snapshot.is_empty() or instance_id.is_empty():
		return _unsupported("missing_campaign_or_return_instance")
	if _sessions.has(instance_id) or _probes.has(instance_id):
		return _unsupported("instance_belongs_to_another_operation")
	if _returns.has(instance_id):
		return _school_view(_returns[instance_id], "duplicate") if _returns[instance_id]["parent"] == result_instance \
			else _unsupported("instance_input_conflict")
	if not _active.is_empty() or not _active_return.is_empty() or not _sessions.has(result_instance):
		return _unsupported("pending_or_missing_result_parent")
	var parent: Dictionary = _sessions[result_instance]
	if not parent["completed"] or parent["completed_revision"] != _revision \
			or int(parent["result"]["branch"]) != 0 or parent["result"]["requested_state"] != 6 \
			or parent["result"]["week_executed"]:
		return _unsupported("outside_completed_ordinary_result_return")
	var calculator := Continuation.new()
	var result := calculator.begin(instance_id, _snapshot, _rules)
	if not result["supported"]:
		return result
	var reason := _validate_school_publication(result, result["phase_log"])
	if not reason.is_empty():
		return _unsupported(reason)
	var session := {"parent": result_instance, "calculator": calculator, "result": result.duplicate(true),
		"source_inputs": {"result_instance": result_instance, "result_context": parent["context"].duplicate(true),
			"result_source_inputs": parent["source_inputs"].duplicate(true)}, "completed": false}
	_returns[instance_id] = session
	_active_return = instance_id
	_publish(instance_id, result["after"], result["phase_log"], session["source_inputs"])
	return _school_view(session, result["status"])


func advance_school_return(instance_id: String, chapter_key_ready: bool, continue_ready: bool, school_fade_ready: bool) -> Dictionary:
	if not _returns.has(instance_id):
		return _unsupported("missing_return_instance")
	var session: Dictionary = _returns[instance_id]
	if session["completed"]:
		return _school_view(session, "duplicate")
	if _active_return != instance_id:
		return _unsupported("return_is_not_active")
	var result: Dictionary = session["calculator"].advance(instance_id, chapter_key_ready, continue_ready, school_fade_ready)
	if not result["supported"]:
		return result
	var phases: Array = result["phase_log"].slice(session["result"]["phase_log"].size())
	var reason := _validate_school_publication(result, phases)
	if not reason.is_empty():
		return _unsupported(reason)
	if not phases.is_empty():
		var sources: Dictionary = session["source_inputs"].duplicate(true)
		sources["declared_readiness"] = {"chapter_key_ready": chapter_key_ready,
			"continue_ready": continue_ready, "school_fade_ready": school_fade_ready}
		_publish(instance_id, result["after"], phases, sources)
	session["result"] = result.duplicate(true)
	if result["completed"]:
		session["completed"] = true
		_active_return = ""
	return _school_view(session, result["status"])


func _validate_school_publication(result: Dictionary, phases: Array) -> String:
	var candidate := _snapshot.duplicate(true)
	for phase in phases:
		if phase["before"] != candidate:
			return "school_phase_before_conflict"
		var reason := Layout.validate(phase["after"], _rules["week"])
		if not reason.is_empty():
			return reason
		candidate = phase["after"].duplicate(true)
	return "" if candidate == result["after"] else "school_phase_publication_mismatch"


func _school_view(session: Dictionary, status: String) -> Dictionary:
	var result: Dictionary = session["result"].duplicate(true)
	result["status"] = status
	return {"supported": true, "status": status, "result": result,
		"campaign_snapshot": read_snapshot(), "campaign_revision": _revision,
		"execution_scope": "isolated_sourced_return_checkpoints", "school_constructed": result["school_constructed"],
		"school_initialized": false, "live_witness": false, "authorizes_persistent_write": false}


func _probe_guard(instance_id: String, input: Dictionary) -> Dictionary:
	if _snapshot.is_empty() or instance_id.is_empty():
		return _unsupported("missing_campaign_or_instance")
	if _sessions.has(instance_id):
		return _unsupported("instance_belongs_to_result")
	if _returns.has(instance_id):
		return _unsupported("instance_belongs_to_school_return")
	if _probes.has(instance_id):
		if _probes[instance_id]["input"] != input:
			return _unsupported("instance_input_conflict")
		return _probe_view(_probes[instance_id], "duplicate")
	return {}


func _publish_probe(instance_id: String, input: Dictionary, result: Dictionary, after: Dictionary,
		phase: String, source_inputs: Dictionary) -> void:
	_publish(instance_id, after, [{"phase": phase, "before": read_snapshot(), "after": after.duplicate(true)}], source_inputs)
	_probes[instance_id] = {"input": input.duplicate(true), "result": result.duplicate(true),
		"revision": _revision, "source_inputs": source_inputs.duplicate(true)}


func _probe_view(entry: Dictionary, status: String) -> Dictionary:
	var result: Dictionary = entry["result"].duplicate(true)
	result["status"] = status
	return {"supported": true, "status": status, "result": result, "operation_kind": entry["input"]["kind"],
		"campaign_snapshot": read_snapshot(), "campaign_revision": _revision,
		"execution_scope": "isolated_direct_data_probe", "chapter_completed": false,
		"live_witness": false, "authorizes_persistent_write": false, "school_initialized": false}


func _stage_result_publication(after: Dictionary, phases: Array) -> Dictionary:
	if not _snapshot.has("school"):
		return {"supported": true, "after": after.duplicate(true), "phases": phases.duplicate(true)}
	var candidate := _snapshot.duplicate(true)
	var logs := []
	for phase in phases:
		var merged := Layout.merge_result(candidate, phase["after"], _rules["week"])
		if not merged["supported"]:
			return merged
		var record: Dictionary = phase.duplicate(true)
		record["before"] = candidate.duplicate(true)
		candidate = merged["snapshot"]
		record["after"] = candidate.duplicate(true)
		logs.append(record)
	var final := Layout.merge_result(candidate, after, _rules["week"])
	if not final["supported"]:
		return final
	if final["snapshot"] != candidate:
		return _unsupported("result_phase_publication_mismatch")
	return {"supported": true, "after": candidate, "phases": logs}


func _publish(instance_id: String, after: Dictionary, phases: Array, source_inputs: Dictionary) -> void:
	_snapshot = after.duplicate(true)
	_revision += 1
	for phase in phases:
		var record: Dictionary = phase.duplicate(true)
		record["instance_id"] = instance_id
		record["revision"] = _revision
		record["source_inputs"] = source_inputs.duplicate(true)
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
