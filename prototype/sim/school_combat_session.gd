extends "res://sim/school_field_session.gd"
## Source initial actors and scalar math; scheduler/HP application are remake-only.
const Inputs := preload("res://sim/school_attack_inputs.gd")
const ResultConsumer := preload("res://sim/tactics_result_consumer.gd")
const Progression := preload("res://sim/school_scene5_progression.gd")
const Settlement := preload("res://sim/school_battle_settlement.gd")
const REINFORCEMENTS_PATH := "res://assets/school_reinforcements/catalog.json"
const REINFORCEMENTS_SHA := "4e444e53669255b9b5d926642a535962d9ea50397815b2ac0a1a7e9e8deebbe7"
const COMBAT_CATALOG := "res://assets/school_combat/catalog.json"
const COMBAT_SHA := "4d7d3e4beed860a7163bb4c4c3cd772185fc45c775425eefafb8b75f059dc70b"
const OPENING_PATH := "res://data/school_opening_dialogue.json"
const OPENING_SHA := "645cf3b69aecc6806886b79080dc66eac583527d74dac6dc90e93431c35a7a10"
# T0005 op50/51 follows text indices 1, 2, 6, 9 (file offsets 696..864).
# The remaining text advances when the Godot presentation is ready.
const OPENING_CONFIRMATIONS := [1,2,6,9]

var combat_rules: Dictionary = {}
var phases: Dictionary = {}
var events: Array[Dictionary] = []
var rng := RandomNumberGenerator.new()
var source_actors: Dictionary = {}
var trial_complete := false
var _ending_phase := "closed"
var _ending_outcome := ""
var _result_consumer: ResultConsumer
var _ending_summary: Dictionary = {}
var _initial_enemies := 0
var _record_calls := 0
var _opening_pages: Array = []
var _opening_index := -1
var reserves: Dictionary = {}
var event20_seen := false
var _event_pages: Array = []
var _event_index := -1
var _placement_rotation := 0
var _own_casualties := 0
var _terminal_choice: Dictionary = {}
# This is a remake clock, not evidence of original world-loop cadence.
var remaining_ticks := -1
var _capture_mask := PackedByteArray()
var _pending_activations: Array[Dictionary] = []
var _battle_stats: Dictionary = {}
var _participant_ids: Array = []
var _settlement: Settlement
var _settlement_error := ""
var _trace: Array = []
var _trace_clock := 0
var _trace_overflow := false


