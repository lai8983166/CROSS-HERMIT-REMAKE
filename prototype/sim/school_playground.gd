extends RefCounted
## Local remake playground. Restores commands, never decoded internal snapshots.

const Session := preload("res://sim/new_game_school_session.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const Week := preload("res://sim/week_settlement_replay.gd")
const AdventureHandoff := preload("res://sim/school_adventure_handoff.gd")
const AdventurePreparation := preload("res://sim/school_adventure_preparation.gd")
const CombatLimits := preload("res://sim/school_combat_limits.gd")
const BattleRecord := preload("res://sim/school_battle_record.gd")
const Postbattle := preload("res://sim/school_postbattle_flow.gd")
const RULE_PATHS := {
	"school":"res://data/new_game_school_rules.json",
	"growth":"res://data/school_course_settlement_rules.json",
	"confirmation":"res://data/school_course_confirmation_rules.json",
	"result":"res://data/school_course_result_handoff_rules.json",
	"week":"res://data/school_story_week_rules.json",
	"story":"res://assets/school_story/catalog.json",
	"fifth":"res://data/school_fifth_week_rules.json",
	"fifth_story":"res://assets/school_fifth_story/catalog.json",
	"planning":"res://data/school_fifth_planning_rules.json",
	"workroom":"res://assets/school_workroom/catalog.json"}
const LEGACY_KEYS := ["school","growth","confirmation","result"]
const VERSION2_KEYS := ["school","growth","confirmation","result","week","story"]
const VERSION3_KEYS := VERSION2_KEYS+["fifth","fifth_story"]
const VERSION2_OPS := ["story_start","story_next","story_prev","story_skip","week"]
const VERSION3_OPS := VERSION2_OPS+["fifth_start","fifth_next","fifth_prev","fifth_skip","fifth_finish"]
const STORY_LF_SHA := "e6d0c109295145c419a20f30d093c2bcb795ef010919f32f659419e8aa3ec98a"
const LEGACY_STORY_CRLF_SHA := "fb7a98f8bdf021f601a4001cc0b69efc021002f7e037cb4fb7b2faeef09430bf"
const SCHOOL_OPS := ["move","mode","course","grow","confirm","complete"]
const SAVE_PATH := "user://school_playground.json"
const SAVE_CONTEXTS := {
	1:"school_playground_4_4",
	2:"school_playground_story_4_4",
	3:"school_playground_fifth_4_5",
	4:"school_playground_fifth_planning_4_5",
	5:"school_playground_return_5_1",
	6:"school_playground_return_plan_5_1",
	7:"school_playground_sortie_week",
	8:"school_playground_course_week",
	9:"school_playground_may_week_three",
	10:"school_playground_may_week_four",
	11:"school_playground_mandatory_seven",
	12:"school_playground_may_five_work",
	13:"school_playground_mandatory_four",
	14:"school_playground_mandatory_six",
	15:"school_playground_mandatory_ten",
	16:"school_playground_mandatory_thirteen",
	17:"school_playground_june_five_work",
	18:"school_playground_july_work",
	19:"school_playground_mandatory_nine",
	20:"school_playground_mandatory_fourteen",
	21:"school_playground_july_five_work",
	22:"school_playground_august_courses",
	23:"school_playground_mandatory_twenty",
	24:"school_playground_mandatory_twenty_one",
	25:"school_playground_august_four_work",
	26:"school_playground_adventure_thirty_five",
	27:"school_playground_september_courses",
	28:"school_playground_september_course_25",
	29:"school_playground_mandatory_twenty_two",
	30:"school_playground_mandatory_twenty_four",
	31:"school_playground_october_one",
	32:"school_playground_october_two",
	33:"school_playground_autumn_courses",
	34:"school_playground_job_change",
	35:"school_playground_november_three",
	36:"school_playground_mandatory_forty_one",
	37:"school_playground_november_five",
	38:"school_playground_december_one",
	39:"school_playground_mandatory_thirty_one"
}
const MAX_COMMANDS := 512
const MAX_BYTES := 262144
const POST_MAX_BYTES := 1048576
const POST_MAX_COMMANDS := 2048

var session: Session
var _commands: Array = []
var _rules: Dictionary = {}
var _fingerprints: Dictionary = {}
var _story_pages: Array = []
var _story_cursor := -1
var _continuation_revision := 0
var _week: Dictionary = {}
var _fifth_pages: Array = []
var _fifth_cursor := -1
var _fifth_exit: Dictionary = {}
var fifth_session: Session
var _workroom: Dictionary = {}
var _work_pages: Array = []
var _work_cursor := -1
var _school_entry: Dictionary = {}
var _postbattle: Postbattle


var _last_save_digest := ""
var _last_save_path := ""
var replay_progress: Callable


func _init() -> void:
	for key in RULE_PATHS:
		_rules[key] = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(RULE_PATHS[key])))
		_fingerprints[key] = FileAccess.get_sha256(RULE_PATHS[key])
	for scene in _rules["story"]["scenes"]:
		for page in scene["pages"]:
			var entry: Dictionary = page.duplicate(true)
			entry["chapter"] = scene["chapter"]
			entry["scene_label"] = scene["label"]
			_story_pages.append(entry)
	for scene in _rules["fifth_story"]["scenes"]:
		for page in scene["pages"]:
			var entry: Dictionary = page.duplicate(true)
			entry["chapter"] = scene["chapter"]
			entry["scene_label"] = scene["label"]
			_fifth_pages.append(entry)
	for scene in _rules["workroom"]["scenes"]:
		for page in scene["pages"]:
			var entry: Dictionary = page.duplicate(true)
			entry["chapter"] = scene["chapter"]
			entry["scene_label"] = scene["label"]
			_work_pages.append(entry)


