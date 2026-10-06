extends RefCounted
## 新局学校数据会话；不重写旧返回会话，不读期望快照。

const Origin := preload("res://sim/new_game_school_origin.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")
const Courses := preload("res://sim/school_course_unlocking.gd")
const Student := preload("res://sim/school_student_movement.gd")
const Teacher := preload("res://sim/school_teacher_movement.gd")
const Sort := preload("res://sim/school_waitlist_sort.gd")
const CONTROLS := ["idle_sort_mode","teacher_sort_mode","drag_kind","drag_origin","drag_group",
	"drag_slot","drag_id","drag_source_rank","task_drag_state","task_command","teacher_work_records"]

var _origin_rules: Dictionary = {}
var _course_rules: Dictionary = {}
var _snapshot: Dictionary = {}
var _ratings: Array = []
var _journal: Array = []
var _revision := 0
var _prepared := false
var _movement_rules: Dictionary = {}


func initialize(origin_rules: Dictionary, course_rules: Dictionary, movement_rules: Dictionary = {}) -> Dictionary:
	var origin_source := Origin.source_subset(origin_rules)
	var movement_source := _movement_source(movement_rules)
	var course_source := {}
	for key in ["source_image_sha256","template_fields_sha256","templates"]:
		if course_rules.has(key):
			if key == "templates" and course_rules[key] is Array:
				var rows := []
				for row in course_rules[key]:
					rows.append(Origin.field_subset(row,["work_id","month","week","metadata","category","key","teacher_mask"]) if row is Dictionary else row)
				course_source[key] = rows
			else:
				course_source[key] = course_rules[key].duplicate(true) if course_rules[key] is Array or course_rules[key] is Dictionary else course_rules[key]
	if not _snapshot.is_empty():
		if _origin_rules != origin_source or _course_rules != course_source or _movement_rules != movement_source:
			return Origin.failure("school_origin_input_conflict")
		return _view("duplicate")
	var result := Origin.construct(origin_source)
	if not result["supported"]:
		return result
	if not Courses._rules_valid(course_source):
		return Origin.failure("unsupported_course_rules")
	if not movement_source.is_empty():
		var reason := _validate_movement_rules(result["after"],movement_source)
		if not reason.is_empty():
			return Origin.failure(reason)
	_origin_rules = origin_source
	_course_rules = course_source
	_movement_rules = movement_source
	_snapshot = result["after"].duplicate(true)
	_revision = 1
	_journal.append({"revision":1,"phase":"initialize","before":{},"after":read_snapshot()})
	return _view("initialized_once")


func prepare_school(expected_revision: Variant) -> Dictionary:
	if _snapshot.is_empty():
		return Origin.failure("missing_school_origin")
	if not Courses._integer(expected_revision,_revision,_revision):
		return Origin.failure("stale_school_revision")
	if _prepared:
		return _view("duplicate")
	var unlocked := Courses.unlock_courses(_snapshot,_course_rules)
	if not unlocked["supported"]:
		return unlocked
	var clean := Groups.reconcile(unlocked["after"],Origin.group_rules())
	if not clean["supported"]:
		return clean
	var rated := Groups.rate(clean["after"],Origin.group_rules())
	if not rated["supported"]:
		return rated
	# Calculate all phases first, then publish one revision. No partial state.
	var before := read_snapshot()
	_revision += 1
	for pair in [["unlock",unlocked],["reconcile",clean],["rate",rated]]:
		var after: Dictionary = pair[1]["after"].duplicate(true)
		_journal.append({"revision":_revision,"phase":pair[0],"before":before,"after":after})
		before = after.duplicate(true)
	_snapshot = rated["after"].duplicate(true)
	_ratings = rated["ratings"].duplicate(true)
	_prepared = true
	return _view("prepared_once")


func move_member(command: Dictionary, expected_revision: Variant) -> Dictionary:
	if not _prepared or _movement_rules.is_empty():
		return Origin.failure("school_movement_not_prepared")
	if not Courses._integer(expected_revision,_revision,_revision):
		return Origin.failure("stale_school_revision")
	for key in command:
		if key not in ["kind","member_id","target_group","target_slot"]:
			return Origin.failure("invalid_owned_move_command")
	var kind: Variant = command.get("kind")
	var identity: Variant = command.get("member_id")
	var target: Variant = command.get("target_group")
	var slot: Variant = command.get("target_slot",-1)
	if kind not in ["student","teacher"] or not Courses._integer(target,-1,4) \
			or not Courses._integer(slot,-1,3):
		return Origin.failure("invalid_owned_move_target")
	if (kind == "teacher" and (not Courses._integer(identity,101,101) or slot != -1)) \
			or (kind == "student" and (not Courses._integer(identity,1,12) \
			or (target == -1 and slot != -1) or (target >= 0 and slot < 0))):
		return Origin.failure("invalid_owned_move_member")
	var source := _locate(kind,int(identity))
	if source.is_empty():
		return Origin.failure("missing_owned_school_member")
	var working := _working(_snapshot)
	working["drag_kind"] = 1 if kind == "teacher" else 0
	working["drag_origin"] = 0 if source["group"] == -1 else 1
	working["drag_group"] = source["group"]
	working["drag_slot"] = source["slot"]
	working["drag_id"] = int(identity)
	working["drag_source_rank"] = _ratings[source["group"]]["relationship_rank"] if source["group"] >= 0 else 0
	var request := {"kind":kind,kind + "_id":int(identity),"source_group":source["group"],
		"source_slot":source["slot"],"target_group":int(target),"released":true}
	if kind == "student":
		request["target_slot"] = int(slot)
	var moved: Dictionary
	if kind == "teacher":
		moved = Teacher.move_teacher(working,request,_profiles(),Origin.group_rules(),_movement_rules["sort_rules"],_movement_rules["work_rules"])
	else:
		moved = Student.move_student(working,request,_profiles(),Origin.group_rules(),_movement_rules["sort_rules"])
	if not moved["supported"]:
		return moved
	var clean := Teacher.reconcile(moved["after"],Origin.group_rules(),_movement_rules["work_rules"])
	if not clean["supported"]:
		return clean
	var rated := Groups.rate(clean["after"],Origin.group_rules())
	if not rated["supported"]:
		return rated
	var final := _canonical(rated["after"])
	if final == _snapshot and rated["ratings"] == _ratings:
		return _view("duplicate")
	# Complete all native-equivalent calculations before publishing any state.
	_revision += 1
	var before := read_snapshot()
	for pair in [["movement",moved],["move_reconcile",clean],["move_rate",rated]]:
		var after := _canonical(pair[1]["after"])
		_journal.append({"revision":_revision,"phase":pair[0],"command":command.duplicate(true),
			"before":before,"after":after})
		before = after.duplicate(true)
	_snapshot = final
	_ratings = rated["ratings"].duplicate(true)
	return _view("member_moved")


