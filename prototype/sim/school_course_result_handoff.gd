extends RefCounted
## Native course MVP selector/count and pending ADV entry only.

const Origin := preload("res://sim/new_game_school_origin.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")
const Courses := preload("res://sim/school_course_unlocking.gd")
const IDS := [3,4,9]
const FIELDS_SHA := "f4409f56277445996a73d3c3b7765e382dadd04a24356e1414bf0df9c56cf437"
const SCRIPTS := {
	"allresult/dat/mvp.ybc":"0f2b11ea9c4ae58e6d1505a3f3cfdbfb0cf3daf5d8842e0bc95fb8beaadedca7",
	"allresult/dat/mvp003.ybc":"fa521b24e434a620f5448814a34a8ddb7e7ebf939ccefa5fee0cf32ad7857b1f",
	"allresult/dat/mvp004.ybc":"8bc8de84ba4d5ce8a82e49f441cdcc777ba2b0764710bc31a22c129953224639",
	"allresult/dat/mvp009.ybc":"b4f1f963b9997ebb0fc201703453ff5e48de7d5179d9e03e237e694ccf2dc0bf",
	"adv/dat/ch003.ybc":"5c24ef18116b91cf6b31601ce0e0e6389f01eb2befc2fb0eb9b8f2fd8a6c805b",
	"adv/dat/chapter016.ybc":"59530042604f198ebd24bbed8ac20118a0b6bfcd81189f4f836b440203c39c04"}
const FIELDS := ["class_count","slots_per_class","eligible_id_limit","initial_best","count_cap",
	"month","week","request_state","next_task","chapter_number"]


static func source_subset(input: Dictionary) -> Dictionary:
	return Origin.field_subset(input,["source_image_sha256","result_fields_sha256"]+FIELDS+["script_sha256","initial_counts"])


static func valid_counts(counts: Variant) -> bool:
	if not counts is Array or counts.size() != 3:
		return false
	for i in range(3):
		var row: Variant = counts[i]
		if not row is Dictionary or row.keys() != ["character_id","count"] \
				or not Courses._integer(row.get("character_id"),IDS[i],IDS[i]) \
				or not Courses._integer(row.get("count"),0,5):
			return false
	return true


static func valid_rules(rules: Dictionary) -> bool:
	if rules.get("source_image_sha256") != Courses.SOURCE_SHA or rules.get("result_fields_sha256") != FIELDS_SHA \
			or rules.get("script_sha256") != SCRIPTS or not valid_counts(rules.get("initial_counts")):
		return false
	var values := PackedStringArray()
	for key in FIELDS:
		if not Courses._integer(rules.get(key),0,100):
			return false
		values.append(str(rules[key]))
	for row in rules["initial_counts"]:
		if row["count"] != 0:
			return false
	return ":".join(values).sha256_text() == FIELDS_SHA


static func apply(settled_school: Dictionary, growth: Array, counts: Array, rules: Dictionary) -> Dictionary:
	if not valid_rules(rules):
		return Origin.failure("invalid_course_result_rules")
	if not valid_counts(counts):
		return Origin.failure("invalid_mvp_counts")
	if not Courses._integer(settled_school.get("month"),4,4) or not Courses._integer(settled_school.get("week"),4,4) \
			or not Courses._integer(settled_school.get("student_count"),3,3) \
			or not settled_school.get("student_ids") is Array or settled_school["student_ids"].slice(0,3) != IDS:
		return Origin.failure("course_result_requires_declared_date_and_roster")
	if growth.size() != 3:
		return Origin.failure("invalid_mvp_growth")
	var totals := {}
	for i in range(3):
		var row: Variant = growth[i]
		if not row is Dictionary or not Courses._integer(row.get("character_id"),IDS[i],IDS[i]) \
				or not Courses._integer(row.get("staged_total"),0,0x7fffffff):
			return Origin.failure("invalid_mvp_growth")
		totals[IDS[i]] = row["staged_total"]
	var rated := Groups.rate(settled_school,Origin.group_rules())
	if not rated["supported"]:
		return rated
	var recipient := -1
	var best := 0
	for group in range(5):
		var rating: Dictionary = rated["ratings"][group]
		var assigned: Array = rated["after"]["derived_student_ids"][group]
		if rating["state"] in [2,3,5] or (assigned.any(func(id): return id != -1) and rating["state"] != 4):
			return Origin.failure("unsupported_mvp_class")
		if rating["state"] == 4 and rating["work_fields"][2] not in [10,11,12]:
			return Origin.failure("unsupported_mvp_course")
		for identity in assigned:
			if identity == -1:
				continue
			if not totals.has(identity):
				return Origin.failure("unsupported_mvp_student")
			if identity < 13 and totals[identity] > best:
				best = totals[identity]
				recipient = identity
	if recipient == -1:
		return Origin.failure("missing_positive_mvp_recipient")
	var output := counts.duplicate(true)
	var old_count := 0
	for row in output:
		if row["character_id"] == recipient:
			old_count = row["count"]
			row["count"] = clampi(old_count+1,0,5)
	var result := Origin.success("course_result_handoff")
	result.merge({"recipient":recipient,"staged_total":best,"old_count":old_count,
		"before_counts":counts.duplicate(true),"counts":output,
		"mvp_script":"allresult/dat/mvp%03d.ybc" % recipient,
		"adv_request":{"state":6,"script":"adv/dat/ch003.ybc","chapter":"adv/dat/chapter016.ybc",
			"next_task":7,"status":"pending_chapter","chapter_completed":false,"week_advanced":false},
		"date":[4,4]})
	return result
