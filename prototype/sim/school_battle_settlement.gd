extends RefCounted
## Current remake battle -> source score/loot -> growth -> confirmation -> ADV request.
## Owns an in-memory result, never substitutes fixture case outputs or writes saves.
const Roles := preload("res://sim/all_result_role_replay.gd")
const Score := preload("res://sim/tactics_score_preparation.gd")
const Loot := preload("res://sim/campaign_tactics_preparation.gd")
const Confirmation := preload("res://sim/school_battle_confirmation.gd")
const Preparation := preload("res://sim/school_adventure_preparation.gd")
const CourseGrowth := preload("res://sim/school_course_settlement.gd")
const SOURCES := {
	"preparation":["res://data/campaign_preparation_evidence.json","db3c9f1f133d307f2e1cbb874a17642995b82d6d8f478f5162a7f5ea19ad7a48"],
	"role":["res://data/role_application_evidence.json","b0c1f014711dabe3a70482967f58761d8915779da1bbcfcf2eadb18969d38055"]}
var _context: Dictionary = {}
var _rules: Dictionary = {}
var _result: Dictionary = {}
var _phase := "closed"


func initialize(context: Dictionary) -> bool:
	if _phase != "closed": return false
	var rules := {}
	for key in SOURCES:
		var text := FileAccess.get_file_as_string(SOURCES[key][0]).replace("\r\n","\n")
		if text.sha256_text() != SOURCES[key][1]: return false
		# Read only source tables; cases and synthetic expected worlds are not inputs.
		rules[key] = Roles._integers(JSON.parse_string(text)["rules"])
	if not context.get("school") is Dictionary or not context.get("preparation") is Dictionary \
			or not context.get("growth") is Array or not context.get("records") is Array \
			or not context.get("counts") is Array: return false
	var prepared := Preparation.project(context["school"],Roles._integers(JSON.parse_string(
		FileAccess.get_file_as_string(Preparation.RULE_PATH))))
	if not prepared.get("ready",false) or prepared["prepared"] != context["preparation"]: return false
	if not CourseGrowth._validate_records(context["school"],context["growth"],rules["role"]).is_empty() \
			or not Confirmation.Confirmation.valid_records(context["records"]) \
			or not Confirmation.Handoff.valid_counts(context["counts"]): return false
	if not Roles._bounded(context.get("clock_seed"),0,0x7fffffff) \
			or not Roles._bounded(context.get("growth_seed"),0,0x7fffffff) \
			or context.get("origin") != "current_new_game_first_scene5": return false
	_context = context.duplicate(true); _rules = rules; _phase = "waiting_battle"
	return true


func prepare(tactical: Dictionary) -> Dictionary:
	if _phase != "waiting_battle": return _failure("result_already_prepared")
	if not tactical.get("units") is Array or not Roles._vector(tactical.get("objective_slots"),16,0,1):
		return _failure("invalid_battle_result")
	for unit in tactical["units"]:
		if not unit is Dictionary: return _failure("invalid_battle_unit")
	var round: Dictionary = _context["preparation"]["rounds"][0]
	var ids: Array = round["student_ids"]
	if tactical["units"].map(func(u): return u.get("character_id")) != ids:
		return _failure("battle_participant_mismatch")
	var characters := []
	var records := []
	for index in range(ids.size()):
		var id: int = ids[index]
		var matches: Array = _context["growth"].filter(func(r): return r["character_id"]==id)
		var history: Array = _context["records"].filter(func(r): return r["character_id"]==id)
		if matches.size()!=1 or history.size()!=1: return _failure("missing_current_growth")
		var record: Dictionary = matches[0].duplicate(true)
		record["job_progress"] = history[0]["job_progress"].slice(0,31)
		var points := 0
		for sid in range(84):
			if record["skill_statuses"][sid] in [3,5,6]: points += int(_rules["role"]["skills"][sid]["learned_points"])
		var character: Dictionary = tactical["units"][index].duplicate(true)
		character.merge({"rate_class":_rules["preparation"]["job_rate_classes"][record["job"]],
			"growth_pools":record["growth_pools"].duplicate(),"skill_points":points,
			"group_bonus":_context["preparation"]["class_ratings"][round["student_groups"][index]]["relationship_mean"]})
		characters.append(character); records.append(record)
	var score := Score.calculate({"task_id":5,"mode":0,"cap_mode":0,
		"result_selector":tactical.get("result_selector"),"time_key":tactical.get("time_key"),
		"unit_key":tactical.get("unit_condition_key"),"initial_grade":5,
		"initial_total":_context["school"]["global_total_511c"],"characters":characters},_rules["preparation"]["score"])
	if not score["supported"]: return score
	# 49E930 clears the new-game item words, initializes all task grades to5.
	# This playground has no prior adventure/item-grant commands. This first result
	# owns the new inventory; it is not a claim about an imported original save.
	var flags := []; flags.resize(360); flags.fill(0)
	var loot := Loot._loot(flags,score["grade_index"],{"clock_seed":_context["clock_seed"],
		"objective_slots":tactical["objective_slots"]},_rules["preparation"])
	if not loot["supported"]: return loot
	for i in range(records.size()):
		records[i]["staged_package"] = score["characters"][i]["staged_package"].duplicate()
		records[i]["staged_total"] = score["characters"][i]["staged_total"]
	# Validate growth and post fields before publishing any reward stage.
	var growth := Roles.project_growth_records(records,ids,_context["growth_seed"],_rules["role"])
	if not growth["supported"]: return growth
	var confirmed := Confirmation.apply(_context["school"],_context["records"],growth["after"]["characters"],
		_context["counts"],_context["preparation"],score["grade_index"])
	if not confirmed["supported"]: return confirmed
	confirmed["after"]["global_total_511c"] = score["total_after"]
	_result = {"tactical":tactical.duplicate(true),"score":score,"loot":loot,
		"prepared_records":records,"growth":growth,"confirmation":confirmed}
	_phase = "round_result"
	return snapshot()


func confirm_round() -> Dictionary:
	if _phase == "round_result": _phase = "total_result"
	elif _phase not in ["total_result","adv_pending"]: return _failure("round_result_not_ready")
	return snapshot()


func confirm_total(mvp_ready: bool) -> Dictionary:
	if _phase == "total_result" and mvp_ready: _phase = "adv_pending"
	elif _phase not in ["total_result","adv_pending"]: return _failure("total_result_not_ready")
	return snapshot()


func snapshot() -> Dictionary:
	var output := {"supported":true,"phase":_phase,"native_equivalence_verified":false,
		"authorizes_persistent_write":false,"week_advanced":false,"original_save_written":false}
	if _result.is_empty(): return output
	output.merge({"tactical":_result["tactical"].duplicate(true),"score":_result["score"].duplicate(true),
		"loot_groups":_result["loot"]["loot_groups"].duplicate(true),
		"item_flags":_result["loot"]["item_flags"].duplicate(),
		"growth_applied":_phase in ["total_result","adv_pending"],"confirmation_applied":_phase=="adv_pending"})
	if output["growth_applied"]:
		output["growth"] = _result["growth"].duplicate(true)
		output["recipient"] = _result["confirmation"]["recipient"]
	if output["confirmation_applied"]:
		output["confirmation"] = _result["confirmation"].duplicate(true)
		output["adv_request"] = _result["confirmation"]["adv_request"].duplicate(true)
	return output


static func _failure(reason: String) -> Dictionary:
	return {"supported":false,"reason":reason,"authorizes_persistent_write":false}
