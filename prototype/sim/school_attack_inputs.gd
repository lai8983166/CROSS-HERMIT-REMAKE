extends RefCounted
## Source-projected no-item combat fields and verified original scalar formulas.
const Limits := preload("res://sim/school_combat_limits.gd")
const RULE_PATH := "res://data/school_attack_inputs_rules.json"
const RULE_SHA := "fb5b0d4d4f39216c930c382760b6558303e57935911ead574d090c0938f77fef"


static func load_rules() -> Dictionary:
	var raw := FileAccess.get_file_as_string(RULE_PATH)
	if raw.replace("\r\n","\n").sha256_text() != RULE_SHA: return {}
	return Limits._source_numbers(JSON.parse_string(raw))


static func project(input: Dictionary, rules: Dictionary) -> Dictionary:
	var allowed := {3:10,4:6,9:7}
	var identity = input.get("character_id")
	if rules.is_empty() or identity not in allowed or input.get("job") != allowed[identity]: return {"supported":false}
	var valid := Limits.project(input,JSON.parse_string(FileAccess.get_file_as_string(Limits.RULE_PATH)))
	if not valid["supported"]: return {"supported":false}
	var job: Dictionary = rules["jobs"][str(input["job"])]
	var j: PackedByteArray = String(job["job_hex"]).hex_decode()
	var w: PackedByteArray = String(job["attack_hex"]).hex_decode()
	var c: Dictionary = rules["coefficients"]
	var attributes: Array = valid["limits"]["attributes"]
	var a: int = attributes[0]; var b: int = attributes[1]; var sense: int = attributes[2]
	var vital: int = attributes[3]; var intellect: int = attributes[4]
	var body: int = attributes[5]; var spirit: int = attributes[6]
	var stat: int = sense if job["family"] == 2 else vital if job["family"] == 3 else intellect
	if job["family"] not in [2,3,4] or (job["family"] == 2 and job["weapon_type"] != 2): return {"supported":false}
	var attack_range := clampi(int(w[18]+stat*c["eight_hundredths" if job["family"] == 2 else "tenth"]),0,127)
	var accuracy := clampi(int(w[20]+sense*c["fifth"]),0,999) if job["family"] == 2 else 999
	var variation := clampi(int(w.decode_s16(36)*stat/100),0,999)
	return {"supported":true,"fields":{"character_id":identity,"job":input["job"],"attack_id":job["archetype"],
		"attack_class":w[5],"target_filter":w[25],"attack_rate":clampi(int(j[18]+sense*c["tenth"]),0,32),
		"movement_rate":clampi(j.decode_s16(20)+int((j.decode_u16(20)>>1)*b/100),0,999),
		"movement_type":0,"cast_ticks":w.decode_u16(14),"attack_range":attack_range,"accuracy":accuracy,
		"power":clampi(int(w.decode_s16(32)*stat/100)+(variation>>1),0,999),"power_range":variation,
		"evasion":clampi(int(j[26]*b/100+b*c["quarter"]),0,255),
		"armor":clampi(int(j[27]*a/100+a*c["fifteen_hundredths"]),0,255),
		"body":clampi(int(j[28]+body*c["tenth"]+sense*c["twentieth"]),0,99),
		"magic_body":clampi(int(j[29]+intellect*c["fifteen_hundredths"]),0,255),
		"magic_resist":clampi(int(j[30]+spirit*c["twentieth"]+vital*c["tenth"]),0,99),
		"mental":clampi(int(valid["limits"]["hp_max"]*c["tenth"]),0,999)}}


static func snapshot(fields: Dictionary, terrain: int, mode: int, rules: Dictionary) -> Dictionary:
	if rules.is_empty() or terrain < 0 or terrain >= rules["terrain_modifiers"].size() or mode < 0 or mode > 4: return {}
	var modifiers: Array = rules["terrain_modifiers"][terrain][mode]
	var result := fields.duplicate(true)
	result.merge({"evasion_coefficient":modifiers[0],"armor_coefficient":modifiers[1],
		"body_coefficient":modifiers[2],"magic_modifier":0})
	return result


static func damage(attack: Dictionary, defense: Dictionary, rng, magic: bool) -> int:
	if magic:
		var power: int = attack["power"]
		if attack["power_range"]: power += rng.randi()%attack["power_range"]
		return maxi(int(power*(100-defense["magic_resist"]+defense["magic_modifier"])/100)
			-int(defense["magic_body"]*defense["body_coefficient"]/100),1)
	var roll: int = rng.randi()%100
	var residual: int = attack["accuracy"]-int(defense["evasion"]*defense["evasion_coefficient"]/100)-roll
	var multiplier := 100
	if defense["evasion"] == 0 or roll <= 4 or residual >= 150:
		if defense["evasion"] != 0 and roll > 94: return -1
		multiplier = maxi(residual,150)
	elif roll > 94 or residual < 0: return -1
	var power: int = attack["power"]
	if attack["power_range"]: power += rng.randi()%attack["power_range"]
	var damage: int = int(power*multiplier/100)-int(defense["armor"]*defense["armor_coefficient"]/100)
	return maxi(damage,0) if multiplier == 100 else (1 if damage < 0 else damage)
