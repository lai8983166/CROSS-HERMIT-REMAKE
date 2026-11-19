extends "res://sim/school_combat_session.gd"
## Source scenes and predicates on the existing explicit remake combat scheduler.
const AttackPaths := preload("res://sim/school_sortie_paths.gd")
const PlayerUnits := preload("res://sim/school_sortie_units.gd")
const SOURCE_PATH := "res://assets/school_sorties/catalog.json"
const SOURCE_SHA := "d272b6ad0da5a0da30676b8ae6ca4273dc045794b6470af419c7f44a14c4d376"
const SCENES_PATH := "res://data/school_adventure_scene_rules.json"
const SCENES_SHA := "c87a1ddcda957cc5b235dd35ef95bcd5385bf91c59aecea0fcb26cfb0d90266c"
const SEVEN_PATH := "res://assets/school_seven/catalog.json"
const SEVEN_SHA := "1e7d03f2b4fdb7517f8e43cc8931121b02fc747e3b881f6f3fbf8b207f24873c"
const Adventures := preload("res://sim/school_return_adventures.gd")
var event_rng := RandomNumberGenerator.new()
var recurring_events: Array = []
var rendezvous := false
var scene_id := 0
var elapsed := 0
var departure: Dictionary = {}
var scene_scripts: Array = []
var timers: Array = []
var ambushed: Array = []
var spawn_points: Array = []
var ending_sub := -1
var attack_paths: AttackPaths


