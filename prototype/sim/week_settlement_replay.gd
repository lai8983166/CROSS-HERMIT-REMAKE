class_name WeekSettlementReplay
extends RefCounted
## Isolated projection of the COMPLETE 4D3510 body for the audited record layout.
## Shared campaign replay consumes this through its result transaction.
## No original live scene or save authority is inferred from the projection.

var _instances: Dictionary = {}


func apply_once(instance_id: String, context: Dictionary, before: Dictionary, rules: Dictionary) -> Dictionary:
	if instance_id.is_empty():
		return _unsupported("missing_instance_id")
	for key in ["task_state", "mode", "current", "total", "result_fields_completed"]:
		if not context.has(key):
			return _unsupported("missing_context_" + key)
	for key in ["task_state", "mode", "current", "total"]:
		if not _integer(context[key]):
			return _unsupported("invalid_context_" + key)
	if int(context["task_state"]) != 12 or int(context["current"]) != int(context["total"]) \
			or int(context["current"]) < 0 or int(context["total"]) > 5:
		return _unsupported("pending_state12_round_gate")
	if int(context["mode"]) != 0:
		return _unsupported("no_week_call_in_mode1_or_unknown")
	if not context["result_fields_completed"] is bool or not context["result_fields_completed"]:
		return _unsupported("pending_result_fields")
	var result := project(before, rules)
	if not result["supported"]:
		return result
	if int(before["month"]) != 15 or int(before["week"]) != 4:
		return {"supported": true, "status": "no_week_request", "after": before.duplicate(true),
			"authorizes_persistent_write": false}
	if _instances.has(instance_id):
		var entry: Dictionary = _instances[instance_id]
		if entry["context"] != context or entry["before"] != before or entry["rules"] != rules:
			return _unsupported("instance_input_conflict")
		return {"supported": true, "status": "duplicate", "after": entry["after"].duplicate(true),
			"authorizes_persistent_write": false}
	_instances[instance_id] = {"context": context.duplicate(true), "before": before.duplicate(true),
		"rules": rules.duplicate(true), "after": result["after"].duplicate(true)}
	result["status"] = "projected_once"
	return result


static func project(before: Dictionary, rules: Dictionary) -> Dictionary:
	var reason := _validate(before, rules)
	if not reason.is_empty():
		return _unsupported(reason)
	var after: Dictionary = before.duplicate(true)
	# JSON decodes integral numbers as floats. Normalize only after complete
	# validation: Array.has() otherwise treats int IDs and float IDs differently.
	for key in ["month", "week"]:
		after[key] = int(after[key])
	for key in ["0x7a55fa", "0x7a4e62", "0x7a55f6", "0x7e11a0"]:
		after["flags"][key] = int(after["flags"][key])
	for key in ["availability", "item_flags"]:
		for index in range(after[key].size()):
			after[key][index] = int(after[key][index])
	for record in after["participants"]:
		record["character_id"] = int(record["character_id"])
		for key in ["attributes", "job_progress", "unlock_flags", "skill_statuses", "equipped_skills", "equipped_items"]:
			for index in range(record[key].size()):
				record[key][index] = int(record[key][index])
	after["week"] = int(before["week"]) + 1
	if int(after["week"]) > 5:
		after["month"] = int(before["month"]) + 1
		after["week"] = 1
	after["flags"]["0x7a55fa"] = 0
	after["flags"]["0x7a4e62"] = 0
	var records := {}
	for record in after["participants"]:
		records[int(record["character_id"])] = record
		apply_unlocks(record, int(after["month"]), int(after["week"]), rules)
	for item in range(1, 361):
		var flags := int(after["item_flags"][item - 1])
		var kind := (flags >> 8) & 15
		if (flags & 1) == 0 or kind < 3 or kind > 4:
			continue
		var owner := (flags >> 1) & 127
		if int(after["availability"][owner]) == 0 or not records[owner]["equipped_items"].has(item):
			after["item_flags"][item - 1] = (flags & 0xf0ff) | 0x100
		else:
			after["item_flags"][item - 1] = (flags & 0xff01) | ((owner & 127) << 1)
	for character in range(1, 45):
		if int(after["availability"][character]) == 0:
			continue
		var record: Dictionary = records[character]
		for skill in range(84):
			if int(record["skill_statuses"][skill]) == 6 and not record["equipped_skills"].has(skill + 1):
				record["skill_statuses"][skill] = 5
	after["flags"]["0x7a55f6"] = 11
	after["flags"]["0x7e11a0"] = 0
	return {"supported": true, "after": after, "authorizes_persistent_write": false}