func start() -> Dictionary:
	if not _valid_story_art() or not _valid_fifth_art() or not _valid_workroom_art():
		return _failure("invalid_story_assets")
	var fresh := Session.new()
	var rules: Dictionary = _rules["school"]
	var result := fresh.initialize_course_example(rules["origin_rules"],rules["course_rules"],rules)
	if not result["supported"]:
		return result
	session = fresh
	_commands = []
	_story_cursor = -1
	_continuation_revision = 0
	_week = {}
	_fifth_cursor = -1
	_fifth_exit = {}
	fifth_session = null
	_workroom = {}
	_work_cursor = -1
	_school_entry = {}
	_postbattle = null
	return {"supported":true,"status":"started"}


func _valid_story_art() -> bool:
	var expected := ["actor_4.png","actor_7.png","actor_130.png","background_8.png","background_52.png"]
	var outputs: Variant = _rules["story"].get("outputs_sha256")
	if not outputs is Dictionary or outputs.size() != expected.size():
		return false
	for filename in expected:
		if outputs.get(filename) != FileAccess.get_sha256("res://assets/school_story/"+filename):
			return false
	return true


func _valid_fifth_art() -> bool:
	var expected := ["body_9.png","body_10.png","body_12.png","portrait_12.png","portrait_27.png",
		"portrait_29.png","portrait_30.png","portrait_31.png","background_47.png"]
	var outputs: Variant = _rules["fifth_story"].get("outputs_sha256")
	if not outputs is Dictionary or outputs.size() != expected.size():
		return false
	for filename in expected:
		if outputs.get(filename) != FileAccess.get_sha256("res://assets/school_fifth_story/"+filename):
			return false
	return true


func stage() -> String:
	if session == null:
		return "uninitialized"
	if _postbattle!=null: return _postbattle.phase
	if fifth_session != null:
		return "fifth_planning"
	if _work_cursor == _work_pages.size():
		return "work_completed"
	if _work_cursor >= 0:
		return "work_story"
	if not _workroom.is_empty():
		return "workroom"
	if not _fifth_exit.is_empty():
		return "workroom_entry"
	if _fifth_cursor == _fifth_pages.size():
		return "fifth_completed"
	if _fifth_cursor >= 0:
		return "fifth_story"
	if not _week.is_empty():
		return "arrival"
	if _story_cursor == _story_pages.size():
		return "story_completed"
	if _story_cursor >= 0:
		return "story"
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
	var handoff: Dictionary=_postbattle.planning["handoff"] if _postbattle!=null and _postbattle.phase=="sortie_pending" else {}
	var scene_id: int=handoff.get("prepared",{}).get("adventure_id",0)
	if not command is Dictionary or not _valid_command(command,handoff.get("date",[]),scene_id):
		return _failure("invalid_command")
	if _commands.size() >= (MAX_COMMANDS if _postbattle==null else POST_MAX_COMMANDS):
		return _failure("save_command_limit")
	if _postbattle!=null and command["op"] not in ["course_story","sortie_finish","post_next","post_prev","post_skip","post_choice","post_school","return_move"]+Postbattle.PLAN_OPS:
		return _failure("postbattle_locks_departure")
	if _story_cursor >= 0 and command["op"] in SCHOOL_OPS:
		return _failure("story_locks_school")
	var previous := revision()
	var result := _dispatch(command)
	if result["supported"] and revision() != previous:
		_commands.append(command.duplicate(true))
	return result


func _dispatch(command: Dictionary) -> Dictionary:
	match command["op"]:
		"battle_finish":
			if stage()!="fifth_planning": return _failure("battle_requires_fifth_school")
			var context := adventure_result_context()
			var replayed := BattleRecord.replay(adventure_preparation(),adventure_combat_limits(),command["trace"])
			if not replayed["supported"]: return replayed
			var next := Postbattle.new()
			var begun := next.begin(context,replayed["receipt"],_school_entry["after"]["participants"],_school_entry["after"]["flags"])
			if not begun["supported"]: return begun
			_postbattle=next;return {"supported":true,"status":"battle_committed_once"}
		"course_story","sortie_finish","post_next","post_prev","post_skip","post_choice","post_school","return_move",\
		"return_plan","return_job","return_mode","return_course","return_select","return_settle","return_depart":
			return _failure("postbattle_not_started") if _postbattle==null else _postbattle.execute(command)
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
		"story_start","story_next","story_prev","story_skip","week":
			return _continue(command["op"])
		"fifth_start","fifth_next","fifth_prev","fifth_skip","fifth_finish":
			return _continue_fifth(command["op"])
		"workroom_open","work_start","work_next","work_prev","work_skip","school_enter":
			return _continue_workroom(command["op"])
		"plan_move","plan_mode","plan_course":
			if fifth_session == null:
				return _failure("fifth_planning_not_ready")
			if command["op"] == "plan_move":
				var input := command.duplicate(true)
				input.erase("op")
				return fifth_session.move_member(input,fifth_session.revision())
			if command["op"] == "plan_mode":
				if command["teaching"] and fifth_session.read_snapshot()["adventure_gate"] != 0:
					return _failure("fifth_requires_mandatory_adventure")
				return fifth_session.set_class_mode(command["group"],command["teaching"],fifth_session.revision())
			if fifth_session.read_snapshot()["adventure_gate"] != 0:
				return _failure("fifth_requires_mandatory_adventure")
			return fifth_session.assign_course(command["group"],command["course"],fifth_session.revision())
	return _failure("invalid_command")


