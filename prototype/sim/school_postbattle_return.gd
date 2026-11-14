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
const SOURCES := {
	"candidate":["res://data/school_postbattle_return_rules.json","1775635836be11e1c038437bb7043a2b2989bdccb880d8882fcda06d41fdb854"],
	"week":["res://data/week_settlement_evidence.json","5bdb406c2125c610c75942a9e589a9b427cdbcd5d97b0cbf35c014b1d793aedf"],
	"role":["res://data/role_application_evidence.json","b0c1f014711dabe3a70482967f58761d8915779da1bbcfcf2eadb18969d38055"],
	"school":["res://data/new_game_school_rules.json","ac4faffab74cb73b7f39c0c1a28a05a96f20f426aa1c5124eec58e1541bbef97"],
	"boot":["res://data/school_boot_evidence.json","066ac6af7eb1f8b4b5a8b7d363cff5fcb62760652065b06fc9cf77cb8546301e"]}
const GROWTH_KEYS := ["job","attributes","growth_pools","level_50","skill_statuses","job_sums","staged_total"]


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
	var candidate: Dictionary = rules["candidate"]["candidate"].duplicate(true)
	candidate["unlock_flags"].fill(0)
	candidate["unlock_reserved_bytes"].fill(0)
	candidate["unlock_flags"][candidate["job"]-1] = 1
	for slot in range(8):
		var item: int = candidate["equipped_items"][slot]
		if item > 0:
			var flags: int = after["item_flags"][item-1]
			if flags & 1: candidate["equipped_items"][slot] = 0
			else: after["item_flags"][item-1] = ((flags | 1) & 0xf001) | 0x300 | (5 << 1)
		var skill: int = candidate["equipped_skills"][slot]
		if skill > 0:
			# Native4D3E90 keeps skills at BOTH difficulty0 and1.
			if after["school"]["difficulty"] in [0,1]: candidate["skill_statuses"][skill-1] = 6
			else: candidate["equipped_skills"][slot] = 0
	candidate["level_50"] = Growth._level(Growth._total(candidate,rules["role"]),rules["role"]["level_thresholds"])
	Week.apply_unlocks(candidate,4,5,rules["week"])
	after["participants"].append(candidate)
	after["growth"].append(Origin.field_subset(candidate,["character_id"]+GROWTH_KEYS))
	after["records"].append(rules["candidate"]["history"].duplicate(true))
	after["counts"].append({"character_id":5,"count":0})
	var school: Dictionary = after["school"]
	school["student_count"] = 4
	school["student_ids"][3] = 5
	school["raw_student_ids"][3] = 5
	school["availability"][5] = 1
	school["relationships"].append_array(rules["candidate"]["relationships"].duplicate(true))
	school["member_profiles"].append({"member_id":5,"job":candidate["job"],"level_50":candidate["level_50"],
		"attributes":candidate["attributes"].duplicate(),"storage_kind":"student_record",
		"template_sha256":rules["candidate"]["template_sha256"]})
	after["phase"] = "chapter020_joined"
	return _result(after,"joined",{"join_source":"Chapter020.ybc:0x14/opcode144","joined_id":5})


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


static func move_member(before: Dictionary, command: Dictionary) -> Dictionary:
	var rules := _rules()
	if rules.is_empty(): return Origin.failure("invalid_postbattle_source_rules")
	var reason := _validate(before,[3,4,9,5],5,1,rules)
	if not reason.is_empty(): return Origin.failure(reason)
	if before.get("phase") != "school_returned": return Origin.failure("movement_requires_school_return")
	for key in command:
		if key not in ["kind","member_id","target_group","target_slot"]: return Origin.failure("invalid_move_command")
	var kind: Variant = command.get("kind")
	var id: Variant = command.get("member_id")
	var target: Variant = command.get("target_group")
	var slot: Variant = command.get("target_slot",-1)
	if kind not in ["student","teacher"] or not Week._bounded(target,-1,4) or not Week._bounded(slot,-1,3) 		or (kind=="teacher" and (id!=101 or slot!=-1)) or (kind=="student" and (id not in [3,4,9,5] 		or (target==-1 and slot!=-1) or (target>=0 and slot<0))): return Origin.failure("invalid_move_target")
	var school: Dictionary = before["school"]
	var source := {}
	for group in range(5):
		if kind=="teacher" and Groups._word(school["group_raw_bytes"],group*28)==id: source={"group":group,"slot":-1}
		if kind=="student":
			for index in range(4):
				if Groups._word(school["group_raw_bytes"],group*28+16+index*2)==id: source={"group":group,"slot":index}
	var waiting: Array = school["idle_student_ids" if kind=="student" else "idle_teacher_ids"]
	if waiting.has(id): source={"group":-1,"slot":waiting.find(id)}
	if source.is_empty(): return Origin.failure("missing_current_member")
	var rated := Groups.rate(school,Origin.group_rules())
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
		moved=Student.move_student(working,request,Session._student_profiles(school),Origin.group_rules(),rules["school"]["sort_rules"])
	else:
		moved=Teacher.move_teacher(working,request,Session._student_profiles(school),Origin.group_rules(),rules["school"]["sort_rules"],rules["school"]["work_rules"])
	if not moved["supported"]: return moved
	var prepared := _prepare(Session._canonical(moved["after"]),rules)
	if not prepared["supported"]: return prepared
	var after := before.duplicate(true)
	after["school"] = prepared["after"]
	after["ratings"] = prepared["ratings"]
	return _result(after,"member_moved")


static func _prepare(school: Dictionary, rules: Dictionary) -> Dictionary:
	var clean := Teacher.reconcile(Session._working(school),Origin.group_rules(),rules["school"]["work_rules"])
	if not clean["supported"]: return clean
	var sorted := Sort.order(Session._student_profiles(school),clean["after"]["idle_student_ids"],0,rules["school"]["sort_rules"])
	if not sorted["supported"]: return sorted
	clean["after"]["idle_student_ids"] = sorted["idle_student_ids"]
	var rated := Groups.rate(clean["after"],Origin.group_rules())
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
	var reason := Groups._validate(school,Origin.group_rules())
	if not reason.is_empty(): return reason
	if school.get("month")!=month or school.get("week")!=week or school["student_ids"].slice(0,school["student_count"])!=ids \
		or school["teacher_ids"].slice(0,school["teacher_count"])!=[101] \
		or not Week._bounded(school.get("difficulty"),0,2) or not Week._bounded(school.get("global_total_511c"),0,999999999) \
		or not Week._vector(school.get("raw_student_ids"),40,0,44) \
		or not school.get("member_profiles") is Array or school["member_profiles"].size()!=ids.size()+1: return "outside_current_return_roster"
	var members := [101]+ids
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