func open(handoff: Dictionary, _combat: Dictionary = {}, raw := "") -> bool:
	if handoff.get("date") not in [[5,1],[5,2],[5,3],[5,4]]: return false
	var seven: bool=handoff["date"]==[5,4]
	if raw.is_empty():raw=FileAccess.get_file_as_string(SEVEN_PATH if seven else SOURCE_PATH).replace("\r\n","\n")
	if raw.sha256_text()!=(SEVEN_SHA if seven else SOURCE_SHA) or not handoff.get("supported",false) or not handoff.get("ready",false):return false
	if not handoff.get("prepared") is Dictionary or handoff.get("requested_states")!=[10,16] or handoff.get("round_cursor")!=1:return false
	var prepared: Dictionary=handoff["prepared"];var sid=prepared.get("adventure_id")
	if sid not in ([7] if seven else [8,17]) or prepared.get("round_count")!=1 or prepared.get("round_index")!=0:return false
	if not prepared.get("rounds") is Array or prepared["rounds"].size()!=1:return false
	var round_data: Dictionary=prepared["rounds"][0]
	var teachers=round_data.get("teacher_ids")
	if round_data.get("scene_id")!=sid:return false
	if teachers not in ([[101],[110],[101,110],[110,101]] if seven else [[101]]):return false
	var ids: Array=round_data.get("student_ids",[])
	if ids.is_empty() or ids.size()>(5 if seven else 4) or not handoff.get("participants") is Array or not handoff.get("growth") is Array:return false
	if ids.size()!=handoff["participants"].size() or ids.size()!=handoff["growth"].size():return false
	var source: Dictionary=Limits._source_numbers(JSON.parse_string(raw))
	var next_catalog: Dictionary=source["scenes"][str(sid)].duplicate(true)
	var identity: Dictionary=Adventures.seven_rules().get("scene",{}) if seven else Adventures.rules().get("scenes",{}).get(str(sid),{})
	if identity.is_empty() or handoff.get("scene")!=identity:return false
	var candidates: Array[Dictionary]=[];var seen := {}
	for id in ids:
		if not next_catalog["player_skins"].has(str(id)):return false
		if seen.has(id):return false
		seen[id]=true
		var p: Array=handoff["participants"].filter(func(v):return v.get("character_id")==id)
		var g: Array=handoff["growth"].filter(func(v):return v.get("character_id")==id)
		if p.size()!=1 or g.size()!=1:return false
		var unit := PlayerUnits.project(p[0],g[0],source["attack_rules"])
		if unit.is_empty():return false
		unit.merge({"instance_id":id,"skin_key":next_catalog["player_skins"][str(id)],"controllable":true,"category":0,
			"side":0,"source_state":1,"death_counted":false,"facing":"N","path":[],"destination":Vector2i(-1,-1),
			"move_started_frame":-100000,"visual":"idle","visual_started_frame":0,"target":-1,"dead_at":-1})
		candidates.append(unit)
	var width := 96 if sid in [7,17] else 64;var height := 144 if sid in [7,17] else 96
	var blocked := {}
	for actor in next_catalog["actors"]:
		if actor["state"]==1:blocked[Vector2i(actor["cell"][0],actor["cell"][1])]=true
	var rotation := 0
	for unit in candidates:
		rotation=(rotation+1)%5;var permutation := [0,1,2,3,4]
		for i in rotation*3:
			var first: int=permutation[0];permutation[0]=permutation[i%5];permutation[i%5]=first
		var found := false
		for i in next_catalog["formation_grid"].size():
			var row: Array=next_catalog["formation_grid"][(i/5)*5+permutation[i%5]]
			var cell := Vector2i(next_catalog["origin"][0]+row[0],next_catalog["origin"][1]+row[1])
			if row[2]>next_catalog["formation_radius"] or cell.x<0 or cell.y<0 or cell.x>=width or cell.y>=height or blocked.has(cell):continue
			if next_catalog["passability"][unit["movement_type"]][cell.y*width+cell.x]==0:continue
			unit["cell"]=cell;unit["from_cell"]=cell;blocked[cell]=true;found=true;break
		if not found:return false
	var rules_raw := FileAccess.get_file_as_string(SCENES_PATH).replace("\r\n","\n")
	if rules_raw.sha256_text()!=SCENES_SHA:return false
	var rules: Dictionary=Limits._source_numbers(JSON.parse_string(rules_raw))
	if rules.get("source_image_sha256")!=Limits.SOURCE_SHA or (next_catalog if seven else rules["scenes"][str(sid)])["script_sha256"]!=identity["script_sha256"]:return false
	var wave_raw := FileAccess.get_file_as_string(REINFORCEMENTS_PATH).replace("\r\n","\n")
	if wave_raw.sha256_text()!=REINFORCEMENTS_SHA:return false
	var wave: Dictionary=JSON.parse_string(wave_raw)
	var mask := String(wave["capture_mask"]["hex"]).hex_decode()
	if mask.size()!=121:return false
	close()
	scene_id=sid;field_width=width;field_height=height;catalog=next_catalog
	catalog["skins"]=source["skins"];combat_rules=source["attack_rules"]
	attack_paths=AttackPaths.new(width,height,catalog["passability"])
	units=candidates;departure=handoff.duplicate(true);_participant_ids=ids.duplicate()
	for actor in catalog["actors"]:
		reserves[actor["instance_id"]]=actor.duplicate(true)
		if actor["state"]!=1:continue
		var unit := _actor_unit(actor,Vector2i(actor["cell"][0],actor["cell"][1]))
		units.append(unit);source_actors[actor["instance_id"]]=actor.duplicate(true)
	for mode in range(5):
		var map := SimMapData.new();map.cell_w=width;map.cell_h=height
		var zeros := [];zeros.resize(width*height);zeros.fill(0)
		map._layers={"terrain":catalog["passability"][mode].duplicate(),"variant":zeros,"object":zeros};_maps.append(map)
	_capture_mask=mask
	scene_scripts=(next_catalog if seven else rules["scenes"][str(sid)])["scripts"].duplicate(true);spawn_points=rules["scene17_repeat_rows"]
	_opening_pages=_pages(1);_opening_index=0;_ending_phase="opening"
	ready=true;selected_id=ids[0];reason="opening";rng.seed=20261115+sid;_placement_rotation=rotation
	remaining_ticks=108000 if sid==8 else -1;_initial_enemies=enemies().size()
	for id in ids:_battle_stats[id]={"character_id":id,"count_field_aa":0,"contribution_field_ac":0,"status_field_ae":0}
	if seven:event_rng.seed=20261119+sid
	if sid in [7,8]:
		for cmd in scene_scripts[0]["commands"]:
			var v: Array=cmd.get("values",[])
			if seven and cmd["opcode"]==124 and v.size()==4 and v[2]==20:recurring_events.append({"at":v[3]})
			if cmd["opcode"]==136 and v.size()==7 and v[0]==28:timers.append({"at":v[1],"slot":v[2],"group":v[3],"center":Vector2i(v[4],v[5]),"radius":v[6]})
	else:
		for at in [36000,39600,43200,46800]:timers.append({"at":at,"repeat":true})
		for row in [[10800,5,5],[21600,4,7],[25200,3,10]]:timers.append({"at":row[0],"group":row[1],"ai_parameter":row[2]})
	return true


func _attack_path(unit: Dictionary, target: Dictionary) -> Array[Vector2i]:
	return attack_paths.route(unit["cell"],target["cell"],unit["combat"]["attack_range"],unit["movement_type"],units)


