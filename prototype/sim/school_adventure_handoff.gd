extends RefCounted
## Pure current-school commit/first-round projection; no saved departure or battle.
const Preparation := preload("res://sim/school_adventure_preparation.gd")
const Origin := preload("res://sim/new_game_school_origin.gd")
const RULE_PATH := "res://data/school_adventure_handoff_rules.json"
const CONFIG_HEX := "050000000001140910000000000000051e050a0f01010111111121000000000000000000000000000000"
const CONFIG_SHA := "7c9911a5194a68f4a1019c8c9849d58509cd1a5fbcd7d5aa8a899ba31ff218d0"


static func initial_ledger(template: Dictionary) -> Dictionary:
	var expected := {"id":5,"enabled":1,"month":4,"week":5,"metadata":0,"limit":1,"kind":4,
		"ordinal":5,"condition":1,"record_sha256":Preparation.RECORD_SHA}
	if template != expected:
		return Origin.failure("unsupported_handoff_ledger_origin")
	return {"supported":true,"ledger":{"entries":[{"id":template["id"],
		"metadata":[template["kind"]-1,template["ordinal"]-1,0],"busy":0,
		"limit":template["limit"],"duration":template["metadata"],"busy_elapsed":0,"elapsed":0}]}}


static func project(school: Dictionary, ledger: Dictionary, rules: Dictionary) -> Dictionary:
	if not _rules_valid(rules):
		return Origin.failure("unsupported_adventure_handoff_rules")
	# Only this actual fifth-school ledger is verified. Do not generalize timers,
	# additional offers, already-committed ledgers or replay this pure output.
	var expected := {"entries":[{"id":5,"metadata":[3,4,0],"busy":0,"limit":1,
		"duration":0,"busy_elapsed":0,"elapsed":0}]}
	if ledger != expected:
		return Origin.failure("outside_current_fifth_adventure_ledger")
	var departure := Preparation.project(school,rules["departure"])
	if not departure["supported"]:
		return departure
	var output := {"supported":true,"projection_only":true,"ready":departure["ready"],
		"reason":departure["reason"],"prepared":departure["prepared"],
		"ledger_after":ledger.duplicate(true),"requested_states":[],
		"round_after":null,"configuration":null,"combat_units_ready":false,
		"resources_resolved":false,"battle_executed":false,"mandatory_gate_cleared":false,
		"live_witness":false,"authorizes_persistent_write":false}
	if not departure["ready"]:
		return output
	var round: Dictionary = departure["prepared"]["rounds"][0]
	if round["teacher_ids"] != [101] or round["student_ids"].is_empty():
		return Origin.failure("outside_current_fifth_squad")
	for id in round["student_ids"]:
		if id not in [3,4,9]:
			return Origin.failure("outside_current_fifth_squad")
	# 4A1920 removes selected duration0 task5 before updating remaining timers.
	output["ledger_after"] = {"entries":[]}
	var roster: Array = round["student_ids"].duplicate()
	roster.resize(100)
	for i in range(round["student_ids"].size(),100):
		roster[i] = -1
	output["requested_states"] = [10,16]
	output["round_after"] = {"current":1,"total":1,"temp_roster":roster,
		"temp_count":round["student_ids"].size(),"combat_count":round["student_ids"].size(),"scene_id":5}
	output["configuration"] = _configuration(rules["configuration_record_hex"],round["student_ids"].size())
	return output


static func _configuration(record: String, count: int) -> Dictionary:
	var raw := []
	for i in range(42):
		raw.append(record.substr(i*2,2).hex_to_int())
	var times := []
	for i in range(16,20):
		times.append(0x7fffffff if i == 16 and raw[i] == 255 else raw[i]*3600)
	return {"scene_id":raw[0]+256*raw[1],"field_448a":raw[2]+256*raw[3],
		"flags_448c_4491":[0,count,0,raw[4],0,0],
		"fields_4492_44a0":raw.slice(7,15),"fields_44a2_44a4":[raw[15],raw[5],raw[6]],
		"time_limits":times,"flags_44b8_44bd":raw.slice(20,26),"objective_slots":raw.slice(26,42)}


static func _rules_valid(rules: Dictionary) -> bool:
	return rules.get("schema_version") == 1 and rules.get("source_image_sha256") == Preparation.Groups.SOURCE_SHA \
		and rules.get("departure") is Dictionary and Preparation._rules_valid(rules["departure"]) \
		and rules.get("configuration_table_va") == "0x6ad1d0" and rules.get("configuration_stride") == 42 \
		and rules.get("configuration_id") == 5 and rules.get("configuration_record_hex") == CONFIG_HEX \
		and rules.get("configuration_record_sha256") == CONFIG_SHA \
		and rules.get("functions") == {"commit":"0x4a1920","group":"0x4ab7a0","dispatch":"0x49e2b0",
			"constructor":"0x4b9120","round":"0x4b8ff0","configuration":"0x4da8e0"} \
		and rules.get("unresolved_functions") == ["0x4dab10","0x4b9340"]
