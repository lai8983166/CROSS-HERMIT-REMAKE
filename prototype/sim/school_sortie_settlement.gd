extends RefCounted
## Settle the current May departure using its command-replayed battle facts.
const Adventures := preload("res://sim/school_return_adventures.gd")
const Courses := preload("res://sim/school_return_courses.gd")
const Battle := preload("res://sim/school_battle_settlement.gd")
const Return := preload("res://sim/school_postbattle_return.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const Origin := preload("res://sim/new_game_school_origin.gd")
const TASK_PATH := "res://data/school_sortie_reward_rules.json"
const TASK_SHA := "81020c8f0bba894d13c49e3e825d54f0c7597e67a17c597e4ca5e3373512c7de"


static func apply(bundle: Dictionary, handoff: Dictionary, facts: Dictionary, opening_ledger: Dictionary = {}, task_grades: Dictionary = {}) -> Dictionary:
	if bundle.get("phase") != "sortie_committed":
		return Origin.failure("settlement_requires_committed_sortie")
	var school: Variant=bundle.get("school")
	var previous: Variant=bundle.get("sortie_result",{})
	if not school is Dictionary or school.get("week") not in [1,2,3,4,5] or not previous is Dictionary:
		return Origin.failure("invalid_sortie_school")
	var week: int=school["week"]
	var june: bool=school["month"]==6
	var july: bool=school["month"]==7
	var august: bool=school.month==8 and week in [2,3,4,5]
	var december: bool=[school.month,week]==[12,1]
	var november: bool=[school.month,week]==[11,3]
	var september: bool=school.month==9 and week in [3,4]
	var ledger := opening_ledger if december or june or july or august or week>=3 else Adventures.initial()
	if school["month"]==5 and week==2:
		var previous_id: Variant=previous.get("scene_id",0)
		if ledger.is_empty() or previous_id not in [0,8,17]:
			return Origin.failure("invalid_previous_sortie")
		ledger=Adventures.advance(ledger,previous_id)
		Adventures._open(ledger,5,2,Adventures.rules())
		if opening_ledger!=ledger: return Origin.failure("sortie_opening_ledger_mismatch")
	var school_before := bundle.duplicate(true)
	school_before["phase"] = "school_returned"
	var expected := Adventures.submit(school_before,ledger)
	if not expected.get("supported",false) or expected["handoff"] != handoff:
		return Origin.failure("sortie_departure_mismatch")
	var prepared: Dictionary = handoff["prepared"]
	var scene_id: int = prepared["adventure_id"]
	var round_data: Dictionary = prepared["rounds"][0]
	var ids: Array = round_data["student_ids"]
	var slots: Variant = facts.get("objective_slots")
	if (facts.get("scene_id") != scene_id or (scene_id not in [4,6,7,9,13,14,20,21,22,24,31,35,41] and facts.get("time_key") != 0) or not Roles._bounded(facts.get("time_key"),1 if scene_id in [4,6,7,9,13,14,20,21,22,24,31,35,41] else 0,3)
			or not Roles._vector(slots,16,0,1) or slots.slice(0 if scene_id in [6,9,10,13,18,20,21,35] else 1 if scene_id in [7,22,24,41] else 2 if scene_id in [4,8,31] else 3).has(1)
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
	var initial_grade := 5
	if school["month"]==5 and week==2 and previous.get("scene_id")==scene_id:
		if not Roles._bounded(previous.get("task_grade"),1,5): return Origin.failure("invalid_previous_task_grade")
		initial_grade=previous["task_grade"]
	if december or june or july or august or week>=3:
		var previous_tasks := [8,17]
		if week==5 or june or july or august: previous_tasks.append(7)
		if august or july or (june and week>=2): previous_tasks.append(4)
		if august or july or (june and week>=3): previous_tasks.append(6)
		if august or july or (june and week>=4): previous_tasks.append(10)
		if august or july or (june and week==5): previous_tasks.append(13)
		if august or (july and week>=2): previous_tasks.append(18)
		if august or (july and week>=4): previous_tasks.append(9)
		if august or (july and week==5): previous_tasks.append(14)
		if august and week>=3: previous_tasks.append(20)
		if august and week>=4: previous_tasks.append(21)
		if september:
			previous_tasks=[4,6,7,8,9,10,13,14,17,18,20,21,35]
			if week==4: previous_tasks.append(22)
		if november or december:previous_tasks=[4,6,7,8,9,10,13,14,17,18,20,21,22,24,35]
		if december:previous_tasks.append(41)
		for task in task_grades:
			if task not in previous_tasks or not Roles._bounded(task_grades[task],1,5):
				return Origin.failure("invalid_previous_task_grade")
		initial_grade=task_grades.get(scene_id,5)
	var score := Battle.Score.calculate({"task_id":scene_id,"mode":0,"cap_mode":0,
		"result_selector":facts.get("result_selector"),"time_key":facts["time_key"],
		"unit_key":facts.get("unit_condition_key"),"characters":characters,"initial_grade":initial_grade,
		"initial_total":bundle["school"]["global_total_511c"]},rules["score"],week==5,july or (june and week==5),(july and week==5) or (august and week==4))
	if not score["supported"]: return score
	var loot := Battle.Loot._loot(bundle["item_flags"],score["grade_index"],facts,rules)
	for i in range(records.size()):
		records[i].merge(score["characters"][i],true)
	var after := bundle.duplicate(true)
	after["school"]["global_total_511c"] = score["total_after"]
	var classes := []
	for group in range(5):
		var members := []
		for i in range(ids.size()):
			if round_data["student_groups"][i]==group: members.append(ids[i])
		if members.is_empty():continue
		var teacher := Courses.Groups._word(school["group_raw_bytes"],group*28)
		classes.append({"students":members,"teacher":teacher,"work_fields":prepared["class_ratings"][group]["work_fields"],"activity":2})
	var lessons := []
	var lesson_rules := {}
	if week==5 or july or (august and week==4):
		var plan := Courses._plan(school,Courses._rules(),true)
		if not plan["supported"]:return plan
		classes=plan["classes"]
		lessons=plan["plan"]
		lesson_rules=Courses.lesson_rules(school.month,school.week)
		if lesson_rules.is_empty():return Origin.failure("invalid_week_five_lessons")
	var growth := _grow_classes(after,classes,records,lessons,lesson_rules,rules["role"],facts["growth_seed"])
	if not growth["supported"]:return growth
	var recipient: int=growth["recipient"]
	if recipient < 0 and not (december or november or september or august or (july and week==5)): return Origin.failure("missing_positive_sortie_recipient")
	var confirmation := Courses._confirm(after,classes,rules["job_categories"],2)
	var grade_calls := []
	var delta: int = Battle.Confirmation.GRADE_DELTA[score["grade_index"]]
	for a in ids:
		for b in ids:
			if a != b: grade_calls.append({"from":a,"to":b,"delta":delta})
	for id in ids:
		for teacher in round_data["teacher_ids"]:
			grade_calls.append({"from":id,"to":teacher,"delta":delta})
			grade_calls.append({"from":teacher,"to":id,"delta":delta})
	Courses._apply_relationships(after,grade_calls)
	confirmation["relationship_calls"].append_array(grade_calls)
	var old_count := 0
	if recipient>=0:
		var count := Return._find(after["counts"],recipient)
		old_count=count["count"]
		count["count"]=mini(old_count+1,5)
	after["item_flags"] = loot["item_flags"]
	Return._sync_participants(after)
	var rated := Courses.Groups.rate(after["school"],Return.group_rules(after["school"]))
	if not rated["supported"]: return rated
	after["school"] = Courses.Session._canonical(rated["after"])
	after["ratings"] = rated["ratings"]
	after["rankings"] = Return._rankings(after["school"])
	var summary := {"scene_id":scene_id,"date":[school["month"],week],"result_selector":facts["result_selector"],
		"task_grade":score["task_grade"],"score":score,"loot_groups":loot["loot_groups"],
		"loot_draws":loot["draws"],"clock_seed":facts["clock_seed"],"growth_seed":facts["growth_seed"],
		"learning_draws":growth["learning_draws"],"students":growth["students"],"recipient":recipient,
		"old_mvp_count":old_count,"mvp_script":"allresult/dat/mvp%03d.ybc" % recipient if recipient>=0 else "allresult/dat/nomvp.ybc",
		"history_index":(bundle["school"]["month"]-4)*5+week-1,"relationship_calls":confirmation["relationship_calls"],
		"adv_request":{"state":6,"script":"adv/dat/ch003.ybc","next_task":7,"week_advanced":false}}
	if week==5 or july or (august and week==4) or september or november or december:
		summary["lessons"]=growth["lessons"]
		summary["rand_state"]=growth["rand_state"]
	after["sortie_result"] = summary.duplicate(true)
	after["phase"] = "sortie_settled"
	return Return._result(after,"sortie_settled",{"summary":summary})


## 4C00C0 dispatches each student in class/slot order with one RNG and one MVP.
static func _grow_classes(after: Dictionary, classes: Array, records: Array, lessons: Array,
		lesson_rules: Dictionary, role_rules: Dictionary, seed: int) -> Dictionary:
	var state := seed
	var draws := []
	var battle_changes := []
	var teaching := {"students":[],"packets":[],"bonus":0,"learning_draws":[],"skill_display_needed":0}
	var recipient := -1
	var best := 0
	for item in classes:
		var changes := []
		if item["activity"]==1:
			var rows := lessons.filter(func(row):return row["character_id"] in item["students"])
			var result := Courses.apply_lessons(after,rows,lesson_rules,state)
			changes=result["students"]
			for key in ["students","packets","learning_draws"]:teaching[key].append_array(result[key])
			teaching["bonus"]+=result["bonus"]
			teaching["skill_display_needed"]=maxi(teaching["skill_display_needed"],result["skill_display_needed"])
			state=result["rand_state"]
			draws.append_array(result["learning_draws"])
		elif item["activity"]==2:
			var members: Array=item["students"]
			var inputs := records.filter(func(row):return row["character_id"] in members)
			var result := Roles.project_growth_records(inputs,members,state,role_rules,
				[after.school.month,after.school.week] in [[7,5],[8,2],[8,3],[8,4],[8,5],[9,3],[9,4],[11,3],[12,1]],
				[after.school.month,after.school.week] in [[8,5],[9,3],[9,4],[11,3],[12,1]],
				[after.school.month,after.school.week] in [[11,3],[12,1]],
				[after.school.month,after.school.week]==[12,1])
			if not result["supported"]:return result
			for row in result["after"]["characters"]:
				var id: int=row["character_id"]
				var current := Return._find(after["growth"],id)
				var learned := []
				for sid in range(84):
					if current["skill_statuses"][sid]!=row["skill_statuses"][sid]:learned.append(sid+1)
				changes.append({"character_id":id,"before_attributes":current["attributes"].duplicate(),
					"attributes":row["attributes"].duplicate(),"before_level":current["level_50"],"level":row["level_50"],
					"new_skill_ids":learned,"staged_total":row["staged_total"]})
				current.merge(Origin.field_subset(row,Return.GROWTH_KEYS),true)
				for profile in after["school"]["member_profiles"]:
					if profile["member_id"]==id:
						profile["attributes"]=current["attributes"].duplicate()
						profile["level_50"]=current["level_50"]
			battle_changes.append_array(changes)
			state=result["rand_state"]
			draws.append_array(result["learning_draws"])
		for change in changes:
			if change["character_id"]<13 and change["staged_total"]>best:
				best=change["staged_total"]
				recipient=change["character_id"]
	return {"supported":true,"students":battle_changes,"lessons":teaching,"learning_draws":draws,
		"recipient":recipient,"rand_state":state}


static func _rules(scene_id: int) -> Dictionary:
	var raw := FileAccess.get_file_as_string(TASK_PATH).replace("\r\n","\n")
	if raw.sha256_text() != TASK_SHA: return {}
	var task: Dictionary
	if scene_id in [4,6,7,9,10,13,14,18,20,21,22,24,31,35,41]:
		var mission := Adventures.mission_rules(scene_id)
		if mission.is_empty():return {}
		task=mission["rewards"]
	else:
		task=Roles._integers(JSON.parse_string(raw)[str(scene_id)])
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
