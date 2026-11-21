extends "res://sim/tests/test_base.gd"
const Session := preload("res://sim/school_sortie_session.gd")
const Record := preload("res://sim/school_sortie_record.gd")
const Courses := preload("res://sim/school_return_courses.gd")
const Campaign := preload("res://sim/tests/test_school_july_five_work.gd")
static var departure := {}


func _prepare(bundle: Dictionary, ledger: Dictionary) -> Dictionary:
	for group in range(4):
		bundle=Courses.set_mode(bundle,group,false).after
	bundle=Session.Adventures.select(bundle,ledger,17).after
	return Session.Adventures.submit(bundle,ledger).handoff


func _open() -> Session:
	if departure.is_empty():
		var model := Campaign.Model.new()
		var restored := model.restore(Campaign.new()._save())
		assert_true(restored.supported,str(restored))
		var view := model.read_postbattle()
		departure=_prepare(view.bundle,view.planning.ledger)
	var s := Session.new()
	assert_true(s.open(departure))
	while s.advance_opening(true):pass
	return s


func test_two_recruits_use_their_own_skins_and_job_one_attack() -> void:
	var s := _open()
	assert_eq(s.controlled_units().size(),10)
	var gate := s.find_unit(1246)
	for id in [16,17]:
		var u := s.find_unit(id)
		assert_eq([u.skin_key,u.job,u.combat.attack_id,u.combat.attack_range,u.combat.cast_ticks],
			["job1_v6" if id==16 else "job1_v3",1,101,3,110])
		assert_eq(u.input.equipped_skills,[0,0,0,0,0,0,0,0])
		assert_true(s.command_attack(id,1246))
		gate.cell=u.cell+Vector2i.RIGHT
		var hp: int=gate.limits.hp
		for strike in range(12):
			s._hit(u,gate)
			if gate.limits.hp<hp:break
		assert_true(gate.limits.hp<hp)
	assert_true(Record.valid_trace(s.battle_trace(),[7,5],17))
	assert_false(Record.valid_trace(s.battle_trace(),[7,2],17))
	assert_false(Record.valid_trace(s.battle_trace(),[7,5],18))
	s.close()
	var old := departure.duplicate(true)
	old.date=[7,2]
	assert_false(s.open(old))
	var bad := departure.duplicate(true)
	for p in bad.participants:
		if p.character_id==17:p.equipped_skills[0]=59
	assert_false(s.open(bad))


func test_seven_obstacles_are_passive_and_excluded_from_unit_key() -> void:
	var s := _open()
	var runner := s.find_unit(6)
	var obstacles := 0
	for unit in s.units:
		if unit.character_id==411:
			obstacles+=1
			assert_false(s._admitted(unit,runner))
			assert_true(s._admitted(runner,unit))
		elif unit.category==5:
			unit.source_state=4
			unit.limits.hp=0
	assert_eq(obstacles,7)
	for id in s.reserves:
		if s.find_unit(id).is_empty():
			var raw := String(s.reserves[id].record_hex).hex_decode()
			raw[15]=4
			s.reserves[id].record_hex=raw.hex_encode()
	runner.cell=Vector2i(90,16)
	assert_true(s._detect_trial_end())
	for i in 4:s.advance_exit()
	assert_eq(s.result_inputs().unit_condition_key,2)
	var foe := s.find_unit(1235)
	foe.source_state=1
	assert_eq(s.result_inputs().unit_condition_key,1)
	s.close()
