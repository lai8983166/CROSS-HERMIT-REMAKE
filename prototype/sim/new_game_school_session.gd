extends RefCounted
## 新局学校数据会话；不重写旧返回会话，不读期望快照。

const Origin := preload("res://sim/new_game_school_origin.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")
const Courses := preload("res://sim/school_course_unlocking.gd")

var _origin_rules: Dictionary = {}
var _course_rules: Dictionary = {}
var _snapshot: Dictionary = {}
var _ratings: Array = []
var _journal: Array = []
var _revision := 0
var _prepared := false


func initialize(origin_rules: Dictionary, course_rules: Dictionary) -> Dictionary:
	var origin_source := Origin.source_subset(origin_rules)
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
		if _origin_rules != origin_source or _course_rules != course_source:
			return Origin.failure("school_origin_input_conflict")
		return _view("duplicate")
	var result := Origin.construct(origin_source)
	if not result["supported"]:
		return result
	if not Courses._rules_valid(course_source):
		return Origin.failure("unsupported_course_rules")
	_origin_rules = origin_source
	_course_rules = course_source
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