func open(preparation: Dictionary, combat: Dictionary, raw := "") -> bool:
	if not FileAccess.file_exists(OPENING_PATH): return false
	var opening_raw := FileAccess.get_file_as_string(OPENING_PATH).replace("\r\n","\n")
	if opening_raw.sha256_text() != OPENING_SHA: return false
	var opening: Dictionary = JSON.parse_string(opening_raw)
	var source_raw := FileAccess.get_file_as_string(COMBAT_CATALOG)
	if source_raw.replace("\r\n","\n").sha256_text() != COMBAT_SHA: return false
	var source: Dictionary = Limits._source_numbers(JSON.parse_string(source_raw))
	var wave_raw := FileAccess.get_file_as_string(REINFORCEMENTS_PATH).replace("\r\n","\n")
	if wave_raw.sha256_text() != REINFORCEMENTS_SHA: return false
	var waves: Dictionary = Limits._source_numbers(JSON.parse_string(wave_raw))
	var rules := Inputs.load_rules()
	if rules.is_empty(): return false
	# Build the base projection separately so every refusal preserves this session.
	var base = load("res://sim/school_field_session.gd").new()
	if not base.open(preparation,combat,raw): return false
	var settlement: Settlement
	if combat.has("result_context"):
		if not combat["result_context"] is Dictionary or combat["result_context"].get("preparation") != preparation.get("prepared"): return false
		settlement = Settlement.new()
		if not settlement.initialize(combat["result_context"]): return false
	var next_units: Array[Dictionary] = base.units.duplicate(true)
	for unit in next_units:
		var row: Dictionary = combat["students"].filter(func(r): return r["input"]["character_id"] == unit["character_id"])[0]
		var computed := Inputs.project(row["input"],rules)
		if not computed["supported"]: return false
		unit.merge({"instance_id":unit["character_id"],"controllable":true,"category":0,
			"skin_key":str(unit["character_id"]),"combat":computed["fields"],"target":-1,"dead_at":-1,
			"side":0,"source_state":1,"death_counted":false})
	var new_actors := {}
	for actor in source["actors"]:
		var key: int = actor["instance_id"]
		new_actors[key] = actor.duplicate(true)
		next_units.append({"instance_id":key,"character_id":actor["character_id"],"job":actor["job"],
			"movement_type":actor["movement_type"],"limits":actor["limits"].duplicate(true),"controllable":false,
			"category":actor["category"],"skin_key":actor["skin_key"],"combat":actor["combat"].duplicate(true),
			"cell":Vector2i(actor["cell"][0],actor["cell"][1]),"from_cell":Vector2i(actor["cell"][0],actor["cell"][1]),
			"facing":"S","path":[],"destination":Vector2i(-1,-1),"move_started_frame":-100000,
			"visual":"idle","visual_started_frame":0,"target":-1,"dead_at":-1})
		_apply_record_fields(next_units.back(),actor)
	units = next_units; catalog = base.catalog.duplicate(true); catalog["skins"] = source["skins"].duplicate(true)
	catalog["skins"].merge(waves["skins"],true)
	_maps = base._maps; _reserved.clear(); _accumulator = 0.0
	combat_rules = rules; source_actors = new_actors; phases.clear(); events.clear()
	frame = 0; paused = false; ready = true; selected_id = units[0]["character_id"]; reason = "ready"
	rng.seed = source["trial_policy"]["seed"]; trial_complete = false
	_ending_phase = "opening"; _ending_outcome = ""; _ending_summary = {}
	_result_consumer = null; _initial_enemies = enemies().size(); _record_calls = 0
	_opening_pages = opening["pages"].duplicate(true); _opening_index = 0; reason = "opening"
	reserves.clear()
	for actor in waves["actors"]: reserves[actor["instance_id"]] = actor.duplicate(true)
	_event_pages = waves["event20_dialogue"].duplicate(true); _event_index = -1
	event20_seen = false; _own_casualties = 0; _terminal_choice.clear(); remaining_ticks = 108000
	_capture_mask = String(waves["capture_mask"]["hex"]).hex_decode()
	_pending_activations.clear()
	_placement_rotation = (int(catalog["initial_rotation"])+controlled_units().size())%5
	_settlement = settlement; _settlement_error = ""; _battle_stats.clear()
	_trace.clear(); _trace_clock = 0; _trace_overflow = false
	_participant_ids = preparation["prepared"]["rounds"][0]["student_ids"].duplicate()
	for id in _participant_ids:
		_battle_stats[id] = {"character_id":id,"count_field_aa":0,"contribution_field_ac":0,"status_field_ae":0}
	return true


static func _apply_record_fields(unit: Dictionary, actor: Dictionary) -> void:
	var record := String(actor["record_hex"]).hex_decode()
	unit.merge({"side":int(record[0xa4]),"source_state":int(record[15]),
		"group":int(record[0x98]),"life_kind":int(record[0x96]),"lives":int(record[0x97]),
		"capture_hold":Progression.capture_hold_limit(record[0xa4]),"capture_target":-1,
		"capture_elapsed":-1,"summon_clock":0,"summon_phase":"","summon_remaining":0,
		"death_counted":false})


func opening_snapshot() -> Dictionary:
	var showing := ready and _ending_phase == "opening"
	return {"page_index": _opening_index, "page_count": _opening_pages.size(),
		"page": _opening_pages[_opening_index].duplicate(true) if showing else {},
		"awaiting_confirmation": showing and _opening_index in OPENING_CONFIRMATIONS,
		"completed": not _opening_pages.is_empty() and _opening_index == _opening_pages.size(),
		"original_vm_executed": false}


func advance_opening(confirmed := false) -> bool:
	if not ready or _ending_phase != "opening": return false
	if confirmed != (_opening_index in OPENING_CONFIRMATIONS): return false
	_record_command([1,1 if confirmed else 0])
	_opening_index += 1
	if _opening_index == _opening_pages.size():
		# This hands source-derived dialogue to the existing local combat trial.
		# It is not an original opcode21/world/AI resume or mission-unlock claim.
		_ending_phase = "active"; reason = "ready"; _accumulator = 0.0
	return true


func controlled_units() -> Array:
	return units.filter(func(u): return u["controllable"])


