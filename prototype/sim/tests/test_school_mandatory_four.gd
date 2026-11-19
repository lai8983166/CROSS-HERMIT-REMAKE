extends "res://sim/tests/test_base.gd"
const Prior := preload("res://sim/tests/test_school_may_five_work.gd")
const Model := preload("res://sim/school_playground.gd")
const UI := preload("res://sim/tests/test_school_combat_handoff.gd")


func _saves() -> Array:
	var fixture: Dictionary = Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://sim/tests/june_week1_saved_plans.json")))
	var parent := Prior.new()._save()
	assert_eq(parent["state_sha256"], fixture["parent"])
	var result := []
	for row in fixture["cases"]:
		result.append({"version":fixture["version"], "context":fixture["context"], "rules":fixture["rules"],
			"commands":parent["commands"] + row["commands"], "state_sha256":row["state_sha256"]})
	return result


func _deploy(ui, saved: Dictionary) -> bool:
	var restored: Dictionary = ui.model.restore_text(JSON.stringify(saved))
	assert_true(restored["supported"], str(restored))
	if not restored["supported"]: return false
	assert_eq(ui.model.export_save(), saved)
	ui.refresh()
	var depart = ui.postbattle_panel.find_child("depart",true,false)
	assert_true(depart!=null and not depart.disabled)
	if depart==null or depart.disabled:return false
	depart.pressed.emit()
	ui.postbattle_panel.commit_dialog.hide()
	ui.postbattle_panel.commit_dialog.confirmed.emit()
	assert_eq(ui.model.stage(),"sortie_pending")
	return ui.model.stage()=="sortie_pending"


func test_deploy_prior_june_school_saves() -> void:
	var saves := _saves()
	assert_eq(saves.size(),3)
	for index in saves.size():
		var ui = UI.new()._school_ui()
		if _deploy(ui,saves[index]):
			var view: Dictionary = ui.model.read_postbattle()
			var handoff: Dictionary = view["planning"]["handoff"]
			var party: Dictionary = handoff["prepared"]["rounds"][0]
			assert_eq(party["scene_id"],4)
			assert_eq(party["teacher_ids"],[110,115] if index==1 else [101,110,115])
			assert_eq(party["student_ids"],[8,6,1] if index==1 else [3,8,6,1])
			assert_eq(party["student_groups"],[1,2,2] if index==1 else [0,1,2,2])
			var session := Model.Postbattle.SortieRecord.Sortie.new()
			assert_true(session.open(handoff))
			assert_eq(session.controlled_units().map(func(u):return u["character_id"]),party["student_ids"])
			session.close()
			assert_eq(ui.model.export_save()["version"],13)
			if index==0:
				var downgraded: Dictionary=ui.model.export_save()
				for key in ["version","context","rules"]: downgraded[key]=saves[index][key]
				assert_eq(ui.model.restore(downgraded).get("reason"),"save_work_version_mismatch")
				assert_eq(ui.model.stage(),"sortie_pending")
			assert_false(Model.Postbattle.Adventures.available(view["planning"]["ledger"]).any(func(r):return r["id"]==4))
		ui.free()


