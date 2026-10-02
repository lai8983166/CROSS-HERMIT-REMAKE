class_name TacticsResultTransition
extends RefCounted
## Scene-5 subset of 451670 -> 439E30 -> 49E2B0, after local task exit.
## Explicit isolated replay context; no live evidence or persistent authority.


static func step(exit_frame: Dictionary, context: Dictionary) -> Dictionary:
	for key in ["transition_function_return", "transition_phase", "script_phase",
			"exit_flag", "finish_flags"]:
		if not exit_frame.has(key):
			return _unsupported("missing_" + key)
	for key in ["scene_id", "next_scene", "network_mode", "task_phase", "request_pending", "exit_to_menu"]:
		if not context.has(key):
			return _unsupported("missing_context_" + key)
	if int(context["scene_id"]) != 5 or int(context["next_scene"]) != 0 \
			or bool(context["network_mode"]) or int(context["task_phase"]) != 2:
		return _unsupported("outside_scene5_dispatch_subset")
	var flags: Array = exit_frame["finish_flags"]
	if flags.size() != 3:
		return _unsupported("missing_finish_flags")
	var output := {"supported": true, "status": "pending_task_exit",
		"request_pending": int(context["request_pending"]), "requested_state": -1,
		"dispatch_target_va": 0, "authorizes_persistent_write": false}
	if int(exit_frame["transition_function_return"]) == 0:
		return output
	if int(exit_frame["transition_function_return"]) != 1 \
			or int(exit_frame["transition_phase"]) != 20 \
			or int(exit_frame["script_phase"]) != 6 \
			or int(exit_frame["exit_flag"]) != 1 or int(flags[1]) != 1:
		return _unsupported("inconsistent_terminal_script_exit")
	# 439E30 asserts if a request is already pending; do not silently replace it.
	if int(context["request_pending"]) != 0:
		return _unsupported("request_already_pending")
	output["request_pending"] = 1
	# 4517A1 checks the task's +31 flag before the scene-specific branch.
	if bool(context["exit_to_menu"]):
		output["status"] = "menu_requested"
		output["requested_state"] = 1
		output["dispatch_target_va"] = 0x45E8D0
		return output
	output["status"] = "tactics_result_requested"
	output["requested_state"] = 11
	output["dispatch_target_va"] = 0x4BD6F0
	return output


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "authorizes_persistent_write": false}
