extends RefCounted
## Transient deployment/navigation. Original enemy/world/result loops are absent.
const Limits := preload("res://sim/school_combat_limits.gd")
const CATALOG := "res://assets/school_field/catalog.json"
const CATALOG_SHA := "10473769a06554f7427a73d8c170e17365ff24eabe1b9170478e3aa7be962ab4"

var catalog: Dictionary = {}
var units: Array[Dictionary] = []
var frame := 0
var paused := false
var ready := false
var selected_id := -1
var reason := "closed"
var _maps: Array[SimMapData] = []
var _reserved: Dictionary = {}
var _accumulator := 0.0


func open(preparation: Dictionary, combat: Dictionary, raw := "") -> bool:
	# Construct off to the side. Invalid reopen never destroys an active session.
	if raw.is_empty(): raw = FileAccess.get_file_as_string(CATALOG)
	if raw.replace("\r\n","\n").sha256_text() != CATALOG_SHA:
		return false
	if not preparation.get("supported",false) or not preparation.get("ready",false) \
			or not preparation.get("prepared") is Dictionary \
			or not combat.get("supported",false) or not combat.get("ready",false) \
			or not combat.get("students") is Array:
		return false
	var prepared: Dictionary = preparation["prepared"]
	if prepared.get("adventure_id") != 5 or prepared.get("round_count") != 1 \
			or not prepared.get("rounds") is Array or prepared["rounds"].size() != 1 \
			or not prepared["rounds"][0] is Dictionary:
		return false
	var round_data: Dictionary = prepared["rounds"][0]
	if round_data.get("scene_id") != 5 or round_data.get("teacher_ids") != [101] \
			or not round_data.get("student_ids") is Array or round_data["student_ids"].is_empty() \
			or round_data["student_ids"].size() != combat["students"].size():
		return false
	var source: Dictionary = Limits._source_numbers(JSON.parse_string(raw))
	var limit_rules: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(Limits.RULE_PATH))
	var next_units: Array[Dictionary] = []
	var identities := {}
	for index in combat["students"].size():
		var row = combat["students"][index]
		if not row is Dictionary or not row.get("input") is Dictionary or not row.get("limits") is Dictionary:
			return false
		var identity = row["input"].get("character_id")
		if not identity is int or identity not in [3,4,9] or identities.has(identity) \
				or identity != round_data["student_ids"][index]:
			return false
		var skin: Dictionary = source["skins"][str(identity)]
		if row["input"].get("job") != skin["job"]:
			return false
		var limits := Limits.project(row["input"],limit_rules)
		if not limits["supported"] or limits["limits"] != row["limits"]:
			return false
		identities[identity] = true
		next_units.append({"character_id":identity,"job":skin["job"],"movement_type":skin["movement_type"],
			"limits":limits["limits"].duplicate(true),"cell":Vector2i.ZERO,"from_cell":Vector2i.ZERO,
			"facing":"N","path":[],"destination":Vector2i(-1,-1),"move_started_frame":-100000,
			"visual":"idle","visual_started_frame":0})
	var reserved := {}
	for row in source["static_occupancy"]:
		reserved[Vector2i(row["cell"][0],row["cell"][1])] = true
	var rotation: int = source["initial_rotation"]
	for unit in next_units:
		rotation = (rotation+1)%source["permutation_size"]
		var permutation := [0,1,2,3,4]
		for index in rotation*source["rotation_multiplier"]:
			var old = permutation[0]
			permutation[0] = permutation[index%5]; permutation[index%5] = old
		var found := false
		for index in source["formation_grid"].size():
			var row: Array = source["formation_grid"][(index/5)*5+permutation[index%5]]
			if row[2] > source["formation_radius"]: continue
			var cell := Vector2i(source["origin"][0]+row[0],source["origin"][1]+row[1])
			if not _inside(cell) or reserved.has(cell) \
					or source["passability"][unit["movement_type"]][cell.y*64+cell.x] == 0:
				continue
			unit["cell"] = cell; unit["from_cell"] = cell; reserved[cell] = true
			found = true; break
		if not found: return false
	catalog = source
	units = next_units
	_reserved.clear()
	for row in source["static_occupancy"]:
		_reserved[Vector2i(row["cell"][0],row["cell"][1])] = true
	_maps.clear()
	for mode in range(5):
		var map := SimMapData.new()
		map.cell_w = 64; map.cell_h = 96
		var zeros: Array = []; zeros.resize(6144); zeros.fill(0)
		map._layers = {"terrain":source["passability"][mode].duplicate(),"variant":zeros,"object":zeros}
		_maps.append(map)
	frame = 0; paused = false; ready = true; selected_id = units[0]["character_id"]
	_accumulator = 0.0; reason = "ready"
	return true


