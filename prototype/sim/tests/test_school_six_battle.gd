extends "res://sim/tests/test_base.gd"
const Session := preload("res://sim/school_sortie_session.gd")
const Records := preload("res://sim/school_battle_record.gd")
const Campaign := preload("res://sim/tests/test_school_mandatory_six.gd")
static var departure := {}


func _open() -> Session:
	if departure.is_empty():
		var model:=Campaign.Model.new()
		var restored:=model.restore(Campaign.new()._save())
		assert_true(restored["supported"],str(restored))
		var view:=model.read_postbattle()
		departure=Session.Adventures.submit(view["bundle"],view["planning"]["ledger"])["handoff"]
	var session:=Session.new()
	assert_true(session.open(departure))
	while session.ready and session._ending_phase=="opening":assert_true(session.advance_opening(true))
	return session


func test_boss_removal_and_grading_priority() -> void:
	for sample in [[false,true,0,8],[true,false,0,8],[true,true,1,5],[true,true,0,2]]:
		var s:=_open()
		if not s.ready:return
		assert_eq(s.controlled_units().map(func(u):return u.character_id),[3,8,6,1,2])
		assert_eq(s.enemies().size(),64)
		var boss:=s.find_unit(1245)
		assert_eq([boss.character_id,boss.cell,boss.limits.hp],[457,Vector2i(31,40),260])
		boss.limits.hp=0
		boss.source_state=3
		assert_false(s._detect_trial_end(),"boss removal has not finished")
		boss.source_state=4
		if sample[0]:
			for enemy in s.enemies():
				enemy.limits.hp=0
				enemy.source_state=4
		if not sample[1]:s.find_unit(1248).side=5
		if not sample[0]:
			for ally in s.controlled_units():ally.limits.hp=0
		s._own_casualties=sample[2]
		assert_true(s._detect_trial_end())
		assert_eq(s.ending_sub,sample[3])
		s.close()
	var s:=_open()
	for unit in s.controlled_units():unit.limits.hp=0
	assert_true(s._detect_trial_end())
	assert_eq(s.ending_sub,11)
	s.close()


func test_deployment_and_command_tampering() -> void:
	var s:=_open()
	if not s.ready:return
	assert_true(s.command_attack(2,1245))
	var trace:=s.battle_trace()
	assert_true(Records.valid_trace(trace,true,false,false,false,true))
	assert_false(Records.valid_trace(trace,true,false,false,true,false))
	var other:=Session.new()
	assert_false(other.open(departure,{},"altered catalog"))
	var changed:=departure.duplicate(true)
	changed["scene"]["template_count"]-=1
	assert_false(other.open(changed))
	assert_false(s.command_attack(2,1249),"allied tower")
	assert_false(s.cast_field_spell(2,s.find_unit(2).cell,59),"unequipped")
	var forged:=trace.duplicate(true)
	forged.commands.append([0,4,2,1249])
	forged.ticks=1
	assert_true(other.open(departure))
	assert_false(Records.run_trace(other,forged)["supported"])
	other.close()
	s.close()
