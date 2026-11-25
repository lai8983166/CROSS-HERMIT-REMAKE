extends RefCounted
## The personal screen offers fifteen cells. The weekly settlement owns the
## persistent thirty unlock bits, and the character variant selects each pair.
const SOURCE := "res://data/school_job_menu.json"


static func menu_data() -> Dictionary:
	var raw := FileAccess.get_file_as_string(SOURCE).replace("\r\n","\n")
	if raw.sha256_text()!=MENU_SHA:return {}
	return JSON.parse_string(raw)


static func calculate_eligibility(student: Dictionary, menu: Dictionary) -> Array:
	var member: int=student.get("character_id",0)
	if menu.is_empty() or member<=0 or member>=menu.member_variants.size() or student.get("unlock_flags",[]).size()!=30:
		return []
	var variant: int=menu.member_variants[member]
	if variant not in [1,2]:return []
	var jobs := []
	for base in menu.grid:
		var job: int=int(base)+variant-1
		if student.unlock_flags[job-1]==1:jobs.append(job)
	return jobs


const MENU_SHA := "e3f3eb8596295d54a26b892c6495114ddeccf34421bb3fdb18af98c8eedf237f"
const CHANGE_SHA := "0049238b77eefe79402de53bd300fcde14252ec7d3669f0405c234d1463ff848"
const Return := preload("res://sim/school_postbattle_return.gd")


static func equipment_rules() -> Dictionary:
	var raw := FileAccess.get_file_as_string("res://data/school_job_change.json").replace("\r\n","\n")
	if raw.sha256_text()!=CHANGE_SHA:return {}
	return Return.Roles._integers(JSON.parse_string(raw))


static func apply_equipment(student: Dictionary, item_flags: Array, job: int, rules: Dictionary) -> void:
	var allowed: Dictionary=rules.classes[job-1]
	student.job=job
	for slot in range(8):
		var skill: int=student.equipped_skills[slot]
		if skill>0:
			student.skill_statuses[skill-1]=3
			student.equipped_skills[slot]=0
		var item: int=student.equipped_items[slot]
		if item>0:
			item_flags[item-1]=(int(item_flags[item-1]) & 0xf0ff) | 0x100
			student.equipped_items[slot]=0
	for i in range(item_flags.size()):
		var flags: int=item_flags[i]
		var kind := (flags >> 8) & 15
		if kind not in [1,2,3,4]:continue
		var row: Array=rules.items[i]
		var permitted: bool=student.level_50>=row[1] and row[0] in allowed.item_types
		var new_kind := (1 if kind<=2 else 3) + int(not permitted)
		item_flags[i]=(flags & 0xf0ff) | (new_kind << 8)
	for i in range(student.skill_statuses.size()):
		var status: int=student.skill_statuses[i]
		if status in [2,3,4,5]:
			var usable := 2 + (status%2)
			student.skill_statuses[i]=usable if i+1 in allowed.skills else usable+2


static func change_job(before: Dictionary, member: int, job: int) -> Dictionary:
	if before.get("phase")!="school_returned" or before.school.month<10:
		return {"supported":false,"reason":"job_change_requires_returned_school"}
	var school_rules := Return._rules()
	var reason := Return.validate_planning_roster(before,school_rules)
	if not reason.is_empty():return {"supported":false,"reason":reason}
	var index: int=before.school.student_ids.slice(0,before.school.student_count).find(member)
	if index<0:return {"supported":false,"reason":"unknown_job_change_student"}
	var student: Dictionary=before.participants[index]
	if job not in calculate_eligibility(student,menu_data()):
		return {"supported":false,"reason":"job_not_unlocked"}
	if student.job==job:return Return._result(before,"duplicate")
	var rules := equipment_rules()
	if rules.is_empty():return {"supported":false,"reason":"invalid_job_equipment_source"}
	var after := before.duplicate(true)
	var changed: Dictionary=after.participants[index]
	apply_equipment(changed,after.item_flags,job,rules)
	after.growth[index].job=job
	after.growth[index].skill_statuses=changed.skill_statuses.duplicate()
	for profile in after.school.member_profiles:
		if profile.member_id==member:profile.job=job
	var prepared := Return._prepare(after.school,school_rules)
	if not prepared.supported:return prepared
	after.school=prepared.after
	after.ratings=prepared.ratings
	after.rankings=Return._rankings(after.school)
	return Return._result(after,"job_changed")
