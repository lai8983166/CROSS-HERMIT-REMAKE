extends "res://sim/school_combat_session.gd"
## Source scenes and predicates on the existing explicit remake combat scheduler.
const AttackPaths := preload("res://sim/school_sortie_paths.gd")
const PlayerUnits := preload("res://sim/school_sortie_units.gd")
const JULY_FIVE_PATH := "res://assets/school_july_five/catalog.json"
const JULY_FIVE_SHA := "baaa436fa0a6892cdedb5d50237e0d17f83b86cad582776726622090233bc132"
const SOURCE_PATH := "res://assets/school_sorties/catalog.json"
const SOURCE_SHA := "d272b6ad0da5a0da30676b8ae6ca4273dc045794b6470af419c7f44a14c4d376"
const SCENES_PATH := "res://data/school_adventure_scene_rules.json"
const SCENES_SHA := "c87a1ddcda957cc5b235dd35ef95bcd5385bf91c59aecea0fcb26cfb0d90266c"
const SEVEN_PATH := "res://assets/school_seven/catalog.json"
const SEVEN_SHA := "1e7d03f2b4fdb7517f8e43cc8931121b02fc747e3b881f6f3fbf8b207f24873c"
const Dungeon := preload("res://sim/school_fourteen_dungeon.gd")
const TwentyOne := preload("res://sim/school_twenty_one_battle.gd")
const TWENTY_ONE_PATH := "res://assets/school_twenty_one/catalog.json"
const TWENTY_ONE_SHA := "929718b54932a1a71f9bc986022e191218a7be4bc4312051e3752ad18f8136c5"
var siege: TwentyOne
const TWENTY_PATH := "res://assets/school_twenty/catalog.json"
const TWENTY_SHA := "72ca556e391eb80595f21a4b58cb4b33abdd9f097df5b3635d0fe78ef6db76ba"
const FOURTEEN_PATH := "res://assets/school_fourteen/catalog.json"
const FOURTEEN_SHA := "bcb8592021a4bd031b7ada6b19e5f5ddff2fe1f4d8c8834f419498d85b75e932"
const NINE_PATH := "res://assets/school_nine/catalog.json"
const NINE_SHA := "554f8368f8fc2cbad2f806d9e6a3fac116f7835334822f53e84ece1691a3f49d"
# 4DA7F0 scene 9 -> 6A9B60, route 2 -> 6A9A68: (23,67), no wait, end.
const NINE_PATROL_GOAL := Vector2i(23,67)
const Castle := preload("res://sim/school_eighteen_castle.gd")
const EIGHTEEN_PATH := "res://assets/school_eighteen/catalog.json"
const EIGHTEEN_SHA := "f0786cc9fb448261a9b363914675bf2bbcf1c4485cf7e467729cfd970f131004"
const Prayer := preload("res://sim/school_thirteen_prayer.gd")
const THIRTEEN_PATH := "res://assets/school_thirteen/catalog.json"
const THIRTEEN_SHA := "285c29f1c9f9272a4b9ff1cde3c3b2e65442d20e1a1f1c7c13f735b763f65b11"
const TenEscort := preload("res://sim/school_ten_escort.gd")
const TEN_PATH := "res://assets/school_ten/catalog.json"
const TEN_SHA := "c8e490dd15f511aae8ff4c46550d28da47034b8caba99594e12036df60d5aebf"
const SIX_PATH := "res://assets/school_six/catalog.json"
const SIX_SHA := "6950db913e532eed94b4e2f8522cdde8f928c84eb32d9785268ae4952d6fc5fd"
const FOUR_PATH := "res://assets/school_four/catalog.json"
const FOUR_SHA := "c22c94c6e20614b96da655537beba004d66c8704f553ec52bbcf4da5d32567d5"
const MAY_FIVE_JOB_SHA := "bb97f131787378887731413a15b45dbbff92bc78198c918413c651f54d97c0b7"
const Adventures := preload("res://sim/school_return_adventures.gd")
var event_rng := RandomNumberGenerator.new()
var recurring_events: Array = []
var field_spell: Dictionary = {}
var healing_spell: Dictionary = {}
var healing_impacts: Array = []
var castle: Castle
var prayer: Prayer
var escort_route: TenEscort
var dungeon: Dungeon
var knight_released := false
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
var weapon_masks: Array[PackedByteArray] = []
var weapon_distances := PackedByteArray()


