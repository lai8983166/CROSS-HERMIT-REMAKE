extends "res://sim/tests/test_base.gd"
const Campaign := preload("res://sim/tests/test_school_mandatory_twenty_one.gd")
const Session := preload("res://sim/school_sortie_session.gd")
const Record := preload("res://sim/school_sortie_record.gd")
static var departure := {}


func _open() -> Session:
	if departure.is_empty():
		var model := Campaign.Model.new()
		assert_true(model.restore(Campaign.new()._save()).supported)
		var v := model.read_postbattle()
		departure=Session.Adventures.submit(v.bundle,v.planning.ledger).handoff
	var s := Session.new()
	assert_true(s.open(departure))
	return s


func _own(s, towers: int, springs: int) -> void:
	for i in 2:
		var count := towers if i==0 else springs
		for j in s.siege.objectives[i].size():
			s.siege.objectives[i][j].side=0 if j<count else 5


func test_consecutive_ownership_and_win_before_wipe() -> void:
	var s := _open()
	assert_eq([s.field_width,s.field_height,s.reserves.size()],[128,192,91])
	assert_eq(s.opening_snapshot().page_count,0)
	assert_false(s.advance_opening(true))
	assert_eq(s.siege.slots,{1:10800,2:18000,3:25200,4:14400,5:21600,6:28800})
	for row in [[2,3],[1,4]]:
		_own(s,row[0],row[1])
		s.siege.hold=53999
		s.tick()
		assert_eq(s.siege.hold,0)
	_own(s,2,4)
	s.siege.hold=53996
	s.tick()
	assert_eq(s.siege.hold,53998)
	for row in [[2,4,0,8],[4,13,1,5],[4,13,0,2]]:
		_own(s,row[0],row[1])
		s._own_casualties=row[2]
		s.siege.hold=53999
		for u in s.controlled_units():u.source_state=3
		s.frame+=1
		assert_eq(s.siege.result(s),row[3])
	assert_eq(s._pages(8)[0].size(),3)
	s.close()


func test_wipe_time_and_reinforcement_gate() -> void:
	var s := _open()
	var slots: Dictionary=s.siege.slots.duplicate()
	s.elapsed=10800
	s.siege.advance(s)
	assert_false(s.siege.slots.has(1))
	assert_true(s.siege.slots.has(0))
	assert_true(s.siege.slots[0]>=14400 and s.siege.slots[0]<=21600)
	assert_eq(s.siege.slots[2],slots[2]+2)
	var inactive := s.units.filter(func(u):return u.get("group",0)==12)
	for u in inactive:u.source_state=4
	s.siege.slots={1:10800}
	s.siege.hold=1
	s.siege.advance(s)
	for u in inactive:
		assert_eq(u.source_state,1)
		assert_true(u.cell.distance_to(Vector2i(3,143))<=5)
		assert_true(u.patrol in [20,21,22,23,24,26])
	for u in s.controlled_units():u.source_state=3
	s.elapsed=53999
	assert_eq(s.siege.result(s),14)
	s.elapsed=54000
	assert_eq(s.siege.result(s),11)
	s.close()


func test_trace_party_date_and_large_map_bounds() -> void:
	var t := {"version":1,"ticks":1,"overflow":false,"commands":[[0,3,17,127,191],[0,4,8,16],[0,7,3,127,191]]}
	assert_true(Record.valid_trace(t,[8,3],21))
	assert_false(Record.valid_trace(t,[8,2],21))
	assert_false(Record.valid_trace(t,[8,3],20))
	for cmd in [[0,3,17,128,191],[0,3,17,127,192],[0,3,7,0,0],[0,4,3,16],[0,2],[0,1,1]]:
		var bad:=t.duplicate(true)
		bad.commands=[cmd]
		assert_false(Record.valid_trace(bad,[8,3],21))

func test_healing_31_uses_the_saved_caster_and_allied_area() -> void:
	var s:=_open()
	var healer:=s.find_unit(9)
	var ally:=s.find_unit(6)
	var enemy:=s.find_unit(1249)
	ally.cell=healer.cell
	enemy.cell=healer.cell
	ally.limits.hp=5
	enemy.limits.hp=5
	var mp:int=healer.limits.mp
	assert_false(s.can_cast_spell(3,31))
	assert_false(s.cast_field_spell(9,healer.cell+Vector2i(9,0),31))
	assert_true(s.cast_field_spell(9,healer.cell,31))
	assert_eq(healer.limits.mp,mp-30)
	assert_false(s.can_cast_spell(9,31))
	assert_false(s.stop(9))
	assert_true(s.can_cast_spell(3,57))
	var recorded:=s.battle_trace()
	assert_eq(recorded.commands[-1],[0,9,9,healer.cell.x,healer.cell.y])
	assert_true(Record.valid_trace(recorded,[8,3],21))
	assert_false(Record.valid_trace(recorded,[8,2],20))
	s.elapsed=119
	s._update_field_spell(s.healing_spell)
	assert_eq(ally.limits.hp,5)
	s.elapsed=120
	s._update_field_spell(s.healing_spell)
	assert_eq(ally.limits.hp,5)
	s.elapsed=138
	s._apply_healing_impacts()
	assert_eq(ally.limits.hp,5)
	s.elapsed=199
	s._apply_healing_impacts()
	var restored:int=ally.limits.hp-5
	var morality:int=healer.input.attributes[3]
	var minimum:=10+int(morality*50/100)
	assert_true(restored>=minimum and restored<=minimum+10+int(morality*10/100)+4)
	assert_eq(enemy.limits.hp,5)
	s._update_field_spell(s.healing_spell)
	assert_true(s.healing_spell.is_empty())
	s.close()
