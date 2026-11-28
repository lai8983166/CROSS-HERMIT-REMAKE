extends RefCounted
## T0001 timers are measured in the session's original elapsed units.
var wave_index := 0
var finish_due := -1
var retreating := false
var gate_breached := false
var penetrations := 0
var escaped := 0
var shown := {}
var pending := 0

func _show(s, sub: int, block := 0) -> void:
	pending = sub
	shown[Vector2i(block,sub)] = true
	s._event_pages = s._pages(sub,block)
	if block == 1 and sub == 1:
		# First visit, source byte 0 reports whether both flanking towers are held.
		var towers: bool = s.find_unit(1245).side == 0 and s.find_unit(1244).side == 0
		var start := 0x488e if towers else 0x4578
		var end := 0x4a2c if towers else 0x4764
		s._event_pages = s._event_pages.filter(func(page): return page[0].offset >= start and page[0].offset < end)
	s._event_index = 0
	s._ending_phase = "event20"
	s._accumulator = 0.0

func finish_event(s) -> void:
	if pending == 24:
		s._spawn_group(9,Vector2i(32,94),3)
		if wave_index >= 4: finish_due = s.elapsed + 1800
	elif pending == 27:
		retreating = true
		finish_due = s.elapsed + 300
	pending = 0
	s._ending_phase = "active"

func advance(s) -> void:
	const TIMES := [3600,7200,12600,16200]
	const CENTERS := [Vector2i(3,94),Vector2i(60,78),Vector2i(20,94),Vector2i(32,94)]
	if wave_index < TIMES.size() and s.elapsed >= TIMES[wave_index]:
		s._spawn_group(5+wave_index,CENTERS[wave_index],3)
		wave_index += 1
		if wave_index == 4 and gate_breached: finish_due = s.elapsed + 300
	if not gate_breached and not retreating and s.elapsed >= 19800:
		_show(s,27)
		return
	if s.frame % 12 != 0: return
	for u in s.units:
		if u.side != 5 or u.category != 5 or u.source_state != 1 or u.limits.hp <= 0 or u.character_id >= 387: continue
		if s._on_region(u,"2") or (retreating and s._on_region(u,"3")):
			if s._on_region(u,"2"): penetrations += 1
			else: escaped += 1
			u.source_state = 2
			u.limits.hp = 0
			u.path = []
			s.phases.erase(u.instance_id)
			continue
		if retreating and u.path.is_empty():
			var cells: Array = s.catalog.regions["3"]
			for offset in range(cells.size()):
				var i: int = cells[(u.instance_id+offset)%cells.size()]
				var goal := Vector2i(i%s.field_width,i/s.field_width)
				var path: Array = s.attack_paths.route(u.cell,goal,0,u.movement_type,s.units)
				if not path.is_empty():
					u.path = path
					u.destination = goal
					break

func result(s, unavailable: bool) -> int:
	if s._ending_phase != "active": return -1
	for id in [1249,1248,1247]:
		var gate: Dictionary = s.find_unit(id)
		if not shown.has(Vector2i(0,29)) and gate.source_state == 1 and gate.limits.hp < 200:
			_show(s,29)
			return -1
	for id in [1249,1248,1247]:
		var gate: Dictionary = s.find_unit(id)
		if gate.source_state in [2,3,4] and not gate_breached and not retreating:
			gate_breached = true
			_show(s,24)
			return -1
	if not shown.has(Vector2i(0,25)) and s.find_unit(1246).side == 0:
		_show(s,25)
		return -1
	if not shown.has(Vector2i(0,26)) and (s.find_unit(1245).side == 0 or s.find_unit(1244).side == 0):
		_show(s,26)
		return -1
	if not shown.has(Vector2i(1,1)) and s.controlled_units().any(func(u): return s._on_region(u,"1")):
		_show(s,1,1)
		return -1
	if penetrations > 0 and not shown.has(Vector2i(1,2)):
		_show(s,2,1)
		return -1
	if unavailable: return 14
	if finish_due < 0 or s.elapsed < finish_due: return -1
	for u in s.units:
		if u.side == 5 and u.character_id not in range(387,405) and u.source_state in [1,3]: return -1
	if penetrations > 0: return 11
	for id in [1249,1248,1247,1246,1245,1244]:
		var object: Dictionary = s.find_unit(id)
		if object.side != 0 or object.source_state in [2,3,4]: return 8
	return 2 if s._own_casualties == 0 else 5
