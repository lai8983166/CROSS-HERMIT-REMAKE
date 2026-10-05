extends RefCounted
## Isolated original teacher registration, group cleanup and defined rating fields.
## Does not insert Chapter012 into the campaign or accept interactive assignments.

const Week = preload("res://sim/week_settlement_replay.gd")
const SOURCE_SHA := "588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005"
const CHAPTER_SHA := "dfbdb1dc1f197f2d198a9d6b71e68c12d8f8f7fb72d1b2a4328f8f164affd5cf"
const TEACHERS := [117, 118]


static func register_teacher(before: Dictionary, context: Dictionary, rules: Dictionary) -> Dictionary:
	var reason := _validate(before, rules)
	if not reason.is_empty():
		return _unsupported(reason)
	if context.get("kind") not in ["chapter012_prefix", "direct_helper"] \
			or not Week._bounded(context.get("teacher_id"), 117, 117) \
			or not Week._bounded(context.get("group"), -1, 4) \
			or not Week._bounded(context.get("slot"), -1, -1):
		return _unsupported("outside_teacher_join_context")
	var group := int(context["group"])
	if context["kind"] == "chapter012_prefix" and group != -1:
		return _unsupported("source_opcode_has_no_placement")
	var after := before.duplicate(true)
	if int(before["availability"][117]) == 1:
		return _view(after, "already_available")
	if group >= 0 and _word(before["group_raw_bytes"], group * 28) != -1:
		return _unsupported("outside_empty_teacher_placement")
	var count := int(after["teacher_count"])
	after["teacher_ids"][count] = 117
	after["teacher_count"] = count + 1
	after["availability"][117] = 1
	if group >= 0:
		_put_word(after["group_raw_bytes"], group * 28, 117)
		after["derived_teacher_ids"][group] = 117
		after["derived_teacher_indices"][group] = count
	return _view(after, "registered_once")


static func reconcile(before: Dictionary, rules: Dictionary) -> Dictionary:
	var reason := _validate(before, rules)
	if not reason.is_empty():
		return _unsupported(reason)
	var after := before.duplicate(true)
	var raw: Array = after["group_raw_bytes"]
	var reset := int(before["reset_groups"]) != 0
	after["reset_groups"] = 0
	var students: Array = after["student_ids"].slice(0, int(after["student_count"]))
	var teachers: Array = after["teacher_ids"].slice(0, int(after["teacher_count"]))
	var selected := false
	for group in range(5):
		var base := group * 28
		if reset:
			raw[base + 3] = 1
			raw[base + 4] = 255
			_put_word(raw, base + 6, -1)
			_put_word(raw, base + 8, -1)
		var teacher := _word(raw, base)
		if not _available(after, teacher):
			_put_word(raw, base, -1)
			raw[base + 3] = 1
			after["derived_teacher_ids"][group] = -1
			after["derived_teacher_indices"][group] = -1
		else:
			teachers.erase(teacher)
			if not selected:
				after["selected_group"] = group
				selected = true
			if reset:
				# 4A5F40's later unconditional write wins even with adventure_gate.
				raw[base + 3] = 0
	for group in range(5):
		var base := group * 28
		raw[base + 14] = 0
		for slot in range(4):
			var offset := base + 16 + slot * 2
			var identity := _word(raw, offset)
			if not _available(after, identity) or _word(raw, base) == -1 or not students.has(identity):
				_put_word(raw, offset, -1)
				after["derived_student_ids"][group][slot] = -1
				after["derived_student_indices"][group][slot] = -1
			else:
				students.erase(identity)
				raw[base + 14] = int(raw[base + 14]) + 1
	after["idle_student_ids"] = students
	after["idle_teacher_ids"] = teachers
	return _view(after, "reconciled")


