class_name CampaignSchoolLayout
extends RefCounted
## One canonical character catalog, with explicit result and school views.
## Mapping carries no execution/completion or original save authority.

const Roles = preload("res://sim/all_result_role_replay.gd")
const Week = preload("res://sim/week_settlement_replay.gd")
const Transaction = preload("res://sim/result_transaction_replay.gd")
const RESULT_ONLY = ["staged_package", "staged_total", "recipient_count", "week_records"]
const SHARED = ["month", "week", "flags", "availability", "item_flags"]


static func validate(snapshot: Dictionary, rules: Dictionary) -> String:
	var reason := Roles._validate_snapshot(snapshot, true)
	if reason.is_empty():
		reason = Week._validate(Transaction._week_input(snapshot), rules)
	if not reason.is_empty():
		return reason
	if not snapshot.get("school") is Dictionary:
		return "missing_school_layout"
	var school: Dictionary = snapshot["school"]
	if not Week._bounded(school.get("student_count"), 0, 20) \
			or not Week._bounded(school.get("teacher_count"), 0, 0) \
			or not Week._vector(school.get("student_ids"), 20, -1, 12) \
			or not Week._vector(school.get("teacher_ids"), 20, -1, -1):
		return "outside_school_catalog_subset"
	var records := Roles._records(snapshot)
	var students := {}
	for index in range(20):
		var identity := int(school["student_ids"][index])
		if index < int(school["student_count"]):
			if not records.has(identity) or students.has(identity) or int(snapshot["availability"][identity]) != 1:
				return "missing_or_duplicate_available_student"
			students[identity] = true
		elif identity != -1:
			return "invalid_student_tail"
	for identity in range(1, 45):
		if int(snapshot["availability"][identity]) != (1 if students.has(identity) else 0):
			return "catalog_availability_mismatch"
	for record in snapshot["characters"]:
		if not Week._vector(record.get("unlock_reserved_bytes"), 2, 0, 255):
			return "missing_reserved_unlock_bytes"
	for key in ["group_student_ids", "group_student_indices"]:
		if not school.get(key) is Array or school[key].size() != 5:
			return "invalid_group_layout"
	for group in range(5):
		if not Week._vector(school["group_student_ids"][group], 4, -1, 12) \
				or not Week._vector(school["group_student_indices"][group], 4, -1, int(school["student_count"]) - 1):
			return "invalid_group_layout"
		for slot in range(4):
			var identity := int(school["group_student_ids"][group][slot])
			var index := int(school["group_student_indices"][group][slot])
			if identity == -1:
				if index != -1:
					return "inconsistent_group_index"
			elif not students.has(identity) or index < 0 or int(school["student_ids"][index]) != identity:
				return "inconsistent_group_index"
	if not school.get("adv_globals") is Dictionary or school["adv_globals"].has("0x7e1180"):
		return "duplicated_or_missing_recipient_alias"
	for key in ["0x7a5292", "0x7e1182"]:
		if not Week._bounded(school["adv_globals"].get(key), -32768, 32767):
			return "invalid_adv_global"
	return ""


static func school_view(snapshot: Dictionary, rules: Dictionary) -> Dictionary:
	var reason := validate(snapshot, rules)
	if not reason.is_empty():
		return _unsupported(reason)
	var view: Dictionary = snapshot["school"].duplicate(true)
	for key in SHARED:
		view[key] = snapshot[key].duplicate(true) if snapshot[key] is Array or snapshot[key] is Dictionary else snapshot[key]
	view["adv_globals"]["0x7e1180"] = snapshot["recipient_id"]
	view["participants"] = []
	for record in snapshot["characters"]:
		var row: Dictionary = record.duplicate(true)
		for key in RESULT_ONLY:
			row.erase(key)
		view["participants"].append(row)
	return _mapped(view)


static func result_view(snapshot: Dictionary, ordered_ids: Variant, rules: Dictionary) -> Dictionary:
	var reason := validate(snapshot, rules)
	if not reason.is_empty():
		return _unsupported(reason)
	if not ordered_ids is Array or ordered_ids.is_empty() or ordered_ids.size() > 4 \
			or not Week._vector(ordered_ids, ordered_ids.size(), 1, 12):
		return _unsupported("invalid_result_catalog_ids")
	var records := Roles._records(snapshot)
	var selected := {0: true}
	for identity in ordered_ids:
		if not records.has(int(identity)) or selected.has(int(identity)):
			return _unsupported("missing_or_duplicate_result_catalog_id")
		selected[int(identity)] = true
	var view := snapshot.duplicate(true)
	view.erase("school")
	view["characters"] = []
	for record in snapshot["characters"]:
		if selected.has(int(record["character_id"])):
			view["characters"].append(record.duplicate(true))
	view["relationships"] = []
	for relation in snapshot["relationships"]:
		if selected.has(int(relation["from"])) and selected.has(int(relation["to"])):
			view["relationships"].append(relation.duplicate(true))
	# A result subset cannot omit an available week participant. Keep this
	# fail-closed guard rather than manufacturing a smaller availability table.
	reason = Week._validate(Transaction._week_input(view), rules)
	return _mapped(view) if reason.is_empty() else _unsupported(reason)


