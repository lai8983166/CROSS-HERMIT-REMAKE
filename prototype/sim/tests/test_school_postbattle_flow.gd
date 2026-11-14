extends "res://sim/tests/test_base.gd"
const Helpers := preload("res://sim/tests/test_school_combat_session.gd")
const UIHelpers := preload("res://sim/tests/test_school_combat_handoff.gd")
const Record := preload("res://sim/school_battle_record.gd")
const Model := preload("res://sim/school_playground.gd")
const Flow := preload("res://sim/school_postbattle_flow.gd")
const Settlement := preload("res://sim/school_battle_settlement.gd")
const BattleTests := preload("res://sim/tests/test_school_battle_settlement.gd")


func _trace() -> Dictionary:
	return Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_postbattle_battle_record.json")))["trace"]


func _begin():
	var model = Helpers.new()._school()
	var result: Dictionary = model.execute({"op":"battle_finish","trace":_trace()})
	assert_true(result["supported"],str(result))
	return model


func _roundtrip(model) -> void:
	var restored := Model.new()
	assert_true(restored.restore_text(JSON.stringify(model.export_save()))["supported"])
	assert_eq(restored.state(),model.state())
	assert_eq(restored.export_save(),model.export_save())


func test_recorded_live_battle_story_week_school_and_all_save_boundaries() -> void:
	# 9,227 ticks / 114 accepted commands from an actual local battle, without
	# editing HP, units or result fields. This record ends in squad_defeated.
	var model = _begin()
	assert_eq(model.stage(),"post_story")
	assert_eq(model.export_save()["version"],5)
	var post: Dictionary = model.read_postbattle()
	assert_eq(post["result_summary"]["outcome"],"squad_defeated")
	assert_eq(post["bundle"]["school"]["student_ids"].slice(0,4),[3,4,9,5])
	assert_eq(post["page"]["chapter"],20);assert_eq(post["total"],324)
	assert_eq([post["bundle"]["school"]["month"],post["bundle"]["school"]["week"]],[4,5])
	_roundtrip(model)
	assert_true(model.execute({"op":"post_next"})["supported"])
	assert_eq(model.read_postbattle()["cursor"],1);_roundtrip(model)
	assert_true(model.execute({"op":"post_prev"})["supported"])
	assert_eq(model.read_postbattle()["bundle"],post["bundle"],"previous page never rejoins or reawards")
	assert_true(model.execute({"op":"post_skip"})["supported"])
	assert_eq(model.stage(),"new_week_story")
	post=model.read_postbattle()
	assert_eq(post["page"]["chapter"],22);assert_eq(post["total"],87)
	assert_eq([post["bundle"]["school"]["month"],post["bundle"]["school"]["week"]],[5,1])
	_roundtrip(model)
	assert_true(model.execute({"op":"post_skip"})["supported"])
	assert_eq(model.stage(),"post_workroom")
	assert_eq(model.read_postbattle()["bundle"]["flags"]["0x7a55f6"],9)
	_roundtrip(model)
	assert_true(model.execute({"op":"post_school"})["supported"])
	assert_eq(model.stage(),"returned_school")
	post=model.read_postbattle()
	assert_eq(post["bundle"]["school"]["idle_student_ids"],[5])
	assert_eq(post["bundle"]["flags"]["0x7a55f6"],11)
	assert_true(model.execute({"op":"return_move","kind":"student","member_id":5,"target_group":0,"target_slot":3})["supported"])
	assert_eq(model.read_postbattle()["bundle"]["school"]["derived_student_ids"][0],[3,4,9,5])
	_roundtrip(model)
	var final: Dictionary=model.export_save()
	assert_true(model.execute({"op":"post_school"})["supported"])
	for command in [{"op":"battle_finish","trace":_trace()},{"op":"post_skip"},{"op":"work_start"},{"op":"school_enter"}]:
		assert_false(model.execute(command)["supported"])
	assert_eq(model.export_save(),final,"no duplicate join, growth or week settlement")


func test_save_tampering_and_cached_context_refusal_are_atomic() -> void:
	var model = _begin();var good: Dictionary=model.export_save();var before: Dictionary=model.state()
	for mutate in [func(s):s["state_sha256"]="0".repeat(64),
		func(s):s["commands"][-1]["trace"]["commands"][0][2]=1,
		func(s):s["commands"][-1]["trace"]["ticks"]=0,
		func(s):s["commands"][-1]["trace"]["reward"]=99999,
		func(s):s["rules"]["postbattle_story"]="changed",
		func(s):s["commands"].append({"op":"post_school"})]:
		var bad := good.duplicate(true);mutate.call(bad)
		assert_false(model.restore(bad)["supported"]);assert_eq(model.state(),before)
	var fresh = Helpers.new()._school()
	var prep: Dictionary=fresh.adventure_preparation();var combat: Dictionary=fresh.adventure_combat_limits()
	combat["result_context"]["preparation"]["class_ratings"][0]["relationship_mean"]+=1
	var key := Record._cache_key(prep,combat,_trace())
	# Simulate a stale successful entry. Source/context admission must still run.
	Record._cache[key]={"supported":true,"receipt":{}}
	assert_eq(Record.replay(prep,combat,_trace()).get("reason"),"battle_context_rejected")
	Record._cache.erase(key)
	assert_true(model.restore(fresh.export_save())["supported"])
	assert_eq(model.stage(),"fifth_planning");assert_eq(model.read_postbattle(),{})
	assert_eq(model.export_save()["version"],4)


