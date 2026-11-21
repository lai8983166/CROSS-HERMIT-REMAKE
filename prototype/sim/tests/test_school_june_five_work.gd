extends "res://sim/tests/test_base.gd"
const Prior := preload("res://sim/tests/test_school_mandatory_thirteen.gd")
const Model := preload("res://sim/school_playground.gd")


func _save() -> Dictionary:
	var saved := Prior.new()._save()
	var delta: Dictionary=Prior.Fixtures.new()._fixture("june_week5_saved_plan")
	assert_eq(saved["state_sha256"],delta["parent"])
	saved["commands"].append({"op":"return_depart"})
	saved["commands"].append({"op":"sortie_finish","trace":Prior.Fixtures.new()._fixture("mandatory_thirteen_victory_trace")["trace"]})
	saved["commands"].append_array(delta["after_battle"])
	saved["rules"].merge(delta["rules_added"])
	for key in ["version","context","state_sha256"]:saved[key]=delta[key]
	return saved


func test_four_saved_courses_through_july() -> void:
	_round_trip(false)


func test_training_and_lessons_through_july() -> void:
	_round_trip(true)


func _round_trip(sortie: bool) -> void:
	var path := "user://july-week1-%s.json" % Time.get_ticks_usec()
	_play(_save(),sortie,path)
	if FileAccess.file_exists(path):DirAccess.remove_absolute(ProjectSettings.globalize_path(path))


func _play(saved: Dictionary, sortie: bool, path: String) -> void:
	var ui=Prior.UI.new()._school_ui()
	var model=ui.model
	var result: Dictionary=model.restore(saved)
	assert_true(result["supported"],str(result))
	if result["supported"]:
		assert_eq(model.export_save(),saved)
		ui.refresh()
		_commit_week(ui,sortie,path)
	ui.free()


func _commit_week(ui, sortie: bool, path: String) -> void:
	var panel=ui.postbattle_panel
	var model=ui.model
	assert_eq(model.read_postbattle()["bundle"]["ratings"].map(func(r):return r["state"]),[4,4,4,4,0])
	if sortie:
		panel.find_child("mode_2_0",true,false).pressed.emit()
		panel.find_child("adventure_17",true,false).pressed.emit()
	var button=panel.find_child("depart" if sortie else "settle",true,false)
	assert_true(button!=null and not button.disabled)
	if button==null or button.disabled:return
	button.pressed.emit()
	panel.commit_dialog.hide()
	panel.commit_dialog.confirmed.emit()
	if sortie:
		assert_eq(model.stage(),"sortie_pending")
		if model.stage()!="sortie_pending":return
		var hand: Dictionary=model.read_postbattle()["planning"]["handoff"]
		assert_eq(hand["prepared"]["rounds"][0],{"scene_id":17,"teacher_ids":[115],"student_ids":[6,1,2,5],"student_groups":[2,2,2,2]})
		panel.find_child("play_sortie",true,false).pressed.emit()
		var trial=ui.sortie_trial
		var battle=trial.session
		assert_true(battle.ready)
		if not battle.ready:return
		var trace: Dictionary=Prior.Fixtures.new()._fixture("june_week5_training_trace")
		var replay: Dictionary=Model.BattleRecord.run_trace(battle,trace)
		assert_true(replay["supported"],str(replay))
		assert_eq([battle.ending_sub,battle._at_exit(),battle.battle_trace()["ticks"]],[14,true,2568])
		if not replay["supported"] or battle.ending_sub<0:return
		trial._refresh()
		trial.continue_button.pressed.emit()
	assert_eq(model.stage(),"sortie_result" if sortie else "course_result")
	if model.stage() not in ["sortie_result","course_result"]:return
	var settled: Dictionary=model.read_postbattle()
	var summary: Dictionary=settled["planning"]["sortie_summary" if sortie else "course_summary"]
	var lessons: Dictionary=summary["lessons"] if sortie else summary
	assert_eq(summary["date"],[6,5])
	assert_eq(summary["history_index"],14)
	if sortie:
		assert_eq(summary["students"].map(func(r):return r["character_id"]),[6,1,2,5])
		assert_eq(summary["result_selector"],5)
	else:
		assert_eq([summary["bonus"],summary["recipient"]],[106500,9])
	var expected_total: int=550936+lessons["bonus"]
	if sortie:expected_total+=summary["score"]["total_delta"]
	assert_eq(settled["bundle"]["school"]["global_total_511c"],expected_total)
	assert_eq(lessons["students"].map(func(r):return [r["character_id"],r["work_id"]]),[[3,8],[4,8],[8,19],[9,28]] if sortie else [[3,8],[4,8],[8,19],[6,26],[1,26],[2,26],[5,26],[9,28]])
	for id in [1,2,3,4,5,6,8,9]:
		assert_eq(Model.Postbattle.Return._find(settled["bundle"]["records"],id)["week_records"][42],2 if sortie and id in [6,1,2,5] else 1)
	assert_eq(model.export_save()["version"],17)
	assert_false(model.execute({"op":"return_settle"})["supported"])
	panel.find_child("continue_sortie_story" if sortie else "continue_course_story",true,false).pressed.emit()
	var start: Dictionary=model.read_postbattle()
	assert_eq(model.stage(),"new_week_story")
	if model.stage()!="new_week_story":return
	assert_eq([start["total"],start["page"]["chapter"]],[51,303])
	panel.skip_dialog.confirmed.emit()
	assert_eq(model.stage(),"post_workroom")
	panel.next.pressed.emit()
	assert_eq(model.stage(),"returned_school")
	if model.stage()!="returned_school":return
	var school: Dictionary=model.read_postbattle()["bundle"]["school"]
	assert_eq([school["month"],school["week"],school["teacher_count"],school["student_count"]],[7,1,4,8])
	assert_eq(Model.Postbattle.Adventures.available(model.read_postbattle()["planning"]["ledger"]).map(func(r):return r["id"]),[18,17])
	panel.find_child("adventure_18",true,false).pressed.emit()
	panel.find_child("mode_2_1",true,false).pressed.emit()
	var courses=panel.find_child("courses_2",true,false)
	var idx: int=courses.get_item_index(27)
	assert_true(idx>0)
	if idx<=0:return
	courses.item_selected.emit(idx)
	school=model.read_postbattle()["bundle"]["school"]
	assert_eq(school["lecture_work_fields"][2],18)
	assert_eq(Model.Postbattle.Return.Groups._word(school["group_raw_bytes"],2*28+10),27)
	assert_true(model.save_file(path)["supported"])
	var fresh := Model.new()
	var loaded := fresh.load_file(path)
	assert_true(loaded["supported"],str(loaded))
	if not loaded["supported"]:return
	assert_eq(fresh.state(),model.state())
	assert_eq(fresh.export_save(),model.export_save())
	var changed := fresh.export_save()
	changed["rules"]["june_five_courses"]="altered"
	assert_eq(fresh.restore(changed).get("reason"),"save_rules_changed")


func test_text_size_limits_include_the_new_save_version() -> void:
	var model := Model.new()
	var padding := " ".repeat(Model.MAX_BYTES)
	assert_eq(model.restore_text(JSON.stringify({"version":17})+padding).get("reason"),"invalid_save")
	assert_eq(model.restore_text(JSON.stringify({"version":4})+padding).get("reason"),"save_too_large")
	assert_eq(model.restore_text(" ".repeat(Model.POST_MAX_BYTES+1)).get("reason"),"save_too_large")
