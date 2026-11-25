extends "res://sim/school_twenty_one_battle.gd"
## T0024 rescue-region event, recurring waves and 435410 terminal priority.
var rescued := false
var previous_cells := {}
var waves := {}
var rescue_script: Array = []
var protectees: Array = []


func start(s) -> void:
	patrol_mask=String(s.catalog.spells.masks["3"]).hex_decode()
	for n in s.catalog.grade_objects:objectives[0].append(s.find_unit(1250-n))
	for id in [1241,1240]:protectees.append(s.find_unit(id))
	for u in s.controlled_units():previous_cells[u.instance_id]=u.cell
	for entry in s.scene_scripts:
		if entry.block==1 and entry.sub==1:rescue_script=entry.commands
		if entry.block!=0 or entry.sub not in [20,21,22]:continue
		var wave:={"groups":[],"route":[]}
		for cmd in entry.commands:
			var v:Array=cmd.values
			match cmd.opcode:
				136:
					if v[0]==32:wave.groups.append(v[1])
				146:
					if v[1]==2:wave["route" if v[0]==4 else "delay"]=[v[2],v[3]]
				130:
					wave.center=Vector2i(v[1],v[2])
					wave.radius=v[3]
		waves[entry.sub]=wave


func check_event(s) -> bool:
	if rescued:return false
	var region:Array=s.catalog.regions["1"]
	for u in s.controlled_units():
		if u.source_state!=1 or u.side!=0 or u.limits.hp<=0:continue
		var from:Vector2i=previous_cells[u.instance_id]
		if u.cell==from:continue
		previous_cells[u.instance_id]=u.cell
		if region.has(from.y*s.field_width+from.x) or not region.has(u.cell.y*s.field_width+u.cell.x):continue
		s._event_pages=s._pages(1,1)
		s._event_index=0
		s._ending_phase="event20"
		s._accumulator=0.0
		return true
	return false


func finish_event(s) -> void:
	var id:=-1
	for cmd in rescue_script:
		var v:Array=cmd.values
		match cmd.opcode:
			146:
				if v[1]==1:id=1250-int(v[2])
			112:
				var center:=Vector2i(v[1],v[2])
				if not s._activate(id,center,10):s._pending_activations.append({"identity":id,"center":center,"radius":10})
			130:s._spawn_group(v[0],Vector2i(v[1],v[2]),v[3])
			124:slots[v[0]]={"sub":v[2],"due":s.elapsed+int(v[3])}
			136:
				if v[0]==25:s.find_unit(id).side=v[2]
	rescued=true
	s._ending_phase="active"
	s.reason="refugees_found"


func result(s) -> int:
	if s._source_status(1194).state==4 and s._source_status(1193).state==4:
		if objectives[0].all(func(u):return u.side==0):return 2 if s._own_casualties==0 else 5
		return 8
	if protectees.any(func(u):return u.source_state==4):return 11
	if s.controlled_units().all(func(u):return u.source_state in [0,2,3,4,5]):return 14
	return -1


func advance(s) -> void:
	for slot in range(16):
		if not slots.has(slot) or slots[slot].due>s.elapsed:continue
		var sub:int=slots[slot].sub
		var wave:Dictionary=waves[sub]
		slots.erase(slot)
		for other in slots:
			if other>slot:slots[other].due+=2
		_repeat_wave(s,wave)
		for next in range(16):
			if slots.has(next):continue
			var span:Array=wave.delay
			slots[next]={"sub":sub,"due":s.elapsed+int(span[0])+int(s.rng.randi()%(int(span[1])-int(span[0])+1))}
			break
		break
	_advance_units(s)


func _repeat_wave(s,wave: Dictionary) -> void:
	var order:Array=wave.groups.duplicate()
	for i in order.size():
		var a:=int(s.rng.randi()%order.size())
		var b:=int(s.rng.randi()%order.size())
		var tmp:int=order[a]
		order[a]=order[b]
		order[b]=tmp
	for group in order:
		if s.units.any(func(u):return u.get("group",0)==group and u.side==5 and u.source_state==1):continue
		for u in s.units:
			if u.get("group",0)==group and u.source_state in [2,3,4]:u.source_state=2
		var route:=-1
		if not wave.route.is_empty():
			route=int(wave.route[0])+int(s.rng.randi()%(int(wave.route[1])-int(wave.route[0])+1))
		var center:Vector2i=wave.centers[s.rng.randi()%wave.centers.size()] if wave.has("centers") else wave.center
		s._spawn_group(group,center,wave.radius,route)
		if route>0:
			for u in s.units:
				if u.get("group",0)==group:
					u.patrol=route
					u.patrol_index=0
					u.patrol_finished=false
		break


func guard_target(s,u: Dictionary) -> int:
	if u.character_id in [413,461,462]:return -1
	var row:Dictionary=s.reserves[u.instance_id]
	var mode:int=row.search_mode
	if mode>1:return -1
	var id:=-1
	var best:=0x7fffffff
	for ally in living+protectees:
		if ally.side not in [0,4] or ally.source_state!=1 or ally.limits.hp<=0:continue
		var d:Vector2i=(ally.cell-u.cell).abs()
		if mode==1 and (d.x>row.vision or d.y>row.vision or s._distance(u,ally)>row.vision):continue
		var cost:=d.x*2+d.y
		if cost<best:
			id=ally.instance_id
			best=cost
	return id
