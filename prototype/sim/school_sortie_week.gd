extends RefCounted
## May and June work results through September week 1, CH003, state 7, CH001, workroom and school boot.
const YearLoop := preload("res://sim/school_year_loop.gd")
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


const JUNE_SHA := Return.JUNE_ONE[1]
const JUNE_TWO_SHA := Return.JUNE_TWO[1]
const JUNE_THREE_SHA := "9b9b721baa9ed42beb921da28a7a78b38ac211a60dbad569a80c237b1fe28588"
const JUNE_FOUR_SHA := "4e919ba9c4f5438502ef8c37ade19eb71234eddf09d15f9916f4e0c123e63df9"
const JUNE_FIVE_SHA := Return.JUNE_FIVE[1]
const JULY_ONE_SHA := "f9306a20c7ce69d07bfbb8b5522cf91a97dd3a2e278e6082ab4adcdf19232434"
const JULY_TWO_SHA := "1e5b476300d000b8f5c1863f21f6085e1e97e77851b4dc230d3f72411dc5a4cd"
const JULY_THREE_SHA := "b814ce752fb1f8eed446e8715cafcf34baa26ade393fc1d2d055be1b965ac48c"
const JULY_FOUR_SHA := "51be1f6e71eb47b99bed1e2f27cacd7e97ad562d7639456757489acb0de887b8"
const JULY_FIVE_SHA := Return.JULY_FIVE[1]
const AUGUST_ONE_SHA := "4cbdcbbef3484723d4fb0ada0795d743f37a569cb288295905244b2ce27695bd"
const AUGUST_TWO_SHA := "123be3bb046d9728c94c3de377d44b3c960ecc3aebdd143988b21e4b1967d1c6"
const AUGUST_THREE_SHA := "e84464a033a1b6034cdda0179dca8665cde480f7a683f3c28faf983b35c7af34"
const AUGUST_FIVE_SHA := "5de7224184119f6e4732cfebebfb93cea933f768f50b958a25802f92342105c7"
const SEPTEMBER_ONE_SHA := "7d4d9bd3ce4ebe5adf871b67b0a705474685b07eba4c05b0e0eddc176b47b86a"
const SEPTEMBER_TWO_SHA := "58fbd576337b91cd5b76d07dad0d1e60daf22948a26a3e83425b3754607b0f3a"
const SEPTEMBER_THREE_SHA := "8c177184de59357ea446aa09603029955f70fbba49c53037a9e28f1807026395"
const SEPTEMBER_FOUR_SHA := "505a554441ed424bd78e4423cc4edf9fdc476ac4fd82742ffe0a9fab61d22de1"
const OCTOBER_TWO := ["res://data/school_october_week2_story.json", "c3edaaa885c530c63a81c1f9d6175ac258af0028176d17de88585baa8824bfbc"]
const SEPTEMBER_STORIES := [["res://data/school_september_week2_story.json", SEPTEMBER_TWO_SHA],
	["res://data/school_september_week3_story.json", SEPTEMBER_THREE_SHA],
	["res://data/school_september_week4_story.json", SEPTEMBER_FOUR_SHA],Return.SEPTEMBER_FIVE,
	Return.OCTOBER_ONE]
const AUGUST_STORIES := [["res://data/school_august_week2_story.json",AUGUST_TWO_SHA],
	["res://data/school_august_week3_story.json",AUGUST_THREE_SHA],Return.AUGUST_FOUR,
	["res://data/school_august_week5_story.json",AUGUST_FIVE_SHA],
	["res://data/school_september_week1_story.json",SEPTEMBER_ONE_SHA]]
const JULY_STORIES := [["res://data/school_july_week2_story.json",JULY_TWO_SHA],
	["res://data/school_july_week3_story.json",JULY_THREE_SHA],["res://data/school_july_week4_story.json",JULY_FOUR_SHA],Return.JULY_FIVE,
	["res://data/school_august_week1_story.json",AUGUST_ONE_SHA]]