func open(handoff: Dictionary, _combat: Dictionary = {}, raw := "") -> bool:
	if handoff.get("date") not in [[5,1],[5,2],[5,3],[5,4],[5,5],[6,1],[6,2],[6,3],[6,4],[6,5],[7,1],[7,2],[7,3],[7,4],[7,5],[8,2],[8,3],[8,4]]: return false
	var twenty_one: bool=handoff["date"]==[8,3]
	var august: bool=twenty_one or handoff["date"]==[8,2]
	var twenty: bool=handoff["date"]==[8,2]
	var august_training: bool=handoff["date"]==[8,4]
	var expanded_training: bool=handoff["date"]==[7,5] or august_training
	var july: bool=handoff["date"][0]==7
	if not handoff.get("prepared") is Dictionary:return false
	var fourteen: bool=handoff["date"]==[7,4]
	var nine: bool=handoff["date"]==[7,3]
	var eighteen: bool=handoff["date"]==[7,1] and handoff["prepared"].get("adventure_id")==18
	var june_five: bool=handoff["date"] in [[6,5],[8,4]] or (july and not eighteen and not nine and not fourteen)
	var thirteen: bool=handoff["date"]==[6,4]
	var ten: bool=handoff["date"]==[6,3]
	var six: bool=handoff["date"]==[6,2]
	var four: bool=handoff["date"]==[6,1]
	var may_five: bool=handoff["date"]==[5,5]
	var seven: bool=handoff["date"]==[5,4]
	if raw.is_empty():raw=FileAccess.get_file_as_string(TWENTY_ONE_PATH if twenty_one else TWENTY_PATH if twenty else FOURTEEN_PATH if fourteen else NINE_PATH if nine else EIGHTEEN_PATH if eighteen else THIRTEEN_PATH if thirteen else TEN_PATH if ten else SIX_PATH if six else FOUR_PATH if four else SEVEN_PATH if seven else SOURCE_PATH).replace("\r\n","\n")
	if raw.sha256_text()!=(TWENTY_ONE_SHA if twenty_one else TWENTY_SHA if twenty else FOURTEEN_SHA if fourteen else NINE_SHA if nine else EIGHTEEN_SHA if eighteen else THIRTEEN_SHA if thirteen else TEN_SHA if ten else SIX_SHA if six else FOUR_SHA if four else SEVEN_SHA if seven else SOURCE_SHA) or not handoff.get("supported",false) or not handoff.get("ready",false):return false
	if not handoff.get("prepared") is Dictionary or handoff.get("requested_states")!=[10,16] or handoff.get("round_cursor")!=1:return false
	var prepared: Dictionary=handoff["prepared"];var sid=prepared.get("adventure_id")
	if sid not in ([21] if twenty_one else [20] if twenty else [14] if fourteen else [9] if nine else [18] if eighteen else [17] if june_five else [13] if thirteen else [10] if ten else [6] if six else [4] if four else [7] if seven else [8,17]) or prepared.get("round_count")!=1 or prepared.get("round_index")!=0:return false
	if not prepared.get("rounds") is Array or prepared["rounds"].size()!=1:return false
	var round_data: Dictionary=prepared["rounds"][0]
	var teachers=round_data.get("teacher_ids")
	if round_data.get("scene_id")!=sid:return false
	if may_five or four or six or ten or thirteen or eighteen or nine or fourteen or august or june_five:
		if not teachers is Array or teachers.is_empty() or teachers.size()>(5 if august_training else 4 if june_five or eighteen or nine or fourteen or august else 3):return false
		for teacher in teachers:
			if teacher not in ([101,110,115,116,118] if august_training else [101,110,115,118] if june_five or eighteen or nine or fourteen or august else [101,110,115]) or teachers.count(teacher)!=1:return false
	elif teachers not in ([[101],[110],[101,110],[110,101]] if seven else [[101]]):return false
	var ids: Array=round_data.get("student_ids",[])
	if ids.is_empty() or ids.size()>(10 if august or expanded_training else 8 if fourteen or nine or eighteen or june_five or six or ten or thirteen else 7 if four else 6 if may_five else 5 if seven else 4) or not handoff.get("participants") is Array or not handoff.get("growth") is Array:return false
	if ids.size()!=handoff["participants"].size() or ids.size()!=handoff["growth"].size():return false
	var source: Dictionary=Limits._source_numbers(JSON.parse_string(raw))
	var next_catalog: Dictionary=source["scenes"][str(sid)].duplicate(true)
	if four or six or ten or thirteen or eighteen or nine or fourteen or august:source["attack_rules"]["bow189_hex"]=next_catalog["bow189_hex"]
	if june_five and not _add_june_five_players(next_catalog,source):return false
	if (expanded_training or august) and not _add_july_five_players(next_catalog,source):return false
	if may_five and not _add_may_five_players(next_catalog,source):return false
	var identity: Dictionary=Adventures.twenty_one_rules().get("scene",{}) if twenty_one else Adventures.twenty_rules().get("scene",{}) if twenty else Adventures.fourteen_rules().get("scene",{}) if fourteen else Adventures.nine_rules().get("scene",{}) if nine else Adventures.eighteen_rules().get("scene",{}) if eighteen else Adventures.thirteen_rules().get("scene",{}) if thirteen else Adventures.ten_rules().get("scene",{}) if ten else Adventures.six_rules().get("scene",{}) if six else Adventures.four_rules().get("scene",{}) if four else Adventures.seven_rules().get("scene",{}) if seven else Adventures.rules().get("scenes",{}).get(str(sid),{})
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
		if four or six or ten or thirteen or eighteen or nine or fourteen or august:
			var job := String(source["attack_rules"]["jobs"][str(unit["job"])]["job_hex"]).hex_decode()
			var attr: Array=unit["input"]["attributes"]
			if eighteen or nine or fourteen or august:
				var weapon := String(source["attack_rules"]["jobs"][str(unit["job"])]["attack_hex"]).hex_decode()
				unit["normal_heal"]=weapon.decode_u16(2)==5
			if thirteen:unit["family_bit"]=1 << (int(job[2])-1)
			unit["recovery"]=[clampi(int(job.decode_u16(8)-attr[5]-attr[0]*0.5),30,999),
				clampi(int(job.decode_u16(12)-attr[6]-attr[3]*0.5),30,999)]
			unit["recovery_clock"]=[0,0]
		candidates.append(unit)
	var width := 128 if fourteen or twenty_one else 96 if sid in [7,10,13,17] else 64;var height := 192 if fourteen or twenty_one else 144 if sid in [7,10,13,17] else 96
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
	if rules.get("source_image_sha256")!=Limits.SOURCE_SHA or (next_catalog if (seven or four or six or ten or thirteen or eighteen or nine or fourteen or august) else rules["scenes"][str(sid)])["script_sha256"]!=identity["script_sha256"]:return false
	var wave_raw := FileAccess.get_file_as_string(REINFORCEMENTS_PATH).replace("\r\n","\n")
	if wave_raw.sha256_text()!=REINFORCEMENTS_SHA:return false
	var wave: Dictionary=JSON.parse_string(wave_raw)
	var mask := String(wave["capture_mask"]["hex"]).hex_decode()
	if mask.size()!=121:return false
	close()
	scene_id=sid;field_width=width;field_height=height;catalog=next_catalog
	catalog["skins"]=source["skins"];combat_rules=source["attack_rules"]
	attack_paths=AttackPaths.new(width,height,catalog["passability"])
	if august:
		# 477AD9 -> 47BED0 asks 43C1D0 for the MAPCOM mask at the
		# attack radius. For example (3,1) is in range of a melee weapon.
		weapon_distances.resize(33*33)
		weapon_distances.fill(255)
		for reach in range(33):
			var reach_mask := String(catalog.spells.masks[str(reach)]).hex_decode()
			weapon_masks.append(reach_mask)
			for dy in range(reach+1):
				for dx in range(reach+1):
					var index := dy*33+dx
					if weapon_distances[index]==255 and reach_mask[(dy+reach)*(2*reach+1)+dx+reach]!=0:weapon_distances[index]=reach
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
	scene_scripts=(next_catalog if (seven or four or six or ten or thirteen or eighteen or nine or fourteen or august) else rules["scenes"][str(sid)])["scripts"].duplicate(true);spawn_points=rules["scene17_repeat_rows"]
	_opening_pages=_pages(1);_opening_index=0;_ending_phase="opening"
	ready=true;selected_id=ids[0];reason="opening";rng.seed=20261115+sid;_placement_rotation=rotation
	remaining_ticks=int(String(next_catalog["configuration_hex"]).hex_decode()[16])*3600 if thirteen or nine else 36000 if four else 108000 if sid==8 else -1;_initial_enemies=enemies().size()
	for id in ids:_battle_stats[id]={"character_id":id,"count_field_aa":0,"contribution_field_ac":0,"status_field_ae":0}
	if twenty_one:
		siege=TwentyOne.new()
		siege.start(self)
		_ending_phase="active"
		reason="ready"
	if fourteen:
		dungeon=Dungeon.new()
		dungeon.start(self)
	if eighteen:
		castle=Castle.new()
		castle.start(self)
	if thirteen:
		prayer=Prayer.new()
		prayer.start(self)
	if ten:
		escort_route=TenEscort.new()
		escort_route.start(self)
	if seven:event_rng.seed=20261119+sid
	if sid in [7,8,13]:
		for cmd in scene_scripts[0]["commands"]:
			var v: Array=cmd.get("values",[])
			if seven and cmd["opcode"]==124 and v.size()==4 and v[2]==20:recurring_events.append({"at":v[3]})
			if cmd["opcode"]==136 and v.size()==7 and v[0]==28:timers.append({"at":v[1],"slot":v[2],"group":v[3],"center":Vector2i(v[4],v[5]),"radius":v[6]})
	elif sid==17:
		for at in [36000,39600,43200,46800]:timers.append({"at":at,"repeat":true})
		for row in [[10800,5,5],[21600,4,7],[25200,3,10]]:timers.append({"at":row[0],"group":row[1],"ai_parameter":row[2]})
	return true


