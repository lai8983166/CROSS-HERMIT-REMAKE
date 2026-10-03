class_name AllResultRoleReplay
extends RefCounted
## Isolated state12 role store. Native fixtures authorize this projection only;
## Shared campaign replay can consume it through ResultTransactionReplay.
## Original saves remain outside its authority; week/school are separate stages.

var _instances: Dictionary = {}


func begin(instance_id: String, context: Dictionary, before: Dictionary, rules: Dictionary) -> Dictionary:
	if instance_id.is_empty():
		return _unsupported("missing_instance_id")
	var reason := _validate_snapshot(before)
	if reason.is_empty():
		reason = _validate_context(context, before, true)
	if reason.is_empty():
		reason = _validate_rules(rules)
	if not reason.is_empty():
		return _unsupported(reason)
	var input := {"context": context.duplicate(true), "before": before.duplicate(true), "rules": rules.duplicate(true)}
	if _instances.has(instance_id):
		if _instances[instance_id]["input"] != input:
			return _unsupported("instance_input_conflict")
		return _view(_instances[instance_id], "duplicate")
	var ctx: Dictionary = _integers(input["context"])
	var branch := 1 if ctx["mode"] == 1 else (2 if before["month"] == 15 and before["week"] == 4 else 0)
	var ids: Array = ctx["round_ids"] if branch == 1 else _group_ids(ctx)
	if branch == 1 and ctx["result_flag"] == 0:
		ids = []
	var growth := project_growth(before, ids, ctx["clock_seed"], rules)
	if not growth["supported"]:
		return growth
	var after: Dictionary = growth["after"]
	after["recipient_id"] = -1
	if branch != 1:
		var best := 0
		var records := _records(after)
		for character in _group_ids(ctx):
			if records[character]["staged_total"] > best:
				best = records[character]["staged_total"]
				after["recipient_id"] = character
		# Native later accesses this ID without a negative-ID guard.
		if after["recipient_id"] < 0:
			return _unsupported("unresolved_recipient_address")
	after["global_total_511c"] = clampi(after["global_total_511c"], 0, 999999999)
	var entry := {"input": input, "after": after, "branch": branch,
		"learning_draws": growth["learning_draws"], "rand_state": growth["rand_state"],
		"display_request": growth["display_request"], "skill_display_needed": growth["skill_display_needed"],
		"confirmed_seen": false, "completed": false, "requested_state": 12,
		"result_fields_completed": false, "week_pending": false}
	_instances[instance_id] = entry
	return _view(entry, "initialized_once")


func finish(instance_id: String, confirmed: bool, mvp_ready: bool) -> Dictionary:
	if not _instances.has(instance_id):
		return _unsupported("missing_initialized_instance")
	var entry: Dictionary = _instances[instance_id]
	if entry["completed"]:
		return _view(entry, "duplicate")
	var context: Dictionary = entry["input"]["context"]
	if entry["branch"] == 0:
		entry["confirmed_seen"] = entry["confirmed_seen"] or confirmed
		if not entry["confirmed_seen"]:
			return _view(entry, "waiting_confirmation")
		if not mvp_ready:
			return _view(entry, "waiting_mvp")
	if entry["branch"] == 1:
		entry["requested_state"] = 15 if context["result_flag"] == 0 else 13
	else:
		var post := project_post_fields(entry["after"], context)
		if not post["supported"]:
			return post
		entry["after"] = post["after"]
		var records := _records(entry["after"])
		var recipient: Dictionary = records[entry["after"]["recipient_id"]]
		recipient["recipient_count"] = clampi(recipient["recipient_count"] + 1, 0, 5)
		entry["result_fields_completed"] = true
		entry["week_pending"] = entry["branch"] == 2
		entry["requested_state"] = 12 if entry["week_pending"] else 6
	entry["completed"] = true
	return _view(entry, "week_boundary" if entry["week_pending"] else "completed_once")


