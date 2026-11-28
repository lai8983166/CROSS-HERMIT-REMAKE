extends "res://sim/school_twenty_four_battle.gd"
## 432100 dispatches these missions to 435850, 4360B0, 4355A0 and 4361A0.
const DATES := {32:[12,3],44:[13,2],29:[13,3],45:[15,4]}
const MAP_SIZE := {32:Vector2i(64,192),44:Vector2i(96,144),29:Vector2i(64,192),45:Vector2i(128,192)}
const TEMPLATES := {32:96,44:119,29:102,45:102}
const OBJECTS := {32:[3,4,5,6],44:[2,3,96],29:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],45:[3,4,5,6,7,8,44,45]}
const Roles := preload("res://sim/all_result_role_replay.gd")
const ATTACK_TIMING_SHA := "b8c1e2d33090ebe35257da5c86cb733c82480be8ac3d27657109c82bc8e937ba"
const RULE_SHA := "827671c44a784142669317400f680f7f1bc929f4c6f1f7dda261d29126461ce5"


static func mission_rules(id:int) -> Dictionary:
	var raw:=FileAccess.get_file_as_string("res://data/school_mandatory_winter.json").replace(String.chr(13),"")
	return Roles._integers(JSON.parse_string(raw)).get(str(id),{}) if raw.sha256_text()==RULE_SHA else {}


var second_king := false


func start(s) -> void:
	patrol_mask=String(s.catalog.spells.masks["3"]).hex_decode()
	for script in s.scene_scripts:
		if script.block!=0:continue
		if script.sub==1:
			for cmd in script.commands:
				if cmd.opcode==124:
					var v:Array=cmd.values
					slots[v[0]]={"sub":v[2],"due":v[3]}
		if script.sub not in [20,21,22]:continue
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
		if wave.centers.size()==1:
			wave.center=wave.centers[0]
			wave.erase("centers")
		waves[script.sub]=wave


func result(s) -> int:
	var owned:=0
	var fallen:=0
	for ordinal in OBJECTS[s.scene_id]:
		var status:Dictionary=s._source_status(1250-ordinal)
		if status.side==0:owned+=1
		if status.state in [2,3,4]:fallen+=1
	var grade:=2 if s._own_casualties==0 else 5
	var unavailable:bool=s.controlled_units().all(func(u):return u.source_state in [0,2,3,4,5])
	match s.scene_id:
		32:
			if owned==0:return 11
			if s.remaining_ticks==0:return grade if owned==4 else 8
		44:
			if s._source_status(1249).state==4:return grade if owned==3 else 8
			if s.remaining_ticks==0:return 11
		29:
			if fallen>0:return 14
			if owned==15:
				for ordinal in range(19,30):
					if s._source_status(1250-ordinal).state in [2,3,4]:
						return 11 if s._source_status(1231).state in [2,3,4] else 8
				return grade
		45:
			if not second_king and s._source_status(1249).state==4:
				second_king=true
				s._activate(1248,Vector2i(12,27),0)
			elif second_king and s._source_status(1248).state==4:return grade if owned==8 else 8
			if unavailable:return 11 if second_king else 14
	return 14 if unavailable else -1


func _patrol(s,u: Dictionary) -> void:
	var route:Array=s.catalog.patrol_routes.get(str(u.patrol),[])
	if route.is_empty():return
	var index:int=u.get("patrol_index",0)
	var row:Array=route[index]
	if row==[0,0,0,0]:return
	var resume:int=u.get("patrol_resume",-1)
	if resume>=0 and s.elapsed<resume:return
	if resume<0:
		s._walk_patrol(u,Vector2i(row[0],row[1]),patrol_mask)
		if not u.get("patrol_finished",false):return
		if row[2]>0:
			u.patrol_resume=s.elapsed+row[2]
			return
	u.patrol_resume=-1
	u.patrol_finished=false
	if row[3]!=0:
		u.patrol=row[3]
		u.patrol_index=0
	else:u.patrol_index=(index+1)%route.size()
