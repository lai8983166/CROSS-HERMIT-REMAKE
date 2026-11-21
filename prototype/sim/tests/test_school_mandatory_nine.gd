extends "res://sim/tests/test_base.gd"
const July := preload("res://sim/tests/test_school_july_eighteen.gd")
const Fixtures := preload("res://sim/tests/test_school_mandatory_six.gd")
const UI := preload("res://sim/tests/test_school_combat_handoff.gd")
const Model := preload("res://sim/school_playground.gd")


func _save() -> Dictionary:
	var parent := July.new()._save()
	var fixtures := Fixtures.new()
	var delta := fixtures._fixture("july_week3_saved_plan")
	assert_eq(parent.state_sha256,delta.parent)
	parent.commands.append_array(delta.before_battle)
	parent.commands.append({"op":"sortie_finish","trace":fixtures._fixture("july_eighteen_victory_trace").trace})
	parent.commands.append_array(delta.after_battle)
	for i in range(delta.chapter209_pages):parent.commands.append({"op":"post_next"})
	parent.commands.append_array(delta.after_chapter)
	parent.rules.merge(delta.rules_added)
	for key in ["version","context","state_sha256"]:parent[key]=delta[key]
	return parent


func test_saved_party_wins_and_replans_at_next_school() -> void:
	var path := "user://july-four-%s.json" % Time.get_ticks_usec()
	_play(_save(),path)
	if FileAccess.file_exists(path):DirAccess.remove_absolute(ProjectSettings.globalize_path(path))


func _play(saved: Dictionary, path: String) -> void:
	var ui=UI.new()._school_ui()
	var restored: Dictionary=ui.model.restore(saved)
	assert_true(restored.supported,str(restored))
	if restored.supported:
		assert_eq(ui.model.export_save(),saved)
		ui.refresh()
		_depart(ui,saved,path)
	ui.free()


func _mission() -> Dictionary:
	return {"scene":9,"week":3,"opening_total":712166,"students":[3,4,8,1,6,2,5,9],
		"groups":[0,0,1,1,2,2,2,3],"version":19,"trace":"mandatory_nine_victory_trace"}


func _depart(ui, saved: Dictionary, path: String) -> void:
	var model=ui.model
	var panel=ui.postbattle_panel
	var mission := _mission()
	var school: Dictionary=model.read_postbattle().bundle.school
	assert_eq([school.month,school.week,school.lecture_work_fields,school.global_total_511c],[7,mission.week,[3,mission.scene-1,mission.scene,0],mission.opening_total])
	for rejected in [{"op":"return_select","adventure":17},{"op":"return_settle"},{"op":"return_mode","group":2,"teaching":true}]:
		assert_false(model.execute(rejected).supported)
	assert_eq(model.export_save(),saved)
	var depart=panel.find_child("depart",true,false)
	assert_true(depart!=null and not depart.disabled)
	if depart==null or depart.disabled:return
	depart.pressed.emit()
	panel.commit_dialog.hide()
	panel.commit_dialog.confirmed.emit()
	assert_eq(model.stage(),"sortie_pending")
	if model.stage()!="sortie_pending":return
	var hand: Dictionary=model.read_postbattle().planning.handoff
	var party: Dictionary=hand.prepared.rounds[0]
	assert_eq(party,{"scene_id":mission.scene,"teacher_ids":[101,110,115,118],"student_ids":mission.students,"student_groups":mission.groups})
	assert_eq(model.export_save().version,mission.version)
	assert_eq(model.export_save().commands[-1],{"op":"return_depart"})
	panel.find_child("play_sortie",true,false).pressed.emit()
	var trial=ui.sortie_trial
	var session=trial.session
	assert_true(session.ready)
	if not session.ready:return
	var fixture:=Fixtures.new()._fixture(mission.trace)
	assert_eq(fixture.parent,saved.state_sha256)
	var replay:=Model.BattleRecord.run_trace(session,fixture.trace)
	assert_true(replay.supported,str(replay))
	if not replay.supported:return
	assert_eq(session.ending_sub,fixture.ending_sub)
	assert_true(session.ending_sub in [2,5,8])
	assert_eq(session.battle_trace(),fixture.trace)
	var facts: Dictionary=session.result_inputs()
	trial._refresh()
	trial.continue_button.pressed.emit()
	assert_eq(model.stage(),"sortie_result")
	if model.stage()!="sortie_result":return
	var view: Dictionary=model.read_postbattle()
	var result: Dictionary=view.planning.sortie_summary
	assert_eq([result.scene_id,result.date,result.history_index,result.result_selector],[mission.scene,[7,mission.week],14+mission.week,facts.result_selector])
	assert_eq(result.students.map(func(s):return s.character_id),party.student_ids)
	assert_eq(view.bundle.school.global_total_511c,mission.opening_total+result.score.total_delta)
	for id in party.student_ids:
		assert_eq(Model.Postbattle.Return._find(view.bundle.records,id).week_records[3*result.history_index],2)
	assert_false(model.execute({"op":"sortie_finish","trace":fixture.trace}).supported)
	panel.find_child("continue_sortie_story",true,false).pressed.emit()
	_read_and_replan(ui,path)


func _read_and_replan(ui, path: String) -> void:
	var model=ui.model
	var panel=ui.postbattle_panel
	var dated:=Model.Postbattle.SortieWeek.story(3,7)
	assert_eq(dated.pre_week,[])
	var card: Dictionary=model.read_postbattle()
	assert_eq(model.stage(),"new_week_story")
	assert_eq(card.get("date_card",{}).get("image"),"res://assets/school_story/tc0704.png")
	assert_true(panel.card_frame.visible and panel.card_image.texture!=null)
	panel.next.pressed.emit()
	for page in dated.week_start:
		assert_eq(model.stage(),"new_week_story")
		assert_false(panel.card_frame.visible)
		assert_eq(model.read_postbattle().page,page)
		assert_eq(page.chapter,214)
		panel.next.pressed.emit()
	assert_eq(model.stage(),"post_workroom")
	panel.next.pressed.emit()
	assert_eq(model.stage(),"returned_school")
	if model.stage()!="returned_school":return
	var view: Dictionary=model.read_postbattle()
	var school: Dictionary=view.bundle.school
	assert_eq([school.month,school.week,school.adventure_gate,school.lecture_work_fields],[7,4,1,[3,13,14,0]])
	assert_eq([school.teacher_count,school.student_count],[4,8])
	assert_eq(Model.Postbattle.Adventures.available(view.planning.ledger).map(func(a):return a.id),[14,17])
	assert_false(model.execute({"op":"return_select","adventure":17}).supported)
	assert_false(model.execute({"op":"return_settle"}).supported)
	panel.find_child("member_1",true,false).pressed.emit()
	panel.assignments.get_child(3).get_child(3).pressed.emit()
	assert_eq(model.export_save().commands[-1],{"op":"return_move","kind":"student","member_id":1,"target_group":3,"target_slot":1})
	assert_eq(model.export_save().version,19)
	assert_true(model.save_file(path).supported)
	var fresh:=Model.new()
	var loaded:=fresh.load_file(path)
	assert_true(loaded.supported,str(loaded))
	if not loaded.supported:return
	assert_eq(fresh.state(),model.state())
	assert_eq(fresh.export_save(),model.export_save())
	var altered:=fresh.export_save()
	altered.rules.nine_battle="changed"
	assert_eq(fresh.restore(altered).get("reason"),"save_rules_changed")