static func rate(before: Dictionary, rules: Dictionary) -> Dictionary:
	var reason := _validate(before, rules)
	if not reason.is_empty():
		return _unsupported(reason)
	var after := before.duplicate(true)
	var pairs := {}
	for row in before["relationships"]:
		pairs[_pair(row["from"], row["to"])] = int(row["value"])
	var ratings := []
	var seen_students := {}
	for group in range(5):
		var base := group * 28
		var raw: Array = before["group_raw_bytes"]
		var teacher := _word(raw, base)
		after["derived_teacher_ids"][group] = -1
		after["derived_teacher_indices"][group] = -1
		after["derived_student_ids"][group] = [-1, -1, -1, -1]
		after["derived_student_indices"][group] = [-1, -1, -1, -1]
		var members := []
		if teacher != -1:
			if not _available(before, teacher):
				return _unsupported("pending_group_reconciliation")
			members.append(teacher)
			after["derived_teacher_ids"][group] = teacher
			after["derived_teacher_indices"][group] = before["teacher_ids"].find(teacher)
		for slot in range(4):
			var identity := _word(raw, base + 16 + slot * 2)
			if identity == -1:
				continue
			if teacher == -1 or not _available(before, identity) or seen_students.has(identity):
				return _unsupported("pending_group_reconciliation")
			seen_students[identity] = true
			members.append(identity)
			after["derived_student_ids"][group][slot] = identity
			after["derived_student_indices"][group][slot] = before["student_ids"].find(identity)
		var rating := {"state": 0 if teacher == -1 else 1, "relationship_mean": 0,
			"relationship_rank": 0, "work_fields": []}
		if members.size() > 1:
			var total := 0
			var count := 0
			for a in members:
				for b in members:
					if a == b:
						continue
					if not pairs.has(_pair(a, b)):
						return _unsupported("missing_group_relationship")
					total += pairs[_pair(a, b)]
					count += 1
			rating["relationship_mean"] = int(float(total) / float(count))
			rating["relationship_rank"] = 1
			for threshold in rules["relationship_thresholds"]:
				if rating["relationship_mean"] >= int(threshold):
					rating["relationship_rank"] += 1
			if int(raw[base + 3]) == 1:
				rating["state"] = 5 if _word(raw, base + 8) < 0 else 4
				if rating["state"] == 4:
					for offset in [6, 8, 10, 12]:
						rating["work_fields"].append(_word(raw, base + offset))
			else:
				rating["state"] = 2 if int(before["lecture_active"]) != 0 else 3
				if rating["state"] == 2:
					rating["work_fields"] = before["lecture_work_fields"].duplicate()
		ratings.append(rating)
	var result := _view(after, "rated")
	result["ratings"] = ratings
	return result


