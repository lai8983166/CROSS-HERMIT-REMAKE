extends "res://sim/tests/test_base.gd"
const Combat := preload("res://sim/school_combat_session.gd")
const Playground := preload("res://sim/school_playground.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")


func _school():
	var model := Playground.new()
	var fixture: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_playground_legacy_v3.json")))
	assert_true(model.restore(fixture["cases"][1]["save"])["supported"])
	for op in ["workroom_open","work_start","work_skip","school_enter"]: assert_true(model.execute({"op":op})["supported"])
	return model


func _combat(model):
	var session := Combat.new()
	assert_true(session.open(model.adventure_preparation(),model.adventure_combat_limits()))
	_finish_opening(session)
	return session


func _finish_opening(session) -> void:
	for index in range(10):
		assert_true(session.advance_opening(session.opening_snapshot()["awaiting_confirmation"]))
	assert_eq(session.ending_snapshot()["phase"],"active")


func _declared_nearby_geometry(session, enemy_id := 1243) -> void:
	# Explicit local test geometry; never an original world/placement witness.
	var player: Dictionary = session.find_unit(3); var enemy: Dictionary = session.find_unit(enemy_id)
	for y in range(-3,4):
		for x in range(-3,4):
			var cell: Vector2i = enemy["cell"]+Vector2i(x,y)
			if cell == enemy["cell"] or not session.walkable(cell) or session._blocked(3).has(cell): continue
			player["cell"] = cell; player["from_cell"] = cell
			return
	assert_true(false,"declared encounter has a valid nearby source cell")


func test_source_initial_actors_current_students_and_unique_instance_ids() -> void:
	var model = _school(); var before: Dictionary = model.state(); var save: Dictionary = model.export_save()
	var session = _combat(model)
	assert_eq(session.units.size(),14); assert_eq(session.enemies().size(),7)
	assert_eq(session.controlled_units().map(func(u): return u["character_id"]),[3,4,9])
	var keys := {}
	for unit in session.units:
		assert_false(keys.has(session.unit_key(unit))); keys[session.unit_key(unit)] = true
		if not unit["controllable"]:
			var actor: Dictionary = session.source_actors[session.unit_key(unit)]
			assert_eq(unit["cell"],Vector2i(actor["cell"][0],actor["cell"][1]))
			assert_eq(unit["limits"],actor["limits"])
	assert_eq(session.find_unit(3)["combat"]["power"],27)
	assert_eq(session.find_unit(4)["combat"]["accuracy"],91)
	assert_eq(session.find_unit(9)["combat"]["magic_resist"],53)
	assert_eq(model.state(),before); assert_eq(model.export_save(),save)


func test_player_attack_moves_then_hits_without_moving_source_stationary_opponents() -> void:
	var session = _combat(_school())
	var source_positions: Dictionary = {}
	for enemy in session.enemies(): source_positions[enemy["instance_id"]] = enemy["cell"]
	assert_true(session.command_attack(3,1243))
	for index in range(1600): session.tick()
	assert_false(session.events.is_empty(),"actual local scheduler moves into source range and releases attacks")
	assert_lt(session.find_unit(1243)["limits"]["hp"],162)
	for key in source_positions: assert_eq(session.find_unit(key)["cell"],source_positions[key],"source movement_rate0 never chases")
	assert_eq(session.find_unit(3)["limits"]["mp"],445,"basic attacks invent no skill resource spending")


func test_protected_invalid_dead_and_nonplayer_commands_refuse_atomically() -> void:
	var session = _combat(_school())
	assert_true(session.command_attack(3,1243))
	var before: Array = session.read_units()
	for key in [101,9999,3,4,1249,1248,1247,1217]:
		assert_false(session.command_attack(3,key)); assert_eq(session.read_units(),before)
	assert_false(session.command_attack(1243,3)); assert_false(session.select(1243))
	assert_false(session.command_move(1243,Vector2i(10,20)))
	session.find_unit(1243)["limits"]["hp"] = 0
	before = session.read_units()
	assert_false(session.command_attack(3,1243)); assert_eq(session.read_units(),before)