func _actor_unit(actor: Dictionary, cell: Vector2i) -> Dictionary:
	var unit := {"instance_id":actor["instance_id"],"character_id":actor["character_id"],"job":actor["job"],
		"movement_type":actor["movement_type"],"limits":actor["limits"].duplicate(true),"controllable":false,
		"category":6 if _capture_role(actor["character_id"]) else actor["category"],"skin_key":actor["skin_key"],"combat":actor["combat"].duplicate(true),
		"cell":cell,"from_cell":cell,"facing":"S","path":[],"destination":Vector2i(-1,-1),"move_started_frame":-100000,
		"visual":"idle","visual_started_frame":frame,"target":-1,"dead_at":-1}
	_apply_record_fields(unit,actor)
	if actor.has("source_ai_request"):unit["source_ai_request"]=actor["source_ai_request"].duplicate()
	return unit


static func _capture_role(role: int) -> bool:return role>=387 and role<=406


func _pages(sub: int, block := 0) -> Array:
	for row in scene_scripts:
		if row["block"]==block and row["sub"]==sub:return row["pages"].duplicate(true)
	return []


func opening_snapshot() -> Dictionary:
	return {"page_index":_opening_index,"page_count":_opening_pages.size(),
		"page":_opening_pages[_opening_index].duplicate(true) if _ending_phase=="opening" else [],
		"awaiting_confirmation":_ending_phase=="opening","completed":_opening_index==_opening_pages.size()}


func advance_opening(confirmed := false) -> bool:
	if not ready or _ending_phase!="opening" or not confirmed:return false
	_record_command([1,1]);_opening_index+=1
	if _opening_index==_opening_pages.size():_ending_phase="active";reason="ready"
	return true


func _update_captures() -> void:
	for object in units:
		if not _capture_role(object["character_id"]):continue
		if object["capture_elapsed"]>=0:
			object["capture_elapsed"]+=1
			if object["capture_elapsed"]>=Progression.capture_transition_ticks(object["character_id"]):
				object["side"]=object["capture_target"];object["capture_hold"]=Progression.capture_hold_limit(object["side"])
				object["capture_elapsed"]=-1;object["capture_target"]=-1
			continue
		var counts := [];counts.resize(16);counts.fill(0)
		for unit in units:
			if unit==object or unit["source_state"]!=1 or unit["side"]==7:continue
			var delta: Vector2i=(object["cell"]-unit["cell"]).abs()
			if delta.x<=5 and delta.y<=5 and _capture_mask[(delta.y+5)*11+delta.x+5]!=0:counts[unit["side"]]=(counts[unit["side"]]+1)%256
		var candidate := Progression.capture_candidate(object["side"],counts)
		if candidate==4 and object["side"]!=7:candidate=-1
		if candidate<0:object["capture_hold"]=mini(object["capture_hold"]+1,Progression.capture_hold_limit(object["side"]))
		else:
			object["capture_hold"]-=1
			if object["side"]==7 or object["capture_hold"]<=0:object["capture_target"]=candidate;object["capture_elapsed"]=0


func _activate(identity: int, center: Vector2i, radius: int) -> bool:
	var old := find_unit(identity)
	if not reserves.has(identity) or (not old.is_empty() and old["source_state"] not in [0,2,3,4]):return false
	var actor: Dictionary=reserves[identity];var blocked := _blocked(identity)
	_placement_rotation=(_placement_rotation+1)%5
	var permutation := [0,1,2,3,4]
	for i in _placement_rotation*3:
		var first: int=permutation[0];permutation[0]=permutation[i%5];permutation[i%5]=first
	for i in catalog["formation_grid"].size():
		var row: Array=catalog["formation_grid"][(i/5)*5+permutation[i%5]];var cell := center+Vector2i(row[0],row[1])
		if row[2]>radius or not walkable(cell,actor["movement_type"]) or blocked.has(cell):continue
		var next := _actor_unit(actor,cell);next["source_state"]=1
		if old.is_empty():units.append(next)
		else:old.clear();old.merge(next)
		for request in _pending_activations.duplicate():
			if request["identity"]==identity:_pending_activations.erase(request)
		source_actors[identity]=actor.duplicate(true);return true
	return false


func _spawn_group(group: int, center: Vector2i, radius: int, ai_parameter := -1) -> void:
	for id in reserves:
		var raw := String(reserves[id]["record_hex"]).hex_decode()
		if raw[0x98]==group and not _activate(id,center,radius):
			var old := find_unit(id)
			if (old.is_empty() or old["source_state"] in [0,2,3,4]) and not _pending_activations.any(func(r):return r["identity"]==id):
				_pending_activations.append({"identity":id,"center":center,"radius":radius})
	if ai_parameter>=0:_set_group_ai(group,ai_parameter)