static func _valid_command(command: Dictionary, departure_date: Array = [], scene_id := 0) -> bool:
	var keys: Array
	match command.get("op"):
		"move","plan_move","return_move":
			keys = ["op","kind","member_id","target_group","target_slot"]
			if command.get("kind") not in ["student","teacher"] or not _integer(command.get("member_id"),1,118) \
					or not _integer(command.get("target_group"),-1,4) or not _integer(command.get("target_slot"),-1,3):
				return false
		"mode","plan_mode","return_mode":
			keys = ["op","group","teaching"]
			if not _integer(command.get("group"),0,4) or not command.get("teaching") is bool:
				return false
		"course","plan_course":
			keys = ["op","group","course"]
			if not _integer(command.get("group"),0,4) or not _integer(command.get("course"),10,12):
				return false
		"return_course":
			keys=["op","group","course"]
			if not _integer(command.get("group"),0,4) or not _integer(command.get("course"),1,100):return false
		"post_choice":
			keys=["op","choice"]
			if not _integer(command.get("choice"),0,1):return false
		"return_job":
			keys=["op","member","job"]
			if not _integer(command.get("member"),1,44) or not _integer(command.get("job"),1,30):return false
		"return_select":
			keys=["op","adventure"]
			if not _integer(command.get("adventure"),1,100):return false
		"grow","confirm","complete","story_start","story_next","story_prev","story_skip","week",\
		"fifth_start","fifth_next","fifth_prev","fifth_skip","fifth_finish",\
		"workroom_open","work_start","work_next","work_prev","work_skip","school_enter":
			keys = ["op"]
		"post_next","post_prev","post_skip","post_school","return_plan","return_settle","return_depart","course_story":
			keys=["op"]
		"sortie_finish":
			keys=["op","trace"]
			if not Postbattle.SortieRecord.valid_trace(command.get("trace"),departure_date,scene_id): return false
		"battle_finish":
			keys=["op","trace"]
			if not BattleRecord.valid_trace(command.get("trace")): return false
		_:
			return false
	return command.size() == keys.size() and keys.all(func(key): return command.has(key))


static func _integer(value: Variant, low: int, high: int) -> bool:
	return value is int and value >= low and value <= high


func revision() -> int:
	return 0 if session == null else session.revision()+_continuation_revision+(0 if fifth_session == null else fifth_session.revision())+(0 if _postbattle==null else _postbattle.revision)


func planning_session() -> Session:
	return session if fifth_session == null else fifth_session


func adventure_preparation() -> Dictionary:
	if stage() != "fifth_planning" or fifth_session == null:
		return _failure("adventure_preparation_requires_fifth_school")
	var text := FileAccess.get_file_as_string(AdventurePreparation.RULE_PATH)
	var parsed: Variant = JSON.parse_string(text)
	if not parsed is Dictionary:
		return _failure("missing_adventure_preparation_rules")
	return AdventurePreparation.project(fifth_session.read_snapshot(),Roles._integers(parsed))



func adventure_ledger() -> Dictionary:
	if stage() != "fifth_planning" or fifth_session == null:
		return _failure("adventure_ledger_requires_fifth_school")
	return AdventureHandoff.initial_ledger(_rules["planning"]["adventure_template"])


func adventure_handoff() -> Dictionary:
	var ledger := adventure_ledger()
	if not ledger["supported"]:
		return ledger
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(AdventureHandoff.RULE_PATH))
	if not parsed is Dictionary:
		return _failure("missing_adventure_handoff_rules")
	return AdventureHandoff.project(fifth_session.read_snapshot(),ledger["ledger"],Roles._integers(parsed))


func adventure_combat_limits() -> Dictionary:
	var handoff := adventure_handoff()
	if not handoff["supported"]:
		return handoff
	var rules: Variant = JSON.parse_string(FileAccess.get_file_as_string(CombatLimits.RULE_PATH))
	if not rules is Dictionary or not CombatLimits._rules_valid(rules):
		return _failure("invalid_current_combat_source")
	var output := {"supported":true,"ready":handoff["ready"],"reason":handoff["reason"],
		"projection_only":true,"students":[],"full_combat_records":false,
		"battle_world_constructed":false,"battle_executed":false,"mandatory_gate_cleared":false,
		"live_witness":false,"authorizes_persistent_write":false}
	if not handoff["ready"]:
		return output
	# Current profiles own post-course job/level/attributes; the carried entry
	# owns equipment/skills. Neither source rules nor audit fixtures supply roles.
	var profiles: Array = fifth_session.read_snapshot()["member_profiles"]
	var roles: Array = _school_entry["after"]["participants"]
	for id in handoff["prepared"]["rounds"][0]["student_ids"]:
		var profile := {}
		var role := {}
		for entry in profiles:
			if entry["member_id"] == id:
				profile = entry
		for entry in roles:
			if entry["character_id"] == id:
				role = entry
		if profile.is_empty() or role.is_empty():
			return _failure("missing_current_combat_role")
		var input := {"character_id":id,"job":profile["job"],"level":profile["level_50"],
			"attributes":profile["attributes"].duplicate(true),
			"equipped_items":role["equipped_items"].duplicate(true),
			"equipped_skills":role["equipped_skills"].duplicate(true)}
		var projected := CombatLimits.project(input,rules)
		if not projected["supported"]:
			return projected
		output["students"].append({"input":input,"limits":projected["limits"]})
	output["result_context"] = adventure_result_context()
	return output


