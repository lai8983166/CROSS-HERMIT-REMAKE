extends "res://sim/tests/test_base.gd"
const Session := preload("res://sim/school_sortie_session.gd")
const Records := preload("res://sim/school_battle_record.gd")
const Campaign := preload("res://sim/tests/test_school_mandatory_four.gd")
static var context := {}


func _open() -> Session:
	if context.is_empty():
		var campaign := Campaign.new()
		var model := Campaign.Model.new()
		var restored: Dictionary=model.restore(campaign._saves()[0])
		assert_true(restored["supported"])
		var view := model.read_postbattle()
		context=Session.Adventures.submit(view["bundle"],view["planning"]["ledger"])["handoff"]
	var session := Session.new()
	assert_true(session.open(context))
	while session.ready and session._ending_phase=="opening":assert_true(session.advance_opening(true))
	return session


func test_priority_and_hostile_chests() -> void:
	for sample in [[25200,0,2],[25200,1,5],[25202,0,8],[36000,0,8]]:
		var s:=_open()
		if not s.ready:return
		assert_eq(s.enemies().size(),53)
		for enemy in s.enemies():
			enemy["limits"]["hp"]=0
			enemy["source_state"]=2 if enemy["life_kind"]==3 else 4
		for id in [1249,1248]:
			assert_eq(s.find_unit(id)["side"],5)
			assert_false(s.command_attack(3,id))
		s.elapsed=sample[0]
		s.remaining_ticks=36000-s.elapsed
		s._own_casualties=sample[1]
		assert_true(s._detect_trial_end())
		assert_eq(s.ending_sub,sample[2])
		for i in 4:s.advance_exit()
		assert_eq(s.result_inputs()["unit_condition_key"],2)
		assert_false(s.result_inputs()["objective_slots"].has(1))
		s.close()
	var s:=_open()
	if not s.ready:return
	for u in s.controlled_units():u["limits"]["hp"]=0
	s.remaining_ticks=0
	assert_true(s._detect_trial_end())
	assert_eq(s.ending_sub,11)
	s.close()


func test_current_party_weapon_spell_and_healing_orders() -> void:
	var s:=_open()
	if not s.ready:return
	var archer:=s.find_unit(1)
	assert_eq(archer.combat.accuracy,127)
	assert_eq(archer.combat.movement_rate,135)
	assert_eq(archer.combat.attack_rate,17)
	var knight:=s.find_unit(6)
	var priest:=s.find_unit(8)
	assert_false(s.command_attack(8,6))
	assert_false(s.command_attack(3,6))
	knight.limits.hp-=1
	assert_true(s.command_move(8,knight.cell))
	assert_eq(s.battle_trace().commands.back(),[0,4,8,6])
	s._hit(priest,knight)
	assert_eq(knight.limits.hp,knight.limits.hp_max)
	var caster:=s.find_unit(3)
	assert_false(s.cast_field_spell(8,priest.cell,59))
	assert_false(s.cast_field_spell(3,Vector2i(-1,0),57))
	var mp:int=caster.limits.mp
	caster.limits.mp=14
	assert_false(s.cast_field_spell(3,caster.cell,57))
	assert_false(s.cast_field_spell(3,caster.cell,59))
	caster.limits.mp=mp
	assert_true(s.cast_field_spell(3,knight.cell,57))
	assert_eq(caster.limits.mp,mp-15)
	assert_false(s.cast_field_spell(3,caster.cell,59))
	for t in 30:s.tick()
	assert_true(knight.get("barrier_until",0)>s.elapsed)
	assert_true(s._packet(knight)["evasion"]>knight.combat.evasion)
	for t in 31:s.tick()
	var before_lightning: int=caster.limits.mp
	assert_true(s.cast_field_spell(3,caster.cell,59))
	assert_eq(caster.limits.mp,before_lightning-75)
	var trace:=s.battle_trace()
	assert_true(Records.valid_trace(trace,true,false,false,true))
	assert_false(Records.valid_trace(trace,true,false,true))
	assert_false(Records.valid_trace(trace,true,true))
	s.close()


func test_right_click_wounded_ally_issues_healing_order() -> void:
	var source:=_open()
	source.close()
	var trial:=preload("res://ui/school_sortie_trial.gd").new()
	(Engine.get_main_loop() as SceneTree).root.add_child(trial)
	assert_true(trial.open_trial(context,{},{}))
	while trial.session._ending_phase=="opening":trial._continue()
	trial.member_buttons[8].pressed.emit()
	var patient: Dictionary=trial.session.find_unit(6)
	patient.limits.hp-=1
	var click:=InputEventMouseButton.new()
	click.button_index=MOUSE_BUTTON_RIGHT
	click.pressed=true
	click.position=trial.canvas.point(patient.cell)
	trial.canvas._gui_input(click)
	assert_eq(trial.session.battle_trace().commands.back(),[0,4,8,6])
	trial.free()
