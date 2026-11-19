extends "res://sim/tests/test_base.gd"
const Model := preload("res://sim/school_playground.gd")
const Previous := preload("res://sim/tests/test_school_mandatory_seven.gd")
const UI := preload("res://sim/tests/test_school_combat_handoff.gd")


func _save() -> Dictionary:
	var fixture: Dictionary=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://sim/tests/may_week5_saved_plan.json")))
	var escort: Dictionary=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://sim/tests/mandatory_seven_escort_trace.json")))
	var parent: Dictionary=Previous.new()._saves().filter(func(s):return s["state_sha256"]==fixture["parent"])[0]
	var saved: Dictionary=fixture["save"]
	for command in saved["commands"]:
		if command["op"]=="sortie_finish": command["trace"]=escort["trace"]
	saved["commands"]=parent["commands"]+saved["commands"]
	return saved


func _open():
	var ui=UI.new()._school_ui()
	var saved := _save()
	var restored: Dictionary=ui.model.restore_text(JSON.stringify(saved))
	assert_true(restored["supported"],str(restored))
	if not restored["supported"]:
		ui.free()
		return null
	assert_eq(ui.model.export_save(),saved)
	ui.refresh()
	var post: Dictionary=ui.model.read_postbattle()
	assert_eq(post["bundle"]["ratings"].map(func(r):return r["state"]),[3,4,4,0,0])
	assert_eq(Model.Postbattle.Adventures.available(post["planning"]["ledger"]).map(func(a):return a["id"]),[17])
	return ui


func _read_back(model) -> void:
	var path := "user://june-return-%s.json" % Time.get_ticks_usec()
	assert_true(model.save_file(path)["supported"])
	var fresh := Model.new()
	var result := fresh.load_file(path)
	assert_true(result["supported"],str(result))
	assert_eq(fresh.state(),model.state())
	assert_eq(fresh.export_save(),model.export_save())
	DirAccess.remove_absolute(ProjectSettings.globalize_path(path))


func _finish(ui) -> void:
	var panel=ui.postbattle_panel
	var view: Dictionary=ui.model.read_postbattle()
	assert_eq(view["page"].get("chapter"),32)
	assert_eq(view["total"],68)
	if view["phase"]!="post_story":return
	panel.next.pressed.emit()
	panel.previous.pressed.emit()
	panel.skip_dialog.confirmed.emit()
	view=ui.model.read_postbattle()
	assert_eq(view["page"].get("chapter"),33)
	assert_eq(view["total"],58)
	if view["phase"]!="new_week_story":return
	var school: Dictionary=view["bundle"]["school"]
	assert_eq([school["month"],school["week"]],[6,1])
	assert_eq(school["student_ids"].slice(0,school["student_count"]),[3,4,9,5,8,6,1])
	_read_back(ui.model)
	panel.skip_dialog.confirmed.emit()
	assert_eq(ui.model.stage(),"post_workroom")
	panel.next.pressed.emit()
	view=ui.model.read_postbattle()
	assert_eq(view["phase"],"returned_school")
	if view["phase"]!="returned_school":return
	school=view["bundle"]["school"]
	assert_eq(school["lecture_work_fields"][2],4)
	assert_eq(school["adventure_gate"],1)
	assert_true(panel.find_child("mode_1_1",true,false).disabled)
	assert_false(ui.model.execute({"op":"return_mode","group":0,"teaching":true})["supported"])
	panel.find_child("member_1",true,false).pressed.emit()
	panel.assignments.get_child(2).get_child(3).pressed.emit()
	assert_eq(ui.model.export_save()["commands"][-1],{"op":"return_move","kind":"student","member_id":1,"target_group":2,"target_slot":1})
	assert_eq(ui.model.export_save()["version"],12)
	_read_back(ui.model)
	var altered: Dictionary=ui.model.export_save()
	altered["rules"]["may_five_courses"]="altered"
	assert_eq(ui.model.restore(altered).get("reason"),"save_rules_changed")


func test_settle_saved_formation_and_return() -> void:
	_settle_courses(true)


func test_only_courses_17_and_27_and_return() -> void:
	_settle_courses(false)


