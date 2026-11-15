extends "res://sim/tests/test_base.gd"
const Courses := preload("res://sim/school_return_courses.gd")
const Return := preload("res://sim/school_postbattle_return.gd")
const ReturnTests := preload("res://sim/tests/test_school_postbattle_return.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")


func _returned() -> Dictionary:
	var joined := Return.join(ReturnTests.new()._bundle())
	var week := Return.next_week(joined["after"])
	return Return.school_return(week["after"])["after"]


func _planned(work := 1, all_four := true) -> Dictionary:
	var bundle := _returned()
	if all_four: bundle=Return.move_member(bundle,{"kind":"student","member_id":5,"target_group":0,"target_slot":3})["after"]
	bundle=Courses.set_mode(bundle,0,true)["after"]
	var result := Courses.assign_course(bundle,0,work)
	assert_true(result["supported"],str(result.get("reason")))
	return result.get("after",{})


func test_new_and_existing_original_instruction_growth_oracles() -> void:
	var rules := Courses._rules()
	assert_false(rules.is_empty())
	for path in ["res://data/school_course_settlement_evidence_v1.json","res://data/school_return_courses_source.json"]:
		var raw: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
		assert_true(raw is Dictionary,"missing source oracle "+path)
		if not raw is Dictionary: continue
		var data: Dictionary = Roles._integers(raw)
		for row in data["cases"]:
			var plan := []
			for packet in row["packets"]:
				plan.append({"character_id":packet["character_id"],"training_id":packet["training_id"],"coefficient":packet["coefficient"]})
			var result := Courses._grow(row["before_records"],plan,rules["growth"],row.get("difficulty",row.get("before",{}).get("difficulty",0)),row["declared_clock_seed"])
			for key in ["packets","learning_draws","rand_state","bonus","skill_display_needed"]:
				assert_eq(result[key],row[key],row["name"]+" "+key)
			assert_eq(result["records"],row["after_records"],row["name"]+" complete growth")


func test_all_eight_current_courses_use_current_four_member_growth() -> void:
	var listed := Courses.list_courses(_returned(),0)
	assert_true(listed["supported"],str(listed.get("reason")))
	var ids := []
	for category in listed["courses"]:
		for row in category: ids.append(row[1])
	ids.sort()
	assert_eq(ids,[1,2,3,4,5,10,11,12])
	for work in ids:
		var before := _planned(work)
		var original := before.duplicate(true)
		var result := Courses.settle(before)
		assert_true(result["supported"],"work%d %s" % [work,str(result.get("reason"))])
		if not result["supported"]: continue
		var after: Dictionary = result["after"]
		assert_eq(result["summary"]["students"].map(func(r):return r["character_id"]),[3,4,9,5])
		assert_eq(after["phase"],"courses_confirmed")
		assert_eq([after["school"]["month"],after["school"]["week"]],[5,1])
		assert_eq(after["school"]["group_raw_bytes"],before["school"]["group_raw_bytes"],"plan preserved")
		assert_eq(after["flags"],before["flags"])
		assert_eq(after["item_flags"],before["item_flags"])
		assert_eq(after["school"]["global_total_511c"],before["school"]["global_total_511c"]+result["summary"]["bonus"])
		for index in range(4):
			var growth: Dictionary = after["growth"][index]
			var packet: Array = result["summary"]["packets"][index]["packet"]
			for k in range(7): assert_eq(growth["growth_pools"][k],before["growth"][index]["growth_pools"][k]+packet[k])
			assert_eq(after["records"][index]["week_records"].slice(0,15),before["records"][index]["week_records"].slice(0,15),"earlier history retained")
			assert_eq(after["records"][index]["week_records"].slice(18),before["records"][index]["week_records"].slice(18))
			assert_eq(after["records"][index]["week_records"][15],1)
			for key in Return.GROWTH_KEYS: assert_eq(after["participants"][index][key],growth[key],"participant synced")
			assert_eq(after["participants"][index]["job_progress"],after["records"][index]["job_progress"].slice(0,31))
			assert_eq(after["participants"][index]["equipped_items"],before["participants"][index]["equipped_items"])
		assert_eq(before,original,"input remains owned")
		assert_eq(Courses.settle(before),result,"deterministic source seed")


func test_waiting_growth_and_history_bytes_survive_confirmation() -> void:
	var before := _planned(1,false)
	before=Return.move_member(before,{"kind":"student","member_id":9,"target_group":-1,"target_slot":-1})["after"]
	for id in [9,5]:
		Return._find(before["growth"],id)["staged_total"]=2147480000
		var record := Return._find(before["records"],id)
		record["week_records"][16]=42;record["week_records"][17]=43
	Return._sync_participants(before)
	var result := Courses.settle(before)
	assert_true(result["supported"],str(result.get("reason")))
	if not result["supported"]: return
	assert_true(result["summary"]["recipient"] in [3,4],"stale waiting totals cannot win MVP")
	var after: Dictionary = result["after"]
	assert_eq(after["school"]["idle_student_ids"],before["school"]["idle_student_ids"])
	for id in [9,5]:
		var prior := Return._find(before["growth"],id)
		var current := Return._find(after["growth"],id)
		for key in Return.GROWTH_KEYS:
			if key!="job_sums": assert_eq(current[key],prior[key],"waiting growth "+key)
		var old := Return._find(before["records"],id)
		var record := Return._find(after["records"],id)
		assert_eq(record["week_records"].slice(15,18),[3,42,43])
		assert_eq(record["job_progress"][current["job"]],mini(99,old["job_progress"][current["job"]]+1))
	assert_true(result["summary"]["relationship_calls"].has({"from":9,"to":3,"delta":-1}))
	assert_false(result["summary"]["relationship_calls"].has({"from":3,"to":9,"delta":-1}))