func test_ranged_attack_reaches_firing_cell_without_enemy_adjacency() -> void:
	var session = _combat(_school())
	var player: Dictionary = session.find_unit(3); var enemy: Dictionary = session.find_unit(1243)
	# Declared obstruction geometry exercises range seeking, rather than original placement.
	var blockers := [1249,1248,1247,1217]
	for index in range(4):
		var obstacle: Dictionary = session.find_unit(blockers[index])
		obstacle["cell"] = enemy["cell"]+[Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN][index]
		obstacle["from_cell"] = obstacle["cell"]
	var path: Array = session._attack_path(player,enemy)
	assert_false(path.is_empty(),"ranged firing cell is reachable even when all adjacent cells are occupied")
	var goal: Vector2i = path.back()
	var distance := absi(goal.x-enemy["cell"].x)+absi(goal.y-enemy["cell"].y)
	assert_true(distance > 1 and distance <= player["combat"]["attack_range"])
	for cell in path:
		assert_true(session.walkable(cell,player["movement_type"]))
		assert_false(session._blocked(3).has(cell))


func test_nearby_cast_pause_stop_and_enemy_retaliation() -> void:
	var session = _combat(_school()); _declared_nearby_geometry(session)
	assert_true(session.command_attack(3,1243)); session.tick()
	assert_true(session.phases.has(3)); assert_eq(session.find_unit(3)["visual"],"cast")
	var before: Array = session.read_units(); var phases: Dictionary = session.phases.duplicate(true); var frame: int = session.frame
	session.paused = true; session.advance(1000); session.tick()
	assert_eq(session.frame,frame); assert_eq(session.read_units(),before); assert_eq(session.phases,phases)
	session.paused = false
	assert_true(session.stop(3)); assert_false(session.phases.has(3)); assert_eq(session.find_unit(3)["target"],-1)
	for index in range(400): session.tick()
	assert_eq(session.find_unit(1243)["limits"]["hp"],162,"stopped player attack cannot release delayed damage")
	assert_lt(session.find_unit(3)["limits"]["hp"],117,"nearby source opponent retaliates under declared trial scheduler")


func test_seeded_attack_replay_and_nonoverlapping_paths_are_deterministic() -> void:
	var model = _school(); var a = _combat(model); var b = _combat(model)
	for session in [a,b]: assert_true(session.command_attack(3,1243))
	for index in range(1400):
		a.tick(); b.tick()
		assert_eq(a.events,b.events)
		assert_eq(a.read_units(),b.read_units())
		var used := {}
		for unit in a.units:
			if unit["limits"]["hp"] <= 0: continue
			assert_false(used.has(unit["cell"])); used[unit["cell"]] = true


func test_death_cancels_phases_and_completion_has_no_school_authority() -> void:
	var model = _school(); var state: Dictionary = model.state(); var save: Dictionary = model.export_save()
	var session = _combat(model)
	for enemy in session.enemies().duplicate():
		_declared_nearby_geometry(session,enemy["instance_id"])
		for index in range(200):
			if enemy["limits"]["hp"] <= 0: break
			session._hit(session.find_unit(3),enemy)
		assert_eq(enemy["limits"]["hp"],0); assert_false(session.phases.has(enemy["instance_id"]))
		assert_false(session._blocked(3).has(enemy["cell"]),"dead trial actor releases collision")
	session.tick(); assert_false(session.trial_complete); assert_true(session.enemies().is_empty())
	assert_eq(session.ending_snapshot()["phase"],"active","initial clear does not imply mission completion")
	assert_eq(model.state(),state); assert_eq(model.export_save(),save)
	assert_eq(model.fifth_session.read_snapshot()["adventure_gate"],1)
	session.close(); assert_true(session.units.is_empty()); assert_true(session.phases.is_empty()); assert_true(session.events.is_empty())
	assert_true(session.open(model.adventure_preparation(),model.adventure_combat_limits()))
	assert_eq(session.enemies().size(),7); assert_eq(session.find_unit(1243)["limits"]["hp"],162); assert_eq(session.frame,0)


