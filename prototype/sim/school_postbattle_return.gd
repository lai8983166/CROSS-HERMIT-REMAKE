extends RefCounted
## Current first scene5 result -> Chapter020 join -> state7 week -> 5/1 data.
## Pure projections. The caller owns ADV completion, once-only commit and saves.
const Origin := preload("res://sim/new_game_school_origin.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const Week := preload("res://sim/week_settlement_replay.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")
const Courses := preload("res://sim/school_course_unlocking.gd")
const Growth := preload("res://sim/school_course_settlement.gd")
const Confirmation := preload("res://sim/school_course_confirmation.gd")
const Handoff := preload("res://sim/school_course_result_handoff.gd")
const Student := preload("res://sim/school_student_movement.gd")
const Teacher := preload("res://sim/school_teacher_movement.gd")
const Sort := preload("res://sim/school_waitlist_sort.gd")
const Session := preload("res://sim/new_game_school_session.gd")
const WEEK_FOUR := ["res://data/school_may_week4_story.json","9000c19fd20f9d7433e93e5cf9480d429bf6a15ae9e60bf10a4e26421c3fc80a"]
const WEEK_FIVE := ["res://data/school_may_week5_story.json","1d74ded43259f2145b716d742433c738b412f0b40279fe8387acf81ae2391542"]
const JUNE_ONE := ["res://data/school_june_week1_story.json","59bb89bf67f2ec0321ec07f46efc0a02ac8c9108db420429c119a47499a9dcca"]
const JUNE_FIVE := ["res://data/school_june_week5_story.json","1ff332986c340d8221e8dd0ae5d0bc1db7d216ebdc54dbcde883610fcdf4dedb"]
const JUNE_TWO := ["res://data/school_june_week2_story.json","6f4d9e85a6999e7f93bacb5c60b46a46052fecd3dd76601f9bf83beba83c061a"]
const JULY_FIVE := ["res://data/school_july_week5_story.json","659ec34f5bc053cb8feb10c7e3e6fbaa2d91bb2d4327e64482a35bf76f3aaa99"]
const AUGUST_FOUR := ["res://data/school_august_week4_story.json","ad68ccde061718a14e0c26ece14fb92af5a28738515b612984c2709b5703abff"]
const SOURCES := {
	"candidate":["res://data/school_postbattle_return_rules.json","1775635836be11e1c038437bb7043a2b2989bdccb880d8882fcda06d41fdb854"],
	"week":["res://data/week_settlement_evidence.json","5bdb406c2125c610c75942a9e589a9b427cdbcd5d97b0cbf35c014b1d793aedf"],
	"role":["res://data/role_application_evidence.json","b0c1f014711dabe3a70482967f58761d8915779da1bbcfcf2eadb18969d38055"],
	"school":["res://data/new_game_school_rules.json","ac4faffab74cb73b7f39c0c1a28a05a96f20f426aa1c5124eec58e1541bbef97"],
	"boot":["res://data/school_boot_evidence.json","066ac6af7eb1f8b4b5a8b7d363cff5fcb62760652065b06fc9cf77cb8546301e"]}
const GROWTH_KEYS := ["job","attributes","growth_pools","level_50","skill_statuses","job_sums","staged_total"]


static func group_rules(school: Dictionary) -> Dictionary:
	var rules := Origin.group_rules()
	if _has_chapter304(school):rules["chapter304_students"]=true
	if _has_chapter306(school):
		rules["chapter306_students"]=true
		rules["teacher_scope"]="chapter306"
		rules["chapter_sha256"]=Groups.CHAPTER306_SHA
	elif _has_four_teachers(school):
		rules["teacher_scope"]="ch003_week_four"
		rules["chapter_sha256"]=Groups.CH003_SHA
	elif _has_later_teachers(school) and school.get("teacher_count")==3:
		rules["teacher_scope"]="chapter030b"
		rules["chapter_sha256"]=Groups.CHAPTER030B_SHA
	elif school.get("month")==5 and school.get("week")==4:
		rules["teacher_scope"]="chapter029"
		rules["chapter_sha256"]=Groups.CHAPTER029_SHA
	return rules


static func _has_chapter306(school: Dictionary) -> bool:
	return school.get("month")==8 and school.get("week")==4 and school.get("student_count")==11 and school.get("teacher_count")==5


static func _has_chapter304(school: Dictionary) -> bool:
	return _has_chapter306(school) or ((school.get("month")==7 and school.get("week") in [4,5]) or (school.get("month")==8 and school.get("week") in [1,2,3,4])) and school.get("student_count")==10


static func sort_rules(school: Dictionary, rules: Dictionary) -> Dictionary:
	var result: Dictionary=rules["school"]["sort_rules"].duplicate()
	if _has_chapter304(school):result["chapter304_students"]=true
	if _has_chapter306(school):result["chapter306_students"]=true
	return result


static func _has_four_teachers(school: Dictionary) -> bool:
	return (school.get("month")==6 and school.get("week")==5) or (school.get("month")==7 and school.get("week") in [1,2,3,4,5]) or (school.get("month")==8 and school.get("week") in [1,2,3,4])


static func _has_later_teachers(school: Dictionary) -> bool:
	return (school.get("month")==5 and school.get("week") in [4,5]) or (school.get("month")==6 and school.get("week") in [1,2,3,4,5]) or _has_four_teachers(school)


static func work_rules(school: Dictionary, rules: Dictionary) -> Dictionary:
	var work: Dictionary = rules["school"]["work_rules"]
	if _has_later_teachers(school):
		work=work.duplicate(true)
		for teacher in school["member_profiles"]:
			if teacher["member_id"]<=101: continue
			work["teacher_profiles"].append({"teacher_id":teacher["member_id"],"job":teacher["job"],
				"level_50":teacher["level_50"],"attributes":teacher["attributes"]})
	return work


static func join(before: Dictionary) -> Dictionary:
	var rules := _rules()
	if rules.is_empty(): return Origin.failure("invalid_postbattle_source_rules")
	var reason := _validate(before, [3,4,9], 4,5,rules)
	if not reason.is_empty(): return Origin.failure(reason)
	if before.has("phase"): return Origin.failure("join_requires_confirmed_result")
	if not Confirmation.valid_records(before["records"]) or not Handoff.valid_counts(before["counts"]):
		return Origin.failure("invalid_postbattle_history")
	if not Growth._validate_records(before["school"],before["growth"],rules["role"]).is_empty():
		return Origin.failure("invalid_postbattle_growth")
	var after := before.duplicate(true)
	_sync_participants(after)
	_append_student(after,rules["candidate"],rules)
	after["school"]["relationships"].append_array(rules["candidate"]["relationships"].duplicate(true))
	after["phase"] = "chapter020_joined"
	return _result(after,"joined",{"join_source":"Chapter020.ybc:0x14/opcode144","joined_id":5})


static func join_week_four(before: Dictionary, rules: Dictionary) -> Dictionary:
	if before.get("phase") not in ["course_week_advanced","sortie_week_advanced"]:
		return Origin.failure("chapter029_requires_new_week")
	var reason := _validate(before,[3,4,9,5],5,4,rules)
	if not reason.is_empty(): return Origin.failure(reason)
	return _join_pair(before,rules,WEEK_FOUR,"chapter029_joined",110)


static func join_chapter033(before: Dictionary, rules: Dictionary) -> Dictionary:
	if before.get("phase") not in ["course_week_advanced","sortie_week_advanced"]:
		return Origin.failure("chapter033_requires_new_week")
	var reason := _validate(before,[3,4,9,5,8,6],6,1,rules)
	if not reason.is_empty(): return Origin.failure(reason)
	return _join_student(before,rules,JUNE_ONE,"chapter033_joined")


static func join_chapter036(before: Dictionary, rules: Dictionary) -> Dictionary:
	if before.get("phase")!="sortie_settled": return Origin.failure("chapter036_requires_settled_sortie")
	var reason := _validate(before,[3,4,9,5,8,6,1],6,1,rules)
	if not reason.is_empty(): return Origin.failure(reason)
	if before["school"]["lecture_work_fields"][2]!=4: return Origin.failure("chapter036_requires_adventure4")
	return _join_student(before,rules,JUNE_TWO,"chapter036_joined")


static func join_ch003_teacher(before: Dictionary) -> Dictionary:
	var encoded := FileAccess.get_file_as_string(JUNE_FIVE[0]).replace("\r\n","\n")
	if encoded.sha256_text()!=JUNE_FIVE[1]:return Origin.failure("invalid_join_source")
	var source: Dictionary=Roles._integers(JSON.parse_string(encoded))
	var after:=before.duplicate(true)
	var school: Dictionary=after["school"]
	if school["availability"][118]!=0:return Origin.failure("outside_ch003_teacher_join")
	_append_teacher(school,source["join_profiles"][0])
	school["relationships"].append_array(source["join_relationships"].duplicate(true))
	return _result(after,"ch003_teacher_joined",{"joined_ids":[118]})


static func _join_student(before: Dictionary, rules: Dictionary, resource: Array, status: String) -> Dictionary:
	var encoded := FileAccess.get_file_as_string(resource[0]).replace("\r\n","\n")
	if encoded.sha256_text()!=resource[1]: return Origin.failure("invalid_join_source")
	var source: Dictionary = Roles._integers(JSON.parse_string(encoded))
	var after := before.duplicate(true)
	_append_student(after,source,rules)
	after["school"]["relationships"].append_array(source["join_relationships"].duplicate(true))
	if status=="chapter036_joined": after["phase"]=status
	return _result(after,status,{"joined_ids":[source["candidate"]["character_id"]]})


static func join_chapter304(before: Dictionary, rules: Dictionary) -> Dictionary:
	if before.get("phase")!="sortie_settled":return Origin.failure("chapter304_requires_settled_sortie")
	var reason := _validate(before,[3,4,9,5,8,6,1,2],7,4,rules)
	if not reason.is_empty():return Origin.failure(reason)
	var school: Dictionary=before["school"]
	if school.get("adventure_gate")!=1 or school.get("lecture_active")!=1 or school.get("lecture_work_fields")!=[3,13,14,0]:
		return Origin.failure("chapter304_requires_adventure14")
	var raw:=FileAccess.get_file_as_string(JULY_FIVE[0]).replace("\r\n","\n")
	if raw.sha256_text()!=JULY_FIVE[1]:return Origin.failure("invalid_join_source")
	var data: Dictionary=Roles._integers(JSON.parse_string(raw))
	var after:=before.duplicate(true)
	for source in data["joins"]:
		_append_student(after,source,rules)
		after["school"]["relationships"].append_array(source["join_relationships"].duplicate(true))
	after["phase"]="chapter304_joined"
	return _result(after,"chapter304_joined",{"joined_ids":[16,17]})


static func join_chapter306(before: Dictionary, rules: Dictionary) -> Dictionary:
	if rules.is_empty():return Origin.failure("invalid_join_source")
	if before.get("phase")!="sortie_workroom":return Origin.failure("chapter306_requires_workroom")
	var reason := _validate(before,[3,4,9,5,8,6,1,2,16,17],8,4,rules)
	if not reason.is_empty():return Origin.failure(reason)
	var raw := FileAccess.get_file_as_string(AUGUST_FOUR[0]).replace("\r\n","\n")
	if raw.sha256_text()!=AUGUST_FOUR[1]:return Origin.failure("invalid_join_source")
	var source: Dictionary=Roles._integers(JSON.parse_string(raw))
	var after:=before.duplicate(true)
	var school: Dictionary=after["school"]
	_append_teacher(school,source["join_profiles"][1])
	_append_student(after,source,rules)
	school["relationships"].append_array(source["join_relationships"].duplicate(true))
	after["phase"]="chapter306_joined"
	return _result(after,"chapter306_joined",{"joined_ids":[116,13]})


static func join_chapter030b(before: Dictionary, rules: Dictionary) -> Dictionary:
	if before.get("phase")!="sortie_settled":
		return Origin.failure("chapter030b_requires_settled_sortie")
	var reason := _validate(before,[3,4,9,5,8],5,4,rules)
	if not reason.is_empty(): return Origin.failure(reason)
	if before["school"]["lecture_work_fields"][2]!=7:
		return Origin.failure("chapter030b_requires_adventure7")
	return _join_pair(before,rules,WEEK_FIVE,"chapter030b_joined",115)


static func _join_pair(before: Dictionary, rules: Dictionary, resource: Array, status: String, teacher: int) -> Dictionary:
	var encoded := FileAccess.get_file_as_string(resource[0]).replace("\r\n","\n")
	if encoded.sha256_text()!=resource[1]: return Origin.failure("invalid_join_source")
	var source: Dictionary = Roles._integers(JSON.parse_string(encoded))
	var after := before.duplicate(true)
	_append_student(after,source,rules)
	var school: Dictionary = after["school"]
	_append_teacher(school,source["join_profiles"][1])
	school["relationships"].append_array(source["join_relationships"].duplicate(true))
	if teacher==115: after["phase"]=status
	return _result(after,status,{"joined_ids":[source["candidate"]["character_id"],teacher]})


static func _append_teacher(school: Dictionary, profile: Dictionary) -> void:
	var id: int=profile["member_id"]
	var index: int=school["teacher_count"]
	school["teacher_ids"][index]=id
	school["raw_teacher_ids"][index]=id
	school["availability"][id]=1
	school["teacher_count"]+=1
	school["member_profiles"].append(profile.duplicate(true))


static func _append_student(after: Dictionary, source: Dictionary, rules: Dictionary) -> void:
	var school: Dictionary = after["school"]
	var candidate: Dictionary = source["candidate"].duplicate(true)
	var identity: int = candidate["character_id"]
	candidate["unlock_flags"].fill(0)
	candidate["unlock_reserved_bytes"].fill(0)
	candidate["unlock_flags"][candidate["job"]-1] = 1
	for slot in range(8):
		var item: int = candidate["equipped_items"][slot]
		if item > 0:
			var flags: int = after["item_flags"][item-1]
			if flags & 1: candidate["equipped_items"][slot] = 0
			else: after["item_flags"][item-1] = ((flags | 1) & 0xf001) | 0x300 | (identity << 1)
		var skill: int = candidate["equipped_skills"][slot]
		if skill > 0:
			# Native4D3E90 keeps skills at BOTH difficulty0 and1.
			if after["school"]["difficulty"] in [0,1]: candidate["skill_statuses"][skill-1] = 6
			else: candidate["equipped_skills"][slot] = 0
	candidate["level_50"] = Growth._level(Growth._total(candidate,rules["role"]),rules["role"]["level_thresholds"])
	Week.apply_unlocks(candidate,school["month"],school["week"],rules["week"])
	after["participants"].append(candidate)
	after["growth"].append(Origin.field_subset(candidate,["character_id"]+GROWTH_KEYS))
	after["records"].append(source["history"].duplicate(true))
	after["counts"].append({"character_id":identity,"count":0})
	var index: int=school["student_count"]
	school["student_ids"][index] = identity
	school["raw_student_ids"][index] = identity
	school["student_count"] += 1
	school["availability"][identity] = 1
	school["member_profiles"].insert(index+1,{"member_id":identity,"job":candidate["job"],"level_50":candidate["level_50"],
		"attributes":candidate["attributes"].duplicate(),"storage_kind":"student_record",
		"template_sha256":source["join_profiles"][0]["template_sha256"] if source.has("join_profiles") else source["template_sha256"]})


static func next_week(before: Dictionary) -> Dictionary:
	var rules := _rules()
	if rules.is_empty(): return Origin.failure("invalid_postbattle_source_rules")
	var reason := _validate(before,[3,4,9,5],4,5,rules)
	if not reason.is_empty(): return Origin.failure(reason)
	if before.get("phase") != "chapter020_joined": return Origin.failure("week_requires_chapter020_join")
	var result := Week.project(_week_input(before),rules["week"])
	if not result["supported"]: return result
	var after := before.duplicate(true)
	after["participants"] = result["after"]["participants"]
	after["item_flags"] = result["after"]["item_flags"]
	after["flags"] = result["after"]["flags"]
	after["school"]["month"] = 5
	after["school"]["week"] = 1
	for row in after["growth"]:
		var participant := _find(after["participants"],row["character_id"])
		for key in GROWTH_KEYS: row[key] = participant[key].duplicate(true) if participant[key] is Array else participant[key]
	after["phase"] = "week_advanced"
	return _result(after,"week_advanced",{"date":[5,1],"week_executed":true,"week_source":"0x49f4e0->0x4d3510"})


static func school_return(before: Dictionary) -> Dictionary:
	var rules := _rules()
	if rules.is_empty(): return Origin.failure("invalid_postbattle_source_rules")
	var reason := _validate(before,[3,4,9,5],5,1,rules)
	if not reason.is_empty(): return Origin.failure(reason)
	if before.get("phase") != "week_advanced": return Origin.failure("school_requires_week_advance")
	var after := before.duplicate(true)
	var unlocked := Courses.unlock_courses(after["school"],rules["school"]["course_rules"])
	if not unlocked["supported"]: return unlocked
	var school: Dictionary = unlocked["after"]
	# 4A5CE0 clears a prior selected adventure if it is absent from the new list.
	# This first result's mandatory scene5 has ended; newly dated work8 is optional.
	school["adventure_gate"] = 0
	school["lecture_active"] = 0
	var prepared := _prepare(school,rules)
	if not prepared["supported"]: return prepared
	after["school"] = prepared["after"]
	after["ratings"] = prepared["ratings"]
	after["flags"]["0x7a55fa"] = 0
	after["flags"]["0x7a4e62"] = 1
	# CH002 opcode151 at5/1 restores11/0 after Chapter208's9/1.
	after["flags"]["0x7a55f6"] = 11
	after["flags"]["0x7e11a0"] = 0
	after["newly_dated_adventures"] = []
	for rule in rules["boot"]["adventures"]:
		if rule["present"] and rule["gate"] and rule["kind"] and rule["month"]==5 and rule["week"]==1:
			after["newly_dated_adventures"].append(rule.duplicate(true))
	after["rankings"] = _rankings(after["school"])
	after["phase"] = "school_returned"
	return _result(after,"school_returned",{"unlocked_work_ids":unlocked["unlocked_work_ids"],
		"school_boot_data_projected":true,"adventure_catalog_complete":false,
		"planning_scope":"four_students_teacher101_movement_and_course_availability"})


static func validate_planning_roster(bundle: Dictionary, rules: Dictionary) -> String:
	var school: Variant = bundle.get("school")
	if not school is Dictionary or school.get("week") not in [1,2,3,4,5]:
		return "outside_current_return_week"
	if school.get("month")==8 and school["week"]==4 and bundle.get("phase") not in ["sortie_week_advanced","sortie_workroom"]:
		return _validate(bundle,[3,4,9,5,8,6,1,2,16,17,13],8,4,rules)
	if (school.get("month")==7 and school["week"]==5) or (school.get("month")==8 and school["week"] in [1,2,3,4]):
		return _validate(bundle,[3,4,9,5,8,6,1,2,16,17],school.month,school.week,rules)
	if school.get("month")==7 and school["week"] in [1,2,3,4]:
		return _validate(bundle,[3,4,9,5,8,6,1,2],7,school["week"],rules)
	if school.get("month")==6 and school["week"] in [2,3,4,5]:
		return _validate(bundle,[3,4,9,5,8,6,1,2],6,school["week"],rules)
	if school.get("month")==6 and school["week"]==1:
		return _validate(bundle,[3,4,9,5,8,6,1],6,1,rules)
	var ids := [3,4,9,5]
	if school["week"]>=4: ids.append(8)
	if school["week"]==5: ids.append(6)
	return _validate(bundle,ids,5,school["week"],rules)


static func move_member(before: Dictionary, command: Dictionary) -> Dictionary:
	var rules := _rules()
	if rules.is_empty(): return Origin.failure("invalid_postbattle_source_rules")
	var reason := validate_planning_roster(before,rules)
	if not reason.is_empty(): return Origin.failure(reason)
	if before.get("phase") != "school_returned": return Origin.failure("movement_requires_school_return")
	for key in command:
		if key not in ["kind","member_id","target_group","target_slot"]: return Origin.failure("invalid_move_command")
	var kind: Variant = command.get("kind")
	var id: Variant = command.get("member_id")
	var target: Variant = command.get("target_group")
	var slot: Variant = command.get("target_slot",-1)
	var school: Dictionary = before["school"]
	if kind not in ["student","teacher"] or not Week._bounded(target,-1,4) or not Week._bounded(slot,-1,3):
		return Origin.failure("invalid_move_target")
	if id not in school[kind+"_ids"].slice(0,school[kind+"_count"]):
		return Origin.failure("invalid_move_target")
	if (kind=="teacher" and slot!=-1) or (kind=="student" and ((target==-1 and slot!=-1) or (target>=0 and slot<0))):
		return Origin.failure("invalid_move_target")
	var source := {}
	for group in range(5):
		if kind=="teacher" and Groups._word(school["group_raw_bytes"],group*28)==id: source={"group":group,"slot":-1}
		if kind=="student":
			for index in range(4):
				if Groups._word(school["group_raw_bytes"],group*28+16+index*2)==id: source={"group":group,"slot":index}
	var waiting: Array = school["idle_student_ids" if kind=="student" else "idle_teacher_ids"]
	if waiting.has(id): source={"group":-1,"slot":waiting.find(id)}
	if source.is_empty(): return Origin.failure("missing_current_member")
	var rated := Groups.rate(school,group_rules(school))
	if not rated["supported"]: return rated
	var working := Session._working(school)
	working.merge({"drag_kind":1 if kind=="teacher" else 0,"drag_origin":0 if source["group"]==-1 else 1,
		"drag_group":source["group"],"drag_slot":source["slot"],"drag_id":id,
		"drag_source_rank":0 if source["group"]==-1 else rated["ratings"][source["group"]]["relationship_rank"]},true)
	var request := {"kind":kind,kind+"_id":id,"source_group":source["group"],"source_slot":source["slot"],
		"target_group":target,"released":true}
	var moved: Dictionary
	if kind=="student":
		request["target_slot"]=slot
		moved=Student.move_student(working,request,Session._student_profiles(school),group_rules(school),sort_rules(school,rules))
	else:
		moved=Teacher.move_teacher(working,request,Session._student_profiles(school),group_rules(school),sort_rules(school,rules),work_rules(school,rules))
	if not moved["supported"]: return moved
	var prepared := _prepare(Session._canonical(moved["after"]),rules)
	if not prepared["supported"]: return prepared
	var after := before.duplicate(true)
	after["school"] = prepared["after"]
	after["ratings"] = prepared["ratings"]
	return _result(after,"member_moved")


static func _prepare(school: Dictionary, rules: Dictionary) -> Dictionary:
	var clean := Teacher.reconcile(Session._working(school),group_rules(school),work_rules(school,rules))
	if not clean["supported"]: return clean
	var sorted := Sort.order(Session._student_profiles(school),clean["after"]["idle_student_ids"],0,sort_rules(school,rules))
	if not sorted["supported"]: return sorted
	clean["after"]["idle_student_ids"] = sorted["idle_student_ids"]
	var rated := Groups.rate(clean["after"],group_rules(school))
	if not rated["supported"]: return rated
	return {"supported":true,"after":Session._canonical(rated["after"]),"ratings":rated["ratings"]}


static func _rankings(school: Dictionary) -> Array:
	var profiles := Session._student_profiles(school)
	var values := []
	for row in profiles:
		var attributes: Array = row["attributes"].duplicate()
		var total := 0
		for value in attributes: total+=value
		attributes.append(total)
		values.append(attributes)
	var ranks := []
	for row in values:
		var current := []
		for column in range(8):
			var rank := 1
			for other in values:
				if other[column]>row[column]: rank+=1
			current.append(rank)
		ranks.append(current)
	return ranks


static func _sync_participants(bundle: Dictionary) -> void:
	for row in bundle["participants"]:
		var growth := _find(bundle["growth"],row["character_id"])
		for key in GROWTH_KEYS: row[key] = growth[key].duplicate(true) if growth[key] is Array else growth[key]
		row["job_progress"] = _find(bundle["records"],row["character_id"])["job_progress"].slice(0,31)


static func _find(rows: Array, id: int) -> Dictionary:
	for row in rows:
		if row["character_id"]==id: return row
	return {}


static func _week_input(bundle: Dictionary) -> Dictionary:
	return {"month":bundle["school"]["month"],"week":bundle["school"]["week"],"flags":bundle["flags"].duplicate(true),
		"availability":bundle["school"]["availability"].slice(0,45),"participants":bundle["participants"].duplicate(true),
		"item_flags":bundle["item_flags"].duplicate()}


static func _validate(bundle: Dictionary, ids: Array, month: int, week: int, rules: Dictionary) -> String:
	if not bundle.get("school") is Dictionary or not bundle.get("participants") is Array 		or not bundle.get("growth") is Array or not bundle.get("records") is Array or not bundle.get("counts") is Array 		or not bundle.get("flags") is Dictionary or not Week._vector(bundle.get("item_flags"),360,0,65535): return "invalid_postbattle_bundle"
	var school: Dictionary = bundle["school"]
	var teachers := [101]
	if ids.has(8): teachers.append(110)
	if ids.has(6): teachers.append(115)
	if _has_four_teachers(school): teachers.append(118)
	if ids.has(13):teachers.append(116)
	var reason := Groups._validate(school,group_rules(school))
	if not reason.is_empty(): return reason
	if school.get("month")!=month or school.get("week")!=week or school["student_ids"].slice(0,school["student_count"])!=ids \
		or school["teacher_ids"].slice(0,school["teacher_count"])!=teachers \
		or not Week._bounded(school.get("difficulty"),0,2) or not Week._bounded(school.get("global_total_511c"),0,999999999) \
		or not Week._vector(school.get("raw_student_ids"),40,0,44) \
		or not school.get("member_profiles") is Array or school["member_profiles"].size()!=ids.size()+teachers.size(): return "outside_current_return_roster"
	if teachers.has(110):
		if (not Week._vector(school.get("raw_teacher_ids"),20,0,120)
				or school["raw_teacher_ids"].slice(0,teachers.size())!=teachers
				or school["raw_student_ids"].slice(0,ids.size())!=ids):
			return "invalid_chapter029_roster"
		for index in range(1,teachers.size()):
			var teacher: Variant=school["member_profiles"][ids.size()+index]
			var identity: int=teachers[index]
			var expected_sha := "bc3a30a04ca4e32a3d40c50f9beb18d65354006d9246e43858049bd9cd84cabc" if identity==110 else "5bcf15751c390f22d43e7d3c7e88259f009e523cfdb93f937fb3a88e17a663c7"
			if identity==118:expected_sha="2b6766966dc7f55df460999262331520e52be33433117109a2d8ff8aeffdcc04"
			if identity==116:expected_sha="b986d2e72edf00de0185aa5422ccc526e113ebb4b7ebff67380320a289177eeb"
			if (not teacher is Dictionary or teacher.get("member_id")!=identity or teacher.get("job")!=1
					or teacher.get("level_50")!=0 or not Week._vector(teacher.get("attributes"),7,0,0)
					or teacher.get("storage_kind")!="static_teacher_template" or teacher.get("template_sha256")!=expected_sha):
				return "invalid_chapter029_teacher_profile" if identity==110 else "invalid_chapter030b_teacher_profile"

	var members := teachers+ids
	if school["relationships"].size()!=members.size()*(members.size()-1): return "incomplete_return_relationships"
	for a in members:
		for b in members:
			if a==b: continue
			var found := false
			for relation in school["relationships"]:
				if relation["from"]==a and relation["to"]==b: found=true
			if not found: return "incomplete_return_relationships"
	for key in ["participants","growth","records","counts"]:
		if bundle[key].size()!=ids.size(): return "missing_return_"+key
		for index in range(ids.size()):
			if not bundle[key][index] is Dictionary or bundle[key][index].get("character_id")!=ids[index]: return "invalid_return_"+key
	for index in range(ids.size()):
		var growth: Dictionary = bundle["growth"][index]
		for key in GROWTH_KEYS:
			if not growth.has(key): return "missing_return_growth_field"
		for spec in [["attributes",7,1,135],["growth_pools",7,0,2147483647],["skill_statuses",84,0,6],["job_sums",5,-768,762]]:
			if not Week._vector(growth[spec[0]],spec[1],spec[2],spec[3]): return "invalid_return_growth_field"
		if not Week._bounded(growth["job"],1,30) or not Week._bounded(growth["level_50"],1,50) 			or not Week._bounded(growth["staged_total"],0,2147483647): return "invalid_return_growth_scalar"
		var profile: Variant = school["member_profiles"][index+1]
		if not profile is Dictionary or profile.get("member_id")!=ids[index]: return "invalid_return_profile"
		for key in ["job","attributes","level_50"]:
			if profile.get(key)!=growth[key]: return "stale_return_profile"
		if not Week._vector(bundle["records"][index].get("job_progress"),33,0,100) 			or not Week._vector(bundle["records"][index].get("week_records"),177,0,255) 			or not Week._bounded(bundle["counts"][index].get("count"),0,5): return "invalid_return_history"
		if bundle.has("phase"):
			for key in GROWTH_KEYS:
				if bundle["participants"][index].get(key)!=growth[key]: return "stale_return_participant"
			if bundle["participants"][index].get("job_progress")!=bundle["records"][index]["job_progress"].slice(0,31): return "stale_return_history"
	reason = Week._validate(_week_input(bundle),rules["week"])
	return reason


static func _rules() -> Dictionary:
	var output := {}
	for key in SOURCES:
		var content := FileAccess.get_file_as_string(SOURCES[key][0]).replace("\r\n","\n")
		if content.sha256_text()!=SOURCES[key][1]: return {}
		var raw: Variant = JSON.parse_string(content)
		if not raw is Dictionary: return {}
		# Historic fixture cases are never selected or used as current state.
		output[key]=Roles._integers(raw["rules"] if key in ["week","role"] else raw["boot_rules"] if key=="boot" else raw)
	return output


static func _result(after: Dictionary, status: String, extra: Dictionary = {}) -> Dictionary:
	var output := Origin.success(status)
	output.merge({"after":after,"native_equivalence_verified":false,"original_save_written":false})
	output.merge(extra)
	return output
