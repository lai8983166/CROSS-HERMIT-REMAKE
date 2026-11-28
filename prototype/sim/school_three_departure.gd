extends RefCounted
## The verified April week-three native school checkpoint, read without changing it.
const SAVE_SHA := "cf37a6c6854b4dcb4df461418aa07c0dd0276ee96668a941bc8efee332797cd6"
const SCENE := {"scene_id":3,"configuration_hex":"03000000000114045b0000000000000514050a0f0101010b0b0b00000000000000000000000000000000","script_sha256":"b119aa40130d837edd43e9b67c2d0e9d7f186004daa596f43e1f3f7c6f06c5cb"}
const BASE := 0x7a50e8

static func load_save(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):return {}
	var raw := FileAccess.get_file_as_bytes(path)
	var digest := HashingContext.new()
	digest.start(HashingContext.HASH_SHA256)
	digest.update(raw)
	if digest.finish().hex_encode()!=SAVE_SHA:return {}
	if raw.decode_u16(0)!=7 or raw.decode_u16(0x1a6)!=4 or raw.decode_u16(0x1a8)!=3 or raw.decode_s16(0x7aab16-BASE)!=3:return {}
	var teachers := []
	var students := []
	var members := []
	for group in range(5):
		var record := 0x7aaa12-BASE+28*group
		teachers.append(raw.decode_s16(record))
		var group_members := [teachers.back()-55]
		for slot in range(raw[record+14]):
			group_members.append(raw.decode_s16(record+16+2*slot))
		var relationship_sum := 0
		for a in group_members:
			for b in group_members:
				if a!=b:relationship_sum+=raw[0x7d3d71-BASE+a*68+b]
		var group_bonus := relationship_sum/(group_members.size()*(group_members.size()-1))
		for slot in range(raw[record+14]):
			var id := raw.decode_s16(record+16+2*slot)
			var role := 0x7bc6ac-BASE+id*0x4a0
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
	return {"date":[4,3],"supported":true,"ready":true,"requested_states":[10,16],"round_cursor":1,
		"native_sha256":SAVE_SHA,"initial_total":raw.decode_s32(0x7a511c-BASE),"initial_grade":raw[0x7a54ca-BASE+3],"participants":members,"growth":members.duplicate(true),"scene":SCENE,
		"prepared":{"adventure_id":3,"round_count":1,"round_index":0,
			"rounds":[{"scene_id":3,"student_ids":students,"teacher_ids":teachers}]}}

static func score(handoff: Dictionary, facts: Dictionary) -> Dictionary:
	const Battle := preload("res://sim/school_battle_settlement.gd")
	var tables := {}
	for key in Battle.SOURCES:
		var source: Array=Battle.SOURCES[key]
		var raw := FileAccess.get_file_as_string(source[0]).replace("\r\n","\n")
		if raw.sha256_text()!=source[1]:return {}
		tables[key]=Battle.Roles._integers(JSON.parse_string(raw).rules)
	var rules: Dictionary=tables.preparation.score.duplicate(true)
	# Mission 3 row, 73BEF4 + 3*100h through 73BF1B + 3*100h.
	rules.merge({"task_id":3,"base_points":[36000,34000,32000,21000,14000],
		"unit_bonus":110,"time_bonuses":[115,110,105],"count_bonuses":[100,100,100,100,100,0]},true)
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
	return Battle.Score.calculate({"task_id":3,"mode":0,"cap_mode":0,"result_selector":facts.result_selector,
		"time_key":facts.time_key,"unit_key":facts.unit_condition_key,"initial_grade":handoff.initial_grade,
		"initial_total":handoff.initial_total,"characters":characters},rules)
