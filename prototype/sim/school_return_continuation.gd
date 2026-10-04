class_name SchoolReturnContinuation
extends RefCounted
## Audited 4/5->5/1 checkpoints; this does not implement the general ADV VM.
## Owns calculators and control transitions, without live/save authority.

const Layout = preload("res://sim/campaign_school_layout.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const Join = preload("res://sim/roster_join_replay.gd")
const Start = preload("res://sim/week_start_replay.gd")
const Workroom = preload("res://sim/workroom_return_replay.gd")
const School = preload("res://sim/school_entry_replay.gd")
const Boot = preload("res://sim/school_boot_replay.gd")
const JOIN_CONTEXT = {"task_state": 6, "script_path": "DATA/ADV/DAT/Chapter020.ybc",
	"script_file_offset": 20, "opcode": 144, "character_id": 5, "group": -1, "slot": -1, "difficulty": 0}
const WORK_CONTEXT = {"task_state": 8, "pending_flag": 1, "vm_active": 0,
	"next_task_state": 8, "end_file_offset": 0x1b0, "opcode": 19,
	"script_path": "chapter208.ybc", "adv_completed": true}
const CH002_CONTEXT = {"state": 6, "pending_flag": 1, "next_task_state": 9,
	"vm_active": 1, "vm_pc": 0, "path": "ch002.ybc"}

var _snapshot: Dictionary = {}
var _rules: Dictionary = {}
var _input: Dictionary = {}
var _instance := ""
var _phase := ""
var _requested_state := 6
var _pending_flag := 0
var _week_executed := false
var _tasks: Array = []
var _log: Array = []
var _workroom := Workroom.new()


func begin(instance_id: String, before: Dictionary, rules: Dictionary) -> Dictionary:
	var input := {"before": before.duplicate(true), "rules": rules.duplicate(true)}
	if not _instance.is_empty():
		return _view("duplicate") if _instance == instance_id and _input == input else _unsupported("instance_input_conflict")
	if instance_id.is_empty() or not rules.get("role") is Dictionary or not rules.get("week") is Dictionary:
		return _unsupported("missing_instance_or_rules")
	var reason := Layout.validate(before, rules["week"])
	if reason.is_empty():
		reason = Roles._validate_rules(rules["role"])
	if not reason.is_empty():
		return _unsupported(reason)
	var students: Array = before["school"]["student_ids"].slice(0, 3).map(func(id): return int(id))
	if int(before["month"]) != 4 or int(before["week"]) != 5 \
			or int(before["school"]["student_count"]) != 3 or students != [3, 4, 9] \
			or int(before["availability"][5]) != 0 or int(before["recipient_id"]) != 4 \
			or int(before["school"]["adv_globals"]["0x7a5292"]) != 1 \
			or int(before["school"]["adv_globals"]["0x7e1182"]) != 0:
		return _unsupported("outside_captured_return_catalog")
	var join_rules := {"week": rules["week"].duplicate(true),
		"level_thresholds": rules["role"]["level_thresholds"].duplicate(true),
		"learned_points": rules["role"]["skills"].map(func(skill): return skill["learned_points"])}
	var view := Layout.school_view(before, rules["week"])
	var joined := Join.new().apply_once(instance_id, JOIN_CONTEXT, view["snapshot"], join_rules)
	if not joined["supported"]:
		return joined
	var merged := Layout.merge_school(before, joined["after"], rules["week"])
	if not merged["supported"]:
		return merged
	_instance = instance_id
	_input = input
	_rules = rules.duplicate(true)
	_snapshot = before.duplicate(true)
	_record("chapter020_join", merged["snapshot"], {"path": "chapter020.ybc", "offset": 20, "opcode": 144})
	_phase = "chapter"
	return _view("waiting_chapter_end")


func advance(instance_id: String, chapter_key_ready: bool, continue_ready: bool, school_fade_ready: bool) -> Dictionary:
	if _instance.is_empty() or _instance != instance_id:
		return _unsupported("missing_return_instance")
	if _phase in ["school_constructed", "school_boot_data"]:
		return _view("duplicate")
	if _phase == "chapter":
		if not chapter_key_ready:
			return _view("waiting_chapter_end")
		_record("chapter021_end", _snapshot, {"path": "chapter021.ybc", "offset": 0x61e, "opcode": 19,
			"source_request_va": "0x439e30", "requested_state": 7})
		var start := Start.new()
		var school := Layout.school_view(_snapshot, _rules["week"])
		var week := start.begin(_instance, {"task_state": 7, "adv_completed": true}, school["snapshot"], _rules["week"])
		if not week["supported"]:
			return week
		var merged := Layout.merge_school(_snapshot, week["after"], _rules["week"])
		if not merged["supported"]:
			return merged
		_record("state7_week", merged["snapshot"], {"native_va": "0x49f4e0", "week_va": "0x4d3510"})
		_week_executed = true
		var ready := start.finish(_instance, true)
		if not ready["supported"]:
			return ready
		# At 5/1 the sourced CH001->Chapter022->208 chain writes music and
		# background globals before END. UI/movie readiness here is fixed ready;
		# only the three explicitly supported wait boundaries are modeled.
		var after := _snapshot.duplicate(true)
		after["flags"]["0x7a55f6"] = 9
		after["flags"]["0x7e11a0"] = 1
		after["school"]["adv_globals"]["0x7a5292"] = 8
		_record("ch001_end", after, {"path": "chapter208.ybc", "offset": 0x1b0, "opcode": 19,
			"source_request_va": "0x439e30", "requested_state": 8})
		school = Layout.school_view(_snapshot, _rules["week"])
		var work := _workroom.begin(_instance, WORK_CONTEXT, school["snapshot"], _rules["week"])
		if not work["supported"]:
			return work
		_record("workroom_constructed", _snapshot, {"native_va": "0x49e2b0", "consumed_state": 8})
		_phase = "workroom"
		_requested_state = 8
		_pending_flag = 0
	if _phase == "workroom":
		if not continue_ready:
			return _view("waiting_continue")
		var work := _workroom.continue_workroom(_instance, true)
		if not work["supported"]:
			return work
		var merged := Layout.merge_school(_snapshot, work["after"], _rules["week"])
		if not merged["supported"]:
			return merged
		_record("workroom_continue", merged["snapshot"], {"native_va": "0x4a1570", "requested_state": 6})
		work = _workroom.start_ch002(_instance, CH002_CONTEXT)
		if not work["supported"]:
			return work
		merged = Layout.merge_school(_snapshot, work["after"], _rules["week"])
		if not merged["supported"]:
			return merged
		_record("ch002_opcode151", merged["snapshot"], {"path": "ch002.ybc", "opcode": 151})
		_phase = "ch002"
		_requested_state = 6
		_pending_flag = 0
	if _phase == "ch002":
		if not school_fade_ready:
			return _view("waiting_ch002_end")
		var work := _workroom.finish_ch002(_instance, true)
		if not work["supported"]:
			return work
		_record("ch002_end", _snapshot, {"path": "ch002.ybc", "offset": 0x6d0, "opcode": 19,
			"source_request_va": "0x439e30", "requested_state": 9})
		var school := Layout.school_view(_snapshot, _rules["week"])
		var entry := School.new().dispatch_once(_instance, {"task_state": 9, "pending_flag": 1,
			"adv_active": 0, "source_request_va": "0x439e30"}, school["snapshot"], _rules["week"])
		if not entry["supported"]:
			return entry
		_tasks = entry["tasks"].duplicate(true)
		_record("school_dispatch", _snapshot, {"native_va": "0x49e2b0", "consumed_state": 9})
		_phase = "school_constructed"
		_requested_state = 9
		_pending_flag = 0
	return _view("completed_once")


func project_school_boot(instance_id: String) -> Dictionary:
	if _instance.is_empty() or _instance != instance_id:
		return _unsupported("missing_return_instance")
	if _phase == "school_boot_data":
		return _view("duplicate")
	if _phase != "school_constructed":
		return _unsupported("pending_school_construction")
	if not _rules.get("school_boot") is Dictionary:
		return _unsupported("missing_frozen_school_boot_rules")
	var school := Layout.school_view(_snapshot, _rules["week"])
	var boot := Boot.new().initialize_once(_instance, {"task_state": 9, "pending_flag": 0,
		"school_constructed": true, "tasks": _tasks}, school["snapshot"], _rules["week"], _rules["school_boot"])
	if not boot["supported"]:
		return boot
	var merged := Layout.merge_school(_snapshot, boot["after"], _rules["week"])
	if not merged["supported"]:
		return merged
	_record("school_boot_data", merged["snapshot"], {"group_body_va": "0x4ab7a0", "person_body_va": "0x4b8d50",
		"group_menu_boundary_va": "0x4a7c40", "projection": "captured_school_boot_fields"})
	_phase = "school_boot_data"
	return _view("projected_once")


func _record(phase: String, after: Dictionary, source: Dictionary) -> void:
	_log.append({"phase": phase, "before": _snapshot.duplicate(true), "after": after.duplicate(true),
		"source": source.duplicate(true)})
	_snapshot = after.duplicate(true)


func _view(status: String) -> Dictionary:
	return {"supported": true, "status": status, "after": _snapshot.duplicate(true),
		"phase": _phase, "phase_log": _log.duplicate(true), "requested_state": _requested_state,
		"pending_flag": _pending_flag, "week_executed": _week_executed, "tasks": _tasks.duplicate(true),
		"completed": _phase in ["school_constructed", "school_boot_data"],
		"school_constructed": _phase in ["school_constructed", "school_boot_data"],
		"school_boot_data_projected": _phase == "school_boot_data", "interactive_school_ready": false,
		"execution_scope": "isolated_sourced_return_checkpoints", "school_initialized": false,
		"live_witness": false, "authorizes_persistent_write": false}


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "school_initialized": false,
		"live_witness": false, "authorizes_persistent_write": false}
