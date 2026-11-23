extends "res://sim/tests/test_base.gd"
const Record:=preload("res://sim/school_sortie_record.gd")
const Helper:=preload("res://sim/tests/test_school_sortie_session.gd")


func _open():
	var h:=Helper.new().handoff(17)
	h.date=[9,4]
	h.scene=Record.Sortie.Adventures.twenty_four_rules().scene
	h.prepared.adventure_id=24
	h.prepared.rounds[0].scene_id=24
	var s:=Record.Sortie.new()
	assert_true(s.open(h))
	return s


func test_rescue_and_reinforcement_slots() -> void:
	var s=_open()
	if not s.ready:return
	assert_eq([s.field_width,s.field_height,s.opening_snapshot().page_count],[96,144,3])
	assert_eq(s.find_unit(1241).side,7)
	assert_true(s.find_unit(1194).is_empty())
	for i in 3:assert_true(s.advance_opening(true))
	var scout:Dictionary=s.find_unit(3)
	scout.cell=Vector2i(24,106)
	assert_true(s._detect_trial_end())
	assert_eq(s._event_pages.size(),37)
	for i in 37:assert_true(s.advance_event())
	assert_eq([s.find_unit(1241).side,s.find_unit(1240).side],[4,4])
	for id in [1194,1193]:assert_eq(s.find_unit(id).limits.hp,840)
	assert_eq(s.siege.slots.size(),7)
	s.elapsed=3600
	s.siege.advance(s)
	assert_eq(s.find_unit(1204).source_state,1)
	assert_true(s.find_unit(1199).is_empty())
	s.elapsed+=2
	s.siege.advance(s)
	assert_eq(s.find_unit(1199).source_state,1)
	assert_eq(s.siege.slots.size(),7)
	s.close()


func test_removal_results_and_competing_conditions() -> void:
	var s=_open()
	if not s.ready:return
	var battle=s.siege
	assert_true(s._activate(1194,Vector2i(68,6),10))
	assert_true(s._activate(1193,Vector2i(70,8),10))
	for row in [[3,4,1,1,false,true,0,14],[3,4,4,1,false,true,0,11],
			[4,3,1,4,true,false,0,11],[4,4,4,4,false,true,0,8],
			[4,4,4,4,true,true,0,2],[4,4,1,1,true,false,1,5]]:
		s.find_unit(1194).source_state=row[0]
		s.find_unit(1193).source_state=row[1]
		s.find_unit(1241).source_state=row[2]
		s.find_unit(1240).source_state=row[3]
		for n in s.catalog.grade_objects:s.find_unit(1250-n).side=0 if row[4] else 5
		for u in s.controlled_units():u.source_state=4 if row[5] else 1
		s._own_casualties=row[6]
		assert_eq(battle.result(s),row[7])
		assert_eq(s._pages(row[7]).size(),31 if row[7] in [11,14] else 28)
	s.close()


func test_replay_commands_bound_to_map_and_week() -> void:
	var t:={"version":1,"ticks":2,"overflow":false,"commands":[[0,1,1],[1,2],[2,3,13,95,143]]}
	assert_true(Record.valid_trace(t,[9,4],24))
	assert_false(Record.valid_trace(t,[9,3],24))
	assert_false(Record.valid_trace(t,[9,4],22))
	for cmd in [[0,1,0],[1,3,13,96,143],[0,3,13,95,144],[0,4,7,1194],[1,7,3,96,143]]:
		t.commands=[cmd]
		assert_false(Record.valid_trace(t,[9,4],24))


func test_real_battle_panel_loads_assets() -> void:
	var s=_open()
	if not s.ready:return
	var panel=preload("res://ui/school_sortie_trial.gd").new()
	Engine.get_main_loop().root.add_child(panel)
	assert_true(panel.open_trial(s.departure,{},{}))
	if panel.session.ready:assert_eq(panel.session.reserves.size(),74)
	panel.free()
	s.close()