func test_invalid_reopen_and_waiting_squad_preserve_owned_state() -> void:
	var model = _school(); var session = _combat(model); var units: Array = session.read_units()
	assert_false(session.open({},model.adventure_combat_limits())); assert_eq(session.read_units(),units)
	assert_false(session.open(model.adventure_preparation(),model.adventure_combat_limits(),"{}")); assert_eq(session.read_units(),units)
	assert_true(model.execute({"op":"plan_move","kind":"student","member_id":9,"target_group":-1,"target_slot":-1})["supported"])
	var save: Dictionary = model.export_save()
	assert_true(session.open(model.adventure_preparation(),model.adventure_combat_limits()))
	assert_eq(session.units.size(),13); assert_true(session.find_unit(9).is_empty()); assert_eq(session.enemies().size(),7)
	assert_eq(model.export_save(),save)


func _capture_and_read_event(session) -> void:
	# Local near-event fixture: clear guards and place a living pupil near the
	# source spring. Ownership still changes through the actual session stages.
	for enemy in session.enemies(): enemy["limits"]["hp"] = 0
	_declared_nearby_geometry(session,1247)
	for index in range(80):
		session.tick()
		if session.ending_snapshot()["phase"] == "event20": break
	assert_eq(session.ending_snapshot()["phase"],"event20")
	assert_true(session.progression_snapshot()["spring_owned"])
	assert_true(session.find_unit(1239).is_empty(),"boss request follows dialogue")
	var units: Array = session.read_units(); var frame: int = session.frame
	var time: int = session.remaining_ticks
	session.advance(10); session.tick()
	assert_eq(session.read_units(),units); assert_eq(session.frame,frame); assert_eq(session.remaining_ticks,time)
	var pages: int = session.progression_snapshot()["event_pages"]
	for index in pages: assert_true(session.advance_event())
	assert_false(session.advance_event(),"cannot issue event twice")
	assert_eq(session.ending_snapshot()["phase"],"active")


func test_capture_event_spawns_source_groups_boss_and_allied_fana() -> void:
	var model = _school(); var save: Dictionary = model.export_save(); var session = _combat(model)
	assert_false(session.progression_snapshot()["spring_owned"])
	assert_false(session.command_move(3,session.find_unit(1247)["cell"]),"clicking the occupied spring does not capture it")
	_capture_and_read_event(session)
	assert_eq(session.enemies().size(),16,"five three-unit groups plus boss; summon reserves stay inactive")
	assert_eq(session.find_unit(1239)["character_id"],452)
	assert_eq(session.controlled_units().size(),4)
	assert_eq(session.find_unit(1249)["character_id"],5); assert_eq(session.find_unit(1249)["side"],0)
	assert_true(session.catalog["skins"]["scene_4_v5"]["actions"].has("attack"))
	var cells := {}
	for unit in session.units:
		if unit["limits"]["hp"]<=0: continue
		assert_false(cells.has(unit["cell"]),"source placement reserves every chosen cell")
		cells[unit["cell"]] = true
		assert_true(session.walkable(unit["cell"],unit["movement_type"]))
	assert_eq(model.export_save(),save,"event has no persistent roster effect")


func test_boss_actual_hit_waits_for_removal_then_consumes_selected_result() -> void:
	var model = _school(); var save: Dictionary = model.export_save(); var session = _combat(model)
	_capture_and_read_event(session)
	# Keep other reinforcements alive: success does not require full enemy clear.
	_declared_nearby_geometry(session,1239)
	var boss: Dictionary = session.find_unit(1239); boss["limits"]["hp"] = 1
	assert_true(session.command_attack(3,1239))
	for index in range(300):
		session.tick()
		if boss["limits"]["hp"]==0: break
	assert_eq(boss["limits"]["hp"],0); assert_eq(session.ending_snapshot()["phase"],"active")
	assert_true(session.events.any(func(e): return e["target"]==1239 and e["after_hp"]==0))
	for index in range(32):
		session.tick()
		if session.ending_snapshot()["phase"] != "active": break
	assert_eq(boss["source_state"],4)
	assert_eq(session.ending_snapshot()["outcome"],"mission_objectives_met")
	assert_true(session.enemies().size()>0)
	assert_eq(session.ending_snapshot()["summary"]["terminal_choice"]["tactical_result_selector"],1)
	assert_false(session.ending_snapshot()["consumer"]["result_consumed"])
	for index in range(4): session.advance_exit()
	assert_eq(session.ending_snapshot()["phase"],"summary")
	assert_eq(session.take_handoff()["outcome"],"mission_objectives_met")
	assert_eq(model.export_save(),save)


