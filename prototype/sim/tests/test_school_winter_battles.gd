extends "res://sim/tests/test_base.gd"
const Record := preload("res://sim/school_sortie_record.gd")
const Helper := preload("res://sim/tests/test_school_sortie_session.gd")
const Winter := Record.Sortie.Winter


func _opening(id:int) -> Dictionary:
	var h:=Helper.new().handoff(17)
	h.date=Winter.DATES[id]
	h.scene=Winter.mission_rules(id).scene
	h.prepared.adventure_id=id
	h.prepared.rounds[0].scene_id=id
	if id==32:
		h.prepared.rounds[0].student_ids.erase(4)
		h.participants=h.participants.filter(func(u):return u.character_id!=4)
		h.growth=h.growth.filter(func(u):return u.character_id!=4)
	return h


func test_winter_mission_identity_commands_and_objectives() -> void:
	for id in Winter.DATES:
		var s:=Record.Sortie.new()
		assert_true(s.open(_opening(id)),"winter opening %d" % id)
		if not s.ready:continue
		assert_eq(Vector2i(s.field_width,s.field_height),Winter.MAP_SIZE[id])
		assert_eq(s.reserves.size(),Winter.TEMPLATES[id])
		while s._ending_phase=="opening":assert_true(s.advance_opening(true))
		var trace:=s.battle_trace()
		assert_true(Record.valid_trace(trace,Winter.DATES[id],id))
		assert_false(Record.valid_trace(trace,[15,5],id))
		var invalid:=trace.duplicate(true)
		invalid.commands.append([0,3,3,s.field_width,0])
		assert_false(Record.valid_trace(invalid,Winter.DATES[id],id))
		s.tick()
		assert_eq(s._ending_phase,"active")
		match id:
			32:
				assert_eq(s.siege.slots.size(),7)
				s.remaining_ticks=0
				assert_eq(s.siege.result(s),2)
				s.find_unit(1247).side=5
				assert_eq(s.siege.result(s),8)
				for n in Winter.OBJECTS[id]:s.find_unit(1250-n).side=5
				assert_eq(s.siege.result(s),11)
			44:
				assert_eq(s.siege.slots.size(),13)
				s.remaining_ticks=0
				assert_eq(s.siege.result(s),11)
				s.find_unit(1249).source_state=4
				assert_eq(s.siege.result(s),8)
			29:
				for n in Winter.OBJECTS[id]:s.find_unit(1250-n).side=0
				assert_eq(s.siege.result(s),2)
				s.find_unit(1230).source_state=3
				assert_eq(s.siege.result(s),8)
				s.find_unit(1231).source_state=2
				assert_eq(s.siege.result(s),11)
				s.find_unit(1249).source_state=4
				assert_eq(s.siege.result(s),14)
			45:
				assert_true(s.find_unit(1248).is_empty())
				var boss:=s.find_unit(1249)
				boss.source_state=4
				boss.limits.hp=0
				assert_eq(s.siege.result(s),-1)
				assert_eq(s.find_unit(1248).cell,Vector2i(12,27))
				s.find_unit(1248).source_state=4
				assert_eq(s.siege.result(s),8)
		s.close()


func test_winter_panels_read_the_original_maps_and_skinned_units() -> void:
	var panel=preload("res://ui/school_sortie_trial.gd").new()
	Engine.get_main_loop().root.add_child(panel)
	for id in Winter.DATES:
		assert_true(panel.open_trial(_opening(id),{},{}),"winter panel %d" % id)
		if not panel.session.ready:continue
		assert_eq(panel.canvas.texture.get_size(),Vector2(Winter.MAP_SIZE[id]*Vector2i(32,16)))
		assert_true(panel.targets.get_item_index(1249)>=0)
		while panel.session._ending_phase=="opening":panel.session.advance_opening(true)
		if id in [44,45]:
			assert_true(panel._command_cell(panel.session.find_unit(1249).cell))
			assert_eq(panel.session.battle_trace().commands.back()[1],4)
	panel.free()