func enemies() -> Array:
	return units.filter(func(u): return u["category"] == 5 and u["limits"]["hp"] > 0)


func select(identity: int) -> bool:
	if not ready or _ending_phase != "active": return false
	var unit := find_unit(identity)
	if unit.is_empty() or not unit["controllable"]: return false
	return super.select(identity)


func _blocked(identity: int) -> Dictionary:
	var result := {}
	for unit in units:
		if unit_key(unit) != identity and unit["limits"]["hp"] > 0: result[unit["cell"]] = true
	return result


func at_cell(cell: Vector2i) -> Dictionary:
	for unit in units:
		if unit["cell"] == cell and unit["limits"]["hp"] > 0: return unit
	return {}


func command_move(identity: int, destination: Vector2i) -> bool:
	if not ready or _ending_phase != "active": return false
	var unit := find_unit(identity)
	if unit.is_empty() or not unit["controllable"] or unit["limits"]["hp"] <= 0: return false
	# Base command_move calls the virtual stop for this case. Record it once.
	if destination==unit["cell"]: return stop(identity)
	var target := at_cell(destination)
	if not target.is_empty() and target["category"] == 5:
		return command_attack(identity,unit_key(target))
	var accepted := super.command_move(identity,destination)
	if accepted:
		unit["target"] = -1; phases.erase(identity); _visual(unit,"idle")
		_record_command([3,identity,destination.x,destination.y])
	return accepted


func _admitted(unit: Dictionary, target: Dictionary) -> bool:
	if _ending_phase != "active": return false
	if unit.is_empty() or target.is_empty() or unit["limits"]["hp"] <= 0 or target["limits"]["hp"] <= 0: return false
	return (unit["controllable"] and target["category"] == 5) or (unit["category"] == 5 and target["controllable"])


func command_attack(identity: int, target_id: int) -> bool:
	var unit := find_unit(identity); var target := find_unit(target_id)
	if not ready or unit.is_empty() or not unit["controllable"] or not _admitted(unit,target): return false
	unit["target"] = target_id; phases.erase(identity); unit["path"] = []
	unit["destination"] = Vector2i(-1,-1); reason = "attack_order"
	_record_command([4,identity,target_id])
	return true


func stop(identity: int) -> bool:
	if not ready or _ending_phase != "active": return false
	var unit := find_unit(identity)
	if unit.is_empty() or not unit["controllable"] or unit["limits"]["hp"] <= 0: return false
	phases.erase(identity); unit["target"] = -1
	var accepted := super.stop(identity)
	if accepted: _record_command([5,identity])
	return accepted


func _distance(a: Dictionary, b: Dictionary) -> int:
	return absi(a["cell"].x-b["cell"].x)+absi(a["cell"].y-b["cell"].y)


func _attack_path(unit: Dictionary, target: Dictionary) -> Array[Vector2i]:
	# Reach a free firing cell, including across water; enemy-adjacent tiles need not be walkable.
	var blocked := _blocked(unit_key(unit)); var previous := PackedInt32Array()
	previous.resize(6144); previous.fill(-1)
	var start: int = unit["cell"].y*64+unit["cell"].x
	previous[start] = start
	var queue := PackedInt32Array([start]); var head := 0; var goal := -1
	while head < queue.size():
		var index: int = queue[head]; head += 1
		var cell := Vector2i(index%64,index/64)
		if absi(cell.x-target["cell"].x)+absi(cell.y-target["cell"].y) <= unit["combat"]["attack_range"]:
			goal = index; break
		for delta in SimPath.DIRS:
			var next: Vector2i = cell+delta
			if not walkable(next,unit["movement_type"]) or blocked.has(next): continue
			var next_index: int = next.y*64+next.x
			if previous[next_index] >= 0: continue
			previous[next_index] = index; queue.append(next_index)
	var result: Array[Vector2i] = []
	while goal >= 0 and goal != start:
		result.append(Vector2i(goal%64,goal/64)); goal = previous[goal]
	result.reverse()
	return result


func _face(unit: Dictionary, target: Dictionary) -> void:
	var delta: Vector2i = target["cell"]-unit["cell"]
	unit["facing"] = "NW" if delta.x < 0 and delta.y < 0 else "NE" if delta.x > 0 and delta.y < 0 \
		else "SW" if delta.x < 0 and delta.y > 0 else "SE" if delta.x > 0 and delta.y > 0 \
		else "W" if delta.x < 0 else "E" if delta.x > 0 else "N" if delta.y < 0 else "S"