func test_confirmation_and_mvp_are_once_only_and_deep_owned() -> void:
	var before := _planned(10)
	var result := Courses.settle(before)
	assert_true(result["supported"],str(result.get("reason")))
	if not result["supported"]: return
	var after: Dictionary = result["after"]
	var duplicate := Courses.settle(after)
	assert_true(duplicate["supported"],str(duplicate.get("reason")))
	assert_eq(duplicate["status"],"duplicate")
	assert_eq(duplicate["after"],after)
	assert_false(Courses.settle(after,1)["supported"])
	assert_false(Courses.assign_course(after,0,1)["supported"])
	assert_false(Courses.set_mode(after,0,false)["supported"])
	for row in after["counts"]:
		var old := Return._find(before["counts"],row["character_id"])
		assert_eq(row["count"],mini(5,old["count"]+1) if row["character_id"]==result["summary"]["recipient"] else old["count"])
	duplicate["after"]["growth"][0]["growth_pools"][0]=-1
	assert_true(after["growth"][0]["growth_pools"][0]>=0)


func test_plan_replay_from_json_commands_is_exact_and_has_no_rewards() -> void:
	var start := _returned()
	var commands := [{"mode":true},{"course":5},{"mode":false},{"mode":true},{"course":2}]
	var after := start.duplicate(true)
	var replay := start.duplicate(true)
	for command in commands:
		after=(Courses.set_mode(after,0,command["mode"]) if command.has("mode") else Courses.assign_course(after,0,command["course"]))["after"]
	var decoded: Array = Roles._integers(JSON.parse_string(JSON.stringify(commands)))
	for command in decoded:
		replay=(Courses.set_mode(replay,0,command["mode"]) if command.has("mode") else Courses.assign_course(replay,0,command["course"]))["after"]
	assert_eq(after,replay)
	for key in ["growth","records","counts","participants","flags","item_flags"]: assert_eq(after[key],start[key],key)
	assert_eq([after["school"]["month"],after["school"]["week"]],[5,1])
	assert_eq(Courses.settle(after),Courses.settle(replay),"saved plan settles identically")


func test_invalid_input_and_adventure_mode_refuse_atomically() -> void:
	var before := _planned()
	for mutate in [func(b):b["school"]["month"]=4,func(b):b["growth"].pop_back(),
		func(b):b["school"]["member_profiles"][1]["attributes"][0]+=1,
		func(b):b["records"][3]["week_records"]=[],func(b):b["school"]["relationships"].pop_back(),
		func(b):b["school"]["group_raw_bytes"][3]=0,func(b):b["school"]["group_raw_bytes"][10]=9,
		func(b):b["growth"][0]["growth_pools"][0]+=100000]:
		var bad := before.duplicate(true)
		mutate.call(bad)
		var copy := bad.duplicate(true)
		var result := Courses.settle(bad)
		assert_false(result["supported"])
		assert_false(result.has("after"))
		assert_eq(bad,copy)
	assert_false(Courses.settle(before,4660.0)["supported"])
	assert_false(Courses.assign_course(before,0,9)["supported"])
	assert_false(Courses.assign_course(before,1,1)["supported"])
	var adventure := Courses.set_mode(before,0,false)
	assert_true(adventure["supported"])
	assert_false(Courses.settle(adventure["after"])["supported"])
	assert_false(Courses.assign_course(adventure["after"],0,1)["supported"])
	var gated := before.duplicate(true)
	gated["school"]["adventure_gate"]=1
	var forced := Courses.set_mode(gated,0,true)
	assert_true(forced["supported"])
	if forced["supported"]:
		assert_eq(forced["after"]["school"]["group_raw_bytes"][3],0)
		assert_false(Courses.settle(forced["after"])["supported"])


func test_relocated_class_has_same_course_growth_and_slot_order_mvp() -> void:
	var before := _planned(10)
	var moved: Dictionary = Return.move_member(before,{"kind":"teacher","member_id":101,"target_group":4,"target_slot":-1})["after"]
	for index in range(4):
		moved=Return.move_member(moved,{"kind":"student","member_id":[3,4,9,5][index],"target_group":4,"target_slot":index})["after"]
	moved=Courses.set_mode(moved,4,true)["after"]
	moved=Courses.assign_course(moved,4,10)["after"]
	var first := Courses.settle(before)
	var second := Courses.settle(moved)
	assert_true(first["supported"] and second["supported"])
	if not first["supported"] or not second["supported"]: return
	for key in ["growth","records","counts","participants"]: assert_eq(first["after"][key],second["after"][key],key)
	assert_eq(first["summary"],second["summary"])
