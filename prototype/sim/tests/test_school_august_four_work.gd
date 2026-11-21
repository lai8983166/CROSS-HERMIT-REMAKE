extends "res://sim/tests/test_base.gd"
const Prior := preload("res://sim/tests/test_school_mandatory_twenty_one.gd")
const Model := preload("res://sim/school_playground.gd")


func _save() -> Dictionary:
	var saved := Prior.new()._save()
	var delta := Prior.Fixtures.new()._fixture("august_week4_saved_plan")
	assert_eq(saved.state_sha256,delta.parent)
	saved.commands.append({"op":"return_depart"})
	saved.commands.append({"op":"sortie_finish","trace":Prior.Fixtures.new()._fixture("mandatory_twenty_one_victory_trace").trace})
	saved.commands.append_array(delta.commands_after_battle)
	saved.rules.merge(delta.rules_added)
	for key in ["version","context","state_sha256"]:saved[key]=delta[key]
	return saved


func test_five_lessons_through_august_five() -> void:
	_round_trip(false)


func test_training_with_fifth_class_through_august_five() -> void:
	_round_trip(true)


func _round_trip(training: bool) -> void:
	var path := "user://august-five-%s.json" % Time.get_ticks_usec()
	_play(training,path)
	if FileAccess.file_exists(path):DirAccess.remove_absolute(ProjectSettings.globalize_path(path))


func _play(training: bool, path: String, parent_path: String="") -> void:
	var ui := Prior.August.new()._screen()
	var saved := _save()
	if parent_path.is_empty():
		var loaded := ui.model.restore(saved)
		assert_true(loaded.supported,str(loaded))
		ui._restore_view()
		ui.refresh()
	else:
		ui.save_path=parent_path
		ui.load_button.pressed.emit()
	assert_eq(ui.model.export_save(),saved,"accepted parent")
	if ui.model.stage()=="returned_school":_work(ui,training,path)
	ui.free()


func _choose(panel, group: int, course: int) -> bool:
	panel.find_child("mode_%d_1"%group,true,false).pressed.emit()
	var options: OptionButton=panel.find_child("courses_%d"%group,true,false)
	var idx:=options.get_item_index(course)
	assert_true(idx>=0 and not options.disabled,"course %d unavailable"%course)
	if idx<0 or options.disabled:return false
	options.item_selected.emit(idx)
	return true