const JUNE_STORIES := [Return.JUNE_TWO,["res://data/school_june_week3_story.json",JUNE_THREE_SHA],
	["res://data/school_june_week4_story.json",JUNE_FOUR_SHA],Return.JUNE_FIVE,
	["res://data/school_july_week1_story.json",JULY_ONE_SHA]]
const STORIES := [[PATH,SHA],[WEEK3_PATH,WEEK3_SHA],[WEEK4_PATH,WEEK4_SHA],Return.WEEK_FIVE,Return.JUNE_ONE]


static func story(start_week: int = 1, month: int = 5) -> Dictionary:
	if [month,start_week]==[11,3]:
		var data := _november_four()
		if data.is_empty() or FileAccess.get_sha256(data.date_card.image)!=data.date_card.png_sha256:
			return {"supported":false,"reason":"invalid_november_four_story"}
		var scenes: Array=data.scenes
		return {"supported":true,"pre_week":scenes[0].pages+scenes[1].pages,
			"pre_week_join_page":scenes[0].pages.size(),"date_card":data.date_card,
			"week_start":scenes[2].pages,"school_entry":scenes[3].pages}
	if YearLoop.has_departure(month,start_week):return YearLoop.story(month,start_week)
	var dated: Array = {5:STORIES,6:JUNE_STORIES,7:JULY_STORIES,8:AUGUST_STORIES,9:SEPTEMBER_STORIES,10:[OCTOBER_TWO]}.get(month,[])
	if start_week<1 or start_week>dated.size():
		return {"supported":false,"reason":"outside_sortie_story_week"}
	var resource: Array = dated[start_week-1]
	var june := month==6
	var raw := FileAccess.get_file_as_string(resource[0]).replace("\r\n","\n")
	if raw.sha256_text()!=resource[1]:
		return {"supported":false,"reason":"sortie_week_story_changed"}
	var data: Dictionary = Roles._integers(JSON.parse_string(raw))
	var scenes: Array = data["scenes"]
	if month in [7,8,9,10]:
		var result := {"supported":true,"pre_week":[],"week_start":[] if scenes.is_empty() else scenes[0]["pages"],"school_entry":[]}
		if month == 9 and start_week == 5:
			result["pre_week"] = scenes[0]["pages"]
			result["week_start"] = scenes[1]["pages"] + scenes[2]["pages"]
		if month==10 or (month==9 and start_week==1):
			result["pre_week"] = scenes[0]["pages"]
			result["week_start"] = scenes[1]["pages"]
		if month==9 and start_week==3:
			result["pre_week"] = scenes[0]["pages"] + scenes[1]["pages"]
			result["week_start"] = scenes[2]["pages"]
		if month==9 and start_week==4:
			result["pre_week"]=scenes[0]["pages"]
			result["week_start"]=scenes[1]["pages"]+scenes[2]["pages"]
			result["school_entry"]=scenes[3]["pages"]
		if month==7 and start_week==4:
			result["pre_week"]=scenes[0]["pages"]
			result["week_start"]=scenes[1]["pages"]
		if month==8 and start_week==3:
			result["pre_week"]=scenes[0]["pages"]+scenes[1]["pages"]
			result["week_start"]=[]
			result["school_entry"]=scenes[2]["pages"]
		if month==8 and start_week==4:
			result["pre_week"]=scenes[0]["pages"]
			result["week_start"]=scenes[1]["pages"]+scenes[2]["pages"]
		if data.has("date_card"):
			var card: Dictionary=data["date_card"]
			if not FileAccess.file_exists(card["image"]) or FileAccess.get_sha256(card["image"])!=card["png_sha256"]:
				return {"supported":false,"reason":"invalid_july_date_card"}
			result["date_card"]=card
		return result
	if june and start_week in [3,4,5]:
		var pages: Array=scenes[0]["pages"].duplicate()
		if start_week>=4:pages.append_array(scenes[1]["pages"])
		return {"supported":true,"pre_week":[],"week_start":pages,"school_entry":[]}
	if june:
		var post: Array = scenes[0]["pages"] + scenes[1]["pages"]
		var result := {"supported":true,"pre_week":post,
			"week_start":scenes[2]["pages"] + scenes[3]["pages"],"school_entry":[]}
		if start_week==1:
			result["pre_week_join_page"]=scenes[0]["pages"].size()
			result["school_entry"]=scenes[4]["pages"]
		return result
	var week_start: Array = scenes[1]["pages"]
	if start_week==2: week_start.append_array(data["scenes"][2]["pages"])
	return {"supported":true,"pre_week":data["scenes"][0]["pages"],
		"week_start":week_start,"school_entry":data["scenes"][2]["pages"] if start_week==3 else []}