func _locate(kind: String, identity: int) -> Dictionary:
	var waiting: Array = _snapshot["idle_teacher_ids" if kind == "teacher" else "idle_student_ids"]
	var index := waiting.find(identity)
	if index >= 0:
		return {"group":-1,"slot":index}
	for group in range(5):
		if kind == "teacher" and Groups._word(_snapshot["group_raw_bytes"],group * 28) == identity:
			return {"group":group,"slot":-1}
		if kind == "student":
			for slot in range(4):
				if Groups._word(_snapshot["group_raw_bytes"],group * 28 + 16 + slot * 2) == identity:
					return {"group":group,"slot":slot}
	return {}


func _profiles() -> Array:
	return _student_profiles(_snapshot)


static func _student_profiles(snapshot: Dictionary) -> Array:
	var result := []
	for row in snapshot["member_profiles"]:
		if row["member_id"] < 101:
			result.append({"character_id":row["member_id"],"job":row["job"],"level_50":row["level_50"],"attributes":row["attributes"].duplicate()})
	return result


static func _working(snapshot: Dictionary) -> Dictionary:
	var result := snapshot.duplicate(true)
	for key in CONTROLS:
		result[key] = -1
	result.merge({"idle_sort_mode":0,"teacher_sort_mode":0,"drag_source_rank":0,
		"task_drag_state":1,"task_command":14,"teacher_work_records":{"101":[]}},true)
	for row in snapshot["course_buffers"][0]:
		result["teacher_work_records"]["101"].append({"slot":row[0],"enabled":row[1],"blocked":row[2],"work_id":row[3]})
	return result


static func _canonical(snapshot: Dictionary) -> Dictionary:
	var result := snapshot.duplicate(true)
	for key in CONTROLS:
		result.erase(key)
	return result


static func _movement_source(input: Dictionary) -> Dictionary:
	if input.is_empty():
		return {}
	var result := {}
	if input.get("sort_rules") is Dictionary:
		result["sort_rules"] = Origin.field_subset(input["sort_rules"],["source_image_sha256","job_categories"])
	if input.get("work_rules") is Dictionary:
		var rules: Dictionary = input["work_rules"]
		var work := Origin.field_subset(rules,["source_image_sha256","template_fields_sha256","origin_fields_sha256"])
		for pair in [["templates",["work_id","category","sort_key"]],["teacher_profiles",["teacher_id","job","level_50","attributes"]]]:
			if rules.get(pair[0]) is Array:
				work[pair[0]] = []
				for row in rules[pair[0]]:
					work[pair[0]].append(Origin.field_subset(row,pair[1]) if row is Dictionary else row)
		result["work_rules"] = work
	# Preserve refusal for malformed nonempty inputs instead of silently disabling.
	return result if not result.is_empty() else {"invalid":true}


static func _validate_movement_rules(snapshot: Dictionary, rules: Dictionary) -> String:
	if not rules.get("sort_rules") is Dictionary or not rules.get("work_rules") is Dictionary:
		return "missing_owned_movement_rules"
	var sorted := Sort.order(_student_profiles(snapshot),[],0,rules["sort_rules"])
	if not sorted["supported"]:
		return sorted["reason"]
	var categories := PackedStringArray()
	for value in rules["sort_rules"]["job_categories"]:
		categories.append(str(value))
	if ":".join(categories).sha256_text() != "a611966c0b24eceda544383a0b64b1acb1df6866557c508175d396612933f411":
		return "owned_sort_source_mismatch"
	return Teacher._basic(_working(snapshot),Origin.group_rules(),rules["work_rules"])


func read_snapshot() -> Dictionary:
	return _snapshot.duplicate(true)


func revision() -> int:
	return _revision


func journal() -> Array:
	return _journal.duplicate(true)


func read_teacher_profile(identity: Variant) -> Dictionary:
	if not Courses._integer(identity,101,101) or _snapshot.is_empty():
		return Origin.failure("missing_source_teacher")
	for profile in _snapshot["member_profiles"]:
		if profile["member_id"] == identity:
			var result := Origin.success("source_teacher_profile")
			result["profile"] = profile.duplicate(true)
			return result
	return Origin.failure("missing_source_teacher")


func _view(status: String) -> Dictionary:
	var result := Origin.success(status)
	result["snapshot"] = read_snapshot()
	result["revision"] = _revision
	result["ratings"] = _ratings.duplicate(true)
	result["school_data_prepared"] = _prepared
	return result
