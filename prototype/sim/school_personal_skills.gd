extends RefCounted
## 4AE370 drags a learned skill into a current-job slot. 4B66F0 refreshes
## item availability and the remaining 84 skill statuses for that student.
const Job := preload("res://sim/school_job_eligibility.gd")
const Return := preload("res://sim/school_postbattle_return.gd")
const SHA := "28663fe9659cebbbff20934116e864890e121ce8dc31d039a4967884257db85e"
const COMMAND_SKILLS := [11,20,31,57,59]
static var _catalog: Dictionary={}
static var _job_rules: Dictionary={}


static func rules() -> Dictionary:
	if _catalog.is_empty():
		var raw:=FileAccess.get_file_as_string("res://data/school_personal_skills.json").replace(String.chr(13),"")
		if raw.sha256_text()==SHA:_catalog=Return.Roles._integers(JSON.parse_string(raw))
	return _catalog


static func skill_name(skill:int) -> String:
	if skill==29:return "復原" # Equipped in the starting roster. SKILLEXP.YBC +2108h.
	return rules().get("names",{}).get(str(skill),"")


static func slot_count(job:int) -> int:
	var source:=rules()
	return source.slots[job] if job>=1 and job<=30 and not source.is_empty() else 0


static func _equipment_rules() -> Dictionary:
	if _job_rules.is_empty():_job_rules=Job.equipment_rules()
	return _job_rules


static func _refresh_skills(student: Dictionary, permitted: Dictionary) -> void:
	var source:=rules()
	var used: Array=[]
	for current in student.equipped_skills.slice(0,slot_count(student.job)):
		if current!=0:used.append(source.families[current])
	for i in student.skill_statuses.size():
		var status:int=student.skill_statuses[i]
		if status not in [2,3,4,5]:continue
		var incompatible:int=source.incompatible[source.families[i+1]]
		var usable:bool=i+1 in permitted.skills and incompatible not in used
		student.skill_statuses[i]=2+status%2+(0 if usable else 2)


static func available(student: Dictionary) -> Array:
	var choices: Array=[]
	if student.get("skill_statuses",[]).size()!=84 or student.get("equipped_skills",[]).size()!=8 or slot_count(student.get("job",0))==0:return choices
	var equipment:=_equipment_rules()
	if equipment.is_empty():return choices
	var preview:=student.duplicate(true)
	_refresh_skills(preview,equipment.classes[student.job-1])
	for skill in COMMAND_SKILLS:
		if preview.skill_statuses[skill-1]==3:choices.append(skill)
	return choices


static func equip(before: Dictionary,member:int,skill:int,slot:int) -> Dictionary:
	if before.get("phase")!="school_returned":return {"supported":false,"reason":"skill_requires_returned_school"}
	var reason:=Return.validate_planning_roster(before,Return._rules())
	if not reason.is_empty():return {"supported":false,"reason":reason}
	var index:int=before.school.student_ids.slice(0,before.school.student_count).find(member)
	if index<0:return {"supported":false,"reason":"unknown_skill_student"}
	var student:Dictionary=before.participants[index]
	if slot<0 or slot>=slot_count(student.job) or skill not in COMMAND_SKILLS:
		return {"supported":false,"reason":"invalid_skill_slot"}
	if student.equipped_skills[slot]==skill:return Return._result(before,"duplicate")
	if skill not in available(student):return {"supported":false,"reason":"skill_not_available"}
	var job_rules:=_equipment_rules()
	if job_rules.is_empty():return {"supported":false,"reason":"invalid_skill_rules"}
	var after:=before.duplicate(true)
	var changed:Dictionary=after.participants[index]
	var previous:int=changed.equipped_skills[slot]
	if previous!=0:changed.skill_statuses[previous-1]=3
	changed.equipped_skills[slot]=skill
	changed.skill_statuses[skill-1]=6
	var permitted:Dictionary=job_rules.classes[changed.job-1]
	_refresh_skills(changed,permitted)
	for i in after.item_flags.size():
		var flags:int=after.item_flags[i]
		var kind: int=(flags>>8)&15
		if kind not in [1,2,3,4]:continue
		var item:Array=job_rules.items[i]
		var allowed:bool=changed.level_50>=item[1] and item[0] in permitted.item_types
		var next_kind: int=(1 if kind<=2 else 3)+(0 if allowed else 1)
		after.item_flags[i]=(flags&0xf0ff)|(next_kind<<8)
	after.growth[index].skill_statuses=changed.skill_statuses.duplicate()
	return Return._result(after,"skill_equipped")
