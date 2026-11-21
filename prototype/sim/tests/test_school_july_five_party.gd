extends "res://sim/tests/test_base.gd"
const Campaign := preload("res://sim/tests/test_school_july_five_work.gd")
const Settlement := preload("res://sim/school_sortie_settlement.gd")
const Adventures := Settlement.Adventures
const Return := Settlement.Return
const PARTY := [3,16,4,8,17,6,2,5,9,1]
static var source := {}


func _opening() -> Dictionary:
	if not source.is_empty():return source
	var model:=Campaign.Model.new()
	var restored:=model.restore(Campaign.new()._save())
	assert_true(restored.supported,str(restored))
	if not restored.supported:return {}
	var view:=model.read_postbattle()
	source={"bundle":view.bundle,"ledger":view.planning.ledger,"grades":model._postbattle._task_grades.duplicate()}
	return source


func _settle_party(only_recruits: bool) -> Dictionary:
	var opening:=_opening()
	if opening.is_empty():return {}
	var bundle: Dictionary=opening.bundle.duplicate(true)
	if only_recruits:
		for id in PARTY:
			if id in [16,17]:continue
			var moved:=Return.move_member(bundle,{"kind":"student","member_id":id,"target_group":-1,"target_slot":-1})
			assert_true(moved.supported,str(moved))
			if not moved.supported:return {}
			bundle=moved.after
		for teacher in [115,118]:
			var moved:=Return.move_member(bundle,{"kind":"teacher","member_id":teacher,"target_group":-1,"target_slot":-1})
			assert_true(moved.supported,str(moved.get("reason")))
			if not moved.supported:return {}
			bundle=moved.after
	for group in range(2 if only_recruits else 4):
		var changed:=Settlement.Courses.set_mode(bundle,group,false)
		assert_true(changed.supported,str(changed.get("reason")))
		if not changed.supported:return {}
		bundle=changed.after
	var selected:=Adventures.select(bundle,opening.ledger,17)
	assert_true(selected.supported,str(selected.get("reason")))
	if not selected.supported:return {}
	var ready:=Adventures.submit(selected.after,opening.ledger)
	assert_true(ready.supported,str(ready.get("reason")))
	if not ready.supported:return {}
	var ids: Array=ready.handoff.prepared.rounds[0].student_ids
	assert_eq(ids,[16,17] if only_recruits else PARTY)
	var slots: Array=[]
	slots.resize(16)
	slots.fill(0)
	var facts:={"scene_id":17,"result_selector":3,"time_key":0,"unit_condition_key":1,"objective_slots":slots,
		"clock_seed":4660,"growth_seed":4660,"units":[]}
	for id in ids:
		facts.units.append({"character_id":id,"count_field_aa":10 if id==16 else 0,
			"contribution_field_ac":1000 if id==16 else 0,"status_field_ae":0})
	var result:=Settlement.apply(ready.after,ready.handoff,facts,opening.ledger,opening.grades)
	assert_true(result.supported,str(result.get("reason")))
	return result if result.supported else {}


func test_ten_students_grow_and_mvp_uses_only_original_eligible_ids() -> void:
	var result:=_settle_party(false)
	if result.is_empty():return
	var summary: Dictionary=result.summary
	assert_eq(summary.students.map(func(row):return row.character_id),PARTY)
	assert_eq(summary.lessons.students,[])
	var best:=0
	var winner:=-1
	for row in summary.students:
		assert_eq(Return._find(result.after.records,row.character_id).week_records[57],2)
		if row.character_id<13 and row.staged_total>best:
			best=row.staged_total
			winner=row.character_id
	assert_true(best>0)
	assert_true(Return._find(summary.students,16).staged_total>best)
	assert_eq(summary.recipient,winner)
	for id in [16,17]:
		assert_eq(Return._find(result.after.counts,id),Return._find(source.bundle.counts,id))


func test_only_new_students_get_growth_and_no_mvp() -> void:
	var result:=_settle_party(true)
	if result.is_empty():return
	assert_eq(result.summary.students.map(func(row):return row.character_id),[16,17])
	assert_eq([result.summary.recipient,result.summary.old_mvp_count,result.summary.mvp_script],[-1,0,"allresult/dat/nomvp.ybc"])
	assert_eq(result.after.counts,source.bundle.counts)
	assert_eq(result.after.phase,"sortie_settled")
	assert_eq(result.summary.adv_request.script,"adv/dat/ch003.ybc")
