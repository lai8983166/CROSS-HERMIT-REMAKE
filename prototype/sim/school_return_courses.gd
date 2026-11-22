extends RefCounted
## Current returned school roster adapter. Original 4/4 fixture gates stay intact.
## Pure commands; the owning replay commits one result and advances the story/week.
const Origin := preload("res://sim/new_game_school_origin.gd")
const Return := preload("res://sim/school_postbattle_return.gd")
const Session := preload("res://sim/new_game_school_session.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")
const Teacher := preload("res://sim/school_teacher_movement.gd")
const Planning := preload("res://sim/school_course_planning.gd")
const Growth := preload("res://sim/school_course_settlement.gd")
const Confirmation := preload("res://sim/school_course_confirmation.gd")
const Courses := preload("res://sim/school_course_unlocking.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const MAY_FIVE_SHA := "f1672fbbbae4b817bd3e1188c734493538411c73461f71b59880e9bb84d2fc04"
const JUNE_FIVE_SHA := "34f20195975120edf92a77ad82ba106cfd481186c54a6e9e9fbfd5683ede6683"
const AUGUST_FOUR_SHA := "12b84b6c1b134f8fd0d9b459f8af68b6eb465b4c14e2e95c3515000799eade30"
const SEPTEMBER_ONE_SHA := "d5d82913601e590e8a98e8e279e14e8edb2c5a27d88ab563e271090b2322bde3"
const SEPTEMBER_TWO_SHA := "fb52868543960fa9883dca08e265a6945a10e14ce25a92de2db7fbc5f4e5c2f0"
const SOURCES := {
	"growth":["res://data/school_course_settlement_rules.json","5f2738db67bdacf1677e6de1c823ac8dfa542e6b103cd913af9c51a2fe93c439"],
	"confirmation":["res://data/school_course_confirmation_rules.json","2a75e6e4dd30ae8e99a5e014dc3ba87b646f65b73b3a04d03999d2ceaebaf6a6"]}


static func list_courses(before: Dictionary, group: Variant) -> Dictionary:
	var rules := _rules()
	var reason := _guard(before,rules)
	if not reason.is_empty(): return Origin.failure(reason)
	if not Courses._integer(group,0,4): return Origin.failure("invalid_return_course_class")
	var selected := Teacher.select_group(Session._working(before["school"]),group,Return.group_rules(before["school"]),Return.work_rules(before["school"],rules))
	if not selected["supported"]: return selected
	var output := Origin.success("return_course_list")
	output.merge({"group":group,"courses":selected["after"]["work_rows"].duplicate(true)})
	return output


static func set_mode(before: Dictionary, group: Variant, teaching: Variant) -> Dictionary:
	var rules := _rules()
	var reason := _guard(before,rules)
	if not reason.is_empty(): return Origin.failure(reason)
	var school: Dictionary=before["school"]
	if teaching==true and school["adventure_gate"]!=0 and (school["week"]==4 or school["month"]==6 or (school["month"]==7 and school["week"]==3) or (school.month==8 and school.week in [2,3]) or [school.month,school.week]==[9,3]):
		return Origin.failure("mandatory_adventure_requires_sortie")
	var changed := Planning.set_mode(Session._working(before["school"]),group,teaching,Return.group_rules(before["school"]),Return.work_rules(before["school"],rules))
	if not changed["supported"]: return changed
	return _publish_plan(before,changed["after"])


static func assign_course(before: Dictionary, group: Variant, work_id: Variant) -> Dictionary:
	var rules := _rules()
	var reason := _guard(before,rules)
	if not reason.is_empty(): return Origin.failure(reason)
	if not Courses._integer(group,0,4) or not Courses._integer(work_id,1,100):
		return Origin.failure("invalid_return_course_command")
	var selected := Teacher.select_group(Session._working(before["school"]),group,Return.group_rules(before["school"]),Return.work_rules(before["school"],rules))
	if not selected["supported"]: return selected
	var working: Dictionary = selected["after"]
	for category in range(3):
		for row in working["work_rows"][category]:
			if row[1] != work_id: continue
			var ordinal: int = row[2]
			var page := maxi(0,int(ceil((ordinal-9)/2.0)))
			working["course_category"] = category
			working["work_pages"][category] = page
			working["detail_work_id"] = -1
			working["detail_previous_work_id"] = -1
			var chosen := Planning.select_course(working,{"group":group,"category":category,"row":ordinal-page*2,"page":page,"clicked":true},Return.group_rules(before["school"]),Return.work_rules(before["school"],rules))
			if not chosen["supported"]: return chosen
			return _publish_plan(before,chosen["after"])
	return Origin.failure("return_course_unavailable")


static func _publish_plan(before: Dictionary, school: Dictionary) -> Dictionary:
	var rated := Groups.rate(school,Return.group_rules(school))
	if not rated["supported"]: return rated
	var after := before.duplicate(true)
	after["school"] = Session._canonical(rated["after"])
	after["ratings"] = rated["ratings"]
	return Return._result(after,"duplicate" if after==before else "return_course_planned")


static func settle(before: Dictionary, seed: Variant = 4660) -> Dictionary:
	var rules := _rules()
	if not Courses._integer(seed,0,0x7fffffff): return Origin.failure("invalid_declared_clock_seed")
	var reason := _guard(before,rules,true)
	if not reason.is_empty(): return Origin.failure(reason)
	var week: int=before["school"]["week"]
	var month: int=before["school"]["month"]
	if not ((month==5 and week in [1,2,3,5]) or (month==6 and week==5) or (month==7 and week in [1,2,5]) or (month==8 and week in [1,4]) or (month==9 and week in [1,2])): return Origin.failure("outside_supported_course_week")
	if before.get("phase")=="courses_confirmed":
		if not before.get("course_result") is Dictionary or before["course_result"].get("declared_clock_seed")!=seed:
			return Origin.failure("return_course_result_conflict")
		return Return._result(before.duplicate(true),"duplicate",{"summary":before["course_result"].duplicate(true)})
	var prepared := _plan(before["school"],rules)
	if not prepared["supported"]: return prepared
	var after := before.duplicate(true)
	var growth_rules: Dictionary=lesson_rules(month,week) if week==5 or month>=7 else rules["growth"]
	if growth_rules.is_empty():return Origin.failure("invalid_return_course_sources")
	var growth := apply_lessons(after,prepared["plan"],growth_rules,seed)
	# MVP is chosen from this result's assigned slots, never stale waiting totals.
	var recipient := -1
	var best := 0
	for command in prepared["plan"]:
		var row := Return._find(after["growth"],command["character_id"])
		if row["character_id"]<13 and row["staged_total"]>best:
			best=row["staged_total"];recipient=row["character_id"]
	# Courses 6 and 26 put their entire award in packet[7]. Original 4C00C0
	# leaves the recipient at -1. Do not index counts with this sentinel.
	var bonus_only: bool = (week in [3,5] or month==7) and prepared["plan"].all(func(command):return command["training_id"] in [6,26])
	if recipient<0 and not bonus_only and [month,week] not in [[7,5],[8,1],[8,4],[9,1],[9,2]]: return Origin.failure("missing_positive_return_course_mvp")
	var confirmed := _confirm(after,prepared["classes"],rules["confirmation"]["job_categories"])
	var old_count := 0
	if recipient>=0:
		var counts := Return._find(after["counts"],recipient)
		old_count = counts["count"]
		counts["count"] = clampi(old_count+1,0,5)
	Return._sync_participants(after)
	var rated := Groups.rate(after["school"],Return.group_rules(after["school"]))
	if not rated["supported"]: return rated
	after["school"] = Session._canonical(rated["after"])
	after["ratings"] = rated["ratings"]
	after["rankings"] = Return._rankings(after["school"])
	var summary := {"date":[month,week],"declared_clock_seed":seed,"packets":growth["packets"],
		"learning_draws":growth["learning_draws"],"rand_state":growth["rand_state"],"bonus":growth["bonus"],
		"skill_display_needed":growth["skill_display_needed"],"recipient":recipient,"old_mvp_count":old_count,
		"mvp_script":"allresult/dat/mvp%03d.ybc" % recipient if recipient>=0 else "allresult/dat/nomvp.ybc" if [month,week] in [[7,5],[8,1],[8,4],[9,1],[9,2]] else "","history_index":(before["school"]["month"]-4)*5+week-1,
		"relationship_calls":confirmed["relationship_calls"],"students":growth["students"],
		"adv_request":{"state":6,"script":"adv/dat/ch003.ybc","next_task":7,"chapter_completed":false,"week_advanced":false}}
	after["course_result"] = summary
	after["phase"] = "courses_confirmed"
	return Return._result(after,"return_courses_confirmed",{"summary":summary.duplicate(true)})


static func lesson_rules(month := 5, week := 1) -> Dictionary:
	if month not in [5,6,7,8] and not (month==9 and week in [1,2]):return {}
	var source := _rules()
	if source.is_empty():return {}
	var growth: Dictionary=source["growth"]
	var tables := [["res://data/school_may_five_courses.json",MAY_FIVE_SHA]]
	if month>=6:
		tables.append(["res://data/school_june_five_courses.json",JUNE_FIVE_SHA])
	var size := 30 if month>=6 else 28
	if (month==8 and week in [4,5]) or (month==9 and week in [1,2]):
		tables.append(["res://data/school_august_four_courses.json",AUGUST_FOUR_SHA])
		size=34
	if (month==9 and week in [1,2]):
		tables.append(["res://data/school_september_one_courses.json",SEPTEMBER_ONE_SHA])
		size=37
	if [month,week]==[9,2]:
		tables.append(["res://data/school_september_two_courses.json",SEPTEMBER_TWO_SHA])
	growth["training"].resize(size)
	for table in tables:
		var raw := FileAccess.get_file_as_string(table[0]).replace("\r\n","\n")
		if raw.sha256_text()!=table[1]:return {}
		var extra: Dictionary=Roles._integers(JSON.parse_string(raw))
		for id in extra:growth["training"][int(id)]=extra[id]
	return growth


static func apply_lessons(after: Dictionary, plan: Array, rules: Dictionary, seed: int) -> Dictionary:
	var previous: Array=after["growth"]
	var growth := _grow(after["growth"],plan,rules,after["school"]["difficulty"],seed)
	after["growth"] = growth["records"]
	after["school"]["global_total_511c"] = clampi(after["school"]["global_total_511c"]+growth["bonus"],0,999999999)
	for row in after["growth"]:
		for profile in after["school"]["member_profiles"]:
			if profile["member_id"]==row["character_id"]:
				profile["attributes"]=row["attributes"].duplicate()
				profile["level_50"]=row["level_50"]
	var changes := []
	for command in plan:
		var id: int = command["character_id"]
		var old := Return._find(previous,id)
		var current := Return._find(after["growth"],id)
		var learned := []
		for sid in range(84):
			if old["skill_statuses"][sid]!=current["skill_statuses"][sid]: learned.append(sid+1)
		changes.append({"character_id":id,"work_id":command["training_id"],
			"before_attributes":old["attributes"].duplicate(),"attributes":current["attributes"].duplicate(),
			"before_level":old["level_50"],"level":current["level_50"],"new_skill_ids":learned,"staged_total":current["staged_total"]})
	growth["students"]=changes
	return growth


static func _plan(school: Dictionary, rules: Dictionary, mixed := false) -> Dictionary:
	var rated := Groups.rate(school,Return.group_rules(school))
	if not rated["supported"]: return rated
	var plan := []
	var classes := []
	var available_courses := [1,2,3,4,5,6,7,10,11,12,17,18,23,27]
	if (school["month"]==6 and school["week"]==5) or school["month"] in [7,8] or (school.month==9 and school.week in [1,2]):
		available_courses.append_array([8,19,20,26,28,29])
	if (school.month==8 and school.week in [4,5]) or (school.month==9 and school.week in [1,2]):
		available_courses.append_array([30,33])
	if (school.month==9 and school.week in [1,2]):
		available_courses.append_array([24,36])
	if [school.month,school.week]==[9,2]:
		available_courses.append(25)
	for group in range(5):
		var rating: Dictionary = rated["ratings"][group]
		if rating["state"]==0:continue
		var students: Array = rated["after"]["derived_student_ids"][group].filter(func(id):return id>=0)
		if mixed and rating["state"]==2:
			classes.append({"students":students,"teacher":Groups._word(school["group_raw_bytes"],28*group),
				"work_fields":rating["work_fields"],"activity":2})
			continue
		if rating["state"]!=4: return Origin.failure("return_class_requires_assigned_course")
		var fields: Array = rating["work_fields"]
		if fields[0]<0 or fields[0]>2 or fields[2] not in available_courses:
			return Origin.failure("outside_return_course_subset")
		var selected := Teacher.select_group(Session._working(school),group,Return.group_rules(school),Return.work_rules(school,rules))
		if not selected["supported"]: return selected
		# New unlocks can move a saved course down its menu. 4C0400 uses the
		# assigned course ID at 7A52A4, independent of the prior display row.
		var rows: Array = selected["after"]["work_rows"][fields[0]]
		if not rows.any(func(row):return row[0]==fields[1] and row[1]==fields[2]):
			return Origin.failure("stale_return_course_assignment")
		classes.append({"students":students,"teacher":Groups._word(school["group_raw_bytes"],28*group),"work_fields":fields,"activity":1})
		for id in students: plan.append({"character_id":id,"training_id":fields[2],"coefficient":rating["relationship_mean"]})
	if plan.is_empty() and not mixed: return Origin.failure("no_return_course_students")
	return {"supported":true,"plan":plan,"classes":classes}


static func _grow(records: Array, plan: Array, rules: Dictionary, difficulty: int, seed: int) -> Dictionary:
	var after := records.duplicate(true)
	var state := seed
	var draws := []
	var packets := []
	var bonus := 0
	var skill_display := 0
	var cap := Growth._pool_cap(difficulty,rules)
	for command in plan:
		var record := Return._find(after,command["character_id"])
		var training: Dictionary = rules["training"][command["training_id"]]
		var packet := Growth._packet(record,training["package"],command["coefficient"],cap,rules)
		var event: Dictionary = command.duplicate()
		event["packet"]=packet.duplicate();packets.append(event);bonus+=packet[7]
		record["staged_total"]=0
		for k in range(7):
			record["growth_pools"][k]+=packet[k]
			record["staged_total"]+=packet[k]
		# Source4C0400 attempts the first status0 candidate in each skill category.
		# It checks pre-growth attributes; its job-sum loop does not reject learning.
		for category in range(11):
			for ordinal in range(rules["job_skill_caps"][record["job"]][category]):
				var sid: int = rules["skill_grid"][category][ordinal]
				if record["skill_statuses"][sid-1]!=0: continue
				var rate: int = training["learning_rates"][category]
				if rate!=100:
					state=(state*214013+2531011)&0xffffffff
					var draw := (state>>16)&32767
					draws.append(draw)
					if draw%101>rate: break
				var skill: Dictionary = rules["skills"][sid-1]
				var capable := true
				var total := 0
				for k in range(7):
					total+=record["attributes"][k]
					if record["attributes"][k]<skill["minimum_attributes"][k]: capable=false
				if total<skill["minimum_total"]: capable=false
				if capable:
					record["skill_statuses"][sid-1]=2;skill_display=1
				break
		for k in range(7): record["attributes"][k]=Growth._attribute(record["growth_pools"][k],rules["attribute_increments"])
		record["level_50"]=Growth._level(Growth._total(record,rules),rules["level_thresholds"])
	return {"records":after,"packets":packets,"learning_draws":draws,"rand_state":state,"bonus":bonus,"skill_display_needed":skill_display}


static func _confirm(after: Dictionary, classes: Array, categories: Array, activity := 1) -> Dictionary:
	var assigned := []
	for item in classes: assigned.append_array(item["students"])
	var waiting: Array = after["school"]["student_ids"].slice(0,after["school"]["student_count"]).filter(func(id):return id not in assigned)
	var history_index: int = (after["school"]["month"]-4)*5+after["school"]["week"]-1
	for row in after["records"]:
		var growth := Return._find(after["growth"],row["character_id"])
		var job: int = growth["job"]
		var value: int = row["job_progress"][job]
		if value!=100: row["job_progress"][job]=clampi(((value+1+128)&255)-128,0,99)
		if waiting.has(row["character_id"]):row["week_records"][history_index*3]=3
		for item in classes:
			if row["character_id"] in item["students"]:
				row["week_records"][history_index*3]=item.get("activity",activity)
				row["week_records"][history_index*3+1]=item["work_fields"][0]&255
				row["week_records"][history_index*3+2]=item["work_fields"][1]&255
		for k in range(5):
			var total := 0
			for offset in [0,1,10,11,20,21]: total+=row["job_progress"][1+2*k+offset]
			growth["job_sums"][k]=total
	var calls := []
	for a in waiting:
		for b in waiting:
			if a==b: continue
			var left := Return._find(after["growth"],a)
			var right := Return._find(after["growth"],b)
			if categories[left["job"]]==categories[right["job"]]: calls.append({"from":a,"to":b,"delta":1})
			if left["level_50"]==right["level_50"]: calls.append({"from":a,"to":b,"delta":1})
	for a in waiting:
		for b in waiting:
			if a!=b: calls.append({"from":a,"to":b,"delta":2})
	for a in waiting:
		for b in assigned: calls.append({"from":a,"to":b,"delta":-1})
	for item in classes:
		for a in item["students"]:
			for b in item["students"]:
				if a!=b: calls.append({"from":a,"to":b,"delta":1})
		for a in item["students"]:
			calls.append({"from":a,"to":item["teacher"],"delta":1})
			calls.append({"from":item["teacher"],"to":a,"delta":1})
	_apply_relationships(after, calls)
	return {"relationship_calls":calls}


static func _apply_relationships(after: Dictionary, calls: Array) -> void:
	for call in calls:
		for row in after["school"]["relationships"]:
			if row["from"]==call["from"] and row["to"]==call["to"]:
				row["value"]=clampi(row["value"]+call["delta"],1,100)


static func _guard(before: Dictionary, rules: Dictionary, allow_completed := false) -> String:
	if rules.is_empty(): return "invalid_return_course_sources"
	var reason := Return.validate_planning_roster(before,rules)
	if not reason.is_empty(): return reason
	if before.get("phase")!="school_returned" and not (allow_completed and before.get("phase")=="courses_confirmed"):
		return "return_course_requires_current_school"
	var cap := Growth._pool_cap(before["school"]["difficulty"],rules["growth"])
	for row in before["growth"]:
		for k in range(7):
			if row["growth_pools"][k]>cap or Growth._attribute(row["growth_pools"][k],rules["growth"]["attribute_increments"])!=row["attributes"][k]:
				return "inconsistent_return_course_growth"
	return ""


static func _rules() -> Dictionary:
	var rules := Return._rules()
	if rules.is_empty(): return {}
	for key in SOURCES:
		var text := FileAccess.get_file_as_string(SOURCES[key][0]).replace("\r\n","\n")
		if text.sha256_text()!=SOURCES[key][1]: return {}
		var data: Variant = JSON.parse_string(text)
		if not data is Dictionary: return {}
		rules[key]=Roles._integers(data)
	if not Growth.valid_rules(Growth.source_subset(rules["growth"])) or not Confirmation.valid_rules(Confirmation.source_subset(rules["confirmation"])): return {}
	return rules