static func project_growth(before: Dictionary, ordered_ids: Array, seed: int, rules: Dictionary) -> Dictionary:
	var reason := _validate_snapshot(before)
	if reason.is_empty():
		reason = _validate_rules(rules)
	if not reason.is_empty():
		return _unsupported(reason)
	if seed < 0 or seed > 0xffffffff:
		return _unsupported("invalid_seed")
	var records := _records(_normalized_snapshot(before))
	var seen := {}
	var ids := []
	# Validate ALL participating pools before copying/applying any role.
	var increments: Array = rules["attribute_increments"]
	var maximum_pool := 0
	for k in range(1, 136):
		maximum_pool += int(increments[k])
	for value in ordered_ids:
		if not _bounded(value, 1, 12) or seen.has(int(value)) or not records.has(int(value)):
			return _unsupported("missing_or_duplicate_growth_id")
		var id := int(value)
		seen[id] = true
		ids.append(id)
		for k in range(7):
			var pool: int = records[id]["growth_pools"][k] + records[id]["staged_package"][k]
			if pool < 0 or pool >= maximum_pool:
				return _unsupported("pool_walk_outside_source_table")
	var after: Dictionary = _normalized_snapshot(before)
	records = _records(after)
	var normalized_rules: Dictionary = _integers(rules)
	var state := seed
	var draws := []
	var display := []
	var skill_display := 0
	for id in ids:
		var record: Dictionary = records[id]
		var old_attributes: Array = record["attributes"].duplicate()
		var old_level: int = record["level_50"]
		var points := 0
		for k in range(7):
			record["growth_pools"][k] += record["staged_package"][k]
			points += int(record["growth_pools"][k])
			var cumulative := 0
			for level in range(1, 136):
				cumulative += int(increments[level])
				if cumulative > int(record["growth_pools"][k]):
					record["attributes"][k] = maxi(1, level - 1)
					break
		for sid in range(84):
			if record["skill_statuses"][sid] in [3, 5, 6]:
				points += int(normalized_rules["skills"][sid]["learned_points"])
		if points > 0x7fffffff:
			return _unsupported("level_total_overflow")
		var level := 2
		while level < 51 and int(normalized_rules["level_thresholds"][level - 1]) <= points:
			level += 1
		record["level_50"] = level - 1
		var job_sums := [0, 0, 0, 0, 0]
		for k in range(5):
			for block in range(3):
				for j in range(2):
					job_sums[k] += int(record["job_progress"][1 + block * 10 + k * 2 + j])
		var effects := [0, 0, 0, 0, 0, 0, 0]
		for category in range(11):
			var cap: int = normalized_rules["job_skill_caps"][record["job"]][category]
			if cap == 0:
				continue
			var grid: Array = normalized_rules["skill_grid"][category]
			var learned_span := 0
			for position in range(7):
				if record["skill_statuses"][grid[position] - 1] in [3, 5, 6]:
					learned_span = position + 1
			for position in range(cap):
				var sid: int = grid[position]
				var status: int = record["skill_statuses"][sid - 1]
				if status in [3, 5, 6]:
					continue
				if status != 0:
					break
				var probability := cap + learned_span * 5
				if probability != 100:
					state = (state * 214013 + 2531011) & 0xffffffff
					var draw := (state >> 16) & 32767
					draws.append(draw)
					if draw % 101 > probability:
						break
				var rule: Dictionary = normalized_rules["skills"][sid - 1]
				var eligible := true
				var total := 0
				for k in range(7):
					total += int(record["attributes"][k])
					if int(record["attributes"][k]) < int(rule["minimum_attributes"][k]):
						eligible = false
				if total < int(rule["minimum_total"]):
					eligible = false
				for k in range(5):
					if job_sums[k] < int(rule["minimum_job_sums"][k]):
						eligible = false
				if eligible:
					record["skill_statuses"][sid - 1] = 2
					skill_display = 1
					effects[[0, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4][category]] = 1
				break # A category tests only its first missing candidate.
		display.append({"character_id": id, "attributes_before": old_attributes,
			"level_before": old_level, "attributes_after": record["attributes"].duplicate(),
			"level_after": record["level_50"], "skill_effect_flags": effects})
	return {"supported": true, "after": after, "learning_draws": draws, "rand_state": state,
		"display_request": display, "skill_display_needed": skill_display,
		"authorizes_persistent_write": false, "live_witness": false}


static func project_post_fields(before: Dictionary, context: Dictionary) -> Dictionary:
	var reason := _validate_snapshot(before)
	if reason.is_empty():
		reason = _validate_context(context, before, false)
	if not reason.is_empty():
		return _unsupported(reason)
	var after: Dictionary = _normalized_snapshot(before)
	var ctx: Dictionary = _integers(context)
	var records := _records(after)
	var ids: Array = ctx["participant_ids"]
	var history_index: int = (after["month"] - 4) * 5 + after["week"] - 1
	for id in ids:
		var record: Dictionary = records[id]
		var value: int = record["job_progress"][record["job"]]
		if value != 100:
			value = ((value + 1 + 128) & 255) - 128 # Native add CL,1 then MOVSX.
			record["job_progress"][record["job"]] = clampi(value, 0, 99)
		record["week_records"][history_index * 3] = 2
		record["week_records"][history_index * 3 + 1] = ctx["group0_record_data"][0]
		record["week_records"][history_index * 3 + 2] = ctx["group0_record_data"][1]
	# Native clamps each individual update, including raw task teacher slot0.
	for relation in after["relationships"]:
		if relation["from"] == 0 or relation["to"] == 0:
			relation["value"] = clampi(relation["value"] + 1, 1, 100)
		else:
			relation["value"] = clampi(relation["value"] + 1, 1, 100)
			relation["value"] = clampi(relation["value"] + [3, 2, 1, 0, -1][ctx["round_grade"]], 1, 100)
	return {"supported": true, "after": after, "authorizes_persistent_write": false}


