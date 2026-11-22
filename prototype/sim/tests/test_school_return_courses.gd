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


func test_june_five_lessons_match_original_growth_and_skill_draws() -> void:
	# Original 4C0400, one independent call per new dated course. The common
	# input is student 3 from the first existing settlement case, coefficient 60.
	var cases := [
		[8,[0,2750,0,0,2750,0,2750,0],[15,14,27,35,61,29,67],[]],
		[19,[0,0,6600,0,0,1650,0,0],[15,13,28,35,61,29,67],[]],
		[20,[0,0,6600,0,0,1650,0,0],[15,13,28,35,61,29,67],[17]],
		[26,[0,0,0,0,0,0,0,27500],[15,13,27,35,61,29,67],[8]],
		[28,[1650,1650,1650,1650,1650,1650,1650,1650],[15,13,27,35,61,29,67],[8]],
		[29,[0,0,0,0,30250,0,0,0],[15,13,27,35,62,29,67],[33]]]
	_assert_original_lesson_vectors(Courses.lesson_rules(6),cases)


func test_august_four_lessons_match_original_growth_and_skill_draws() -> void:
	assert_eq(Courses.lesson_rules(8,3)["training"].size(),30)
	var cases := [
		[30,[0,0,0,0,8250,0,1650,0],[15,13,27,35,61,29,67],[64]],
		[33,[1100,1100,1100,1100,1100,1100,1100,1100],[15,13,27,35,61,29,67],[8]]]
	_assert_original_lesson_vectors(Courses.lesson_rules(8,4),cases)


func test_september_one_lessons_match_original_growth_and_skill_draws() -> void:
	var cases := [
		[7,[0,0,0,0,6600,0,3300,0],[15,13,27,35,61,29,67],[]],
		[19,[0,0,6600,0,0,1650,0,0],[15,13,28,35,61,29,67],[]],
		[24,[0,0,0,6600,0,0,1650,0],[15,13,27,35,61,29,67],[]],
		[30,[0,0,0,0,8250,0,1650,0],[15,13,27,35,61,29,67],[64]],
		[36,[13750,0,0,0,0,0,0,0],[20,13,27,35,61,29,67],[8]]]
	_assert_original_lesson_vectors(Courses.lesson_rules(9,1),cases)


func _assert_original_lesson_vectors(rules: Dictionary, cases: Array) -> void:
	var data: Dictionary=Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_settlement_evidence_v1.json")))
	var case: Dictionary=data["cases"][0]
	assert_false(rules.is_empty())
	if rules.is_empty():return
	for row in cases:
		var bundle := {"growth":[case["before_records"][0]],"school":{"difficulty":case["before"]["difficulty"],"global_total_511c":0,"member_profiles":[]}}
		var result := Courses.apply_lessons(bundle,[{"character_id":3,"training_id":row[0],"coefficient":60}],rules,4660)
		assert_eq(result["packets"][0]["packet"],row[1])
		assert_eq(result["students"][0]["attributes"],row[2])
		assert_eq(result["students"][0]["new_skill_ids"],row[3])
		assert_eq([result["students"][0]["level"],result["learning_draws"].size(),result["rand_state"]],[31,7,1896039533])


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


func test_third_week_new_courses_preserve_history_and_bonus_only_recipient() -> void:
	var calendar := preload("res://sim/school_sortie_week.gd")
	var adventures := preload("res://sim/school_return_adventures.gd")
	var course := Courses.settle(_planned())
	var ledger := adventures.initial()
	var school: Dictionary
	for week in [1,2]:
		var opening := ledger
		ledger=adventures.advance(ledger,0)
		var room := calendar.finish_story(calendar.next_week(course["after"])["after"])
		school=calendar.school_return(room["after"],ledger,opening)["after"]
		if week==1:course=Courses.settle(school)
	for work in [6,7]:
		var assigned := Courses.assign_course(school,0,work)
		assert_true(assigned["supported"],str(assigned.get("reason")))
		if not assigned["supported"]:continue
		var result := Courses.settle(assigned["after"])
		assert_true(result["supported"],str(result.get("reason")))
		if not result["supported"]:continue
		var after: Dictionary=result["after"]
		var summary: Dictionary=result["summary"]
		assert_eq(summary["date"],[5,3])
		assert_eq(summary["history_index"],7)
		assert_true(not summary["learning_draws"].is_empty())
		assert_eq(after["item_flags"],school["item_flags"])
		for i in range(4):
			assert_eq(after["records"][i]["week_records"].slice(0,21),school["records"][i]["week_records"].slice(0,21))
			assert_eq(after["records"][i]["week_records"][21],1)
			assert_eq(after["records"][i]["week_records"].slice(24),school["records"][i]["week_records"].slice(24))
		if work==6:
			assert_true(summary["bonus"]>0)
			assert_eq(summary["recipient"],-1)
			assert_eq(summary["mvp_script"],"")
			assert_eq(after["counts"],school["counts"])
			for i in range(4):
				assert_eq(after["growth"][i]["growth_pools"],school["growth"][i]["growth_pools"])
		else:
			assert_true(summary["recipient"] in [3,4,9,5])
			assert_eq(summary["bonus"],0)
			for packet in summary["packets"]:
				assert_true(packet["packet"][4]>0 and packet["packet"][6]>0)


func test_third_week_original_instruction_packets_and_draws() -> void:
	# Declared 5/3, initial students 3/4/9, seed 4660. Original 4C0400
	# runs both assignments in sequence on the same growth records.
	var fixture: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_settlement_evidence_v1.json")))
	var records: Array = fixture["cases"][0]["before_records"]
	var rules: Dictionary = Courses._rules()["growth"]
	for work in [6,7]:
		var plan := []
		for id in [3,4,9]:
			plan.append({"character_id":id,"training_id":work,"coefficient":65})
		var growth := Courses._grow(records,plan,rules,fixture["cases"][0]["before"]["difficulty"],4660)
		for event in growth["packets"]:
			assert_eq(event["packet"],[0,0,0,0,0,0,0,23000] if work==6 else [0,0,0,0,6900,0,3450,0])
		assert_eq(growth["bonus"],69000 if work==6 else 0)
		assert_eq(growth["learning_draws"].size(),22)
		assert_eq(growth["rand_state"],1174792322)
		records=growth["records"]


func test_saved_course_keeps_its_identity_when_the_menu_row_moves() -> void:
	var school: Dictionary = _planned(10).school
	var rules := Courses._rules()
	var original := Courses._plan(school,rules)
	assert_true(original.supported)
	Groups._put_word(school.group_raw_bytes,12,Groups._word(school.group_raw_bytes,12)+1)
	var retained := Courses._plan(school,rules)
	assert_true(retained.supported)
	if retained.supported:
		assert_eq(retained.plan,original.plan)
	Groups._put_word(school.group_raw_bytes,8,99)
	assert_false(Courses._plan(school,rules).supported)