static func _add_june_five_players(scene: Dictionary, source: Dictionary) -> bool:
	var raw := FileAccess.get_file_as_string(THIRTEEN_PATH).replace("\r\n","\n")
	if raw.sha256_text()!=THIRTEEN_SHA:return false
	var previous: Dictionary=Limits._source_numbers(JSON.parse_string(raw))
	var field: Dictionary=previous["scenes"]["13"]
	scene["player_skins"].merge(field["player_skins"])
	for key in field["player_skins"].values():
		if not source["skins"].has(key):source["skins"][key]=previous["skins"][key]
	source["attack_rules"]["jobs"].merge(previous["attack_rules"]["jobs"])
	source["attack_rules"]["bow189_hex"]=field["bow189_hex"]
	return true


static func _add_july_five_players(scene: Dictionary, source: Dictionary) -> bool:
	var raw := FileAccess.get_file_as_string(JULY_FIVE_PATH).replace("\r\n","\n")
	if raw.sha256_text()!=JULY_FIVE_SHA:return false
	var recruits: Dictionary=Limits._source_numbers(JSON.parse_string(raw))
	scene.player_skins.merge(recruits.player_skins)
	source.skins.merge(recruits.skins)
	source.attack_rules.jobs.merge(recruits.jobs)
	return true


static func _add_may_five_players(scene: Dictionary, source: Dictionary) -> bool:
	var seven_raw := FileAccess.get_file_as_string(SEVEN_PATH).replace("\r\n","\n")
	var job_raw := FileAccess.get_file_as_string("res://data/school_may_five_sortie_job.json").replace("\r\n","\n")
	if seven_raw.sha256_text()!=SEVEN_SHA or job_raw.sha256_text()!=MAY_FIVE_JOB_SHA:return false
	var seven: Dictionary=Limits._source_numbers(JSON.parse_string(seven_raw))
	var escort: Dictionary=seven["scenes"]["7"]
	var skin_keys := {"8":escort["player_skins"]["8"]}
	for actor in escort["actors"]:
		if actor["character_id"]==6:skin_keys["6"]=actor["skin_key"]
	if not skin_keys.has("6"):return false
	scene["player_skins"].merge(skin_keys)
	for key in skin_keys.values():source["skins"][key]=seven["skins"][key]
	source["attack_rules"]["jobs"]["2"]=Limits._source_numbers(JSON.parse_string(job_raw))
	source["attack_rules"]["jobs"]["8"]=seven["attack_rules"]["jobs"]["8"]
	return true


func _distance(a: Dictionary, b: Dictionary) -> int:
	if scene_id in [20,21]:
		var delta: Vector2i=(a.cell-b.cell).abs()
		if delta.x<=32 and delta.y<=32 and weapon_distances[delta.y*33+delta.x]!=255:
			return weapon_distances[delta.y*33+delta.x]
	return super._distance(a,b)