static func _view(entry: Dictionary, status: String) -> Dictionary:
	var result := {"supported": true, "status": status, "school_initialized": false,
		"authorizes_persistent_write": false, "live_witness": false}
	for key in ["after", "branch", "learning_draws", "rand_state", "display_request", "skill_display_needed",
			"requested_state", "result_fields_completed", "week_pending"]:
		result[key] = entry[key]
	return result.duplicate(true)


static func _records(snapshot: Dictionary) -> Dictionary:
	var result := {}
	for record in snapshot["characters"]:
		result[int(record["character_id"])] = record
	return result


static func _group_ids(context: Dictionary) -> Array:
	var result := []
	for index in context["group_slots"][0]:
		if int(index) >= 0:
			result.append(int(context["participant_ids"][int(index)]))
	return result


static func _validate_context(context: Dictionary, before: Dictionary, gate: bool) -> String:
	if gate:
		for key in ["task_state", "current", "total", "mode", "result_flag", "clock_seed"]:
			if not context.has(key) or not _bounded(context[key], 0, 0xffffffff):
				return "invalid_context_" + key
		if int(context["task_state"]) != 12 or int(context["current"]) != int(context["total"]) or int(context["total"]) > 5:
			return "pending_state12_round_gate"
		if int(context["mode"]) > 1 or int(context["result_flag"]) > 1:
			return "unknown_mode_or_result_flag"
	for key in ["participant_ids", "group_slots", "round_ids", "group0_record_data", "teacher_ids", "task_teacher_slots"]:
		if not context.get(key) is Array:
			return "invalid_context_" + key
	var records := _records(before)
	var ids: Array = context["participant_ids"]
	if ids.size() != records.size() or ids.is_empty() or ids.size() > 4:
		return "uncovered_roster_size"
	var seen := {}
	for id in ids:
		if not _bounded(id, 1, 12) or seen.has(int(id)) or not records.has(int(id)):
			return "missing_or_duplicate_participant_id"
		seen[int(id)] = true
	if not _vector(context["round_ids"], ids.size(), 1, 12):
		return "invalid_round_ids"
	seen = {}
	for id in context["round_ids"]:
		if seen.has(int(id)) or not records.has(int(id)):
			return "missing_or_duplicate_round_id"
		seen[int(id)] = true
	if context["group_slots"].size() != 5:
		return "invalid_groups"
	seen = {}
	for group in range(5):
		if not _vector(context["group_slots"][group], 4, -1, ids.size() - 1):
			return "invalid_group_indices"
		for index in context["group_slots"][group]:
			if int(index) >= 0:
				if group != 0 or seen.has(int(index)):
					return "uncovered_group_or_duplicate_member"
				seen[int(index)] = true
	if seen.size() != ids.size():
		return "unassigned_participant"
	if not _bounded(context.get("group0_activity_type"), 2, 2) or not _bounded(context.get("support_count"), 0, 0):
		return "uncovered_course_or_support"
	if not _vector(context["teacher_ids"], 5, -1, -1) or not _vector(context["task_teacher_slots"], 5, 0, 0) \
			or context.get("task_allocation_initial_contents") != "explicit_zero_memory":
		return "uncovered_task_teacher_initial_contents"
	if not _vector(context["group0_record_data"], 2, 0, 255) or not _bounded(context.get("round_grade"), 0, 4):
		return "invalid_history_or_grade"
	return ""


