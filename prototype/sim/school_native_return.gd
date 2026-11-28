extends RefCounted
## Remake campaign state decoded from an original v7 school, kept separate from the .SAV.
const Native := preload("res://sim/school_native_departure.gd")
const Courses := preload("res://sim/school_return_courses.gd")
const Battle := preload("res://sim/school_battle_settlement.gd")
const Ledger := preload("res://sim/school_return_adventures.gd")
const Week := preload("res://sim/week_settlement_replay.gd")
const REWARDS := "res://data/school_native_april_rewards.json"
const REWARD_SHA := "588a6bb4d395ce88e4adc3c55a0f73894baf51381c469b8f3b4d0f3e4446826c"

static func _array(raw: PackedByteArray, start: int, count: int, step: int, kind: String) -> Array:
	var values := []
	for i in range(count):
		var at := start+i*step
		match kind:
			"byte": values.append(int(raw[at]))
			"sbyte": values.append(raw.decode_s8(at))
			"word": values.append(raw.decode_u16(at))
			"short": values.append(raw.decode_s16(at))
			"int": values.append(raw.decode_s32(at))
	return values


static func from_save(raw: PackedByteArray) -> Dictionary:
	var handoff := Native.decode(raw)
	if handoff.is_empty():return {}
	var count := raw.decode_s16(0x178)
	var roster := _array(raw,0x128,count,2,"short")
	var faculty := _array(raw,0x7a5262-Native.BASE,raw.decode_s16(0x7a528a-Native.BASE),2,"short")
	var school := {"month":4,"week":handoff.date[1],"student_count":count,"student_ids":roster,"relationships":[]}
	for id in roster+faculty:
		for other in roster+faculty:
			if id==other:continue
			var a: int=id-55 if id>100 else id
			var b: int=other-55 if other>100 else other
			school.relationships.append({"from":id,"to":other,"value":int(raw[0x7d3d71-Native.BASE+a*68+b])})
	var state := {"school":school,"members":{},"classes":[],"grades":_array(raw,0x7a54ca-Native.BASE+1,100,1,"byte"),
		"score":handoff.initial_total,"availability":_array(raw,0x7a5120-Native.BASE,45,1,"byte"),
		"item_flags":_array(raw,0x7aacac-Native.BASE,360,2,"word"),"origin_sha":handoff.native_sha256,
		"ledger":{"entries":[],"unlock_flags":_array(raw,0x7a55fc-Native.BASE+1,100,1,"byte")} }
	for i in range(raw.decode_s16(0x7a5b62-Native.BASE)):
		var pos := 0x7a5662-Native.BASE+16*i
		state.ledger.entries.append({"id":raw.decode_s16(pos),"metadata":_array(raw,pos+3,3,1,"byte"),
			"busy":int(raw[pos+6]),"limit":raw.decode_s16(pos+8),"duration":raw.decode_s16(pos+10),
			"busy_elapsed":raw.decode_s16(pos+12),"elapsed":raw.decode_s16(pos+14)})
	for group in range(5):
		var row := 0x7aaa12-Native.BASE+28*group
		var teacher := raw.decode_s16(row)
		if teacher<0:continue
		var students := _array(raw,row+16,4,2,"short").filter(func(id):return id>=0)
		state.classes.append({"group":group,"teacher":teacher,"students":students,"activity":2 if raw[row+3]==0 else 1,
			"work_fields":_array(raw,row+6,4,2,"short")})
	for id in roster:
		var role: int=0x7bc6ac-Native.BASE+id*0x4a0
		var pack: int=0x7cf34c-Native.BASE+id*0x124
		state.members[id]={"character_id":id,"job":raw.decode_s16(role+6),"level_50":int(raw[role+0x50]),
			"attributes":_array(raw,role+12,7,8,"byte"),"growth_pools":_array(raw,role+16,7,8,"int"),
			"equipped_skills":_array(raw,role+0x52,8,2,"short"),"equipped_items":_array(raw,role+0x62,8,2,"short"),
			"skill_statuses":_array(raw,role+0xb8,84,12,"byte"),"job_progress":_array(raw,pack+0xd7,31,1,"sbyte"),
			"unlock_flags":_array(raw,pack+0xf9,30,1,"byte"),"week_records":_array(raw,pack+0x24,177,1,"byte"),
			"job_sums":[0,0,0,0,0],"mvp_count":raw.decode_s16(pack+0x120)}
	return state


