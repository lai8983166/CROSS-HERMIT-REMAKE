extends RefCounted
## T0010 patrol, map event cells, dialogue and reinforcements.
const ELDER := 1249
var waypoint := 0
var resume_at := -1
var enabled_region := 0
var timers := {}
var previous_cell := Vector2i(-1,-1)
var previous_region := 0
var arrival_mask := PackedByteArray()
var active_block := -1
var active_sub := -1
var arrived := false


func start(session) -> void:
	previous_cell=session.find_unit(ELDER).cell
	arrival_mask=String(session.catalog["spells"]["masks"]["3"]).hex_decode()
	_apply_script(session,0,1)


func _apply_script(s,block: int,sub: int) -> void:
	var unit_number := -1
	for entry in s.scene_scripts:
		if entry["block"]!=block or entry["sub"]!=sub:continue
		for command in entry["commands"]:
			var v: Array=command["values"]
			match command["opcode"]:
				113:
					if v[1]==1:enabled_region=v[0]
					elif enabled_region==v[0]:enabled_region=0
				124:
					timers[v[0]]={"sub":v[2],"due":s.elapsed+v[3]}
				130:s._spawn_group(v[0],Vector2i(v[1],v[2]),v[3])
				146:
					if v[1]==1:unit_number=v[2]
				112:
					if unit_number>0:
						var request={"identity":1250-unit_number,"center":Vector2i(v[1],v[2]),"radius":10}
						if not s._activate(request.identity,request.center,request.radius):s._pending_activations.append(request)
				165:
					if block==1 and sub==6 and v==[1,65535,0]:arrived=true
		return


func check_event(s) -> bool:
	var elder: Dictionary=s.find_unit(ELDER)
	if elder.limits.hp<=0:return false
	var entered:=0
	if elder.cell!=previous_cell:
		previous_cell=elder.cell
		var region:=enabled_region if enabled_region>0 and s._on_region(elder,str(enabled_region)) else 0
		if elder.side==4 and region!=previous_region:entered=region
		previous_region=region
	if entered>0:
		active_block=1
		active_sub=entered
	else:
		active_sub=-1
		for slot in range(6):
			if timers.has(slot) and timers[slot].due<=s.elapsed:
				active_block=0
				active_sub=timers[slot].sub
				timers.erase(slot)
				break
		if active_sub<0:return false
	s._event_pages=s._pages(active_sub,active_block)
	s._event_index=0
	if s._event_pages.is_empty():
		_apply_script(s,active_block,active_sub)
		return false
	s._ending_phase="event20"
	s._accumulator=0.0
	return true


func finish_event(s) -> void:
	_apply_script(s,active_block,active_sub)
	s._ending_phase="active"
	s.reason="escorting"


func _in_arrival_mask(delta: Vector2i) -> bool:
	delta=delta.abs()
	return delta.x<=3 and delta.y<=3 and arrival_mask[(delta.y+3)*7+delta.x+3]!=0


func walk(s) -> void:
	var elder: Dictionary=s.find_unit(ELDER)
	var route: Array=s.catalog["elder_route"]
	if elder.limits.hp<=0 or waypoint>=route.size():return
	if resume_at>=0:
		if s.elapsed<resume_at:return
		resume_at=-1
		waypoint+=1
		if waypoint>=route.size():return
	var point: Array=route[waypoint]
	var goal:=Vector2i(point[0],point[1])
	if not elder.path.is_empty():return
	# 43C1D0 view 3 uses the same MAPCOM mask as combat.
	if _in_arrival_mask(elder.cell-goal):
		elder.destination=Vector2i(-1,-1)
		resume_at=s.elapsed+point[2]
	elif s.frame%12==0:
		elder.path=s.attack_paths.route(elder.cell,goal,0,elder.movement_type,s.units)
		if elder.path.is_empty():
			# Some original patrol coordinates are on water. Choose a reachable
			# cell accepted by the original arrival mask, avoiding occupied cells.
			var cells: Array[Vector2i]=[]
			for y in range(-3,4):
				for x in range(-3,4):
					var p:=goal+Vector2i(x,y)
					if not _in_arrival_mask(Vector2i(x,y)):continue
					if s.walkable(p,elder.movement_type) and s.at_cell(p).is_empty():cells.append(p)
			cells.sort_custom(func(a,b):return a.distance_squared_to(goal)<b.distance_squared_to(goal))
			for p in cells:
				elder.path=s.attack_paths.route(elder.cell,p,0,elder.movement_type,s.units)
				if not elder.path.is_empty():break
		if not elder.path.is_empty():elder.destination=elder.path.back()