func _work(ui, training: bool, path: String) -> void:
	var panel=ui.postbattle_panel
	var model=ui.model
	var opening: Dictionary=model.read_postbattle().bundle.school
	assert_eq([opening.month,opening.week,opening.global_total_511c],[8,4,1748100])
	assert_eq(opening.derived_student_ids[4],[13,-1,-1,-1])
	assert_eq(panel.find_child("courses_4",true,false).get_selected_id(),33)
	if training:
		panel.find_child("adventure_17",true,false).pressed.emit()
	else:
		for group in range(4):
			if not _choose(panel,group,[8,19,26,30][group]):return
	var commit=panel.find_child("depart" if training else "settle",true,false)
	assert_true(commit!=null and not commit.disabled,"work unavailable")
	if commit==null or commit.disabled:return
	commit.pressed.emit()
	assert_true(panel.commit_dialog.visible)
	panel.commit_dialog.hide()
	panel.commit_dialog.confirmed.emit()
	if training:
		assert_eq(model.stage(),"sortie_pending")
		if model.stage()!="sortie_pending":return
		var party: Dictionary=model.read_postbattle().planning.handoff.prepared.rounds[0]
		assert_eq([party.scene_id,party.teacher_ids,party.student_ids],[17,[101,110,115,118],[3,16,4,8,17,6,5,2,9,1]])
		panel.find_child("play_sortie",true,false).pressed.emit()
		var trial=ui.sortie_trial
		var trace:=Prior.Fixtures.new()._fixture("august_week4_training_trace")
		assert_eq(trial.session._pages(1).size(),3)
		var remaining:=trace.duplicate(true)
		for page in trial.session._pages(1):
			assert_eq(trial.text_label.text,"\n".join(page.map(func(line):return line.text)))
			assert_eq(remaining.commands.pop_front(),[0,1,1])
			trial.continue_button.pressed.emit()
		var replay:=Model.BattleRecord.run_trace(trial.session,remaining)
		assert_true(replay.supported,str(replay))
		if not replay.supported:return
		assert_true(trial.session._at_exit())
		assert_eq(trial.session.battle_trace(),trace)
		trial._refresh()
		var ending: Array=trial.session._pages(trial.session.ending_sub)
		assert_eq(ending.size(),2)
		assert_true(trial.summary_navigation.visible,"training exit pagination")
		for i in range(ending.size()):
			assert_eq(trial.text_label.text.split("\n（")[0],"\n".join(ending[i].map(func(line):return line.text)),"training exit page %d"%i)
			if i+1<ending.size():trial.next_page.pressed.emit()
		print("T0017 pages ",trial.session._pages(1).size(),"/",ending.size(),", exit ",trial.session.ending_sub)
		trial.continue_button.pressed.emit()
	assert_eq(model.stage(),"sortie_result" if training else "course_result")
	if model.stage() not in ["sortie_result","course_result"]:return
	var result: Dictionary=model.read_postbattle()
	var summary: Dictionary=result.planning.sortie_summary if training else result.planning.course_summary
	var lessons: Dictionary=summary.lessons if training else summary
	var work: Array=lessons.students.map(func(r):return [r.character_id,r.work_id])
	assert_eq(work,[[13,33]] if training else [[3,8],[16,8],[4,8],[8,19],[17,19],[6,26],[5,26],[2,26],[9,30],[1,30],[13,33]])
	assert_eq(summary.history_index,23)
	if not training:
		assert_eq([lessons.bonus,summary.recipient,result.bundle.school.global_total_511c],[92500,9,1840600])
		assert_eq(lessons.students.back().new_skill_ids,[46])
	else:
		assert_eq([summary.result_selector,summary.task_grade,summary.score.total_delta,lessons.bonus,summary.recipient,result.bundle.school.global_total_511c],[5,5,9910,1000,4,1759010])
		assert_eq(lessons.students[0].new_skill_ids,[68])
		assert_true(summary.loot_groups.all(func(row):return row.size()==10 and row.count(0)==10))
	for row in result.bundle.records:
		assert_eq(row.week_records[69],2 if training and row.character_id!=13 else 1)
	print("SETTLED ",training," ",work," bonus ",lessons.bonus," MVP ",summary.recipient," total ",result.bundle.school.global_total_511c)
	panel.find_child("continue_sortie_story" if training else "continue_course_story",true,false).pressed.emit()
	var story:=Model.Postbattle.SortieWeek.story(4,8)
	assert_eq([story.pre_week.size(),story.week_start.size(),story.school_entry.size()],[26,40,0])
	_read_pages(ui,"post_story",story.pre_week)
	var view: Dictionary=model.read_postbattle()
	assert_eq(view.phase,"new_week_story")
	assert_eq(view.get("date_card",{}).get("image"),"res://assets/school_story/tc0805.png")
	assert_true(panel.card_frame.visible and panel.card_image.texture!=null)
	panel.next.pressed.emit()
	_read_pages(ui,"new_week_story",story.week_start)
	assert_eq(model.stage(),"post_workroom")
	panel.next.pressed.emit()
	view=model.read_postbattle()
	assert_eq(view.phase,"returned_school")
	if view.phase!="returned_school":return
	var school: Dictionary=view.bundle.school
	assert_eq([school.month,school.week,school.student_count,school.teacher_count],[8,5,11,5])
	assert_eq([view.bundle.flags["0x7a55f6"],view.bundle.flags["0x7e11a0"],view.bundle.adv_background],[3,1,14])
	assert_eq(school.derived_student_ids,opening.derived_student_ids)
	if training:assert_eq(school.lecture_work_fields,[1,0,17,1])
	assert_eq(view.bundle.newly_dated_adventures.map(func(r):return r.id),[35])
	assert_eq(Model.Postbattle.Adventures.available(view.planning.ledger).map(func(r):return r.id),[35,17])
	panel.find_child("adventure_35",true,false).pressed.emit()
	assert_eq(model.read_postbattle().bundle.school.lecture_work_fields,[0,1,35,0])
	if not _choose(panel,0,7):return
	assert_eq(panel.find_child("courses_0",true,false).get_selected_id(),7)
	assert_eq(panel.find_child("courses_4",true,false).get_selected_id(),33)
	ui.save_path=path
	panel.save_requested.emit()
	assert_true(FileAccess.file_exists(path))
	var fresh:=Prior.August.new()._screen()
	fresh.save_path=path
	fresh.load_button.pressed.emit()
	assert_eq(fresh.model.state(),model.state())
	assert_eq(fresh.model.export_save(),model.export_save())
	var changed: Dictionary=model.export_save()
	assert_eq(changed.version,25)
	changed.rules.august_five_story="changed"
	assert_eq(fresh.model.restore(changed).get("reason"),"save_rules_changed")
	print("RELOADED ",training," ",model.export_save().state_sha256," commands ",model.export_save().commands.size())
	fresh.free()


func _read_pages(ui, phase: String, pages: Array) -> void:
	for expected in pages:
		var view: Dictionary=ui.model.read_postbattle()
		assert_eq(view.phase,phase)
		assert_eq(view.page,expected)
		assert_eq([ui.postbattle_panel.speaker.text,ui.postbattle_panel.dialogue.text],[expected.speaker,expected.text])
		if view.phase!=phase:return
		ui.postbattle_panel.next.pressed.emit()
