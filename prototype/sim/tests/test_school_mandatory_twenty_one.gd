extends "res://sim/tests/test_school_mandatory_twenty.gd"


func _save() -> Dictionary:
	var saved := super._save()
	var delta := Fixtures.new()._fixture("august_week3_saved_plan")
	assert_eq(saved.state_sha256,delta.parent)
	saved.commands.append({"op":"return_depart"})
	saved.commands.append({"op":"sortie_finish","trace":Fixtures.new()._fixture("mandatory_twenty_victory_trace").trace})
	saved.commands.append_array(delta.commands_after_battle)
	saved.rules.merge(delta.rules_added)
	for key in ["version","context","state_sha256"]:saved[key]=delta[key]
	return saved


func _mission() -> Dictionary:
	return {"scene":21,"month":8,"week":3,"opening_total":1553433,"students":[3,16,4,8,17,6,5,2,9,1],
		"groups":[0,0,0,1,1,2,2,2,3,3],"opening_pages":0,"ending_pages":1,"version":24,"trace":"mandatory_twenty_one_victory_trace"}


func _read_pages(ui, phase: String, pages: Array) -> void:
	for expected in pages:
		var view: Dictionary=ui.model.read_postbattle()
		assert_eq(view.phase,phase)
		assert_eq(view.page,expected)
		assert_eq([ui.postbattle_panel.speaker.text,ui.postbattle_panel.dialogue.text],[expected.speaker,expected.text])
		ui.postbattle_panel.next.pressed.emit()


func _read_and_replan(ui, path: String) -> void:
	var panel=ui.postbattle_panel
	var model=ui.model
	var dated:=Model.Postbattle.SortieWeek.story(3,8)
	var result: Dictionary=model.read_postbattle().planning.sortie_summary
	print("ADVENTURE21 ",JSON.stringify({"grade":result.task_grade,"score":result.score.total_delta,
		"total":result.score.total_after,"mvp":result.recipient,"awards":result.loot_groups}))
	assert_eq([dated.pre_week.size(),dated.week_start.size(),dated.school_entry.size()],[79,0,38])
	_read_pages(ui,"post_story",dated.pre_week)
	var card: Dictionary=model.read_postbattle()
	assert_eq(card.phase,"new_week_story")
	assert_eq(card.get("date_card",{}).get("image"),"res://assets/school_story/tc0804.png")
	assert_true(panel.card_frame.visible and panel.card_image.texture!=null)
	panel.next.pressed.emit()
	assert_eq(model.stage(),"post_workroom")
	var before: Dictionary=model.read_postbattle().bundle
	assert_eq([before.school.teacher_count,before.school.student_count,before.adv_background],[4,10,14])
	panel.next.pressed.emit()
	var joined: Dictionary=model.read_postbattle().bundle
	assert_eq([joined.school.teacher_count,joined.school.student_count],[5,11])
	_read_pages(ui,"school_entry_story",dated.school_entry)
	var v: Dictionary=model.read_postbattle()
	assert_eq([v.phase,v.bundle.school.month,v.bundle.school.week,v.bundle.school.adventure_gate],["returned_school",8,4,0])
	assert_eq(Model.Postbattle.Adventures.available(v.planning.ledger).map(func(r):return r.id),[17])
	assert_true(v.bundle.school.idle_teacher_ids.has(116) and v.bundle.school.idle_student_ids.has(13))
	if v.phase!="returned_school":return
	for member in [[116,1],[13,2]]:
		panel.find_child("member_%d"%member[0],true,false).pressed.emit()
		panel.assignments.get_child(4).get_child(member[1]).pressed.emit()
	var school: Dictionary=model.read_postbattle().bundle.school
	assert_eq(Model.Postbattle.Courses.Groups._word(school.group_raw_bytes,112),116)
	assert_eq(school.derived_student_ids[4],[13,-1,-1,-1])
	panel.find_child("mode_4_1",true,false).pressed.emit()
	var courses: OptionButton=panel.find_child("courses_4",true,false)
	assert_true(courses!=null and courses.item_count>1 and not courses.disabled)
	if courses==null or courses.item_count<2:return
	var choice:=33
	var option:=courses.get_item_index(choice)
	assert_true(option>=0)
	if option<0:return
	courses.item_selected.emit(option)
	assert_eq(Model.Postbattle.Courses.Groups._word(model.read_postbattle().bundle.school.group_raw_bytes,122),choice)
	ui.save_path=path
	panel.save_requested.emit()
	assert_true(FileAccess.file_exists(path))
	var fresh:=August.new()._screen()
	fresh.save_path=path
	fresh.load_button.pressed.emit()
	assert_eq(fresh.model.state(),model.state())
	assert_eq(fresh.model.export_save(),model.export_save())
	var changed: Dictionary=fresh.model.export_save()
	changed.rules.twenty_one_battle="changed"
	assert_eq(fresh.model.restore(changed).get("reason"),"save_rules_changed")
	print("RELOADED ",model.export_save().state_sha256," fifth course ",choice)
	fresh.free()