func test_summon_capacity_animation_gate_and_last_rebirth() -> void:
	var session = _combat(_school()); _capture_and_read_event(session)
	var boss: Dictionary = session.find_unit(1239)
	# Direct local AI opportunities keep the source interval distinct from ticks.
	for index in range(149): session._update_summoning()
	assert_eq(boss["summon_phase"],"")
	session._update_summoning(); assert_eq(boss["summon_phase"],"prepare")
	for index in range(180): session._update_summoning()
	assert_eq(boss["summon_phase"],"animation")
	assert_eq(session.enemies().size(),16)
	for index in range(boss["summon_remaining"]): session._update_summoning()
	assert_eq(session.enemies().size(),24)
	var summoned: Array = session.units.filter(func(u): return u.get("group",0)==1 and u.get("life_kind",0)==3)
	assert_eq(summoned.size(),8)
	var unit: Dictionary = summoned[0]; var identity: int = session.unit_key(unit)
	unit["lives"] = 1; unit["limits"]["hp"] = 0; unit["dead_at"] = session.frame-30
	session._update_removal()
	assert_eq(unit["source_state"],2); assert_eq(unit["lives"],0,"last decremented life still returns to reserve")
	assert_true(session._activate(identity,boss["cell"],8))
	unit["limits"]["hp"] = 0; unit["dead_at"] = session.frame-30
	session._update_removal(); assert_eq(unit["source_state"],4)
	assert_false(session._activate(identity,boss["cell"],8),"exhausted source record cannot return")


func test_pending_appearance_retry_and_summon_animation_survive_movement_tick() -> void:
	var session = _combat(_school()); _capture_and_read_event(session)
	var reserve_id := -1
	var blocker: Dictionary = session.find_unit(3)
	var center: Vector2i = blocker["cell"]
	for identity in session.reserves:
		if session._source_status(identity)["state"]==0 and session.walkable(center,session.reserves[identity]["movement_type"]):
			reserve_id=identity; break
	assert_true(reserve_id>=0)
	if reserve_id<0: return
	# Radius0 is deliberately occupied; no fallback spawn or silent lost request.
	session._pending_activations.append({"identity":reserve_id,"center":center,"radius":0})
	session._attempt_activations(); assert_eq(session.progression_snapshot()["pending_activations"],1)
	var boss: Dictionary = session.find_unit(1239)
	for delta in [Vector2i.UP,Vector2i.DOWN,Vector2i.LEFT,Vector2i.RIGHT]:
		if session.walkable(center+delta,blocker["movement_type"]) and not session._blocked(3).has(center+delta):
			blocker["cell"] = center+delta; blocker["from_cell"] = blocker["cell"]; break
	session._attempt_activations(); assert_eq(session.progression_snapshot()["pending_activations"],0)
	assert_eq(session.find_unit(reserve_id).get("cell"),center)
	boss["summon_clock"] = 149; session.tick()
	assert_eq(boss["summon_phase"],"prepare")
	assert_eq(boss["visual"],"summon_prepare","parent movement cannot replace summon with idle")


func test_allied_fana_participates_in_unavailable_check_and_can_attack() -> void:
	var session = _combat(_school()); _capture_and_read_event(session)
	for student in session.controlled_units():
		if session.unit_key(student)!=1249: student["limits"]["hp"] = 0
	session.tick()
	assert_eq(session.ending_snapshot()["phase"],"active","living allied ID5 prevents all-playable-unavailable")
	assert_true(session.select(1249)); assert_true(session.command_attack(1249,1239))
	var ally: Dictionary = session.find_unit(1249); var boss: Dictionary = session.find_unit(1239)
	ally["cell"] = boss["cell"]+Vector2i.DOWN; ally["from_cell"] = ally["cell"]
	session.tick(); assert_true(session.phases.has(1249),"original ally attack art/action is usable")
	ally["limits"]["hp"] = 0; session.tick()
	assert_eq(session.ending_snapshot()["outcome"],"squad_defeated")
	assert_eq(session.ending_snapshot()["summary"]["terminal_choice"]["selector_arg"],14)
	assert_eq(session.ending_snapshot()["summary"]["terminal_choice"]["script_sub"],8)


