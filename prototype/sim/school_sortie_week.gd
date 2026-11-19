extends RefCounted
## May weeks 1–4 course or sortie result, CH003, state 7, CH001, workroom and school boot.
const Return := preload("res://sim/school_postbattle_return.gd")
const Week := preload("res://sim/week_settlement_replay.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const Courses := preload("res://sim/school_course_unlocking.gd")
const Adventures := preload("res://sim/school_return_adventures.gd")
const PATH := "res://data/school_sortie_week_story.json"
const SHA := "eb886bac32bb4b98652b37490277c56144a6dbda105730ac59beb5dbb1328175"
const WEEK3_PATH := "res://data/school_may_week3_story.json"
const WEEK3_SHA := "0326170c7084c81f0b16ecf44510ff0beec29f50939d05ff147f04c29a1869c9"


const WEEK4_PATH := "res://data/school_may_week4_story.json"
const WEEK4_SHA := "9000c19fd20f9d7433e93e5cf9480d429bf6a15ae9e60bf10a4e26421c3fc80a"


static func story(start_week: int = 1) -> Dictionary:
	if start_week not in [1,2,3,4]:
		return {"supported":false,"reason":"outside_sortie_story_week"}
	var raw := FileAccess.get_file_as_string([PATH,WEEK3_PATH,WEEK4_PATH,Return.WEEK_FIVE[0]][start_week-1]).replace("\r\n","\n")
	if raw.sha256_text()!=[SHA,WEEK3_SHA,WEEK4_SHA,Return.WEEK_FIVE[1]][start_week-1]:
		return {"supported":false,"reason":"sortie_week_story_changed"}
	var data: Dictionary = Roles._integers(JSON.parse_string(raw))
	var week_start: Array = data["scenes"][1]["pages"]
	if start_week==2: week_start.append_array(data["scenes"][2]["pages"])
	return {"supported":true,"pre_week":data["scenes"][0]["pages"],
		"week_start":week_start,"school_entry":data["scenes"][2]["pages"] if start_week==3 else []}


static func begin_story(before: Dictionary) -> Dictionary:
	var rules := Return._rules()
	if rules.is_empty(): return {"supported":false,"reason":"invalid_sortie_week_sources"}
	return Return.join_chapter030b(before,rules)


static func next_week(before: Dictionary) -> Dictionary:
	var rules := Return._rules()
	var course: bool = before.get("phase")=="courses_confirmed"
	var phase := "courses_confirmed" if course else "sortie_settled"
	if before.get("school") is Dictionary and before["school"].get("week")==4: phase="chapter030b_joined"
	var reason := _guard(before,1,phase,rules)
	if not reason.is_empty(): return {"supported":false,"reason":reason}
	var result := Week.project(Return._week_input(before),rules["week"])
	if not result["supported"]: return result
	var after := before.duplicate(true)
	var advanced: Dictionary = result["after"]
	after["school"]["month"] = advanced["month"]
	after["school"]["week"] = advanced["week"]
	for key in ["participants","flags","item_flags"]: after[key] = advanced[key]
	for row in after["growth"]:
		var participant := Return._find(after["participants"],row["character_id"])
		for key in Return.GROWTH_KEYS:
			row[key] = participant[key].duplicate(true) if participant[key] is Array else participant[key]
	after["phase"] = "course_week_advanced" if course else "sortie_week_advanced"
	if advanced["week"]==4:
		var joined := Return.join_week_four(after,rules)
		if not joined["supported"]: return joined
		after=joined["after"]
	return Return._result(after,after["phase"],{"date":[advanced["month"],advanced["week"]],"week_executed":true})


static func finish_story(before: Dictionary) -> Dictionary:
	var course: bool = before.get("phase")=="course_week_advanced"
	var reason := _guard(before,2,"course_week_advanced" if course else "sortie_week_advanced",Return._rules())
	if not reason.is_empty(): return {"supported":false,"reason":reason}
	var after := before.duplicate(true)
	var week: int = after["school"]["week"]
	# Chapter024 and Chapter027 both restore background 8 before entering task8.
	after["flags"]["0x7a55f6"] = 16 if week==2 else 11
	after["flags"]["0x7e11a0"] = 1 if week==2 else 0
	after["adv_background"] = 6 if week>=4 else 8
	after["phase"] = "course_workroom" if course else "sortie_workroom"
	return Return._result(after,after["phase"])


static func school_return(before: Dictionary, ledger: Dictionary, departure_ledger: Dictionary = {}) -> Dictionary:
	var rules := Return._rules()
	var course: bool = before.get("phase")=="course_workroom"
	var reason := _guard(before,2,"course_workroom" if course else "sortie_workroom",rules)
	if not reason.is_empty(): return {"supported":false,"reason":reason}
	var id: int = before["school"]["lecture_work_fields"][2]
	var week: int = before["school"]["week"]
	var source := Adventures.rules()
	var initial := Adventures.initial()
	if initial.is_empty() or source.is_empty():
		return {"supported":false,"reason":"invalid_sortie_week_sources"}
	var departure := initial
	if week>=3:
		if not Adventures.valid_opening(departure_ledger,week-1): return {"supported":false,"reason":"invalid_departure_ledger"}
		departure = departure_ledger
	if not course and not Adventures.available(departure).any(func(row):return row["id"]==id):
		return {"supported":false,"reason":"unavailable_departure_adventure"}
	if ledger!=Adventures.advance(departure,0 if course else id):
		return {"supported":false,"reason":"invalid_sortie_week_ledger"}
	var opened := ledger.duplicate(true)
	Adventures._open(opened,5,week,source)
	var unlocked := Courses.unlock_courses(before["school"],rules["school"]["course_rules"])
	if not unlocked["supported"]: return unlocked
	var after := before.duplicate(true)
	after["phase"] = "school_returned"
	after["school"] = unlocked["after"]
	after["school"]["adventure_gate"] = int(week==4)
	# 4A5CE0 preserves the previous selection only while it remains available.
	if week==4:
		var mandatory := Adventures.select(after,opened,7)
		if not mandatory["supported"]: return mandatory
		after["school"]=mandatory["after"]["school"]
		for group in range(5):
			if Return.Groups._word(after["school"]["group_raw_bytes"],group*28)>=0:
				after["school"]["group_raw_bytes"][group*28+3]=0
	elif after["school"]["lecture_active"]==1:
		if Adventures.available(opened).any(func(row):return row["id"]==id):
			var selected := Adventures.select(after,opened,id)
			if not selected["supported"]: return selected
			after["school"] = selected["after"]["school"]
		else:
			after["school"]["lecture_active"] = 0
	var prepared := Return._prepare(after["school"],rules)
	if not prepared["supported"]: return prepared
	after["school"] = prepared["after"]
	after["ratings"] = prepared["ratings"]
	after["rankings"] = Return._rankings(after["school"])
	after["flags"]["0x7a55fa"] = int(week==4)
	after["flags"]["0x7a4e62"] = 1
	# CH002(5/2) jumps to END. At 5/3 its op151 sets the music fields again.
	if week>=3:
		after["flags"]["0x7a55f6"] = 11
		after["flags"]["0x7e11a0"] = 1
	after["newly_dated_adventures"] = []
	if week==4:
		for rule in rules["boot"]["adventures"]:
			if rule["present"] and rule["gate"] and rule["kind"] and rule["month"]==5 and rule["week"]==week:
				after["newly_dated_adventures"].append(rule.duplicate(true))
	return Return._result(after,"school_returned",{"ledger_after":opened,"unlocked_work_ids":unlocked["unlocked_work_ids"]})


static func _guard(before: Dictionary, first_week: int, phase: String, rules: Dictionary) -> String:
	if rules.is_empty(): return "invalid_sortie_week_sources"
	if before.get("phase")!=phase: return "unexpected_sortie_week_phase"
	var school: Variant = before.get("school")
	if not school is Dictionary or school.get("week") not in range(first_week,first_week+4):
		return "outside_sortie_week"
	if phase=="chapter030b_joined":
		return Return._validate(before,[3,4,9,5,8,6],5,4,rules)
	return Return.validate_planning_roster(before,rules)
