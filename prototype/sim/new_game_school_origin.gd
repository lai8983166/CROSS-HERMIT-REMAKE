extends RefCounted
## 来源构造学校字段子集；前驱模板加载与完整新局未移植。

const Groups := preload("res://sim/school_teacher_group_replay.gd")
const Courses := preload("res://sim/school_course_unlocking.gd")
const SOURCE_SHA := Courses.SOURCE_SHA
const ORIGIN_SHA := "d06bdeb2e5951237481a121d0ccec4b46db3e3f9c5509622d19a5b9444a08f76"
const IDS := [101,3,4,9]
const CALLS := [0x49EDA8,0x49EDB8,0x49EDC8,0x49EDD8]
const RULE_KEYS := ["source_image_sha256","initializer_va","origin_fields_sha256","calls",
	"member_profiles","relationships","student_level_inputs","level_thresholds","learned_points"]


static func construct(rules: Dictionary, selected_group: Variant = -1) -> Dictionary:
	rules = source_subset(rules)
	if not validate_rules(rules):
		return failure("invalid_school_origin_rules")
	if not Courses._integer(selected_group,-1,0):
		return failure("outside_declared_origin_selection")
	var raw: Array = []
	raw.resize(140)
	raw.fill(0)
	var derived_teachers := [101,-1,-1,-1,-1]
	var derived_teacher_indices := [0,-1,-1,-1,-1]
	var students: Array = []
	var indices: Array = []
	for group in range(5):
		var base := group*28
		Groups._put_word(raw,base,-1)
		raw[base+3] = 1
		raw[base+4] = 255
		for offset in [6,8,10,12]:
			Groups._put_word(raw,base+offset,-1)
		for slot in range(4):
			Groups._put_word(raw,base+16+slot*2,-1)
		students.append([-1,-1,-1,-1])
		indices.append([-1,-1,-1,-1])
	for call in rules["calls"]:
		var identity: int = call["member_id"]
		if identity > 100:
			Groups._put_word(raw,0,identity)
		else:
			var slot: int = call["slot"]
			Groups._put_word(raw,16+slot*2,identity)
			students[0][slot] = identity
			indices[0][slot] = slot
	var profiles: Array = rules["member_profiles"].duplicate(true)
	for index in range(3):
		var inputs: Dictionary = rules["student_level_inputs"][index]
		var statuses: Array = inputs["skill_statuses"].duplicate()
		for skill in inputs["equipped_skills"]:
			if skill > 0:
				statuses[skill-1] = 6
		var total := 0
		for pool in inputs["growth_pools"]:
			total += pool
		for skill in range(84):
			if statuses[skill] in [3,5,6]:
				total += rules["learned_points"][skill]
		var level := 2
		while level < 51 and rules["level_thresholds"][level-1] <= total:
			level += 1
		profiles[index+1]["level_50"] = level-1
	var availability := _filled(121,0)
	for identity in IDS:
		availability[identity] = 1
	var buffers: Array = []
	for teacher in range(20):
		buffers.append([])
	var after := {"month":4,"week":0,"difficulty":1,"global_total_511c":0,
		"student_count":3,"teacher_count":1,"student_ids":[3,4,9]+_filled(17,-1),
		"teacher_ids":[101]+_filled(19,-1),"raw_student_ids":[3,4,9]+_filled(37,0),
		"raw_teacher_ids":[101]+_filled(19,0),"availability":availability,
		"group_raw_bytes":raw,"derived_teacher_ids":derived_teachers,
		"derived_teacher_indices":derived_teacher_indices,"derived_student_ids":students,
		"derived_student_indices":indices,"idle_student_ids":[],"idle_teacher_ids":[],
		"selected_group":selected_group,"reset_groups":1,"adventure_gate":0,"lecture_active":0,
		"lecture_work_fields":[0,0,0,0],"relationships":rules["relationships"].duplicate(true),
		"member_profiles":profiles,"course_unlocked_flags":_filled(101,0),
		"course_counts":_filled(20,0),"course_buffers":buffers,
		"work_counts":[0,0,0],"work_pages":[0,0,0],"work_page_limits":[0,0,0],"work_rows":[[],[],[]]}
	var result := success("initialized")
	result["after"] = after
	return result


static func _filled(size: int, value: int) -> Array:
	var result: Array = []
	result.resize(size)
	result.fill(value)
	return result


static func _vector(value: Variant, size: int, low: int, high: int) -> bool:
	if not value is Array or value.size() != size:
		return false
	for item in value:
		if not Courses._integer(item,low,high):
			return false
	return true


static func _encode(values: Array) -> String:
	var fields := PackedStringArray()
	for item in values:
		fields.append(str(item))
	return ":".join(fields)


