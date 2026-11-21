extends "res://sim/tests/test_base.gd"
const Session := preload("res://sim/school_sortie_session.gd")
const Record := preload("res://sim/school_sortie_record.gd")
const Campaign := preload("res://sim/tests/test_school_mandatory_nine.gd")
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
	assert_eq(s.opening_snapshot().page_count,9)
	while s.advance_opening(true):pass
	return s


func _own_towers(s: Session) -> void:
	for id in [1205,1204]:s.find_unit(id).side=0


func test_reinforcements_precede_timeout_and_require_both_intact_towers() -> void:
	var s := _open()
	if not s.ready:return
	assert_eq([s.field_width,s.field_height,s.reserves.size(),s.remaining_ticks],[64,96,75,108000])
	assert_true(s.find_unit(1203).is_empty())
	s.find_unit(1205).side=0
	assert_false(s._detect_trial_end())
	s.find_unit(1204).side=0
	s.remaining_ticks=0
	assert_true(s._detect_trial_end())
	assert_eq([s.knight_released,s._ending_phase,s._event_pages.size()],[true,"event20",15])
	for u in s.units:
		if u.get("group",0) in [1,2]:assert_eq(u.source_ai_request,[0,0,2,1])
	for row in [[9,52,85],[10,2,3],[11,3,91]]:
		var troops := s.units.filter(func(u):return u.get("group",0)==row[0])
		assert_true(troops.any(func(u):return u.source_state==1))
	var tick := s._trace_clock
	s.tick()
	assert_eq(s._trace_clock,tick)
	for page in 15:assert_true(s.advance_event())
	assert_false(s.advance_event())
	s._advance_nine_patrol()
	var guards := s.units.filter(func(u):return u.get("group",0) in [1,2])
	assert_true(guards.any(func(u):return not u.path.is_empty() and u.destination.distance_to(Session.NINE_PATROL_GOAL)<=2))
	assert_true(s._detect_trial_end())
	assert_eq(s.ending_sub,11)
	s.close()


func test_boss_removal_grades_and_all_down_precedence() -> void:
	for sample in [[true,0,2],[true,1,5],[false,0,8]]:
		var s := _open()
		_own_towers(s)
		s._detect_trial_end()
		while s.advance_event():pass
		if not sample[0]:s.find_unit(1207).source_state=3
		s._own_casualties=sample[1]
		s.find_unit(1203).source_state=3
		assert_false(s._detect_trial_end())
		s.find_unit(1203).source_state=4
		for u in s.controlled_units():u.limits.hp=0
		s.remaining_ticks=0
		assert_true(s._detect_trial_end())
		assert_eq(s.ending_sub,sample[2])
		for i in 4:s.advance_exit()
		assert_eq(s.result_inputs().objective_slots.count(0),16)
		s.close()
	var loss := _open()
	_own_towers(loss)
	loss.find_unit(1204).source_state=3
	for u in loss.controlled_units():u.limits.hp=0
	loss.remaining_ticks=0
	assert_true(loss._detect_trial_end())
	assert_eq(loss.ending_sub,14)
	loss.close()


func test_hostile_tower_takes_field_damage_and_destruction_ends_mission() -> void:
	var s := _open()
	var tower := s.find_unit(1205)
	var caster := s.find_unit(3)
	caster.cell=tower.cell+Vector2i.RIGHT
	var hp: int=tower.limits.hp
	assert_eq(hp,999)
	assert_true(s.cast_field_spell(3,tower.cell,59))
	s.elapsed=s.field_spell.release
	s._update_field_spell()
	assert_lt(tower.limits.hp,hp)
	s.elapsed=s.field_spell.finish
	s._update_field_spell()
	tower.limits.hp=1
	assert_true(s.cast_field_spell(3,tower.cell,59))
	s.elapsed=s.field_spell.release
	s._update_field_spell()
	s._update_removal()
	assert_true(s._detect_trial_end())
	assert_eq([s.ending_sub,s._terminal_choice.tactical_result_selector],[12,4])
	s.close()


func test_attack_orders_from_saved_formation_destroy_guardian_tower() -> void:
	var s := _open()
	var tower := s.find_unit(1205)
	assert_eq(tower.limits.hp,999)
	for unit in s.controlled_units():
		assert_true(s.command_move(unit.instance_id,tower.cell))
		assert_eq(s.battle_trace().commands.back(),[0,4,unit.instance_id,1205])
	assert_false(s.command_attack(6,1207))
	for tick_index in 3000:
		if s.ending_sub>=0:break
		s.tick()
	assert_eq([s.ending_sub,tower.limits.hp],[12,0])
	s.close()


func test_scene_date_spell_and_event_trace_guards() -> void:
	var s := _open()
	var invalid := departure.duplicate(true)
	invalid.date=[7,2]
	assert_false(s.open(invalid))
	assert_false(s.open(departure,{},"{}"))
	var trace := {"commands":[[0,2],[0,7,3,63,95]],"ticks":0,"version":1,"overflow":false}
	assert_true(Record.valid_trace(trace,[7,3],9))
	assert_false(Record.valid_trace(trace,[7,2],9))
	assert_false(Record.valid_trace(trace,[6,3],9))
	assert_false(Record.valid_trace(trace,[7,3],18))
	trace.commands[1][3]=64
	assert_false(Record.valid_trace(trace,[7,3],9))
	s.close()