func _settle_courses(keep_first_class: bool) -> void:
	var ui=_open()
	if ui==null:return
	var panel=ui.postbattle_panel
	var prior: Dictionary=ui.model.read_postbattle()["bundle"]
	assert_true(panel.find_child("settle",true,false).disabled)
	assert_false(ui.model.execute({"op":"return_settle"})["supported"])
	if keep_first_class:
		panel.find_child("mode_0_1",true,false).pressed.emit()
		assert_eq(ui.model.read_postbattle()["bundle"]["school"]["derived_student_ids"],prior["school"]["derived_student_ids"])
	else:
		panel.find_child("member_101",true,false).pressed.emit()
		panel.find_child("move_to_waiting",true,false).pressed.emit()
	assert_false(panel.find_child("settle",true,false).disabled)
	panel.find_child("settle",true,false).pressed.emit()
	panel.commit_dialog.hide()
	panel.commit_dialog.confirmed.emit()
	var view: Dictionary=ui.model.read_postbattle()
	assert_eq(view["phase"],"course_result")
	if view["phase"]=="course_result":
		var summary: Dictionary=view["planning"]["course_summary"]
		assert_eq(summary["date"],[5,5])
		assert_eq(summary["history_index"],9)
		var assignments := [[8,17],[6,27]]
		var packets := [[1020,1020,1020,1020,1020,1020,1020,1020],[0,0,0,25000,0,0,0,0]]
		if keep_first_class:
			assignments.push_front([3,7])
			packets.push_front([0,0,0,0,7740,0,3870,0])
		assert_eq(summary["students"].map(func(r):return [r["character_id"],r["work_id"]]),assignments)
		assert_eq(summary["bonus"],1020)
		assert_eq(summary["recipient"],6)
		assert_eq(summary["packets"].map(func(r):return r["packet"]),packets)
		assert_eq(summary["learning_draws"].size(),18 if keep_first_class else 13)
		assert_eq(summary["rand_state"],190065246 if keep_first_class else 3106899907)
		var record := Model.Postbattle.Return._find(view["bundle"]["records"],3)
		assert_eq(record["week_records"].slice(27,30),[1,1,6] if keep_first_class else [3,0,0])
		assert_eq(Model.Postbattle.Return._find(view["bundle"]["records"],8)["week_records"].slice(27,30),[1,0,16])
		assert_eq(Model.Postbattle.Return._find(view["bundle"]["records"],6)["week_records"].slice(27,30),[1,0,26])
		assert_eq(view["bundle"]["school"]["global_total_511c"],prior["school"]["global_total_511c"]+summary["bonus"])
		assert_false(ui.model.execute({"op":"return_settle"})["supported"])
		panel.find_child("continue_course_story",true,false).pressed.emit()
		_finish(ui)
	ui.free()


func test_open_sortie_with_saved_classes_and_return() -> void:
	var ui=_open()
	if ui==null:return
	var panel=ui.postbattle_panel
	var before: Dictionary=ui.model.read_postbattle()["bundle"]
	panel.find_child("adventure_17",true,false).pressed.emit()
	var depart=panel.find_child("depart",true,false)
	assert_false(depart.disabled)
	depart.pressed.emit()
	panel.commit_dialog.hide()
	panel.commit_dialog.confirmed.emit()
	var pending: Dictionary=ui.model.read_postbattle()
	assert_eq(pending["phase"],"sortie_pending")
	if pending["phase"]!="sortie_pending":
		ui.free()
		return
	var round_data: Dictionary=pending["planning"]["handoff"]["prepared"]["rounds"][0]
	assert_eq(round_data["student_ids"],[3])
	assert_eq(round_data["teacher_ids"],[101])
	_read_back(ui.model)
	panel.find_child("play_sortie",true,false).pressed.emit()
	var trial=ui.sortie_trial
	var battle=trial.session
	assert_true(battle.ready)
	if not battle.ready:
		ui.free()
		return
	while battle._ending_phase=="opening":trial._continue()
	assert_true(battle.command_move(3,Vector2i(90,15)))
	for tick in range(9000):
		battle.tick()
		if battle.ending_sub>=0:break
	assert_true(battle.ending_sub>=0)
	assert_eq([battle.ending_sub,battle._at_exit(),battle.battle_trace()["ticks"]],[14,false,1496])
	assert_eq(battle.find_unit(3).limits.hp,0)
	for step in range(4): battle.advance_exit()
	trial._refresh()
	trial.continue_button.pressed.emit()
	var view: Dictionary=ui.model.read_postbattle()
	assert_eq(view["phase"],"sortie_result")
	if view["phase"]=="sortie_result":
		var summary: Dictionary=view["planning"]["sortie_summary"]
		assert_eq(summary["scene_id"],17)
		assert_eq([summary["result_selector"],summary["score"]["total_delta"],summary["lessons"]["bonus"],summary["recipient"],summary["rand_state"]],[5,8315,1020,6,200332154])
		assert_eq(summary["date"],[5,5])
		assert_eq(summary["history_index"],9)
		assert_eq(summary["students"].map(func(r):return r["character_id"]),[3])
		assert_eq(summary["lessons"]["students"].map(func(r):return [r["character_id"],r["work_id"]]),[[8,17],[6,27]])
		assert_eq(view["bundle"]["school"]["global_total_511c"],before["school"]["global_total_511c"]+summary["score"]["total_delta"]+summary["lessons"]["bonus"])
		for id in [3,8,6]:
			var record := Model.Postbattle.Return._find(view["bundle"]["records"],id)
			assert_eq(record["week_records"][27],2 if id==3 else 1)
		panel.find_child("continue_sortie_story",true,false).pressed.emit()
		_finish(ui)
	ui.free()
