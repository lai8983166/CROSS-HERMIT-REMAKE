extends RefCounted
## Settle the current 5/1 departure using its command-replayed battle facts.
const Adventures := preload("res://sim/school_return_adventures.gd")
const Courses := preload("res://sim/school_return_courses.gd")
const Battle := preload("res://sim/school_battle_settlement.gd")
const Return := preload("res://sim/school_postbattle_return.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const Origin := preload("res://sim/new_game_school_origin.gd")
const TASK_PATH := "res://data/school_sortie_reward_rules.json"
const TASK_SHA := "81020c8f0bba894d13c49e3e825d54f0c7597e67a17c597e4ca5e3373512c7de"


static func apply(bundle: Dictionary, handoff: Dictionary, facts: Dictionary) -> Dictionary:
	if bundle.get("phase") != "sortie_committed":
		return Origin.failure("settlement_requires_committed_sortie")
	# This first optional sortie follows the reconstructed 5/1 ledger.
	var school_before := bundle.duplicate(true)
	school_before["phase"] = "school_returned"
	var expected := Adventures.submit(school_before, Adventures.initial())
	if not expected.get("supported",false) or expected["handoff"] != handoff:
		return Origin.failure("sortie_departure_mismatch")
	var prepared: Dictionary = handoff["prepared"]
	var scene_id: int = prepared["adventure_id"]
	var round_data: Dictionary = prepared["rounds"][0]
	var ids: Array = round_data["student_ids"]
	var slots: Variant = facts.get("objective_slots")
	if (facts.get("scene_id") != scene_id or facts.get("time_key") != 0
			or not Roles._vector(slots,16,0,1) or slots.slice(2 if scene_id == 8 else 3).has(1)
			or not Roles._bounded(facts.get("clock_seed"),0,0x7fffffff)
			or not Roles._bounded(facts.get("growth_seed"),0,0x7fffffff)
			or not facts.get("units") is Array or facts["units"].size() != ids.size()):
		return Origin.failure("invalid_sortie_result_facts")
	var rules := _rules(scene_id)
	if rules.is_empty(): return Origin.failure("invalid_sortie_result_rules")
	var records := []
	var characters := []
	for i in range(ids.size()):
		var id: int = ids[i]
		var unit: Variant = facts["units"][i]
		if not unit is Dictionary or unit.get("character_id") != id:
			return Origin.failure("sortie_result_participant_mismatch")
		var record := Return._find(bundle["growth"],id).duplicate(true)
		record["job_progress"] = Return._find(bundle["records"],id)["job_progress"].slice(0,31)
		var character := Origin.field_subset(unit,["character_id","count_field_aa","contribution_field_ac","status_field_ae"])
		character["rate_class"] = rules["job_rate_classes"][record["job"]]
		character["growth_pools"] = record["growth_pools"]
		character["group_bonus"] = prepared["class_ratings"][round_data["student_groups"][i]]["relationship_mean"]
		var skill_points := 0
		for sid in range(84):
			if record["skill_statuses"][sid] in [3,5,6]:
				skill_points += int(rules["role"]["skills"][sid]["learned_points"])
		character["skill_points"] = skill_points
		characters.append(character)
		records.append(record)
	var score := Battle.Score.calculate({"task_id":scene_id,"mode":0,"cap_mode":0,
		"result_selector":facts.get("result_selector"),"time_key":facts["time_key"],
		"unit_key":facts.get("unit_condition_key"),"characters":characters,"initial_grade":5,
		"initial_total":bundle["school"]["global_total_511c"]},rules["score"])
	if not score["supported"]: return score
	var loot := Battle.Loot._loot(bundle["item_flags"],score["grade_index"],facts,rules)
	for i in range(records.size()):
		records[i].merge(score["characters"][i],true)
	var growth := Roles.project_growth_records(records,ids,facts["growth_seed"],rules["role"])
	if not growth["supported"]: return growth
	var after := bundle.duplicate(true)
	var best := 0
	var recipient := -1
	var changes := []
	for row in growth["after"]["characters"]:
		var id: int = row["character_id"]
		var old := Return._find(bundle["growth"],id)
		var current := Return._find(after["growth"],id)
		current.merge(Origin.field_subset(row,Return.GROWTH_KEYS),true)
		var learned := []
		for sid in range(84):
			if old["skill_statuses"][sid] != current["skill_statuses"][sid]: learned.append(sid+1)
		changes.append({"character_id":id,"before_attributes":old["attributes"].duplicate(),
			"attributes":current["attributes"].duplicate(),"before_level":old["level_50"],"level":current["level_50"],
			"new_skill_ids":learned,"staged_total":current["staged_total"]})
		for profile in after["school"]["member_profiles"]:
			if profile["member_id"] == id:
				profile["attributes"] = current["attributes"].duplicate()
				profile["level_50"] = current["level_50"]
		if current["staged_total"] > best:
			best = current["staged_total"]
			recipient = id
	if recipient < 0: return Origin.failure("missing_positive_sortie_recipient")
	var rating: Dictionary = prepared["class_ratings"][round_data["student_groups"][0]]
	var classes := [{"students":ids,"teacher":101,"work_fields":rating["work_fields"]}]
	var confirmation := Courses._confirm(after,classes,rules["job_categories"],2)
	var grade_calls := []
	var delta: int = Battle.Confirmation.GRADE_DELTA[score["grade_index"]]
	for a in ids:
		for b in ids:
			if a != b: grade_calls.append({"from":a,"to":b,"delta":delta})
	for id in ids:
		grade_calls.append({"from":id,"to":101,"delta":delta})
		grade_calls.append({"from":101,"to":id,"delta":delta})
	Courses._apply_relationships(after,grade_calls)
	confirmation["relationship_calls"].append_array(grade_calls)
	var count := Return._find(after["counts"],recipient)
	var old_count: int = count["count"]
	count["count"] = mini(old_count+1,5)
	after["school"]["global_total_511c"] = score["total_after"]
	after["item_flags"] = loot["item_flags"]
	Return._sync_participants(after)
	var rated := Courses.Groups.rate(after["school"],Origin.group_rules())
	if not rated["supported"]: return rated
	after["school"] = Courses.Session._canonical(rated["after"])
	after["ratings"] = rated["ratings"]
	after["rankings"] = Return._rankings(after["school"])
	var summary := {"scene_id":scene_id,"date":[5,1],"result_selector":facts["result_selector"],
		"task_grade":score["task_grade"],"score":score,"loot_groups":loot["loot_groups"],
		"loot_draws":loot["draws"],"clock_seed":facts["clock_seed"],"growth_seed":facts["growth_seed"],
		"learning_draws":growth["learning_draws"],"students":changes,"recipient":recipient,
		"old_mvp_count":old_count,"mvp_script":"allresult/dat/mvp%03d.ybc" % recipient,
		"history_index":5,"relationship_calls":confirmation["relationship_calls"],
		"adv_request":{"state":6,"script":"adv/dat/ch003.ybc","next_task":7,"week_advanced":false}}
	after["sortie_result"] = summary.duplicate(true)
	after["phase"] = "sortie_settled"
	return Return._result(after,"sortie_settled",{"summary":summary})


static func _rules(scene_id: int) -> Dictionary:
	var raw := FileAccess.get_file_as_string(TASK_PATH).replace("\r\n","\n")
	if raw.sha256_text() != TASK_SHA: return {}
	var task: Dictionary = Roles._integers(JSON.parse_string(raw)[str(scene_id)])
	var base: Array = Battle.SOURCES["preparation"]
	raw = FileAccess.get_file_as_string(base[0]).replace("\r\n","\n")
	if raw.sha256_text() != base[1]: return {}
	var rules: Dictionary = Roles._integers(JSON.parse_string(raw)["rules"])
	rules["score"].merge(Origin.field_subset(task,["task_id","base_points","unit_bonus","time_bonuses","count_bonuses"]),true)
	rules.merge(Origin.field_subset(task,["loot_quotas","fixed_items","objective_rewards"]),true)
	var school_rules := Courses._rules()
	if school_rules.is_empty(): return {}
	rules["role"] = school_rules["role"]
	rules["job_categories"] = school_rules["confirmation"]["job_categories"]
	return rules