func _route_units(mover: Dictionary) -> Array:
	if scene_id not in [20,21]:return units
	# 47E02A resolves an occupied cell. 47E05A permits same-side
	# traversal, and 47E0AD keeps full speed past a stationary gate.
	return units.filter(func(u):return u.side!=mover.side)


func _wait_for_occupant(mover: Dictionary, cell: Vector2i) -> bool:
	if scene_id not in [20,21] or (frame/int(catalog.interaction.move_interval))%2==0:return false
	for u in units:
		if u.instance_id!=mover.instance_id and u.cell==cell and u.side==mover.side and u.limits.hp>0:
			if mover.combat.movement_rate<=u.combat.movement_rate:return true
	return false


func _blocked(identity: int) -> Dictionary:
	if scene_id not in [20,21]:return super._blocked(identity)
	var mover:=find_unit(identity)
	if mover.is_empty():return super._blocked(identity)
	var blocked := {}
	for u in _route_units(mover):
		if u.instance_id!=identity and u.limits.hp>0:blocked[u.cell]=true
	return blocked


func _attack_path(unit: Dictionary, target: Dictionary) -> Array[Vector2i]:
	var reach: int=unit.combat.attack_range
	var mask := weapon_masks[reach] if scene_id in [20,21] and reach<weapon_masks.size() else PackedByteArray()
	return attack_paths.route(unit.cell,target.cell,reach,unit.movement_type,_route_units(unit),mask)


func _actor_unit(actor: Dictionary, cell: Vector2i) -> Dictionary:
	var unit := {"instance_id":actor["instance_id"],"character_id":actor["character_id"],"job":actor["job"],
		"movement_type":actor["movement_type"],"limits":actor["limits"].duplicate(true),"controllable":false,
		"category":6 if _capture_role(actor["character_id"]) else actor["category"],"skin_key":actor["skin_key"],"combat":actor["combat"].duplicate(true),
		"cell":cell,"from_cell":cell,"facing":"S","path":[],"destination":Vector2i(-1,-1),"move_started_frame":-100000,
		"visual":"idle","visual_started_frame":frame,"target":-1,"dead_at":-1}
	_apply_record_fields(unit,actor)
	if scene_id in [4,6,9,10,13,14,18,20,21]:
		var record := String(actor["record_hex"]).hex_decode()
		unit["recovery"]=[record.decode_u16(24),record.decode_u16(30)]
		unit["recovery_clock"]=[0,0]
	if scene_id in [20,21]:unit["patrol"]=String(actor["record_hex"]).hex_decode()[0xa2]
	if actor.has("source_ai_request"):
		unit["source_ai_request"]=actor["source_ai_request"].duplicate()
		if scene_id==21:unit["patrol"]=unit["source_ai_request"][1]
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


func _guard_target(unit: Dictionary) -> int:
	if scene_id==21:return siege.guard_target(self,unit)
	return super._guard_target(unit)


func find_unit(identity: int) -> Dictionary:
	if siege!=null and siege.by_id.has(identity):return siege.by_id[identity]
	if identity<0:return {}
	return super.find_unit(identity)


func _update_captures() -> void:
	if scene_id==21:siege.refresh_positions(self)
	for object in units:
		if not _capture_role(object["character_id"]):continue
		if scene_id in [9,14,20,21] and (object.source_state!=1 or object.limits.hp<=0):continue
		if object["capture_elapsed"]>=0:
			object["capture_elapsed"]+=1
			if object["capture_elapsed"]>=Progression.capture_transition_ticks(object["character_id"]):
				object["side"]=object["capture_target"];object["capture_hold"]=Progression.capture_hold_limit(object["side"])
				object["capture_elapsed"]=-1;object["capture_target"]=-1
				if scene_id==21:siege.capture_candidates.clear()
			continue
		var candidate: int
		if scene_id==21 and siege.capture_candidates.has(object.instance_id):
			candidate=siege.capture_candidates[object.instance_id]
		else:
			var counts := [];counts.resize(16);counts.fill(0)
			for unit in units:
				if unit==object or unit["source_state"]!=1 or unit["side"]==7:continue
				var delta: Vector2i=(object["cell"]-unit["cell"]).abs()
				if delta.x<=5 and delta.y<=5 and _capture_mask[(delta.y+5)*11+delta.x+5]!=0:counts[unit["side"]]=(counts[unit["side"]]+1)%256
			candidate=Progression.capture_candidate(object["side"],counts)
			if scene_id==21:siege.capture_candidates[object.instance_id]=candidate
		if candidate==4 and object["side"]!=7:candidate=-1
		if candidate<0:object["capture_hold"]=mini(object["capture_hold"]+1,Progression.capture_hold_limit(object["side"]))
		else:
			object["capture_hold"]-=1
			if object["side"]==7 or object["capture_hold"]<=0:object["capture_target"]=candidate;object["capture_elapsed"]=0


func _activate(identity: int, center: Vector2i, radius: int) -> bool:
	var old := find_unit(identity)
	if scene_id in [4,9,10,14,20,21] and not old.is_empty() and old["source_state"] not in [0,2]:return false
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
		else:
			if scene_id in [4,9,10,14,20,21]:next["lives"]=old["lives"]
			old.clear();old.merge(next)
		for request in _pending_activations.duplicate():
			if request["identity"]==identity:_pending_activations.erase(request)
		if scene_id==21:
			siege.nearby.clear()
			siege.by_id[identity]=next if old.is_empty() else old
		source_actors[identity]=actor.duplicate(true);return true
	return false


func _spawn_group(group: int, center: Vector2i, radius: int, ai_parameter := -1) -> void:
	for id in reserves:
		var raw := String(reserves[id]["record_hex"]).hex_decode()
		if raw[0x98]==group and not _activate(id,center,radius):
			var old := find_unit(id)
			if scene_id in [14,21] and not old.is_empty() and old.source_state not in [0,2]:continue
			if (old.is_empty() or old["source_state"] in [0,2,3,4]) and not _pending_activations.any(func(r):return r["identity"]==id):
				_pending_activations.append({"identity":id,"center":center,"radius":radius})
	if ai_parameter>=0:_set_group_ai(group,ai_parameter)


