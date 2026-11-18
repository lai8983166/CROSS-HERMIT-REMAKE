extends "res://sim/tests/test_base.gd"
const Settlement := preload("res://sim/school_sortie_settlement.gd")
const Fixtures := preload("res://sim/tests/test_school_return_courses.gd")
const Adventures := preload("res://sim/school_return_adventures.gd")
const Return := preload("res://sim/school_postbattle_return.gd")


func _departure(scene: int, four: bool) -> Dictionary:
	var bundle := Fixtures.new()._returned()
	if four:
		bundle = Return.move_member(bundle,{"kind":"student","member_id":5,"target_group":0,"target_slot":3})["after"]
	var ledger := Adventures.initial()
	bundle = Adventures.select(bundle,ledger,scene)["after"]
	return Adventures.submit(bundle,ledger)


func _facts(departure: Dictionary) -> Dictionary:
	var prepared: Dictionary = departure["handoff"]["prepared"]
	var units := []
	for id in prepared["rounds"][0]["student_ids"]:
		units.append({"character_id":id,"count_field_aa":1,"contribution_field_ac":5,"status_field_ae":0})
	var slots := []; slots.resize(16); slots.fill(0); slots[0]=1
	return {"scene_id":prepared["adventure_id"],"units":units,"objective_slots":slots,"time_key":0,
		"unit_condition_key":2,"result_selector":1,"clock_seed":4660,"growth_seed":4660}


func test_each_task_score_loot_growth_mvp_history_and_waiting() -> void:
	for scene in [8,17]:
		var departure := _departure(scene,scene==8)
		var before: Dictionary = departure["after"]
		var saved := before.duplicate(true)
		var facts := _facts(departure)
		var result := Settlement.apply(before,departure["handoff"],facts)
		assert_true(result["supported"],str(result.get("reason")))
		if not result["supported"]: continue
		var after: Dictionary = result["after"]
		var summary: Dictionary = result["summary"]
		assert_eq(before,saved)
		assert_eq(summary["score"]["time_display"],4)
		assert_eq(summary["score"]["unit_display"],0 if scene==8 else 2)
		assert_eq(summary["students"].size(),4 if scene==8 else 3)
		assert_eq(after["school"]["global_total_511c"]-before["school"]["global_total_511c"],summary["score"]["total_delta"])
		assert_true(after["school"]["global_total_511c"] > before["school"]["global_total_511c"])
		var earned := []
		for row in summary["loot_groups"]:
			for item in row:
				if item>0:
					earned.append(item)
					assert_eq(before["item_flags"][item-1]&1,0)
					assert_eq(after["item_flags"][item-1]&1,1)
		# Verified with original 4BD210/4BCA40/4BBD40 instructions using
		# these same 5/1 records, current inventory, task ID and declared seed.
		assert_eq(earned,[113,86,17,6,1,11,23,24,9] if scene==8 else [56,61,36,41,30,25,11,23,24,9])
		assert_eq(summary["score"]["total_delta"],151200 if scene==8 else 114300)
		assert_eq(summary["students"].map(func(row):return row["staged_total"]),
			[145200,151200,157200,151200] if scene==8 else [109800,114300,118800])
		for i in range(360):
			if (before["item_flags"][i]&1)!=0: assert_eq(after["item_flags"][i],before["item_flags"][i])
		for i in range(4):
			var id: int = before["growth"][i]["character_id"]
			var assigned: bool = scene==8 or id!=5
			assert_eq(after["records"][i]["week_records"][15],2 if assigned else 3)
			if assigned:
				assert_true(after["growth"][i]["growth_pools"]!=before["growth"][i]["growth_pools"])
			else:
				assert_eq(after["growth"][i]["growth_pools"],before["growth"][i]["growth_pools"])
			assert_eq(after["counts"][i]["count"],mini(5,before["counts"][i]["count"]+int(id==summary["recipient"])))
		assert_true(after["school"]["relationships"]!=before["school"]["relationships"])
		assert_eq(after["phase"],"sortie_settled")
		assert_false(Settlement.apply(after,departure["handoff"],facts)["supported"])
		assert_eq(Settlement.apply(before,departure["handoff"],facts)["after"],after)


func test_reject_stale_handoff_mismatched_roster_and_unconfigured_objective() -> void:
	var departure := _departure(17,true)
	var facts := _facts(departure)
	var stale: Dictionary = departure["handoff"].duplicate(true)
	stale["growth"][0]["growth_pools"][0]+=1
	assert_false(Settlement.apply(departure["after"],stale,facts)["supported"])
	facts["units"].reverse()
	assert_false(Settlement.apply(departure["after"],departure["handoff"],facts)["supported"])
	facts=_facts(departure); facts["objective_slots"][3]=1
	assert_false(Settlement.apply(departure["after"],departure["handoff"],facts)["supported"])


func test_second_training_uses_saved_best_grade_and_current_inventory() -> void:
	var calendar := preload("res://sim/school_sortie_week.gd")
	var first := _departure(17,true)
	var first_result := Settlement.apply(first["after"],first["handoff"],_facts(first))
	var week := calendar.next_week(first_result["after"])
	var room := calendar.finish_story(week["after"])
	var school := calendar.school_return(room["after"],first["ledger_after"])
	var opening: Dictionary=school["ledger_after"]
	var second := Adventures.submit(school["after"],opening)
	assert_false(Settlement.apply({"phase":"sortie_committed"},second["handoff"],{})["supported"])
	var bad: Dictionary=second["after"].duplicate(true)
	bad["sortie_result"]=null
	assert_false(Settlement.apply(bad,second["handoff"],{},opening)["supported"])
	var facts := _facts(second)
	facts["result_selector"]=5
	assert_false(Settlement.apply(second["after"],second["handoff"],facts,Adventures.initial())["supported"])
	var result := Settlement.apply(second["after"],second["handoff"],facts,opening)
	assert_true(result["supported"],str(result.get("reason")))
	if not result["supported"]:return
	assert_eq(result["summary"]["result_selector"],5)
	assert_eq(result["summary"]["task_grade"],1)
	assert_eq(result["summary"]["history_index"],6)
	for i in range(360):
		if (school["after"]["item_flags"][i]&1)!=0:
			assert_true((result["after"]["item_flags"][i]&1)!=0)
	for i in range(4):
		assert_eq(result["after"]["records"][i]["week_records"].slice(15,18),first_result["after"]["records"][i]["week_records"].slice(15,18))
