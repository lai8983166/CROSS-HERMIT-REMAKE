class_name TacticsExitHandshake
extends RefCounted
## Post-VM subset of 454CF0 -> 453F10, checked against original x86 emulation.
## Synthetic replay only: it never authorizes dispatch or persistent writes.


static func step(previous: Dictionary, external: Dictionary) -> Dictionary:
	var state := previous.duplicate(true)
	var required := ["transition_phase", "script_phase", "script_control_active",
		"exit_flag", "script_completion_phase", "finish_flags", "result_selector",
		"fade_in_value", "fade_out_value"]
	for key in required:
		if not state.has(key):
			return _unsupported("missing_" + key)
	for key in ["fade_step", "animation_ready"]:
		if not external.has(key):
			return _unsupported("missing_external_" + key)
	var delta := int(external["fade_step"])
	if delta < 0 or delta > 255 or int(state["result_selector"]) not in range(6):
		return _unsupported("outside_audited_input_range")
	for key in ["fade_in_value", "fade_out_value"]:
		if int(state[key]) < -32768 or int(state[key]) > 32767:
			return _unsupported("outside_signed_short_range")
	var flags: Array = state["finish_flags"]
	if flags.size() != 3:
		return _unsupported("missing_finish_flags")
	# 454D22 returns 1 when script control is inactive. 4539B0 ignores this value.
	var script_return := 1
	if int(state["script_control_active"]) != 0 and int(state["script_completion_phase"]) != 0:
		script_return = 0
		match int(state["script_phase"]):
			5:
				state["script_completion_phase"] = 3
				if int(state["exit_flag"]) == 1:
					flags[1] = 1
					flags[2] = 1
					state["script_phase"] = 6
				else:
					state["script_control_active"] = 0
				script_return = 1
			6:
				pass
			_:
				return _unsupported("requires_vm_or_script_work_execution")
	var transition_return := 0
	match int(state["transition_phase"]):
		4:
			flags[0] = 1
			flags[1] = 0
			state["transition_phase"] = 5
		5:
			if int(flags[1]) != 0:
				state["transition_phase"] = 15
		15:
			state["fade_in_value"] = 0
			state["transition_phase"] = 16
		16:
			state["fade_in_value"] = _short(int(state["fade_in_value"]) + delta)
			if int(state["fade_in_value"]) > 254:
				state["transition_phase"] = 18 if int(state["result_selector"]) == 0 else 17
		17:
			if bool(external["animation_ready"]):
				state["transition_phase"] = 18
		18:
			state["fade_out_value"] = 1279
			state["transition_phase"] = 19
		19:
			state["fade_out_value"] = _short(int(state["fade_out_value"]) - delta)
			if int(state["fade_out_value"]) < 0:
				state["transition_phase"] = 20
				transition_return = 1
		20:
			transition_return = 1
		_:
			return _unsupported("outside_post_vm_transition_subset")
	return {"supported": true, "state": state,
		"script_function_return": script_return,
		"transition_function_return": transition_return,
		"authorizes_persistent_write": false}

static func _short(value: int) -> int:
	var bits := value & 0xffff
	return bits - 65536 if bits >= 32768 else bits


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "authorizes_persistent_write": false}
