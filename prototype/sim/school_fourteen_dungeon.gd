extends RefCounted
## T0014 escape region, repeating reinforcements and 4345B0 result selection.
var slots := {}
var waves := {}
var patrol_driver
var summoners: Array[int]=[]
var previous_cells := {}
var escaped_id := -1


func start(s) -> void:
	if s.scene_id in [15,16]:
		patrol_driver=preload("res://sim/school_winter_battle.gd").new()
		patrol_driver.patrol_mask=String(s.catalog.spells.masks["3"]).hex_decode()
		patrol_driver.living=s.controlled_units()
		for actor in s.catalog.actors:
			if actor.has("summon_interval"):summoners.append(actor.instance_id)
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


static func last_floor_result(s, unavailable: bool) -> int:
	# 434770 checks four towers, then six springs, before time and loss.
	for number in s.catalog.grade_groups[0]:
		var tower: Dictionary=s.find_unit(1250-number)
		if tower.side!=0 or tower.source_state==0:
			return 11 if s.remaining_ticks==0 else 14 if unavailable else -1
	for number in s.catalog.grade_groups[1]:
		var spring: Dictionary=s.find_unit(1250-number)
		if spring.side!=0 or spring.source_state==0:return 8
	return 2 if s._own_casualties==0 else 5


static func aggregate(floors: Array) -> Dictionary:
	# 4DAB50 adds the per-floor records. 4DAE70 converts their mean grade.
	var result: Dictionary=floors[0].duplicate(true)
	var grade := 0
	for i in floors.size():
		var floor_data: Dictionary=floors[i]
		grade += [0,10,7,5,1,0][floor_data.result_selector]
		if i==0:continue
		for j in range(16):result.objective_slots[j]=int(result.objective_slots[j] or floor_data.objective_slots[j])
		for j in result.units.size():
			for key in ["count_field_aa","contribution_field_ac","status_field_ae"]:
				result.units[j][key]=mini(127 if key=="status_field_ae" else 32767,result.units[j][key]+floor_data.units[j][key])
		result.unit_condition_key=maxi(result.unit_condition_key,floor_data.unit_condition_key)
	result.time_key=0 # 4DAB10 clears 80968C; 4DAE70 reads the untouched sum field.
	result.dungeon_depth=floors.size()
	var average := grade/floors.size()
	result.result_selector=1 if average>=10 else 2 if average>=7 else 3 if average>=5 else 4 if average>=1 else 5
	return result


func advance_lower_floor(s) -> void:
	if s.frame%12==0:
		for u in s.units:
			if u.get("patrol",0)>0 and u.source_state==1 and u.target<0 and u.summon_phase=="":
				patrol_driver._patrol(s,u)
	for id in summoners:
		var u: Dictionary=s.find_unit(id)
		if not u.is_empty() and u.source_state==1 and u.limits.hp>0:
			s._update_summoner(u,u.group,u.lives,s.reserves[id].summon_interval)
