extends "res://sim/school_field_session.gd"
## Source initial actors and scalar math; scheduler/HP application are remake-only.
const Inputs := preload("res://sim/school_attack_inputs.gd")
const COMBAT_CATALOG := "res://assets/school_combat/catalog.json"
const COMBAT_SHA := "4d7d3e4beed860a7163bb4c4c3cd772185fc45c775425eefafb8b75f059dc70b"

var combat_rules: Dictionary = {}
var phases: Dictionary = {}
var events: Array[Dictionary] = []
var rng := RandomNumberGenerator.new()
var source_actors: Dictionary = {}
var trial_complete := false


func open(preparation: Dictionary, combat: Dictionary, raw := "") -> bool:
	var source_raw := FileAccess.get_file_as_string(COMBAT_CATALOG)
	if source_raw.replace("\r\n","\n").sha256_text() != COMBAT_SHA: return false
	var source: Dictionary = Limits._source_numbers(JSON.parse_string(source_raw))
	var rules := Inputs.load_rules()
	if rules.is_empty(): return false
	# Build the base projection separately so every refusal preserves this session.
	var base = load("res://sim/school_field_session.gd").new()
	if not base.open(preparation,combat,raw): return false
	var next_units: Array[Dictionary] = base.units.duplicate(true)
	for unit in next_units:
		var row: Dictionary = combat["students"].filter(func(r): return r["input"]["character_id"] == unit["character_id"])[0]
		var computed := Inputs.project(row["input"],rules)
		if not computed["supported"]: return false
		unit.merge({"instance_id":unit["character_id"],"controllable":true,"category":0,
			"skin_key":str(unit["character_id"]),"combat":computed["fields"],"target":-1,"dead_at":-1})
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
	units = next_units; catalog = base.catalog.duplicate(true); catalog["skins"] = source["skins"].duplicate(true)
	_maps = base._maps; _reserved.clear(); _accumulator = 0.0
	combat_rules = rules; source_actors = new_actors; phases.clear(); events.clear()
	frame = 0; paused = false; ready = true; selected_id = units[0]["character_id"]; reason = "ready"
	rng.seed = source["trial_policy"]["seed"]; trial_complete = false
	return true


func controlled_units() -> Array:
	return units.filter(func(u): return u["controllable"])


func enemies() -> Array:
	return units.filter(func(u): return u["category"] == 5 and u["limits"]["hp"] > 0)


func select(identity: int) -> bool:
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
	var unit := find_unit(identity)
	if unit.is_empty() or not unit["controllable"] or unit["limits"]["hp"] <= 0: return false
	var target := at_cell(destination)
	if not target.is_empty() and target["category"] == 5:
		return command_attack(identity,unit_key(target))
	var accepted := super.command_move(identity,destination)
	if accepted:
		unit["target"] = -1; phases.erase(identity); _visual(unit,"idle")
	return accepted


func _admitted(unit: Dictionary, target: Dictionary) -> bool:
	if unit.is_empty() or target.is_empty() or unit["limits"]["hp"] <= 0 or target["limits"]["hp"] <= 0: return false
	return (unit["controllable"] and target["category"] == 5) or (unit["category"] == 5 and target["controllable"])


func command_attack(identity: int, target_id: int) -> bool:
	var unit := find_unit(identity); var target := find_unit(target_id)
	if not ready or unit.is_empty() or not unit["controllable"] or not _admitted(unit,target): return false
	unit["target"] = target_id; phases.erase(identity); unit["path"] = []
	unit["destination"] = Vector2i(-1,-1); reason = "attack_order"
	return true


func stop(identity: int) -> bool:
	var unit := find_unit(identity)
	if unit.is_empty() or not unit["controllable"] or unit["limits"]["hp"] <= 0: return false
	phases.erase(identity); unit["target"] = -1
	return super.stop(identity)


func _distance(a: Dictionary, b: Dictionary) -> int:
	return absi(a["cell"].x-b["cell"].x)+absi(a["cell"].y-b["cell"].y)


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
		phases.erase(unit_key(target)); target["path"] = []; target["target"] = -1
		target["destination"] = Vector2i(-1,-1); target["dead_at"] = frame


func _visual(unit: Dictionary, action: String) -> void:
	if unit.get("dead_at",-1) >= 0 or (action == "idle" and phases.has(unit_key(unit))): return
	super._visual(unit,action)


func tick() -> void:
	if not ready or paused: return
	# Local targeting decisions. Source immobile actors never become chasing units.
	for unit in units:
		if unit["limits"]["hp"] <= 0 or (not unit["controllable"] and unit["category"] != 5): continue
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
			unit["path"] = SimPath.find_path(_maps[unit["movement_type"]],{"blocked_terrain":[0]},unit["cell"],target["cell"],_blocked(identity))
			unit["destination"] = target["cell"]
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
	trial_complete = enemies().is_empty()


func close() -> void:
	super.close(); combat_rules.clear(); phases.clear(); events.clear(); source_actors.clear(); trial_complete = false
