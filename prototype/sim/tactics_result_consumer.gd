class_name TacticsResultConsumer
extends RefCounted
## Source-derived 453CB0..453CDD control flow, not native execution evidence.
## The input is the retained [EBP-8] completion value, NOT an outcome selector
## or a WaitForSingleObject return. Scheduling is explicit, never tied to FPS.

var _phase := "idle"
var _iteration := 0
var _ordinal := 0
var _completion := 0
var _consumed := false


func begin_iteration(completion_value: int) -> Dictionary:
	if _phase not in ["idle", "continue_loop"]:
		return _refused("iteration_already_pending_or_returned")
	if completion_value < -2147483648 or completion_value > 4294967295:
		return _refused("completion_outside_u32_bits")
	_iteration += 1
	_completion = completion_value & 0xffffffff
	_consumed = false
	_ordinal = 1
	_phase = "waiting"
	return _result()


func resume_wait(iteration: int, ordinal: int, wait_status: int) -> Dictionary:
	if _phase != "waiting" or iteration != _iteration or ordinal != _ordinal:
		return _refused("stale_or_out_of_order_resume")
	# Original code ignores the OS wait status. The remake adapter accepts only
	# a successful event completion; failure/timeout must not masquerade as one.
	if wait_status != 0:
		return _refused("wait_did_not_complete")
	if _ordinal == 1:
		_consumed = true
		_phase = "continue_loop" if _completion == 0 else "record_pending"
	elif _ordinal == 2:
		_ordinal = 3
	else:
		_phase = "returned"
	return _result()


func replay_record_returned(iteration: int, call_return: int) -> Dictionary:
	if _phase != "record_pending" or iteration != _iteration:
		return _refused("record_call_not_pending")
	if call_return < -2147483648 or call_return > 4294967295:
		return _refused("record_return_outside_u32_bits")
	# 4967B0 is called even when recording is disabled, and its return is ignored.
	# The record bytes and file IO remain the caller's responsibility. No rewards.
	_phase = "waiting"
	_ordinal = 2
	return _result()


func snapshot() -> Dictionary:
	return _result()


func _result() -> Dictionary:
	var action := "none"
	match _phase:
		"waiting": action = "wait"
		"continue_loop": action = "continue_loop"
		"record_pending": action = "call_replay_record"
		"returned": action = "return_completed"
	var output := {"supported": true, "phase": _phase, "action": action,
		"iteration": _iteration, "wait_ordinal": _ordinal,
		"completion_value": _completion, "result_consumed": _consumed,
		"function_returned": _phase == "returned",
		"evidence_kind": "source_derived_remake_logic",
		"native_wait_verified": false, "authorizes_persistent_write": false}
	if _phase == "waiting": output["delay"] = 0
	if _phase == "returned": output["scene_function_return"] = 1
	return output


func _refused(reason: String) -> Dictionary:
	var output := _result()
	output["supported"] = false
	output["reason"] = reason
	return output
