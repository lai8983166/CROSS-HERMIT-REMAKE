extends "res://sim/tests/test_base.gd"
const Model := preload("res://sim/school_playground.gd")
const PostTests := preload("res://sim/tests/test_school_postbattle_flow.gd")
const UIHelpers := preload("res://sim/tests/test_school_combat_handoff.gd")


func _returned():
	var model=PostTests.new()._begin()
	for op in ["post_skip","post_skip","post_school"]:assert_true(model.execute({"op":op})["supported"])
	return model


func _roundtrip(model) -> void:
	var restored := Model.new()
	assert_true(restored.restore_text(JSON.stringify(model.export_save()))["supported"])
	assert_eq(restored.state(),model.state())
	if restored.stage()=="sortie_pending":
		var battle=load("res://sim/school_sortie_session.gd").new()
		var before: Dictionary=restored.export_save()
		assert_true(battle.open(restored.read_postbattle()["planning"]["handoff"]))
		assert_eq(battle.controlled_units().map(func(u):return u["character_id"]),[3,4,9,5])
		battle.close();assert_eq(restored.export_save(),before)


func test_v6_current_plans_course_commit_and_old_v5_restore() -> void:
	var model=_returned();var old: Dictionary=model.export_save()
	assert_eq(old["version"],5)
	# Exported by unchanged parent c2edbe4, then restored by this implementation.
	assert_eq(old["state_sha256"],"38e6ac062c037c68b2a40cecd6c7853cebf3356d37805ebadeb55abb5eaf1cdc")
	assert_true(model.execute({"op":"return_plan"})["supported"])
	assert_eq(model.export_save()["version"],6)
	assert_true(model.execute({"op":"return_move","kind":"student","member_id":5,"target_group":0,"target_slot":3})["supported"])
	assert_true(model.execute({"op":"return_mode","group":0,"teaching":true})["supported"])
	assert_true(model.execute({"op":"return_course","group":0,"course":4})["supported"])
	_roundtrip(model)
	assert_false(model.execute({"op":"return_depart"})["supported"])
	assert_true(model.execute({"op":"return_settle"})["supported"])
	assert_eq(model.stage(),"course_result")
	var snapshot: Dictionary=model.read_postbattle()
	assert_eq(snapshot["planning"]["course_summary"]["students"].size(),4)
	assert_eq(snapshot["planning"]["ledger"]["entries"].map(func(r):return r["elapsed"]),[1,3])
	_roundtrip(model)
	var final: Dictionary=model.state()
	for op in ["return_plan","return_settle","return_depart","post_school"]:assert_false(model.execute({"op":op})["supported"])
	assert_eq(model.state(),final)
	assert_true(model.restore(old)["supported"])
	assert_eq(model.export_save(),old);assert_eq(model.stage(),"returned_school")
	assert_false(model.read_postbattle().has("planning"))


func test_sortie_is_saved_once_with_selected_current_members_and_tampering_rejected() -> void:
	var model=_returned();var old: Dictionary=model.export_save()
	for id in [8,17]:
		assert_true(model.restore(old)["supported"])
		for command in [{"op":"return_plan"},{"op":"return_select","adventure":id},
			{"op":"return_move","kind":"student","member_id":5,"target_group":0,"target_slot":3},
			{"op":"return_depart"}]:assert_true(model.execute(command)["supported"])
		assert_eq(model.stage(),"sortie_pending")
		assert_eq(model.read_postbattle()["planning"]["handoff"]["prepared"]["adventure_id"],id)
		_roundtrip(model)
		var valid: Dictionary=model.export_save();var current: Dictionary=model.state()
		for mutate in [func(s):s["state_sha256"]="0".repeat(64),
			func(s):s["commands"].append({"op":"return_depart"}),
			func(s):s["rules"]["return_adventures"]="changed",
			func(s):s["commands"][-1]={"op":"return_select","adventure":5},
			func(s):s["commands"][-1]["reward"]=100]:
			var bad := valid.duplicate(true);mutate.call(bad)
			assert_false(model.restore(bad)["supported"]);assert_eq(model.state(),current)
		assert_false(model.execute({"op":"return_settle"})["supported"])


func test_controls_course_selection_and_both_explicit_commit_dialogs() -> void:
	var ui=UIHelpers.new()._school_ui();var model=_returned()
	assert_true(ui.model.restore(model.export_save())["supported"]);ui.refresh()
	var panel=ui.postbattle_panel
	panel.find_child("plan_start",true,false).pressed.emit()
	assert_eq(ui.model.export_save()["version"],6)
	panel.find_child("mode_0_1",true,false).pressed.emit()
	var option=panel.find_child("courses_0",true,false)
	assert_eq(option.item_count,9)
	option.item_selected.emit(option.get_item_index(3))
	assert_false(panel.find_child("settle",true,false).disabled)
	assert_true(panel.find_child("depart",true,false).disabled)
	panel.find_child("settle",true,false).pressed.emit()
	assert_true(panel.commit_dialog.visible);assert_eq(ui.model.stage(),"returned_school")
	panel.commit_dialog.hide();panel.commit_dialog.canceled.emit()
	assert_eq(ui.model.stage(),"returned_school");assert_eq(panel._pending,{})
	panel.find_child("settle",true,false).pressed.emit()
	panel.commit_dialog.hide();panel.commit_dialog.confirmed.emit()
	assert_eq(ui.model.stage(),"course_result");assert_true(panel.speaker.text.contains("授课已结算"))
	assert_true(ui.model.restore(model.export_save())["supported"]);ui.refresh()
	panel.find_child("plan_start",true,false).pressed.emit()
	panel.find_child("adventure_17",true,false).pressed.emit()
	assert_false(panel.find_child("depart",true,false).disabled)
	panel.find_child("depart",true,false).pressed.emit()
	assert_eq(ui.model.stage(),"returned_school")
	panel.commit_dialog.hide();panel.commit_dialog.confirmed.emit()
	assert_eq(ui.model.stage(),"sortie_pending");assert_true(panel.dialogue.text.contains("进入本次任务的战场"))
	assert_false(panel.next.visible)
	var before: Dictionary=ui.model.export_save()
	panel.find_child("play_sortie",true,false).pressed.emit()
	assert_true(ui.sortie_trial.visible);assert_false(panel.visible)
	assert_eq(ui.sortie_trial.session.scene_id,17)
	ui.sortie_trial.close_trial()
	for i in range(4):ui.sortie_trial.session.advance_exit()
	ui.sortie_trial._continue()
	assert_false(ui.sortie_trial.visible);assert_true(panel.visible)
	assert_eq(ui.model.export_save(),before)
	ui.free()