func _start_attack(unit: Dictionary, target: Dictionary) -> void:
	var identity := unit_key(unit)
	unit["path"] = []; unit["destination"] = Vector2i(-1,-1); _face(unit,target)
	var skin: Dictionary = catalog["skins"][unit["skin_key"]]
	var release: Dictionary = skin["actions"]["attack"][unit["facing"]]
	var recover: Dictionary = skin["actions"]["recover"][unit["facing"]]
	phases[identity] = {"target":unit_key(target),"stage":"cast","deadline":frame+maxi(1,ceili(unit["combat"]["cast_ticks"]/2.0)),
		"release_frames":maxi(1,ceili(AnimTimeline.total_ticks(release)/2.0)),
		"recover_frames":maxi(1,ceili(AnimTimeline.total_ticks(recover)/2.0))}
	unit["visual"] = "cast"; unit["visual_started_frame"] = frame


func _packet(unit: Dictionary) -> Dictionary:
	var terrain: int = catalog["cells"][unit["cell"].y*64+unit["cell"].x][0]
	return Inputs.snapshot(unit["combat"],terrain,unit["movement_type"],combat_rules)


func _hit(unit: Dictionary, target: Dictionary) -> void:
	if not _admitted(unit,target) or _distance(unit,target) > unit["combat"]["attack_range"]: return
	var value := Inputs.damage(_packet(unit),_packet(target),rng,unit["combat"]["attack_class"] == 2)
	var before: int = target["limits"]["hp"]
	if value >= 0: target["limits"]["hp"] = maxi(0,before-value)
	events.append({"frame":frame,"attacker":unit_key(unit),"target":unit_key(target),"damage":value,
		"before_hp":before,"after_hp":target["limits"]["hp"]})
	if events.size() > 64: events.pop_front()
	if target["limits"]["hp"] <= 0:
		if before > 0: _record_defeat(unit,target)
		phases.erase(unit_key(target)); target["path"] = []; target["target"] = -1
		target["destination"] = Vector2i(-1,-1); target["dead_at"] = frame


func _record_defeat(attacker: Dictionary, target: Dictionary) -> void:
	# 4799C0 mode2 entry: signed AA/AC add only when the new value is greater;
	# AE saturates at127. Credit uses the defeated record+A8, not damage dealt.
	var victim := unit_key(target)
	if _battle_stats.has(victim):
		_battle_stats[victim]["status_field_ae"] = mini(127,_battle_stats[victim]["status_field_ae"]+1)
	var id := unit_key(attacker)
	if not _battle_stats.has(id): return # Temporary Fana slot249 is not a settled role.
	var actor: Dictionary = source_actors.get(victim,reserves.get(victim,{}))
	if actor.is_empty(): return
	var raw := String(actor["record_hex"]).hex_decode()
	var points := int(raw[0xa8])+256*int(raw[0xa9])
	if points >= 32768: points -= 65536
	var row: Dictionary = _battle_stats[id]
	if row["count_field_aa"] < 32767: row["count_field_aa"] += 1
	var next: int = row["contribution_field_ac"]+points
	if next > row["contribution_field_ac"] and next <= 32767: row["contribution_field_ac"] = next


func result_inputs() -> Dictionary:
	if _terminal_choice.is_empty(): return {}
	var no_hostile := true
	# This remake's state3 is the local death-display interval before removal,
	# mapped to the original displayed list; original record state3 is not tested.
	for unit in units:
		if unit["category"]==5 and unit["side"]!=0 and unit["source_state"] in [1,3]: no_hostile = false
	for id in reserves:
		var raw := String(reserves[id]["record_hex"]).hex_decode()
		if raw[0x96]!=3 and _source_status(id)["state"]==0: no_hostile = false
	var objectives := []; objectives.resize(16); objectives.fill(0)
	objectives[0] = 1 if find_unit(1217)["side"]==0 else 0 # Config slot33 -> work217.
	var elapsed := 108000-remaining_ticks
	return {"result_selector":_terminal_choice["tactical_result_selector"],
		"time_key":1 if elapsed<=18000 else 2 if elapsed<=36000 else 3,
		"unit_condition_key":2 if no_hostile else 1,"objective_slots":objectives,
		"units":_participant_ids.map(func(id): return _battle_stats[id].duplicate(true))}


