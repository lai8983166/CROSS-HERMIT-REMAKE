extends "res://sim/tests/test_base.gd"
const Plans := preload("res://sim/tests/test_school_return_planning.gd")
const UIHelpers := preload("res://sim/tests/test_school_combat_handoff.gd")
const Model := preload("res://sim/school_playground.gd")


func test_played_sortie_result_story_planning_and_version_seven_restore() -> void:
	var model=Plans.new()._returned()
	for id in [4,9]:
		assert_true(model.execute({"op":"return_move","kind":"student","member_id":id,
			"target_group":-1,"target_slot":-1})["supported"])
	for command in [{"op":"return_plan"},{"op":"return_select","adventure":8},{"op":"return_depart"}]:
		assert_true(model.execute(command)["supported"])
	var ui=UIHelpers.new()._school_ui()
	assert_true(ui.model.restore(model.export_save())["supported"])
	ui.refresh()
	var panel=ui.postbattle_panel
	panel.find_child("play_sortie",true,false).pressed.emit()
	var battle=ui.sortie_trial.session
	while battle._ending_phase=="opening": ui.sortie_trial._continue()
	assert_true(battle.command_attack(3,1231))
	for i in range(610): battle.tick()
	for i in range(4): battle.advance_exit()
	ui.sortie_trial._refresh()
	assert_eq(battle.ending_sub,14)
	assert_eq(ui.sortie_trial.continue_button.text,"确认战果")
	var trace: Dictionary=battle.battle_trace()
	ui.sortie_trial.continue_button.pressed.emit()
	assert_eq(ui.model.stage(),"sortie_result")
	if ui.model.stage()!="sortie_result":
		ui.free()
		return
	assert_false(ui.sortie_trial.visible)
	var receipt: Dictionary=ui.model.read_postbattle()["planning"]["sortie_summary"]
	assert_eq(receipt["recipient"],3)
	assert_eq(receipt["scene_id"],8)
	assert_eq(receipt["result_selector"],5)
	assert_eq(receipt["students"].size(),1)
	assert_eq(ui.model.export_save()["version"],7)
	_check_save(ui.model)
	assert_false(ui.model.execute({"op":"sortie_finish","trace":trace})["supported"])
	panel.find_child("continue_sortie_story",true,false).pressed.emit()
	assert_eq(ui.model.read_postbattle()["page"]["chapter"],23)
	for op in ["post_next","post_prev","post_skip"]:
		assert_true(ui.model.execute({"op":op})["supported"])
	assert_eq(ui.model.read_postbattle()["page"]["chapter"],24)
	_check_save(ui.model)
	for op in ["post_skip","post_school"]:
		assert_true(ui.model.execute({"op":op})["supported"])
	ui.refresh()
	assert_eq(ui.model.stage(),"returned_school")
	assert_eq(ui.model.read_postbattle()["bundle"]["school"]["week"],2)
	assert_true(panel.heading.text.contains("第2周"))
	assert_true(panel.find_child("adventure_8",true,false)==null)
	assert_true(panel.find_child("adventure_17",true,false)!=null)
	panel.find_child("mode_0_1",true,false).pressed.emit()
	var courses=panel.find_child("courses_0",true,false)
	courses.item_selected.emit(courses.get_item_index(3))
	_check_save(ui.model)
	var saved: Dictionary=ui.model.export_save()
	for mutate in [
		func(s):s["commands"].filter(func(c):return c["op"]=="sortie_finish")[0]["trace"]["ticks"]=0,
		func(s):s["commands"].append({"op":"sortie_finish","trace":trace}),
		func(s):s["rules"]["sortie_rewards"]="changed",
		func(s):s["commands"].filter(func(c):return c["op"]=="sortie_finish")[0]["reward"]=1]:
		var bad := saved.duplicate(true)
		mutate.call(bad)
		assert_false(ui.model.restore(bad)["supported"])
		assert_eq(ui.model.export_save(),saved)
	ui.free()


func _check_save(model) -> void:
	var restored := Model.new()
	assert_true(restored.restore_text(JSON.stringify(model.export_save()))["supported"])
	assert_eq(restored.state(),model.state())


func test_four_student_training_record_continues_to_second_week() -> void:
	var model=Plans.new()._returned()
	for command in [{"op":"return_plan"},{"op":"return_move","kind":"student","member_id":5,
			"target_group":0,"target_slot":3},{"op":"return_select","adventure":17},{"op":"return_depart"}]:
		assert_true(model.execute(command)["supported"])
	# Captured through the normal three opening confirmations and one move order.
	var trace := {"version":1,"commands":[[0,1,1],[0,1,1],[0,1,1],[0,3,3,90,15]],
		"ticks":3052,"overflow":false}
	var finished: Dictionary=model.execute({"op":"sortie_finish","trace":trace})
	assert_true(finished["supported"],str(finished))
	if not finished["supported"]: return
	for op in ["post_next","post_skip","post_skip","post_school"]:
		assert_true(model.execute({"op":op})["supported"])
	var view: Dictionary=model.read_postbattle()
	assert_eq(view["planning"]["sortie_summary"]["students"].size(),4)
	assert_eq(view["bundle"]["school"]["lecture_work_fields"][2],17)
	_check_save(model)
