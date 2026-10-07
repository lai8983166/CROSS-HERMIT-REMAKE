extends RefCounted
## Native4C1350/4BF9E0 post fields only; MVP/ADV/week remain separate.

const Origin := preload("res://sim/new_game_school_origin.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")
const Courses := preload("res://sim/school_course_unlocking.gd")
const Settlement := preload("res://sim/school_course_settlement.gd")
const FIELDS_SHA := "d2d952f5fc2dc41cd137ba817640ae5a0041d305f89384e1613ccc726110836e"
const IDS := [3,4,9]


static func source_subset(input: Dictionary) -> Dictionary:
	return Origin.field_subset(input,["source_image_sha256","confirmation_fields_sha256","job_categories","initial_records"])


static func valid_rules(rules: Dictionary) -> bool:
	if rules.get("source_image_sha256") != Courses.SOURCE_SHA or rules.get("confirmation_fields_sha256") != FIELDS_SHA \
			or not Origin._vector(rules.get("job_categories"),31,0,5) or not valid_records(rules.get("initial_records")):
		return false
	var fields := []
	for key in ["job_categories","initial_records"]:
		if not Settlement._flatten(rules[key],fields):
			return false
	var encoded := PackedStringArray()
	for value in fields:
		encoded.append(str(value))
	return ":".join(encoded).sha256_text() == FIELDS_SHA


static func valid_records(records: Variant) -> bool:
	if not records is Array or records.size() != 3:
		return false
	for index in range(3):
		var row: Variant = records[index]
		if not row is Dictionary or row.keys() != ["character_id","job_progress","week_records"] \
				or not Courses._integer(row.get("character_id"),IDS[index],IDS[index]) \
				or not Origin._vector(row.get("job_progress"),33,0,255) or not Origin._vector(row.get("week_records"),177,0,255):
			return false
	return true


static func apply(before: Dictionary, records: Array, rules: Dictionary) -> Dictionary:
	if not valid_rules(rules):
		return Origin.failure("invalid_confirmation_source_rules")
	if not valid_records(records):
		return Origin.failure("invalid_confirmation_records")
	if not Courses._integer(before.get("month"),4,4) or not Courses._integer(before.get("week"),4,4) \
			or not Courses._integer(before.get("student_count"),3,3) or not before.get("student_ids") is Array \
			or before["student_ids"].slice(0,3) != IDS:
		return Origin.failure("confirmation_requires_declared_source_date_and_roster")
	var rated := Groups.rate(before,Origin.group_rules())
	if not rated["supported"]:
		return rated
	if not before.get("member_profiles") is Array or before["member_profiles"].size() != 4:
		return Origin.failure("invalid_confirmation_profiles")
	var profiles := {}
	for row in before["member_profiles"]:
		if not row is Dictionary or not Courses._integer(row.get("member_id"),1,101) \
				or row["member_id"] not in [101,3,4,9] or profiles.has(row["member_id"]) \
				or not Courses._integer(row.get("job"),1,30) \
				or not Courses._integer(row.get("level_50"),0 if row["member_id"] == 101 else 1,50):
			return Origin.failure("invalid_confirmation_profiles")
		profiles[row["member_id"]] = row
	var assigned := []
	var classes := []
	var eligible := false
	for group in range(5):
		var students: Array = rated["after"]["derived_student_ids"][group].filter(func(id): return id != -1)
		var rating: Dictionary = rated["ratings"][group]
		if rating["state"] in [2,3,5] or (not students.is_empty() and rating["state"] != 4):
			return Origin.failure("unsupported_confirmation_class")
		if rating["state"] == 4:
			if rating["work_fields"][2] not in [10,11,12]:
				return Origin.failure("unsupported_confirmation_course")
			eligible = true
		assigned.append_array(students)
		classes.append({"students":students,"teacher":Groups._word(before["group_raw_bytes"],28*group),"rating":rating})
	if not eligible:
		return Origin.failure("missing_settled_course_class")
	# All directed relationships among the supported roster must exist once.
	var relations := {}
	for row in before["relationships"]:
		relations["%d:%d" % [row["from"],row["to"]]] = row
	for a in [101,3,4,9]:
		for b in [101,3,4,9]:
			if a != b and not relations.has("%d:%d" % [a,b]):
				return Origin.failure("missing_confirmation_relationship")
	var after := before.duplicate(true)
	var output := records.duplicate(true)
	var history_index := 3 # Declared4/4 only; full calendar is a separate stage.
	for index in range(3):
		var row: Dictionary = output[index]
		var job: int = profiles[IDS[index]]["job"]
		var value: int = row["job_progress"][job]
		if value != 100:
			value = ((value + 1 + 128) & 255) - 128
			row["job_progress"][job] = clampi(value,0,99)
		row["week_records"][history_index*3] = 3
		for item in classes:
			if IDS[index] in item["students"]:
				row["week_records"][history_index*3] = 1
				row["week_records"][history_index*3+1] = item["rating"]["work_fields"][0] & 255
				row["week_records"][history_index*3+2] = item["rating"]["work_fields"][1] & 255
	var waiting := IDS.filter(func(id): return id not in assigned)
	var calls := []
	for a in waiting:
		for b in waiting:
			if a == b:
				continue
			if rules["job_categories"][profiles[a]["job"]] == rules["job_categories"][profiles[b]["job"]]:
				calls.append({"from":a,"to":b,"delta":1})
			if profiles[a]["level_50"] == profiles[b]["level_50"]:
				calls.append({"from":a,"to":b,"delta":1})
	for a in waiting:
		for b in waiting:
			if a != b:
				calls.append({"from":a,"to":b,"delta":2})
	for a in waiting:
		for b in assigned:
			if a != b:
				calls.append({"from":a,"to":b,"delta":-1})
	for item in classes:
		for a in item["students"]:
			for b in item["students"]:
				if a != b:
					calls.append({"from":a,"to":b,"delta":1})
		for a in item["students"]:
			calls.append({"from":a,"to":item["teacher"],"delta":1})
			calls.append({"from":item["teacher"],"to":a,"delta":1})
	for call in calls:
		for row in after["relationships"]:
			if row["from"] == call["from"] and row["to"] == call["to"]:
				row["value"] = clampi(row["value"]+call["delta"],1,100)
	var result := Origin.success("course_confirmation_fields")
	result.merge({"after":after,"records":output,"relationship_calls":calls,"history_index":history_index})
	return result
