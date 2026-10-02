class_name TacticsScorePreparation
extends RefCounted
## Isolated task5/mode0 score preparation; produces staged packages only.
## Source rules and native expectation are exported separately from original EXE.


static func calculate(inputs: Dictionary, rules: Dictionary) -> Dictionary:
	for key in ["task_id", "mode", "cap_mode", "result_selector", "time_key", "unit_key",
			"initial_grade", "initial_total", "characters"]:
		if not inputs.has(key):
			return _unsupported("missing_" + key)
	for key in ["task_id", "base_points", "unit_bonus", "time_bonuses", "count_bonuses",
			"contribution_thresholds", "rates", "distributions", "attribute_thresholds", "growth_limit"]:
		if not rules.has(key):
			return _unsupported("missing_rules_" + key)
	if not _rules_valid(rules):
		return _unsupported("invalid_source_rules")
	for key in ["task_id", "mode", "cap_mode", "result_selector", "time_key", "unit_key", "initial_grade", "initial_total"]:
		if not _integer(inputs[key]):
			return _unsupported("invalid_" + key)
	if int(inputs["task_id"]) != 5 or int(inputs["mode"]) != 0 or int(inputs["cap_mode"]) != 0:
		return _unsupported("outside_task5_mode0_cap100")
	var selector := int(inputs["result_selector"])
	var time_key := int(inputs["time_key"])
	var unit_key := int(inputs["unit_key"])
	if selector < 1 or selector > 5 or time_key < 0 or time_key > 3 or unit_key < 1 or unit_key > 2:
		return _unsupported("outside_audited_result_keys")
	var units: Variant = inputs["characters"]
	if not units is Array or units.size() != 3:
		return _unsupported("outside_three_unit_subset")
	var seen := {}
	var contribution_sum := 0
	var status_sum := 0
	for unit in units:
		if not unit is Dictionary:
			return _unsupported("invalid_character")
		for key in ["character_id", "rate_class", "growth_pools", "skill_points", "group_bonus",
				"count_field_aa", "contribution_field_ac", "status_field_ae"]:
			if not unit.has(key):
				return _unsupported("missing_character_" + key)
		for key in ["character_id", "rate_class", "skill_points", "group_bonus", "count_field_aa", "contribution_field_ac", "status_field_ae"]:
			if not _integer(unit[key]) or int(unit[key]) < 0:
				return _unsupported("invalid_character_" + key)
		var character := int(unit["character_id"])
		if character < 1 or character > 45 or seen.has(character):
			return _unsupported("missing_or_duplicate_character_id")
		seen[character] = true
		if int(unit["rate_class"]) > 5 or int(unit["group_bonus"]) > 1000 \
				or int(unit["contribution_field_ac"]) > 1000 or int(unit["count_field_aa"]) > 1000 \
				or int(unit["status_field_ae"]) > 127 or int(unit["skill_points"]) > 8500000:
			return _unsupported("outside_audit_unit_bounds")
		if not unit["growth_pools"] is Array or unit["growth_pools"].size() != 7:
			return _unsupported("missing_growth_pools")
		for pool in unit["growth_pools"]:
			if not _integer(pool) or int(pool) < 0 or int(pool) > 1952500:
				return _unsupported("outside_cap100_pool_bounds")
		contribution_sum += int(unit["contribution_field_ac"])
		status_sum += int(unit["status_field_ae"])
	if int(inputs["initial_total"]) < 0 or int(inputs["initial_total"]) > 999999999 \
			or int(inputs["initial_grade"]) < 1 or int(inputs["initial_grade"]) > 5:
		return _unsupported("invalid_initial_grade_or_total")
	var grade_index := selector - 1
	var time_display := 3 if time_key == 0 or grade_index > 2 else time_key - 1
	if rules["time_bonuses"].all(func(value): return int(value) == 0):
		time_display = 4
	var unit_display := 0 if unit_key == 2 else 1
	var bonus := 0
	var bonus_count := 0
	if int(rules["unit_bonus"]) == 0:
		unit_display = 2
	elif unit_key == 2:
		bonus += int(rules["unit_bonus"])
		bonus_count += 1
	if time_display >= 0 and time_display < 3:
		bonus += int(rules["time_bonuses"][time_display])
		bonus_count += 1
	bonus_count += 1
	bonus += int(rules["count_bonuses"][0]) - bonus_count * 100
	var base_points := int(rules["base_points"][grade_index])
	var base_gain := base_points + _div(base_points * bonus, 100)
	var cap_pool := 0
	for index in range(101):
		cap_pool += int(rules["attribute_thresholds"][index])
	var packages := []
	var package_sum := 0
	var overflow_compensation := 0
	for unit in units:
		var ratio := 0 if contribution_sum == 0 else _div(int(unit["contribution_field_ac"]) * 100, contribution_sum)
		var rate_index := 0
		while rate_index < 10 and int(rules["contribution_thresholds"][rate_index]) - 1 < ratio:
			rate_index += 1
		var rate_class := int(unit["rate_class"])
		var weight := int(rules["rates"][rate_class][rate_index])
		var gain := base_gain + _div((weight - 100) * base_gain, 100) \
			+ _div(base_gain * _div(int(unit["group_bonus"]), 10), 100)
		gain = maxi(gain, _div(base_points, 2))
		var remaining := int(rules["growth_limit"]) - int(unit["skill_points"])
		for pool in unit["growth_pools"]:
			remaining -= int(pool)
		remaining = maxi(remaining, 0)
		var staged := []
		var total := 0
		for attribute in range(7):
			var amount := _div(gain * int(rules["distributions"][rate_class][attribute]), 100)
			var attribute_remaining := cap_pool - int(unit["growth_pools"][attribute])
			if amount > attribute_remaining:
				overflow_compensation += _div(amount - attribute_remaining, 2)
				amount = attribute_remaining
			if total + amount > remaining:
				var excess := total + amount - remaining
				var removed := mini(excess, amount)
				overflow_compensation += _div(removed, 2)
				amount -= removed
			staged.append(amount)
			total += amount
		staged.append(0)
		packages.append({"character_id": int(unit["character_id"]), "staged_package": staged,
			"staged_total": total})
		package_sum += total
	var status_factor := 90 if status_sum != 0 and status_sum <= units.size() else 100
	var total_delta := _div(_div(package_sum * status_factor, units.size()), 100) + overflow_compensation
	return {"supported": true, "task_grade": mini(int(inputs["initial_grade"]), selector),
		"grade_index": grade_index, "time_display": time_display, "unit_display": unit_display,
		"total_delta": total_delta, "total_after": clampi(int(inputs["initial_total"]) + total_delta, 0, 999999999),
		"characters": packages, "authorizes_persistent_write": false}


