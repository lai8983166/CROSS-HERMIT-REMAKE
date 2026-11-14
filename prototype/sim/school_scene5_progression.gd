class_name SchoolScene5Progression
extends RefCounted
## Source-derived scene 5 predicates and requests; no scheduler or save writes.
## See docs/school_scene5_conditions.md. Native state is not inferred from HP.


static func choose_terminal(snapshot: Dictionary) -> Dictionary:
	if not _bounded(snapshot.get("scene_id"), 5, 5) \
			or not _bounded(snapshot.get("own_side"), 0, 3) \
			or not snapshot.get("event20_seen") is bool \
			or not _bounded(snapshot.get("own_casualties"), 0, 255) \
			or not _bounded(snapshot.get("remaining_ticks"), -2147483648, 2147483647) \
			or not snapshot.get("own_playable_unavailable") is bool:
		return _unsupported("missing_or_invalid_scene5_state")
	for key in ["enemy2", "enemy3", "enemy11"]:
		if not _actor(snapshot.get(key)):
			return _unsupported("missing_or_invalid_actor")
	# The native predicates on #3 and #11 assert these records are in use.
	if not snapshot.enemy3.used or not snapshot.enemy11.used:
		return _unsupported("required_actor_not_used")
	var own := int(snapshot.own_side)
	var seen := bool(snapshot.event20_seen)
	if int(snapshot.enemy3.side) == own and not seen:
		return _result("event20", -1, 20, 0, 0, 1, "captured_enemy3", "0x433849")
	if int(snapshot.enemy11.state) == 4 and snapshot.enemy2.used \
			and int(snapshot.enemy2.side) == own and int(snapshot.enemy3.side) == own:
		if int(snapshot.own_casualties) == 0:
			return _result("terminal", 2, 2, 1, 1, 0, "objective_without_casualties", "0x4338ad")
		return _result("terminal", 5, 5, 2, 1, 0, "objective_with_casualties", "0x4338bf")
	# The native input is signed32; negative values are not zero.
	if int(snapshot.remaining_ticks) == 0:
		return _result("terminal", 8 if seen else 11, 8 if seen else 11,
			3 if seen else 4, 1, 0, "timer_zero", "0x4338f4" if seen else "0x433908")
	if snapshot.own_playable_unavailable:
		return _result("terminal", 14, 8 if seen else 14, 5, 1, 0,
			"own_playable_unavailable", "0x43393a" if seen else "0x43394e")
	return _result("continue", -1, -1, 0, 0, 0, "no_condition", "0x4337f0")


static func capture_candidate(current_side: int, counts: Array) -> int:
	# 480D00 counts only the native mask's occupants (43C1D0); the caller
	# excludes side 7. -2 denotes unsupported input, -1 no takeover candidate.
	if current_side < 0 or current_side > 15 or counts.size() != 16:
		return -2
	for value in counts:
		if not _bounded(value, 0, 255):
			return -2
	if int(counts[7]) != 0:
		return -2
	var candidate := -1
	var maximum := 0
	for side in range(15, -1, -1):
		var value := _signed_byte(int(counts[side]))
		if value > maximum:
			maximum = value
			candidate = side
	if candidate == -1 or candidate == current_side:
		return -1
	if current_side == 7 or maximum > _signed_byte(int(counts[current_side])):
		return candidate
	return -1


static func capture_hold_limit(side: int) -> int:
	if side < 0 or side > 15:
		return -1
	return 900 if side < 4 else 600


static func capture_transition_ticks(character_id: int) -> int:
	# 47A590 mode21 phase2. These are source counter thresholds, not seconds.
	if character_id >= 387 and character_id <= 392 \
			or character_id >= 399 and character_id <= 404:
		return 72
	if character_id >= 393 and character_id <= 398:
		return 37
	if character_id in [405, 406]:
		return 62
	return -1


static func activation_requests() -> Array:
	# Ordered subset inside T0005 sub20, after its dialogue/control operations.
	# This does not claim those operations or placement/queue consumption ran.
	return [
		{"kind": "group", "group": 2, "center": Vector2i(3, 58), "radius": 3, "source_offset": 0x2A68},
		{"kind": "group", "group": 3, "center": Vector2i(4, 90), "radius": 3, "source_offset": 0x2A7C},
		{"kind": "group", "group": 4, "center": Vector2i(42, 48), "radius": 3, "source_offset": 0x2A90},
		{"kind": "group", "group": 5, "center": Vector2i(52, 39), "radius": 3, "source_offset": 0x2AA4},
		{"kind": "group", "group": 6, "center": Vector2i(28, 41), "radius": 3, "source_offset": 0x2AB8},
		{"kind": "unit", "enemy_number": 11, "work_index": 239, "center": Vector2i(16, 40), "radius": 10, "source_offset": 0x2AE8},
	]


static func _actor(value: Variant) -> bool:
	return value is Dictionary and value.get("used") is bool \
		and _bounded(value.get("side"), 0, 15) and _bounded(value.get("state"), 0, 5)


static func _bounded(value: Variant, minimum: int, maximum: int) -> bool:
	return typeof(value) == TYPE_INT and value >= minimum and value <= maximum


static func _signed_byte(value: int) -> int:
	return value - 256 if value >= 128 else value


static func _result(action: String, selector: int, sub: int, tactical: int,
		exit_flag: int, bit_write: int, reason: String, source_call: String) -> Dictionary:
	return {"supported": true, "action": action, "selector_arg": selector,
		"script_sub": sub, "tactical_result_selector": tactical, "exit_flag": exit_flag,
		"event20_bit_write": bit_write, "reason": reason, "source_handler_va": "0x4337f0",
		"source_call_va": source_call, "execution_scope": "source_derived_scene5_conditions",
		"live_witness": false, "authorizes_persistent_write": false}


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "live_witness": false,
		"authorizes_persistent_write": false}
