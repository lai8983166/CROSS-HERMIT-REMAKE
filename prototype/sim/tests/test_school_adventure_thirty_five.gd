extends "res://sim/tests/test_base.gd"
const August := preload("res://sim/tests/test_school_august_four_work.gd")
const Model := preload("res://sim/school_playground.gd")
const Fixtures := August.Prior.Fixtures
const ROSTER := [[3,16,-1,4],[8,-1,17,-1],[6,5,2,-1],[9,1,-1,-1],[13,-1,-1,-1]]


const SORTIE_GROUPS := [0,2,3]
const TEACHERS := [101,110,115,118,116]
const COURSES := [7,19,26,30,33]


func _save() -> Dictionary:
	var saved := August.new()._save()
	var delta := Fixtures.new()._fixture("august_week5_course_plan")
	assert_eq(saved.state_sha256,delta.parent)
	saved.commands.append_array(delta.commands)
	saved.rules.merge(delta.rules_added)
	for key in ["version","context","state_sha256"]:saved[key]=delta[key]
	return saved


func test_saved_class_through_chapter049_and_september_planning() -> void:
	var path := "user://september-one-%s.json"%Time.get_ticks_usec()
	_play(path)
	if FileAccess.file_exists(path):DirAccess.remove_absolute(ProjectSettings.globalize_path(path))


func _play(path: String, parent_path: String="") -> void:
	var ui:=August.Prior.August.new()._screen()
	if parent_path.is_empty():
		var opened:=ui.model.restore(_save())
		assert_true(opened.supported,str(opened))
		ui._restore_view()
		ui.refresh()
	else:
		ui.save_path=parent_path
		ui.load_button.pressed.emit()
	assert_eq(ui.model.export_save(),_save(),"accepted August 5 course save")
	if ui.model.stage()=="returned_school" and _battle(ui):
		_school(ui,path)
	ui.free()


func _battle(ui) -> bool:
	var model=ui.model
	var panel=ui.postbattle_panel
	var opening: Dictionary=model.read_postbattle().bundle.school
	assert_eq([opening.month,opening.week,opening.global_total_511c,opening.lecture_work_fields],[8,5,1840600,[0,1,35,0]])
	assert_eq(opening.derived_student_ids,ROSTER)
	for group in range(5):
		assert_eq(panel.find_child("courses_%d"%group,true,false).get_selected_id(),[7,19,26,30,33][group])
	for group in SORTIE_GROUPS:
		panel.find_child("mode_%d_0"%group,true,false).pressed.emit()
	var depart=panel.find_child("depart",true,false)
	assert_true(depart!=null and not depart.disabled,"saved party ready for adventure 35")
	if depart==null or depart.disabled:return false
	depart.pressed.emit()
	panel.commit_dialog.hide()
	panel.commit_dialog.confirmed.emit()
	assert_eq(model.stage(),"sortie_pending")
	if model.stage()!="sortie_pending":return false
	var party: Dictionary=model.read_postbattle().planning.handoff.prepared.rounds[0]
	var students := []
	var groups := []
	var teachers := []
	var lessons := []
	for group in range(5):
		if group in SORTIE_GROUPS:teachers.append(TEACHERS[group])
		for pupil in ROSTER[group]:
			if pupil<0:continue
			if group in SORTIE_GROUPS:
				students.append(pupil)
				groups.append(group)
			else:
				lessons.append([pupil,COURSES[group]])
	assert_eq(party,{"scene_id":35,"teacher_ids":teachers,"student_ids":students,"student_groups":groups})
	panel.find_child("play_sortie",true,false).pressed.emit()
	var trial=ui.sortie_trial
	var battle=trial.session
	assert_true(battle.ready,"open scene 35")
	if not battle.ready:return false
	assert_eq(battle._pages(1),[])
	var trace:=Fixtures.new()._fixture("august_week5_adventure35_trace")
	var run:=Model.BattleRecord.run_trace(battle,trace)
	assert_true(run.supported,str(run))
	if not run.supported:return false
	assert_eq(battle.battle_trace(),trace)
	assert_eq([trace.ticks,trace.commands.size(),battle.elapsed,battle.ending_sub],[28815,300,57630,11])
	var ending: Dictionary=battle.ending_snapshot()
	assert_true(battle.ending_sub in [2,5,8,11],"all statues cleared")
	var pages: Array=ending.text
	assert_eq(pages.size(),1,"original ending page")
	if pages.size()!=1 or battle.ending_sub not in [2,5,8,11]:return false
	assert_eq(pages[0].size(),3,"three original ending lines")
	assert_eq(ending.summary.defeated_enemies,36)
	assert_eq(battle.controlled_units().filter(func(u):return u.limits.hp>0).size(),party.student_ids.size())
	trial._refresh()
	assert_true(trial.text_label.text.begins_with("\n".join(pages[0].map(func(r):return r.text))),"original scene 35 ending")
	print("FIELD35 sub ",battle.ending_sub," ticks ",trace.ticks," ending ",JSON.stringify(pages))
	trial.continue_button.pressed.emit()
	assert_eq(model.stage(),"sortie_result")
	if model.stage()!="sortie_result":return false
	var view: Dictionary=model.read_postbattle()
	var summary: Dictionary=view.planning.sortie_summary
	assert_eq([summary.date,summary.scene_id,summary.history_index],[[8,5],35,24])
	assert_eq([summary.result_selector,summary.task_grade,summary.score.total_delta,summary.lessons.bonus,summary.recipient,view.bundle.school.global_total_511c],[4,4,89098,1010,5,1930708])
	assert_eq(summary.students.map(func(r):return r.character_id),party.student_ids)
	assert_eq(summary.lessons.students.map(func(r):return [r.character_id,r.work_id]),lessons)
	assert_eq(view.bundle.school.global_total_511c,1840600+summary.score.total_delta+summary.lessons.bonus)
	for r in view.bundle.records:assert_eq(r.week_records[72],2 if r.character_id in party.student_ids else 1)
	assert_eq(model.export_save().version,26)
	assert_false(model.execute({"op":"sortie_finish","trace":trace}).supported)
	print("RESULT35 ",JSON.stringify({"selector":summary.result_selector,"grade":summary.task_grade,"score":summary.score.total_delta,"bonus":summary.lessons.bonus,"total":view.bundle.school.global_total_511c,"mvp":summary.recipient,"loot":summary.loot_groups}))
	panel.find_child("continue_sortie_story",true,false).pressed.emit()
	return true


