extends "res://sim/tests/test_base.gd"
const Model := preload("res://sim/school_playground.gd")
const UI := preload("res://sim/tests/test_school_combat_handoff.gd")
const Plans := preload("res://sim/school_return_adventures.gd")


func _save(route: String) -> Dictionary:
	var data: Dictionary=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://sim/tests/may_week2_saved_plans.json")))
	var save: Dictionary=data["saves"][route]
	for command in data["common_commands"]:
		if command["op"]=="battle_finish":
			var battle: Dictionary=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_postbattle_battle_record.json")))
			command["trace"]=battle["trace"]
	save["commands"]=data["common_commands"]+save["commands"]
	return save


func _restore(model, route: String) -> void:
	var saved := _save(route)
	var restored: Dictionary=model.restore_text(JSON.stringify(saved))
	assert_true(restored["supported"],str(restored))
	assert_eq(model.export_save(),saved)


func _roundtrip(model) -> bool:
	var copy := Model.new()
	var restored := copy.restore_text(JSON.stringify(model.export_save()))
	assert_true(restored["supported"],str(restored))
	assert_eq(copy.state(),model.state())
	return restored["supported"]


func _check_week_three(ui, opening: Dictionary, used: int) -> void:
	var view: Dictionary=ui.model.read_postbattle()
	assert_eq(view["phase"],"returned_school")
	assert_eq(view["bundle"]["school"]["week"],3)
	assert_eq(view["planning"]["ledger"],Plans.advance(opening,used))
	assert_true(ui.postbattle_panel.heading.text.contains("第3周"))
	assert_true(ui.postbattle_panel.find_child("settle",true,false)==null)
	assert_true(ui.postbattle_panel.find_child("depart",true,false)==null)
	ui.postbattle_panel.find_child("mode_0_1",true,false).pressed.emit()
	var courses=ui.postbattle_panel.find_child("courses_0",true,false)
	for id in [6,7]: assert_true(courses.get_item_index(id)>=0)
	courses.item_selected.emit(courses.get_item_index(7))
	assert_eq(ui.model.export_save()["commands"][-1],{"op":"return_course","group":0,"course":7})
	var path := "user://may-week-three-%d.json" % Time.get_ticks_usec()
	assert_true(ui.model.save_file(path)["supported"])
	assert_eq(FileAccess.get_file_as_string(path).strip_edges(),JSON.stringify(ui.model.export_save(),"",true))
	var loaded := Model.new()
	assert_true(loaded.load_file(path)["supported"])
	assert_eq(loaded.state(),ui.model.state())
	assert_eq(loaded.export_save(),ui.model.export_save())
	DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	for op in ["return_settle","return_depart","post_skip"]:
		assert_false(loaded.execute({"op":op})["supported"])


func _finish_story(ui, opening: Dictionary, used: int) -> void:
	var panel=ui.postbattle_panel
	var story: Dictionary=ui.model.read_postbattle()
	assert_eq(story["page"]["chapter"],25)
	assert_eq(story["total"],20)
	panel.next.pressed.emit()
	panel.previous.pressed.emit()
	assert_eq(ui.model.read_postbattle()["cursor"],0)
	panel.skip_dialog.confirmed.emit()
	assert_eq(ui.model.read_postbattle()["page"]["chapter"],26)
	assert_eq(ui.model.read_postbattle()["total"],336)
	assert_true(_roundtrip(ui.model))
	panel.skip_dialog.confirmed.emit()
	assert_eq(ui.model.stage(),"post_workroom")
	assert_eq(ui.model.read_postbattle()["bundle"]["flags"]["0x7e11a0"],0)
	panel.next.pressed.emit()
	assert_eq(ui.model.read_postbattle()["bundle"]["flags"]["0x7e11a0"],1)
	_check_week_three(ui,opening,used)


