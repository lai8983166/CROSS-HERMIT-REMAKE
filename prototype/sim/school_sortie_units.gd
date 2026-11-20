extends RefCounted
## Current returned-school members and their source-backed attack packets.
const Limits := preload("res://sim/school_combat_limits.gd")


static func project(participant: Dictionary, growth: Dictionary, rules: Dictionary) -> Dictionary:
	var id = participant.get("character_id")
	var jobs := {1:6,2:4,3:10,4:6,9:7,5:4,8:8,6:2}
	if id not in jobs or growth.get("character_id")!=id or participant.get("job")!=jobs[id] or growth.get("job")!=jobs[id]: return {}
	if participant.get("attributes")!=growth.get("attributes") or participant.get("level_50")!=growth.get("level_50"):return {}
	if not Limits._numbers(growth.get("attributes"),7,0,255) or not Limits._integer(growth.get("level_50"),0,99):return {}
	var bow: bool=id==1 and participant.get("equipped_items")==[189,0,0,0,0,0,0,0]
	var item := String(rules.get("bow189_hex","")).hex_decode()
	if bow and item.size()!=56:return {}
	if (not bow and participant.get("equipped_items")!=[0,0,0,0,0,0,0,0]) or not Limits._numbers(participant.get("equipped_skills"),8,0,65535):return {}
	for skill in participant["equipped_skills"]:
		if id not in [6,8] and skill not in [0,11,20,29,31,57,59]:return {}
		if id in [6,8] and skill!=0:return {}
	var job: Dictionary=rules["jobs"][str(jobs[id])]
	var j := String(job["job_hex"]).hex_decode();var w := String(job["attack_hex"]).hex_decode()
	var attrs: Array=growth["attributes"].map(func(v):return clampi(v,1,135))
	var a: int=attrs[0];var b: int=attrs[1];var sense: int=attrs[2];var vital: int=attrs[3]
	var intellect: int=attrs[4];var body: int=attrs[5];var spirit: int=attrs[6]
	var hp := clampi(Limits._signed16(int((body*3+a+b)*j.decode_u16(6)/100.0)),1,999)
	var mp := clampi(Limits._signed16(int((spirit*3+intellect+vital)*j.decode_u16(10)/100.0)),1,999)
	var family: int=job["family"]
	var stat: int=a if family==0 else b if family==1 else sense if family==2 else vital if family==3 else intellect
	var reach := int(w[18]) if family in [0,1] else int(w[18]+stat*(0.08 if family==2 else 0.1))
	var accuracy := int(w[20]+a*0.5) if family==0 else int(w[20]+b) if family==1 else int(w[20]+sense*0.2) if family==2 else 999
	var variation := clampi(int(w.decode_s16(36)*stat/100),0,999)
	return {"character_id":id,"job":jobs[id],"movement_type":0,
		"limits":{"hp":hp,"hp_max":hp,"mp":mp,"mp_max":mp},
		"input":{"character_id":id,"job":jobs[id],"attributes":growth["attributes"].duplicate(),"level":growth["level_50"],
			"equipped_items":participant["equipped_items"].duplicate(),"equipped_skills":participant["equipped_skills"].duplicate()},
		"combat":{"character_id":id,"job":jobs[id],"attack_id":job["archetype"],"attack_class":w[5],"target_filter":w[25],
			"attack_rate":clampi(int(j[18]+sense*0.1)+(item.decode_s16(24) if bow else 0),0,32),"movement_rate":clampi(j.decode_s16(20)+int((j.decode_u16(20)>>1)*b/100)+(item.decode_s16(26) if bow else 0),0,999),
			"movement_type":0,"cast_ticks":w.decode_u16(14),"attack_range":clampi(reach,0,127),"accuracy":clampi(accuracy+(item.decode_s16(34) if bow else 0),0,999),
			"power":clampi(int(w.decode_s16(32)*stat/100)+(variation>>1),0,999),"power_range":variation,
			"evasion":clampi(int(j[26]*b/100+b*0.25),0,255),"armor":clampi(int(j[27]*a/100+a*0.15),0,255),
			"body":clampi(int(j[28]+body*0.1+sense*0.05),0,99),"magic_body":clampi(int(j[29]+intellect*0.15),0,255),
			"magic_resist":clampi(int(j[30]+spirit*0.05+vital*0.1),0,99),"mental":clampi(int(hp*0.1),0,999)}}