static func validate_rules(rules: Dictionary) -> bool:
	if rules.get("source_image_sha256") != SOURCE_SHA or rules.get("origin_fields_sha256") != ORIGIN_SHA \
			or not Courses._integer(rules.get("initializer_va"),0x49E930,0x49E930):
		return false
	for pair in [["calls",4],["member_profiles",4],["relationships",12],["student_level_inputs",3]]:
		if not Courses._array(rules.get(pair[0]),pair[1]):
			return false
	var encoded := ""
	for index in range(4):
		var row: Variant = rules["calls"][index]
		if not row is Dictionary:
			return false
		for pair in [["call_va",CALLS[index]],["member_id",IDS[index]],["group",0],["slot",index-1]]:
			if not Courses._integer(row.get(pair[0]),pair[1],pair[1]):
				return false
		encoded += _encode([row["call_va"],row["member_id"],row["group"],row["slot"]])+";"
	encoded += "|"
	for index in range(4):
		var p: Variant = rules["member_profiles"][index]
		if not p is Dictionary or not Courses._integer(p.get("member_id"),IDS[index],IDS[index]) \
				or not Courses._integer(p.get("job"),1,30) or not Courses._integer(p.get("level_50"),0,50) \
				or not _vector(p.get("attributes"),7,0,255) or not p.get("template_sha256") is String \
				or p["template_sha256"].length() != 64:
			return false
		if p.get("storage_kind") != ("static_teacher_template" if index == 0 else "student_record"):
			return false
		encoded += _encode([p["member_id"],p["job"],p["level_50"]]+p["attributes"])+":"+p["storage_kind"]+":"+p["template_sha256"]+";"
	encoded += "|"
	var relation_index := 0
	for a in IDS:
		for b in IDS:
			if a == b:
				continue
			var row: Variant = rules["relationships"][relation_index]
			if not row is Dictionary or not Courses._integer(row.get("from"),a,a) \
					or not Courses._integer(row.get("to"),b,b) or not Courses._integer(row.get("value"),1,100):
				return false
			encoded += _encode([a,b,row["value"]])+";"
			relation_index += 1
	encoded += "|"
	for index in range(3):
		var row: Variant = rules["student_level_inputs"][index]
		if not row is Dictionary or not Courses._integer(row.get("member_id"),IDS[index+1],IDS[index+1]) \
				or not _vector(row.get("growth_pools"),7,0,2147483647) \
				or not _vector(row.get("skill_statuses"),84,0,255) or not _vector(row.get("equipped_skills"),8,0,84):
			return false
		encoded += _encode([row["member_id"]]+row["growth_pools"]+row["skill_statuses"]+row["equipped_skills"])+";"
	if not _vector(rules.get("level_thresholds"),50,0,2147483647) or not _vector(rules.get("learned_points"),84,0,2147483647):
		return false
	encoded += "|"+_encode(rules["level_thresholds"])+"|"+_encode(rules["learned_points"])
	return encoded.sha256_text() == ORIGIN_SHA


static func group_rules() -> Dictionary:
	return {"source_image_sha256":SOURCE_SHA,"teacher_scope":"new_game_initializer",
		"initializer_va":0x49E930,"origin_fields_sha256":ORIGIN_SHA,"relationship_thresholds":[16,31,46,61,76,91]}


static func source_subset(rules: Dictionary) -> Dictionary:
	var result := {}
	var row_fields := {"calls":["call_va","member_id","group","slot"],
		"member_profiles":["member_id","job","level_50","attributes","storage_kind","template_sha256"],
		"relationships":["from","to","value"],
		"student_level_inputs":["member_id","growth_pools","skill_statuses","equipped_skills"]}
	for key in RULE_KEYS:
		if rules.has(key):
			if row_fields.has(key) and rules[key] is Array:
				var rows := []
				for row in rules[key]:
					rows.append(field_subset(row,row_fields[key]) if row is Dictionary else row)
				result[key] = rows
			else:
				result[key] = rules[key].duplicate(true) if rules[key] is Array or rules[key] is Dictionary else rules[key]
	return result


static func field_subset(row: Dictionary, keys: Array) -> Dictionary:
	var result := {}
	for key in keys:
		if row.has(key):
			result[key] = row[key].duplicate(true) if row[key] is Array or row[key] is Dictionary else row[key]
	return result


static func success(status: String) -> Dictionary:
	return {"supported":true,"status":status,"school_initialized":false,"interactive_school_ready":false,
		"live_witness":false,"authorizes_persistent_write":false}


static func failure(reason: String) -> Dictionary:
	var result := success("refused")
	result["supported"] = false
	result["reason"] = reason
	return result