func test_requested_exit_consumes_results_in_order_without_damage_or_school_writes() -> void:
	var model = _school(); var school: Dictionary = model.state(); var save: Dictionary = model.export_save()
	var session = _combat(model)
	assert_true(session.command_attack(3,1243)); session.paused = true
	assert_true(session.request_return(), "return works while combat is paused")
	var started: Dictionary = session.ending_snapshot()
	assert_eq(started["phase"],"consuming"); assert_eq(started["outcome"],"player_exit")
	assert_false(started["consumer"]["result_consumed"], "end trigger does not skip the first wait")
	assert_false(session.request_return(), "duplicate exit cannot replace the pending frame")
	assert_true(session.take_handoff().is_empty(), "cannot leave before result consumption")
	var units: Array = session.read_units(); var events: Array = session.events.duplicate(true)
	assert_false(session.command_attack(3,1243)); assert_false(session.command_move(3,Vector2i(1,1)))
	assert_false(session.stop(3)); assert_false(session.select(4))
	session.advance(1.0/240.0)
	assert_eq(session.ending_snapshot()["consumer"]["action"],"call_replay_record")
	assert_true(session.take_handoff().is_empty())
	session.advance(10.0)
	assert_eq(session.ending_snapshot()["consumer"]["wait_ordinal"],2)
	session.tick()
	assert_eq(session.ending_snapshot()["consumer"]["wait_ordinal"],3)
	assert_eq(session.ending_snapshot()["phase"],"consuming")
	session.advance_exit()
	assert_eq(session.ending_snapshot()["phase"],"summary")
	assert_eq(session.ending_snapshot()["replay_record_calls"],1)
	assert_eq(session.read_units(),units); assert_eq(session.events,events)
	var handoff: Dictionary = session.take_handoff()
	assert_eq(handoff["successor"],"school_adventure_preparation")
	assert_false(handoff["authorizes_persistent_write"]); assert_false(handoff["native_equivalence_verified"])
	assert_false(handoff["summary"]["rewards_applied"]); assert_false(handoff["summary"]["campaign_advanced"])
	assert_true(session.take_handoff().is_empty(), "one handoff only")
	assert_eq(model.state(),school); assert_eq(model.export_save(),save)
	session.close()
	assert_true(session.units.is_empty()); assert_true(session.phases.is_empty()); assert_true(session.events.is_empty())
	assert_eq(session.ending_snapshot()["phase"],"closed")
	assert_true(session.open(model.adventure_preparation(),model.adventure_combat_limits()))
	assert_eq(session.ending_snapshot()["phase"],"opening"); assert_eq(session.enemies().size(),7)
	_finish_opening(session)


func test_last_initial_hit_keeps_mission_open_until_explicit_exit() -> void:
	var model = _school(); var save: Dictionary = model.export_save(); var session = _combat(model)
	# Explicit local near-terminal fixture. The last HP change comes from the
	# actual remake attack scheduler, not a fabricated completion/consumer flag.
	for enemy in session.enemies(): enemy["limits"]["hp"] = 1 if enemy["instance_id"] == 1243 else 0
	_declared_nearby_geometry(session)
	assert_true(session.command_attack(3,1243))
	for index in range(600):
		session.tick()
		if session.ending_snapshot()["phase"] != "active": break
	assert_eq(session.find_unit(1243)["limits"]["hp"],0)
	assert_true(session.events.any(func(event): return event["target"] == 1243 and event["after_hp"] == 0))
	assert_false(session.trial_complete); assert_eq(session.ending_snapshot()["phase"],"active")
	assert_true(session.request_return())
	assert_eq(session.ending_snapshot()["outcome"],"player_exit")
	assert_false(session.ending_snapshot()["consumer"]["result_consumed"])
	for index in range(4): session.advance_exit()
	var summary: Dictionary = session.ending_snapshot()["summary"]
	assert_eq(summary["remaining_enemies"],0); assert_eq(summary["defeated_enemies"],7)
	assert_eq(session.ending_snapshot()["phase"],"summary")
	assert_eq(model.export_save(),save, "clearing initial enemies is not formal adventure completion")


