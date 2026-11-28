extends RefCounted
## Read the selected early-April sortie from a version-7 original school save.
const SCENES := {
	1:{"scene_id":1,"configuration_hex":"010000000001141f0e00000000000005ff0000000101010b0b0b00000000000000000000000000000000","script_sha256":"69b81351612650da1369c9597b80ec59610fab9f6e43a91a90c496b302475f72"},
	2:{"scene_id":2,"configuration_hex":"020000000001145b1000000000000005140a0f140101010f0f0f01020300000000000000000000000000","script_sha256":"810950ba5b22f2bc4a65654d47d4389986892deec5f9dc403bcbfb133606b81c"},
	3:{"scene_id":3,"configuration_hex":"03000000000114045b0000000000000514050a0f0101010b0b0b00000000000000000000000000000000","script_sha256":"b119aa40130d837edd43e9b67c2d0e9d7f186004daa596f43e1f3f7c6f06c5cb"}
}
const BASE := 0x7a50e8

static func load_save(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):return {}
	var file := FileAccess.open(path,FileAccess.READ)
	if file==null or file.get_length()!=0x306d4:return {}
	return decode(file.get_buffer(0x306d4))


static func decode(raw: PackedByteArray) -> Dictionary:
	if raw.size()!=0x306d4 or raw.decode_u16(0)!=7 or raw.decode_u32(4)>0x10002:return {}
	var checksum := 0
	for i in range(raw.size()):
		if i<44 or i>=48:checksum+=raw[i] if raw[i]<128 else raw[i]-256
	if checksum!=raw.decode_s32(44):return {}
	var week := raw.decode_s16(0x1a8)
	if not SCENES.has(week) or raw.decode_s16(0x1a6)!=4 or raw.decode_s16(0x7aab16-BASE)!=week:return {}
	if raw[0x7a55fc-BASE+week]!=1 or raw.decode_s16(0x7aab0a-BASE)==0:return {}
	var ledger_count := raw.decode_s16(0x7a5b62-BASE)
	if ledger_count<1 or ledger_count>80:return {}
	var available := false
	for i in range(ledger_count):
		var slot := 0x7a5662-BASE+16*i
		if raw.decode_s16(slot)!=week:continue
		var elapsed := raw.decode_s16(slot+14)
		if raw[slot+2]==1 and raw[slot+6]==0 and elapsed>=0 and elapsed<raw.decode_s16(slot+8):available=true
	if not available:return {}
	var roster := _roster(raw,0x128,raw.decode_s16(0x178),40,1,45)
	var faculty := _roster(raw,0x7a5262-BASE,raw.decode_s16(0x7a528a-BASE),20,101,120)
	if roster.is_empty() or faculty.is_empty():return {}
	var grade := raw[0x7a54ca-BASE+week]
	var total := raw.decode_s32(0x7a511c-BASE)
	if grade<1 or grade>5 or total<0 or total>999999999:return {}
	var digest := HashingContext.new()
	digest.start(HashingContext.HASH_SHA256)
	digest.update(raw)
	var source_sha := digest.finish().hex_encode()
	var teachers := []
	var students := []
	var members := []
	var assigned_teachers := []
	var assigned_students := []
	for group in range(5):
		var record := 0x7aaa12-BASE+28*group
		var teacher := raw.decode_s16(record)
		var group_students := []
		for slot in range(4):
			var student := raw.decode_s16(record+16+slot*2)
			if student==-1:continue
			if student not in roster or student in assigned_students:return {}
			group_students.append(student)
			assigned_students.append(student)
		if raw[record+14]!=group_students.size():return {}
		if teacher==-1:
			if not group_students.is_empty():return {}
			continue
		if teacher not in faculty or teacher in assigned_teachers or group_students.is_empty():return {}
		assigned_teachers.append(teacher)
		if raw[record+3]==1:
			if raw.decode_s16(record+8)<0:return {}
			continue
		if raw[record+3]!=0:return {}
		teachers.append(teacher)
		var group_members: Array=group_students.duplicate()
		group_members.append(teacher-55)
		var relationship_sum := 0
		for a in group_members:
			for b in group_members:
				if a!=b:relationship_sum+=raw[0x7d3d71-BASE+a*68+b]
		var group_bonus := relationship_sum/(group_members.size()*(group_members.size()-1))
		for id in group_students:
			var role: int=0x7bc6ac-BASE+id*0x4a0
			var member := {"character_id":id,"job":raw.decode_s16(role+6),"level_50":raw[role+0x50],
				"group_bonus":group_bonus,"attributes":[],"growth_pools":[],"equipped_skills":[],"equipped_items":[],"skill_statuses":[]}
			for i in range(7):
				member.attributes.append(raw[role+12+8*i])
				member.growth_pools.append(raw.decode_u32(role+16+8*i))
			for i in range(8):
				member.equipped_skills.append(raw.decode_s16(role+0x52+2*i))
				member.equipped_items.append(raw.decode_s16(role+0x62+2*i))
			for i in range(84):member.skill_statuses.append(raw[role+0xb8+12*i])
			members.append(member)
			students.append(id)
	if students.is_empty():return {}
	return {"date":[4,week],"supported":true,"ready":true,"requested_states":[10,16],"round_cursor":1,
		"native_sha256":source_sha,"initial_total":total,"initial_grade":grade,"participants":members,"growth":members.duplicate(true),"scene":SCENES[week],
		"prepared":{"adventure_id":week,"round_count":1,"round_index":0,
			"rounds":[{"scene_id":week,"student_ids":students,"teacher_ids":teachers}]}}

