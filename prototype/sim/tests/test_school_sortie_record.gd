extends "res://sim/tests/test_base.gd"
const Record := preload("res://sim/school_sortie_record.gd")
const Helpers := preload("res://sim/tests/test_school_sortie_session.gd")


func test_objective_inputs_follow_scene_and_current_owners() -> void:
	for id in [8,17]:
		var session := Record.Sortie.new()
		assert_true(session.open(Helpers.new().handoff(id)))
		Helpers.new().start(session)
		session.find_unit(1249)["side"]=0
		session.find_unit(1248)["side"]=5
		if id==17:
			session.find_unit(1247)["side"]=0
			session.controlled_units()[0]["cell"]=Vector2i(90,15)
		else:
			session.elapsed=108000
		assert_true(session._detect_trial_end())
		for i in range(4): session.advance_exit()
		var facts := session.result_inputs()
		assert_eq(facts["objective_slots"].slice(0,3),[1,0,1 if id==17 else 0])
		assert_eq(facts["objective_slots"].slice(3).count(0),13)
		assert_eq(facts["time_key"],0)
		assert_eq(facts["units"].map(func(u):return u["character_id"]),[3,4,9,5])


func test_abort_and_forged_trace_cannot_create_a_result() -> void:
	var handoff := Helpers.new().handoff(17)
	var session := Record.Sortie.new()
	assert_true(session.open(handoff))
	assert_true(session.request_return())
	assert_false(Record.replay(handoff,session.battle_trace())["supported"])
	var trace := session.battle_trace()
	trace["result_selector"]=1
	assert_false(Record.replay(handoff,trace)["supported"])