func test_second_week_class_after_both_accepted_saves() -> void:
	for route in ["sortie","course"]:
		var ui=UI.new()._school_ui()
		_restore(ui.model,route)
		ui.refresh()
		var panel=ui.postbattle_panel
		var original: Dictionary=ui.model.export_save()
		var opening: Dictionary=ui.model.read_postbattle()["planning"]["ledger"]
		panel.find_child("mode_0_1",true,false).pressed.emit()
		var courses=panel.find_child("courses_0",true,false)
		courses.item_selected.emit(courses.get_item_index(4))
		panel.find_child("settle",true,false).pressed.emit()
		panel.commit_dialog.hide()
		panel.commit_dialog.confirmed.emit()
		assert_eq(ui.model.stage(),"course_result")
		if ui.model.stage()!="course_result":
			ui.free()
			return
		assert_eq(ui.model.export_save()["version"],9)
		assert_false(ui.model.execute({"op":"return_settle"})["supported"])
		var result: Dictionary=ui.model.read_postbattle()
		assert_eq(result["planning"]["course_summary"]["date"],[5,2])
		assert_eq(result["planning"]["course_summary"]["history_index"],6)
		assert_false(result["planning"].has("sortie_summary"))
		assert_true(_roundtrip(ui.model))
		var invalid: Dictionary=ui.model.export_save()
		for key in ["version","context","rules"]: invalid[key]=original[key]
		assert_false(ui.model.restore(invalid)["supported"])
		panel.find_child("continue_course_story",true,false).pressed.emit()
		_finish_story(ui,opening,0)
		var after: Dictionary=ui.model.read_postbattle()["bundle"]
		for key in ["counts","records","item_flags"]: assert_eq(after[key],result["bundle"][key])
		ui.free()


func test_actual_battles_after_both_accepted_saves() -> void:
	for route in ["course","sortie"]:
		var id := 8 if route=="course" else 17
		var ui=UI.new()._school_ui()
		_restore(ui.model,route)
		var opening: Dictionary=ui.model.read_postbattle()["planning"]["ledger"]
		for student in [4,9,5]:
			assert_true(ui.model.execute({"op":"return_move","kind":"student","member_id":student,"target_group":-1,"target_slot":-1})["supported"])
		ui.refresh()
		var panel=ui.postbattle_panel
		panel.find_child("mode_0_0",true,false).pressed.emit()
		panel.find_child("adventure_%d" % id,true,false).pressed.emit()
		panel.find_child("depart",true,false).pressed.emit()
		panel.commit_dialog.hide()
		panel.commit_dialog.confirmed.emit()
		assert_eq(ui.model.stage(),"sortie_pending")
		if ui.model.stage()!="sortie_pending":
			ui.free()
			return
		assert_eq(ui.model.export_save()["version"],9)
		assert_true(_roundtrip(ui.model))
		panel.find_child("play_sortie",true,false).pressed.emit()
		var trial=ui.sortie_trial
		assert_true(trial.title_label.text.contains("第2周"))
		var battle=trial.session
		while battle._ending_phase=="opening":trial._continue()
		var enemies: Array=battle.enemies()
		enemies.sort_custom(func(a,b):return battle._distance(battle.controlled_units()[0],a)<battle._distance(battle.controlled_units()[0],b))
		assert_true(battle.command_attack(3,battle.unit_key(enemies[0])))
		for i in range(9000):
			battle.tick()
			if battle.ending_sub>=0:break
		for i in range(4):battle.advance_exit()
		trial._refresh()
		assert_true(battle.ending_sub>=0)
		trial.continue_button.pressed.emit()
		assert_eq(ui.model.stage(),"sortie_result")
		if ui.model.stage()!="sortie_result":
			ui.free()
			return
		var result: Dictionary=ui.model.read_postbattle()
		assert_eq(result["planning"]["sortie_summary"]["date"],[5,2])
		assert_eq(result["planning"]["sortie_summary"]["history_index"],6)
		assert_false(result["planning"].has("course_summary"))
		panel.find_child("continue_sortie_story",true,false).pressed.emit()
		_finish_story(ui,opening,id)
		ui.free()
