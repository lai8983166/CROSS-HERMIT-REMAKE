class_name BattleRoundGate
extends RefCounted
## Isolated projection of 4B8FF0 and roster/count writes. No transaction authority.
## Configuration 5 only; resources and combat-unit derivation remain unresolved.


static func step(before: Dictionary, table: Dictionary, state10_dispatched: bool) -> Dictionary:
	if not state10_dispatched:
		return {"supported": true, "status": "pending_state10", "requested_state": -1,
			"authorizes_persistent_write": false}
	for key in ["current", "total", "temp_roster", "temp_count", "combat_count", "scene_id"]:
		if not before.has(key):
			return _unsupported("missing_" + key)
	if not _integer(before["current"]) or not _integer(before["total"]):
		return _unsupported("invalid_counters")
	var current := int(before["current"])
	var total := int(before["total"])
	# Safety limits for this audit subset; original native code has no such guard.
	if current < 0 or current > total or total > 5:
		return _unsupported("outside_audit_counter_subset")
	if not before["temp_roster"] is Array or before["temp_roster"].size() != 100:
		return _unsupported("invalid_temp_roster")
	for key in ["temp_count", "combat_count", "scene_id"]:
		if not _integer(before[key]):
			return _unsupported("invalid_" + key)
	var after := before.duplicate(true)
	var output := {"supported": true, "after": after, "requested_state": 12,
		"status": "all_result_requested", "dispatch_target_va": 0x4C1D30,
		"preparation_resolved": false, "combat_units_ready": false,
		"authorizes_persistent_write": false}
	if current == total:
		return output
	if not table.has("config_id") or not _integer(table["config_id"]) \
			or int(table["config_id"]) != 5:
		return _unsupported("outside_configuration_five")
	if not table.has("next_roster") or not table["next_roster"] is Array \
			or table["next_roster"].size() > 20:
		return _unsupported("invalid_next_roster")
	for character in table["next_roster"]:
		if not _integer(character) or int(character) < 0 or int(character) >= 68:
			return _unsupported("outside_audit_character_subset")
	after["temp_roster"] = []
	after["temp_roster"].resize(100)
	after["temp_roster"].fill(-1)
	for ordinal in range(table["next_roster"].size()):
		after["temp_roster"][ordinal] = int(table["next_roster"][ordinal])
	after["temp_count"] = table["next_roster"].size()
	after["combat_count"] = table["next_roster"].size()
	after["scene_id"] = 5
	after["current"] = current + 1
	output["requested_state"] = 16
	output["status"] = "next_round_requested"
	output["dispatch_target_va"] = 0x451080
	return output


static func _integer(value: Variant) -> bool:
	return (value is int or value is float) and is_finite(float(value)) \
		and float(value) == floor(float(value))


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "authorizes_persistent_write": false}