func adventure_result_context() -> Dictionary:
	var prepared := adventure_preparation()
	if not prepared.get("ready",false): return {}
	var growth := session.read_growth_records()
	var records := session.read_confirmation_records()
	# Carry the actual post-week skills/progress, not the old course result copy.
	for role in _school_entry["after"]["participants"]:
		for row in growth:
			if row["character_id"] == role["character_id"]:
				row["skill_statuses"] = role["skill_statuses"].duplicate()
		for row in records:
			if row["character_id"] == role["character_id"]:
				for i in range(31): row["job_progress"][i] = role["job_progress"][i]
	return {"origin":"current_new_game_first_scene5","school":fifth_session.read_snapshot(),
		"preparation":prepared["prepared"].duplicate(true),"growth":growth,"records":records,
		"counts":session.read_mvp_counts(),"clock_seed":4660,"growth_seed":4660}


func read_work_page() -> Dictionary:
	return {} if _work_cursor < 0 or _work_cursor >= _work_pages.size() else _work_pages[_work_cursor].duplicate(true)


func work_catalog() -> Dictionary:
	return _rules["workroom"].duplicate(true)


func _valid_workroom_art() -> bool:
	var expected := ["background.png","portrait_101.png","portrait_117.png"]
	var outputs: Variant = _rules["workroom"].get("outputs_sha256")
	if not outputs is Dictionary or outputs.size() != expected.size():
		return false
	for filename in expected:
		if outputs.get(filename) != FileAccess.get_sha256("res://assets/school_workroom/"+filename):
			return false
	return true


func _continue_workroom(op: String) -> Dictionary:
	if _fifth_exit.is_empty():
		return _failure("workroom_requires_fifth_exit")
	if op == "workroom_open":
		if not _workroom.is_empty():
			return {"supported":true,"status":"duplicate"}
		if _fifth_exit["handoff"]["pending_state"] != 8:
			return _failure("invalid_workroom_handoff")
		_workroom = {"entry_state":8,"date":[4,5],"original_menu_body_executed":false}
	elif _workroom.is_empty():
		return _failure("workroom_not_open")
	elif op == "school_enter":
		if fifth_session != null:
			return {"supported":true,"status":"duplicate"}
		if _work_cursor != _work_pages.size():
			return _failure("school_requires_workroom_story")
		var candidate := Session.new()
		var initialized := candidate.initialize_fifth_planning(session,_rules["planning"])
		if not initialized["supported"]:
			return initialized
		var before: Dictionary = _fifth_exit["after"].duplicate(true)
		var after: Dictionary = before.duplicate(true)
		after["flags"]["0x7a4e62"] = 1
		after["flags"]["0x7a55fa"] = candidate.read_snapshot()["adventure_gate"]
		_school_entry = {"before":before,"after":after,"pending_state":9,
			"source_school_data_prepared":true,"original_menu_body_executed":false}
		fifth_session = candidate
	elif fifth_session != null:
		return _failure("school_already_entered")
	elif op == "work_start":
		if _work_cursor >= 0:
			return {"supported":true,"status":"duplicate"}
		_work_cursor = 0
	elif _work_cursor < 0:
		return _failure("work_story_not_started")
	elif op == "work_next":
		if _work_cursor == _work_pages.size():
			return {"supported":true,"status":"duplicate"}
		_work_cursor += 1
	elif op == "work_prev":
		if _work_cursor == 0:
			return {"supported":true,"status":"duplicate"}
		_work_cursor -= 1
	elif op == "work_skip":
		if _work_cursor == _work_pages.size():
			return {"supported":true,"status":"duplicate"}
		_work_cursor = _work_pages.size()
	_continuation_revision += 1
	return {"supported":true,"status":"continued_once"}


func read_story_page() -> Dictionary:
	return {} if _story_cursor < 0 or _story_cursor >= _story_pages.size() else _story_pages[_story_cursor].duplicate(true)


func story_catalog() -> Dictionary:
	return _rules["story"].duplicate(true)


func read_fifth_page() -> Dictionary:
	return {} if _fifth_cursor < 0 or _fifth_cursor >= _fifth_pages.size() else _fifth_pages[_fifth_cursor].duplicate(true)


func fifth_catalog() -> Dictionary:
	return _rules["fifth_story"].duplicate(true)


func _continue_fifth(op: String) -> Dictionary:
	if _week.is_empty():
		return _failure("fifth_requires_arrival")
	if not _fifth_exit.is_empty():
		return {"supported":true,"status":"duplicate"} if op == "fifth_finish" else _failure("fifth_already_finished")
	if op == "fifth_start":
		if _fifth_cursor >= 0:
			return {"supported":true,"status":"duplicate"}
		_fifth_cursor = 0
	elif op == "fifth_finish":
		if _fifth_cursor != _fifth_pages.size():
			return _failure("fifth_requires_completed_story")
		var before := _fifth_input()
		var rules: Dictionary = _rules["fifth"]
		if [before["month"],before["week"]] != rules["required_date"] \
				or _week["handoff"]["pending_state"] != rules["entry_state"] \
				or _week["handoff"]["next_task"] != rules["next_task"] \
				or _week["handoff"]["script"] != rules["entry_script"]:
			return _failure("invalid_fifth_handoff")
		var after: Dictionary = before.duplicate(true)
		for field in rules["flag_writes"]:
			after["flags"][field] = rules["flag_writes"][field]
		for field in rules["adv_global_writes"]:
			after["adv_globals"][field] = rules["adv_global_writes"][field]
		_fifth_exit = {"before":before,"after":after,"handoff":{
			"pending_state":rules["exit_state"],"next_task":rules["next_task"],
			"script":rules["selected_script"],"ch001_body_executed":true,
			"workroom_body_executed":false,"school_initialized":false}}
	elif _fifth_cursor < 0:
		return _failure("fifth_not_started")
	elif op == "fifth_next":
		if _fifth_cursor == _fifth_pages.size():
			return {"supported":true,"status":"duplicate"}
		_fifth_cursor += 1
	elif op == "fifth_prev":
		if _fifth_cursor == 0:
			return {"supported":true,"status":"duplicate"}
		_fifth_cursor -= 1
	elif op == "fifth_skip":
		if _fifth_cursor == _fifth_pages.size():
			return {"supported":true,"status":"duplicate"}
		_fifth_cursor = _fifth_pages.size()
	_continuation_revision += 1
	return {"supported":true,"status":"continued_once"}


