extends "res://sim/school_twenty_four_battle.gd"
## T0041: five slots per recurring subroutine; independent route and entrance draws.


func start(s) -> void:
	patrol_mask=String(s.catalog.spells.masks["3"]).hex_decode()
	for script in s.scene_scripts:
		if script.sub==1:
			for cmd in script.commands:
				if cmd.opcode==124:
					var v:Array=cmd.values
					slots[v[0]]={"sub":v[2],"due":v[3]}
		if script.sub not in [20,21]:continue
		var wave:={"groups":[],"route":[],"centers":[]}
		for cmd in script.commands:
			var v:Array=cmd.values
			match cmd.opcode:
				136:
					if v[0]==32:wave.groups.append(v[1])
				146:
					if v[1]==2 and v[0]==1:wave.delay=[v[2],v[3]]
					if v[1]==2 and v[0]==4:wave.route=[v[2],v[3]]
				130:
					wave.centers.append(Vector2i(v[1],v[2]))
					wave.radius=v[3]
		waves[script.sub]=wave


func result(s) -> int:
	if s._source_status(1249).state==4:
		if s._source_status(1248).side==0:return 2 if s._own_casualties==0 else 5
		return 8
	if s.remaining_ticks==0:return 11
	if s.controlled_units().all(func(u):return u.side!=0 or u.source_state in [0,2,3,4,5]):return 14
	return -1
