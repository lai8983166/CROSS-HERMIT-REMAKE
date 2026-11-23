extends RefCounted
## MAP21 uses a consecutive ownership counter and T0021's recurring sub20.
var by_id := {}
var capture_candidates := {}
var positions := PackedInt32Array()
var living_positions := PackedInt32Array()
var living := []
var guard_targets := {}
var nearby := {}

var hold := 0
var sampled_frame := 0
var owned := [0,0]
var objectives := [[],[]]
var slots := {}
var groups := []
var centers := []
var delay := []
var patrol_bounds := []
var patrol_mask := PackedByteArray()


func refresh_positions(s) -> void:
	# Only faction, work state and cell affect the original capture mask.
	# Keep per-object decisions across identical samples. A completed takeover
	# invalidates them immediately, including the remaining objects this tick.
	var visible := PackedInt32Array()
	visible.resize(s.units.size())
	var allies := PackedInt32Array()
	living.clear()
	for i in s.units.size():
		var u: Dictionary=s.units[i]
		var cell: int=u.cell.y*s.field_width+u.cell.x
		visible[i]=(cell<<9)|(int(u.side)<<4)|int(u.source_state)
		by_id[u.instance_id]=u
		if u.controllable and u.limits.hp>0:
			allies.append((cell<<6)|int(u.instance_id))
			living.append(u)
	if visible!=positions:
		capture_candidates.clear()
		nearby.clear()
		positions=visible
	if allies!=living_positions:
		guard_targets.clear()
		living_positions=allies


func guard_target(s,u: Dictionary) -> int:
	if guard_targets.has(u.cell):return guard_targets[u.cell]
	var closest := -1
	var best := 0x7fffffff
	for ally in living:
		var distance: int=s._distance(u,ally)
		if distance<best:
			best=distance
			closest=ally.instance_id
	guard_targets[u.cell]=closest
	return closest


func start(s) -> void:
	for i in 2:
		for number in s.catalog.grade_groups[i]:
			objectives[i].append(s.find_unit(1250-number))
	patrol_mask=String(s.catalog.spells.masks["3"]).hex_decode()
	for script in s.scene_scripts:
		for command in script.commands:
			var v: Array=command.values
			if script.sub==1 and command.opcode==124:slots[v[0]]=v[3]
			if script.sub!=20:continue
			match command.opcode:
				136:
					if v[0]==32:groups.append(v[1])
				146:
					if v[1]==2 and v[0]==1:delay=[v[2],v[3]]
					if v[1]==2 and v[0]==4:patrol_bounds=[v[2],v[3]]
				130:centers.append([Vector2i(v[1],v[2]),v[3]])


func result(s) -> int:
	# 431DD0 only requires a used work slot and own faction (+A4).
	for i in 2:
		owned[i]=0
		for object in objectives[i]:
			if object.side==0:owned[i]+=1
	if sampled_frame!=s.frame:
		sampled_frame=s.frame
		# 467B60 advances the original clock by one per sample. This
		# 30 Hz scheduler covers two original clock units per active tick.
		if owned[0]>=2 and owned[1]>=4:hold=mini(54000,hold+2)
		else:hold=0
	if hold>=54000:
		if owned!=[4,13]:return 8
		return 2 if s._own_casualties==0 else 5
	if s.controlled_units().all(func(u):return u.side!=0 or u.source_state in [0,2,3,4,5]):
		return 14 if s.elapsed<54000 else 11
	return -1


func advance(s) -> void:
	for slot in range(16):
		if not slots.has(slot) or slots[slot]>s.elapsed:continue
		slots.erase(slot)
		for pending in slots:
			if pending>slot:slots[pending]+=2
		# 435190 writes global bit 0 (field type 3) when both minima hold.
		if hold>0:_wave(s)
		for next_slot in range(16):
			if not slots.has(next_slot):
				slots[next_slot]=s.elapsed+int(s.rng.randi()%(delay[1]-delay[0]+1))+delay[0]
				break
		break
	_advance_units(s)


func _advance_units(s) -> void:
	for u in s.units:
		if u.controllable or u.limits.hp<=0:continue
		if u.life_kind==2:s._update_summoner(u,u.group,u.lives,s.reserves[u.instance_id].summon_interval)
		if u.patrol>0 and s.frame%12==0 and u.summon_phase=="":_patrol(s,u)
		if u.character_id in [388,394] and not s.phases.has(u.instance_id):
			var closest := {}
			var best: int=u.combat.attack_range+1
			if not nearby.has(u.instance_id):
				var reach: int=u.combat.attack_range
				nearby[u.instance_id]=s.units.filter(func(t):var offset: Vector2i=(t.cell-u.cell).abs();return offset.x<=reach and offset.y<=reach)
			for target in nearby[u.instance_id]:
				var d: Vector2i=(target.cell-u.cell).abs()
				if d.x>=best or d.y>=best or not s._admitted(u,target):continue
				var distance: int=s._distance(u,target)
				if distance<best:
					best=distance
					closest=target
			if not closest.is_empty():
				u.target=closest.instance_id
				s._start_attack(u,closest)


func _wave(s) -> void:
	var shuffled:=groups.duplicate()
	for i in shuffled.size():
		var a:=int(s.rng.randi()%shuffled.size())
		var b:=int(s.rng.randi()%shuffled.size())
		var tmp: int=shuffled[a]
		shuffled[a]=shuffled[b]
		shuffled[b]=tmp
	for group in shuffled:
		if s.units.any(func(u):return u.get("group",-1)==group and u.side==5 and u.source_state==1):continue
		for u in s.units:
			if u.get("group",-1)==group and u.source_state in [2,3,4]:u.source_state=2
		var route: int=patrol_bounds[0]+int(s.rng.randi()%(patrol_bounds[1]-patrol_bounds[0]+1))
		if route==25:route=26
		# T0021:B18 compares v4 (the route) with 1, after drawing v5.
		s.rng.randi()
		var center: Array=centers[1 if route==1 else 0]
		s._spawn_group(group,center[0],center[1],route)
		for u in s.units:
			if u.get("group",-1)==group:
				u.patrol=route
				u.patrol_index=0
				u.patrol_finished=false
		break


func _patrol(s,u: Dictionary) -> void:
	var route: Array=s.catalog.patrol_routes[str(u.patrol)]
	var i: int=u.get("patrol_index",0)
	var row: Array=route[i]
	s._walk_patrol(u,Vector2i(row[0],row[1]),patrol_mask)
	if not u.get("patrol_finished",false):return
	u.patrol_finished=false
	if row[3]!=0:
		u.patrol=row[3]
		u.patrol_index=0
	else:u.patrol_index=i+1
