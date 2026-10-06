extends RefCounted
## 4A2BA0 / 4A24A0 的独立数据操作，不发布会话或存档。

const SOURCE_SHA := "588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005"
const TEMPLATE_SHA := "cf7c1a6b640a930e9ce9ccafd339c93ad4178d6683013d8163c9aa77bfdab890"
const RULE_FIELDS := ["work_id","month","week","metadata","category","key"]


static func unlock_courses(before: Dictionary, rules: Dictionary) -> Dictionary:
	if not _rules_valid(rules):
		return _result(false,"unsupported_course_rules")
	if not _state_valid(before):
		return _result(false,"invalid_course_state")
	var pending: Array = []
	var counts: Array = before["course_counts"].duplicate()
	var stamp: int = before["month"] * 6 + before["week"]
	for template in rules["templates"]:
		var identity: int = template["work_id"]
		if before["course_unlocked_flags"][identity] != 0:
			continue
		if template["month"] * 6 + template["week"] > stamp:
			continue
		if template["category"] == 0 or template["key"] == 0:
			continue
		pending.append(template)
		for teacher in range(20):
			if template["teacher_mask"][teacher] != 0:
				counts[teacher] += 1
				if counts[teacher] > 100:
					return _result(false,"course_capacity_exceeded")
	var after := before.duplicate(true)
	var buffers: Array = []
	for teacher in range(20):
		var rows: Array = []
		for slot in range(100):
			rows.append([slot,0,0,0,0,0,0,0])
		for row in before["course_buffers"][teacher]:
			rows[row[0]] = row.duplicate()
		buffers.append(rows)
	var unlocked: Array = []
	for template in pending:
		var identity: int = template["work_id"]
		for teacher in range(20):
			if template["teacher_mask"][teacher] == 0:
				continue
			var count: int = after["course_counts"][teacher]
			var rows: Array = buffers[teacher]
			for slot in range(count,0,-1):
				# Defined fields move; physical opaque bytes at indices6/7 do not.
				for field in range(1,6):
					rows[slot][field] = rows[slot-1][field]
			rows[0][1] = 1
			rows[0][2] = 0
			rows[0][3] = identity
			rows[0][4] = template["metadata"]
			rows[0][5] = 0
			after["course_counts"][teacher] = count + 1
		after["course_unlocked_flags"][identity] = 1
		unlocked.append(identity)
	for teacher in range(20):
		var sparse: Array = []
		for row in buffers[teacher]:
			if _nonzero(row):
				sparse.append(row)
		after["course_buffers"][teacher] = sparse
	var result := _result(true,"unlocked" if not unlocked.is_empty() else "unchanged")
	result["after"] = after
	result["unlocked_work_ids"] = unlocked
	return result


static func _integer(value: Variant, low: int, high: int) -> bool:
	return value is int and value >= low and value <= high


static func _array(value: Variant, size: int) -> bool:
	return value is Array and value.size() == size


static func _nonzero(row: Array) -> bool:
	for field in range(1,8):
		if row[field] != 0:
			return true
	return false


static func _rules_valid(rules: Dictionary) -> bool:
	if rules.get("source_image_sha256") != SOURCE_SHA or rules.get("template_fields_sha256") != TEMPLATE_SHA:
		return false
	if not _array(rules.get("templates"),100):
		return false
	var encoded := ""
	for index in range(100):
		var template: Variant = rules["templates"][index]
		if not template is Dictionary:
			return false
		if not _integer(template.get("work_id"),index+1,index+1):
			return false
		if not _integer(template.get("month"),0,255) or not _integer(template.get("week"),0,255):
			return false
		for key in ["metadata","category","key"]:
			if not _integer(template.get(key),-32768,32767):
				return false
		if not _array(template.get("teacher_mask"),20):
			return false
		var fields := PackedStringArray()
		for key in RULE_FIELDS:
			fields.append(str(template[key]))
		for byte in template["teacher_mask"]:
			if not _integer(byte,0,255):
				return false
			fields.append(str(byte))
		encoded += ":".join(fields) + ";"
	return encoded.sha256_text() == TEMPLATE_SHA


static func _state_valid(before: Dictionary) -> bool:
	if not _integer(before.get("month"),0,255) or not _integer(before.get("week"),0,5):
		return false
	if not _array(before.get("course_unlocked_flags"),101) or not _array(before.get("course_counts"),20) or not _array(before.get("course_buffers"),20):
		return false
	for flag in before["course_unlocked_flags"]:
		if not _integer(flag,0,255):
			return false
	for teacher in range(20):
		if not _integer(before["course_counts"][teacher],0,100):
			return false
		var rows: Variant = before["course_buffers"][teacher]
		if not rows is Array or rows.size() > 100:
			return false
		var previous := -1
		for row in rows:
			if not _array(row,8) or not _integer(row[0],previous+1,99):
				return false
			previous = row[0]
			for field in [1,2,6,7]:
				if not _integer(row[field],0,255):
					return false
			for field in [3,4,5]:
				if not _integer(row[field],-32768,32767):
					return false
			if not _nonzero(row):
				return false
	return true


static func _result(supported: bool, reason: String) -> Dictionary:
	return {"supported":supported,"reason":reason,"school_initialized":false,
		"interactive_school_ready":false,"live_witness":false,"authorizes_persistent_write":false}