func _visual(unit: Dictionary, action: String) -> void:
	if unit.get("dead_at",-1) >= 0 or (action == "idle" and (phases.has(unit_key(unit)) or unit.get("summon_phase","")!="")): return
	super._visual(unit,action)


func tick() -> void:
	if ready and _ending_phase == "consuming":
		advance_exit(); return
	if _ending_phase != "active": return
	if not ready or paused: return
	_trace_clock += 1
	_update_removal()
	if _detect_trial_end(): return
	_update_captures()
	if _detect_trial_end(): return
	_attempt_activations()
	_update_summoning()
	if remaining_ticks > 0: remaining_ticks = maxi(0,remaining_ticks-2)
	# Local targeting decisions. Source immobile actors never become chasing units.
	for unit in units:
		if unit["limits"]["hp"] <= 0 or (not unit["controllable"] and unit["category"] != 5): continue
		if unit.get("summon_phase","") != "": continue
		var identity := unit_key(unit)
		if phases.has(identity): continue
		if unit["category"] == 5:
			var candidates := controlled_units().filter(func(p): return p["limits"]["hp"] > 0)
			candidates.sort_custom(func(a,b): return _distance(unit,a) < _distance(unit,b))
			unit["target"] = unit_key(candidates[0]) if not candidates.is_empty() else -1
		var target := find_unit(unit["target"])
		if not _admitted(unit,target):
			unit["target"] = -1; continue
		if _distance(unit,target) <= unit["combat"]["attack_range"]:
			_start_attack(unit,target)
		elif unit["combat"]["movement_rate"] > 0 and (unit["path"].is_empty() or frame%12 == 0):
			unit["path"] = _attack_path(unit,target)
			unit["destination"] = unit["path"].back() if not unit["path"].is_empty() else Vector2i(-1,-1)
	super.tick()
	for identity in phases.keys():
		if not phases.has(identity): continue
		var unit := find_unit(identity); var target := find_unit(phases[identity]["target"])
		if not _admitted(unit,target):
			phases.erase(identity); unit["target"] = -1; _visual(unit,"idle"); continue
		var phase: Dictionary = phases[identity]
		if frame < phase["deadline"]: continue
		if phase["stage"] == "cast":
			_hit(unit,target); phase["stage"] = "attack"; phase["deadline"] = frame+phase["release_frames"]
			unit["visual"] = "attack"; unit["visual_started_frame"] = frame
		elif phase["stage"] == "attack":
			phase["stage"] = "recover"; phase["deadline"] = frame+phase["recover_frames"]
			unit["visual"] = "recover"; unit["visual_started_frame"] = frame
		else:
			phases.erase(identity); _visual(unit,"idle")
	_detect_trial_end()


func advance(delta: float) -> void:
	if not is_finite(delta) or delta <= 0: return
	if _ending_phase == "consuming":
		advance_exit(); return
	if _ending_phase == "active": super.advance(delta)


func _detect_trial_end() -> bool:
	var choice := Progression.choose_terminal({"scene_id":5,"own_side":0,
		"event20_seen":event20_seen,"enemy2":_source_status(1248),"enemy3":_source_status(1247),
		"enemy11":_source_status(1239),"own_casualties":_own_casualties,
		"remaining_ticks":remaining_ticks,
		"own_playable_unavailable":units.filter(func(u): return u["side"]==0 and u["character_id"]>=1 and u["character_id"]<=45).all(func(u): return u["source_state"] in [0,2,3,4,5])})
	if not choice["supported"]: reason = "unsupported_progression"; return false
	if choice["action"] == "event20":
		event20_seen = true; _event_index = 0; _ending_phase = "event20"; _accumulator = 0.0
		reason = "event20_dialogue"; return true
	if choice["action"] == "terminal":
		_terminal_choice = choice
		_begin_ending("mission_objectives_met" if choice["selector_arg"] in [2,5] else
			"time_expired" if choice["selector_arg"] in [8,11] else "squad_defeated")
		return true
	return false


func _source_status(identity: int) -> Dictionary:
	var unit := find_unit(identity)
	if not unit.is_empty(): return {"used":true,"side":unit["side"],"state":unit["source_state"]}
	if reserves.has(identity):
		var raw := String(reserves[identity]["record_hex"]).hex_decode()
		return {"used":true,"side":int(raw[0xa4]),"state":int(raw[15])}
	return {"used":false,"side":7,"state":0}


