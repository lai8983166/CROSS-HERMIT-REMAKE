extends "res://sim/tests/test_base.gd"
const Record := preload("res://sim/school_sortie_record.gd")
const Helper := preload("res://sim/tests/test_school_sortie_session.gd")


func _open():
	var handoff := Helper.new().handoff(17)
	handoff.date=[8,5]
	handoff.scene=Record.Sortie.Adventures.thirty_five_rules().scene
	handoff.prepared.adventure_id=35
	handoff.prepared.rounds[0].scene_id=35
	var battle := Record.Sortie.new()
	assert_true(battle.open(handoff))
	return battle


func test_map_statues_and_playable_orders() -> void:
	var battle=_open()
	if not battle.ready:return
	assert_eq([battle.field_width,battle.field_height],[64,96])
	assert_eq([battle.ending_snapshot().phase,battle.opening_snapshot().page_count],["active",0])
	var types := {}
	for unit in battle.enemies():
		types[unit.character_id]=types.get(unit.character_id,0)+1
		assert_eq(unit.combat.movement_rate,0)
	assert_eq(types,{427:29,428:4,429:2,430:1})
	var statue=battle.find_unit(1249)
	assert_true(battle.command_move(3,statue.cell))
	assert_eq(battle.find_unit(3).target,1249)
	assert_false(battle._admitted(statue,battle.find_unit(3)))
	for sub in [2,5,8,11,14]:
		var pages:Array=battle._pages(sub)
		assert_eq(pages.size(),1)
		assert_eq(pages[0].size(),3)
		assert_eq(pages[0][2].text,"希望你們以後可以活用這些訓練的經驗。")
	battle.close()


func test_new_student_uses_her_own_source_skin() -> void:
	var base=_open()
	if not base.ready:return
	var handoff: Dictionary=base.departure.duplicate(true)
	base.close()
	var json := FileAccess.get_file_as_string("res://data/school_august_week4_story.json")
	var recruit: Dictionary=Record.Sortie.Adventures.Roles._integers(JSON.parse_string(json)).candidate
	handoff.prepared.rounds[0].student_ids=[13]
	handoff.prepared.rounds[0].teacher_ids=[116]
	handoff.participants=[recruit]
	handoff.growth=[recruit]
	assert_true(base.open(handoff))
	if base.ready:
		var unit: Dictionary=base.find_unit(13)
		assert_eq([unit.job,unit.skin_key],[10,"job10_v4"])
		assert_true(base.command_attack(13,1249))
	base.close()


func test_clear_time_boundaries_and_party_loss_priority() -> void:
	var battle=_open()
	if not battle.ready:return
	battle.elapsed=36001
	assert_false(battle._detect_trial_end())
	for unit in battle.enemies():unit.source_state=3
	for pair in [[10800,2],[10801,5],[18000,5],[18001,8],[36000,8],[36001,11]]:
		battle.elapsed=pair[0]
		battle._ending_phase="active"
		assert_true(battle._detect_trial_end())
		assert_eq(battle.ending_sub,pair[1])
	for unit in battle.controlled_units():unit.source_state=3
	battle._ending_phase="active"
	assert_true(battle._detect_trial_end())
	assert_eq(battle.ending_sub,14)
	battle.close()


func test_equipped_sword_wave_and_poison_arrow() -> void:
	var battle=_open()
	if not battle.ready:return
	var statue: Dictionary=battle.find_unit(1232)
	var sword: Dictionary=battle.find_unit(5)
	var archer: Dictionary=battle.find_unit(4)
	sword.cell=Vector2i(25,20)
	archer.cell=Vector2i(25,21)
	var sword_mp: int=sword.limits.mp
	var bow_mp: int=archer.limits.mp
	assert_false(battle.cast_aimed_skill(4,1232,11))
	assert_false(battle.cast_aimed_skill(5,3,11))
	assert_true(battle.cast_aimed_skill(5,1232,11))
	assert_false(battle.command_attack(5,1232))
	assert_true(battle.cast_aimed_skill(4,1232,20))
	assert_eq([sword.limits.mp,archer.limits.mp],[sword_mp-35,bow_mp-30])
	assert_eq(battle.battle_trace().commands,[[0,10,5,1232],[0,11,4,1232]])
	for i in 14:battle.tick()
	assert_eq(statue.limits.hp,600)
	battle.tick()
	assert_lt(statue.limits.hp,600)
	for i in 90:battle.tick()
	assert_true(battle.aimed_skills.is_empty())
	battle.close()


func test_trace_is_bound_to_the_week_and_map() -> void:
	var trace := {"version":1,"ticks":1,"overflow":false,"commands":[[0,3,13,63,95],[0,4,16,1249]]}
	assert_true(Record.valid_trace(trace,[8,5],35))
	assert_false(Record.valid_trace(trace,[8,4],35))
	assert_false(Record.valid_trace(trace,[8,5],17))
	for cmd in [[0,10,4,1232],[0,11,5,1232],[0,10,5,3],[0,1,1],[0,2],[0,3,13,64,95],[0,3,13,63,96],[0,4,7,1249]]:
		trace.commands=[cmd]
		assert_false(Record.valid_trace(trace,[8,5],35))