static func _roster(raw: PackedByteArray, offset: int, count: int, capacity: int, first: int, last: int) -> Array:
	var ids := []
	if count<1 or count>capacity:return []
	for i in range(count):
		var id := raw.decode_s16(offset+2*i)
		if id<first or id>last or id in ids:return []
		ids.append(id)
	return ids


static func score(handoff: Dictionary, facts: Dictionary) -> Dictionary:
	const Battle := preload("res://sim/school_battle_settlement.gd")
	var tables := {}
	for key in Battle.SOURCES:
		var source: Array=Battle.SOURCES[key]
		var raw := FileAccess.get_file_as_string(source[0]).replace("\r\n","\n")
		if raw.sha256_text()!=source[1]:return {}
		tables[key]=Battle.Roles._integers(JSON.parse_string(raw).rules)
	var sid: int=handoff.prepared.adventure_id
	var rules: Dictionary=tables.preparation.score.duplicate(true)
	# Mission rows at 73BEF4h + mission*100h through 73BF1Bh + mission*100h.
	var bases := {1:[20000,20000,18000,15000,12500],2:[36000,30000,24000,18000,12000],3:[36000,34000,32000,21000,14000]}
	rules.merge({"task_id":sid,"base_points":bases[sid],"unit_bonus":{1:0,2:120,3:110}[sid],
		"time_bonuses":[0,0,0] if sid==1 else [115,110,105],"count_bonuses":[100,100,100,100,100,0]},true)
	var characters := []
	for i in range(facts.units.size()):
		var member: Dictionary=handoff.participants[i]
		var row: Dictionary=facts.units[i].duplicate()
		if row.character_id!=member.character_id:return {}
		row.rate_class=tables.preparation.job_rate_classes[member.job]
		row.group_bonus=member.group_bonus
		row.growth_pools=member.growth_pools
		row.skill_points=0
		for j in range(84):
			if member.skill_statuses[j] in [3,5,6]:row.skill_points+=tables.role.skills[j].learned_points
		characters.append(row)
	return Battle.Score.calculate({"task_id":sid,"mode":0,"cap_mode":0,"result_selector":facts.result_selector,
		"time_key":facts.time_key,"unit_key":facts.unit_condition_key,"initial_grade":handoff.initial_grade,
		"initial_total":handoff.initial_total,"characters":characters},rules)