func _set_group_ai(group: int, parameter: int) -> void:
	# Preserve source requests; pursuit cadence remains the declared local scheduler.
	var request := [0,0,parameter,1] if scene_id==9 else [0,parameter,1]
	for unit in units:
		if unit.get("group",0)==group:unit["source_ai_request"]=request.duplicate()
	for id in reserves:
		if String(reserves[id]["record_hex"]).hex_decode()[0x98]==group:reserves[id]["source_ai_request"]=request.duplicate()


func _update_summoning() -> void:
	# Elapsed source units advance by two at the explicitly local 30Hz scheduler.
	elapsed+=2
	if scene_id in [4,6,9,10,13,14,18,20,21]:
		_update_recovery()
		_update_field_spell(field_spell)
		if not healing_spell.is_empty():_update_field_spell(healing_spell)
		if not healing_impacts.is_empty():_apply_healing_impacts()
		if scene_id==6:return
		if scene_id==18:return
		if scene_id==21:
			siege.advance(self)
			return
		if scene_id==20:
			_advance_twenty()
			return
	if scene_id in [4,9,10,14,20,21]:
		if scene_id==14 and frame%12==0:dungeon.walk(self)
		if scene_id==10:escort_route.walk(self)
		if scene_id==9 and knight_released and frame%12==0:_advance_nine_patrol()
		for identity in ([1194] if scene_id==14 else [1214,1183] if scene_id==9 else [1214,1183,1178] if scene_id==10 else [1230,1223,1216,1209]):
			var caster := find_unit(identity)
			if not caster.is_empty() and caster["limits"]["hp"]>0:
				_update_summoner(caster,caster["group"],caster["lives"],reserves[identity]["summon_interval"])
		return
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
		if scene_id in [7,8,13]:_spawn_group(timer["group"],timer["center"],timer["radius"])
		elif timer.has("ai_parameter"):_set_group_ai(timer["group"],timer["ai_parameter"])
		else:_repeat_group();timers.append({"at":elapsed+int(rng.randi()%16200)+1800,"repeat":true})
		if scene_id==13:
			# 455EC0 stops the slot scan after a delivery. Later slots missed this decrement.
			for pending in timers:
				if pending["slot"]>timer["slot"]:pending["at"]+=2
		break # One timer delivery per local opportunity.
	if scene_id==17:
		for number in [45,46]:
			var unit := find_unit(1250-number)
			if unit.is_empty() or unit["source_state"]!=4 or ambushed.has(number):continue
			ambushed.append(number);var point: Array=spawn_points[rng.randi()%4]
			_spawn_group(number-31,Vector2i(point[0],point[1]),point[2],point[3])



func _update_recovery() -> void:
	for unit in units:
		if unit["limits"]["hp"]<=0:continue
		for i in 2:
			var quantity: String=["hp","mp"][i]
			var limits: Dictionary=unit["limits"]
			if limits[quantity]>=limits[quantity+"_max"]:
				unit["recovery_clock"][i]=0
				continue
			unit["recovery_clock"][i]+=2
			if unit["recovery_clock"][i]>=maxi(1,unit["recovery"][i]):
				unit["recovery_clock"][i]=0
				limits[quantity]+=1


func can_cast_spell(id: int, skill: int) -> bool:
	if not ready or scene_id not in [4,6,9,10,13,14,18,20,21] or _ending_phase!="active":return false
	if skill==31:
		if scene_id!=21 or not healing_spell.is_empty():return false
	elif skill not in [57,59] or not field_spell.is_empty():return false
	var unit := find_unit(id)
	var row := String(catalog["spells"]["rows"][str(skill)]).hex_decode()
	return unit.get("controllable",false) and unit["limits"]["hp"]>0 and unit["limits"]["mp"]>=row.decode_u16(8) and unit["input"]["equipped_skills"].has(skill)


func _advance_twenty() -> void:
	var mask := String(catalog.spells.masks["3"]).hex_decode()
	for u in units:
		if u.controllable or u.limits.hp<=0:continue
		if u.life_kind==2:
			_update_summoner(u,u.group,u.lives,reserves[u.instance_id].summon_interval)
		if u.patrol>0 and frame%12==0 and u.summon_phase=="":
			var goal: Array=catalog.patrol_goals[u.patrol-1]
			_walk_patrol(u,Vector2i(goal[0],goal[1]),mask)
		if u.character_id in [393,399] and not phases.has(u.instance_id) and u.side in [0,5]:
			var closest := {}
			var distance: int=u.combat.attack_range+1
			for target in units:
				if not _admitted(u,target):continue
				var delta := _distance(u,target)
				if delta<distance:
					closest=target
					distance=delta
			if not closest.is_empty():
				u.target=unit_key(closest)
				_start_attack(u,closest)


func _advance_nine_patrol() -> void:
	var mask := String(catalog.spells.masks["3"]).hex_decode()
	for unit in units:
		if unit.get("source_ai_request")==[0,0,2,1]:_walk_patrol(unit,NINE_PATROL_GOAL,mask)


func _walk_patrol(u: Dictionary, goal: Vector2i, mask: PackedByteArray) -> void:
	# 47F6B0 resets the waypoint cursor. 47ED90/47F090 follow the route
	# requested by record+A2; actors engaged by the local guard AI resume later.
	if u.get("patrol_finished",false) or u.limits.hp<=0 or u.combat.movement_rate<=0:return
	if phases.has(unit_key(u)) or not u.path.is_empty() or (u.target>=0 and _admitted(u,find_unit(u.target))):return
	var delta: Vector2i=(u.cell-goal).abs()
	if delta.x<=3 and delta.y<=3 and mask[(3+delta.y)*7+3+delta.x]!=0:
		u.patrol_finished=true
		return
	u.path=attack_paths.route(u.cell,goal,2,u.movement_type,_route_units(u))
	if not u.path.is_empty():u.destination=u.path.back()