static func handoff(state: Dictionary) -> Dictionary:
	var sid: int=state.school.week
	if not Native.SCENES.has(sid) or not Ledger.available(state.ledger).any(func(r):return r.id==sid):return {}
	var teachers := []
	var members := []
	var ids := []
	var pairs := {}
	for row in state.school.relationships:pairs[Vector2i(row.from,row.to)]=row.value
	for group in state.classes:
		if group.activity!=2:continue
		teachers.append(group.teacher)
		var people: Array=group.students+[group.teacher]
		var total := 0
		for a in people:
			for b in people:
				if a!=b:total+=int(pairs[Vector2i(a,b)])
		var bonus: int=total/(people.size()*(people.size()-1))
		for id in group.students:
			var member: Dictionary=state.members[id].duplicate(true)
			member.group_bonus=bonus
			members.append(member)
			ids.append(id)
	if ids.is_empty():return {}
	return {"date":[4,sid],"supported":true,"ready":true,"requested_states":[10,16],"round_cursor":1,
		"native_sha256":state.origin_sha,"initial_total":state.score,"initial_grade":state.grades[sid-1],"participants":members,
		"growth":members.duplicate(true),"scene":Native.SCENES[sid],"prepared":{"adventure_id":sid,"round_count":1,
		"round_index":0,"rounds":[{"scene_id":sid,"student_ids":ids,"teacher_ids":teachers}]}}


static func settle(before: Dictionary, sortie: Dictionary, facts: Dictionary, score: Dictionary) -> Dictionary:
	var sid: int=before.school.week
	if sortie.date!=[4,sid] or not score.get("supported",false) or facts.get("scene_id")!=sid:return {}
	var catalog := FileAccess.get_file_as_string(REWARDS).replace("\r\n","\n")
	if catalog.sha256_text()!=REWARD_SHA:return {}
	var rules := Courses._rules()
	if rules.is_empty():return {}
	var state := before.duplicate(true)
	var packages := {}
	for row in score.characters:packages[row.character_id]=row
	var rng: int=facts.growth_seed
	var best := 0
	var mvp := -1
	var changes := []
	for group in state.classes:
		var rows := []
		for id in group.students:
			var record: Dictionary=state.members[id].duplicate(true)
			record.merge(packages[id],true)
			rows.append(record)
		var growth := Battle.Roles.project_growth_records(rows,group.students,rng,rules.role,false,false,false,false,true)
		if not growth.supported:return {}
		rng=growth.rand_state
		for record in growth.after.characters:
			var id: int=record.character_id
			var old: Dictionary=state.members[id]
			changes.append({"id":id,"before_level":old.level_50,"level":record.level_50,"staged_total":record.staged_total})
			for key in ["attributes","growth_pools","level_50","skill_statuses","job_sums"]:old[key]=record[key]
			if id<13 and record.staged_total>best:
				mvp=id
				best=record.staged_total
	var preparation := Battle.SOURCES.preparation
	var input := FileAccess.get_file_as_string(preparation[0]).replace("\r\n","\n")
	if input.sha256_text()!=preparation[1]:return {}
	var loot_rules: Dictionary=Battle.Roles._integers(JSON.parse_string(input).rules)
	loot_rules.merge(Battle.Roles._integers(JSON.parse_string(catalog).missions[str(sid)]),true)
	var loot := Battle.Loot._loot(state.item_flags,score.grade_index,facts,loot_rules)
	state.item_flags=loot.item_flags
	var working := {"school":state.school,"growth":state.members.values(),"records":state.members.values()}
	for group in state.classes:group.work_fields=[3,sid-1,sid,0]
	Courses._confirm(working,state.classes,rules.confirmation.job_categories,2)
	var ids: Array=sortie.prepared.rounds[0].student_ids
	var teachers: Array=sortie.prepared.rounds[0].teacher_ids
	var delta: int=Battle.Confirmation.GRADE_DELTA[score.grade_index]
	var calls := []
	for id in ids:
		for other in ids:
			if id!=other:calls.append({"from":id,"to":other,"delta":delta})
		for teacher in teachers:
			calls.append({"from":id,"to":teacher,"delta":delta})
			calls.append({"from":teacher,"to":id,"delta":delta})
	Courses._apply_relationships(working,calls)
	if mvp>=0:state.members[mvp].mvp_count=mini(5,state.members[mvp].mvp_count+1)
	var week := Week.project({"month":4,"week":sid,"participants":state.members.values(),"availability":state.availability,
		"item_flags":state.item_flags,"flags":{"0x7a55fa":1,"0x7a4e62":0,"0x7a55f6":0,"0x7e11a0":0}},rules.week,true)
	if not week.supported:return {}
	for updated in week.after.participants:state.members[updated.character_id].merge(updated,true)
	state.item_flags=week.after.item_flags
	state.school.week=week.after.week
	state.score=score.total_after
	state.grades[sid-1]=score.task_grade
	state.ledger=Ledger.advance(state.ledger,sid)
	Ledger._open(state.ledger,4,state.school.week,Ledger.rules())
	state["last_result"]={"scene":sid,"grade":score.grade_index+1,"experience":score.total_delta,
		"mvp":mvp,"changes":changes,"loot":loot.loot_groups}
	return state