static func _validate_snapshot(before: Dictionary) -> String:
	if not _bounded(before.get("month"), 4, 15) or not _bounded(before.get("week"), 1, 5):
		return "outside_calendar_bounds"
	if (int(before["month"]) - 4) * 5 + int(before["week"]) - 1 >= 59:
		return "history_overlaps_progress_fields"
	if not _bounded(before.get("global_total_511c"), -0x80000000, 0x7fffffff) or not _bounded(before.get("recipient_id"), -1, 12):
		return "invalid_global_fields"
	if not before.get("characters") is Array or before["characters"].is_empty() or before["characters"].size() > 4:
		return "invalid_characters"
	var seen := {}
	for record in before["characters"]:
		if not record is Dictionary or not _bounded(record.get("character_id"), 1, 12):
			return "missing_character_id"
		var id := int(record["character_id"])
		if seen.has(id):
			return "duplicate_character_id"
		seen[id] = true
		for bounds in [["job", 1, 30], ["level_50", 1, 50], ["staged_total", -0x80000000, 0x7fffffff], ["recipient_count", -32768, 32767]]:
			if not _bounded(record.get(bounds[0]), bounds[1], bounds[2]):
				return "invalid_character_" + bounds[0]
		for bounds in [["attributes", 7, 1, 135], ["growth_pools", 7, 0, 0x7fffffff],
				["skill_statuses", 84, 0, 6], ["staged_package", 8, -0x80000000, 0x7fffffff],
				["job_progress", 31, -128, 127], ["week_records", 177, 0, 255]]:
			if not _vector(record.get(bounds[0]), bounds[1], bounds[2], bounds[3]):
				return "invalid_character_" + bounds[0]
	seen[0] = true # Raw relation slot0; it is not a named participant/teacher.
	if not before.get("relationships") is Array or before["relationships"].size() != seen.size() * (seen.size() - 1):
		return "incomplete_relationship_snapshot"
	var links := {}
	for relation in before["relationships"]:
		if not relation is Dictionary or not _bounded(relation.get("from"), 0, 12) or not _bounded(relation.get("to"), 0, 12) \
				or not _bounded(relation.get("value"), 0, 100):
			return "invalid_relationship"
		var a := int(relation["from"])
		var b := int(relation["to"])
		var key := a * 68 + b
		if a == b or not seen.has(a) or not seen.has(b) or links.has(key):
			return "duplicate_or_unknown_relationship"
		links[key] = true
	return ""


static func _validate_rules(rules: Dictionary) -> String:
	if not _vector(rules.get("attribute_increments"), 136, 0, 0x7fffffff) \
			or not _vector(rules.get("level_thresholds"), 50, 0, 0x7fffffff):
		return "invalid_growth_tables"
	for k in range(1, 136):
		if int(rules["attribute_increments"][k]) <= 0:
			return "invalid_attribute_increment"
	if not rules.get("skill_grid") is Array or rules["skill_grid"].size() != 12:
		return "invalid_skill_grid"
	var seen := {}
	for row in rules["skill_grid"]:
		if not _vector(row, 7, 1, 84):
			return "invalid_skill_grid_row"
		for sid in row:
			if seen.has(int(sid)):
				return "duplicate_skill_grid_id"
			seen[int(sid)] = true
	if not rules.get("job_skill_caps") is Array or rules["job_skill_caps"].size() != 31:
		return "invalid_job_caps"
	for job in range(31):
		# Export preserves the bytes at index0, including header values >7.
		# Actual audited characters use jobs1..30; never execute that header.
		if not _vector(rules["job_skill_caps"][job], 11, 0, 255 if job == 0 else 7):
			return "invalid_job_caps_row"
	if not rules.get("skills") is Array or rules["skills"].size() != 84:
		return "invalid_skill_rules"
	for skill in rules["skills"]:
		if not skill is Dictionary or not _vector(skill.get("minimum_attributes"), 7, -32768, 32767) \
				or not _vector(skill.get("minimum_job_sums"), 5, -32768, 32767) \
				or not _bounded(skill.get("minimum_total"), -32768, 32767) \
				or not _bounded(skill.get("learned_points"), 0, 0x7fffffff):
			return "invalid_skill_requirement"
	return ""


static func _integers(value: Variant) -> Variant:
	if value is float:
		return int(value)
	if value is Array:
		var result := []
		for entry in value:
			result.append(_integers(entry))
		return result
	if value is Dictionary:
		var result := {}
		for key in value:
			result[key] = _integers(value[key])
		return result
	return value


static func _normalized_snapshot(before: Dictionary) -> Dictionary:
	# Preserve opaque/extra data, including fractional presentation fields.
	var after := before.duplicate(true)
	for key in ["month", "week", "global_total_511c", "recipient_id"]:
		after[key] = int(after[key])
	for record in after["characters"]:
		for key in ["character_id", "job", "level_50", "staged_total", "recipient_count"]:
			record[key] = int(record[key])
		for key in ["attributes", "growth_pools", "skill_statuses", "staged_package", "job_progress", "week_records"]:
			for index in range(record[key].size()):
				record[key][index] = int(record[key][index])
	for relation in after["relationships"]:
		for key in ["from", "to", "value"]:
			relation[key] = int(relation[key])
	return after


static func _bounded(value: Variant, minimum: int, maximum: int) -> bool:
	return (value is int or value is float) and is_finite(float(value)) and float(value) == float(int(value)) \
		and int(value) >= minimum and int(value) <= maximum


static func _vector(value: Variant, count: int, minimum: int, maximum: int) -> bool:
	if not value is Array or value.size() != count:
		return false
	for entry in value:
		if not _bounded(entry, minimum, maximum):
			return false
	return true


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "authorizes_persistent_write": false}
