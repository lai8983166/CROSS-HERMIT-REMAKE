extends RefCounted
## Original 4A3CA0/4A8BF0 ordering; no role, reward, calendar or class edits.

const Roles = preload("res://sim/all_result_role_replay.gd")
const Week = preload("res://sim/week_settlement_replay.gd")
const Layout = preload("res://sim/campaign_school_layout.gd")
const SOURCE_SHA := "588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005"


static func order(profiles: Variant, waiting_ids: Variant, mode: Variant, rules: Dictionary) -> Dictionary:
	if not Week._bounded(mode, 0, 2):
		return _unsupported("invalid_waitlist_sort_mode")
	if rules.get("source_image_sha256") != SOURCE_SHA \
			or not Week._vector(rules.get("job_categories"), 31, 0, 5):
		return _unsupported("invalid_waitlist_sort_rules")
	if not profiles is Array or not waiting_ids is Array or waiting_ids.size() > 20 \
			or not Week._vector(waiting_ids, waiting_ids.size(), 1, 12):
		return _unsupported("invalid_waitlist_members")
	var records := {}
	for row in profiles:
		if not row is Dictionary or not Week._bounded(row.get("character_id"), 1, 12) \
				or records.has(int(row["character_id"])) or not Week._bounded(row.get("job"), 1, 30) \
				or not Week._bounded(row.get("level_50"), 0, 255) \
				or not Week._vector(row.get("attributes"), 7, 0, 255):
			return _unsupported("invalid_waitlist_profile")
		records[int(row["character_id"])] = row
	var ids: Array = Roles._integers(waiting_ids)
	var seen := {}
	for id in ids:
		if not records.has(id) or seen.has(id):
			return _unsupported("missing_or_duplicate_waitlist_member")
		seen[id] = true
	if int(mode) == 1:
		var categorized := []
		for category in range(6):
			for id in ids:
				if int(rules["job_categories"][int(records[id]["job"])]) == category:
					categorized.append(id)
		ids = categorized
	else:
		var keys := {}
		for id in ids:
			var total := 0
			for value in records[id]["attributes"]:
				total += int(value)
			keys[id] = int(records[id]["level_50"]) if int(mode) == 0 else total
		# Strict comparison + pair swaps: stable sorting would change tied outputs.
		for i in range(ids.size()):
			for j in range(i + 1, ids.size()):
				if keys[ids[i]] < keys[ids[j]]:
					var old: int = ids[i]
					ids[i] = ids[j]
					ids[j] = old
	return {"supported": true, "idle_student_ids": ids, "idle_sort_mode": int(mode)}


static func project(snapshot: Dictionary, mode: Variant, rules: Dictionary, week_rules: Dictionary) -> Dictionary:
	var reason := Layout.validate(snapshot, week_rules)
	if not reason.is_empty():
		return _unsupported(reason)
	var school: Dictionary = snapshot["school"]
	if not school.get("school_control") is Dictionary or int(school["school_control"]["person_ready"]) != 1:
		return _unsupported("pending_school_waitlist")
	# This operation is currently bounded to the captured teacherless layout.
	for group in school["group_student_ids"]:
		if group != [-1, -1, -1, -1]:
			return _unsupported("outside_teacherless_waitlist")
	var ids: Array = school["school_control"]["idle_student_ids"].duplicate()
	var roster: Array = school["student_ids"].slice(0, int(school["student_count"]))
	var sorted_ids := ids.duplicate()
	sorted_ids.sort()
	roster.sort()
	if sorted_ids != roster:
		return _unsupported("waitlist_roster_mismatch")
	var profiles := []
	var records := Roles._records(snapshot)
	for id in ids:
		profiles.append(records[int(id)])
	var result := order(profiles, ids, mode, rules)
	if not result["supported"]:
		return result
	var after := snapshot.duplicate(true)
	after["school"]["school_control"]["idle_student_ids"] = result["idle_student_ids"].duplicate()
	after["school"]["school_control"]["idle_sort_mode"] = result["idle_sort_mode"]
	return {"supported": true, "after": after, "changed": after != snapshot,
		"execution_scope": "sourced_student_waitlist_ordering", "live_witness": false,
		"authorizes_persistent_write": false, "school_initialized": false, "interactive_school_ready": false}


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "live_witness": false,
		"authorizes_persistent_write": false, "school_initialized": false, "interactive_school_ready": false}