func _fifth_input() -> Dictionary:
	var before: Dictionary = _week["after"].duplicate(true)
	before["adv_globals"] = _rules["fifth"]["entry_adv_globals"].duplicate(true)
	var result := session.read_result_handoff()
	before["adv_globals"]["0x7e1180"] = result["recipient"]
	before["adv_globals"]["0x7e1182"] = result["old_count"]
	return before


func _continue(op: String) -> Dictionary:
	if session.read_result_handoff().is_empty():
		return _failure("story_requires_course_result")
	if not _week.is_empty():
		return {"supported":true,"status":"duplicate"} if op == "week" else _failure("week_already_arrived")
	if op == "week":
		if _story_cursor != _story_pages.size():
			return _failure("week_requires_completed_story")
		var before := _week_input()
		var projected := Week.project(before,_rules["week"]["week_rules"])
		if not projected["supported"]:
			return projected
		_week = {"before":before,"after":projected["after"],
			"handoff":{"pending_state":6,"next_task":8,"script":"adv/dat/ch001.ybc",
				"school_initialized":false,"ch001_body_executed":false}}
	elif op == "story_start":
		if _story_cursor >= 0:
			return {"supported":true,"status":"duplicate"}
		_story_cursor = 0
	elif _story_cursor < 0:
		return _failure("story_not_started")
	elif op == "story_next":
		if _story_cursor == _story_pages.size():
			return {"supported":true,"status":"duplicate"}
		_story_cursor += 1
	elif op == "story_prev":
		if _story_cursor == 0:
			return {"supported":true,"status":"duplicate"}
		_story_cursor -= 1
	elif op == "story_skip":
		if _story_cursor == _story_pages.size():
			return {"supported":true,"status":"duplicate"}
		_story_cursor = _story_pages.size()
	_continuation_revision += 1
	return {"supported":true,"status":"continued_once"}


func _week_input() -> Dictionary:
	var before: Dictionary = _rules["week"]["baseline"].duplicate(true)
	before["month"] = 4
	before["week"] = 4
	var growth := session.read_growth_records()
	var confirmation := session.read_confirmation_records()
	for index in range(before["participants"].size()):
		before["participants"][index]["attributes"] = growth[index]["attributes"].duplicate(true)
		before["participants"][index]["skill_statuses"] = growth[index]["skill_statuses"].duplicate(true)
		before["participants"][index]["job_progress"] = confirmation[index]["job_progress"].slice(0,31)
	return before


func _school_state() -> Dictionary:
	if session == null:
		return {}
	return {"snapshot":session.read_snapshot(),"growth":session.read_growth_records(),
		"confirmation":session.read_confirmation_records(),"result":session.read_result_handoff(),
		"counts":session.read_mvp_counts(),"revision":session.revision()}


func _version2_state() -> Dictionary:
	var result := _school_state()
	if result.is_empty():
		return result
	result["revision"] = revision()
	result["story"] = {"cursor":_story_cursor,"total":_story_pages.size(),"completed":_story_cursor == _story_pages.size()}
	result["week"] = _week.duplicate(true)
	return result


func _version3_state() -> Dictionary:
	var result := _version2_state()
	if not result.is_empty():
		result["fifth_story"] = {"cursor":_fifth_cursor,"total":_fifth_pages.size(),
			"completed":_fifth_cursor == _fifth_pages.size()}
		result["fifth_exit"] = _fifth_exit.duplicate(true)
	return result


func state() -> Dictionary:
	var result := _version4_state()
	if _postbattle!=null: result["postbattle"]=_postbattle.snapshot()
	return result


func _version4_state() -> Dictionary:
	var result := _version3_state()
	if not result.is_empty():
		result["workroom"] = _workroom.duplicate(true)
		result["work_story"] = {"cursor":_work_cursor,"total":_work_pages.size(),"completed":_work_cursor == _work_pages.size()}
		result["school_entry"] = _school_entry.duplicate(true)
		result["fifth_school"] = {} if fifth_session == null else {"snapshot":fifth_session.read_snapshot(),
			"revision":fifth_session.revision()}
	return result


func export_save() -> Dictionary:
	if session == null:
		return {}
	var version := _save_version()
	return {"version":version,"context":SAVE_CONTEXTS[version],"rules":_save_fingerprints(version),
		"commands":_commands.duplicate(true),"state_sha256":JSON.stringify(state(),"",true).sha256_text()}


