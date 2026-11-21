extends "res://sim/tests/test_base.gd"
const Prior := preload("res://sim/tests/test_school_july_five_work.gd")
const Model := preload("res://sim/school_playground.gd")
const Screen := preload("res://ui/school_playground.gd")
const ROSTER := [[3,16,-1,4],[8,17,-1,-1],[6,-1,2,5],[9,1,-1,-1]]
const LESSONS := [[3,8],[16,8],[4,8],[8,19],[17,19],[6,26],[2,26],[5,26],[9,28],[1,28]]


func _save() -> Dictionary:
	var saved := Prior.new()._save()
	var delta := Prior.Prior.Fixtures.new()._fixture("august_week1_course_plan")
	assert_eq(saved.state_sha256,delta.parent)
	saved.commands.append_array(delta.commands)
	saved.rules.merge(delta.rules_added)
	for key in ["version","context","state_sha256"]:saved[key]=delta[key]
	return saved


func _screen() -> Screen:
	var ui := Screen.new()
	ui.auto_load=false
	ui.autosave=false
	(Engine.get_main_loop() as SceneTree).root.add_child(ui)
	return ui


func test_saved_courses_through_chapter_220_and_mandatory_adventure_20() -> void:
	var path := "user://august-two-%s.json" % Time.get_ticks_usec()
	var ui := _screen()
	var saved := _save()
	var restored := ui.model.restore(saved)
	assert_true(restored.supported,str(restored))
	if restored.supported:
		ui._restore_view()
		ui.refresh()
		_play(ui,saved,path)
	ui.free()
	if FileAccess.file_exists(path):DirAccess.remove_absolute(ProjectSettings.globalize_path(path))


func _play(ui: Screen, saved: Dictionary, path: String) -> void:
	var model := ui.model
	var panel=ui.postbattle_panel
	assert_eq(model.export_save(),saved)
	assert_eq(model.stage(),"returned_school")
	var school: Dictionary=model.read_postbattle().bundle.school
	assert_eq([school.month,school.week,school.global_total_511c],[8,1,1289287])
	assert_eq(school.derived_student_ids.slice(0,4),ROSTER)
	for group in range(4):
		var course=panel.find_child("courses_%d"%group,true,false)
		assert_eq(course.get_selected_id(),[8,19,26,28][group])
	var settle=panel.find_child("settle",true,false)
	assert_true(settle!=null and not settle.disabled)
	if settle==null or settle.disabled:return
	settle.pressed.emit()
	assert_true(panel.commit_dialog.visible)
	panel.commit_dialog.hide()
	panel.commit_dialog.confirmed.emit()
	assert_eq(model.stage(),"course_result")
	if model.stage()!="course_result":return
	var result := model.read_postbattle()
	var summary: Dictionary=result.planning.course_summary
	assert_eq([summary.date,summary.history_index],[[8,1],20])
	assert_eq([summary.bonus,summary.recipient,result.bundle.school.global_total_511c],[90930,9,1380217])
	assert_eq(summary.students.map(func(r):return [r.character_id,r.work_id]),LESSONS)
	assert_eq(result.bundle.school.global_total_511c,school.global_total_511c+summary.bonus)
	for entry in LESSONS:
		var record:=Model.Postbattle.Return._find(result.bundle.records,entry[0])
		assert_eq(record.week_records[60],1)
	print("8/1 courses ",LESSONS," bonus ",summary.bonus," MVP ",summary.recipient," total ",result.bundle.school.global_total_511c)
	var confirmed:=model.export_save()
	assert_false(model.execute({"op":"return_settle"}).supported)
	assert_eq(model.export_save(),confirmed)
	panel.find_child("continue_course_story",true,false).pressed.emit()
	assert_eq(model.stage(),"new_week_story")
	if model.stage()!="new_week_story":return
	var card:=model.read_postbattle()
	assert_eq(card.date_card.image,"res://assets/school_story/tc0802.png")
	assert_true(panel.card_frame.visible and panel.card_image.texture!=null)
	panel.next.pressed.emit()
	var expected: Array=Model.Postbattle.SortieWeek.story(1,8).week_start
	assert_eq(expected.size(),6)
	var indices: Array=[]
	for page in expected:
		var view := model.read_postbattle()
		assert_eq([view.phase,view.total,view.page],["new_week_story",6,page])
		assert_eq([page.chapter,panel.speaker.text,panel.dialogue.text],[220,page.speaker,page.text])
		indices.append_array(page.text_indices)
		panel.next.pressed.emit()
	assert_eq(indices,range(11))
	assert_eq(model.stage(),"post_workroom")
	panel.next.pressed.emit()
	assert_eq(model.stage(),"returned_school")
	if model.stage()!="returned_school":return
	school=model.read_postbattle().bundle.school
	assert_eq([school.month,school.week,school.adventure_gate,school.lecture_work_fields[2]],[8,2,1,20])
	assert_eq(school.derived_student_ids.slice(0,4),ROSTER)
	for group in range(4):
		assert_eq(school.group_raw_bytes[group*28+3],0)
		assert_true(panel.find_child("mode_%d_1"%group,true,false).disabled)
	var mission=panel.find_child("adventure_20",true,false)
	assert_true(mission!=null and mission.disabled and mission.button_pressed)
	assert_true(panel.find_child("adventure_17",true,false)==null)
	assert_true(panel.find_child("depart",true,false)==null)
	assert_true(panel.find_child("settle",true,false)==null)
	for cmd in [{"op":"return_mode","group":2,"teaching":true},{"op":"return_select","adventure":17},{"op":"return_settle"},{"op":"return_depart"}]:
		assert_false(model.execute(cmd).supported)
	panel.find_child("member_5",true,false).pressed.emit()
	panel.assignments.get_child(2).get_child(3).pressed.emit()
	var planned:=model.export_save()
	assert_eq(planned.commands[-1],{"op":"return_move","kind":"student","member_id":5,"target_group":2,"target_slot":1})
	assert_eq(model.read_postbattle().bundle.school.derived_student_ids[2],[6,5,2,-1])
	assert_eq(planned.version,22)
	ui.save_path=path
	panel.save_requested.emit()
	assert_true(FileAccess.file_exists(path))
	var fresh:=_screen()
	fresh.save_path=path
	fresh.load_button.pressed.emit()
	assert_eq(fresh.model.export_save(),planned)
	assert_eq(fresh.model.state(),model.state())
	assert_true(fresh.postbattle_panel.visible)
	var changed:=fresh.model.export_save()
	changed.rules.august_two_story="altered"
	assert_eq(fresh.model.restore(changed).get("reason"),"save_rules_changed")
	print("8/2 Chapter220 ",expected.size()," pages / ",indices.size()," lines, mandatory ",school.lecture_work_fields[2],", seats ",model.read_postbattle().bundle.school.derived_student_ids.slice(0,4),", restored ",fresh.model.export_save().state_sha256)
	fresh.free()
