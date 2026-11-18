extends "res://sim/tests/test_base.gd"
const Session := preload("res://sim/school_sortie_session.gd")
const Helpers := preload("res://sim/tests/test_school_return_courses.gd")
const Adventures := preload("res://sim/school_return_adventures.gd")
const Return := preload("res://sim/school_postbattle_return.gd")


func handoff(id: int, waiting := false) -> Dictionary:
	var bundle := Helpers.new()._returned()
	bundle=Return.move_member(bundle,{"kind":"student","member_id":5,"target_group":0,"target_slot":3})["after"]
	if waiting:bundle=Return.move_member(bundle,{"kind":"student","member_id":9,"target_group":-1,"target_slot":-1})["after"]
	var ledger := Adventures.initial();bundle=Adventures.select(bundle,ledger,id)["after"]
	return Adventures.submit(bundle,ledger)["handoff"]


func start(session) -> void:
	while session.ending_snapshot()["phase"]=="opening":assert_true(session.advance_opening(true))


func test_saved_four_members_current_growth_and_distinct_maps() -> void:
	for id in [8,17]:
		var source := handoff(id);var before := source.duplicate(true);var session := Session.new()
		assert_true(session.open(source),"open%d" % id)
		if not session.ready:continue
		assert_eq(session.controlled_units().map(func(u):return u["character_id"]),[3,4,9,5])
		assert_eq(session.field_width,64 if id==8 else 96);assert_eq(session.field_height,96 if id==8 else 144)
		assert_eq(session.units.size(),40 if id==8 else 61)
		for unit in session.controlled_units():
			var growth: Dictionary=source["growth"].filter(func(g):return g["character_id"]==unit["character_id"])[0]
			assert_eq(unit["input"]["attributes"],growth["attributes"])
			assert_eq(unit["input"]["level"],growth["level_50"])
			assert_true(session.walkable(unit["cell"]))
		assert_eq(source,before)
		session.tick();assert_eq(session.frame,0);start(session);session.tick();assert_eq(session.frame,1)
		assert_true(session.request_return())
		for i in range(5):session.advance_exit()
		assert_eq(session.ending_snapshot()["phase"],"summary")
		assert_eq(session.ending_snapshot()["summary"]["rewards_applied"],false)
		session.close();assert_false(session.ready);assert_true(session.units.is_empty())


func test_waiting_member_rejected_data_and_atomic_reopen() -> void:
	var session := Session.new();var source := handoff(17,true)
	assert_true(session.open(source));if not session.ready:return
	assert_eq(session.controlled_units().map(func(u):return u["character_id"]),[3,4,5])
	var before := session.read_units()
	var bad := source.duplicate(true);bad["scene"]["script"]="T0005.BIN"
	assert_false(session.open(bad));assert_eq(session.read_units(),before)
	bad=source.duplicate(true);bad.erase("date")
	assert_false(session.open(bad));assert_eq(session.read_units(),before)
	bad=source.duplicate(true);bad["date"]=[5,4]
	assert_false(session.open(bad));assert_eq(session.read_units(),before)
	bad=source.duplicate(true);bad["participants"][0]["attributes"][0]+=1
	assert_false(session.open(bad));assert_eq(session.read_units(),before)
	assert_false(session.open(source,{},"{}"));assert_eq(session.read_units(),before)


func test_source_timed_defense_priority_and_no_clear_enemy_win() -> void:
	var session := Session.new();assert_true(session.open(handoff(8)));if not session.ready:return
	start(session)
	for enemy in session.enemies():enemy["limits"]["hp"]=0;enemy["source_state"]=4
	assert_false(session._detect_trial_end(),"clear enemies does not finish defense")
	session.elapsed=8998;session._update_summoning()
	assert_eq(session.units.filter(func(u):return u.get("group")==25 and u["source_state"]==1).size()+session._pending_activations.size(),6,"9000 wave places or queues all six without overlapping")
	assert_eq(session.units.filter(func(u):return u.get("group")==10 and u["source_state"]==1).size(),0)
	session.elapsed=108000
	assert_true(session._detect_trial_end());assert_eq(session.ending_snapshot()["script_sub"],8)
	var lost := Session.new();assert_true(lost.open(handoff(8)));start(lost)
	for number in [3,4,5]:lost.find_unit(1250-number)["side"]=5
	for unit in lost.controlled_units():unit["limits"]["hp"]=0
	assert_true(lost._detect_trial_end());assert_eq(lost.ending_snapshot()["script_sub"],15)