func _save_version() -> int:
	if _postbattle==null: return 4
	if _postbattle.planning.get("committed_date")==[12,1]:return 39
	if _postbattle.planning.get("committed_date")==[11,5]:return 38
	if _november_four_planning() or _postbattle.planning.get("committed_date")==[11,4]:return 37
	if _postbattle.planning.get("committed_date")==[11,3]:return 36
	if _postbattle.planning.get("committed_date")==[11,2]:return 35
	if _commands.any(func(c):return c.op=="return_job"):return 34
	var date: Array=_postbattle.planning.get("committed_date",[])
	if date.size()==2 and Postbattle.SortieWeek.YearLoop.has_departure(date[0],date[1]):return 33
	if _postbattle.planning.get("committed_date")==[10,1]:return 32
	if _postbattle.planning.get("committed_date")==[9,5]: return 31
	if _postbattle.planning.get("committed_date")==[9,4]: return 30
	if _postbattle.planning.get("committed_date")==[9,3]: return 29
	if _postbattle.planning.get("committed_date")==[9,2]: return 28
	if _postbattle.planning.get("committed_date")==[9,1]: return 27
	if _postbattle.planning.get("committed_date")==[8,5]: return 26
	if _postbattle.planning.get("committed_date")==[8,4]: return 25
	if _postbattle.planning.get("committed_date")==[8,3]: return 24
	if _postbattle.planning.get("committed_date")==[8,2]: return 23
	if _postbattle.planning.get("committed_date")==[8,1]: return 22
	if _postbattle.planning.get("committed_date")==[7,5]: return 21
	if _postbattle.planning.get("committed_date")==[7,4]: return 20
	if _postbattle.planning.get("committed_date")==[7,3]: return 19
	if _postbattle.planning.get("committed_date") in [[7,1],[7,2]]: return 18
	if _postbattle.planning.get("committed_date")==[6,5]: return 17
	if _postbattle.planning.get("committed_date")==[6,4]: return 16
	if _postbattle.planning.get("committed_date")==[6,3]: return 15
	if _postbattle.planning.get("committed_date")==[6,2]: return 14
	if _postbattle.planning.get("committed_date")==[6,1]: return 13
	if _postbattle.planning.get("committed_week")==5: return 12
	if _postbattle.planning.get("committed_week")==4: return 11
	if _postbattle.planning.get("committed_week")==3: return 10
	if _postbattle.planning.has("opening_ledger"): return 9
	if _postbattle.course_continued(): return 8
	if _postbattle.planning.has("sortie_summary"): return 7
	if not _postbattle.planning.is_empty(): return 6
	return 5


func _november_four_planning() -> bool:
	return _postbattle!=null and _postbattle.phase=="returned_school" and [_postbattle.bundle.school.month,_postbattle.bundle.school.week]==[11,4] and not _commands.is_empty() and _commands.back().op in ["return_course","return_mode","return_move","return_job","return_select"]