func test_squad_down_and_invalid_reopen_preserve_the_pending_end() -> void:
	var model = _school(); var session = _combat(model)
	for student in session.controlled_units(): student["limits"]["hp"] = 0
	session.tick()
	assert_eq(session.ending_snapshot()["outcome"],"squad_defeated")
	assert_false(session.trial_complete)
	var pending: Dictionary = session.ending_snapshot(); var units: Array = session.read_units()
	assert_false(session.open({},model.adventure_combat_limits()))
	assert_eq(session.ending_snapshot(),pending); assert_eq(session.read_units(),units)
	pending["summary"]["outcome"] = "changed externally"
	assert_eq(session.ending_snapshot()["summary"]["outcome"],"squad_defeated")
	for index in range(4): session.advance_exit()
	assert_eq(session.ending_snapshot()["phase"],"summary")
	assert_eq(session.ending_snapshot()["summary"]["surviving_students"],0)
	assert_eq(session.ending_snapshot()["summary"]["remaining_enemies"],7)


func test_opening_confirmation_groups_freeze_combat_until_final_handoff() -> void:
	var model = _school(); var session := Combat.new(); var save: Dictionary = model.export_save()
	assert_true(session.open(model.adventure_preparation(),model.adventure_combat_limits()))
	var units: Array = session.read_units(); var random_state: int = session.rng.state
	var expected: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(Combat.OPENING_PATH))
	var confirmations := 0
	for index in range(10):
		var opening: Dictionary = session.opening_snapshot()
		assert_eq(opening["page_index"],index); assert_eq(opening["page"],expected["pages"][index])
		assert_eq(session.ending_snapshot()["phase"],"opening")
		assert_false(session.select(4)); assert_false(session.command_move(3,Vector2i(10,20)))
		assert_false(session.command_attack(3,1243)); assert_false(session.stop(3))
		session.tick(); session.advance(100.0)
		assert_eq(session.frame,0); assert_eq(session.read_units(),units)
		assert_eq(session.rng.state,random_state); assert_true(session.events.is_empty())
		var confirmation: bool = index in [1,2,6,9]
		assert_eq(opening["awaiting_confirmation"],confirmation)
		assert_false(session.advance_opening(not confirmation),"automatic text cannot bypass a confirmation")
		assert_eq(session.opening_snapshot(),opening)
		assert_true(session.advance_opening(confirmation))
		if confirmation: confirmations += 1
	assert_eq(confirmations,4)
	assert_eq(session.ending_snapshot()["phase"],"active")
	assert_true(session.opening_snapshot()["completed"])
	assert_false(session.opening_snapshot()["original_vm_executed"])
	assert_false(session.advance_opening(true)); assert_false(session.advance_opening())
	assert_eq(session.frame,0,"dialogue time must not become overdue combat ticks")
	assert_true(session.command_attack(3,1243)); session.advance(1.0/30.0)
	assert_eq(session.frame,1)
	assert_eq(model.export_save(),save)


func test_opening_abort_and_failed_reopen_preserve_page_and_school() -> void:
	var model = _school(); var session := Combat.new(); var state: Dictionary = model.state()
	var save: Dictionary = model.export_save()
	assert_true(session.open(model.adventure_preparation(),model.adventure_combat_limits()))
	assert_true(session.advance_opening())
	var opening: Dictionary = session.opening_snapshot(); var units: Array = session.read_units()
	assert_false(session.open({},model.adventure_combat_limits()))
	assert_eq(session.opening_snapshot(),opening); assert_eq(session.read_units(),units)
	opening["page"]["text"] = "external change"
	assert_false(session.opening_snapshot()["page"]["text"] == "external change")
	assert_true(session.request_return()); assert_false(session.request_return())
	assert_false(session.advance_opening(true)); assert_false(session.opening_snapshot()["completed"])
	for index in range(4): session.advance_exit()
	assert_eq(session.ending_snapshot()["phase"],"summary")
	assert_eq(session.ending_snapshot()["outcome"],"player_exit")
	assert_eq(session.ending_snapshot()["summary"]["battle_frames"],0)
	assert_false(session.take_handoff().is_empty())
	assert_eq(model.state(),state); assert_eq(model.export_save(),save)
	session.close(); assert_eq(session.opening_snapshot()["page_count"],0)
	assert_true(session.open(model.adventure_preparation(),model.adventure_combat_limits()))
	assert_eq(session.opening_snapshot()["page_index"],0); assert_eq(session.frame,0)
