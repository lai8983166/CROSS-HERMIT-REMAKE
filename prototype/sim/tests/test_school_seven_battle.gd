extends "res://sim/tests/test_base.gd"
const Battles := preload("res://sim/tests/test_school_sortie_session.gd")
const Session := preload("res://sim/school_sortie_session.gd")


# Focused objective predicates use a one-class projection. The campaign suite
# exercises the two actual saved classes and legal command replay through town.
func _scenario() -> Session:
	var source := Battles.new().handoff(8)
	source["date"]=[5,4]
	source["prepared"]["adventure_id"]=7
	source["prepared"]["rounds"][0]["scene_id"]=7
	source["scene"]=Session.Adventures.seven_rules()["scene"]
	var session := Session.new()
	assert_true(session.open(source))
	if session.ready:Battles.new().start(session)
	return session


func test_rendezvous_ownership_and_escort_identity() -> void:
	var session := _scenario()
	if not session.ready:return
	assert_eq([session.field_width,session.field_height],[96,144])
	assert_eq(session.reserves.size(),68)
	assert_eq(session.units.size(),53+4)
	assert_eq(session.catalog["regions"]["1"].size(),34)
	assert_eq(session.catalog["regions"]["2"].size(),54)
	assert_false(session.command_move(1248,Vector2i(7,123)))
	session.find_unit(3)["cell"]=Vector2i(68,25)
	assert_true(session._detect_trial_end())
	assert_eq(session._ending_phase,"event20")
	assert_eq(session._event_pages.size(),13)
	for i in range(13):assert_true(session.advance_event())
	assert_true(session.rendezvous)
	for id in [1248,1247]:
		assert_true(session.find_unit(id)["controllable"])
		assert_eq(session.find_unit(id)["side"],0)
	session.find_unit(1247)["cell"]=Vector2i(7,123)
	assert_false(session._detect_trial_end())
	session.find_unit(1248)["cell"]=Vector2i(7,123)
	assert_true(session._detect_trial_end())
	assert_eq(session.ending_sub,8)
	session.close()


func test_source_timer_slots_and_group_revive() -> void:
	var session := _scenario()
	if not session.ready:return
	assert_eq(session.recurring_events.map(func(row):return row["at"]),[600,800,1000,1200])
	assert_eq(session.timers.size(),6)
	session.find_unit(1246)["side"]=0
	session._update_summoning()
	assert_eq(session.timers.map(func(row):return row["slot"]),[0,4,5])
	session.find_unit(1245)["side"]=0
	session._update_summoning()
	assert_eq(session.timers.map(func(row):return row["slot"]),[0])
	session.elapsed=43198
	session._update_summoning()
	assert_true(session.find_unit(1196)["source_state"]==1)
	for unit in session.units:
		if unit.get("group",0)==1:
			unit["source_state"]=4
			unit["limits"]["hp"]=0
	session._repeat_seven_group()
	assert_true(session.units.any(func(u):return u.get("group",0)==1 and u["source_state"]==1))
	session.close()


func test_seven_grades_time_and_only_chest_loot_slot() -> void:
	for sample in [[0,2,36000,1],[1,5,36001,2],[2,11,54000,2],[3,14,54001,3]]:
		var session := _scenario()
		if not session.ready:return
		session.rendezvous=true
		session.find_unit(1248)["cell"]=Vector2i(7,123)
		for id in [1249,1246,1245]:session.find_unit(id)["side"]=0
		session.elapsed=sample[2]
		if sample[0]==1:session._own_casualties=1
		if sample[0]==2:
			for unit in session.controlled_units():unit["limits"]["hp"]=0
		if sample[0]==3:
			session.find_unit(1248)["limits"]["hp"]=0
			session.find_unit(1248)["source_state"]=4
		assert_true(session._detect_trial_end())
		assert_eq(session.ending_sub,sample[1])
		for i in 4:session.advance_exit()
		var facts := session.result_inputs()
		assert_eq(facts["time_key"],sample[3])
		assert_eq(facts["objective_slots"],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
		assert_eq(facts["units"].size(),4)
		session.close()