static func join_october_student(before: Dictionary, chapter: int) -> Dictionary:
	var pre_week := chapter == 313
	var expected_date := [9,5] if pre_week else [10,1]
	var expected_count := 14 if pre_week else 15
	if chapter not in [313,233] or [before.school.month,before.school.week] != expected_date or before.school.student_count != expected_count:
		return {"supported":false,"reason":"outside_october_join"}
	var reason := Return.validate_planning_roster(before, Return._rules())
	if not reason.is_empty():return {"supported":false,"reason":reason}
	var raw := FileAccess.get_file_as_string(Return.OCTOBER_ONE[0]).replace("
","
")
	if raw.sha256_text() != Return.OCTOBER_ONE[1]:return {"supported":false,"reason":"invalid_join_source"}
	var data: Dictionary = Roles._integers(JSON.parse_string(raw))
	var source: Dictionary = data.joins[0 if pre_week else 1]
	var after := before.duplicate(true)
	Return._append_student(after,source,Return._rules())
	after.school.relationships.append_array(source.join_relationships.duplicate(true))
	return Return._result(after,after.phase)


static func _november_four() -> Dictionary:
	var raw := FileAccess.get_file_as_string(Return.NOVEMBER_FOUR[0]).replace("\r\n","\n")
	if raw.sha256_text()!=Return.NOVEMBER_FOUR[1]:return {}
	return Roles._integers(JSON.parse_string(raw))


static func join_november(before: Dictionary, chapter: int) -> Dictionary:
	var rules := Return._rules()
	var reason := Return.validate_planning_roster(before,rules)
	if not reason.is_empty():return {"supported":false,"reason":reason}
	if [before.school.month,before.school.week]!=[11,3] or before.school.lecture_work_fields!=[3,26,41,0] or before.school.adventure_gate!=1 or before.school.lecture_active!=1:
		return {"supported":false,"reason":"outside_adventure41_join"}
	var after := before.duplicate(true)
	if chapter==72 and before.phase=="sortie_settled" and before.has("chapter071_absent"):
		var absent: Dictionary=after.chapter071_absent
		var source := {"candidate":absent.participants,"history":absent.records,"template_sha256":absent.profile.template_sha256}
		Return._append_student(after,source,rules)
		after.counts[-1]=absent.counts
		after.school.relationships.append_array(absent.relationships)
		after.erase("chapter071_absent")
		after.phase="chapter072_joined"
	elif chapter==74 and before.phase=="chapter072_joined":
		var data := _november_four()
		if data.is_empty():return {"supported":false,"reason":"invalid_november_four_story"}
		var source: Dictionary=data.joins[0]
		Return._append_student(after,source,rules)
		after.school.relationships.append_array(source.join_relationships)
		after.phase="chapter074_joined"
	else:return {"supported":false,"reason":"outside_adventure41_join"}
	return Return._result(after,after.phase)


static func begin_story(before: Dictionary) -> Dictionary:
	var rules := Return._rules()
	if rules.is_empty(): return {"supported":false,"reason":"invalid_sortie_week_sources"}
	if before.get("school") is Dictionary and before.school.month==9:
		return Return.join_september_students(before,false)
	if before.get("school") is Dictionary and before["school"].get("month")==7:
		return Return.join_chapter304(before,rules)
	if before.get("school") is Dictionary and before["school"].get("month")==6:
		return Return.join_chapter036(before,rules)
	return Return.join_chapter030b(before,rules)


static func next_week(before: Dictionary) -> Dictionary:
	var rules := Return._rules()
	var course: bool = before.get("phase")=="courses_confirmed"
	var phase := "courses_confirmed" if course else "sortie_settled"
	if before.get("school") is Dictionary:
		if [before.school.month,before.school.week]==[11,3]:phase="chapter074_joined"
		elif [before.school.month,before.school.week]==[9,4]:phase="chapter054_joined"
		elif before["school"].get("month")==7 and before["school"].get("week")==4:phase="chapter304_joined"
		elif before["school"].get("month")==6 and before["school"].get("week")!=5:
			phase="chapter036_joined" if before["school"].get("week")==1 else "sortie_settled"
		elif before["school"].get("month")==5 and before["school"].get("week")==4: phase="chapter030b_joined"
	var reason := _guard(before,1,phase,rules)
	if not reason.is_empty(): return {"supported":false,"reason":reason}
	if before["school"]["month"]==6 and before["school"]["week"]==4:
		var joined := Return.join_ch003_teacher(before)
		if not joined["supported"]:return joined
		before=joined["after"]
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
	if advanced["month"]==5 and advanced["week"]==4:
		var joined := Return.join_week_four(after,rules)
		if not joined["supported"]: return joined
		after=joined["after"]
	if advanced["month"]==6 and advanced["week"]==1:
		var joined := Return.join_chapter033(after,rules)
		if not joined["supported"]: return joined
		after=joined["after"]
	if [advanced.month,advanced.week]==[11,4]:
		var data := _november_four()
		if data.is_empty():return {"supported":false,"reason":"invalid_november_four_story"}
		var source: Dictionary=data.joins[1]
		Return._append_teacher(after.school,source.join_profiles[1])
		Return._append_student(after,source,rules)
		after.school.relationships.append_array(source.join_relationships)
	if [advanced.month,advanced.week]==[11,3]:
		var removed := _leave_chapter071(after,rules)
		if not removed.supported:return removed
	return Return._result(after,after["phase"],{"date":[advanced["month"],advanced["week"]],"week_executed":true})


## The opening opcode precedes even the date card. Keep the absent student's
## backing records for the later chapter, outside the active school arrays.
static func _leave_chapter071(after: Dictionary, rules: Dictionary) -> Dictionary:
	var school: Dictionary=after.school
	var index: int=school.student_ids.slice(0,school.student_count).find(2)
	if index<0 or after.has("chapter071_absent"):
		return {"supported":false,"reason":"unexpected_chapter071_roster"}
	var absent := {}
	for key in ["participants","growth","records","counts"]:
		absent[key]=after[key].pop_at(index)
	absent.profile=school.member_profiles.pop_at(index+1)
	absent.relationships=school.relationships.filter(func(r):return r.from==2 or r.to==2)
	school.relationships=school.relationships.filter(func(r):return r.from!=2 and r.to!=2)
	after.chapter071_absent=absent
	for item in absent.participants.equipped_items:
		if item>0 and (after.item_flags[item-1]&1)!=0:
			after.item_flags[item-1]=(after.item_flags[item-1]&0xf0ff)|0x100
	for i in range(index,school.student_count-1):
		school.raw_student_ids[i]=school.raw_student_ids[i+1]
	school.student_count-=1
	school.student_ids.remove_at(index)
	school.student_ids.append(-1)
	school.availability[2]=0
	for group in range(5):
		for slot in range(4):
			var at := group*28+16+2*slot
			if Return.Groups._word(school.group_raw_bytes,at)==2:
				Return.Groups._put_word(school.group_raw_bytes,at,-1)
	var prepared := Return._prepare(school,rules)
	if not prepared.supported:return prepared
	after.school=prepared.after
	after.ratings=prepared.ratings
	after.rankings=Return._rankings(after.school)
	return {"supported":true}


static func finish_story(before: Dictionary) -> Dictionary:
	var course: bool = before.get("phase")=="course_week_advanced"
	var reason := _guard(before,2,"course_week_advanced" if course else "sortie_week_advanced",Return._rules())
	if not reason.is_empty(): return {"supported":false,"reason":reason}
	var after := before.duplicate(true)
	var week: int = after["school"]["week"]
	# These op151 and op91 values end the dated CH001 chapter.
	var june: bool = after["school"]["month"]==6
	after["flags"]["0x7a55f6"] = [8,6,16,9,2][week-1] if june else (16 if week==2 else 11)
	after["flags"]["0x7e11a0"] = int(june or week==2)
	after["adv_background"] = [6,7,6,8,8][week-1] if june else (6 if week>=4 else 8)
	if after["school"]["month"]==7:
		after["flags"]["0x7a55f6"]=[12,3,17,10,9][week-1]
		after["flags"]["0x7e11a0"]=0 if week==2 else 1
		after["adv_background"]=2 if week==2 else 122 if week==5 else 8
	if after["school"]["month"]==8:
		after["flags"]["0x7a55f6"]=[9,5,12,4,3][week-1]
		after["flags"]["0x7e11a0"]=0 if week in [1,4] else 1
		after["adv_background"]=14 if week in [4,5] else 122
	if [after.school.month,week]==[9,1]:
		after.flags["0x7a55f6"]=11
		after.flags["0x7e11a0"]=0
		after.adv_background=14
	if [after.school.month,week]==[9,2]:
		after.flags["0x7a55f6"]=1
		after.flags["0x7e11a0"]=1
		after.adv_background=13
	if [after.school.month,week]==[9,3]:
		after.flags["0x7a55f6"]=12
		after.flags["0x7e11a0"]=1
		after.adv_background=10
	if [after.school.month,week]==[9,4]:
		after.flags["0x7a55f6"]=9
		after.flags["0x7e11a0"]=1
		after.adv_background=10
	if after.school.month==10 and week==2:
		after.flags["0x7a55f6"]=3
		after.flags["0x7e11a0"]=1
		after.adv_background=14
	if [after.school.month,week]==[10,1]:
		after.flags["0x7a55f6"]=11
		after.flags["0x7e11a0"]=0
		after.adv_background=14
	if [after.school.month,week]==[9,5]:
		after.flags["0x7a55f6"]=9
		after.flags["0x7e11a0"]=1
		after.adv_background=14
	if [after.school.month,week]==[11,4]:
		after.flags["0x7a55f6"]=5
		after.flags["0x7e11a0"]=1
		after.adv_background=122
	if YearLoop.has_arrival(after.school.month,week) and not YearLoop.apply_arrival_effects(after,false):
		return {"supported":false,"reason":"invalid_school_year_week_start"}
	after["phase"] = "course_workroom" if course else "sortie_workroom"
	return Return._result(after,after["phase"])


static func begin_school_entry(before: Dictionary) -> Dictionary:
	if [before.school.month,before.school.week]==[9,5]:return Return.join_september_students(before,true)
	return Return.join_chapter306(before,Return._rules())


static func school_return(before: Dictionary, ledger: Dictionary, departure_ledger: Dictionary = {}) -> Dictionary:
	var rules := Return._rules()
	var course: bool = before.get("phase")=="course_workroom"
	var expected_phase := "course_workroom" if course else "sortie_workroom"
	var school: Variant=before.get("school")
	if school is Dictionary and school.get("month")==8 and school.get("week")==4:
		expected_phase="chapter306_joined"
	if school is Dictionary and [school.month,school.week]==[9,5]:expected_phase="chapter056_joined"
	var reason := _guard(before,2,expected_phase,rules)
	if not reason.is_empty(): return {"supported":false,"reason":reason}
	var id: int = before["school"]["lecture_work_fields"][2]
	var week: int = before["school"]["week"]
	var month: int = before["school"]["month"]
	var required_id := Adventures._mandatory_id(month,week)
	var source := Adventures.rules()
	var initial := Adventures.initial()
	if initial.is_empty() or source.is_empty():
		return {"supported":false,"reason":"invalid_sortie_week_sources"}
	var departure := initial
	if week>=3 or month>=6:
		var prior_week := 5 if week==1 else week-1
		var prior_month := month-1 if week==1 else month
		if not Adventures.valid_opening(departure_ledger,prior_week,prior_month): return {"supported":false,"reason":"invalid_departure_ledger"}
		departure = departure_ledger
	if not course and not Adventures.available(departure).any(func(row):return row["id"]==id):
		return {"supported":false,"reason":"unavailable_departure_adventure"}
	if ledger!=Adventures.advance(departure,0 if course else id):
		return {"supported":false,"reason":"invalid_sortie_week_ledger"}
	var opened := ledger.duplicate(true)
	Adventures._open(opened,month,week,source)
	var unlocked := Courses.unlock_courses(before["school"],rules["school"]["course_rules"])
	if not unlocked["supported"]: return unlocked
	var after := before.duplicate(true)
	after["phase"] = "school_returned"
	after["school"] = unlocked["after"]
	after["school"]["adventure_gate"] = int(required_id!=0)
	# 4A5CE0 preserves the previous selection only while it remains available.
	if required_id!=0:
		var mandatory := Adventures.select(after,opened,required_id)
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
	after["flags"]["0x7a55fa"] = int(required_id!=0)
	after["flags"]["0x7a4e62"] = 1
	# CH002(5/2) jumps to END. At 5/3 its op151 sets the music fields again.
	if month==5 and week>=3:
		after["flags"]["0x7a55f6"] = 11
		after["flags"]["0x7e11a0"] = 1
	if month==6 and week<=2:
		after["flags"]["0x7a55f6"] = 11
		after["flags"]["0x7e11a0"] = 0
	if (month==7 and week==2) or (month==8 and week==1):
		after["flags"]["0x7a55f6"]=3 if month==7 else 9
		after["flags"]["0x7e11a0"]=1
	if month==8 and week==4:
		after["flags"]["0x7a55f6"]=4
		after["flags"]["0x7e11a0"]=1
	if [month,week] in [[9,1],[10,1]]:
		after.flags["0x7a55f6"]=11
		after.flags["0x7e11a0"]=1
	if [month,week]==[9,5]:
		after.flags["0x7a55f6"]=11
		after.flags["0x7e11a0"]=0
	if [month,week]==[11,4]:
		after.flags["0x7a55f6"]=11
		after.flags["0x7e11a0"]=0
	if YearLoop.has_arrival(month,week) and not YearLoop.apply_arrival_effects(after,true):
		return {"supported":false,"reason":"invalid_school_year_school_entry"}
	after["newly_dated_adventures"] = []
	if required_id!=0 or month==7 or [month,week] in [[8,5],[9,5]]:
		for rule in rules["boot"]["adventures"]:
			if rule["present"] and rule["gate"] and rule["kind"] and rule["month"]==month and rule["week"]==week:
				after["newly_dated_adventures"].append(rule.duplicate(true))
	return Return._result(after,"school_returned",{"ledger_after":opened,"unlocked_work_ids":unlocked["unlocked_work_ids"]})


static func _guard(before: Dictionary, first_week: int, phase: String, rules: Dictionary) -> String:
	if rules.is_empty(): return "invalid_sortie_week_sources"
	if before.get("phase")!=phase: return "unexpected_sortie_week_phase"
	var school: Variant = before.get("school")
	if not school is Dictionary: return "outside_sortie_week"
	var may: bool = school.get("month")==5 and school.get("week") in range(first_week,6)
	var june: bool = school.get("month")==6 and school.get("week") in range(1,6)
	var july: bool = school.get("month")==7 and school.get("week") in range(1,6)
	if july and first_week==1 and school["week"]==4:
		if phase!="chapter304_joined" or school.get("adventure_gate")!=1 or school.get("lecture_active")!=1 or school.get("lecture_work_fields")!=[3,13,14,0]:return "outside_mandatory_sortie_return"
		return Return._validate(before,[3,4,9,5,8,6,1,2,16,17],7,4,rules)
	elif july and first_week==1 and school["week"]==3:
		if phase!="sortie_settled" or school.get("adventure_gate")!=1 or school.get("lecture_active")!=1 or school.get("lecture_work_fields")!=[3,8,9,0]:
			return "outside_mandatory_sortie_return"
	elif july and first_week==1:
		if school.get("adventure_gate")!=0:return "outside_july_work_return"
		if phase=="sortie_settled":
			var options: Array=[[1,0,17,0],[0,0,18,0]] if school["week"]==1 else [[1,0,17,0]]
			if school.get("lecture_active")!=1 or school.get("lecture_work_fields") not in options:return "outside_july_work_return"
	if june and school.get("week")==5 and first_week==1:
		if school.get("adventure_gate")!=0 or (phase=="sortie_settled" and school.get("lecture_work_fields")!=[1,0,17,0]):
			return "outside_june_five_return"
	elif june and school.get("week") in [2,3,4,5]:
		if phase=="sortie_settled":
			var week: int=school["week"]
			var required: Array = {2:[3,5,6,0],3:[3,9,10,0],4:[3,12,13,0]}[week]
			if school.get("lecture_work_fields")!=required: return "outside_mandatory_sortie_return"
			# CH003 at 6/3 invokes 4D4250(117); 4D46E0 returns zero for this roster.
			if week==3 and (not school.get("availability") is Array or school["availability"].size()<=117 or school["availability"][117]!=0):
				return "outside_ch003_teacher_removal"
		elif phase not in ["sortie_week_advanced","sortie_workroom"]:
			return "outside_sortie_week"
	var august: bool = school.get("month")==8 and school.get("week") in range(1,6)
	if august and first_week==1:
		if school["week"]==1 and (phase!="courses_confirmed" or school.get("adventure_gate")!=0):
			return "outside_august_course_return"
		if school.week==5:
			if phase!="sortie_settled" or school.adventure_gate!=0 or school.lecture_active!=1 or school.lecture_work_fields!=[0,1,35,0]:
				return "outside_august_five_sortie"
		if school.week==4:
			if school.adventure_gate!=0 or (phase=="sortie_settled" and (school.lecture_active!=1 or school.lecture_work_fields!=[1,0,17,0])):
				return "outside_august_four_work"
		if school["week"] in [2,3]:
			var id := 18+int(school["week"])
			if phase!="sortie_settled" or school.get("adventure_gate")!=1 or school.get("lecture_active")!=1 or school.get("lecture_work_fields")!=[3,id-1,id,0]:
				return "outside_mandatory_sortie_return"
	var september: bool = school.get("month")==9 and school.get("week") in [1,2,3,4,5]
	if september and first_week==1:
		if school.week==4:
			if phase!="chapter054_joined" or school.adventure_gate!=1 or school.lecture_active!=1 or school.lecture_work_fields!=[3,22,24,0]:return "outside_mandatory_sortie_return"
		elif school.week==3:
			if phase!="sortie_settled" or school.adventure_gate!=1 or school.lecture_active!=1 or school.lecture_work_fields!=[3,21,22,0]:
				return "outside_mandatory_sortie_return"
		elif school.week not in [1,2,5] or phase!="courses_confirmed" or school.get("adventure_gate")!=0:
			return "outside_september_course_return"
	if school.get("month")==10 and (school.week==1 and phase=="courses_confirmed" or first_week==2 and school.week in [1,2]):
		return Return.validate_planning_roster(before,rules)
	if first_week==1 and YearLoop.has_departure(school.month,school.week) and phase=="courses_confirmed" and school.adventure_gate==0:
		return Return.validate_planning_roster(before,rules)
	if first_week==2 and YearLoop.has_arrival(school.month,school.week):
		return Return.validate_planning_roster(before,rules)
	if [school.month,school.week]==[11,3] and first_week==1 and phase=="chapter074_joined" and school.student_count==17 and school.lecture_work_fields==[3,26,41,0]:
		return Return.validate_planning_roster(before,rules)
	if [school.month,school.week]==[11,4] and first_week==2 and school.student_count==18:
		return Return.validate_planning_roster(before,rules)
	if not may and not june and not july and not august and not september:
		return "outside_sortie_week"
	if phase=="chapter036_joined":
		return Return._validate(before,[3,4,9,5,8,6,1,2],6,1,rules)
	if phase=="chapter030b_joined":
		return Return._validate(before,[3,4,9,5,8,6],5,4,rules)
	return Return.validate_planning_roster(before,rules)