func _set_group_ai(group: int, parameter: int) -> void:
	# Preserve source requests; pursuit cadence remains the declared local scheduler.
	for unit in units:
		if unit.get("group",0)==group:unit["source_ai_request"]=[0,parameter,1]
	for id in reserves:
		if String(reserves[id]["record_hex"]).hex_decode()[0x98]==group:reserves[id]["source_ai_request"]=[0,parameter,1]


func _update_summoning() -> void:
	# Elapsed source units advance by two at the explicitly local 30Hz scheduler.
	elapsed+=2
	if scene_id==7:
		for tower in [1246,1245]:
			if find_unit(tower)["side"]!=0:continue
			for timer in timers.duplicate():
				if timer["slot"] in ([1,2,3] if tower==1246 else [4,5,6]):timers.erase(timer)
		for event in recurring_events:
			if event["at"]>elapsed:continue
			_repeat_seven_group()
			event["at"]=elapsed+event_rng.randi_range(3600,18000)
			break
	for timer in timers.duplicate():
		if timer["at"]>elapsed:continue
		timers.erase(timer)
		if scene_id in [7,8]:_spawn_group(timer["group"],timer["center"],timer["radius"])
		elif timer.has("ai_parameter"):_set_group_ai(timer["group"],timer["ai_parameter"])
		else:_repeat_group();timers.append({"at":elapsed+int(rng.randi()%16200)+1800,"repeat":true})
		break # One timer delivery per local opportunity.
	if scene_id==17:
		for number in [45,46]:
			var unit := find_unit(1250-number)
			if unit.is_empty() or unit["source_state"]!=4 or ambushed.has(number):continue
			ambushed.append(number);var point: Array=spawn_points[rng.randi()%4]
			_spawn_group(number-31,Vector2i(point[0],point[1]),point[2],point[3])


func _repeat_seven_group() -> void:
	# T0007 sub20 requests one eliminated group among the original groups 1..15.
	var groups := range(1,16)
	for i in groups.size():
		var a := event_rng.randi_range(0,groups.size()-1)
		var b := event_rng.randi_range(0,groups.size()-1)
		var old: int=groups[a]
		groups[a]=groups[b]
		groups[b]=old
	var east := event_rng.randi_range(0,1)==1
	for group in groups:
		if units.any(func(u):return u.get("group",0)==group and u["side"]==5 and u["source_state"]==1):continue
		var parameters := [8,14,15] if east else [9,13,16,17]
		var parameter: int=parameters[event_rng.randi_range(0,parameters.size()-1)]
		_spawn_group(group,Vector2i(79,66) if east else Vector2i(12,82),10,parameter)
		break


func _repeat_group() -> void:
	var groups := []
	for group in range(1,16):
		if group==13:continue
		if group>=14 and _source_status(1205-(group-14))["state"] not in [2,3,4]:continue
		groups.append(group)
	for i in groups.size():
		var first := int(rng.randi()%groups.size());var second := int(rng.randi()%groups.size())
		var old: int=groups[first];groups[first]=groups[second];groups[second]=old
	for group in groups:
		if units.any(func(u):return u.get("group",0)==group and u["side"]==5 and u["source_state"]==1):continue
		var point: Array=spawn_points[rng.randi()%4]
		_spawn_group(group,Vector2i(point[0],point[1]),point[2],point[3]);break


func _detect_trial_end() -> bool:
	var sub := -1
	var unavailable := controlled_units().filter(func(u):return u["character_id"]<=45).all(func(u):return u["limits"]["hp"]<=0)
	if scene_id==7:
		var escort := find_unit(1248)
		if rendezvous and _on_region(escort,"2"):
			var towers: bool=find_unit(1246)["side"]==0 and find_unit(1245)["side"]==0
			sub=(2 if _own_casualties==0 else 5) if towers else 8
		if unavailable:sub=11
		elif escort["source_state"]==4:sub=14
		if sub<0 and not rendezvous and controlled_units().any(func(u):return _on_region(u,"1")):
			_event_pages=_pages(1,1)
			_event_index=0
			_ending_phase="event20"
			_accumulator=0.0
			return true
	elif scene_id==8:
		var owned := 0;var hostile := 0
		for number in [3,4,5]:
			var unit := find_unit(1250-number)
			if unit["side"]==0:owned+=1
			elif unit["side"]==5:hostile+=1
		if elapsed>=108000:
			var all_owned := owned==3
			for number in [1,2,6]:all_owned=all_owned and find_unit(1250-number)["side"]==0
			sub=2 if all_owned and _own_casualties==0 else 5 if all_owned else 8 if owned==3 else 11
		elif hostile==3:sub=15
		elif unavailable:sub=14
	else:
		if _at_exit():
			if elapsed<54000:sub=14
			else:
				var complete := _training_objectives()
				sub=2 if complete.count(true)==3 and _own_casualties==0 else 5 if complete.count(true)==3 else 8 if complete.has(true) else 11
		if unavailable:sub=14
	if sub<0:return false
	ending_sub=sub
	_terminal_choice={"tactical_result_selector":1 if sub==2 else 2 if sub==5 else 3 if sub==8 else 4 if sub==11 else 5,"script_sub":sub}
	_begin_ending("squad_defeated" if unavailable else "bases_lost" if sub==15 else "training_ended" if scene_id==17 else "escort_lost" if sub==14 else "mission_objectives_met" if scene_id==7 else "defense_completed")
	return true


