class_name CampaignTacticsPreparation
extends RefCounted
## Task5 score/loot preparation over the owned catalog, before state12 growth.
## Initial grade, bonus, clock and objective facts remain declared replay inputs.

const Score = preload("res://sim/tactics_score_preparation.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const Week = preload("res://sim/week_settlement_replay.gd")
const Layout = preload("res://sim/campaign_school_layout.gd")


static func project(before: Dictionary, inputs: Dictionary, rules: Dictionary) -> Dictionary:
	if not rules.get("preparation") is Dictionary or not rules.get("role") is Dictionary or not rules.get("week") is Dictionary:
		return _unsupported("missing_preparation_rules")
	var reason := Layout.validate(before, rules["week"])
	if reason.is_empty():
		reason = Roles._validate_rules(rules["role"])
	if not reason.is_empty():
		return _unsupported(reason)
	var source: Dictionary = rules["preparation"]
	if not source.get("score") is Dictionary or not Week._vector(source.get("job_rate_classes"), 31, 0, 255) \
			or not Week._vector(source.get("item_types"), 360, 0, 8) \
			or not Week._vector(source.get("fixed_items"), 8, 0, 360) \
			or not source.get("loot_quotas") is Array or source["loot_quotas"].size() != 5 \
			or not source.get("objective_rewards") is Array or source["objective_rewards"].size() != 16:
		return _unsupported("invalid_preparation_rules")
	for row in source["loot_quotas"]:
		if not Week._vector(row, 7, 0, 10):
			return _unsupported("invalid_loot_quotas")
	for row in source["objective_rewards"]:
		if not Week._vector(row, 3, 0, 360) or int(row[1]) > 7 or int(row[2]) > 10:
			return _unsupported("invalid_objective_rewards")
	for spec in [["task_id", 5, 5], ["mode", 0, 0], ["cap_mode", 0, 0],
			["initial_grade", 1, 5], ["group_bonus", 0, 1000], ["clock_seed", 0, 0x7fffffff]]:
		if not Week._bounded(inputs.get(spec[0]), spec[1], spec[2]):
			return _unsupported("invalid_preparation_" + spec[0])
	if not Week._vector(inputs.get("objective_slots"), 16, 0, 255) or not inputs.get("result_inputs") is Dictionary:
		return _unsupported("invalid_tactical_result_inputs")
	var tactical: Dictionary = inputs["result_inputs"]
	for spec in [["result_selector", 1, 5], ["time_key", 0, 3], ["unit_condition_key", 1, 2], ["field_4512", 0, 32767]]:
		if not Week._bounded(tactical.get(spec[0]), spec[1], spec[2]):
			return _unsupported("invalid_tactical_" + spec[0])
	if not tactical.get("units") is Array or tactical["units"].size() != 3:
		return _unsupported("outside_three_unit_preparation")
	var records := Roles._records(before)
	var seen := {}
	var ordinals := {}
	var units: Array = tactical["units"].duplicate(true)
	for unit in units:
		if not unit is Dictionary or not Week._bounded(unit.get("character_id"), 1, 12) \
				or not Week._bounded(unit.get("ordinal"), 0, 2):
			return _unsupported("invalid_tactical_unit_identity")
		var id := int(unit["character_id"])
		var ordinal := int(unit["ordinal"])
		if seen.has(id) or ordinals.has(ordinal) or not records.has(id) or int(before["availability"][id]) != 1:
			return _unsupported("missing_or_duplicate_preparation_id")
		seen[id] = true
		ordinals[ordinal] = true
		for spec in [["count_field_aa", 0, 1000], ["contribution_field_ac", 0, 1000], ["status_field_ae", 0, 127]]:
			if not Week._bounded(unit.get(spec[0]), spec[1], spec[2]):
				return _unsupported("invalid_tactical_unit_" + spec[0])
	units.sort_custom(func(a, b): return int(a["ordinal"]) < int(b["ordinal"]))
	# The next owned result currently requires complete week participants.
	# Reject a catalog we cannot carry forward before awarding anything or
	# occupying a preparation instance (e.g. three units with four active roles).
	var result_view := Layout.result_view(before, units.map(func(unit): return int(unit["character_id"])), rules["week"])
	if not result_view["supported"]:
		return result_view
	var score_inputs := {"task_id": 5, "mode": 0, "cap_mode": 0,
		"result_selector": tactical["result_selector"], "time_key": tactical["time_key"],
		"unit_key": tactical["unit_condition_key"], "initial_grade": inputs["initial_grade"],
		"initial_total": before["global_total_511c"], "characters": []}
	for unit in units:
		var id := int(unit["character_id"])
		var record: Dictionary = records[id]
		var points := 0
		for skill in range(84):
			if int(record["skill_statuses"][skill]) in [3, 5, 6]:
				points += int(rules["role"]["skills"][skill]["learned_points"])
		var character: Dictionary = unit.duplicate(true)
		character.merge({"rate_class": source["job_rate_classes"][int(record["job"])],
			"growth_pools": record["growth_pools"].duplicate(), "skill_points": points,
			"group_bonus": inputs["group_bonus"]})
		score_inputs["characters"].append(character)
	var score := Score.calculate(score_inputs, source["score"])
	if not score["supported"]:
		return score
	# 4BBCC0 calls grade/skill guard, loot, then score in that order. Score
	# validation is pure and runs first here so no invalid input can be published.
	var loot := _loot(before["item_flags"], score["grade_index"], inputs, source)
	if not loot["supported"]:
		return loot
	var loot_after := before.duplicate(true)
	loot_after["item_flags"] = loot["item_flags"]
	var after := loot_after.duplicate(true)
	records = Roles._records(after)
	for character in score["characters"]:
		var record: Dictionary = records[int(character["character_id"])]
		record["staged_package"] = character["staged_package"].duplicate()
		record["staged_total"] = character["staged_total"]
	after["global_total_511c"] = score["total_after"]
	# 4BD210 updates the task grade for task5; its random skill awards require
	# task_id==37 and therefore do not mutate this catalog's skills.
	reason = Layout.validate(after, rules["week"])
	if not reason.is_empty():
		return _unsupported(reason)
	return {"supported": true, "after": after, "summary": score,
		"loot_groups": loot["loot_groups"], "loot_draws": loot["draws"], "loot_rand_state": loot["rand_state"],
		"ordered_ids": units.map(func(unit): return int(unit["character_id"])),
		"phase_log": [{"phase": "tactical_grade_preparation", "before": before.duplicate(true),
			"after": before.duplicate(true), "task_grade": score["task_grade"], "source_functions": ["0x4bd210"]},
			{"phase": "tactical_loot_preparation", "before": before.duplicate(true),
			"after": loot_after, "source_functions": ["0x4bca40", "0x4d1c60", "0x4d1cb0"]},
			{"phase": "tactical_score_preparation", "before": loot_after.duplicate(true),
			"after": after.duplicate(true), "source_functions": ["0x4bbd40", "0x4d58e0", "0x4d5850"]}],
		"live_witness": false, "authorizes_persistent_write": false, "school_initialized": false}


static func _loot(flags: Array, grade: int, inputs: Dictionary, rules: Dictionary) -> Dictionary:
	var after := flags.duplicate()
	var candidates := []
	var awarded := []
	var quota := []
	for category in range(9):
		candidates.append([])
		awarded.append([])
		quota.append(0)
	for item in range(1, 361):
		var category := int(rules["item_types"][item - 1])
		if category > 0:
			candidates[category].append(item)
	for index in range(7):
		quota[7 - index] = int(rules["loot_quotas"][grade][index])
	for value in rules["fixed_items"]:
		var item := int(value)
		if item > 0 and (int(after[item - 1]) & 1) == 0:
			_award(after, awarded, item, int(rules["item_types"][item - 1]))
	for slot in range(16):
		if int(inputs["objective_slots"][slot]) == 0:
			continue
		var reward: Array = rules["objective_rewards"][slot]
		var item := int(reward[0])
		if item == 0:
			quota[int(reward[1])] += int(reward[2])
		elif (int(after[item - 1]) & 1) != 0:
			# Native objective-owned awards add at asStack1a5a[type], which
			# is the quota slot one category below the item type.
			quota[maxi(0, int(rules["item_types"][item - 1]) - 1)] += 2
		else:
			_award(after, awarded, item, int(rules["item_types"][item - 1]))
	var state := int(inputs["clock_seed"])
	var draws := []
	for category in range(7, 0, -1):
		for draw_index in range(int(quota[category])):
			if candidates[category].is_empty():
				quota[category - 1] += 2
				continue
			state = (state * 214013 + 2531011) & 0xffffffff
			var draw := (state >> 16) & 32767
			draws.append(draw)
			var item: int = candidates[category][draw % candidates[category].size()]
			if (int(after[item - 1]) & 1) == 0:
				_award(after, awarded, item, category)
			else:
				quota[category - 1] += 2
	var groups := []
	for category in range(7, 0, -1):
		var row: Array = awarded[category].duplicate()
		while row.size() < 10:
			row.append(0)
		groups.append(row)
	return {"supported": true, "item_flags": after, "loot_groups": groups, "draws": draws, "rand_state": state}


static func _award(flags: Array, awarded: Array, item: int, category: int) -> void:
	if category > 0 and awarded[category].size() < 10:
		awarded[category].append(item)
		flags[item - 1] = ((int(flags[item - 1]) | 1) & 0xf0ff) | 0x100


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "live_witness": false, "authorizes_persistent_write": false}