func test_victory_through_next_school_and_load() -> void:
	var example: Dictionary = Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://sim/tests/mandatory_four_victory_trace.json")))
	var saved: Dictionary = _saves()[0]
	assert_eq(example["parent"], saved["state_sha256"])
	var ui = UI.new()._school_ui()
	if not _deploy(ui,saved):
		ui.free()
		return
	var panel=ui.postbattle_panel
	var prior: Dictionary=ui.model.read_postbattle()["bundle"]
	panel.find_child("play_sortie",true,false).pressed.emit()
	var trial=ui.sortie_trial
	var battle=trial.session
	assert_true(battle.ready)
	if not battle.ready:
		ui.free()
		return
	var run := Model.BattleRecord.run_trace(battle,example["trace"])
	assert_true(run["supported"],str(run))
	assert_eq(battle.ending_sub,8)
	assert_true(battle.controlled_units().all(func(u):return u["limits"]["hp"]>0))
	assert_true(battle.enemies().is_empty())
	assert_eq(battle.result_inputs()["unit_condition_key"],2)
	assert_eq(battle.result_inputs()["time_key"],3)
	assert_eq(battle.battle_trace(),example["trace"])
	trial._refresh()
	trial.continue_button.pressed.emit()
	assert_eq(ui.model.stage(),"sortie_result")
	if ui.model.stage()=="sortie_result":
		var result: Dictionary=ui.model.read_postbattle()
		var summary: Dictionary=result["planning"]["sortie_summary"]
		assert_eq(summary["date"],[6,1])
		assert_eq(summary["scene_id"],4)
		assert_eq(summary["result_selector"],3)
		assert_eq(summary["history_index"],10)
		assert_eq(summary["students"].map(func(row):return row["character_id"]),[3,8,6,1])
		for id in [3,8,6,1]:
			assert_eq(Model.Postbattle.Return._find(result["bundle"]["records"],id)["week_records"].slice(30,33),[2,3,3])
		assert_eq(result["bundle"]["school"]["global_total_511c"],prior["school"]["global_total_511c"]+summary["score"]["total_delta"])
		assert_false(ui.model.execute({"op":"sortie_finish","trace":example["trace"]})["supported"])
		_return_and_replan(ui)
	ui.free()


func _return_and_replan(ui) -> void:
	var panel=ui.postbattle_panel
	panel.find_child("continue_sortie_story",true,false).pressed.emit()
	var view: Dictionary=ui.model.read_postbattle()
	assert_eq([view["page"].get("chapter"),view["total"]],[35,101])
	if view["phase"]!="post_story":return
	var skipped := Model.new()
	assert_true(skipped.restore(ui.model.export_save())["supported"])
	assert_true(skipped.execute({"op":"post_skip"})["supported"])
	for i in 80: assert_true(ui.model.execute({"op":"post_next"})["supported"])
	assert_eq(ui.model.read_postbattle()["bundle"]["school"]["student_count"],7)
	panel.next.pressed.emit()
	view=ui.model.read_postbattle()
	assert_eq(view["page"].get("chapter"),36)
	assert_eq(view["bundle"]["school"]["student_count"],8)
	panel.previous.pressed.emit()
	panel.next.pressed.emit()
	panel.skip_dialog.confirmed.emit()
	view=ui.model.read_postbattle()
	assert_eq([view["page"].get("chapter"),view["total"]],[37,150])
	assert_eq(view["bundle"],skipped.read_postbattle()["bundle"])
	panel.skip_dialog.confirmed.emit()
	assert_eq(ui.model.stage(),"post_workroom")
	panel.next.pressed.emit()
	view=ui.model.read_postbattle()
	assert_eq([view["page"].get("chapter"),view["total"]],[39,128])
	panel.skip_dialog.confirmed.emit()
	assert_eq(ui.model.stage(),"returned_school")
	if ui.model.stage()!="returned_school":return
	var school: Dictionary=ui.model.read_postbattle()["bundle"]["school"]
	assert_eq([school["month"],school["week"],school["lecture_work_fields"]],[6,2,[3,5,6,0]])
	assert_true(panel.find_child("adventure_6",true,false).button_pressed)
	panel.find_child("member_2",true,false).pressed.emit()
	panel.assignments.get_child(2).get_child(4).pressed.emit()
	assert_eq(ui.model.export_save()["commands"][-1],{"op":"return_move","kind":"student","member_id":2,"target_group":2,"target_slot":2})
	_check_file(ui.model)


func _check_file(model) -> void:
	var path := "user://mandatory-four-%s.json" % Time.get_ticks_usec()
	assert_true(model.save_file(path)["supported"])
	var fresh := Model.new()
	assert_true(fresh.load_file(path)["supported"])
	assert_eq(fresh.state(),model.state())
	assert_eq(fresh.export_save(),model.export_save())
	DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	var altered: Dictionary = fresh.export_save()
	altered["rules"]["mandatory_four"]="changed"
	assert_eq(fresh.restore(altered).get("reason"),"save_rules_changed")