func cast_field_spell(id: int, cell: Vector2i, skill: int) -> bool:
	if not can_cast_spell(id,skill) or not inside(cell):return false
	var unit := find_unit(id)
	var row := String(catalog["spells"]["rows"][str(skill)]).hex_decode()
	if absi(cell.x-unit["cell"].x)+absi(cell.y-unit["cell"].y)>row[18]:return false
	unit["path"]=[]
	unit["destination"]=Vector2i(-1,-1)
	unit["target"]=-1
	phases.erase(id)
	unit["limits"]["mp"]-=row.decode_u16(8)
	unit["summon_phase"]="field_spell"
	unit["visual"]="cast"
	unit["visual_started_frame"]=frame
	var cast := {"skill":skill,"caster":id,"cell":cell,"release":elapsed+row.decode_u16(10),"finish":elapsed+row.decode_u16(10)+row.decode_u16(14),"released":false}
	if skill==31:
		cast.target=at_cell(cell).get("instance_id",-1)
		healing_spell=cast
	else:field_spell=cast
	_record_command([9 if skill==31 else 7 if skill==59 else 8,id,cell.x,cell.y])
	return true


func _update_field_spell(cast: Dictionary = field_spell) -> void:
	if cast.is_empty():return
	var caster := find_unit(cast["caster"])
	if caster["limits"]["hp"]<=0 or elapsed>=cast["finish"]:
		caster["summon_phase"]=""
		cast.clear()
		return
	if cast["released"] or elapsed<cast["release"]:return
	cast["released"]=true
	caster["visual"]="attack"
	caster["visual_started_frame"]=frame
	var skill: int=cast["skill"]
	var row := String(catalog["spells"]["rows"][str(skill)]).hex_decode()
	var attr: Array=caster["input"]["attributes"]
	var radius := mini(32,row[22]+int(attr[6]*row[23]/100))
	var mask := String(catalog["spells"]["masks"][str(radius)]).hex_decode()
	if skill==31:
		# 4843A0 draws once for the cast, then adds a separate 0..5 per ally.
		var base := row.decode_s16(32)+int(attr[3]*row.decode_s16(34)/100)
		var spread := row.decode_s16(36)+int(attr[3]*row.decode_s16(38)/100)
		if spread>0:base+=int(rng.randi()%spread)
		for target in units:
			if target.side!=caster.side or target.source_state!=1 or target.limits.hp<=0:continue
			var delta: Vector2i=(target.cell-cast.cell).abs()
			if delta.x>radius or delta.y>radius or mask[(radius+delta.y)*(2*radius+1)+radius+delta.x]==0:continue
			var amount: int=base+int(rng.randi()%6)
			var delay:=20+int(rng.randi()%40)
			if target.instance_id==cast.target:delay=0
			# 4843A0 also draws two visual offsets. Effect 2034 sends its HP event at tick 19.
			rng.randi()
			rng.randi()
			healing_impacts.append({"id":target.instance_id,"amount":amount,"due":elapsed+delay+19})
		return
	var attack := _packet(caster)
	# 4864B0 uses record bytes +8/+5 (intellect/agility) and +A (spirit).
	attack["power"]=int(int((attr[4]+attr[1]+row.decode_s16(32))*attr[4]/100)*row.decode_s16(34)/100)
	attack["power_range"]=int(int((attr[4]+attr[1]+row.decode_s16(36))*attr[4]/100)*row.decode_s16(38)/100)
	var targets := _allied_targets() if skill==57 else enemies()
	if skill==59 and scene_id in [9,14,20,21]:
		# 486749 scans the active list, including hostile bases (46AE20/43C1D0).
		targets=units.filter(func(u):return u.side==5 and u.source_state==1 and u.limits.hp>0)
	for target in targets:
		var delta: Vector2i=(target["cell"]-cast["cell"]).abs()
		if delta.x>radius or delta.y>radius or mask[(radius+delta.y)*(2*radius+1)+radius+delta.x]==0:continue
		if skill==57:
			if target["limits"]["hp"]>0:
				target["barrier_until"]=elapsed+row.decode_u16(28)+int(attr[4]*row.decode_u16(30)/100)
			continue
		var hp: int=target["limits"]["hp"]
		var damage := Inputs.damage(attack,_packet(target),rng,true)
		target["limits"]["hp"]=maxi(0,hp-damage)
		if target["limits"]["hp"]==0:
			_record_defeat(caster,target)
			phases.erase(unit_key(target))
			target["path"]=[]
			target["target"]=-1
			target["dead_at"]=frame


func _apply_healing_impacts() -> void:
	for i in range(healing_impacts.size()-1,-1,-1):
		var impact: Dictionary=healing_impacts[i]
		if elapsed<impact.due:continue
		var target:=find_unit(impact.id)
		if not target.is_empty() and target.source_state==1 and target.limits.hp>0:
			target.limits.hp=mini(target.limits.hp_max,target.limits.hp+impact.amount)
		healing_impacts.remove_at(i)


func command_move(id: int, cell: Vector2i) -> bool:
	if field_spell.get("caster",-1)==id or healing_spell.get("caster",-1)==id:return false
	if scene_id in [9,14,20,21]:
		var object := at_cell(cell)
		if _hostile_base(object):return command_attack(id,unit_key(object))
	if _normal_healer(find_unit(id)):
		var ally := at_cell(cell)
		if _support_target(ally) and ally["limits"]["hp"]<ally["limits"]["hp_max"]:
			return command_attack(id,unit_key(ally))
	if scene_id in [20,21] and not at_cell(cell).is_empty():return false
	return super.command_move(id,cell)


