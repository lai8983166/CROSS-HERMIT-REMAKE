class_name Scene5ConditionSelection
extends RefCounted
## Captured 4337F0 branch subset with a declared end-world, not a battle VM.
const Week = preload("res://sim/week_settlement_replay.gd")


static func select(event_world: Dictionary) -> Dictionary:
	for pair in [["scene_id", 5], ["own_side", 0], ["field_2e6f4", 0]]:
		if not Week._integer(event_world.get(pair[0])) or int(event_world[pair[0]]) != pair[1]:
			return _unsupported("outside_captured_scene5_event_world")
	if not Week._integer(event_world.get("event_bit3_0_word")) \
			or not int(event_world["event_bit3_0_word"]) in [0, 0x80000000]:
		return _unsupported("outside_captured_scene5_event_bit")
	if not event_world.get("units") is Array or event_world["units"].size() != 2:
		return _unsupported("missing_scene5_event_units")
	var units := {}
	for record in event_world["units"]:
		if not record is Dictionary or not Week._integer(record.get("enemy_number")):
			return _unsupported("invalid_scene5_event_unit")
		var number := int(record["enemy_number"])
		if not number in [3, 11] or units.has(number):
			return _unsupported("invalid_scene5_event_identity")
		for pair in [["wrapper_index", 250 - number], ["used", 1], ["side_a4", 1], ["field_f", 0]]:
			if not Week._integer(record.get(pair[0])) or int(record[pair[0]]) != pair[1]:
				return _unsupported("outside_captured_scene5_unit_fields")
		if not Week._bounded(record.get("character_id"), 49 if number == 3 else 50, 49 if number == 3 else 50):
			return _unsupported("outside_captured_scene5_npc_ids")
		units[number] = record
	# 46A430(enemy3) is false (side1 != own0); 469170(enemy11) is 0.
	# field2E6F4==0 leads to 4E2720(3,0), selecting the terminal wrapper.
	var bit := int(event_world["event_bit3_0_word"]) >> 31
	var sub := 11 if bit == 0 else 8
	var result_selector := 4 if sub == 11 else 3  # 60CA7C selector table.
	return {"supported": true, "selector_arg": sub, "script_sub": sub,
		"tactical_result_selector": result_selector, "round_grade_index": result_selector - 1,
		"exit_flag": 1, "source_handler_va": "0x4337f0", "source_call_va": "0x433908" if bit == 0 else "0x4338f4",
		"source_wrapper_va": "0x454af0", "declared_event_world": event_world.duplicate(true),
		"execution_scope": "isolated_declared_scene5_condition_subset", "live_witness": false,
		"authorizes_persistent_write": false}


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "live_witness": false, "authorizes_persistent_write": false}
