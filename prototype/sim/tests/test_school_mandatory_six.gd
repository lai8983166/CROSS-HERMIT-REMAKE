extends "res://sim/tests/test_base.gd"
const Prior := preload("res://sim/tests/test_school_mandatory_four.gd")
const Model := preload("res://sim/school_playground.gd")
const UI := preload("res://sim/tests/test_school_combat_handoff.gd")


func _fixture(name: String) -> Dictionary:
	return Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://sim/tests/"+name+".json")))


func _save() -> Dictionary:
	var saved: Dictionary=Prior.new()._saves()[0]
	var delta := _fixture("june_week2_saved_plan")
	assert_eq(saved["state_sha256"],delta["parent"])
	var four := _fixture("mandatory_four_victory_trace")
	saved["commands"].append({"op":"return_depart"})
	saved["commands"].append({"op":"sortie_finish","trace":four["trace"]})
	for part in delta["after_battle"]:
		for i in part["repeat"]: saved["commands"].append(part["command"])
	saved["rules"].merge(delta["rules_added"])
	for key in ["context","version","state_sha256"]: saved[key]=delta[key]
	return saved


func test_saved_party_through_six_and_next_school() -> void:
	var ui = UI.new()._school_ui()
	var path := "user://mandatory-six-%s.json" % Time.get_ticks_usec()
	_play(ui,_save(),path)
	if FileAccess.file_exists(path): DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	ui.free()


func _play(ui, saved: Dictionary, path: String) -> void:
	var result: Dictionary=ui.model.restore_text(JSON.stringify(saved))
	assert_true(result["supported"],str(result))
	if not result["supported"]:return
	assert_eq(ui.model.export_save(),saved)
	ui.refresh()
	var panel=ui.postbattle_panel
	var depart=panel.find_child("depart",true,false)
	assert_true(depart!=null and not depart.disabled)
	if depart==null or depart.disabled:return
	depart.pressed.emit()
	panel.commit_dialog.hide()
	panel.commit_dialog.confirmed.emit()
	assert_eq(ui.model.stage(),"sortie_pending")
	if ui.model.stage()!="sortie_pending":return
	var view: Dictionary=ui.model.read_postbattle()
	var party: Dictionary=view["planning"]["handoff"]["prepared"]["rounds"][0]
	assert_eq(party,{"scene_id":6,"teacher_ids":[101,110,115],"student_ids":[3,8,6,1,2],"student_groups":[0,1,2,2,2]})
	var prior: Dictionary=view["bundle"]
	assert_eq(ui.model.export_save()["version"],14)
	panel.find_child("play_sortie",true,false).pressed.emit()
	var trial=ui.sortie_trial
	var battle=trial.session
	assert_true(battle.ready)
	if not battle.ready:return
	var example := _fixture("mandatory_six_victory_trace")
	assert_eq(example["parent"],saved["state_sha256"])
	var run := Model.BattleRecord.run_trace(battle,example["trace"])
	assert_true(run["supported"],str(run))
	if not run["supported"]:return
	assert_eq(battle.ending_sub,8)
	assert_eq(battle.battle_trace(),example["trace"])
	var facts: Dictionary=battle.result_inputs()
	trial._refresh()
	trial.continue_button.pressed.emit()
	assert_eq(ui.model.stage(),"sortie_result")
	if ui.model.stage()!="sortie_result":return
	view=ui.model.read_postbattle()
	var summary: Dictionary=view["planning"]["sortie_summary"]
	assert_eq([summary["scene_id"],summary["date"],summary["history_index"]],[6,[6,2],11])
	assert_eq(summary["result_selector"],facts["result_selector"])
	assert_eq(summary["students"].map(func(r):return r["character_id"]),party["student_ids"])
	assert_eq(view["bundle"]["school"]["global_total_511c"],prior["school"]["global_total_511c"]+summary["score"]["total_delta"])
	assert_eq([summary["task_grade"],summary["score"]["total_delta"],summary["recipient"]],[3,55834,3])
	for id in party["student_ids"]:
		assert_eq(Model.Postbattle.Return._find(view["bundle"]["records"],id)["week_records"][33],2)
	assert_false(ui.model.execute({"op":"sortie_finish","trace":example["trace"]})["supported"])
	panel.find_child("continue_sortie_story",true,false).pressed.emit()
	assert_eq(ui.model.read_postbattle()["total"],140)
	panel.skip_dialog.confirmed.emit()
	assert_eq(ui.model.read_postbattle()["total"],35)
	panel.skip_dialog.confirmed.emit()
	assert_eq(ui.model.stage(),"post_workroom")
	panel.next.pressed.emit()
	assert_eq(ui.model.stage(),"returned_school")
	if ui.model.stage()!="returned_school":return
	var school: Dictionary=ui.model.read_postbattle()["bundle"]["school"]
	assert_eq([school["month"],school["week"],school["lecture_work_fields"]],[6,3,[3,9,10,0]])
	assert_true(panel.find_child("adventure_10",true,false).button_pressed)
	panel.find_child("member_4",true,false).pressed.emit()
	panel.assignments.get_child(0).get_child(5).pressed.emit()
	assert_eq(ui.model.export_save()["commands"][-1],{"op":"return_move","kind":"student","member_id":4,"target_group":0,"target_slot":3})
	assert_true(ui.model.save_file(path)["supported"])
	var fresh := Model.new()
	assert_true(fresh.load_file(path)["supported"])
	assert_eq(fresh.export_save()["state_sha256"],"b34615815f3311061f13c2cd5eb06b8d9302fe34bfea66e4998a01bb29e573b5")
	assert_eq(fresh.state(),ui.model.state())
	assert_eq(fresh.export_save(),ui.model.export_save())
	var altered: Dictionary=fresh.export_save()
	altered["rules"]["six_battle"]="changed"
	assert_eq(fresh.restore(altered).get("reason"),"save_rules_changed")