static func _div(numerator: int, denominator: int) -> int:
	@warning_ignore("integer_division")
	return numerator / denominator


static func _integer(value: Variant) -> bool:
	return (value is int or value is float) and is_finite(float(value)) \
		and float(value) == floor(float(value))


static func _rules_valid(rules: Dictionary) -> bool:
	if not _integer(rules["task_id"]) or int(rules["task_id"]) != 5 \
			or not _integer(rules["unit_bonus"]) or int(rules["unit_bonus"]) < 0 \
			or int(rules["unit_bonus"]) > 1000 or not _integer(rules["growth_limit"]) \
			or int(rules["growth_limit"]) != 8500000:
		return false
	for spec in [["base_points", 5, 1000000], ["time_bonuses", 3, 1000],
			["count_bonuses", 6, 1000], ["contribution_thresholds", 10, 100],
			["attribute_thresholds", 136, 1000000]]:
		if not _vector_valid(rules[spec[0]], spec[1], spec[2]):
			return false
	for spec in [["rates", 11, 1000], ["distributions", 7, 100]]:
		if not rules[spec[0]] is Array or rules[spec[0]].size() != 6:
			return false
		for row in rules[spec[0]]:
			if not _vector_valid(row, spec[1], spec[2]):
				return false
	return true


static func _vector_valid(value: Variant, size: int, maximum: int) -> bool:
	if not value is Array or value.size() != size:
		return false
	for number in value:
		if not _integer(number) or int(number) < 0 or int(number) > maximum:
			return false
	return true


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "authorizes_persistent_write": false}