func command_attack(id: int, target: int) -> bool:
	if field_spell.get("caster",-1)==id or healing_spell.get("caster",-1)==id:return false
	return super.command_attack(id,target)


func stop(id: int) -> bool:
	if field_spell.get("caster",-1)==id or healing_spell.get("caster",-1)==id:return false
	return super.stop(id)


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


func _check_before_actions() -> bool:
	# 4539B0 samples the six prayer regions after movement and combat.
	if scene_id in [9,13,14,18,20,21]:return false
	return super._check_before_actions()


func _detect_trial_end() -> bool:
	var sub := -1
	var unavailable := controlled_units().filter(func(u):return u["character_id"]<=45).all(func(u):return u["limits"]["hp"]<=0)
	if scene_id==4:
		# 433720 gives extermination priority over timeout and loss of the party.
		if not units.any(func(u):return u["category"]==5 and u["side"]==5 and u["source_state"] in [1,3]):
			sub=(2 if _own_casualties==0 else 5) if elapsed<=25200 else 8
		elif remaining_ticks==0:sub=11
		elif unavailable:sub=14
	elif scene_id==21:
		sub=siege.result(self)
	elif scene_id==20:
		# 430DF0 -> 46A4C0 / 4695D0 counts own students in states 0,2..5.
		unavailable=controlled_units().filter(func(u):return u.side==0).all(func(u):return u.source_state in [0,2,3,4,5])
		# 435080: template 6 must have completed removal (469170).
		if _source_status(1244).state==4:
			var intact := true
			for number in catalog.grade_objects:
				var objective := _source_status(1250-number)
				if not objective.used or objective.side!=0 or objective.state in [2,3,4]:intact=false
			sub=(2 if _own_casualties==0 else 5) if intact else 8
		elif unavailable:sub=14 if elapsed<36000 else 11
	elif scene_id==14:
		sub=dungeon.result(self,unavailable)
		if sub<0:dungeon.advance(self)
	elif scene_id==9:
		var first := find_unit(1205)
		var second := find_unit(1204)
		var both_owned: bool=first.side==0 and second.side==0
		var destroyed: bool=first.source_state in [2,3,4] or second.source_state in [2,3,4]
		if not knight_released:
			if both_owned and not destroyed:
				knight_released=true
				for row in [[9,52,85],[10,2,3],[11,3,91]]:_spawn_group(row[0],Vector2i(row[1],row[2]),5)
				for group in [1,2]:_set_group_ai(group,2)
				_event_pages=_pages(20)
				_event_index=0
				_ending_phase="event20"
				_accumulator=0.0
				return true
			if not both_owned and destroyed:sub=12
		if sub<0:
			if _source_status(1203).state==4:
				var all_owned := [1207,1206,1205,1204].all(func(id):var u:=find_unit(id);return u.side in [0,4] and u.source_state not in [2,3,4])
				sub=(2 if _own_casualties==0 else 5) if all_owned else 8
			elif unavailable:sub=14
			elif remaining_ticks==0:sub=11
	elif scene_id==18:
		sub=castle.result(self,unavailable)
		if sub<0:castle.advance(self)
	elif scene_id==13:
		if prayer.check_event(self):return true
		if prayer.held(self):
			var defeated: bool=[1249,1248,1247].all(func(id):return _source_status(id)["state"] in [2,3,4])
			sub=(2 if _own_casualties==0 else 5) if defeated else 8
		elif remaining_ticks==0:sub=11
		elif unavailable:sub=14
	elif scene_id==10:
		if unavailable:sub=11
		elif find_unit(TenEscort.ELDER)["source_state"]==4:sub=14
		else:
			if escort_route.check_event(self):return true
			if escort_route.arrived:
				var owned: bool=catalog["grade_objects"].all(func(n):return find_unit(1250-n)["side"]==0)
				sub=(2 if _own_casualties==0 else 5) if owned else 8
	elif scene_id==6:
		# 433970 tests permanent removal of template 5 before the all-down branch.
		if find_unit(1245)["source_state"]==4:
			var owned: bool=catalog["grade_objects"].all(func(n):return find_unit(1250-n)["side"]==0)
			var clear := not units.any(func(u):return u["category"]==5 and u["side"]==5 and u["source_state"] in [1,3])
			sub=(2 if _own_casualties==0 else 5) if owned and clear else 8
		elif unavailable:sub=11
	elif scene_id==7:
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
	_terminal_choice={"tactical_result_selector":1 if sub==2 else 2 if sub==5 else 3 if sub==8 else 4 if sub in [11,12] else 5,"script_sub":sub}
	_begin_ending("mission_objectives_met" if scene_id in [4,6,9,10,13,14,18,20,21] and sub in [2,5,8] else "time_expired" if scene_id in [4,9,13] and sub==11 else "objective_destroyed" if scene_id==9 and sub==12 else "objective_destroyed" if scene_id==18 and sub==11 else "squad_defeated" if unavailable else "bases_lost" if sub==15 else "training_ended" if scene_id==17 else "escort_lost" if sub==14 else "mission_objectives_met" if scene_id==7 else "defense_completed")
	return true


func _on_region(unit: Dictionary, region: String) -> bool:
	return unit["source_state"]==1 and unit["limits"]["hp"]>0 and catalog["regions"][region].has(unit["cell"].y*field_width+unit["cell"].x)


func advance_event() -> bool:
	if scene_id not in [7,9,10,13] or _ending_phase!="event20":return false
	_record_command([2])
	_event_index+=1
	if _event_index==_event_pages.size():
		if scene_id==9:
			_ending_phase="active"
			reason="knight_released"
			return true
		if scene_id==13:
			prayer.finish_event(self)
			return true
		if scene_id==10:
			escort_route.finish_event(self)
			return true
		for identity in [1248,1247]:
			var ally := find_unit(identity)
			ally["side"]=0
			ally["controllable"]=true
		rendezvous=true
		_ending_phase="active"
		reason="escort_ready"
	return true


