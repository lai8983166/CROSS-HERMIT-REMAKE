extends RefCounted
## Window-facing session. Only native inputs/rules are retained, never oracle outputs.

const Campaign = preload("res://sim/campaign_result_state.gd")
const Return = preload("res://sim/battle_return.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const CHAIN_PATH := "res://data/campaign_scene5_evidence.json"
const PREP_PATH := "res://data/campaign_preparation_evidence.json"
const CHAIN_SHA := "b349bb3d0bfcd51407595f8cec02e37fd744684332e31f08d3279d9f615f79f0"
const PREP_SHA := "db3c9f1f133d307f2e1cbb874a17642995b82d6d8f478f5162a7f5ea19ad7a48"
const WAITLIST_PATH := "res://data/school_waitlist_evidence.json"
const WAITLIST_SHA := "3dc11db027bf6e821055bbe7c06d204bfc98160b8797ece209547b61596e823a"
const NOTICE := "返回流程演示：战果使用已核对源样例，不由当前战斗胜负计算。"
const IDS := [3, 4, 9]

var stage := "idle"
var route := 0
var error := ""
var _campaign: Campaign
var _handoff: Return
var _source: Dictionary = {}
var _summary: Dictionary = {}
var _loot: Array = []
var _before: Dictionary = {}
var _terminal: Dictionary = {}


func start(selected_route: int, chain_path := CHAIN_PATH, prep_path := PREP_PATH, waitlist_path := WAITLIST_PATH) -> bool:
	reset()
	if selected_route not in [0, 1]:
		return _fail("invalid_route")
	if not FileAccess.file_exists(chain_path) or not FileAccess.file_exists(prep_path) or not FileAccess.file_exists(waitlist_path):
		return _fail("missing_source")
	if FileAccess.get_sha256(chain_path) != CHAIN_SHA or FileAccess.get_sha256(prep_path) != PREP_SHA \
			or FileAccess.get_sha256(waitlist_path) != WAITLIST_SHA:
		return _fail("source_integrity_mismatch")
	var chain: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(chain_path))
	var preparation: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(prep_path))
	var example: Dictionary = chain["cases"][selected_route]
	var prep: Dictionary = preparation["cases"][selected_route]
	# Whitelist inputs so the session cannot access expected_after/summary/school.
	for key in ["event_world", "exit_frame", "dispatch_context", "round_before", "round_table", "context"]:
		_source[key] = example[key].duplicate(true)
	_source["preparation_inputs"] = prep["inputs"].duplicate(true)
	_before = Roles._integers(prep["before_world"])
	var rules: Dictionary = chain["rules"].duplicate(true)
	rules["preparation"] = preparation["rules"].duplicate(true)
	var waitlist: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(waitlist_path))
	rules["school_waitlist"] = waitlist["rules"].duplicate(true)
	_campaign = Campaign.new()
	if not _campaign.initialize(_before, rules):
		return _fail("invalid_source_catalog")
	_handoff = Return.new()
	route = selected_route
	stage = "battle"
	return true


func reset() -> void:
	stage = "idle"
	route = 0
	error = ""
	_campaign = null
	_handoff = null
	_source.clear()
	_summary.clear()
	_loot.clear()
	_before.clear()
	_terminal.clear()


static func battle_setup(base: Dictionary) -> Dictionary:
	var setup := base.duplicate(true)
	var units := []
	var ally := 0
	for unit in setup.get("units", []):
		if int(unit.get("faction", -1)) == 0:
			if ally >= IDS.size():
				continue
			unit["character_id"] = IDS[ally]
			ally += 1
		units.append(unit)
	if ally != IDS.size():
		return {}
	setup["units"] = units
	setup.erase("skill_demo")
	return setup


func accept_terminal(terminal: Dictionary) -> bool:
	if stage != "battle":
		return false
	if not _handoff.accept_terminal_snapshot(terminal):
		return _fail("invalid_terminal")
	_terminal = terminal.duplicate(true)
	var gate := _handoff.prepare_scene5_result_replay(_source["event_world"], _source["exit_frame"],
		_source["dispatch_context"], _source["round_before"], _source["round_table"], true)
	if not gate.get("supported", false):
		return _fail(gate.get("reason", "invalid_gate"))
	var prepared := _handoff.prepare_tactics_replay("demo-preparation", _source["preparation_inputs"], _campaign)
	if not prepared.get("supported", false):
		return _fail(prepared.get("reason", "invalid_preparation"))
	_summary = prepared["result"]["summary"].duplicate(true)
	_loot = prepared["result"]["loot_groups"].duplicate(true)
	var result := _handoff.begin_result_replay("demo-result", _source["context"], _campaign)
	if not result.get("supported", false):
		return _fail(result.get("reason", "invalid_result"))
	stage = "result"
	return true


func confirm_result() -> bool:
	if stage in ["settled", "school"]:
		return true
	if stage != "result":
		return false
	var result := _handoff.finish_result_replay("demo-result", true, true)
	if not result.get("supported", false):
		return _fail(result.get("reason", "result_failed"))
	stage = "settled"
	return true


func enter_school() -> bool:
	if stage == "school":
		return true
	if stage != "settled":
		return false
	var result := _handoff.begin_school_return_replay("demo-school")
	if not result.get("supported", false):
		return _fail(result.get("reason", "return_failed"))
	result = _handoff.advance_school_return_replay("demo-school", true, true, true)
	if not result.get("school_constructed", false):
		return _fail(result.get("reason", "school_failed"))
	result = _handoff.project_school_return_boot_replay("demo-school")
	if not result.get("school_boot_data_projected", false):
		return _fail(result.get("reason", "school_boot_failed"))
	stage = "school"
	return true


func sort_waitlist(mode: Variant) -> bool:
	if stage != "school":
		return false
	return _campaign.sort_school_waitlist("demo-school", mode).get("supported", false)


func view() -> Dictionary:
	return {"stage": stage, "route": route, "error": error, "notice": NOTICE,
		"snapshot": _campaign.read_snapshot() if _campaign != null else {},
		"revision": _campaign.revision() if _campaign != null else 0,
		"before": _before.duplicate(true), "summary": _summary.duplicate(true),
		"loot": _loot.duplicate(true), "terminal": _terminal.duplicate(true),
		"school_initialized": false, "interactive_school_ready": false,
		"live_witness": false, "authorizes_persistent_write": false}


func journal() -> Array:
	return _campaign.journal() if _campaign != null else []


func _fail(reason: String) -> bool:
	error = reason
	stage = "error"
	return false
