extends RefCounted
## T0018 queues repeating group events and 434E90 checks castle ownership.
var gate_breached := false
var lost_object := 0
var slots := {}
var waves := {}


func start(s) -> void:
	for script in s.scene_scripts:
		var sub: int=script.sub
		if sub==1:
			for command in script.commands:
				if command.opcode==124:
					var v: Array=command.values
					slots[v[0]]={"sub":v[2],"due":v[3]}
		elif sub in range(20,25):
			var wave := {"groups":[],"gate":false}
			for command in script.commands:
				var v: Array=command.values
				match command.opcode:
					161:wave.gate=true
					136:
						if v[0]==32:wave.groups.append(v[1])
					130:
						wave.center=Vector2i(v[1],v[2])
						wave.radius=v[3]
					146:
						if v[1]==2:wave.delay=[v[2],v[3]]
			waves[sub]=wave


func advance(s) -> void:
	# Slots are scanned in native numeric order. Only one event runs at once.
	for slot in range(16):
		if not slots.has(slot) or slots[slot].due>s.elapsed:continue
		var sub: int=slots[slot].sub
		slots.erase(slot)
		for pending in slots:
			if pending>slot:slots[pending].due+=2
		var wave: Dictionary=waves[sub]
		if wave.gate and gate_breached:return
		var groups: Array=wave.groups.duplicate()
		for i in groups.size():
			var a:=int(s.rng.randi()%groups.size())
			var b:=int(s.rng.randi()%groups.size())
			var value: int=groups[a]
			groups[a]=groups[b]
			groups[b]=value
		for group in groups:
			if s.units.any(func(u):return u.get("group",-1)==group and u.side==5 and u.source_state==1):continue
			s._spawn_group(group,wave.center,wave.radius)
			break
		for next_slot in range(16):
			if not slots.has(next_slot):
				slots[next_slot]={"sub":sub,"due":s.elapsed+s.rng.randi_range(wave.delay[0],wave.delay[1]-1)}
				break
		return


func owned(s) -> int:
	return s.catalog.grade_objects.filter(func(n):return s.find_unit(1250-n).side==0).size()


func cleared(s) -> bool:
	# 4307B0 skips structures, obstacles and chests when counting combat enemies.
	for u in s.units:
		if u.category==5 and u.side==5 and u.character_id not in range(411,415) and u.source_state in [1,3]:return false
	return true


func result(s, unavailable: bool) -> int:
	for id in [1246,1245,1244]:
		if s.find_unit(id).source_state in [2,3,4]:gate_breached=true
	if owned(s)==3:
		if not cleared(s):return 8
		return 2 if s._own_casualties==0 else 5
	for n in s.catalog.grade_objects:
		if s.find_unit(1250-n).source_state in [2,3,4]:
			lost_object=n
			return 11
	return 14 if unavailable else -1
