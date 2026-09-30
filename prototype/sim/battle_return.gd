class_name BattleReturn
extends RefCounted
## Separate local terminal facts from a sourced script exit. Neither input is a
## result-branch contract; no profile/calendar mutation occurs at this boundary.

var _terminal_snapshot: Dictionary = {}
var _script_exit_request: Dictionary = {}


func accept_terminal_snapshot(snapshot: Dictionary) -> bool:
	if not _terminal_snapshot.is_empty() or snapshot.is_empty():
		return false
	if not snapshot.has("frame") or not snapshot.has("winner") or not snapshot.has("units"):
		return false
	_terminal_snapshot = snapshot.duplicate(true)
	return true


func accept_script_exit_request(request: Dictionary) -> bool:
	if not _script_exit_request.is_empty():
		return false
	if String(request.get("script", "")).is_empty() \
			or int(request.get("opcode", -1)) != 112 \
			or int(request.get("instruction_offset", -1)) < 0 \
			or int(request.get("source_tick", -1)) < 0:
		return false
	var cells: Array = request.get("raw_cells", [])
	if cells.size() != 3:
		return false
	_script_exit_request = request.duplicate(true)
	return true


func status() -> String:
	if _terminal_snapshot.is_empty():
		return "pending_terminal"
	if _script_exit_request.is_empty():
		return "pending_script_exit"
	return "pending_result_branch"


func inputs() -> Dictionary:
	return {
		"terminal_snapshot": _terminal_snapshot.duplicate(true),
		"script_exit_request": _script_exit_request.duplicate(true),
	}
