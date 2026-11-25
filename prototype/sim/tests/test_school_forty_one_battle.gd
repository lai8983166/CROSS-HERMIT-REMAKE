extends "res://sim/tests/test_base.gd"
const Record:=preload("res://sim/school_sortie_record.gd")
const Helper:=preload("res://sim/tests/test_school_sortie_session.gd")


func _handoff() -> Dictionary:
	var handoff:=Helper.new().handoff(17)
	handoff.date=[11,3]
	handoff.scene=Record.Sortie.Adventures.mission_rules(41).scene
	handoff.prepared.adventure_id=41
	handoff.prepared.rounds[0].scene_id=41
	return handoff


func test_objective_priority_and_reinforcement_schedules() -> void:
	var s:=Record.Sortie.new()
	assert_true(s.open(_handoff()))
	if not s.ready:return
	assert_eq([s.field_width,s.field_height,s.reserves.size(),s.opening_snapshot().page_count],[128,192,106,3])
	for i in 3:assert_true(s.advance_opening(true))
	var mission=s.siege
	assert_eq(mission.slots.size(),10)
	for sub in [20,21]:
		var wave:Dictionary=mission.waves[sub]
		assert_eq(wave.groups,[4,7,8,9,10,11,12,13,14,15] if sub==20 else [16,17,18,19,20])
		assert_eq(wave.delay,[900,7200 if sub==20 else 1800])
		mission.slots={0:{"sub":sub,"due":10}}
		s.elapsed=10
		mission.advance(s)
		assert_eq(mission.slots[0].sub,sub)
		assert_true(mission.slots[0].due in range(910,11+wave.delay[1]))
		assert_true(s.units.any(func(u):return u.source_state==1 and wave.groups.has(u.get("group",-1)) and u.get("source_ai_request",[]).size()==3))
	for row in [[4,0,0,0,true,2],[4,0,1,0,true,5],[4,5,0,0,true,8],[3,0,0,0,true,11],[1,0,0,1,true,14],[1,0,0,1,false,-1]]:
		s.find_unit(1249).source_state=row[0]
		s.find_unit(1248).side=row[1]
		s._own_casualties=row[2]
		s.remaining_ticks=row[3]
		for u in s.controlled_units():u.source_state=4 if row[4] else 1
		assert_eq(mission.result(s),row[5])
	s.close()


func test_record_bounds_and_actual_panel() -> void:
	var trace:Dictionary=Record.Sortie.Limits._source_numbers(JSON.parse_string(FileAccess.get_file_as_string("res://sim/tests/mandatory_forty_one_victory_trace.json")))
	assert_true(Record.valid_trace(trace,[11,3],41))
	assert_false(Record.valid_trace(trace,[9,4],41))
	for row in [[0,2],[0,3,2,0,0],[0,3,32,128,191],[0,3,32,127,192]]:
		var bad:=trace.duplicate(true)
		bad.commands=[row]
		assert_false(Record.valid_trace(bad,[11,3],41))
	var panel=preload("res://ui/school_sortie_trial.gd").new()
	Engine.get_main_loop().root.add_child(panel)
	assert_true(panel.open_trial(_handoff(),{},{}))
	if panel.session.ready:
		assert_eq(panel.canvas.texture.get_size(),Vector2(4096,3072))
		assert_true(panel.targets.get_item_index(1249)>=0)
	panel.free()
