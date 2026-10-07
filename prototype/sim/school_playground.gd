extends RefCounted
## Local remake playground. Restores commands, never decoded internal snapshots.

const Session := preload("res://sim/new_game_school_session.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const RULE_PATHS := {
	"school":"res://data/new_game_school_rules.json",
	"growth":"res://data/school_course_settlement_rules.json",
	"confirmation":"res://data/school_course_confirmation_rules.json",
	"result":"res://data/school_course_result_handoff_rules.json"}
const SAVE_PATH := "user://school_playground.json"
const MAX_COMMANDS := 512
const MAX_BYTES := 262144

var session: Session
var _commands: Array = []
var _rules: Dictionary = {}
var _fingerprints: Dictionary = {}


func _init() -> void:
	for key in RULE_PATHS:
		_rules[key] = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(RULE_PATHS[key])))
		_fingerprints[key] = FileAccess.get_sha256(RULE_PATHS[key])


func start() -> Dictionary:
	var fresh := Session.new()
	var rules: Dictionary = _rules["school"]
	var result := fresh.initialize_course_example(rules["origin_rules"],rules["course_rules"],rules)
	if not result["supported"]:
		return result
	session = fresh
	_commands = []
	return {"supported":true,"status":"started"}


func stage() -> String:
	if session == null:
		return "uninitialized"
	if not session.read_result_handoff().is_empty():
		return "completed"
	if not session.read_confirmation().is_empty():
		return "confirmed"
	if not session.read_settlement().is_empty():
		return "grown"
	return "planning"


func execute(command: Variant) -> Dictionary:
	if session == null:
		return _failure("not_started")
	if not command is Dictionary or not _valid_command(command):
		return _failure("invalid_command")
	if _commands.size() >= MAX_COMMANDS:
		return _failure("save_command_limit")
	var previous := session.revision()
	var result := _dispatch(command)
	if result["supported"] and session.revision() != previous:
		_commands.append(command.duplicate(true))
	return result


func _dispatch(command: Dictionary) -> Dictionary:
	match command["op"]:
		"move":
			var input := command.duplicate(true)
			input.erase("op")
			return session.move_member(input,session.revision())
		"mode":
			return session.set_class_mode(command["group"],command["teaching"],session.revision())
		"course":
			return session.assign_course(command["group"],command["course"],session.revision())
		"grow":
			return session.settle_courses(_rules["growth"],session.revision())
		"confirm":
			return session.confirm_courses(_rules["confirmation"],session.revision())
		"complete":
			return session.complete_course_result(_rules["result"],session.revision())
	return _failure("invalid_command")


static func _valid_command(command: Dictionary) -> bool:
	var keys: Array
	match command.get("op"):
		"move":
			keys = ["op","kind","member_id","target_group","target_slot"]
			if command.get("kind") not in ["student","teacher"] or not _integer(command.get("member_id"),1,118) \
					or not _integer(command.get("target_group"),-1,4) or not _integer(command.get("target_slot"),-1,3):
				return false
		"mode":
			keys = ["op","group","teaching"]
			if not _integer(command.get("group"),0,4) or not command.get("teaching") is bool:
				return false
		"course":
			keys = ["op","group","course"]
			if not _integer(command.get("group"),0,4) or not _integer(command.get("course"),10,12):
				return false
		"grow","confirm","complete":
			keys = ["op"]
		_:
			return false
	return command.size() == keys.size() and keys.all(func(key): return command.has(key))


static func _integer(value: Variant, low: int, high: int) -> bool:
	return value is int and value >= low and value <= high


func state() -> Dictionary:
	if session == null:
		return {}
	return {"snapshot":session.read_snapshot(),"growth":session.read_growth_records(),
		"confirmation":session.read_confirmation_records(),"result":session.read_result_handoff(),
		"counts":session.read_mvp_counts(),"revision":session.revision()}


func export_save() -> Dictionary:
	if session == null:
		return {}
	return {"version":1,"context":"school_playground_4_4","rules":_fingerprints.duplicate(true),
		"commands":_commands.duplicate(true),"state_sha256":JSON.stringify(state(),"",true).sha256_text()}