func progression_snapshot() -> Dictionary:
	return {"event20_seen":event20_seen,"event_page":_event_index,"event_pages":_event_pages.size(),
		"text":_event_pages[_event_index].map(func(p): return p["text"]) if _ending_phase == "event20" else [],
		"stone_owned":find_unit(1248).get("side",-1)==0,"spring_owned":find_unit(1247).get("side",-1)==0,
		"boss_state":_source_status(1239)["state"],"choice":_terminal_choice.duplicate(true),
		"pending_activations":_pending_activations.size(),"remaining_ticks":remaining_ticks,
		"original_world_timing_verified":false}


func advance_event() -> bool:
	if not ready or _ending_phase != "event20": return false
	_record_command([2])
	_event_index += 1
	if _event_index == _event_pages.size():
		# Source command order; the renderer/VM timing remains a remake schedule.
		for request in Progression.activation_requests():
			for identity in reserves:
				var actor: Dictionary = reserves[identity]
				var raw := String(actor["record_hex"]).hex_decode()
				if (request.has("group") and int(raw[0x98]) == request["group"]) or \
						(request.has("work_index") and actor["work_index"] == request["work_index"]):
					_pending_activations.append({"identity":identity,"center":request["center"],"radius":request["radius"]})
		_attempt_activations()
		# T0005 136(25, query(1,1),0,...): type14 ownership transfer of pupil5.
		# Keep her original record, HP, job and abilities; no persistent roster edit.
		var ally := find_unit(1249)
		ally["side"] = 0; ally["controllable"] = true
		_ending_phase = "active"; _accumulator = 0.0; reason = "reinforcements_arrived"
	return true


func _attempt_activations() -> void:
	for request in _pending_activations.duplicate():
		if _activate(request["identity"],request["center"],request["radius"]):
			_pending_activations.erase(request)


func _activate(identity: int, center: Vector2i, radius: int) -> bool:
	var old := find_unit(identity)
	if not reserves.has(identity) or (not old.is_empty() and old["source_state"] not in [0,2]): return false
	var actor: Dictionary = reserves[identity]
	_placement_rotation = (_placement_rotation+1)%5
	var permutation := [0,1,2,3,4]
	for index in _placement_rotation*3:
		var first: int = permutation[0]; permutation[0] = permutation[index%5]; permutation[index%5] = first
	var blocked := _blocked(identity); var cell := Vector2i(-1,-1)
	for index in catalog["formation_grid"].size():
		var row: Array = catalog["formation_grid"][(index/5)*5+permutation[index%5]]
		var candidate := center+Vector2i(row[0],row[1])
		if row[2] <= radius and walkable(candidate,actor["movement_type"]) and not blocked.has(candidate):
			cell = candidate; break
	if cell.x < 0: reason = "reinforcement_placement_blocked"; return false
	var next := {"instance_id":identity,"character_id":actor["character_id"],"job":actor["job"],
		"movement_type":actor["movement_type"],"limits":actor["limits"].duplicate(true),"controllable":false,
		"category":actor["category"],"skin_key":actor["skin_key"],"combat":actor["combat"].duplicate(true),
		"cell":cell,"from_cell":cell,"facing":"S","path":[],"destination":Vector2i(-1,-1),
		"move_started_frame":-100000,"visual":"idle","visual_started_frame":frame,"target":-1,"dead_at":-1}
	_apply_record_fields(next,actor); next["source_state"] = 1
	if old.is_empty(): units.append(next)
	else:
		next["lives"] = old["lives"]; old.clear(); old.merge(next)
	source_actors[identity] = actor.duplicate(true)
	return true


func _update_removal() -> void:
	for unit in units:
		if unit["limits"]["hp"] > 0 or unit["source_state"] in [2,4]: continue
		if unit["dead_at"] < 0: unit["dead_at"] = frame
		unit["source_state"] = 3
		if unit["controllable"] and not unit["death_counted"]:
			_own_casualties += 1; unit["death_counted"] = true
		if frame-unit["dead_at"] < 30: continue
		# The trial's existing fade provides the removal boundary, not native mode timing.
		if unit.get("life_kind",0) == 3 and unit["lives"] > 0:
			if unit["lives"] < 99: unit["lives"] -= 1
			unit["source_state"] = 2
		else: unit["source_state"] = 4