func _school(ui, path: String) -> void:
	var panel=ui.postbattle_panel
	var model=ui.model
	var dated:=Model.Postbattle.SortieWeek.story(5,8)
	assert_eq([dated.pre_week.size(),dated.week_start.size(),dated.school_entry.size()],[0,157,0])
	var v: Dictionary=model.read_postbattle()
	assert_eq(v.phase,"new_week_story")
	assert_eq(v.get("date_card",{}).get("image"),"res://assets/school_story/tc0901.png")
	assert_true(panel.card_frame.visible and panel.card_image.texture!=null,"September date card")
	panel.next.pressed.emit()
	for expected in dated.week_start:
		v=model.read_postbattle()
		assert_eq(v.phase,"new_week_story")
		assert_eq(v.page,expected)
		assert_eq([panel.speaker.text,panel.dialogue.text],[expected.speaker,expected.text])
		if v.phase!="new_week_story":return
		panel.next.pressed.emit()
	v=model.read_postbattle()
	assert_eq(v.phase,"post_workroom")
	assert_eq([v.bundle.flags["0x7a55f6"],v.bundle.flags["0x7e11a0"],v.bundle.adv_background],[11,0,14])
	panel.next.pressed.emit()
	v=model.read_postbattle()
	assert_eq(v.phase,"returned_school")
	if v.phase!="returned_school":return
	var school: Dictionary=v.bundle.school
	assert_eq([school.month,school.week,school.teacher_count,school.student_count,school.adventure_gate],[9,1,5,11,0])
	assert_eq([v.bundle.flags["0x7a55f6"],v.bundle.flags["0x7e11a0"]],[11,1])
	assert_eq(school.derived_student_ids,ROSTER)
	assert_eq(Model.Postbattle.Adventures.available(v.planning.ledger).map(func(r):return r.id),[35,17])
	assert_eq(school.lecture_work_fields,[0,1,35,0])
	for group in SORTIE_GROUPS:
		panel.find_child("mode_%d_1"%group,true,false).pressed.emit()
	for selection in [[0,7],[1,19],[2,24],[3,30],[4,36]]:
		var option: OptionButton=panel.find_child("courses_%d"%selection[0],true,false)
		var index:=option.get_item_index(selection[1])
		assert_true(index>0 and not option.disabled,"September course %d"%selection[1])
		if index<=0 or option.disabled:return
		if option.get_selected_id()!=selection[1]:option.item_selected.emit(index)
	ui.save_path=path
	panel.save_requested.emit()
	assert_true(FileAccess.file_exists(path),"September save written")
	var fresh:=August.Prior.August.new()._screen()
	fresh.save_path=path
	fresh.load_button.pressed.emit()
	assert_eq(fresh.model.state(),model.state())
	assert_eq(fresh.model.export_save(),model.export_save())
	for group in range(5):assert_eq(fresh.postbattle_panel.find_child("courses_%d"%group,true,false).get_selected_id(),[7,19,24,30,36][group])
	var altered: Dictionary=fresh.model.export_save()
	altered.rules.september_one_story="changed"
	assert_eq(fresh.model.restore(altered).get("reason"),"save_rules_changed")
	print("SEPTEMBER ",model.export_save().state_sha256," commands ",model.export_save().commands.size())
	fresh.free()