func restore(payload: Variant) -> Dictionary:
	if not payload is Dictionary or payload.size() != 5 \
			or not ["version","context","rules","commands","state_sha256"].all(func(k): return payload.has(k)):
		return _failure("invalid_save")
	if not _integer(payload["version"],1,1) or payload["context"] != "school_playground_4_4":
		return _failure("unsupported_save_version")
	if payload["rules"] != _fingerprints:
		return _failure("save_rules_changed")
	if not payload["commands"] is Array or payload["commands"].size() > MAX_COMMANDS \
			or not payload["state_sha256"] is String or payload["state_sha256"].length() != 64:
		return _failure("invalid_save")
	var candidate = get_script().new()
	var begun: Dictionary = candidate.start()
	if not begun["supported"]:
		return begun
	for command in payload["commands"]:
		var previous: int = candidate.session.revision()
		var result: Dictionary = candidate.execute(command)
		if not result["supported"] or candidate.session.revision() == previous:
			return _failure("save_command_rejected")
	if candidate.export_save()["state_sha256"] != payload["state_sha256"]:
		return _failure("save_state_mismatch")
	session = candidate.session
	_commands = candidate._commands.duplicate(true)
	return {"supported":true,"status":"restored"}


func restore_text(content: String) -> Dictionary:
	if content.to_utf8_buffer().size() > MAX_BYTES:
		return _failure("save_too_large")
	var json := JSON.new()
	if json.parse(content) != OK:
		return _failure("invalid_save_json")
	return restore(Roles._integers(json.data))


func _read(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return _failure("save_missing")
	var file := FileAccess.open(path,FileAccess.READ)
	if file == null:
		return _failure("save_read_failed")
	if file.get_length() > MAX_BYTES:
		return _failure("save_too_large")
	return restore_text(file.get_as_text())


func load_file(path := SAVE_PATH) -> Dictionary:
	var result := _read(path)
	if result["supported"]:
		return result
	var backup := _read(path+".bak")
	if backup["supported"]:
		return {"supported":true,"status":"recovered_backup","primary_reason":result["reason"]}
	return result


func save_file(path := SAVE_PATH) -> Dictionary:
	var payload := export_save()
	if payload.is_empty():
		return _failure("not_started")
	var content := JSON.stringify(payload,"  ",true)+"\n"
	if content.to_utf8_buffer().size() > MAX_BYTES:
		return _failure("save_too_large")
	var temporary := path+".tmp"
	var file := FileAccess.open(temporary,FileAccess.WRITE)
	if file == null:
		return _failure("save_write_failed")
	file.store_string(content)
	file.flush()
	var write_error := file.get_error()
	file.close()
	if write_error != OK:
		return _failure("save_write_failed")
	# Existing valid saves rotate to backup; a corrupt primary cannot replace it.
	var previous := ""
	if FileAccess.file_exists(path):
		var checker = get_script().new()
		var valid: Dictionary = checker._read(path)
		previous = path+".bak" if valid["supported"] else path+".corrupt"
		if FileAccess.file_exists(previous):
			if previous.ends_with(".corrupt"):
				return _failure("corrupt_copy_exists")
			if DirAccess.remove_absolute(ProjectSettings.globalize_path(previous)) != OK:
				return _failure("save_replace_failed")
		if DirAccess.rename_absolute(ProjectSettings.globalize_path(path),ProjectSettings.globalize_path(previous)) != OK:
			return _failure("save_replace_failed")
	var published := DirAccess.rename_absolute(ProjectSettings.globalize_path(temporary),ProjectSettings.globalize_path(path))
	if published != OK:
		if not previous.is_empty():
			DirAccess.rename_absolute(ProjectSettings.globalize_path(previous),ProjectSettings.globalize_path(path))
		return _failure("save_replace_failed")
	return {"supported":true,"status":"saved"}


static func _failure(reason: String) -> Dictionary:
	return {"supported":false,"reason":reason}
