extends RefCounted
## T0014 escape region, repeating reinforcements and 4345B0 result selection.
var slots := {}
var waves := {}
var previous_cells := {}
var escaped_id := -1


func start(s) -> void:
	for unit in s.controlled_units():previous_cells[unit.instance_id]=unit.cell
	for script in s.scene_scripts:
		if script.block!=0:continue
		if script.sub==1:
			for command in script.commands:
				if command.opcode==124:
					var v: Array=command.values
					slots[v[0]]={"sub":v[2],"due":v[3]}
		elif script.sub in [20,21]:
			var wave := {"groups":[],"centers":[],"patrol":false}
			for command in script.commands:
				var v: Array=command.values
				match command.opcode:
					136:
						if v[0]==32:wave.groups.append(v[1])
					133:wave.patrol=true
					130:
						wave.centers.append(Vector2i(v[1],v[2]))
						wave.radius=v[3]
					146:
						if v[1]==2 and v[0]==1:wave.delay=[v[2],v[3]]
			waves[script.sub]=wave


func result(s, unavailable: bool) -> int:
	# OP113 enables region 1; OP136(20,1,1) enables only faction bit 0.
	for unit in s.controlled_units():
		var cell: Vector2i=unit.cell
		var previous: Vector2i=previous_cells[unit.instance_id]
		if previous==cell:continue
		previous_cells[unit.instance_id]=cell
		var region: Array=s.catalog.regions["1"]
		if unit.side==0 and unit.source_state==1 and region.has(cell.y*s.field_width+cell.x) and not region.has(previous.y*s.field_width+previous.x):
			escaped_id=unit.instance_id
			break
	if escaped_id>=0:return (2 if s._own_casualties==0 else 5) if s.elapsed<=36000 else 8
	if unavailable:return 11 if s.elapsed>=36000 else 14
	return -1


func advance(s) -> void:
	for slot in range(16):
		if not slots.has(slot) or slots[slot].due>s.elapsed:continue
		var sub: int=slots[slot].sub
		var wave: Dictionary=waves[sub]
		slots.erase(slot)
		for pending in slots:
			if pending>slot:slots[pending].due+=2
		var groups: Array=wave.groups.duplicate()
		for i in groups.size():
			var a:=int(s.rng.randi()%groups.size())
			var b:=int(s.rng.randi()%groups.size())
			var value: int=groups[a]
			groups[a]=groups[b]
			groups[b]=value
		for group in groups:
			if s.units.any(func(u):return u.get("group",0)==group and u.side==5 and u.source_state==1):continue
			# OP136(33) -> 47FA40 readies eliminated group members before
			# OP130 attempts their placement. The summoner cannot do this.
			for unit in s.units:
				if unit.get("group",0)==group and unit.source_state in [2,3,4]:
					unit.source_state=2
					# _activate installs the replenished source limits on display.
			var route := -1
			if wave.patrol:route=1+int(s.rng.randi()%6)
			else:
				# T0014:16B0 draws v5, but 16CC compares v4 with 1.
				# 4CE6AF zeroes all 50 locals at sub entry, so the first
				# center is used. The source still consumes the draw.
				s.rng.randi()
			s._spawn_group(group,wave.centers[0],wave.radius,route)
			break
		for next_slot in range(16):
			if not slots.has(next_slot):
				# 496FD0 uses rand % (upper - lower + 1) + lower.
				var delay: int=wave.delay[0]+int(s.rng.randi()%(wave.delay[1]-wave.delay[0]+1))
				slots[next_slot]={"sub":sub,"due":s.elapsed+delay}
				break
		return


func walk(s) -> void:
	var mask := String(s.catalog.spells.masks["3"]).hex_decode()
	for unit in s.units:
		var request: Array=unit.get("source_ai_request",[])
		if request.is_empty():continue
		var point: Array=s.catalog.patrol_goals[request[1]-1]
		s._walk_patrol(unit,Vector2i(point[0],point[1]),mask)
