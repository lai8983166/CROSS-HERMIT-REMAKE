extends RefCounted
## Three approaches to the cave exit. The timer and reinforcement slots are
## expressed in the units used by T0011 and the 434060 objective routine.
var escaped := 0
var timers := {}
var reinforcements := {}
var wave_after_gate := false
var patrol_mask: PackedByteArray
var guards := preload("res://sim/school_twenty_four_battle.gd").new()


func start(s) -> void:
	patrol_mask = String(s.catalog.spells.masks["3"]).hex_decode()
	guards.living = s.controlled_units()
	for script in s.scene_scripts:
		if script.block != 0: continue
		var commands: Array = []
		var actor := 0
		for instruction in script.commands:
			var v: Array = instruction.values
			match instruction.opcode:
				124: timers[int(v[2])] = int(v[3])
				130: commands.append([v[0],Vector2i(v[1],v[2]),v[3]])
				146: actor = 1250-int(v[2])
				112: commands.append([-actor,Vector2i(v[1],v[2]),10])
		if not commands.is_empty(): reinforcements[int(script.sub)] = commands


func _spawn(s, sub: int) -> void:
	for entry in reinforcements[sub]:
		if entry[0] < 0:
			s._activate(-entry[0],entry[1],entry[2])
		else:
			s._spawn_group(entry[0],entry[1],entry[2])


func advance(s) -> void:
	for sub in timers.keys():
		if s.elapsed >= timers[sub]:
			_spawn(s,sub)
			timers.erase(sub)
	if not wave_after_gate and s.find_unit(1243).get("source_state",0) == 4:
		wave_after_gate = true
		_spawn(s,27)
	if s.frame % 12 != 0: return
	for unit in s.units:
		if unit.side != 5 or unit.source_state != 1 or unit.limits.hp <= 0: continue
		if s._on_region(unit,"1"):
			escaped += 1
			unit.source_state = 2
			unit.limits.hp = 0
			unit.path.clear()
			s.phases.erase(unit.instance_id)
			continue
		var route: Array = s.catalog.patrol_routes.get(str(unit.get("patrol",0)),[])
		if route.is_empty(): continue
		var i: int = unit.get("patrol_index",0)
		var row: Array = route[i]
		s._walk_patrol(unit,Vector2i(row[0],row[1]),patrol_mask)
		if not unit.get("patrol_finished",false): continue
		unit.patrol_finished = false
		if row[3] == 0 and i+1 < route.size():
			unit.patrol_index = i+1
		else:
			unit.patrol = maxi(0,row[3])
			unit.patrol_index = 0


func result(remaining: int, unavailable: bool) -> int:
	if escaped >= 10: return 11
	if remaining == 0:
		if escaped == 0: return 2
		return 5 if escaped <= 3 else 8
	return 14 if unavailable else -1
