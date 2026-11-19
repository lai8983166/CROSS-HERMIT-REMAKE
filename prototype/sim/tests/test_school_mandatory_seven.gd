extends "res://sim/tests/test_base.gd"
const Model := preload("res://sim/school_playground.gd")
const Earlier := preload("res://sim/tests/test_school_may_third_week.gd")
const UI := preload("res://sim/tests/test_school_combat_handoff.gd")


func _saves() -> Array:
	var weeks: Array=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://sim/tests/may_week3_saved_plans.json")))["cases"]
	var newest: Array=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://sim/tests/may_week4_saved_plans.json")))["cases"]
	var result := []
	for endpoint in newest:
		for row in weeks:
			if row["save"]["state_sha256"]!=endpoint["parent"]:continue
			var payload: Dictionary=row["save"].duplicate(true)
			payload["version"]=10
			payload["context"]="school_playground_may_week_four"
			payload["rules"]["may_week_four"]="9000c19fd20f9d7433e93e5cf9480d429bf6a15ae9e60bf10a4e26421c3fc80a"
			payload["state_sha256"]=endpoint["state_sha256"]
			payload["commands"]=Earlier.new()._save(row["parent_route"])["commands"]+payload["commands"]+endpoint["suffix"]
			result.append(payload)
	return result


func _deploy(ui, saved: Dictionary) -> Array:
	var restored: Dictionary=ui.model.restore(saved)
	assert_true(restored["supported"],str(restored))
	if not restored["supported"]:return []
	ui.refresh()
	var state: Dictionary=ui.model.read_postbattle()
	var expected := []
	var groups := []
	for group in range(2):
		for slot in range(4):
			var member := Model.Postbattle.Return.Groups._word(state["bundle"]["school"]["group_raw_bytes"],group*28+16+slot*2)
			if member>=0:
				expected.append(member)
				groups.append(group)
	var panel=ui.postbattle_panel
	assert_true(not panel.find_child("depart",true,false).disabled)
	panel.find_child("depart",true,false).pressed.emit()
	panel.commit_dialog.hide()
	panel.commit_dialog.confirmed.emit()
	assert_eq(ui.model.stage(),"sortie_pending")
	if ui.model.stage()!="sortie_pending":return []
	var pending: Dictionary=ui.model.read_postbattle()["planning"]["handoff"]
	var party: Dictionary=pending["prepared"]["rounds"][0]
	assert_eq(party["teacher_ids"],[101,110])
	assert_eq(party["student_ids"],expected)
	assert_eq(party["student_groups"],groups)
	assert_eq(ui.model.export_save()["version"],11)
	return expected


func test_all_saved_formations_can_depart_and_settle() -> void:
	var saves := _saves()
	assert_eq(saves.size(),4)
	for saved in saves:
		var ui=UI.new()._school_ui()
		var ids := _deploy(ui,saved)
		if ids.is_empty():
			ui.free()
			continue
		var view: Dictionary=ui.model.read_postbattle()
		var pending: Dictionary=view["planning"]
		var session := Model.Postbattle.SortieRecord.Sortie.new()
		assert_true(session.open(pending["handoff"]))
		assert_eq(session.controlled_units().map(func(unit):return unit["character_id"]),ids)
		session.close()
		var facts := preload("res://sim/tests/test_school_sortie_settlement.gd").new()._facts({"handoff":pending["handoff"]})
		facts["time_key"]=1
		var result := Model.Postbattle.SortieSettlement.apply(view["bundle"],pending["handoff"],facts,pending["opening_ledger"])
		assert_true(result["supported"],str(result))
		if result["supported"]:
			var summary: Dictionary=result["summary"]
			assert_eq(summary["history_index"],8)
			assert_eq(summary["students"].map(func(row):return row["character_id"]),ids)
			assert_true(summary["relationship_calls"].has({"from":8,"to":110,"delta":1}))
			assert_true(summary["relationship_calls"].has({"from":110,"to":8,"delta":1}))
		ui.free()


func _read_file(model) -> void:
	var path := "user://mandatory-seven-%s.json" % Time.get_ticks_usec()
	assert_true(model.save_file(path)["supported"])
	var copy := Model.new()
	var restored := copy.load_file(path)
	assert_true(restored["supported"],str(restored))
	assert_eq(copy.export_save(),model.export_save())
	assert_eq(copy.state(),model.state())
	DirAccess.remove_absolute(ProjectSettings.globalize_path(path))