static func _validate(before: Dictionary, rules: Dictionary) -> String:
	if rules.get("source_image_sha256") != SOURCE_SHA or rules.get("chapter_sha256") != CHAPTER_SHA \
			or rules.get("teacher_id") != 117 or rules.get("script_file_offset") != 20 \
			or rules.get("opcode") != 144 or rules.get("relationship_thresholds") != [16, 31, 46, 61, 76, 91]:
		return "invalid_teacher_group_rules"
	if not Week._vector(before.get("availability"), 121, 0, 1) \
			or not Week._vector(before.get("group_raw_bytes"), 140, 0, 255):
		return "invalid_school_group_buffers"
	var present := {}
	for spec in [["student", 12], ["teacher", 2]]:
		var prefix: String = spec[0]
		var ids: Variant = before.get(prefix + "_ids")
		if not Week._bounded(before.get(prefix + "_count"), 0, spec[1]) or not ids is Array or ids.size() != 20:
			return "invalid_school_roster"
		for index in range(20):
			var identity: Variant = ids[index]
			if not Week._integer(identity):
				return "invalid_school_roster_identity"
			if index >= int(before[prefix + "_count"]):
				if int(identity) != -1:
					return "invalid_school_roster_tail"
			elif not _domain(identity, prefix == "teacher") or present.has(int(identity)):
				return "unsupported_or_duplicate_school_identity"
			else:
				present[int(identity)] = true
	for identity in range(121):
		if int(before["availability"][identity]) != (1 if present.has(identity) else 0):
			return "school_roster_availability_mismatch"
	for spec in [["reset_groups", 0, 1], ["adventure_gate", 0, 1], ["lecture_active", 0, 1], ["selected_group", -1, 4]]:
		if not Week._bounded(before.get(spec[0]), spec[1], spec[2]):
			return "invalid_school_group_control"
	if not Week._vector(before.get("lecture_work_fields"), 4, -32768, 32767):
		return "invalid_lecture_work_fields"
	if not _matrix(before.get("derived_student_ids"), 5, 4, -1, 12) \
			or not _matrix(before.get("derived_student_indices"), 5, 4, -1, 19) \
			or not Week._vector(before.get("derived_teacher_ids"), 5, -1, 118) \
			or not Week._vector(before.get("derived_teacher_indices"), 5, -1, 19):
		return "invalid_school_derived_buffers"
	for id in before["derived_teacher_ids"]:
		if int(id) != -1 and not _domain(id, true):
			return "invalid_derived_teacher"
	for pair in [["idle_student_ids", false], ["idle_teacher_ids", true]]:
		if not before.get(pair[0]) is Array or before[pair[0]].size() > 20:
			return "invalid_school_waiting_buffer"
		for identity in before[pair[0]]:
			if not _domain(identity, pair[1]):
				return "invalid_school_waiting_identity"
	var teachers := {}
	for group in range(5):
		var raw: Array = before["group_raw_bytes"]
		var base := group * 28
		var teacher := _word(raw, base)
		if teacher != -1:
			if not _domain(teacher, true) or teachers.has(teacher):
				return "unsupported_or_duplicate_group_teacher"
			teachers[teacher] = true
		if int(raw[base + 3]) not in [0, 1]:
			return "invalid_school_activity_mode"
		for slot in range(4):
			var identity := _word(raw, base + 16 + slot * 2)
			if identity != -1 and not _domain(identity, false):
				return "unsupported_group_student"
	if not before.get("relationships") is Array:
		return "missing_school_relationships"
	var pairs := {}
	for row in before["relationships"]:
		if not row is Dictionary or not _identity(row.get("from")) or not _identity(row.get("to")) \
				or row["from"] == row["to"] or not Week._bounded(row.get("value"), 1, 100):
			return "invalid_school_relationship"
		var key := _pair(row["from"], row["to"])
		if pairs.has(key):
			return "duplicate_school_relationship"
		pairs[key] = true
	return ""


static func _available(snapshot: Dictionary, identity: int) -> bool:
	return identity >= 0 and identity < 121 and int(snapshot["availability"][identity]) == 1


static func _identity(identity: Variant) -> bool:
	return _domain(identity, false) or _domain(identity, true)


static func _domain(identity: Variant, teacher: bool) -> bool:
	return Week._integer(identity) and (int(identity) in TEACHERS if teacher else int(identity) >= 1 and int(identity) <= 12)


static func _pair(a: Variant, b: Variant) -> int:
	# Same external-to-matrix mapping as native4D3A20.
	var row := int(a) - 55 if int(a) > 100 else int(a)
	var column := int(b) - 55 if int(b) > 100 else int(b)
	return row * 68 + column


static func _word(raw: Array, offset: int) -> int:
	var word := int(raw[offset]) | (int(raw[offset + 1]) << 8)
	return word - 65536 if word >= 32768 else word


static func _put_word(raw: Array, offset: int, value: int) -> void:
	raw[offset] = value & 255
	raw[offset + 1] = (value >> 8) & 255


static func _matrix(value: Variant, rows: int, columns: int, minimum: int, maximum: int) -> bool:
	if not value is Array or value.size() != rows:
		return false
	for row in value:
		if not Week._vector(row, columns, minimum, maximum):
			return false
	return true


static func _view(after: Dictionary, status: String) -> Dictionary:
	return {"supported": true, "status": status, "after": after, "execution_scope": "isolated_teacher_group_data",
		"school_initialized": false, "interactive_school_ready": false, "live_witness": false,
		"authorizes_persistent_write": false}


static func _unsupported(reason: String) -> Dictionary:
	return {"supported": false, "reason": reason, "school_initialized": false,
		"interactive_school_ready": false, "live_witness": false, "authorizes_persistent_write": false}
