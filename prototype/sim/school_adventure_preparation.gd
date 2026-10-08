extends RefCounted
## Pure defined projection of source4A7D30/4A6A10; no departure or battle commit.

const Groups := preload("res://sim/school_teacher_group_replay.gd")
const Origin := preload("res://sim/new_game_school_origin.gd")
const RECORD_SHA := "65beefd33bf2734d05aaff2ff446ce1a9c2d6e8d978823747181d0b2e4fe9e0b"
const RULE_PATH := "res://data/school_adventure_preparation_rules.json"


static func project(school: Dictionary, rules: Dictionary) -> Dictionary:
	if not _rules_valid(rules):
		return Origin.failure("unsupported_adventure_preparation_rules")
	if school.get("month") != 4 or school.get("week") != 5 \
			or school.get("adventure_gate") != 1 or school.get("lecture_active") != 1 \
			or school.get("lecture_work_fields") != [3,4,5,0]:
		return Origin.failure("outside_fifth_mandatory_adventure")
	var rated := Groups.rate(school,Origin.group_rules())
	if not rated["supported"]:
		return rated
	var ratings: Array = rated["ratings"]
	var ready_classes := []
	var incomplete := []
	for group in range(5):
		match ratings[group]["state"]:
			2: ready_classes.append(group)
			0: pass
			_: incomplete.append(group)
	var ready := not ready_classes.is_empty() and incomplete.is_empty()
	var prepared: Variant = null
	if ready:
		var students := []
		var student_groups := []
		var teachers := []
		var raw: Array = school["group_raw_bytes"]
		for group in ready_classes:
			teachers.append(Groups._word(raw,group*28))
			for slot in range(4):
				var identity := Groups._word(raw,group*28+16+slot*2)
				if identity >= 0:
					students.append(identity)
					student_groups.append(group)
		prepared = {"adventure_id":5,"round_index":0,"round_count":1,
			"class_ratings":ratings.duplicate(true),"rounds":[{"scene_id":5,
			"teacher_ids":teachers,"student_ids":students,"student_groups":student_groups}]}
	return {"supported":true,"ready":ready,"prepared":prepared,
		"reason":"ready" if ready else "incomplete_class" if not incomplete.is_empty() else "no_adventure_class",
		"class_ratings":ratings.duplicate(true),"incomplete_classes":incomplete,
		"idle_student_ids":school["idle_student_ids"].duplicate(),
		"idle_teacher_ids":school["idle_teacher_ids"].duplicate(),
		"adventure_id":5,"scene_ids":[5],"battle_executed":false,"mandatory_gate_cleared":false}


static func _rules_valid(rules: Dictionary) -> bool:
	return rules.get("schema_version") == 1 and rules.get("source_image_sha256") == Groups.SOURCE_SHA \
		and rules.get("record_sha256") == RECORD_SHA and rules.get("adventure_id") == 5 \
		and rules.get("required_date") == [4,5] and rules.get("mandatory_gate") == 1 \
		and rules.get("table_va") == "0x73bed0" and rules.get("record_stride") == 256 \
		and rules.get("round_specs") == [{"scene_id":5,"selection_word":1}] \
		and rules.get("required_work_fields") == [3,4,5,0] \
		and rules.get("functions") == {"readiness":"0x4a7d30","prepare_rounds":"0x4a6a10"}