func _normal_healer(unit: Dictionary) -> bool:
	if scene_id in [9,14,18,20,21]:return unit.get("normal_heal",false)
	return scene_id in [4,6,10,13] and unit.get("character_id")==8


func _support_target(unit: Dictionary) -> bool:
	return unit.get("controllable",false) or (scene_id==10 and unit.get("instance_id")==TenEscort.ELDER)


func _allied_targets() -> Array:
	var targets:=controlled_units()
	if scene_id==20:
		for id in [1246,1245]:
			var gate := find_unit(id)
			if gate.side==0 and gate.source_state==1:targets.append(gate)
	if scene_id==10:targets.append(find_unit(TenEscort.ELDER))
	return targets


func _hostile_base(target: Dictionary) -> bool:
	return target.get("side",-1)==5 and target.character_id>=387 and target.character_id<=404


func _admitted(unit: Dictionary, target: Dictionary) -> bool:
	if scene_id in [20,21] and not unit.is_empty() and not target.is_empty():
		if unit.character_id in [388,393,394,399]:
			if _ending_phase!="active" or unit.source_state!=1 or target.source_state!=1 or unit.limits.hp<=0 or target.limits.hp<=0:return false
			if unit.character_id in [393,394]:return target.side==unit.side and target.limits.hp*100<91*target.limits.hp_max
			return target.side in [0,5] and target.side!=unit.side and (target.controllable or target.category==5 or target.character_id==412)
		if unit.side==5 and unit.category==5 and target.character_id==412:
			return _ending_phase=="active" and unit.limits.hp>0 and target.limits.hp>0 and target.side==0 and _distance(unit,target)<=unit.combat.attack_range+2
	if unit.get("character_id",-1) in range(411,415) and (scene_id in [14,20,21] or departure.get("date") in [[7,5],[8,4]]):
		return false # These gates use attack 511 with no target or effect.
	# Manual target packet 48DAB7/48DBBD/48DBD5 excludes chests via 46A050.
	# The distinct automatic search at 47A9D0 requires the AI base flag.
	if scene_id in [9,14,20,21] and unit.get("controllable",false) and _hostile_base(target):
		return _ending_phase=="active" and unit.limits.hp>0 and target.limits.hp>0 and target.source_state==1
	if _ending_phase=="active" and _normal_healer(unit) and _support_target(target):
		return unit["limits"]["hp"]>0 and target["limits"]["hp"]>0 and target["limits"]["hp"]<target["limits"]["hp_max"]
	if scene_id==10 and unit.get("category")==5 and target.get("instance_id")==TenEscort.ELDER:
		return _ending_phase=="active" and unit.limits.hp>0 and target.limits.hp>0 and _distance(unit,target)<=unit.combat.attack_range+2
	if not super._admitted(unit,target):return false
	if scene_id in [4,6,7,9,10,13,14,18,20,21] and unit["category"]==5:
		# Local guards engage nearby targets, respecting their original reach.
		return _distance(unit,target)<=unit["combat"]["attack_range"]+2
	return true


func _packet(unit: Dictionary) -> Dictionary:
	var result := super._packet(unit)
	if scene_id in [4,6,9,10,13,14,18,20,21] and unit.get("barrier_until",0)>elapsed:
		var row := String(catalog["spells"]["rows"]["57"]).hex_decode()
		var intelligence: int=unit["input"]["attributes"][4] if unit["controllable"] else String(reserves[unit_key(unit)]["record_hex"]).hex_decode()[8]
		# 4DF6F0 applies effect 50 to armor, body and evasion.
		result["armor"]=clampi(result["armor"]+row.decode_s16(32)+int(intelligence*row.decode_s16(34)/100),0,255)
		result["body"]=clampi(result["body"]+row.decode_s16(36)+int(intelligence*row.decode_s16(38)/100),0,100)
		result["evasion"]=clampi(result["evasion"]+row.decode_s16(40)+int(intelligence*row.decode_s16(42)/100),0,255)
	return result


func _hit(unit: Dictionary, target: Dictionary) -> void:
	if (_normal_healer(unit) and _support_target(target)) or (scene_id in [20,21] and unit.character_id in [393,394] and unit.side==target.side):
		if not _admitted(unit,target) or _distance(unit,target)>unit["combat"]["attack_range"]:return
		# 48AAE0 category 5 allied branch -> 48B1B0 -> 482810 (positive HP).
		var amount: int=unit["combat"]["power"]
		var spread: int=unit["combat"]["power_range"]
		if spread>0:amount+=rng.randi()%spread
		target["limits"]["hp"]=mini(target["limits"]["hp"]+amount,target["limits"]["hp_max"])
		return
	super._hit(unit,target)


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
		if (scene_id in [14,20,21] or departure.date in [[7,5],[8,4]]) and unit.character_id in range(411,415):continue
		if unit["category"]==5 and unit["side"]!=0 and unit["source_state"] in [1,3]:
			no_hostile=false
			break
	if no_hostile:
		for identity in reserves:
			var raw := String(reserves[identity]["record_hex"]).hex_decode()
			if raw[0x96]!=3 and _source_status(identity)["state"]==0:
				no_hostile=false
				break
	if scene_id==18:no_hostile=castle.cleared(self)
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
	super.close();siege=null;weapon_masks.clear();weapon_distances.clear();dungeon=null;knight_released=false;castle=null;prayer=null;escort_route=null;field_spell.clear();healing_spell.clear();healing_impacts.clear();recurring_events.clear();rendezvous=false;attack_paths=null;scene_id=0;elapsed=0;departure.clear();scene_scripts.clear();timers.clear();ambushed.clear();spawn_points.clear();ending_sub=-1