func test_own_cell_command_records_one_stop_and_replays_identically() -> void:
	var model = Helpers.new()._school();var first = Helpers.new()._combat(model)
	var cell: Vector2i=first.find_unit(3)["cell"]
	assert_true(first.command_move(3,cell))
	var commands: Array=first.battle_trace()["commands"]
	assert_eq(commands.size(),11);assert_eq(commands[-1],[0,5,3])
	var replay=Helpers.new()._combat(model)
	assert_true(replay.stop(3))
	assert_eq(replay.battle_trace(),first.battle_trace())
	assert_eq(replay.read_units(),first.read_units())


func test_declared_victory_uses_same_source_story_and_current_growth() -> void:
	# A declared result-boundary test, not a claim of automated/native victory.
	var model=Helpers.new()._school();var context: Dictionary=model.adventure_result_context()
	var settlement := Settlement.new();assert_true(settlement.initialize(context))
	assert_true(settlement.prepare(BattleTests.new()._inputs([3,4,9]))["supported"])
	settlement.confirm_round();var result:=settlement.confirm_total(true)
	var flow := Flow.new()
	assert_true(flow.begin(context,{"successor":"adv_ch003_pending","outcome":"mission_complete","settlement":result},
		model._school_entry["after"]["participants"],model._school_entry["after"]["flags"])["supported"])
	assert_eq(flow.snapshot()["page"]["chapter"],20)
	assert_eq(flow.bundle["school"]["global_total_511c"],result["confirmation"]["after"]["global_total_511c"])
	assert_eq(flow.bundle["records"].slice(0,3),result["confirmation"]["records"])
	assert_true(flow.execute({"op":"post_skip"})["supported"])
	assert_true(flow.execute({"op":"post_skip"})["supported"])
	assert_true(flow.execute({"op":"post_school"})["supported"])
	assert_eq(flow.bundle["school"]["student_count"],4)


func test_control_handoff_skip_member_assignment_and_backup_recovery() -> void:
	var ui=UIHelpers.new()._school_ui()
	ui.save_path="user://postbattle-test.json"
	for suffix in ["",".bak",".tmp",".corrupt"]:
		if FileAccess.file_exists(ui.save_path+suffix):DirAccess.remove_absolute(ProjectSettings.globalize_path(ui.save_path+suffix))
	var result := Record.replay(ui.model.adventure_preparation(),ui.model.adventure_combat_limits(),_trace())
	assert_true(result["supported"])
	ui._accept_battle_handoff(result["receipt"]);ui.refresh()
	var panel=ui.postbattle_panel
	assert_true(panel.visible);assert_false(ui.panel.visible)
	assert_eq(panel.dialogue.text,ui.model.read_postbattle()["page"]["text"])
	panel.next.pressed.emit();assert_eq(ui.model.read_postbattle()["cursor"],1)
	panel.skip.pressed.emit();assert_true(panel.skip_dialog.visible)
	assert_eq(ui.model.stage(),"post_story","skip needs explicit confirmation")
	panel.skip_dialog.hide();panel.skip_dialog.confirmed.emit()
	assert_eq(ui.model.stage(),"new_week_story")
	ui._manual_save();var saved: Dictionary=ui.model.state()
	panel.skip_dialog.confirmed.emit();assert_eq(ui.model.stage(),"post_workroom")
	panel.next.pressed.emit();assert_eq(ui.model.stage(),"returned_school")
	assert_eq(panel.roster.get_child_count(),5)
	panel._selected=5;panel._move(0,3,false)
	assert_eq(ui.model.read_postbattle()["bundle"]["school"]["derived_student_ids"][0],[3,4,9,5])
	ui._manual_save()
	var file:=FileAccess.open(ui.save_path,FileAccess.WRITE);file.store_string("broken");file.close()
	ui._load();assert_eq(ui.model.state(),saved,"corrupt primary recovers intact prior-stage backup")
	assert_eq(ui.model.stage(),"new_week_story");assert_true(panel.visible)
	ui.free()
	for suffix in ["",".bak",".tmp",".corrupt"]:
		if FileAccess.file_exists("user://postbattle-test.json"+suffix):DirAccess.remove_absolute(ProjectSettings.globalize_path("user://postbattle-test.json"+suffix))