func _update_captures() -> void:
	for identity in [1248,1247]:
		var object := find_unit(identity)
		if object["capture_elapsed"] >= 0:
			object["capture_elapsed"] += 1
			if object["capture_elapsed"] >= Progression.capture_transition_ticks(object["character_id"]):
				object["side"] = object["capture_target"]
				object["capture_hold"] = Progression.capture_hold_limit(object["side"])
				object["capture_elapsed"] = -1; object["capture_target"] = -1
			continue
		var counts := []; counts.resize(16); counts.fill(0)
		for unit in units:
			if unit_key(unit) == identity or unit["source_state"] != 1 or unit["side"] == 7: continue
			var delta: Vector2i = (object["cell"]-unit["cell"]).abs()
			if delta.x <= 5 and delta.y <= 5 and _capture_mask[(delta.y+5)*11+delta.x+5] != 0:
				counts[unit["side"]] = (counts[unit["side"]]+1)%256
		var candidate := Progression.capture_candidate(object["side"],counts)
		if object["side"] != 7 and candidate == 4: candidate = -1
		if candidate < 0:
			object["capture_hold"] = mini(object["capture_hold"]+1,Progression.capture_hold_limit(object["side"]))
		elif object["side"] == 7:
			object["capture_target"] = candidate; object["capture_elapsed"] = 0
		elif candidate != 4:
			object["capture_hold"] -= 1
			if object["capture_hold"] <= 0:
				object["capture_target"] = candidate; object["capture_elapsed"] = 0


func _update_summoning() -> void:
	var boss := find_unit(1239)
	if boss.is_empty() or boss["source_state"] != 1 or boss["limits"]["hp"] <= 0: return
	# Source thresholds, but explicitly local idle opportunities and animation clock.
	# We do not claim that original AI calls once per Godot tick.
	var phase: String = boss["summon_phase"]
	if phase == "":
		if phases.has(1239): return
		boss["summon_clock"] += 1
		if boss["summon_clock"] < 150: return
		boss["summon_clock"] = 0
		var active := units.filter(func(u): return u.get("group",0)==1 and u.get("life_kind",0)==3 and u["source_state"]==1).size()
		var available := reserves.keys().filter(func(id): return id!=1239 and _source_status(id)["state"] in [0,2] and String(reserves[id]["record_hex"]).hex_decode()[0x98]==1)
		if active >= 8 or available.is_empty(): return
		boss["summon_phase"] = "prepare"; boss["summon_remaining"] = 180
		boss["path"] = []; boss["destination"] = Vector2i(-1,-1); _visual(boss,"summon_prepare")
		return
	boss["summon_remaining"] -= 1
	if boss["summon_remaining"] > 0: return
	if phase == "prepare":
		boss["summon_phase"] = "animation"; _visual(boss,"summon")
		var timeline: Dictionary = catalog["skins"][boss["skin_key"]]["actions"]["summon"][boss["facing"]]
		boss["summon_remaining"] = maxi(1,ceili(AnimTimeline.total_ticks(timeline)/2.0))
	else:
		var count := units.filter(func(u): return u.get("group",0)==1 and u.get("life_kind",0)==3 and u["source_state"]==1).size()
		for identity in reserves:
			if count >= 8: break
			var raw := String(reserves[identity]["record_hex"]).hex_decode()
			if raw[0x98]==1 and raw[0x96]==3 and _activate(identity,boss["cell"],8): count += 1
		boss["summon_phase"] = ""; _visual(boss,"idle")


func request_return() -> bool:
	if not ready or _ending_phase not in ["opening","event20","active"]: return false
	_record_command([6])
	if _ending_phase in ["opening","event20"]:
		_begin_ending("player_exit"); return true
	# Respect an already reached trial endpoint even if the UI requests a return
	# before the next combat tick. Otherwise this is the player's explicit exit.
	if not _detect_trial_end(): _begin_ending("player_exit")
	return true


