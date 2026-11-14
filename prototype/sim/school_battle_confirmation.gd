extends RefCounted
## Source-derived 4C1350/4BF9E0 and ordinary 4C1AA0 post fields.
## One pure calculation: caller owns confirmation/readiness and commit deduplication.

const Origin := preload("res://sim/new_game_school_origin.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")
const Courses := preload("res://sim/school_course_unlocking.gd")
const Confirmation := preload("res://sim/school_course_confirmation.gd")
const Handoff := preload("res://sim/school_course_result_handoff.gd")
const Preparation := preload("res://sim/school_adventure_preparation.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const IDS := [3,4,9]
const MEMBERS := [101,3,4,9]
const GRADE_DELTA := [3,2,1,0,-1]


static func apply(school: Dictionary, records: Array, growth: Array, counts: Array,
		preparation: Dictionary, grade: int) -> Dictionary:
	var rules := _rules()
	if rules.is_empty(): return Origin.failure("invalid_battle_confirmation_rules")
	if not Confirmation.valid_records(records) or not Handoff.valid_counts(counts):
		return Origin.failure("invalid_battle_confirmation_records")
	if grade < 0 or grade > 4: return Origin.failure("invalid_battle_grade")
	if not Courses._integer(school.get("month"),4,4) or not Courses._integer(school.get("week"),5,5) \
			or not Courses._integer(school.get("student_count"),3,3) or not Courses._integer(school.get("teacher_count"),1,1) \
			or not school.get("student_ids") is Array or school["student_ids"].slice(0,3) != IDS \
			or not school.get("teacher_ids") is Array or school["teacher_ids"].slice(0,1) != [101]:
		return Origin.failure("outside_fifth_battle_confirmation")
	var expected := Preparation.project(school,rules["preparation"])
	if not expected.get("supported",false) or not expected.get("ready",false) \
			or expected.get("prepared") != preparation:
		return Origin.failure("battle_preparation_mismatch")
	var round: Dictionary = preparation["rounds"][0]
	# 4A6A10 selector1 actually copies teachers to 7A52FA and count to 7A5304.
	# This is a separate source mapping, not a general teacher==support rule.
	if round["teacher_ids"] != [101]: return Origin.failure("unsupported_battle_support")
	var profiles := _profiles(school)
	if profiles.is_empty(): return Origin.failure("invalid_battle_profiles")
	if not _valid_relations(school.get("relationships")):
		return Origin.failure("incomplete_battle_relationships")
	var updated := {}
	for row in growth:
		if not row is Dictionary or not Courses._integer(row.get("character_id"),1,12) \
				or row["character_id"] not in round["student_ids"] or updated.has(row["character_id"]) \
				or not Origin._vector(row.get("attributes"),7,1,135) \
				or not Courses._integer(row.get("level_50"),1,50) \
				or not Courses._integer(row.get("staged_total"),-2147483648,2147483647):
			return Origin.failure("invalid_battle_growth")
		updated[row["character_id"]] = row
	if updated.size() != round["student_ids"].size():
		return Origin.failure("missing_battle_growth")
	var classes := []
	var assigned := []
	for group in range(5):
		var students: Array = []
		for slot in range(4):
			var identity := Groups._word(school["group_raw_bytes"],28*group+16+2*slot)
			if identity != -1: students.append(identity)
		var rating: Dictionary = preparation["class_ratings"][group]
		if not students.is_empty() and rating["state"] != 2:
			return Origin.failure("unsupported_battle_class")
		if rating["state"] not in [0,2]: return Origin.failure("unsupported_battle_class")
		if not students.is_empty() and Groups._word(school["group_raw_bytes"],28*group) != 101:
			return Origin.failure("unsupported_battle_teacher")
		assigned.append_array(students)
		classes.append({"students":students,"rating":rating})
	if assigned != round["student_ids"]: return Origin.failure("battle_group_order_mismatch")
	# 4C00C0 chooses strictly greater totals in group/slot order; ties keep first.
	var recipient := -1
	var best := 0
	for identity in assigned:
		if updated[identity]["staged_total"] > best:
			best = updated[identity]["staged_total"]; recipient = identity
	if recipient == -1: return Origin.failure("missing_positive_battle_recipient")
	var after := school.duplicate(true)
	for profile in after["member_profiles"]:
		if updated.has(profile["member_id"]):
			var row: Dictionary = updated[profile["member_id"]]
			profile["attributes"] = row["attributes"].duplicate()
			profile["level_50"] = row["level_50"]
	profiles = _profiles(after)
	var output := records.duplicate(true)
	var history_index := 4 # The declared current date is 4/5.
	for row in output:
		var identity: int = row["character_id"]
		var job: int = profiles[identity]["job"]
		var value: int = row["job_progress"][job]
		if value != 100:
			value = ((value+1+128)&255)-128
			row["job_progress"][job] = clampi(value,0,99)
		row["week_records"][history_index*3] = 3
		for item in classes:
			if identity in item["students"]:
				row["week_records"][history_index*3] = 2
				row["week_records"][history_index*3+1] = item["rating"]["work_fields"][0]&255
				row["week_records"][history_index*3+2] = item["rating"]["work_fields"][1]&255
	var waiting := IDS.filter(func(id): return id not in assigned)
	var calls := []
	for a in waiting:
		for b in waiting:
			if a == b: continue
			if rules["confirmation"]["job_categories"][profiles[a]["job"]] == rules["confirmation"]["job_categories"][profiles[b]["job"]]:
				calls.append({"from":a,"to":b,"delta":1})
			if profiles[a]["level_50"] == profiles[b]["level_50"]:
				calls.append({"from":a,"to":b,"delta":1})
	for a in waiting:
		for b in waiting:
			if a != b: calls.append({"from":a,"to":b,"delta":2})
	for a in waiting:
		for b in assigned:
			calls.append({"from":a,"to":b,"delta":-1})
	for item in classes:
		for a in item["students"]:
			for b in item["students"]:
				if a != b: calls.append({"from":a,"to":b,"delta":1})
		for a in item["students"]:
			calls.append({"from":a,"to":101,"delta":1})
			calls.append({"from":101,"to":a,"delta":1})
	for a in round["student_ids"]:
		for b in round["student_ids"]:
			if a != b: calls.append({"from":a,"to":b,"delta":GRADE_DELTA[grade]})
	for a in round["student_ids"]:
		for b in round["teacher_ids"]:
			calls.append({"from":a,"to":b,"delta":GRADE_DELTA[grade]})
			calls.append({"from":b,"to":a,"delta":GRADE_DELTA[grade]})
	for call in calls:
		for relation in after["relationships"]:
			if relation["from"] == call["from"] and relation["to"] == call["to"]:
				relation["value"] = clampi(relation["value"]+call["delta"],1,100)
	var output_counts := counts.duplicate(true)
	var old_count := 0
	for row in output_counts:
		if row["character_id"] == recipient:
			old_count = row["count"]; row["count"] = clampi(old_count+1,0,5)
	var result := Origin.success("battle_confirmation_fields")
	result.merge({"after":after,"records":output,"counts":output_counts,"recipient":recipient,
		"old_count":old_count,"staged_total":best,"relationship_calls":calls,
		"history_index":history_index,"round_support_ids":round["teacher_ids"].duplicate(),
		"adv_request":{"state":6,"script":"adv/dat/ch003.ybc","chapter":"adv/dat/chapter020.ybc",
			"next_task":7,"status":"pending_chapter","chapter_completed":false,"week_advanced":false},
		"date":[4,5],"confirmation_gate_owned_by_caller":true,"persistent_write_authorized":false})
	return result


static func _rules() -> Dictionary:
	var raw: Variant = JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_confirmation_rules.json"))
	var prepared: Variant = JSON.parse_string(FileAccess.get_file_as_string(Preparation.RULE_PATH))
	if not raw is Dictionary or not prepared is Dictionary: return {}
	var confirmation: Dictionary = Roles._integers(raw)
	var preparation: Dictionary = Roles._integers(prepared)
	if not Confirmation.valid_rules(confirmation) or not Preparation._rules_valid(preparation): return {}
	return {"confirmation":confirmation,"preparation":preparation}


static func _profiles(school: Dictionary) -> Dictionary:
	if not school.get("member_profiles") is Array or school["member_profiles"].size() != 4: return {}
	var found := {}
	for row in school["member_profiles"]:
		if not row is Dictionary or not Courses._integer(row.get("member_id"),1,101) \
				or row["member_id"] not in MEMBERS or found.has(row["member_id"]) \
				or not Courses._integer(row.get("job"),1,30) \
				or not Courses._integer(row.get("level_50"),0 if row["member_id"]==101 else 1,50) \
				or not Origin._vector(row.get("attributes"),7,0,255): return {}
		found[row["member_id"]] = row
	return found


static func _valid_relations(value: Variant) -> bool:
	if not value is Array or value.size() != 12: return false
	var found := {}
	for row in value:
		if not row is Dictionary or not Courses._integer(row.get("from"),1,101) \
				or not Courses._integer(row.get("to"),1,101) \
				or row["from"] not in MEMBERS or row["to"] not in MEMBERS or row["from"] == row["to"] \
				or not Courses._integer(row.get("value"),0,100): return false
		var key := "%d:%d" % [row["from"],row["to"]]
		if found.has(key): return false
		found[key] = true
	return found.size() == 12
