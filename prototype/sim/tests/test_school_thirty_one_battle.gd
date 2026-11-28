extends "res://sim/tests/test_base.gd"
const Record := preload("res://sim/school_sortie_record.gd")
const Helper := preload("res://sim/tests/test_school_sortie_session.gd")


func _handoff() -> Dictionary:
	var h:=Helper.new().handoff(17)
	h.date=[12,1]
	h.scene=Record.Sortie.Adventures.mission_rules(31).scene
	h.prepared.adventure_id=31
	h.prepared.rounds[0].scene_id=31
	h.prepared.rounds[0].student_ids.erase(4)
	h.participants=h.participants.filter(func(p):return p.character_id!=4)
	h.growth=h.growth.filter(func(p):return p.character_id!=4)
	return h


func test_map31_grade_priority_and_timers() -> void:
	var s:=Record.Sortie.new()
	assert_true(s.open(_handoff()))
	if not s.ready:return
	assert_eq([s.field_width,s.field_height,s.reserves.size(),s.opening_snapshot().page_count],[96,96,84,6])
	for i in 6:assert_true(s.advance_opening(true))
	var mission=s.siege
	assert_eq(mission.slots,{0:{"sub":20,"due":18000},1:{"sub":21,"due":10800},2:{"sub":22,"due":21600},3:{"sub":23,"due":21600}})
	for sub in [20,21,22,23]:
		mission.slots={0:{"sub":sub,"due":10}}
		s.elapsed=10
		mission.advance(s)
		assert_eq(mission.slots[0].sub,sub)
		assert_true(s.units.any(func(u):return u.source_state==1 and u.get("group",0) in mission.waves[sub].groups))
	for row in [[[1,1,1],3,0,2],[[1,1,1],3,1,5],[[2,1,1],3,0,8],[[3,4,1],3,0,8],[[2,3,4],0,0,11],[[1,1,1],2,0,14]]:
		for i in 3:
			var escort:Dictionary=mission.protectees[i]
			escort.source_state=row[0][i]
			escort.cell=Vector2i(10,87) if i<row[1] else Vector2i(77,51)
		for id in s._participant_ids:s.find_unit(id).source_state=4
		s._own_casualties=row[2]
		assert_eq(mission.result(s),row[3])
	s.close()


func test_escort_controls_and_trace_bounds() -> void:
	var panel=preload("res://ui/school_sortie_trial.gd").new()
	Engine.get_main_loop().root.add_child(panel)
	assert_true(panel.open_trial(_handoff(),{},{}))
	if panel.session.ready:
		var s=panel.session
		assert_eq(panel.canvas.texture.get_size(),Vector2(3072,1536))
		for i in 6:s.advance_opening(true)
		for id in Record.Sortie.ThirtyOne.ESCORTS:
			assert_true(panel.targets.get_item_index(id)>=0)
			panel.member_buttons[s.find_unit(id).character_id].pressed.emit()
			assert_eq(s.selected_id,id)
			assert_true(s.stop(id))
			assert_false(s.command_attack(id,1234))
		assert_true(Record.valid_trace(s.battle_trace(),[12,1],31))
		for row in [[0,2],[0,3,4,10,87],[0,3,1235,96,80],[0,3,1236,95,96],[0,4,1235,1234]]:
			var invalid:Dictionary=s.battle_trace().duplicate(true)
			invalid.commands=[row]
			assert_false(Record.valid_trace(invalid,[12,1],31))
	panel.free()
