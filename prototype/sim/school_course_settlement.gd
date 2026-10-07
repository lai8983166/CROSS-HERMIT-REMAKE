extends RefCounted
## Source4A6A10/4C0400/4D3600 growth only; no confirmation, calendar or saves.

const Origin := preload("res://sim/new_game_school_origin.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")
const Teacher := preload("res://sim/school_teacher_movement.gd")
const Courses := preload("res://sim/school_course_unlocking.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const FIELDS_SHA := "efd978e3a123b14d3c3a470a2b63965a9c709689760ea526c61126bf6931ddb0"
const RULE_KEYS := ["attribute_increments","level_thresholds","skill_grid","job_skill_caps","skills","training"]


static func source_subset(input: Dictionary) -> Dictionary:
	return Origin.field_subset(input,["source_image_sha256","settlement_fields_sha256"] + RULE_KEYS)


static func valid_rules(input: Dictionary) -> bool:
	if input.get("source_image_sha256") != Courses.SOURCE_SHA or input.get("settlement_fields_sha256") != FIELDS_SHA:
		return false
	for pair in [["attribute_increments",136],["level_thresholds",50],["skill_grid",12],["job_skill_caps",31],["skills",84],["training",16]]:
		if not input.get(pair[0]) is Array or input[pair[0]].size() != pair[1]:
			return false
	for row in input["skill_grid"]:
		if not Origin._vector(row,7,0,84):
			return false
	for row in input["job_skill_caps"]:
		if not Origin._vector(row,11,0,11):
			return false
	for row in input["skills"]:
		if not row is Dictionary or row.keys() != ["minimum_attributes","minimum_total","minimum_job_sums","learned_points"] \
				or not Origin._vector(row["minimum_attributes"],7,0,135) or not Origin._vector(row["minimum_job_sums"],5,0,32767) \
				or not Courses._integer(row["minimum_total"],0,945) or not Courses._integer(row["learned_points"],0,0x7fffffff):
			return false
	for row in input["training"]:
		if not row is Dictionary or row.keys() != ["package","attribute_mask","learning_rates"] \
				or not Origin._vector(row["package"],8,-0x7fffffff,0x7fffffff) \
				or not Origin._vector(row["attribute_mask"],7,0,32767) or not Origin._vector(row["learning_rates"],11,0,100):
			return false
	var values := []
	for key in RULE_KEYS:
		if not input.get(key) is Array:
			return false
		if not _flatten(input[key],values):
			return false
	var fields := PackedStringArray()
	for value in values:
		fields.append(str(value))
	return ":".join(fields).sha256_text() == FIELDS_SHA


static func _flatten(value: Variant, output: Array) -> bool:
	if value is Array:
		for item in value:
			if not _flatten(item,output):
				return false
	elif value is Dictionary:
		for key in value:
			if not _flatten(value[key],output):
				return false
	elif value is int:
		output.append(value)
	else:
		return false
	return true


static func initial_records(origin_rules: Dictionary, rules: Dictionary) -> Dictionary:
	if not valid_rules(source_subset(rules)) or rules.get("initial_job_sums_sha256") != "849c03029ed1a9d94af1f0d69bd01b11a1eebaaba7705cdf1aa4c80beccd82c7" \
			or not rules.get("initial_job_sums") is Array or rules["initial_job_sums"].size() != 3:
		return Origin.failure("invalid_course_growth_origin")
	var values := []
	for index in range(3):
		var row: Variant = rules["initial_job_sums"][index]
		if not row is Dictionary or not Courses._integer(row.get("character_id"),[3,4,9][index],[3,4,9][index]) \
				or not Origin._vector(row.get("job_sums"),5,0,600):
			return Origin.failure("invalid_course_growth_origin")
		values.append(str(row["character_id"]))
		for value in row["job_sums"]:
			values.append(str(value))
	if ":".join(PackedStringArray(values)).sha256_text() != rules["initial_job_sums_sha256"]:
		return Origin.failure("invalid_course_growth_origin")
	var initialized := Origin.construct(origin_rules)
	if not initialized["supported"]:
		return initialized
	var result := []
	for index in range(3):
		var seed: Dictionary = origin_rules["student_level_inputs"][index]
		var profile: Dictionary = initialized["after"]["member_profiles"][index+1]
		var statuses: Array = seed["skill_statuses"].duplicate()
		for sid in seed["equipped_skills"]:
			if sid > 0:
				statuses[sid-1] = 6
		var job_sums: Array = rules["initial_job_sums"][index]["job_sums"].duplicate()
		result.append({"character_id":seed["member_id"],"job":profile["job"],
			"attributes":profile["attributes"].duplicate(),"growth_pools":seed["growth_pools"].duplicate(),
			"level_50":profile["level_50"],"skill_statuses":statuses,"job_sums":job_sums,"staged_total":0})
	return {"supported":true,"records":result}


static func settle(before: Dictionary, records: Array, rules: Dictionary, work_rules: Dictionary, seed: Variant = 4660) -> Dictionary:
	rules = source_subset(rules)
	if not valid_rules(rules):
		return Origin.failure("invalid_course_settlement_rules")
	if not Courses._integer(seed,0,0x7fffffff):
		return Origin.failure("invalid_declared_clock_seed")
	var rated := Groups.rate(before,Origin.group_rules())
	if not rated["supported"]:
		return rated
	var reason := _validate_records(before,records,rules)
	if not reason.is_empty():
		return Origin.failure(reason)
	var working := _working(rated["after"])
	var plan := []
	for group in range(5):
		var rating: Dictionary = rated["ratings"][group]
		var slots: Array = rated["after"]["derived_student_ids"][group]
		var populated := false
		for identity in slots:
			populated = populated or identity >= 0
		if not populated:
			continue
		if rating["state"] != 4:
			return Origin.failure("class_not_ready_for_course_settlement")
		var work_id: int = rating["work_fields"][2]
		if work_id not in [10,11,12]:
			return Origin.failure("outside_declared_course_growth_subset")
		var selected := Teacher.select_group(working,group,Origin.group_rules(),work_rules)
		if not selected["supported"]:
			return selected
		var matching := false
		var category: int = rating["work_fields"][0]
		if category < 0 or category > 2:
			return Origin.failure("invalid_course_work_fields")
		for row in selected["after"]["work_rows"][category]:
			if row == [rating["work_fields"][1],work_id,rating["work_fields"][3]]:
				matching = true
		if not matching:
			return Origin.failure("course_settlement_unavailable_or_stale")
		for identity in slots:
			if identity >= 0:
				plan.append({"character_id":identity,"training_id":work_id,"coefficient":rating["relationship_mean"]})
	if plan.is_empty():
		return Origin.failure("no_course_students")
	var after: Array = records.duplicate(true)
	var indexed := {}
	for record in after:
		indexed[record["character_id"]] = record
	var state: int = seed
	var draws := []
	var packets := []
	var bonus := 0
	var skill_display := 0
	var cap := _pool_cap(before["difficulty"],rules)
	for command in plan:
		var record: Dictionary = indexed[command["character_id"]]
		var packet := _packet(record,rules["training"][command["training_id"]]["package"],command["coefficient"],cap,rules)
		bonus += packet[7]
		var packet_event: Dictionary = command.duplicate()
		packet_event["packet"] = packet.duplicate()
		packets.append(packet_event)
		record["staged_total"] = 0
		for k in range(7):
			record["growth_pools"][k] += packet[k]
			record["staged_total"] += packet[k]
		# Native checks old attribute bytes before their post-growth recalculation.
		for category in range(11):
			var count: int = rules["job_skill_caps"][record["job"]][category]
			for ordinal in range(count):
				var sid: int = rules["skill_grid"][category][ordinal]
				if record["skill_statuses"][sid-1] != 0:
					continue
				var rate: int = rules["training"][command["training_id"]]["learning_rates"][category]
				if rate != 100:
					state = (state * 214013 + 2531011) & 0xffffffff
					var draw := (state >> 16) & 32767
					draws.append(draw)
					if draw % 101 > rate:
						break
				var skill: Dictionary = rules["skills"][sid-1]
				var capable := true
				var total := 0
				for k in range(7):
					total += record["attributes"][k]
					if record["attributes"][k] < skill["minimum_attributes"][k]:
						capable = false
				if total < skill["minimum_total"]:
					capable = false
				# 4C0400's job-sum loop does not change its capability flag.
				if capable:
					record["skill_statuses"][sid-1] = 2
					skill_display = 1
				break
		for k in range(7):
			record["attributes"][k] = _attribute(record["growth_pools"][k],rules["attribute_increments"])
		record["level_50"] = _level(_total(record,rules),rules["level_thresholds"])
	var result := Origin.success("course_growth_projected")
	result.merge({"records":after,"packets":packets,"learning_draws":draws,"rand_state":state,
		"bonus":bonus,"global_total_511c":clampi(before["global_total_511c"] + bonus,0,999999999),
		"skill_display_needed":skill_display,"declared_clock_seed":seed})
	return result


static func _packet(record: Dictionary, base: Array, coefficient: int, cap: int, rules: Dictionary) -> Array:
	var remaining := maxi(0,8500000 - _total(record,rules))
	var raw_total := 0
	var bonus := 0
	var packet := []
	for k in range(8):
		var amount: int = base[k]
		if amount > 0:
			amount = _div(_div(amount * (coefficient + 50),100) * 50,100)
		if k == 7:
			packet.append(amount + bonus)
			continue
		raw_total += amount
		if remaining - raw_total < 0:
			var available := amount + remaining - raw_total
			var overflow := amount
			if available < 0:
				amount = 0
			else:
				overflow = amount - available
				amount = available
			bonus += _div(overflow,2)
		else:
			var available: int = cap - record["growth_pools"][k]
			if available < amount:
				bonus += _div(amount - available,2)
				amount = available
		packet.append(amount)
	return packet


static func _div(value: int, divisor: int) -> int:
	return int(value / divisor)


static func _total(record: Dictionary, rules: Dictionary) -> int:
	var total := 0
	for pool in record["growth_pools"]:
		total += pool
	for sid in range(84):
		if record["skill_statuses"][sid] in [3,5,6]:
			total += rules["skills"][sid]["learned_points"]
	return total


static func _attribute(pool: int, increments: Array) -> int:
	var cumulative := 0
	for level in range(1,136):
		cumulative += increments[level]
		if cumulative > pool:
			return maxi(1,level-1)
	return 135


static func _level(total: int, thresholds: Array) -> int:
	var level := 2
	while level < 51 and thresholds[level-1] <= total:
		level += 1
	return level-1


static func _pool_cap(difficulty: int, rules: Dictionary) -> int:
	var total := 0
	for k in range(1,101 if difficulty in [0,1] else 136):
		total += rules["attribute_increments"][k]
	return total


static func _validate_records(before: Dictionary, records: Array, rules: Dictionary) -> String:
	if records.size() != 3 or not before.get("member_profiles") is Array or before["member_profiles"].size() != 4 \
			or not Courses._integer(before.get("difficulty"),0,2) or not Courses._integer(before.get("global_total_511c"),0,999999999) \
			or not before.get("course_buffers") is Array \
			or before["course_buffers"].size() != 20:
		return "invalid_course_growth_records"
	for buffer in before["course_buffers"]:
		if not buffer is Array:
			return "invalid_course_growth_buffers"
		for row in buffer:
			if not row is Array or row.size() != 8:
				return "invalid_course_growth_buffers"
	var cap := _pool_cap(before["difficulty"],rules)
	for index in range(3):
		var record: Variant = records[index]
		if not record is Dictionary or not Courses._integer(record.get("character_id"),[3,4,9][index],[3,4,9][index]):
			return "invalid_course_growth_identity"
		for spec in [["job",1,30],["level_50",0,50],["staged_total",0,0x7fffffff]]:
			if not Courses._integer(record.get(spec[0]),spec[1],spec[2]):
				return "invalid_course_growth_scalar"
		for spec in [["attributes",7,1,135],["growth_pools",7,0,cap],["skill_statuses",84,0,6],["job_sums",5,-768,762]]:
			if not Origin._vector(record.get(spec[0]),spec[1],spec[2],spec[3]):
				return "invalid_course_growth_vector"
		if not before["member_profiles"][index+1] is Dictionary:
			return "invalid_course_growth_profile"
		var profile: Dictionary = before["member_profiles"][index+1]
		if profile.get("member_id") != record["character_id"] or profile.get("job") != record["job"] \
				or profile.get("level_50") != record["level_50"] or profile.get("attributes") != record["attributes"]:
			return "stale_course_growth_profile"
		for k in range(7):
			if _attribute(record["growth_pools"][k],rules["attribute_increments"]) != record["attributes"][k]:
				return "inconsistent_course_growth_pool"
	return ""


static func _working(before: Dictionary) -> Dictionary:
	var result := before.duplicate(true)
	result["teacher_work_records"] = {"101":[]}
	for row in before.get("course_buffers",[[]])[0]:
		result["teacher_work_records"]["101"].append({"slot":row[0],"enabled":row[1],"blocked":row[2],"work_id":row[3]})
	return result