static func _inside(cell: Vector2i) -> bool:
	return cell.x >= 0 and cell.y >= 0 and cell.x < 64 and cell.y < 96


func read_units() -> Array:
	return units.duplicate(true)


func find_unit(identity: int) -> Dictionary:
	for unit in units:
		if unit["character_id"] == identity: return unit
	return {}


func select(identity: int) -> bool:
	if not ready or find_unit(identity).is_empty(): return false
	selected_id = identity
	return true


func _blocked(identity: int) -> Dictionary:
	var blocked: Dictionary = _reserved.duplicate()
	for unit in units:
		if unit["character_id"] != identity: blocked[unit["cell"]] = true
	return blocked


func walkable(cell: Vector2i, mode := 0) -> bool:
	return ready and _inside(cell) and mode >= 0 and mode < 5 \
		and catalog["passability"][mode][cell.y*64+cell.x] != 0


func command_move(identity: int, destination: Vector2i) -> bool:
	var unit := find_unit(identity)
	if not ready or unit.is_empty(): return false
	if not walkable(destination,unit["movement_type"]) or _blocked(identity).has(destination):
		reason = "blocked"; return false
	if destination == unit["cell"]:
		return stop(identity)
	var path := SimPath.find_path(_maps[unit["movement_type"]],{"blocked_terrain":[0]},
		unit["cell"],destination,_blocked(identity))
	if path.is_empty() or path.back() != destination:
		reason = "unreachable"; return false
	unit["path"] = path; unit["destination"] = destination
	reason = "moving"; return true


func stop(identity: int) -> bool:
	var unit := find_unit(identity)
	if not ready or unit.is_empty(): return false
	unit["path"] = []; unit["destination"] = Vector2i(-1,-1)
	_visual(unit,"idle"); reason = "stopped"
	return true


func tick() -> void:
	if not ready or paused: return
	frame += 1
	var interval: int = catalog["interaction"]["move_interval"]
	for unit in units:
		if unit["path"].is_empty():
			if frame-unit["move_started_frame"] >= interval: _visual(unit,"idle")
			continue
		if frame%interval != 0: continue
		var blocked := _blocked(unit["character_id"])
		if blocked.has(unit["path"][0]):
			unit["path"] = SimPath.find_path(_maps[unit["movement_type"]],{"blocked_terrain":[0]},
				unit["cell"],unit["destination"],blocked)
			if not unit["path"].is_empty() and unit["path"].back() != unit["destination"]:
				unit["path"] = []
		if unit["path"].is_empty():
			_visual(unit,"idle"); continue
		var next: Vector2i = unit["path"][0]
		# Never skip occupied waypoints, teleport or silently approach another cell.
		if blocked.has(next) or not walkable(next,unit["movement_type"]) \
				or absi(next.x-unit["cell"].x)+absi(next.y-unit["cell"].y) != 1: continue
		unit["path"].remove_at(0)
		var delta: Vector2i = next-unit["cell"]
		unit["facing"] = "E" if delta.x > 0 else "W" if delta.x < 0 else "S" if delta.y > 0 else "N"
		unit["from_cell"] = unit["cell"]; unit["cell"] = next; unit["move_started_frame"] = frame
		_visual(unit,"move")


func _visual(unit: Dictionary, action: String) -> void:
	if unit["visual"] != action:
		unit["visual"] = action; unit["visual_started_frame"] = frame


func advance(delta: float) -> void:
	if not ready or paused or not is_finite(delta) or delta <= 0: return
	var step := 1.0/float(catalog["interaction"]["logic_hz"])
	_accumulator += minf(delta,float(catalog["interaction"]["delta_cap"]))
	while _accumulator+0.00000001 >= step:
		_accumulator -= step; tick()


func position(unit: Dictionary) -> Vector2:
	var weight := clampf((frame-unit["move_started_frame"]+_accumulator*30.0)/float(
		catalog["interaction"]["move_interval"]),0,1)
	return Vector2(unit["from_cell"]).lerp(Vector2(unit["cell"]),weight)*Vector2(32,16)+Vector2(16,8)


func close() -> void:
	ready = false; units.clear(); catalog.clear(); _maps.clear(); _reserved.clear()
	selected_id = -1; frame = 0; paused = false; _accumulator = 0.0; reason = "closed"
