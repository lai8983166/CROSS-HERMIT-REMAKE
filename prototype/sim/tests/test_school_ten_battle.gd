extends "res://sim/tests/test_base.gd"
const Session := preload("res://sim/school_sortie_session.gd")
const Records := preload("res://sim/school_battle_record.gd")
const Campaign := preload("res://sim/tests/test_school_mandatory_ten.gd")
static var departure := {}


func _open() -> Session:
	if departure.is_empty():
		var model:=Campaign.Model.new()
		var restored:=model.restore(Campaign.new()._save())
		assert_true(restored["supported"],str(restored))
		var view:=model.read_postbattle()
		departure=Session.Adventures.submit(view["bundle"],view["planning"]["ledger"])["handoff"]
	var s:=Session.new()
	assert_true(s.open(departure))
	while s.ready and s._ending_phase=="opening":assert_true(s.advance_opening(true))
	return s


func test_escort_patrol_regions_and_timers() -> void:
	var s:=_open()
	if not s.ready:return
	var r:=s.escort_route
	var elder:=s.find_unit(1249)
	assert_eq([s.field_width,s.field_height],[96,144])
	assert_eq([elder.character_id,elder.side,elder.cell],[451,4,Vector2i(7,80)])
	assert_false(s.command_move(1249,Vector2i(8,9)))
	assert_eq(s.catalog.elder_route.size(),54)
	assert_eq(s.catalog.elder_route[0],[10,76,3600])
	assert_eq(s.catalog.elder_route.back(),[8,9,0])
	assert_false(s.command_attack(6,1249))
	elder.limits.hp-=1
	assert_true(s.command_move(8,elder.cell))
	assert_eq(s.battle_trace().commands.back(),[0,4,8,1249])
	s.find_unit(8).cell=elder.cell+Vector2i(0,1)
	s._hit(s.find_unit(8),elder)
	assert_eq(elder.limits.hp,elder.limits.hp_max)
	r._apply_script(s,1,1)
	assert_eq(r.timers.size(),2)
	assert_eq(r.timers[0],{"sub":20,"due":3540})
	assert_eq(r.timers[1],{"sub":21,"due":840})
	s.elapsed=840
	assert_true(s._detect_trial_end())
	assert_eq([r.active_block,r.active_sub],[0,21])
	while s._ending_phase=="event20":s.advance_event()
	assert_true(r.timers.has(0))
	assert_true(s.find_unit(1183).is_empty())
	assert_true(s.find_unit(1178).is_empty())
	r._apply_script(s,1,3)
	assert_eq(s.find_unit(1183).source_state,1)
	assert_eq(s.find_unit(1178).source_state,1)
	assert_true(s.enemies().any(func(u):return u.group==10))
	r.timers.clear()
	elder.cell=Vector2i(8,9)
	assert_false(s._detect_trial_end())
	r.enabled_region=6
	assert_false(s._detect_trial_end(),"enabling a region under a stationary elder")
	s.find_unit(6).cell=Vector2i(7,9)
	assert_false(s._detect_trial_end(),"a student cannot deliver the elder")
	elder.cell=Vector2i(8,10)
	assert_true(s._detect_trial_end())
	assert_true(r.arrived)
	assert_eq(s.ending_sub,8)
	s.close()


func test_patrol_reaches_original_impassable_waypoint() -> void:
	var s:=_open()
	if not s.ready:return
	var route:=s.escort_route
	var elder:=s.find_unit(1249)
	route.waypoint=35
	elder.cell=Vector2i(70,50)
	assert_eq(s.catalog.elder_route[35],[73,60,0])
	assert_false(s.walkable(Vector2i(73,60),elder.movement_type))
	route.walk(s)
	assert_false(elder.path.is_empty())
	var previous: Vector2i=elder.cell
	for cell in elder.path:
		assert_true(s.walkable(cell,elder.movement_type))
		assert_eq(absi(cell.x-previous.x)+absi(cell.y-previous.y),1)
		previous=cell
	elder.cell=previous
	elder.path=[]
	route.walk(s)
	route.walk(s)
	assert_eq(route.waypoint,36)
	s.close()


func test_ending_priority_and_record_boundaries() -> void:
	for sample in [[false,false,true,0,2],[false,false,true,1,5],[false,false,false,0,8],[false,true,true,0,14],[true,true,true,0,11]]:
		var s:=_open()
		if not s.ready:return
		s.escort_route.arrived=true
		if sample[0]:
			for ally in s.controlled_units():ally.limits.hp=0
		if sample[1]:s.find_unit(1249).source_state=4
		if sample[2]:
			for n in s.catalog.grade_objects:s.find_unit(1250-n).side=0
		s._own_casualties=sample[3]
		assert_true(s._detect_trial_end())
		assert_eq(s.ending_sub,sample[4])
		s.close()
	var trace:={"commands":[[0,2],[1,7,3,95,143]],"ticks":1,"version":1,"overflow":false}
	assert_true(Records.valid_trace(trace,true,false,false,false,false,true))
	assert_false(Records.valid_trace(trace,true,false,false,false,true))
	trace.commands[1][4]=144
	assert_false(Records.valid_trace(trace,true,false,false,false,false,true))
