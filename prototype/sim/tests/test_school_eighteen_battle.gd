extends "res://sim/tests/test_base.gd"
const Session := preload("res://sim/school_sortie_session.gd")
const Record := preload("res://sim/school_sortie_record.gd")
const Course := preload("res://sim/school_return_courses.gd")
const Campaign := preload("res://sim/tests/test_school_july_eighteen.gd")
static var departure := {}
static var full_departure := {}


func _open() -> Session:
	if departure.is_empty():
		var m := Campaign.Model.new()
		var restored := m.restore(Campaign.new()._save())
		assert_true(restored.supported,str(restored))
		var view := m.read_postbattle()
		var mode := Course.set_mode(view.bundle,2,false)
		departure=Session.Adventures.submit(mode.after,view.planning.ledger).handoff
	var s := Session.new()
	assert_true(s.open(departure))
	while s.advance_opening(true):pass
	return s


func _clear(s: Session) -> void:
	for u in s.enemies():
		if u.character_id in range(411,415):continue
		u.source_state=4
		u.limits.hp=0


func test_ownership_grade_and_same_tick_wave_priority() -> void:
	for sample in [[false,0,8,1],[true,0,2,2],[true,1,5,2]]:
		var s := _open()
		if not s.ready:return
		assert_eq([s.field_width,s.field_height,s.reserves.size(),s.remaining_ticks],[64,96,78,-1])
		assert_eq(s.catalog.grade_objects,[1,2,3])
		for n in s.catalog.grade_objects:s.find_unit(1250-n).side=0
		s.find_unit(1172).side=5
		s.castle.slots={0:{"due":0,"sub":20}}
		if sample[0]:_clear(s)
		s._own_casualties=sample[1]
		assert_true(s._detect_trial_end())
		assert_eq(s.ending_sub,sample[2])
		assert_eq(s.castle.slots.size(),1)
		for i in 4:s.advance_exit()
		var facts := s.result_inputs()
		assert_eq([facts.time_key,facts.unit_condition_key],[0,sample[3]])
		assert_eq(facts.objective_slots.count(0),16)
		s.close()


func test_failed_object_and_gate_branch_before_waves() -> void:
	var s := _open()
	if not s.ready:return
	assert_eq(s.castle.slots.size(),9)
	assert_eq(s.castle.waves[23].groups,[10,11,12,13,14,15])
	_clear(s)
	s.castle.slots={0:{"due":0,"sub":23},1:{"due":0,"sub":20}}
	s.find_unit(1246).source_state=3
	assert_false(s._detect_trial_end())
	assert_true(s.castle.gate_breached)
	assert_eq(s.castle.slots,{1:{"due":2,"sub":20}})
	s.elapsed=2
	assert_false(s._detect_trial_end())
	assert_eq(s.find_unit(1207).source_state,1)
	for ally in s.controlled_units():ally.limits.hp=0
	s.find_unit(1248).source_state=3
	assert_true(s._detect_trial_end())
	assert_eq([s.ending_sub,s.castle.lost_object],[11,2])
	s.close()
	var loss := _open()
	for ally in loss.controlled_units():ally.limits.hp=0
	assert_true(loss._detect_trial_end())
	assert_eq(loss.ending_sub,14)
	loss.close()


func test_date_scene_and_command_admission() -> void:
	var s := _open()
	s.close()
	var invalid := departure.duplicate(true)
	invalid.date=[7,2]
	assert_false(s.open(invalid))
	assert_false(s.open(departure,{},"{}"))
	var trace := {"commands":[[0,7,3,63,95]],"ticks":0,"version":1,"overflow":false}
	assert_true(Record.valid_trace(trace,[7,1],18))
	assert_false(Record.valid_trace(trace,[7,1],17))
	assert_false(Record.valid_trace(trace,[7,2],18))
	trace.commands[0][3]=64
	assert_false(Record.valid_trace(trace,[7,1],18))
	trace.commands=[[0,2]]
	assert_false(Record.valid_trace(trace,[7,1],18))

func test_source_healers_and_recorded_friendly_orders() -> void:
	if full_departure.is_empty():
		var m := Campaign.Model.new()
		var restored := m.restore(Campaign.new()._save())
		assert_true(restored.supported,str(restored))
		var view := m.read_postbattle()
		var bundle: Dictionary=view.bundle
		for group in range(4):
			bundle=Course.set_mode(bundle,group,false).after
		full_departure=Session.Adventures.submit(bundle,view.planning.ledger).handoff
	var s := Session.new()
	assert_true(s.open(full_departure))
	if not s.ready:return
	while s.advance_opening(true):pass
	var ally := s.find_unit(6)
	for id in [8,9]:
		var healer := s.find_unit(id)
		var job: Dictionary=s.combat_rules.jobs[str(healer.job)]
		assert_eq(String(job.attack_hex).hex_decode().decode_u16(2),5)
		assert_false(s.command_attack(id,6))
		ally.limits.hp-=1
		healer.cell=ally.cell+Vector2i.RIGHT
		assert_true(s.command_move(id,ally.cell))
		assert_eq(s.battle_trace().commands.back(),[0,4,id,6])
		s._hit(healer,ally)
		assert_eq(ally.limits.hp,ally.limits.hp_max)
	ally.limits.hp-=1
	assert_false(s.command_attack(1,6))
	var trace := {"commands":[[0,4,9,6]],"ticks":0,"version":1,"overflow":false}
	assert_true(Record.valid_trace(trace,[7,1],18))
	assert_false(Record.valid_trace(trace,[6,4],13))
	assert_false(Record.valid_trace(trace,[7,1],17))
	s.close()