func _on_region(unit: Dictionary, region: String) -> bool:
	return unit["source_state"]==1 and unit["limits"]["hp"]>0 and catalog["regions"][region].has(unit["cell"].y*field_width+unit["cell"].x)


func advance_event() -> bool:
	if scene_id!=7 or _ending_phase!="event20":return false
	_record_command([2])
	_event_index+=1
	if _event_index==_event_pages.size():
		for identity in [1248,1247]:
			var ally := find_unit(identity)
			ally["side"]=0
			ally["controllable"]=true
		rendezvous=true
		_ending_phase="active"
		reason="escort_ready"
	return true


func _admitted(unit: Dictionary, target: Dictionary) -> bool:
	if not super._admitted(unit,target):return false
	if scene_id==7 and unit["category"]==5:
		# Local guards engage nearby targets, respecting their original reach.
		return _distance(unit,target)<=unit["combat"]["attack_range"]+2
	return true


func _training_objectives() -> Array:
	var result := [true,true,true]
	for unit in units:
		if unit["controllable"]:continue
		var role: int=unit["character_id"];var removed: bool=unit["source_state"] in [2,3,4]
		if role>=387 and role<=404:result[0]=result[0] and unit["side"]==0 and not removed
		elif role in [405,406]:result[1]=result[1] and unit["side"]==0 and not removed
		elif role>=411 and role<=414:result[2]=result[2] and unit["side"]==5 and removed
	return result


func _at_exit() -> bool:
	# Filled from this scene's logical event layer by the source exporter.
	for unit in controlled_units():
		if unit["source_state"]==1 and unit["limits"]["hp"]>0 and catalog.get("exit_cells",[]).has(unit["cell"].y*field_width+unit["cell"].x):return true
	return false


func result_inputs() -> Dictionary:
	if _ending_phase!="summary" or _terminal_choice.is_empty(): return {}
	var config := String(departure["scene"]["configuration_hex"]).hex_decode()
	var slots := []
	for index in range(16):
		var number := int(config[26+index])
		var unit := find_unit(1250-number) if number>0 else {}
		slots.append(int(unit.get("side",-1)==0))
	var no_hostile := true
	for unit in units:
		if unit["category"]==5 and unit["side"]!=0 and unit["source_state"] in [1,3]:
			no_hostile=false
			break
	if no_hostile:
		for identity in reserves:
			var raw := String(reserves[identity]["record_hex"]).hex_decode()
			if raw[0x96]!=3 and _source_status(identity)["state"]==0:
				no_hostile=false
				break
	var time_key := 0
	if config[17]>0:time_key=1 if elapsed<=config[17]*3600 else 2 if elapsed<=config[18]*3600 else 3
	return {"scene_id":scene_id,"result_selector":_terminal_choice["tactical_result_selector"],
		"time_key":time_key,"objective_slots":slots,"unit_condition_key":2 if no_hostile else 1,
		"units":_participant_ids.map(func(id):return _battle_stats[id].duplicate(true)),
		"clock_seed":4660,"growth_seed":4660}


func ending_snapshot() -> Dictionary:
	var result := super.ending_snapshot()
	result["scene_id"]=scene_id;result["elapsed"]=elapsed;result["script_sub"]=ending_sub
	result["text"]=_pages(ending_sub);return result


func close() -> void:
	super.close();recurring_events.clear();rendezvous=false;attack_paths=null;scene_id=0;elapsed=0;departure.clear();scene_scripts.clear();timers.clear();ambushed.clear();spawn_points.clear();ending_sub=-1
