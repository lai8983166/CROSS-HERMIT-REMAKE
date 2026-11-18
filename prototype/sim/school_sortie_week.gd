extends RefCounted
## May week 1 or 2 course or sortie result, CH003, state 7, CH001, workroom and school boot.
const Return := preload("res://sim/school_postbattle_return.gd")
const Week := preload("res://sim/week_settlement_replay.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const Courses := preload("res://sim/school_course_unlocking.gd")
const Adventures := preload("res://sim/school_return_adventures.gd")
const PATH := "res://data/school_sortie_week_story.json"
const SHA := "eb886bac32bb4b98652b37490277c56144a6dbda105730ac59beb5dbb1328175"
const WEEK3_PATH := "res://data/school_may_week3_story.json"
const WEEK3_SHA := "0326170c7084c81f0b16ecf44510ff0beec29f50939d05ff147f04c29a1869c9"


static func story(start_week: int = 1) -> Dictionary:
	if start_week not in [1,2]:
		return {"supported":false,"reason":"outside_sortie_story_week"}
	var raw := FileAccess.get_file_as_string(PATH if start_week==1 else WEEK3_PATH).replace("\r\n","\n")
	if raw.sha256_text()!=(SHA if start_week==1 else WEEK3_SHA):
		return {"supported":false,"reason":"sortie_week_story_changed"}
	var data: Dictionary = Roles._integers(JSON.parse_string(raw))
	var week_start: Array = data["scenes"][1]["pages"]
	if start_week==2: week_start.append_array(data["scenes"][2]["pages"])
	return {"supported":true,"pre_week":data["scenes"][0]["pages"],
		"week_start":week_start,"school_entry":[]}


static func next_week(before: Dictionary) -> Dictionary:
	var rules := Return._rules()
	var course: bool = before.get("phase")=="courses_confirmed"
	var reason := _guard(before,1,"courses_confirmed" if course else "sortie_settled",rules)
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
	after["adv_background"] = 8
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
	if week==3:
		# Accept only a carried 5/2 ledger reachable from one of the three 5/1 submissions.
		var reachable := false
		for first_selection in [0,8,17]:
			var candidate := Adventures.advance(initial,first_selection)
			Adventures._open(candidate,5,2,source)
			if candidate==departure_ledger:
				reachable = true
				break
		if not reachable: return {"supported":false,"reason":"invalid_departure_ledger"}
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
	after["school"]["adventure_gate"] = 0
	# 4A5CE0 preserves the previous selection only while it remains available.
	if after["school"]["lecture_active"]==1:
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
	after["flags"]["0x7a55fa"] = 0
	after["flags"]["0x7a4e62"] = 1
	# CH002(5/2) jumps to END. At 5/3 its op151 sets the music fields again.
	if week==3:
		after["flags"]["0x7a55f6"] = 11
		after["flags"]["0x7e11a0"] = 1
	after["newly_dated_adventures"] = []
	return Return._result(after,"school_returned",{"ledger_after":opened,"unlocked_work_ids":unlocked["unlocked_work_ids"]})


static func _guard(before: Dictionary, first_week: int, phase: String, rules: Dictionary) -> String:
	if rules.is_empty(): return "invalid_sortie_week_sources"
	if before.get("phase")!=phase: return "unexpected_sortie_week_phase"
	var school: Variant = before.get("school")
	if not school is Dictionary or school.get("week") not in [first_week,first_week+1]:
		return "outside_sortie_week"
	return Return._validate(before,[3,4,9,5],5,school["week"],rules)
