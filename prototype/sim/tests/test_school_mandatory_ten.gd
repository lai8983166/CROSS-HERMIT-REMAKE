extends "res://sim/tests/test_base.gd"
const Prior := preload("res://sim/tests/test_school_mandatory_six.gd")
const Model := preload("res://sim/school_playground.gd")
const UI := preload("res://sim/tests/test_school_combat_handoff.gd")


func _save() -> Dictionary:
	var prior := Prior.new()
	var saved: Dictionary=prior._save()
	var delta: Dictionary=prior._fixture("june_week3_saved_plan")
	assert_eq(saved["state_sha256"],delta["parent"])
	saved["commands"].append({"op":"return_depart"})
	saved["commands"].append({"op":"sortie_finish","trace":prior._fixture("mandatory_six_victory_trace")["trace"]})
	saved["commands"].append_array(delta["after_battle"])
	saved["rules"].merge(delta["rules_added"])
	for key in ["context","version","state_sha256"]: saved[key]=delta[key]
	return saved


func test_saved_party_through_ten_and_next_school() -> void:
	var ui = UI.new()._school_ui()
	var path := "user://mandatory-ten-%s.json" % Time.get_ticks_usec()
	_play(ui,_save(),path)
	if FileAccess.file_exists(path): DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	ui.free()


func _play(ui, saved: Dictionary, path: String) -> void:
	var result: Dictionary=ui.model.restore_text(JSON.stringify(saved))
	assert_true(result["supported"],str(result))
	if not result["supported"]:return
	assert_eq(ui.model.export_save(),saved)
	assert_false(ui.model.execute({"op":"return_select","adventure":17})["supported"])
	assert_false(ui.model.execute({"op":"return_settle"})["supported"])
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
	assert_eq(party,{"scene_id":10,"teacher_ids":[101,110,115],"student_ids":[3,4,8,6,1,2],"student_groups":[0,0,1,2,2,2]})
	var pending: Dictionary=ui.model.export_save()
	assert_eq(pending["version"],15)
	var downgraded := pending.duplicate(true)
	for key in ["version","context","rules"]: downgraded[key]=saved[key]
	assert_eq(ui.model.restore(downgraded).get("reason"),"save_work_version_mismatch")
	assert_eq(ui.model.export_save(),pending)
	assert_eq(Model.Postbattle.Adventures.available(view["planning"]["ledger"]).map(func(r):return r["id"]),[17])
	panel.find_child("play_sortie",true,false).pressed.emit()
	var trial=ui.sortie_trial
	var battle=trial.session
	assert_true(battle.ready)
	if not battle.ready:return
	var example: Dictionary=Prior.new()._fixture("mandatory_ten_victory_trace")
	assert_eq(example["parent"],saved["state_sha256"])
	var run := Model.BattleRecord.run_trace(battle,example["trace"])
	assert_true(run["supported"],str(run))
	if not run["supported"]:return
	assert_true(battle.ending_sub in [2,5,8])
	assert_eq(battle.battle_trace(),example["trace"])
	var facts: Dictionary=battle.result_inputs()
	trial._refresh()
	trial.continue_button.pressed.emit()
	assert_eq(ui.model.stage(),"sortie_result")
	if ui.model.stage()!="sortie_result":return
	var settled: Dictionary=ui.model.read_postbattle()
	var summary: Dictionary=settled["planning"]["sortie_summary"]
	assert_eq([summary["scene_id"],summary["date"],summary["history_index"]],[10,[6,3],12])
	assert_eq(summary["result_selector"],facts["result_selector"])
	assert_eq(summary["students"].map(func(r):return r["character_id"]),party["student_ids"])
	assert_eq(settled["bundle"]["school"]["global_total_511c"],view["bundle"]["school"]["global_total_511c"]+summary["score"]["total_delta"])
	for id in party["student_ids"]:
		assert_eq(Model.Postbattle.Return._find(settled["bundle"]["records"],id)["week_records"][36],2)
	assert_false(ui.model.execute({"op":"sortie_finish","trace":example["trace"]})["supported"])
	panel.find_child("continue_sortie_story",true,false).pressed.emit()
	assert_eq(ui.model.stage(),"new_week_story")
	if ui.model.stage()!="new_week_story":return
	var next_week: Dictionary=ui.model.read_postbattle()
	assert_eq([next_week["page"]["chapter"],next_week["total"]],[213,13])
	assert_eq(next_week["bundle"]["school"]["student_count"],8)
	panel.skip_dialog.confirmed.emit()
	assert_eq(ui.model.stage(),"post_workroom")
	panel.next.pressed.emit()
	assert_eq(ui.model.stage(),"returned_school")
	if ui.model.stage()!="returned_school":return
	var school: Dictionary=ui.model.read_postbattle()["bundle"]["school"]
	assert_eq([school["month"],school["week"],school["lecture_work_fields"]],[6,4,[3,12,13,0]])
	assert_true(panel.find_child("adventure_13",true,false).button_pressed)
	panel.find_child("member_5",true,false).pressed.emit()
	panel.assignments.get_child(2).get_child(5).pressed.emit()
	assert_eq(ui.model.export_save()["commands"][-1],{"op":"return_move","kind":"student","member_id":5,"target_group":2,"target_slot":3})
	assert_true(ui.model.save_file(path)["supported"])
	var fresh := Model.new()
	var loaded := fresh.load_file(path)
	assert_true(loaded["supported"],str(loaded))
	if not loaded["supported"]:return
	assert_eq(fresh.state(),ui.model.state())
	assert_eq(fresh.export_save(),ui.model.export_save())
	var altered: Dictionary=fresh.export_save()
	altered["rules"]["ten_battle"]="changed"
	assert_eq(fresh.restore(altered).get("reason"),"save_rules_changed")