static func merge_result(snapshot: Dictionary, result_after: Dictionary, rules: Dictionary) -> Dictionary:
	var reason := validate(snapshot, rules)
	if reason.is_empty():
		reason = Roles._validate_snapshot(result_after, true)
	if not reason.is_empty():
		return _unsupported(reason)
	var after := snapshot.duplicate(true)
	for key in SHARED + ["global_total_511c", "recipient_id"]:
		if not result_after.has(key):
			return _unsupported("missing_result_shared_field")
		after[key] = result_after[key].duplicate(true) if result_after[key] is Array or result_after[key] is Dictionary else result_after[key]
	var records := Roles._records(after)
	for row in result_after["characters"]:
		if not records.has(int(row["character_id"])):
			return _unsupported("unknown_result_catalog_id")
		for key in row:
			records[int(row["character_id"])][key] = row[key].duplicate(true) if row[key] is Array or row[key] is Dictionary else row[key]
	var relations := {}
	for relation in after["relationships"]:
		relations[int(relation["from"]) * 68 + int(relation["to"])] = relation
	for relation in result_after["relationships"]:
		var pair := int(relation["from"]) * 68 + int(relation["to"])
		if not relations.has(pair):
			return _unsupported("unknown_result_relation")
		relations[pair]["value"] = relation["value"]
	reason = validate(after, rules)
	return _mapped(after) if reason.is_empty() else _unsupported(reason)


static func merge_school(snapshot: Dictionary, school_after: Dictionary, rules: Dictionary) -> Dictionary:
	var reason := validate(snapshot, rules)
	if not reason.is_empty():
		return _unsupported(reason)
	if not school_after.get("participants") is Array or school_after["participants"].size() != snapshot["characters"].size() \
			or not school_after.get("adv_globals") is Dictionary \
			or not Week._bounded(school_after["adv_globals"].get("0x7e1180"), -1, 12):
		return _unsupported("invalid_school_catalog_or_alias")
	var after := snapshot.duplicate(true)
	var records := Roles._records(after)
	var seen := {}
	for row in school_after["participants"]:
		if not row is Dictionary or not Week._bounded(row.get("character_id"), 1, 12) \
				or not records.has(int(row["character_id"])) or seen.has(int(row["character_id"])):
			return _unsupported("missing_or_duplicate_school_catalog_id")
		seen[int(row["character_id"])] = true
		for key in RESULT_ONLY:
			if row.has(key):
				return _unsupported("school_view_cannot_replace_result_fields")
		for key in records[int(row["character_id"])]:
			if key in RESULT_ONLY:
				continue
			if not row.has(key):
				return _unsupported("missing_school_profile_field")
			records[int(row["character_id"])][key] = row[key].duplicate(true) if row[key] is Array or row[key] is Dictionary else row[key]
	for key in SHARED:
		if not school_after.has(key):
			return _unsupported("missing_school_shared_field")
		after[key] = school_after[key].duplicate(true) if school_after[key] is Array or school_after[key] is Dictionary else school_after[key]
	after["recipient_id"] = school_after["adv_globals"]["0x7e1180"]
	for key in after["school"]:
		if not school_after.has(key):
			return _unsupported("missing_school_metadata")
		after["school"][key] = school_after[key].duplicate(true) if school_after[key] is Array or school_after[key] is Dictionary else school_after[key]
	after["school"]["adv_globals"].erase("0x7e1180")
	reason = validate(after, rules)
	return _mapped(after) if reason.is_empty() else _unsupported(reason)


static func _mapped(snapshot: Dictionary) -> Dictionary:
	return {"supported": true, "snapshot": snapshot, "execution_scope": "layout_projection",
		"live_witness": false, "authorizes_persistent_write": false, "school_initialized": false}


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "live_witness": false,
		"authorizes_persistent_write": false, "school_initialized": false}