func _begin_ending(outcome: String) -> void:
	_ending_outcome = outcome; _ending_phase = "consuming"
	trial_complete = outcome == "mission_objectives_met"
	paused = false; _accumulator = 0.0; phases.clear()
	for unit in units:
		unit["target"] = -1; unit["path"] = []; unit["destination"] = Vector2i(-1,-1)
		_visual(unit,"idle")
	_result_consumer = ResultConsumer.new()
	# Completion is generated by this remake's trial lifecycle, never inferred
	# as a native battle outcome from an OS wait status or original selector.
	_result_consumer.begin_iteration(1)
	_ending_summary = {"outcome": outcome, "initial_enemies": _initial_enemies,
		"remaining_enemies": enemies().size(), "defeated_enemies": units.filter(func(u): return u["category"]==5 and u["limits"]["hp"]<=0).size(),
		"surviving_students": controlled_units().filter(func(u): return u["limits"]["hp"] > 0).size(),
		"total_students": controlled_units().size(), "battle_frames": frame,
		"rewards_applied": false, "campaign_advanced": false,"terminal_choice":_terminal_choice.duplicate(true)}
	reason = "finishing_trial"


func advance_exit() -> void:
	if not ready or _ending_phase != "consuming": return
	var current := _result_consumer.snapshot()
	var next: Dictionary
	match current["action"]:
		"wait":
			# One explicit remake scheduler completion per call, independent of
			# renderer FPS. This does not certify a Windows wait or native timing.
			next = _result_consumer.resume_wait(current["iteration"],current["wait_ordinal"],0)
		"call_replay_record":
			# The prototype has no replay recording enabled. Keep the original
			# call boundary and ignored zero return; create no fake record file.
			_record_calls += 1
			next = _result_consumer.replay_record_returned(current["iteration"],0)
		_:
			return
	if next["supported"] and next["function_returned"]:
		_ending_phase = "summary"; reason = "trial_summary"
		if _settlement != null and not _terminal_choice.is_empty():
			var result := _settlement.prepare(result_inputs())
			if not result["supported"]: _settlement_error = result["reason"]


func ending_snapshot() -> Dictionary:
	return {"phase": _ending_phase, "outcome": _ending_outcome,
		"consumer": _result_consumer.snapshot() if _result_consumer != null else {},
		"summary": _ending_summary.duplicate(true), "replay_record_calls": _record_calls,
		"settlement":{} if _settlement == null else _settlement.snapshot(),"settlement_error":_settlement_error,
		"replay_recording_enabled": false, "native_equivalence_verified": false}


func take_handoff() -> Dictionary:
	if not ready or _ending_phase != "summary": return {}
	if _settlement != null and _settlement.snapshot()["phase"] in ["round_result","total_result"]: return {}
	_ending_phase = "handoff_taken"
	var settled := {} if _settlement==null else _settlement.snapshot()
	return {"successor": "adv_ch003_pending" if settled.get("phase")=="adv_pending" else "school_adventure_preparation", "outcome": _ending_outcome,
		"settlement":settled,"battle_trace":battle_trace(),
		"summary": _ending_summary.duplicate(true), "consumer": _result_consumer.snapshot(),
		"evidence_kind": "remake_trial_lifecycle", "native_equivalence_verified": false,
		"authorizes_persistent_write": false}


func confirm_result() -> Dictionary:
	if not ready or _ending_phase!="summary" or _settlement==null: return {}
	match _settlement.snapshot()["phase"]:
		"round_result": return _settlement.confirm_round()
		"total_result": return _settlement.confirm_total(true)
		"adv_pending": return _settlement.snapshot()
	return {}


func _record_command(values: Array) -> void:
	if _trace.size() >= 4096: _trace_overflow = true; return
	_trace.append([_trace_clock]+values)


func battle_trace() -> Dictionary:
	return {"version":1,"ticks":_trace_clock,"commands":_trace.duplicate(true),"overflow":_trace_overflow}


func close() -> void:
	super.close(); combat_rules.clear(); phases.clear(); events.clear(); source_actors.clear(); trial_complete = false
	_ending_phase = "closed"; _ending_outcome = ""; _ending_summary.clear()
	_result_consumer = null; _initial_enemies = 0; _record_calls = 0
	_opening_pages.clear(); _opening_index = -1
	reserves.clear(); _event_pages.clear(); _event_index = -1; event20_seen = false
	_terminal_choice.clear(); _own_casualties = 0; remaining_ticks = -1; _capture_mask.clear(); _pending_activations.clear()
	_battle_stats.clear(); _participant_ids.clear(); _settlement = null; _settlement_error = ""
	_trace.clear();_trace_clock=0;_trace_overflow=false
