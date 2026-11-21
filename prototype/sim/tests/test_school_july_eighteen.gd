extends "res://sim/tests/test_base.gd"
const Prior := preload("res://sim/tests/test_school_june_five_work.gd")
const Model := preload("res://sim/school_playground.gd")
const Dated := preload("res://sim/school_sortie_week.gd")


func _save() -> Dictionary:
	var saved := Prior.new()._save()
	var delta: Dictionary=Prior.Prior.Fixtures.new()._fixture("july_week1_saved_plan")
	assert_eq(saved.state_sha256,delta.parent)
	saved.commands.append_array(delta.commands)
	saved.rules.merge(delta.rules_added)
	for key in ["version","context","state_sha256"]:saved[key]=delta[key]
	return saved


func test_participate_then_continue_to_mandatory_nine() -> void:
	_round_trip(true)


func test_capture_castle_then_continue_to_mandatory_nine() -> void:
	_round_trip(true,true)


func test_expire_then_continue_to_mandatory_nine() -> void:
	_round_trip(false)


func _round_trip(attend: bool, victory := false) -> void:
	var path := "user://july-three-%s.json" % Time.get_ticks_usec()
	_play(_save(),attend,path,victory)
	if FileAccess.file_exists(path):DirAccess.remove_absolute(ProjectSettings.globalize_path(path))


func _play(saved: Dictionary, attend: bool, path: String, victory := false) -> void:
	var ui=Prior.Prior.UI.new()._school_ui()
	var restored: Dictionary=ui.model.restore(saved)
	assert_true(restored.supported,str(restored))
	if restored.supported:
		assert_eq(ui.model.export_save(),saved)
		ui.refresh()
		_play_weeks(ui,attend,path,victory)
	ui.free()


func _confirm(panel, button_name: String) -> bool:
	var button=panel.find_child(button_name,true,false)
	assert_true(button!=null and not button.disabled,button_name)
	if button==null or button.disabled:return false
	button.pressed.emit()
	panel.commit_dialog.hide()
	panel.commit_dialog.confirmed.emit()
	return true