func _return_and_replan(ui) -> void:
	var panel=ui.postbattle_panel
	var result: Dictionary=ui.model.read_postbattle()
	assert_eq(result["phase"],"sortie_result")
	assert_eq(result["planning"]["sortie_summary"]["scene_id"],7)
	assert_eq(result["planning"]["sortie_summary"]["history_index"],8)
	assert_false(ui.model.execute({"op":"return_depart"})["supported"])
	panel.find_child("continue_sortie_story",true,false).pressed.emit()
	var story: Dictionary=ui.model.read_postbattle()
	assert_eq(story["page"].get("chapter"),"030B")
	assert_eq(story["total"],71)
	assert_eq(story["bundle"]["school"]["student_count"],6)
	assert_eq(story["bundle"]["school"]["teacher_count"],3)
	if story["phase"]!="post_story":return
	panel.next.pressed.emit()
	_read_file(ui.model)
	panel.previous.pressed.emit()
	panel.skip_dialog.confirmed.emit()
	story=ui.model.read_postbattle()
	assert_eq(story["page"].get("chapter"),31)
	assert_eq(story["total"],55)
	if story["phase"]!="new_week_story":return
	panel.skip_dialog.confirmed.emit()
	panel.next.pressed.emit()
	story=ui.model.read_postbattle()
	assert_eq(story["phase"],"returned_school")
	if story["phase"]!="returned_school":return
	var school: Dictionary=story["bundle"]["school"]
	assert_eq([school["month"],school["week"]],[5,5])
	assert_eq(school["adventure_gate"],0)
	assert_false(Model.Postbattle.Adventures.available(story["planning"]["ledger"]).any(func(r):return r["id"]==7))
	for member in [115,6]:
		panel.find_child("member_%d" % member,true,false).pressed.emit()
		panel.assignments.get_child(2).get_child(1 if member==115 else 2).pressed.emit()
	for entry in [[1,17],[2,27]]:
		var mode=panel.find_child("mode_%d_1" % entry[0],true,false)
		assert_true(mode!=null)
		if mode==null:return
		mode.pressed.emit()
		var courses=panel.find_child("courses_%d" % entry[0],true,false)
		var index: int=courses.get_item_index(entry[1])
		assert_true(index>=0)
		if index<0:return
		courses.item_selected.emit(index)
		assert_eq(ui.model.export_save()["commands"][-1],{"op":"return_course","group":entry[0],"course":entry[1]})
	_read_file(ui.model)
	var altered: Dictionary=ui.model.export_save()
	altered["rules"]["mandatory_seven"]="changed"
	assert_eq(ui.model.restore(altered).get("reason"),"save_rules_changed")


func test_completed_escort_through_return_and_file_load() -> void:
	var example: Dictionary=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://sim/tests/mandatory_seven_escort_trace.json")))
	var matches := _saves().filter(func(payload):return payload["state_sha256"]==example["parent"])
	assert_eq(matches.size(),1)
	if matches.is_empty():return
	var ui=UI.new()._school_ui()
	var ids := _deploy(ui,matches[0])
	if ids.is_empty():
		ui.free()
		return
	var panel=ui.postbattle_panel
	var pending: Dictionary=ui.model.export_save()
	var pending_score: int=ui.model.read_postbattle()["bundle"]["school"]["global_total_511c"]
	var lower: Dictionary=pending.duplicate(true)
	for key in ["version","context","rules"]:lower[key]=matches[0][key]
	assert_eq(ui.model.restore(lower).get("reason"),"save_work_version_mismatch")
	panel.find_child("play_sortie",true,false).pressed.emit()
	var trial=ui.sortie_trial
	var battle=trial.session
	assert_true(battle.ready)
	if not battle.ready:
		ui.free()
		return
	assert_eq(battle.scene_id,7)
	assert_eq(battle.controlled_units().map(func(unit):return unit["character_id"]),ids)
	var run := Model.BattleRecord.run_trace(battle,example["trace"])
	assert_true(run["supported"],str(run))
	assert_true(battle.rendezvous)
	assert_eq(battle.ending_sub,8)
	assert_eq(battle.result_inputs()["time_key"],1)
	assert_eq(battle.battle_trace(),example["trace"])
	trial._refresh()
	trial.continue_button.pressed.emit()
	assert_eq(ui.model.stage(),"sortie_result")
	if ui.model.stage()=="sortie_result":
		var summary: Dictionary=ui.model.read_postbattle()["planning"]["sortie_summary"]
		assert_eq(summary["result_selector"],3)
		assert_eq(summary["score"]["total_after"]-summary["score"]["total_delta"],pending_score)
		assert_false(ui.model.execute({"op":"sortie_finish","trace":example["trace"]})["supported"])
		_return_and_replan(ui)
	ui.free()
