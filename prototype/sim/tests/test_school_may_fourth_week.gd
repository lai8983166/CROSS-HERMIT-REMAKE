extends "res://sim/tests/test_base.gd"
const Earlier := preload("res://sim/tests/test_school_may_third_week.gd")
const Model := preload("res://sim/school_playground.gd")
const UI := preload("res://sim/tests/test_school_combat_handoff.gd")


func _play_battle(ui, id: int) -> bool:
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
	if ui.model.stage()!="sortie_pending": return false
	panel.find_child("play_sortie",true,false).pressed.emit()
	var trial=ui.sortie_trial
	assert_true(trial.title_label.text.contains("第3周"))
	var battle=trial.session
	while battle._ending_phase=="opening": trial._continue()
	var enemies: Array=battle.enemies()
	enemies.sort_custom(func(a,b):return battle._distance(battle.controlled_units()[0],a)<battle._distance(battle.controlled_units()[0],b))
	assert_true(battle.command_attack(3,battle.unit_key(enemies[0])))
	for tick in range(9000):
		battle.tick()
		if battle.ending_sub>=0: break
	for step in range(4): battle.advance_exit()
	trial._refresh()
	assert_true(battle.ending_sub>=0)
	trial.continue_button.pressed.emit()
	assert_eq(ui.model.stage(),"sortie_result")
	return ui.model.stage()=="sortie_result"


func _play_course(ui, course: int) -> bool:
	var panel=ui.postbattle_panel
	var options=panel.find_child("courses_0",true,false)
	options.item_selected.emit(options.get_item_index(course))
	panel.find_child("settle",true,false).pressed.emit()
	panel.commit_dialog.hide()
	panel.commit_dialog.confirmed.emit()
	assert_eq(ui.model.stage(),"course_result")
	if ui.model.stage()!="course_result": return false
	var result: Dictionary=ui.model.read_postbattle()["planning"]["course_summary"]
	assert_eq(result["students"][0]["work_id"],course)
	if course==6:
		assert_eq(result["recipient"],-1)
		assert_true(result["bonus"]>0)
	return true


func _load_again(model) -> void:
	var path := "user://may-week-four-%d.json" % Time.get_ticks_usec()
	assert_true(model.save_file(path)["supported"])
	var loaded := Model.new()
	var result := loaded.load_file(path)
	assert_true(result["supported"],str(result))
	assert_eq(loaded.export_save(),model.export_save())
	assert_eq(loaded.state(),model.state())
	var altered: Dictionary=model.export_save()
	altered["rules"]["may_week_four"]="changed"
	assert_eq(loaded.restore(altered).get("reason"),"save_rules_changed")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(path))


func _finish(ui) -> void:
	var panel=ui.postbattle_panel
	var chapters := [28,29,207]
	for chapter in chapters:
		var story: Dictionary=ui.model.read_postbattle()
		assert_eq(story["page"].get("chapter"),chapter)
		if story["page"].get("chapter")!=chapter:return
		if chapter==29:
			var school: Dictionary=story["bundle"]["school"]
			assert_eq([school["student_count"],school["teacher_count"]],[5,2])
		panel.next.pressed.emit()
		panel.previous.pressed.emit()
		assert_eq(ui.model.read_postbattle()["cursor"],0)
		if chapter==207:
			assert_eq(story["total"],17)
			assert_false(ui.model.execute({"op":"post_school"})["supported"])
			assert_false(ui.model.execute({"op":"return_plan"})["supported"])
			_load_again(ui.model)
		panel.skip_dialog.confirmed.emit()
		if chapter==29:
			assert_eq(ui.model.stage(),"post_workroom")
			assert_eq(ui.model.read_postbattle()["bundle"]["adv_background"],6)
			assert_eq(ui.model.read_postbattle()["bundle"]["flags"]["0x7e11a0"],0)
			panel.next.pressed.emit()
	assert_eq(ui.model.stage(),"returned_school")
	if ui.model.stage()!="returned_school":return
	var school: Dictionary=ui.model.read_postbattle()["bundle"]["school"]
	var bundle: Dictionary=ui.model.read_postbattle()["bundle"]
	assert_eq(bundle["flags"]["0x7e11a0"],1)
	assert_eq(bundle["newly_dated_adventures"].map(func(rule):return rule["id"]),[7])
	assert_eq([school["month"],school["week"]],[5,4])
	assert_eq(school["lecture_work_fields"][2],7)
	assert_eq([school["student_count"],school["teacher_count"]],[5,2])
	assert_true(panel.find_child("mode_0_1",true,false).disabled)
	assert_false(ui.model.execute({"op":"return_mode","group":0,"teaching":true})["supported"])
	assert_false(ui.model.execute({"op":"return_course","group":0,"course":7})["supported"])
	assert_false(ui.model.execute({"op":"return_select","adventure":17})["supported"])
	# Assign both new members to the second class via the roster and class slots.
	for member in [110,8]:
		panel.find_child("member_%d" % member,true,false).pressed.emit()
		panel.assignments.get_child(1).get_child(1 if member==110 else 2).pressed.emit()
	school=ui.model.read_postbattle()["bundle"]["school"]
	assert_eq(panel.Groups._word(school["group_raw_bytes"],28),110)
	assert_eq(panel.Groups._word(school["group_raw_bytes"],44),8)
	_load_again(ui.model)


func test_third_week_work_from_each_accepted_v9_save() -> void:
	var data: Dictionary=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://sim/tests/may_week3_saved_plans.json")))
	for item in data["cases"]:
		var ui=UI.new()._school_ui()
		var saved: Dictionary=item["save"]
		saved["commands"]=Earlier.new()._save(item["parent_route"])["commands"]+saved["commands"]
		var restored: Dictionary=ui.model.restore_text(JSON.stringify(saved))
		assert_true(restored["supported"],str(restored))
		if not restored["supported"]:
			ui.free()
			continue
		assert_eq(ui.model.export_save(),saved)
		ui.refresh()
		var sortie: bool=item["second_work"]!=0
		var success := _play_battle(ui,17 if item["second_work"]==8 else 8) if sortie else _play_course(ui,6 if item["parent_route"]=="sortie" else 7)
		if success:
			var view: Dictionary=ui.model.read_postbattle()
			var result: Dictionary=view["planning"]["sortie_summary" if sortie else "course_summary"]
			assert_eq(result["date"],[5,3])
			assert_eq(result["history_index"],7)
			assert_eq(ui.model.export_save()["version"],10)
			assert_false(ui.model.execute({"op":"return_settle"})["supported"])
			var downgraded: Dictionary=ui.model.export_save()
			for key in ["version","context","rules"]: downgraded[key]=saved[key]
			assert_false(ui.model.restore(downgraded)["supported"])
			ui.postbattle_panel.find_child("continue_sortie_story" if sortie else "continue_course_story",true,false).pressed.emit()
			_finish(ui)
		ui.free()