# Caller must validate the record and rules before applying this native helper.
static func apply_unlocks(record: Dictionary, month: int, week: int, rules: Dictionary) -> void:
	var total := 0
	for attribute in record["attributes"]:
		total += int(attribute)
	for category in range(30):
		var rule: Dictionary = rules["unlock_rules"][category]
		# The source compares month*6+week, although the calendar has 5 weeks.
		var dated := int(rule["month"]) != 0 and int(rule["week"]) != 0 \
			and (int(record["job_progress"][category + 1]) == 100 \
				or int(rule["month"]) * 6 + int(rule["week"]) <= month * 6 + week)
		var capable := total >= int(rule["minimum_total"])
		for k in range(7):
			if int(record["attributes"][k]) < int(rule["minimum_attributes"][k]):
				capable = false
		for requirement in rule["job_requirements"]:
			var kind := int(requirement["type"])
			if kind != 0 and int(record["job_progress"][kind]) < int(requirement["count"]):
				capable = false
		if dated or capable:
			record["unlock_flags"][category] = 1


static func _validate(before: Dictionary, rules: Dictionary) -> String:
	for key in ["month", "week", "flags", "participants", "availability", "item_flags"]:
		if not before.has(key):
			return "missing_" + key
	if not _bounded(before["month"], 4, 15) or not _bounded(before["week"], 1, 5):
		return "outside_calendar_probe_bounds"
	if not before["flags"] is Dictionary:
		return "invalid_flags"
	for key in ["0x7a55fa", "0x7a4e62", "0x7a55f6", "0x7e11a0"]:
		if not before["flags"].has(key) or not _bounded(before["flags"][key], -32768, 32767):
			return "missing_or_invalid_flag"
	if not _vector(before["availability"], 45, 0, 1) or int(before["availability"][0]) != 0:
		return "outside_availability_subset"
	if not _vector(before["item_flags"], 360, 0, 65535):
		return "invalid_item_flags"
	if not before["participants"] is Array or before["participants"].is_empty() or before["participants"].size() > 20:
		return "invalid_participants"
	var seen := {}
	for record in before["participants"]:
		if not record is Dictionary:
			return "invalid_character_record"
		for key in ["character_id", "attributes", "job_progress", "unlock_flags", "skill_statuses", "equipped_skills", "equipped_items"]:
			if not record.has(key):
				return "missing_character_" + key
		if not _bounded(record["character_id"], 1, 44) or seen.has(int(record["character_id"])):
			return "missing_or_duplicate_character_id"
		seen[int(record["character_id"])] = true
		for spec in [["attributes", 7, 0, 135], ["job_progress", 31, -128, 127],
				["unlock_flags", 30, 0, 1], ["skill_statuses", 84, 0, 6],
				["equipped_skills", 8, 0, 84], ["equipped_items", 8, 0, 360]]:
			if not _vector(record[spec[0]], spec[1], spec[2], spec[3]):
				return "invalid_character_" + spec[0]
	for character in range(1, 45):
		if int(before["availability"][character]) != 0 and not seen.has(character):
			return "missing_available_character_record"
	for flags in before["item_flags"]:
		var kind := (int(flags) >> 8) & 15
		if (int(flags) & 1) != 0 and kind >= 3 and kind <= 4 and ((int(flags) >> 1) & 127) >= 45:
			return "outside_item_owner_subset"
	if not rules.has("unlock_rules") or not rules["unlock_rules"] is Array or rules["unlock_rules"].size() != 30:
		return "missing_unlock_rules"
	for rule in rules["unlock_rules"]:
		if not rule is Dictionary:
			return "invalid_unlock_rule"
		for key in ["month", "week", "minimum_attributes", "minimum_total", "job_requirements"]:
			if not rule.has(key):
				return "missing_unlock_rule_field"
		if not _bounded(rule["month"], 0, 15) or not _bounded(rule["week"], 0, 5) \
				or not _vector(rule["minimum_attributes"], 7, 0, 135) or not _bounded(rule["minimum_total"], 0, 945) \
				or not rule["job_requirements"] is Array or rule["job_requirements"].size() != 3:
			return "invalid_unlock_rule_bounds"
		for requirement in rule["job_requirements"]:
			if not requirement is Dictionary or not requirement.has("type") or not requirement.has("count") \
					or not _bounded(requirement["type"], 0, 30) or not _bounded(requirement["count"], 0, 127):
				return "invalid_job_requirement"
	return ""


static func _integer(value: Variant) -> bool:
	return (value is int or value is float) and is_finite(float(value)) and float(value) == floor(float(value))


static func _bounded(value: Variant, minimum: int, maximum: int) -> bool:
	return _integer(value) and int(value) >= minimum and int(value) <= maximum


static func _vector(value: Variant, size: int, minimum: int, maximum: int) -> bool:
	if not value is Array or value.size() != size:
		return false
	for number in value:
		if not _bounded(number, minimum, maximum):
			return false
	return true


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "authorizes_persistent_write": false}
