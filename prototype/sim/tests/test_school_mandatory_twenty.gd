extends "res://sim/tests/test_school_mandatory_nine.gd"
const August := preload("res://sim/tests/test_school_august_course.gd")


func _save() -> Dictionary:
	var saved := August.new()._save()
	var delta := Fixtures.new()._fixture("august_week2_saved_plan")
	assert_eq(saved.state_sha256,delta.parent)
	saved.commands.append_array(delta.commands)
	saved.rules.merge(delta.rules_added)
	for key in ["version","context","state_sha256"]:saved[key]=delta[key]
	return saved


func _mission() -> Dictionary:
	return {"scene":20,"month":8,"week":2,"opening_total":1380217,"students":[3,16,4,8,17,6,5,2,9,1],
		"groups":[0,0,0,1,1,2,2,2,3,3],"version":23,"trace":"mandatory_twenty_victory_trace"}


func _run_battle(trial, trace: Dictionary) -> Dictionary:
	var session=trial.session
	var remaining:=trace.duplicate(true)
	var opening: Array=session._pages(1)
	assert_eq(opening.size(),2)
	for page in opening:
		assert_eq(trial.text_label.text,"\n".join(page.map(func(line):return line.text)))
		assert_eq(remaining.commands.pop_front(),[0,1,1])
		trial.continue_button.pressed.emit()
	var replay:=Model.BattleRecord.run_trace(session,remaining)
	if not replay.supported:return replay
	trial._refresh()
	var ending: Array=session._pages(session.ending_sub)
	assert_false(ending.is_empty())
	for i in range(ending.size()):
		assert_true(trial.text_label.text.begins_with("\n".join(ending[i].map(func(line):return line.text))))
		if i+1<ending.size():trial.next_page.pressed.emit()
	print("T0020 opening pages ",opening.size()," ending sub ",session.ending_sub," pages ",ending.size())
	return replay


func _read_and_replan(ui, path: String) -> void:
	var model=ui.model
	var panel=ui.postbattle_panel
	var view: Dictionary=model.read_postbattle()
	var result: Dictionary=view.planning.sortie_summary
	print("ADVENTURE20 ",JSON.stringify({"selector":result.result_selector,"score":result.score.total_delta,
		"total":view.bundle.school.global_total_511c,"mvp":result.recipient,"grade":result.task_grade,
		"loot":result.loot_groups,"units":result.score.characters.map(func(c):return c.character_id)}))
	var dated:=Model.Postbattle.SortieWeek.story(2,8)
	assert_eq([dated.pre_week,dated.week_start.size(),dated.school_entry],[[],34,[]])
	assert_eq(model.stage(),"new_week_story")
	if model.stage()!="new_week_story":return
	assert_eq(view.date_card.image,"res://assets/school_story/tc0803.png")
	assert_true(panel.card_frame.visible and panel.card_image.texture!=null)
	panel.next.pressed.emit()
	var indices := []
	for page in dated.week_start:
		assert_eq(model.read_postbattle().page,page)
		assert_eq([page.chapter,panel.speaker.text,panel.dialogue.text],[221,page.speaker,page.text])
		indices.append_array(page.text_indices)
		panel.next.pressed.emit()
	assert_eq(indices,range(43))
	assert_eq(model.stage(),"post_workroom")
	panel.next.pressed.emit()
	view=model.read_postbattle()
	var school: Dictionary=view.bundle.school
	assert_eq([model.stage(),school.month,school.week,school.teacher_count,school.student_count],["returned_school",8,3,4,10])
	assert_eq([school.adventure_gate,school.lecture_work_fields],[1,[3,20,21,0]])
	assert_eq(Model.Postbattle.Adventures.available(view.planning.ledger).map(func(r):return r.id),[21,17])
	assert_true(panel.find_child("adventure_21",true,false).button_pressed)
	assert_false(model.execute({"op":"return_select","adventure":17}).supported)
	panel.find_child("member_17",true,false).pressed.emit()
	panel.assignments.get_child(1).get_child(4).pressed.emit()
	assert_eq(model.read_postbattle().bundle.school.derived_student_ids[1],[8,-1,17,-1])
	assert_eq(model.export_save().commands[-1],{"op":"return_move","kind":"student","member_id":17,"target_group":1,"target_slot":2})
	ui.save_path=path
	panel.save_requested.emit()
	assert_true(FileAccess.file_exists(path))
	var fresh:=August.new()._screen()
	fresh.save_path=path
	fresh.load_button.pressed.emit()
	assert_eq(fresh.model.state(),model.state())
	assert_eq(fresh.model.export_save(),model.export_save())
	var changed: Dictionary=fresh.model.export_save()
	changed.rules.mandatory_twenty="changed"
	assert_eq(fresh.model.restore(changed).get("reason"),"save_rules_changed")
	print("RELOADED ",model.export_save().state_sha256)
	fresh.free()
