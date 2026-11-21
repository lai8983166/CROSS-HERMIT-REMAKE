extends "res://sim/tests/test_base.gd"
const Session := preload("res://sim/school_sortie_session.gd")
const Record := preload("res://sim/school_sortie_record.gd")
const Campaign := preload("res://sim/tests/test_school_mandatory_fourteen.gd")
static var departure := {}


func _open() -> Session:
	if departure.is_empty():
		var model := Campaign.Model.new()
		var restored := model.restore(Campaign.new()._save())
		assert_true(restored.supported,str(restored))
		var view := model.read_postbattle()
		departure=Session.Adventures.submit(view.bundle,view.planning.ledger).handoff
	var s := Session.new()
	assert_true(s.open(departure))
	assert_eq(s.opening_snapshot().page_count,3)
	while s.advance_opening(true):pass
	return s


func test_exit_region_and_exact_ten_minute_threshold() -> void:
	for sample in [[36000,0,2],[36000,1,5],[36002,0,8]]:
		var s := _open()
		assert_eq([s.field_width,s.field_height,s.reserves.size(),s.remaining_ticks],[128,192,83,-1])
		assert_eq(s.catalog.regions["1"].size(),10)
		s.elapsed=sample[0]
		s._own_casualties=sample[1]
		var runner := s.find_unit(6)
		runner.cell=Vector2i(8,139)
		s.dungeon.previous_cells[6]=runner.cell
		assert_eq(s.dungeon.result(s,false),-1)
		s.dungeon.previous_cells[6]=Vector2i(9,139)
		runner.side=4
		assert_eq(s.dungeon.result(s,false),-1)
		runner.side=0
		s.dungeon.previous_cells[6]=Vector2i(9,139)
		assert_eq(s.dungeon.result(s,true),sample[2])
		assert_eq(s.dungeon.escaped_id,6)
		s.close()
	var loss := _open()
	for sample in [[35998,14],[36000,11]]:
		loss.elapsed=sample[0]
		assert_eq(loss.dungeon.result(loss,true),sample[1])
	loss.close()


func test_original_timers_and_variable_branch_spawn_points() -> void:
	var s := _open()
	assert_eq(s.dungeon.slots.size(),11)
	assert_eq(s.dungeon.waves[20].groups,[10,11,12,13,14,15])
	assert_eq(s.dungeon.waves[21].groups,[2,3,4,5,6])
	assert_eq(s.dungeon.waves[20].delay,[900,10800])
	assert_eq(s.dungeon.waves[21].delay,[3600,10800])
	s.elapsed=10800
	s.dungeon.advance(s)
	var wave1:=s.units.filter(func(u):return u.get("group",0) in range(10,16))
	assert_false(wave1.is_empty())
	for u in wave1:
		assert_true(u.cell.distance_to(Vector2i(18,170))<=4.3)
		assert_true(u.source_ai_request[1] in range(1,7))
	assert_eq(s.dungeon.slots[7].due,10802)
	s.elapsed=10802
	s.dungeon.advance(s)
	var wave2:=s.units.filter(func(u):return u.get("group",0) in range(2,7))
	assert_false(wave2.is_empty())
	for u in wave2:assert_true(u.cell.distance_to(Vector2i(101,129))<=4.3)
	# Direct placement cannot resurrect state 4. The explicit OP136(33)
	# in a later reinforcement script makes the group eligible again.
	var group: int=wave1[0].group
	for u in wave1:
		u.source_state=4
		u.limits.hp=0
	assert_false(s._activate(wave1[0].instance_id,Vector2i(18,170),3))
	s.dungeon.waves[20].groups=[group]
	s.dungeon.slots={0:{"sub":20,"due":s.elapsed}}
	s.dungeon.advance(s)
	for u in wave1:assert_eq([u.source_state,u.limits.hp],[1,u.limits.hp_max])
	s.close()


func test_chest_facts_and_tactical_command_bounds() -> void:
	var s := _open()
	s.find_unit(1248).side=0
	s.find_unit(6).cell=Vector2i(8,139)
	assert_true(s._detect_trial_end())
	assert_eq(s.ending_sub,2)
	for i in 4:s.advance_exit()
	assert_eq(s.result_inputs().objective_slots,[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
	s.close()
	var invalid:=departure.duplicate(true)
	invalid.date=[7,3]
	assert_false(s.open(invalid))
	assert_false(s.open(departure,{},"{}"))
	var trace := {"commands":[[0,3,6,127,191],[0,7,3,127,191]],"ticks":0,"version":1,"overflow":false}
	assert_true(Record.valid_trace(trace,[7,4],14))
	assert_false(Record.valid_trace(trace,[7,3],14))
	assert_false(Record.valid_trace(trace,[7,4],9))
	trace.commands[0][3]=128
	assert_false(Record.valid_trace(trace,[7,4],14))
	trace.commands=[[0,2]]
	assert_false(Record.valid_trace(trace,[7,4],14))
