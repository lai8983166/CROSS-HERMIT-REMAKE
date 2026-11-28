extends "res://sim/standalone_battle_session.gd"
## Local two-side practice on the original network selection 1.
const DATA := "res://assets/network_battle/catalog.json"
const DATA_SHA := "22183594aada0c94d9f0afcea77780633b9f8d484aa0a5fa819f65e1c5a67234"

func start(home: Array, away: Array, scenario := 71) -> bool:
	var raw:=FileAccess.get_file_as_string(DATA)
	if raw.sha256_text()!=DATA_SHA:return false
	var source: Dictionary=Limits._source_numbers(JSON.parse_string(raw))
	close()
	scene_id=scenario
	catalog=source.scene
	catalog.skins=source.skins
	if scenario in [42,43,93,94]:
		var path:="res://assets/terrain_practice_%d/catalog.json" if scenario in [93,94] else "res://assets/network_battle_%d/catalog.json"
		var extra_raw:=FileAccess.get_file_as_string(path % scenario)
		var hashes:={93:"4f5c5fc04614811480cd2b235adebf54900e8281cb63de0ce41b27e8aaea6d38",94:"31a4f172cd5f7c834073eb7400cfee2ee5e7efb471ea2947a2267b58cc6b0cf9",42:"92ff0fade58d99ef157f207268238d53fd3598edc5136f3db33fe25caec3fbf8",43:"e4a116c5e8050cf1afa4551d19edef9cde67d944a80c3f190dd86c8f3ac22914"}
		if extra_raw.sha256_text()!=hashes[scenario]:return false
		var extra: Dictionary=Limits._source_numbers(JSON.parse_string(extra_raw))
		catalog=extra.scene
		catalog.skins=source.skins.duplicate()
		catalog.skins.merge(extra.skins,true)
	elif scenario!=71:return false
	combat_rules=source.attack_rules
	_open_terrain()
	var config:=String(catalog.configuration_hex).hex_decode()
	var occupied:={}
	for actor in catalog.get("actors",[]):
		reserves[actor.instance_id]=actor
		if actor.state!=1:continue
		var position:=Vector2i(actor.cell[0],actor.cell[1])
		var enemy:=_actor_unit(actor,position)
		units.append(enemy)
		source_actors[actor.instance_id]=actor
		occupied[position]=true
	for side in (1 if scenario in [42,43] else 2):
		var group:=home if side==0 else away
		if group.is_empty() or group.size()>source.roster.size():return false
		var origin:=Vector2i(config[7+side*2],config[8+side*2])
		var radius:=int(config[15])
		if scenario in [93,94]:
			origin=Vector2i(config[7],config[8])+Vector2i(side*7,side*7)
			radius=12
		var seen:={}
		for i in group.size():
			var id: int=group[i]
			var entries: Array=source.roster.filter(func(candidate):return candidate.character_id==id)
			if entries.size()!=1 or seen.has(id):return false
			seen[id]=true
			var actor: Dictionary=entries[0].duplicate(true)
			actor.instance_id=id if side==0 else 1000+i
			var cell:=_formation_cell(origin,radius,actor.movement_type,i,occupied)
			if cell.x<0:return false
			occupied[cell]=true
			var record:=String(actor.record_hex).hex_decode()
			record.encode_u16(0,side+1)
			record[0xa4]=side
			actor.record_hex=record.hex_encode()
			var unit:=_actor_unit(actor,cell)
			unit.controllable=side==0
			unit.category=0 if side==0 else 5
			units.append(unit)
			if side==0:
				_participant_ids.append(id)
				_battle_stats[id]={"character_id":id,"count_field_aa":0,"contribution_field_ac":0,"status_field_ae":0}
	selected_id=home[0]
	_initial_enemies=enemies().size()
	remaining_ticks=0x7fffffff if config[16]==255 else int(config[16])*3600
	rng.seed=1703
	_ending_phase="active"
	ready=true
	reason="ready"
	return true

func _formation_cell(origin: Vector2i, radius: int, mode: int, index: int, occupied: Dictionary) -> Vector2i:
	var permutation:=[0,1,2,3,4]
	for i in ((index+1)%5)*3:
		var first: int=permutation[0]
		permutation[0]=permutation[i%5]
		permutation[i%5]=first
	for i in catalog.formation_grid.size():
		var row: Array=catalog.formation_grid[(i/5)*5+permutation[i%5]]
		var cell:=origin+Vector2i(row[0],row[1])
		if row[2]>radius or not Rect2i(0,0,field_width,field_height).has_point(cell) or occupied.has(cell):continue
		if catalog.passability[mode][cell.y*field_width+cell.x]!=0:return cell
	return Vector2i(-1,-1)

func _update_summoning() -> void:
	elapsed+=2
	if scene_id!=71:
		for unit in units.duplicate():
			if unit.life_kind==2 and unit.source_state==1 and unit.limits.hp>0 and reserves.has(unit.instance_id):
				_update_summoner(unit,unit.group,unit.lives,reserves[unit.instance_id].summon_interval)

func _admitted(unit: Dictionary, target: Dictionary) -> bool:
	return _ending_phase=="active" and not target.is_empty() and unit.side!=target.side and unit.limits.hp>0 and target.limits.hp>0

func _guard_target(unit: Dictionary) -> int:
	var best:=0x7fffffff
	var target:=-1
	for candidate in controlled_units():
		if not _admitted(unit,candidate):continue
		var distance:=_distance(unit,candidate)
		if distance<best:
			best=distance
			target=candidate.instance_id
	return target

func _check_before_actions() -> bool:
	return _detect_trial_end()

func _detect_trial_end() -> bool:
	var counts:=[0,0,0,0]
	for unit in units:
		if unit.side<4 and unit.source_state==1:counts[unit.side]+=1
	var selector:=0
	if scene_id in [42,43]:
		var objectives: Array=[1249] if scene_id==42 else [1249,1248,1247,1246]
		if objectives.all(func(id):return find_unit(id).get("source_state",-1)==4):
			selector=1 if _own_casualties==0 else 2
		elif counts[0]==0 or remaining_ticks==0:selector=5
	elif counts[0]==0 or counts[1]==0:
		selector=5 if counts[0]==0 else 1
	elif remaining_ticks==0:
		selector=5 if counts[0]<counts[1] else 3 if counts[0]==counts[1] else 1
	if selector==0:return false
	ending_sub=0
	_terminal_choice={"tactical_result_selector":selector,"script_sub":0}
	_begin_ending("mission_objectives_met" if selector in [1,2] else "time_limit" if remaining_ticks==0 else "own_force_defeated")
	return true
