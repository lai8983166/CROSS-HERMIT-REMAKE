extends "res://sim/school_twenty_four_battle.gd"
## The three allied survivors have no patrol route. The player orders their retreat.
const ESCORTS := [1237,1236,1235]


func start(s) -> void:
	patrol_mask=String(s.catalog.spells.masks["3"]).hex_decode()
	for ordinal in s.catalog.grade_objects:
		var ally: Dictionary=s.find_unit(1250-ordinal)
		ally.controllable=true
		protectees.append(ally)
	for script in s.scene_scripts:
		if script.sub==1:
			for cmd in script.commands:
				if cmd.opcode==124:
					var v:Array=cmd.values
					slots[v[0]]={"sub":v[2],"due":v[3]}
		if script.sub not in [20,21,22,23]:continue
		var wave:={"groups":[],"route":[]}
		for cmd in script.commands:
			var v:Array=cmd.values
			match cmd.opcode:
				136:
					if v[0]==32:wave.groups.append(v[1])
				146:
					if v[1]==2 and v[0]==1:wave.delay=[v[2],v[3]]
				130:
					wave.center=Vector2i(v[1],v[2])
					wave.radius=v[3]
		waves[script.sub]=wave


func result(s) -> int:
	var lost:=0
	var arrived:=0
	for ally in protectees:
		if ally.source_state in [2,3,4]:lost+=1
		elif s._on_region(ally,"1"):arrived+=1
	if lost==3:return 11
	if arrived+lost==3:
		if lost>0:return 8
		return 2 if s._own_casualties==0 else 5
	if s.controlled_units().all(func(u):return u.character_id>45 or u.source_state in [0,2,3,4,5]):return 14
	return -1


func _patrol(s,u: Dictionary) -> void:
	var route: Array=s.catalog.patrol_routes[str(u.patrol)]
	var index: int=u.get("patrol_index",0)
	var row: Array=route[index]
	var resume: int=u.get("patrol_resume",-1)
	if resume>=0 and s.elapsed<resume:return
	if resume<0:
		s._walk_patrol(u,Vector2i(row[0],row[1]),patrol_mask)
		if not u.get("patrol_finished",false):return
		if row[2]>0:
			u.patrol_resume=s.elapsed+row[2]
			return
	u.patrol_resume=-1
	u.patrol_finished=false
	u.patrol_index=(index+1)%route.size()
