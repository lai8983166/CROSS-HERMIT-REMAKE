extends RefCounted
## Reconstruct the October opening from the playable campaign's original commands.
const Model := preload("res://sim/school_playground.gd")
const COMMANDS := "res://data/school_year_october_commands.bin"
const OCTOBER_STATE := "880467908274453590eb9de26cd3bb8386e0510ab644cd49886fd06117731778"
const SAVE_PATH := "user://school_year_trial.json"

var _mutex := Mutex.new()
var _cancelled := false
var _completed := 0
var _total := 0


func cancel() -> void:
	_mutex.lock()
	_cancelled=true
	_mutex.unlock()


func progress() -> Array:
	_mutex.lock()
	var state := [_completed,_total,_cancelled]
	_mutex.unlock()
	return state


func _continue_replay(completed: int, total: int) -> bool:
	_mutex.lock()
	_completed=completed
	_total=total
	var proceed := not _cancelled
	_mutex.unlock()
	return proceed


func open(resume: bool) -> Dictionary:
	var model := Model.new()
	model.replay_progress=_continue_replay
	if resume:
		var loaded := model.load_week_state(SAVE_PATH)
		if loaded.supported:
			model.replay_progress=Callable()
			return {"supported":true,"model":model}
		if loaded.reason!="save_missing":return loaded
	var bytes := FileAccess.get_file_as_bytes(COMMANDS).decompress(146572,FileAccess.COMPRESSION_GZIP)
	if bytes.size()!=146572:return {"supported":false,"reason":"trial_commands_missing"}
	var commands: Variant=JSON.parse_string(bytes.get_string_from_utf8())
	if not commands is Array or commands.size()!=1421:return {"supported":false,"reason":"invalid_trial_commands"}
	var result := model.start()
	if not result.supported:return result
	for i in range(commands.size()):
		if not _continue_replay(i,commands.size()):return {"supported":false,"reason":"replay_canceled"}
		result=model.execute(Model.Roles._integers(commands[i]))
		if not result.supported:return result
	model.replay_progress=Callable()
	if model.export_save().state_sha256!=OCTOBER_STATE:return {"supported":false,"reason":"trial_opening_mismatch"}
	return {"supported":true,"model":model}
