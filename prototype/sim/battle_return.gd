class_name BattleReturn
extends RefCounted
## Separate local terminal facts from a sourced intermediate script signal.
## Neither input proves task exit or a result branch; no persistent mutation occurs.

var _terminal_snapshot: Dictionary = {}
var _script_signal: Dictionary = {}


func accept_terminal_snapshot(snapshot: Dictionary) -> bool:
	if not _terminal_snapshot.is_empty() or snapshot.is_empty():
		return false
	if not snapshot.has("frame") or not snapshot.has("winner") or not snapshot.has("units"):
		return false
	_terminal_snapshot = snapshot.duplicate(true)
	return true


func accept_script_signal(script_event: Dictionary) -> bool:
	if not _script_signal.is_empty():
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
	return "pending_task_exit"


func inputs() -> Dictionary:
	return {
		"terminal_snapshot": _terminal_snapshot.duplicate(true),
		"script_signal": _script_signal.duplicate(true),
	}
