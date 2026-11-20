extends "res://sim/tests/test_base.gd"
const Session := preload("res://sim/school_sortie_session.gd")
const Records := preload("res://sim/school_battle_record.gd")
const Campaign := preload("res://sim/tests/test_school_mandatory_thirteen.gd")
static var departure := {}


func _open() -> Session:
	if departure.is_empty():
		var model := Campaign.Model.new()
		var restored := model.restore(Campaign.new()._save())
		assert_true(restored["supported"],str(restored))
		var view := model.read_postbattle()
		departure=Session.Adventures.submit(view.bundle,view.planning.ledger).handoff
	var s := Session.new()
	assert_true(s.open(departure))
	while s.advance_opening(true):pass
	return s


func _place(s: Session, id: int, region: int) -> void:
	var index: int=s.catalog.regions[str(region)][0]
	s.find_unit(id).cell=Vector2i(index%s.field_width,index/s.field_width)


func _formation(s: Session) -> void:
	for pair in [[5,4],[3,5],[8,6],[4,7],[1,8],[6,9]]:_place(s,pair[0],pair[1])


func test_tablet_dialogue_and_continuous_occupation() -> void:
	var s := _open()
	if not s.ready:return
	assert_eq([s.field_width,s.field_height,s.enemies().size(),s.reserves.size(),s.remaining_ticks],[96,144,31,93,72000])
	var prayer := s.prayer
	_place(s,4,3)
	_place(s,1,1)
	assert_true(s._detect_trial_end())
	assert_eq([prayer.reading,s._event_pages.size()],[3,3])
	assert_false(s.command_move(4,Vector2i(7,136)))
	while s.advance_event():pass
	assert_true(s._detect_trial_end())
	assert_eq(prayer.reading,1)
	while s.advance_event():pass
	assert_false(s._detect_trial_end())
	_formation(s)
	assert_false(prayer.held(s))
	assert_eq(prayer.duration,0)
	_place(s,2,2)
	assert_true(s._detect_trial_end())
	while s.advance_event():pass
	assert_true(prayer.discovered.has_all([1,2,3]))
	assert_false(prayer.held(s))
	assert_false(prayer.held(s))
	assert_eq([prayer.occupied,prayer.duration],[6,1])
	_place(s,3,8)
	_place(s,1,5)
	s._trace_clock+=1
	assert_false(prayer.held(s))
	assert_eq([prayer.occupied,prayer.duration],[5,0])
	_formation(s)
	for i in 299:
		s._trace_clock+=1
		assert_false(prayer.held(s))
	assert_eq(prayer.duration,299)
	s._trace_clock+=1
	s.remaining_ticks=0
	assert_true(s._detect_trial_end())
	assert_eq(s.ending_sub,8)
	s.close()


func test_last_tick_samples_after_movement() -> void:
	for leaving in [true,false]:
		var s := _open()
		if not s.ready:return
		_formation(s)
		s.prayer.discovered={1:true,2:true,3:true}
		s.prayer.duration=299
		var unit := s.find_unit(4)
		var pad: Vector2i=unit.cell
		var outside := pad+Vector2i.UP
		unit.cell=pad if leaving else outside
		assert_true(s.command_move(4,outside if leaving else pad))
		s.frame=s.catalog.interaction.move_interval-1
		s.remaining_ticks=2
		s.tick()
		assert_eq(unit.cell,outside if leaving else pad)
		assert_eq(s.ending_sub,11 if leaving else 8)
		s.close()


func test_source_states_timeout_and_slot_delivery() -> void:
	for sample in [[0,2],[1,5]]:
		var s := _open()
		if not s.ready:return
		_formation(s)
		s.prayer.discovered={1:true,2:true,3:true}
		s.prayer.duration=299
		for id in [1248,1247]:assert_true(s._activate(id,Vector2i(45,75),3))
		for id in [1249,1248,1247]:s.find_unit(id).source_state=3
		s._own_casualties=sample[0]
		assert_true(s._detect_trial_end())
		assert_eq(s.ending_sub,sample[1])
		s.close()
	var battle := _open()
	if not battle.ready:return
	assert_eq(battle.timers.size(),15)
	for row in battle.timers.slice(0,4):
		battle.elapsed=battle.timers[0].at-2
		battle._update_summoning()
		assert_true(battle.enemies().any(func(u):return u.group==row.group))
		assert_eq(battle.timers.size(),14-row.slot)
	for ally in battle.controlled_units():ally.limits.hp=0
	battle.remaining_ticks=0
	assert_true(battle._detect_trial_end())
	assert_eq(battle.ending_sub,11)
	battle.close()
	var defeated := _open()
	for ally in defeated.controlled_units():ally.limits.hp=0
	assert_true(defeated._detect_trial_end())
	assert_eq(defeated.ending_sub,14)
	defeated.close()


func test_trace_and_source_admission() -> void:
	var trace := {"commands":[[0,2],[1,7,3,95,143]],"ticks":1,"version":1,"overflow":false}
	assert_true(Records.valid_trace(trace,true,false,false,false,false,false,true))
	assert_false(Records.valid_trace(trace,true,false,false,false,true))
	trace.commands[1][4]=144
	assert_false(Records.valid_trace(trace,true,false,false,false,false,false,true))
	var original := _open()
	original.close()
	var altered := departure.duplicate(true)
	altered.scene.configuration_sha256="bad"
	assert_false(original.open(altered))
	assert_false(original.open(departure,{},"{}"))