func _play_weeks(ui, attend: bool, path: String, victory: bool) -> void:
	var panel=ui.postbattle_panel
	var model=ui.model
	var start: Dictionary=model.read_postbattle()
	var opening:=int(start.bundle.school.global_total_511c)
	assert_eq([start.bundle.school.month,start.bundle.school.week,start.bundle.school.lecture_work_fields[2]],[7,1,18])
	assert_eq(Model.Postbattle.Adventures.available(start.planning.ledger)[0].remaining,1)
	var lesson_rows := []
	var party := {"scene_id":18,"teacher_ids":[],"student_ids":[],"student_groups":[]}
	var groups: Array=[]
	var receipt: Dictionary={}
	if attend:
		receipt=Prior.Prior.Fixtures.new()._fixture("july_eighteen_victory_trace" if victory else "july_eighteen_participation_trace")
		assert_eq(receipt.parent,model.export_save().state_sha256)
		groups=receipt.groups
	for group in range(4):
		var members: Array=[[3,4],[8],[6,1,2,5],[9]][group]
		if group in groups:
			panel.find_child("mode_%d_0" % group,true,false).pressed.emit()
			party.teacher_ids.append([101,110,115,118][group])
			for id in members:
				party.student_ids.append(id)
				party.student_groups.append(group)
		else:
			for id in members:lesson_rows.append([id,[8,19,27,28][group]])
	if attend:
		if not _confirm(panel,"depart"):return
		assert_eq(model.stage(),"sortie_pending")
		if model.stage()!="sortie_pending":return
		var hand: Dictionary=model.read_postbattle().planning.handoff
		assert_eq(hand.prepared.rounds[0],party)
		panel.find_child("play_sortie",true,false).pressed.emit()
		var battle=ui.sortie_trial.session
		assert_true(battle.ready)
		if not battle.ready:return
		var result:=Model.BattleRecord.run_trace(battle,receipt.trace)
		assert_true(result.supported,str(result))
		assert_eq(battle.ending_sub,receipt.ending_sub)
		assert_eq(receipt.ending_sub,8 if victory else 14)
		if not result.supported or battle.ending_sub!=receipt.ending_sub:return
		ui.sortie_trial._refresh()
		ui.sortie_trial.continue_button.pressed.emit()
	else:
		if not _confirm(panel,"settle"):return
	assert_eq(model.stage(),"sortie_result" if attend else "course_result")
	if model.stage() not in ["sortie_result","course_result"]:return
	var settled: Dictionary=model.read_postbattle()
	var summary: Dictionary=settled.planning.sortie_summary if attend else settled.planning.course_summary
	var lessons: Dictionary=summary.lessons if attend else summary
	var expected_total: int=opening+lessons.bonus
	if attend:
		assert_eq(summary.scene_id,18)
		expected_total+=summary.score.total_delta
	assert_eq(settled.bundle.school.global_total_511c,expected_total)
	assert_eq(summary.history_index,15)
	assert_eq(lessons.students.map(func(r):return [r.character_id,r.work_id]),lesson_rows)
	for id in [3,4,8,6,1,2,5,9]:
		assert_eq(Model.Postbattle.Return._find(settled.bundle.records,id).week_records[45],2 if id in party.student_ids else 1)
	panel.find_child("continue_sortie_story" if attend else "continue_course_story",true,false).pressed.emit()
	var card: Dictionary=model.read_postbattle()
	assert_eq([model.stage(),card.total],["new_week_story",0])
	assert_true(card.has("date_card") and panel.card_frame.visible and panel.card_image.texture!=null)
	if not card.has("date_card"):return
	assert_eq(card.date_card.image,"res://assets/school_story/tc0702.png")
	if attend:
		panel.next.pressed.emit()
	else:
		# The source counts VM updates independently of the frame's wall time.
		# Drive the panel countdown explicitly since this test runs headless.
		for i in range(card.date_card.wait_ticks-1):
			panel._process(0.0)
		assert_eq(model.stage(),"new_week_story")
		panel._process(0.0)
	assert_eq(model.stage(),"post_workroom")
	panel.next.pressed.emit()
	assert_eq(model.stage(),"returned_school")
	if model.stage()!="returned_school":return
	var second: Dictionary=model.read_postbattle()
	assert_eq([second.bundle.school.month,second.bundle.school.week,second.bundle.school.lecture_active],[7,2,0])
	assert_eq(Model.Postbattle.Adventures.available(second.planning.ledger).map(func(r):return r.id),[17])
	assert_eq(second.planning.ledger.unlock_flags[17],1)
	assert_false(model.execute({"op":"return_select","adventure":18}).supported)
	for group in groups:panel.find_child("mode_%d_1" % group,true,false).pressed.emit()
	if not _confirm(panel,"settle"):return
	assert_eq(model.stage(),"course_result")
	if model.stage()!="course_result":return
	assert_eq(model.read_postbattle().planning.course_summary.history_index,16)
	panel.find_child("continue_course_story",true,false).pressed.emit()
	var story: Dictionary=Dated.story(2,7)
	assert_eq(model.stage(),"new_week_story")
	if model.stage()!="new_week_story":return
	assert_eq(story.week_start.size(),52)
	for page in story.week_start:
		assert_eq(model.read_postbattle().page,page)
		assert_eq(page.chapter,209)
		panel.next.pressed.emit()
	assert_eq(model.stage(),"post_workroom")
	panel.next.pressed.emit()
	if model.stage()!="returned_school":
		_fail("Chapter209 did not return to school")
		return
	var school: Dictionary=model.read_postbattle().bundle.school
	assert_eq([school.month,school.week,school.adventure_gate,school.lecture_work_fields[2]],[7,3,1,9])
	assert_false(model.execute({"op":"return_select","adventure":17}).supported)
	assert_false(model.execute({"op":"return_settle"}).supported)
	panel.find_child("member_1",true,false).pressed.emit()
	panel.assignments.get_child(1).get_child(3).pressed.emit()
	assert_eq(model.export_save().commands[-1],{"op":"return_move","kind":"student","member_id":1,"target_group":1,"target_slot":1})
	assert_eq(model.export_save().version,18)
	assert_true(model.save_file(path).supported)
	var fresh:=Model.new()
	var loaded:=fresh.load_file(path)
	assert_true(loaded.supported,str(loaded))
	if not loaded.supported:return
	assert_eq(fresh.state(),model.state())
	assert_eq(fresh.export_save(),model.export_save())
	var altered:=fresh.export_save()
	altered.rules.adventure_eighteen="altered"
	assert_eq(fresh.restore(altered).get("reason"),"save_rules_changed")
