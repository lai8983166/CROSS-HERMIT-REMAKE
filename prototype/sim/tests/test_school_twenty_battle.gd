extends "res://sim/tests/test_base.gd"
const Campaign := preload("res://sim/tests/test_school_mandatory_twenty.gd")
const Session := preload("res://sim/school_sortie_session.gd")
const Record := preload("res://sim/school_sortie_record.gd")
static var departure := {}


func _open() -> Session:
	if departure.is_empty():
		var model := Campaign.Model.new()
		var restored := model.restore(Campaign.new()._save())
		assert_true(restored.supported,str(restored))
		var v := model.read_postbattle()
		departure=Session.Adventures.submit(v.bundle,v.planning.ledger).handoff
	var s := Session.new()
	assert_true(s.open(departure))
	assert_eq(s.opening_snapshot().page_count,2)
	while s.advance_opening(true):pass
	return s


func test_boss_removal_precedes_wipe_and_five_objects_set_the_grade() -> void:
	for row in [[0,1,0,2],[0,1,1,5],[4,1,0,8],[5,1,0,8],[0,2,0,8],[0,3,0,8],[0,4,0,8]]:
		var s:=_open()
		assert_eq(s.catalog.grade_objects,[1,2,3,4,5])
		var boss:=s.find_unit(1244)
		boss.limits.hp=0
		boss.source_state=3
		assert_false(s._detect_trial_end())
		boss.source_state=4
		s._own_casualties=row[2]
		s.find_unit(1245).side=row[0]
		s.find_unit(1245).source_state=row[1]
		for u in s.controlled_units():u.source_state=3
		assert_true(s._detect_trial_end())
		assert_eq(s.ending_sub,row[3])
		s.close()


func test_all_down_threshold_and_result_time_brackets() -> void:
	for row in [[18000,14,1],[18001,14,2],[35999,14,2],[36000,11,2],[36001,11,3],[108001,11,3]]:
		var s:=_open()
		s.elapsed=row[0]
		assert_false(s._detect_trial_end())
		for u in s.controlled_units():
			u.limits.hp=0
		assert_false(s._detect_trial_end())
		for u in s.controlled_units():u.source_state=3
		assert_true(s._detect_trial_end())
		assert_eq(s.ending_sub,row[1])
		for i in 4:s.advance_exit()
		var facts:=s.result_inputs()
		assert_eq([facts.time_key,facts.unit_condition_key],[row[2],1])
		assert_eq(facts.objective_slots.count(0),16)
		s.close()


func test_original_patrol_summoning_and_guard_targets() -> void:
	var s:=_open()
	assert_eq([s.field_width,s.field_height,s.reserves.size()],[64,96,80])
	assert_eq(s.catalog.patrol_goals,[[38,57],[54,90],[50,75],[54,75]])
	assert_eq(s.reserves.values().filter(func(r):return r.has("summon_interval")).size(),12)
	var foe:=s.find_unit(1244)
	var gate:=s.find_unit(1245)
	var tower:=s.find_unit(1249)
	var spring:=s.find_unit(1247)
	foe.cell=gate.cell+Vector2i.RIGHT
	assert_true(s._admitted(foe,gate))
	assert_false(s._admitted(gate,foe))
	assert_true(s._admitted(tower,foe))
	assert_false(s._admitted(foe,tower))
	gate.limits.hp=1
	assert_true(s._admitted(spring,gate))
	var summoner:=s.find_unit(1235)
	summoner.summon_clock=s.reserves[1235].summon_interval-1
	s._advance_twenty()
	assert_eq(summoner.summon_phase,"prepare")
	s.close()


func test_commands_and_handoff_are_limited_to_the_saved_party_and_map() -> void:
	var s:=_open()
	assert_eq(s.controlled_units().map(func(u):return u.instance_id),[3,16,4,8,17,6,5,2,9,1])
	var legal: Dictionary={"version":1,"ticks":1,"overflow":false,"commands":[[0,4,8,16],[0,4,9,17],[0,3,16,63,95],[0,7,3,63,95]]}
	assert_true(Record.valid_trace(legal,[8,2],20))
	assert_false(Record.valid_trace(legal,[8,1],20))
	assert_false(Record.valid_trace(legal,[8,2],17))
	for invalid in [[0,3,16,64,95],[0,3,16,63,96],[0,4,16,17],[0,7,16,63,95],[0,2]]:
		var tampered:=legal.duplicate(true)
		tampered.commands=[invalid]
		assert_false(Record.valid_trace(tampered,[8,2],20))
	var wrong:=departure.duplicate(true)
	wrong.date=[8,1]
	assert_false(s.open(wrong))
	s.close()


func test_friendly_gate_traversal_and_original_melee_mask() -> void:
	var s:=_open()
	var mover:=s.find_unit(6)
	var gate:=s.find_unit(1246)
	mover.cell=gate.cell+Vector2i.DOWN
	var dest: Vector2i=gate.cell+Vector2i.UP
	for u in s.controlled_units():
		if u.instance_id!=6:u.cell=Vector2i(55,91)
	assert_false(s._blocked(6).has(gate.cell))
	assert_true(s.command_move(6,dest))
	assert_true(mover.path.has(gate.cell))
	for i in range(24):s.tick()
	assert_eq(mover.cell,dest)
	gate.side=5
	assert_true(s._blocked(6).has(gate.cell))
	var boss:=s.find_unit(1244)
	mover.cell=boss.cell+Vector2i(3,1)
	assert_eq(s._distance(mover,boss),3)
	assert_true(s._attack_path(mover,boss).is_empty())
	mover.cell=boss.cell+Vector2i(3,2)
	assert_true(s._distance(mover,boss)>3)
	assert_false(s._attack_path(mover,boss).is_empty())
	s.close()
