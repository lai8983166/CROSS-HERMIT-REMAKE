extends RefCounted
## Verified current-school limits only; does not construct a combat record/world.
const Origin := preload("res://sim/new_game_school_origin.gd")
const SOURCE_SHA := "588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005"
const RULE_PATH := "res://data/school_combat_records_rules.json"
const JOB_HASHES := ["bb97b79e346d7c148a940f95bc3e6d5c4a2a39e589e893213bb3db85bd6bad78",
	"065758a562bc385bbc0e69f5ba966fade382b54611a5632ae4087eeffadbd43b",
	"6bae1f35dc4ed2adc6a0982a32bef086c99b4bfed5ea9e9cf216b8053a136231"]
const SKILL_HASHES := ["83dc7f73f14f6801e2a29585ebf41d3602934b41042a70f27ad12e6911085707",
	"32c29bfed5e0c84d4db6212e774e16583ec19521aee567fb2de55f423df79fdd",
	"dbe6ccc909d1e7cbc9b58873850acc44fe8bee1935b5bfe4d5e25cca3c86fd02",
	"c45a562d51687914ca9116a1886c86f7d9881c3c868be77d239efcb82f625ac8",
	"e266ba7b50940b02c9b2293196bbadb1e259ae067a4323ae7b4a355b7b17702a"]
const MINUTES := [0,5940,5940,5940,5940,5940,5760,5580,5400,5220,5040,4860,4680,4500,4320,
	4140,3960,3780,3600,3420,3240,3120,3000,2880,2760,2640,2520,2400,2280,2160,2040,1920,
	1800,1680,1560,1440,1380,1320,1260,1200,1140,1080,1020,960,900,840,780,720,660,600,540]


static func project(input: Dictionary, rules: Dictionary) -> Dictionary:
	rules = _source_numbers(rules)
	if not _rules_valid(rules):
		return Origin.failure("invalid_current_combat_source")
	if not _integer(input.get("character_id"),3,9) or input["character_id"] not in [3,4,9] \
			or not _integer(input.get("job"),0,1023) or input["job"] not in [6,7,10] \
			or not _integer(input.get("level"),0,255) \
			or not _numbers(input.get("attributes"),7,0,255) \
			or not _numbers(input.get("equipped_items"),8,0,0) \
			or not _numbers(input.get("equipped_skills"),8,0,65535):
		return Origin.failure("outside_current_combat_subset")
	for skill in input["equipped_skills"]:
		if skill not in rules["supported_skills"]:
			return Origin.failure("unsupported_current_combat_skill")
	var attributes: Array = input["attributes"].map(func(a): return clampi(int(a),1,135))
	var job: Dictionary = rules["jobs"][[6,7,10].find(input["job"])]
	var level := clampi(int(input["level"]),0,99)
	# Verified skills have null callbacks. 4DCF00 accumulates their MP cost at
	# modifier word12; the limits below do not read that slot. Item slots are zero.
	var hp := clampi(_signed16(int((attributes[5]*3+attributes[0]+attributes[1])*job["hp_coefficient"]/100.0)),1,999)
	var mp := clampi(_signed16(int((attributes[6]*3+attributes[4]+attributes[3])*job["mp_coefficient"]/100.0)),1,999)
	var hp_recovery := clampi(_signed16(int(job["hp_recovery_base"]-attributes[5]-attributes[0]*rules["half_coefficient"])),30,999)
	var mp_recovery := clampi(_signed16(int(job["mp_recovery_base"]-attributes[6]-attributes[3]*rules["half_coefficient"])),30,999)
	var engage := clampi(int(rules["engagement_minutes"][clampi(level,0,50)])*60,1,0x57030)
	return {"supported":true,"projection_only":true,"full_combat_record":false,
		"battle_world_constructed":false,"battle_executed":false,"mandatory_gate_cleared":false,
		"live_witness":false,"authorizes_persistent_write":false,"limits":{
			"character_id":int(input["character_id"]),"attributes":attributes,"job":int(input["job"]),"level":level,
			"hp_max":hp,"hp":hp,"hp_recovery":hp_recovery,"mp_max":mp,"mp":mp,"mp_recovery":mp_recovery,
			"engage_initial":engage,"engage_left":engage}}