func _save_fingerprints(version: int) -> Dictionary:
	var result := _fingerprints.duplicate(true)
	if version>=5:
		result["postbattle_story"]=Postbattle.STORY_SHA
		result["postbattle_return"]=Postbattle.Return.SOURCES["candidate"][1]
		result["battle_record"]="1"
	if version>=6:
		result["return_adventures"]=Postbattle.Adventures.SHA
		result["return_courses"]="1"
	if version>=8:
		result["course_week"]=Postbattle.SortieWeek.SHA
	if version==7 or version>=9:
		result["sortie_week"]=Postbattle.SortieWeek.SHA
		result["sortie_rewards"]=Postbattle.SortieSettlement.TASK_SHA
		result["sortie_units"]=Postbattle.SortieRecord.Sortie.SOURCE_SHA
		result["sortie_scene"]=Postbattle.SortieRecord.Sortie.SCENES_SHA
	if version>=9:
		result["may_week_three"]=Postbattle.SortieWeek.WEEK3_SHA
	if version>=39:
		result["mandatory_thirty_one"]=Postbattle.Adventures.THIRTY_ONE_SHA
		result["scene_thirty_one"]=Postbattle.SortieRecord.Sortie.THIRTY_ONE_SHA
		result["december_two_story"]=Postbattle.SortieWeek.YearLoop.DECEMBER_TWO_SHA
	if version>=38:
		result["december_one_story"]=Postbattle.SortieWeek.YearLoop.DECEMBER_ONE_SHA
	if version>=37:
		result["november_five_story"]=Postbattle.SortieWeek.YearLoop.NOVEMBER_FIVE_SHA
		result["november_four_courses"]=Postbattle.Courses.NOVEMBER_FOUR_SHA
	if version>=36:
		result["mandatory_forty_one"]=Postbattle.Adventures.FORTY_ONE_SHA
		result["scene_forty_one"]=Postbattle.SortieRecord.Sortie.FORTY_ONE_SHA
		result["november_four_story"]=Postbattle.Return.NOVEMBER_FOUR[1]
	if version>=35:result["november_three_story"]=Postbattle.SortieWeek.YearLoop.NOVEMBER_SHA
	if version>=34:
		result["job_menu"]=Postbattle.JobEligibility.MENU_SHA
		result["job_change"]=Postbattle.JobEligibility.CHANGE_SHA
	if version>=33:result["autumn_courses_story"]=Postbattle.SortieWeek.YearLoop.SHA
	if version>=32:result["october_two_story"]=Postbattle.SortieWeek.OCTOBER_TWO[1]
	if version>=31:
		result["october_one_story"]=Postbattle.Return.OCTOBER_ONE[1]
		result["september_five_courses"]=Postbattle.Courses.SEPTEMBER_FIVE_SHA
	if version>=30:
		result["september_five_story"]=Postbattle.Return.SEPTEMBER_FIVE[1]
		result["mandatory_twenty_four"]=Postbattle.Adventures.TWENTY_FOUR_SHA
		result["twenty_four_battle"]=Postbattle.SortieRecord.Sortie.TWENTY_FOUR_SHA
	if version>=29:
		result["september_four_story"]=Postbattle.SortieWeek.SEPTEMBER_FOUR_SHA
		result["mandatory_twenty_two"]=Postbattle.Adventures.TWENTY_TWO_SHA
		result["twenty_two_battle"]=Postbattle.SortieRecord.Sortie.TWENTY_TWO_SHA
	if version>=28:
		result["september_three_story"]=Postbattle.SortieWeek.SEPTEMBER_THREE_SHA
		result["september_two_courses"]=Postbattle.Courses.SEPTEMBER_TWO_SHA
	if version>=27:
		result["september_two_story"]=Postbattle.SortieWeek.SEPTEMBER_TWO_SHA
		result["september_courses"]=Postbattle.Courses.SEPTEMBER_ONE_SHA
	if version>=26:
		result["september_one_story"]=Postbattle.SortieWeek.SEPTEMBER_ONE_SHA
		result["adventure_thirty_five"]=Postbattle.Adventures.THIRTY_FIVE_SHA
		result["thirty_five_battle"]=Postbattle.SortieRecord.Sortie.THIRTY_FIVE_SHA
	if version>=25:
		result["august_five_story"]=Postbattle.SortieWeek.AUGUST_FIVE_SHA
		result["august_four_courses"]=Postbattle.Courses.AUGUST_FOUR_SHA
	if version>=24:
		result["mandatory_twenty_one"]=Postbattle.Adventures.TWENTY_ONE_SHA
		result["twenty_one_battle"]=Postbattle.SortieRecord.Sortie.TWENTY_ONE_SHA
		result["august_four_story"]=Postbattle.Return.AUGUST_FOUR[1]
	if version>=23:
		result["mandatory_twenty"]=Postbattle.Adventures.TWENTY_SHA
		result["twenty_battle"]=Postbattle.SortieRecord.Sortie.TWENTY_SHA
		result["august_three_story"]=Postbattle.SortieWeek.AUGUST_THREE_SHA
	if version>=22:
		result["august_two_story"]=Postbattle.SortieWeek.AUGUST_TWO_SHA
	if version>=21:
		result["july_five_battle"]=Postbattle.SortieRecord.Sortie.JULY_FIVE_SHA
		result["august_one_story"]=Postbattle.SortieWeek.AUGUST_ONE_SHA
	if version>=20:
		result["mandatory_fourteen"]=Postbattle.Adventures.FOURTEEN_SHA
		result["fourteen_battle"]=Postbattle.SortieRecord.Sortie.FOURTEEN_SHA
		result["july_five_story"]=Postbattle.SortieWeek.JULY_FIVE_SHA
	if version>=19:
		result["mandatory_nine"]=Postbattle.Adventures.NINE_SHA
		result["nine_battle"]=Postbattle.SortieRecord.Sortie.NINE_SHA
		result["july_four_story"]=Postbattle.SortieWeek.JULY_FOUR_SHA
	if version>=18:
		result["adventure_eighteen"]=Postbattle.Adventures.EIGHTEEN_SHA
		result["eighteen_battle"]=Postbattle.SortieRecord.Sortie.EIGHTEEN_SHA
		result["july_two_story"]=Postbattle.SortieWeek.JULY_TWO_SHA
		result["july_three_story"]=Postbattle.SortieWeek.JULY_THREE_SHA
	if version>=17:
		result["june_five_courses"]=Postbattle.Courses.JUNE_FIVE_SHA
		result["july_one_story"]=Postbattle.SortieWeek.JULY_ONE_SHA
	if version>=16:
		result["mandatory_thirteen"]=Postbattle.Adventures.THIRTEEN_SHA
		result["thirteen_battle"]=Postbattle.SortieRecord.Sortie.THIRTEEN_SHA
		result["june_five_story"]=Postbattle.SortieWeek.JUNE_FIVE_SHA
	if version>=15:
		result["mandatory_ten"]=Postbattle.Adventures.TEN_SHA
		result["ten_battle"]=Postbattle.SortieRecord.Sortie.TEN_SHA
		result["june_four_story"]=Postbattle.SortieWeek.JUNE_FOUR_SHA
	if version>=14:
		result["mandatory_six"]=Postbattle.Adventures.SIX_SHA
		result["six_battle"]=Postbattle.SortieRecord.Sortie.SIX_SHA
		result["june_three_story"]=Postbattle.SortieWeek.JUNE_THREE_SHA
	if version>=13:
		result["mandatory_four"]=Postbattle.Adventures.FOUR_SHA
		result["four_battle"]=Postbattle.SortieRecord.Sortie.FOUR_SHA
		result["june_two_story"]=Postbattle.SortieWeek.JUNE_TWO_SHA
	if version>=12:
		result["may_five_courses"]=Postbattle.Courses.MAY_FIVE_SHA
		result["may_five_sortie_job"]=Postbattle.SortieRecord.Sortie.MAY_FIVE_JOB_SHA
		result["june_story"]=Postbattle.SortieWeek.JUNE_SHA
	if version>=11:
		result["mandatory_seven"]=Postbattle.Adventures.SEVEN_SHA
		result["seven_battle"]=Postbattle.SortieRecord.Sortie.SEVEN_SHA
		result["may_week_five"]=Postbattle.Return.WEEK_FIVE[1]
	if version>=10:
		result["may_week_four"]=Postbattle.SortieWeek.WEEK4_SHA
	return result


func read_postbattle() -> Dictionary:
	return {} if _postbattle==null else _postbattle.snapshot()


