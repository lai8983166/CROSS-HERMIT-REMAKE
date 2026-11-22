extends "res://sim/tests/test_base.gd"
const Record := preload("res://sim/school_sortie_record.gd")
const Helper := preload("res://sim/tests/test_school_sortie_session.gd")


func _open():
	var handoff := Helper.new().handoff(17)
	handoff.date=[9,3]
	handoff.scene=Record.Sortie.Adventures.twenty_two_rules().scene
	handoff.prepared.adventure_id=22
	handoff.prepared.rounds[0].scene_id=22
	var battle:=Record.Sortie.new()
	assert_true(battle.open(handoff))
	return battle


func test_map_opening_factions_and_target_search() -> void:
	var battle=_open()
	if not battle.ready:return
	assert_eq([battle.field_width,battle.field_height],[64,96])
	assert_eq(battle.enemies().map(func(u):return u.character_id),[11,18,19,20,21])
	assert_eq(battle.find_unit(1248).cell,Vector2i(38,45))
	assert_eq(battle.find_unit(1249).cell,Vector2i(29,24))
	assert_eq(battle.opening_snapshot().page_count,5)
	assert_false(battle.advance_opening(false))
	for i in 5:assert_true(battle.advance_opening(true))
	var opponent: Dictionary=battle.find_unit(1242)
	var start: Vector2i=opponent.cell
	for i in 30:battle.tick()
	assert_true(opponent.cell!=start)
	assert_true(battle.find_unit(opponent.target).controllable)
	assert_eq(battle.battle_trace().commands,[[0,1,1],[0,1,1],[0,1,1],[0,1,1],[0,1,1]])
	battle.close()


func test_source_grades_priority_and_reward_object_are_distinct() -> void:
	var battle=_open()
	if not battle.ready:return
	for row in [
		# elapsed, remaining, hostile, tower owned, casualties, all down, sub, selector
		[18000,18000,false,false,0,true,2,1],[18000,18000,false,true,1,false,5,2],
		[18001,17999,false,true,0,false,8,3],[36000,0,false,false,1,true,8,3],
		[35998,2,true,true,0,false,-1,0],[35998,2,true,true,1,true,14,5],
		[36000,0,true,false,0,true,11,4],[36000,0,true,true,0,true,3,1],
		[36000,0,true,true,1,true,6,2]]:
		battle._ending_phase="active"
		battle.elapsed=row[0]
		battle.remaining_ticks=row[1]
		for u in battle.enemies():u.source_state=1 if row[2] else 4
		battle.find_unit(1248).side=0 if row[3] else 7
		battle.find_unit(1249).side=7 if row[3] else 0
		battle._own_casualties=row[4]
		for u in battle.controlled_units():u.source_state=4 if row[5] else 1
		assert_eq(battle._detect_trial_end(),row[6]>=0)
		if row[6]<0:continue
		assert_eq([battle.ending_sub,battle._terminal_choice.tactical_result_selector],[row[6],row[7]])
		assert_true(battle._pages(battle.ending_sub).is_empty())
		battle._ending_phase="summary"
		var facts: Dictionary=battle.result_inputs()
		assert_eq(facts.objective_slots[0],int(not row[3]))
		assert_eq(facts.unit_condition_key,1 if row[2] else 2)
	battle.close()


func test_trace_admission_boundaries() -> void:
	var trace:={"version":1,"ticks":1,"overflow":false,"commands":[[0,1,1],[0,3,13,63,95],[0,4,16,1242]]}
	assert_true(Record.valid_trace(trace,[9,3],22))
	assert_false(Record.valid_trace(trace,[8,5],22))
	assert_false(Record.valid_trace(trace,[9,3],35))
	for command in [[0,1,0],[0,2],[0,3,13,64,95],[0,3,13,63,96],[0,4,7,1242]]:
		trace.commands=[command]
		assert_false(Record.valid_trace(trace,[9,3],22))


func test_opposing_caster_has_source_release_and_ui_assets() -> void:
	var battle=_open()
	if not battle.ready:return
	var panel=preload("res://ui/school_sortie_trial.gd").new()
	var tree:=Engine.get_main_loop() as SceneTree
	tree.root.add_child(panel)
	assert_true(panel.open_trial(battle.departure,{},{}))
	if panel.session.ready:
		var key:String=panel.session.find_unit(1242).skin_key
		assert_false(panel.session.catalog.skins[key].actions.has("basic_attack"))
		var skin:Dictionary=panel.canvas.skin_overrides[key]
		for step in skin.actions.basic_attack.N.steps:
			for layer in step.layers:assert_true(panel.canvas.sprites.has(skin.frames[str(layer.frame)].file))
		assert_false(skin.actions.basic_attack.N.steps[0].layers.is_empty())
	panel.free()
	battle.close()