static func _signed16(value: int) -> int:
	return ((value+32768)&65535)-32768


static func _integer(value: Variant, low: int, high: int) -> bool:
	return (value is int or value is float) and is_finite(float(value)) \
		and value == int(value) and value >= low and value <= high


static func _numbers(value: Variant, count: int, low: int, high: int) -> bool:
	if not value is Array or value.size() != count:
		return false
	for number in value:
		if not _integer(number,low,high):
			return false
	return true


static func _record(raw: Variant, length: int, expected: String) -> PackedByteArray:
	if not raw is String or raw.length() != length*2:
		return PackedByteArray()
	for character in raw:
		if character not in "0123456789abcdef":
			return PackedByteArray()
	var bytes := PackedByteArray()
	for i in range(length):
		bytes.append(raw.substr(i*2,2).hex_to_int())
	var context := HashingContext.new()
	context.start(HashingContext.HASH_SHA256)
	context.update(bytes)
	return bytes if context.finish().hex_encode() == expected else PackedByteArray()


static func _rules_valid(rules: Dictionary) -> bool:
	rules = _source_numbers(rules)
	if rules.get("schema_version") != 1 or rules.get("source_image_sha256") != SOURCE_SHA \
			or rules.get("supported_jobs") != [6,7,10] or rules.get("supported_skills") != [0,20,29,31,57,59] \
			or rules.get("items") != "zero_slots_only" or rules.get("half_coefficient") != 0.5 \
			or rules.get("engagement_minutes") != MINUTES \
			or rules.get("functions") != ["0x4b9340","0x4b93c0","0x4db340","0x4dcf00","0x56cfcc"] \
			or rules.get("work_reset") != {"function":"0x4dab10","target":"0x8093f8","size":666}:
		return false
	for flag in ["school_initialized","interactive_school_ready","live_witness","authorizes_persistent_write"]:
		if not rules.get(flag) is bool or rules[flag]:
			return false
	if not rules.get("jobs") is Array or rules["jobs"].size() != 3 \
			or not rules.get("skills") is Array or rules["skills"].size() != 5:
		return false
	for i in range(3):
		var entry: Variant = rules["jobs"][i]
		if not entry is Dictionary or not _integer(entry.get("job_id"),0,1023) \
				or entry["job_id"] != [6,7,10][i] or entry.get("record_sha256") != JOB_HASHES[i]:
			return false
		var bytes := _record(entry.get("record_hex"),64,JOB_HASHES[i])
		if bytes.is_empty():
			return false
		for pair in [["hp_coefficient",6],["hp_recovery_base",8],["mp_coefficient",10],["mp_recovery_base",12]]:
			if not _integer(entry.get(pair[0]),0,65535) or entry[pair[0]] != bytes.decode_u16(pair[1]):
				return false
	for i in range(5):
		var entry: Variant = rules["skills"][i]
		if not entry is Dictionary or not _integer(entry.get("skill_id"),0,65535) \
				or entry["skill_id"] != [20,29,31,57,59][i] or entry.get("record_sha256") != SKILL_HASHES[i] \
				or not _integer(entry.get("modifier_callback"),0,0) \
				or _record(entry.get("record_hex"),72,SKILL_HASHES[i]).is_empty():
			return false
	return true


static func _source_numbers(value: Variant) -> Variant:
	# JSON has floating numbers. Preserve genuine fractions (including 0.5),
	# so corrupt coefficients cannot become valid by truncation.
	if value is float and is_finite(value) and value == int(value):
		return int(value)
	if value is Array:
		return value.map(func(entry): return _source_numbers(entry))
	if value is Dictionary:
		var result := {}
		for key in value:
			result[key] = _source_numbers(value[key])
		return result
	return value
