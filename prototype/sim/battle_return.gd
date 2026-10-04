class_name BattleReturn
extends RefCounted
## Separate local terminal facts from a sourced intermediate script signal.
## Neither input proves task exit or a result branch. An explicit source replay
## can coordinate the audited task/round gates and shared in-memory result state.

const Transition = preload("res://sim/tactics_result_transition.gd")
const RoundGate = preload("res://sim/battle_round_gate.gd")
const Week = preload("res://sim/week_settlement_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const Campaign = preload("res://sim/campaign_result_state.gd")

var _terminal_snapshot: Dictionary = {}
var _script_signal: Dictionary = {}
var _gate_input: Dictionary = {}
var _result_gate: Dictionary = {}
var _result_instance := ""
var _result_context: Dictionary = {}
var _campaign: Campaign
var _school_return_instance := ""
var _replay_status := ""


func accept_terminal_snapshot(snapshot: Dictionary) -> bool:
	if not _terminal_snapshot.is_empty() or snapshot.is_empty():
		return false
	if not snapshot.has("frame") or not snapshot.has("winner") or not snapshot.has("units"):
		return false
	if not Week._bounded(snapshot["frame"], 0, 0x7fffffff) or not Week._bounded(snapshot["winner"], 0, 1) \
			or not snapshot["units"] is Array:
		return false
	_terminal_snapshot = snapshot.duplicate(true)
	return true


func accept_script_signal(script_event: Dictionary) -> bool:
	if not _script_signal.is_empty() or not _result_instance.is_empty():
		return false
	if String(script_event.get("script", "")).is_empty() \
			or int(script_event.get("opcode", -1)) != 112 \
			or String(script_event.get("interpretation", "")) != "intermediate_script_signal_only" \
			or int(script_event.get("instruction_offset", -1)) < 0 \
			or int(script_event.get("source_tick", -1)) < 0:
		return false
	var cells: Array = script_event.get("raw_cells", [])
	if cells.size() != 3:
		return false
	_script_signal = script_event.duplicate(true)
	return true


func status() -> String:
	if _terminal_snapshot.is_empty():
		return "pending_terminal"
	if not _replay_status.is_empty():
		return _replay_status
	return "pending_task_exit"


func inputs() -> Dictionary:
	var result := {
		"terminal_snapshot": _terminal_snapshot.duplicate(true),
		"script_signal": _script_signal.duplicate(true),
	}
	if not _result_gate.is_empty():
		result["result_replay_gate"] = _result_gate.duplicate(true)
	return result


func prepare_result_replay(exit_frame: Dictionary, dispatch_context: Dictionary,
		round_before: Dictionary, round_table: Dictionary, state11_complete: bool) -> Dictionary:
	if _terminal_snapshot.is_empty():
		return _unsupported("pending_terminal")
	# Validate primitive types before older source projection helpers can coerce
	# them. END/cleanup and state11 completion remain declared replay inputs.
	for spec in [["transition_function_return", 0, 1], ["transition_phase", 0, 20],
			["script_phase", 0, 6], ["exit_flag", 0, 1]]:
		if not Week._bounded(exit_frame.get(spec[0]), spec[1], spec[2]):
			return _unsupported("invalid_exit_" + spec[0])
	if not Week._vector(exit_frame.get("finish_flags"), 3, 0, 1):
		return _unsupported("invalid_exit_flags")
	for spec in [["scene_id", 0, 32767], ["next_scene", 0, 32767], ["task_phase", 0, 20], ["request_pending", 0, 1]]:
		if not Week._bounded(dispatch_context.get(spec[0]), spec[1], spec[2]):
			return _unsupported("invalid_dispatch_" + spec[0])
	for key in ["network_mode", "exit_to_menu"]:
		if not dispatch_context.get(key) is bool:
			return _unsupported("invalid_dispatch_" + key)
	var input := {"exit_frame": exit_frame.duplicate(true), "dispatch_context": dispatch_context.duplicate(true),
		"round_before": round_before.duplicate(true), "round_table": round_table.duplicate(true),
		"state11_complete": state11_complete}
	if not _result_gate.is_empty():
		if _gate_input != input:
			return _unsupported("result_gate_input_conflict")
		return _gate_view("duplicate")
	var transition := Transition.step(exit_frame, dispatch_context)
	if not transition["supported"]:
		return transition
	if transition["requested_state"] != 11:
		_replay_status = transition["status"]
		return {"supported": true, "status": _replay_status, "requested_state": transition["requested_state"],
			"authorizes_persistent_write": false, "live_witness": false}
	if not state11_complete:
		_replay_status = "pending_state11"
		return {"supported": true, "status": _replay_status, "requested_state": 11,
			"authorizes_persistent_write": false, "live_witness": false}
	if not Week._vector(round_before.get("temp_roster"), 100, -32768, 32767):
		return _unsupported("invalid_round_roster")
	var gate := RoundGate.step(round_before, round_table, true)
	if not gate["supported"]:
		return gate
	_gate_input = input
	_result_gate = {"requested_state": gate["requested_state"], "round_after": gate["after"].duplicate(true),
		"state_requests": [11, 10, gate["requested_state"]],
		"source_functions": ["0x451670", "0x439e30", "0x49e2b0", "0x4bd660", "0x4b8ff0"],
		"current": int(round_before["current"]), "total": int(round_before["total"])}
	_replay_status = "pending_result_transaction" if gate["requested_state"] == 12 else "pending_next_round"
	return _gate_view(_replay_status)


func begin_result_replay(instance_id: String, context: Dictionary, campaign: Campaign) -> Dictionary:
	if _result_gate.is_empty() or _result_gate["requested_state"] != 12:
		return _unsupported("pending_state12_result_gate")
	for pair in [["task_state", 12], ["current", _result_gate["current"]], ["total", _result_gate["total"]]]:
		if not Week._integer(context.get(pair[0])) or int(context[pair[0]]) != pair[1]:
			return _unsupported("result_context_does_not_match_gate")
	var reason := _validate_terminal_ids(context)
	if not reason.is_empty():
		return _unsupported(reason)
	if campaign == null or instance_id.is_empty():
		return _unsupported("missing_campaign_or_instance")
	if not _result_instance.is_empty() and (_result_instance != instance_id \
			or _result_context != context or _campaign != campaign):
		return _unsupported("return_instance_input_conflict")
	var result := campaign.begin_result(instance_id, context, {"terminal_snapshot": _terminal_snapshot,
		"result_gate": _result_gate, "script_signal": _script_signal})
	if not result["supported"]:
		return result
	_result_instance = instance_id
	_result_context = context.duplicate(true)
	_campaign = campaign
	if _school_return_instance.is_empty():
		_replay_status = "result_completed" if result["result"]["completed"] else "pending_result_confirmation"
	return result


func finish_result_replay(instance_id: String, confirmed: bool, mvp_ready: bool) -> Dictionary:
	if _campaign == null or _result_instance != instance_id:
		return _unsupported("missing_bound_result_instance")
	var result := _campaign.finish_result(instance_id, confirmed, mvp_ready)
	if result["supported"] and _school_return_instance.is_empty():
		_replay_status = "result_completed" if result["result"]["completed"] else result["status"]
	return result


func begin_school_return_replay(instance_id: String) -> Dictionary:
	if _campaign == null or _result_instance.is_empty():
		return _unsupported("missing_bound_result_instance")
	if not _school_return_instance.is_empty() and _school_return_instance != instance_id:
		return _unsupported("school_return_instance_conflict")
	var result := _campaign.begin_school_return(instance_id, _result_instance)
	if result["supported"]:
		_school_return_instance = instance_id
		_replay_status = "school_constructed" if result["result"]["completed"] else "pending_school_return"
	return result


func advance_school_return_replay(instance_id: String, chapter_key_ready: bool, continue_ready: bool, school_fade_ready: bool) -> Dictionary:
	if _campaign == null or _school_return_instance != instance_id:
		return _unsupported("missing_bound_school_return")
	var result := _campaign.advance_school_return(instance_id, chapter_key_ready, continue_ready, school_fade_ready)
	if result["supported"]:
		_replay_status = "school_constructed" if result["result"]["completed"] else "pending_school_return"
	return result


func _validate_terminal_ids(context: Dictionary) -> String:
	if not _terminal_snapshot.get("units") is Array or _terminal_snapshot["units"].is_empty() \
			or not context.get("round_ids") is Array or context["round_ids"].is_empty():
		return "missing_terminal_or_round_units"
	var ids: Array = []
	var indices := {}
	for unit in _terminal_snapshot["units"]:
		if not unit is Dictionary or not Week._bounded(unit.get("faction"), 0, 1) \
				or not Week._bounded(unit.get("battle_index"), 0, 67) or indices.has(int(unit["battle_index"])):
			return "invalid_terminal_unit_identity"
		indices[int(unit["battle_index"])] = true
		if int(unit["faction"]) != 0:
			continue
		if not Week._bounded(unit.get("character_id"), 1, 12) or ids.has(int(unit["character_id"])):
			return "missing_or_duplicate_terminal_character_id"
		ids.append(int(unit["character_id"]))
	if not Week._vector(context["round_ids"], ids.size(), 1, 12):
		return "terminal_round_id_mismatch"
	var expected: Array = Roles._integers(context["round_ids"])
	ids.sort()
	expected.sort()
	return "" if ids == expected else "terminal_round_id_mismatch"


func _gate_view(view_status: String) -> Dictionary:
	var result := _result_gate.duplicate(true)
	result.merge({"supported": true, "status": view_status, "execution_scope": "isolated_campaign_replay",
		"authorizes_persistent_write": false, "live_witness": false})
	return result


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "authorizes_persistent_write": false, "live_witness": false}