func test_promoted_members_and_original_attack_timing() -> void:
	var h:=_opening(29)
	var p:Dictionary=h.participants.filter(func(u):return u.character_id==4)[0]
	var growth:Dictionary=h.growth.filter(func(u):return u.character_id==4)[0]
	p.job=16
	growth.job=16
	p.equipped_skills.fill(0)
	p.unlock_flags.resize(30)
	p.unlock_flags.fill(0)
	var s:=Record.Sortie.new()
	assert_false(s.open(h))
	p.unlock_flags[15]=1
	assert_true(s.open(h))
	if not s.ready:return
	while s._ending_phase=="opening":s.advance_opening(true)
	var hunter:=s.find_unit(4)
	assert_eq(hunter.job,16)
	assert_true(hunter.skin_key.begins_with("job16_v"))
	assert_true(s.catalog.skins[hunter.skin_key].actions.has("basic_attack"))
	var summoner:=s.find_unit(1219)
	s._start_attack(summoner,hunter)
	assert_eq(s.phases[1219].deadline-s.frame,75)
	assert_eq(s.phases[1219].recover_frames,1)
	s._start_attack(hunter,summoner)
	assert_eq(s.phases[4].deadline-s.frame,1)
	assert_eq(s.phases[4].recover_frames,ceili(hunter.combat.cast_ticks/2.0))
	s.close()


func test_original_learned_skill_equips_and_winter_caster_replays() -> void:
	var personal=preload("res://sim/school_personal_skills.gd")
	var before:Dictionary=Helper.Helpers.new()._returned()
	var idx:int=before.school.student_ids.find(3)
	var p:Dictionary=before.participants[idx]
	var slot:int=p.equipped_skills.find(57)
	assert_true(slot>=0)
	if slot<0:return
	p.equipped_skills[slot]=0
	p.skill_statuses[56]=3
	before.growth[idx].skill_statuses=p.skill_statuses.duplicate()
	assert_true(57 in personal.available(p))
	assert_eq(personal.slot_count(10),6)
	assert_eq(personal.skill_name(57),"氣流障壁")
	assert_false(personal.equip(before,3,57,6).supported)
	var result:Dictionary=personal.equip(before,3,57,slot)
	assert_true(result.supported,str(result.get("reason","")))
	if not result.supported:return
	assert_eq(result.after.participants[idx].equipped_skills[slot],57)
	assert_eq(result.after.growth[idx].skill_statuses[56],6)
	assert_eq(before.participants[idx].skill_statuses[56],3)
	var session:=Record.Sortie.new()
	var h:=_opening(29)
	var knight:Dictionary=h.participants.filter(func(u):return u.character_id==5)[0]
	knight.equipped_skills[1]=57
	knight.skill_statuses[56]=6
	h.growth.filter(func(u):return u.character_id==5)[0].skill_statuses=knight.skill_statuses.duplicate()
	assert_true(session.open(h))
	if not session.ready:return
	while session._ending_phase=="opening":session.advance_opening(true)
	assert_true(session.cast_field_spell(5,session.find_unit(5).cell,57))
	assert_true(session.catalog.skins[session.find_unit(5).skin_key].actions.has("57_attack"))
	assert_true(Record.valid_trace(session.battle_trace(),Winter.DATES[29],29))
	assert_false(session.command_move(5,session.find_unit(5).cell))
	session.close()


func test_winter_attack_finishes_when_its_target_falls() -> void:
	var s:=Record.Sortie.new()
	assert_true(s.open(_opening(29)))
	if not s.ready:return
	while s._ending_phase=="opening":s.advance_opening(true)
	var giant:=s.find_unit(1222)
	var target:=s.find_unit(4)
	target.cell=giant.cell+Vector2i.DOWN
	target.limits.hp=1
	s._start_attack(giant,target)
	var release_duration:int=s.phases[1222].release_frames
	var recovery_duration:int=s.phases[1222].recover_frames
	while s.frame<s.phases[1222].deadline and s.phases[1222].stage=="cast":s.tick()
	assert_eq(target.limits.hp,0)
	assert_eq(s.phases[1222].stage,"attack")
	for i in release_duration:s.tick()
	assert_eq(s.phases[1222].stage,"recover")
	for i in recovery_duration-1:s.tick()
	assert_true(s.phases.has(1222))
	s.tick()
	assert_false(s.phases.has(1222))
	s.close()