func test_training_original_exit_cells_early_exit_and_rating() -> void:
	var session := Session.new();assert_true(session.open(handoff(17)));if not session.ready:return
	start(session);assert_false(session._at_exit())
	assert_eq(session.catalog["exit_cells"],[1530,1626,1627,1723,1724,1820])
	var unit: Dictionary=session.controlled_units()[0];unit["cell"]=Vector2i(92,18)
	assert_true(session._at_exit());assert_true(session._detect_trial_end());assert_eq(session.ending_snapshot()["script_sub"],14)
	var complete := Session.new();assert_true(complete.open(handoff(17)));start(complete)
	complete.elapsed=54000;complete.controlled_units()[0]["cell"]=Vector2i(90,15)
	for actor in complete.units:
		if Session._capture_role(actor["character_id"]):actor["side"]=0
		if actor["character_id"] in range(411,415):actor["source_state"]=4;actor["limits"]["hp"]=0
	assert_eq(complete._training_objectives(),[true,true,true])
	assert_true(complete._detect_trial_end());assert_eq(complete.ending_snapshot()["script_sub"],2)


func test_fana_fields_match_original_instruction_record() -> void:
	var data: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://data/school_postbattle_return_rules.json"))["candidate"]
	data=Session.Limits._source_numbers(data)
	var rules: Dictionary=Session.Limits._source_numbers(JSON.parse_string(FileAccess.get_file_as_string(Session.SOURCE_PATH)))["attack_rules"]
	var unit := Session.PlayerUnits.project(data,data,rules)
	assert_false(unit.is_empty())
	assert_eq([unit["limits"]["hp"],unit["limits"]["mp"],unit["combat"]["accuracy"],unit["combat"]["power"],unit["combat"]["power_range"]],[259,161,149,36,10])


func test_current_growth_changes_combat_and_real_commands_advance() -> void:
	var source := handoff(17);var session := Session.new();assert_true(session.open(source));if not session.ready:return
	start(session)
	var player: Dictionary=session.controlled_units()[0]
	var start_cell: Vector2i=player["cell"]
	var destination := Vector2i(-1,-1)
	for d in SimPath.DIRS:
		if session.command_move(player["character_id"],start_cell+d):destination=start_cell+d;break
	assert_true(destination.x>=0)
	# Keep this movement regression bounded; normal enemy scheduling runs as well.
	for i in range(12):session.tick()
	assert_eq(player["cell"],destination)
	var target: Dictionary=session.enemies()[0]
	assert_true(session.command_attack(player["character_id"],session.unit_key(target)))
	assert_eq(player["target"],session.unit_key(target));assert_true(session.stop(player["character_id"]))
	assert_eq(player["target"],-1)
	var changed := source.duplicate(true)
	for rows in [changed["growth"],changed["participants"]]:rows[0]["attributes"][5]+=10
	var grown := Session.new();assert_true(grown.open(changed))
	assert_true(grown.controlled_units()[0]["limits"]["hp_max"]>player["limits"]["hp_max"])


func test_congested_reinforcements_do_not_duplicate_or_resurrect_from_stale_requests() -> void:
	var session := Session.new();assert_true(session.open(handoff(8)));if not session.ready:return
	start(session)
	var center := Vector2i(7,93)
	session._spawn_group(25,center,3)
	var queued := session._pending_activations.size()
	assert_true(queued>0,"source spawn is intentionally narrow")
	session._spawn_group(25,center,3)
	assert_eq(session._pending_activations.size(),queued)
	var pending: Dictionary=session._pending_activations[0]
	# A different free source-valid destination lets the queued record enter.
	assert_true(session._activate(pending["identity"],Vector2i(20,20),15))
	assert_false(session._pending_activations.any(func(r):return r["identity"]==pending["identity"]))
	var revived: Dictionary=session.find_unit(pending["identity"])
	revived["source_state"]=4;revived["limits"]["hp"]=0
	session._attempt_activations();assert_eq(revived["source_state"],4)


func test_training_parameter_timers_and_repeat_select_only_inactive_enemy_groups() -> void:
	var session := Session.new();assert_true(session.open(handoff(17)));if not session.ready:return
	start(session);session.elapsed=10798;session._update_summoning()
	var group: Array=session.units.filter(func(u):return u.get("group",0)==5)
	assert_false(group.is_empty())
	for unit in group:assert_eq(unit["source_ai_request"],[0,5,1])
	for unit in group:unit["source_state"]=4;unit["limits"]["hp"]=0
	session._repeat_group()
	assert_true(group.any(func(u):return u["source_state"]==1) or not session._pending_activations.is_empty())