func restore(payload: Variant) -> Dictionary:
	if not payload is Dictionary or payload.size() != 5 \
			or not ["version","context","rules","commands","state_sha256"].all(func(k): return payload.has(k)):
		return _failure("invalid_save")
	var legacy: bool = payload["version"] == 1
	var version2: bool = payload["version"] == 2
	var version3: bool = payload["version"] == 3
	if not _integer(payload["version"],1,SAVE_CONTEXTS.size()) or payload["context"] != SAVE_CONTEXTS[payload["version"]]:
		return _failure("unsupported_save_version")
	var fingerprints: Dictionary = _save_fingerprints(payload["version"])
	if legacy or version2 or version3:
		fingerprints = {}
		for key in LEGACY_KEYS if legacy else VERSION2_KEYS if version2 else VERSION3_KEYS:
			fingerprints[key] = _fingerprints[key]
	var previous_line_endings: Dictionary = fingerprints.duplicate(true)
	if not legacy and fingerprints.get("story") == STORY_LF_SHA:
		# Earlier Windows exports wrote CRLF before the Git LF attribute took
		# effect in the working copy. This alias is for those exact source bytes.
		previous_line_endings["story"] = LEGACY_STORY_CRLF_SHA
	if payload["rules"] != fingerprints and payload["rules"] != previous_line_endings:
		return _failure("save_rules_changed")
	if not payload["commands"] is Array or payload["commands"].size() > (POST_MAX_COMMANDS if payload["version"]>=5 else MAX_COMMANDS) \
			or not payload["state_sha256"] is String or payload["state_sha256"].length() != 64:
		return _failure("invalid_save")
	var candidate = get_script().new()
	var begun: Dictionary = candidate.start()
	if not begun["supported"]:
		return begun
	for i in range(payload["commands"].size()):
		if replay_progress.is_valid() and not replay_progress.call(i,payload["commands"].size()):
			return _failure("replay_canceled")
		var command: Variant=payload["commands"][i]
		if payload["version"]<8 and command is Dictionary and command.get("op")=="course_story":
			return _failure("save_command_rejected")
		if payload["version"]<7 and command is Dictionary and command.get("op")=="sortie_finish":
			return _failure("save_command_rejected")
		if payload["version"]<6 and command is Dictionary and command.get("op") in Postbattle.PLAN_OPS:
			return _failure("save_command_rejected")
		if payload["version"]<5 and command is Dictionary and command.get("op") in ["battle_finish","post_next","post_prev","post_skip","post_choice","post_school","return_move"]:
			return _failure("save_command_rejected")
		if legacy and (not command is Dictionary or command.get("op") not in SCHOOL_OPS):
			return _failure("save_command_rejected")
		if (version2 or version3) and (not command is Dictionary or command.get("op") not in SCHOOL_OPS+(VERSION2_OPS if version2 else VERSION3_OPS)):
			return _failure("save_command_rejected")
		var previous: int = candidate.revision()
		var result: Dictionary = candidate.execute(command)
		if not result["supported"] or candidate.revision() == previous:
			return _failure("save_command_rejected")
	var legacy_november_plan: bool=payload["version"]==36 and candidate._november_four_planning()
	if payload["version"]>=5 and candidate._save_version()!=payload["version"] and not legacy_november_plan:
		return _failure("save_work_version_mismatch")
	var candidate_state: Dictionary = candidate._school_state() if legacy else candidate._version2_state() if version2 else candidate._version3_state() if version3 else candidate._version4_state() if payload["version"]==4 else candidate.state()
	if JSON.stringify(candidate_state,"",true).sha256_text() != payload["state_sha256"]:
		return _failure("save_state_mismatch")
	session = candidate.session
	_commands = candidate._commands.duplicate(true)
	_story_cursor = candidate._story_cursor
	_continuation_revision = candidate._continuation_revision
	_week = candidate._week.duplicate(true)
	_fifth_cursor = candidate._fifth_cursor
	_fifth_exit = candidate._fifth_exit.duplicate(true)
	fifth_session = candidate.fifth_session
	_workroom = candidate._workroom.duplicate(true)
	_work_cursor = candidate._work_cursor
	_school_entry = candidate._school_entry.duplicate(true)
	_postbattle=candidate._postbattle
	return {"supported":true,"status":"restored"}


func restore_text(content: String) -> Dictionary:
	if content.to_utf8_buffer().size() > POST_MAX_BYTES:
		return _failure("save_too_large")
	var json := JSON.new()
	if json.parse(content) != OK:
		return _failure("invalid_save_json")
	if json.data is Dictionary and content.to_utf8_buffer().size()>MAX_BYTES:
		var version: Variant=json.data.get("version")
		if not (version is float or version is int) or not SAVE_CONTEXTS.has(int(version)) or version!=int(version) or version<5:
			return _failure("save_too_large")
	return restore(Roles._integers(json.data))


func _read(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return _failure("save_missing")
	var file := FileAccess.open(path,FileAccess.READ)
	if file == null:
		return _failure("save_read_failed")
	if file.get_length() > POST_MAX_BYTES:
		return _failure("save_too_large")
	var content := file.get_as_text()
	var result := restore_text(content)
	if result.supported:
		_last_save_path=path
		_last_save_digest=content.sha256_text()
	return result


func load_file(path := SAVE_PATH) -> Dictionary:
	var result := _read(path)
	if result["supported"]:
		return result
	if result.get("reason")=="replay_canceled":return result
	var backup := _read(path+".bak")
	if backup["supported"]:
		return {"supported":true,"status":"recovered_backup","primary_reason":result["reason"]}
	return result


func save_file(path := SAVE_PATH) -> Dictionary:
	var payload := export_save()
	if payload.is_empty():
		return _failure("not_started")
	var content := JSON.stringify(payload,"" if payload["version"]>=9 else "  ",true)+"\n"
	if content.to_utf8_buffer().size() > (POST_MAX_BYTES if _postbattle!=null else MAX_BYTES):
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
		var valid := path==_last_save_path and FileAccess.get_sha256(path)==_last_save_digest
		if not valid:
			var checker = get_script().new()
			valid=checker._read(path).supported
		previous = path+".bak" if valid else path+".corrupt"
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
	_last_save_path=path
	_last_save_digest=content.sha256_text()
	return {"supported":true,"status":"saved"}


static func _failure(reason: String) -> Dictionary:
	return {"supported":false,"reason":reason}


func save_week_state(path := SAVE_PATH) -> Dictionary:
	return save_file(path)


func load_week_state(path := SAVE_PATH) -> Dictionary:
	return load_file(path)
