extends "res://sim/tests/test_base.gd"
## Headless Control integration only; declared local HP endpoints are not a
## witness of original battle execution, rendering or native input.
const School := preload("res://ui/school_playground.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const CombatTrial := preload("res://ui/school_combat_trial.gd")


class RefusingStage extends "res://ui/school_opening_stage.gd":
	func load_presentation() -> bool: return false


class AssetFailureTrial extends CombatTrial:
	var refuse_opening := false
	func _new_opening_stage():
		return RefusingStage.new() if refuse_opening else super._new_opening_stage()


func _school_ui():
	var ui := School.new()
	ui.auto_load = false; ui.autosave = false
	var tree := Engine.get_main_loop() as SceneTree
	tree.root.add_child(ui)
	assert_true(ui.is_node_ready(),"adding the UI to the existing headless tree runs ready")
	var fixture: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_playground_legacy_v3.json")))
	assert_true(ui.model.restore(fixture["cases"][1]["save"])["supported"])
	for op in ["workroom_open","work_start","work_skip","school_enter"]:
		assert_true(ui.model.execute({"op":op})["supported"])
	ui.page = "adventure"; ui.refresh()
	return ui


func _consume_through_ui(trial) -> void:
	var before: Array = trial.session.read_units()
	var frame: int = trial.session.frame
	assert_true(trial.close_button.disabled,"finishing cannot be requested twice")
	assert_false(trial.canvas.controls_enabled,"combat canvas ignores further commands")
	assert_false(trial.canvas.dragging,"finishing releases an in-progress drag")
	for button in [trial.pause_button,trial.stop_button,trial.enemy_button]:
		assert_true(button.disabled,"combat tools stop during ending")
	for index in range(4):
		assert_eq(trial.session.ending_snapshot()["phase"],"consuming")
		trial._process(1.0/30.0)
		assert_eq(trial.session.read_units(),before,"ending does not advance combat")
		assert_eq(trial.session.frame,frame)
	assert_eq(trial.session.ending_snapshot()["phase"],"summary")
	assert_true(trial.result_panel.visible,"summary remains until explicit return")
	assert_false(trial.canvas.visible)
	assert_true(trial.return_button.is_visible_in_tree())
	assert_false(trial.return_button.disabled)
	assert_eq(trial.return_button.text,"返回学校准备")
	assert_true(trial.return_button.has_focus(),"summary has an explicit keyboard-accessible return")
	trial._process(1.0)
	assert_eq(trial.session.ending_snapshot()["phase"],"summary","no automatic summary dismissal")


func _complete_opening(trial) -> void:
	var units: Array = trial.session.read_units()
	var frame: int = trial.session.frame
	for index in range(10):
		var opening: Dictionary = trial.session.opening_snapshot()
		assert_eq(opening["page_index"],index)
		assert_eq(trial.opening_stage.page_index,index)
		assert_eq(trial.opening_stage.current_text.text,opening["page"]["text"])
		assert_false(trial.opening_stage.display_ready())
		trial.opening_next_button.pressed.emit()
		assert_true(trial.opening_stage.display_ready(),"first press reveals the page")
		assert_eq(trial.session.opening_snapshot()["page_index"],index,"revealing does not confirm")
		if index in [1,2,6,9]:
			assert_eq(trial.opening_next_button.text,"开始操作" if index == 9 else "继续")
			trial._process(1.0)
			assert_eq(trial.session.opening_snapshot()["page_index"],index,"source confirmation waits for input")
			trial.opening_next_button.pressed.emit()
		else:
			trial.opening_next_button.pressed.emit()
			assert_eq(trial.session.opening_snapshot()["page_index"],index,"button cannot replace automatic sequencing")
			trial._process(0.0)
		assert_eq(trial.session.read_units(),units,"opening never advances combat")
		assert_eq(trial.session.frame,frame)
	assert_eq(trial.session.ending_snapshot()["phase"],"active")
	assert_eq(trial.session.opening_snapshot()["page_index"],10)
	assert_eq(trial.opening_stage,null)
	assert_false(trial.opening_panel.visible)
	assert_true(trial.canvas.controls_enabled)


func test_paused_exit_returns_to_same_school_and_reopens_fresh_trial() -> void:
	var ui = _school_ui()
	var school_state: Dictionary = ui.model.state()
	var save: Dictionary = ui.model.export_save()
	ui._open_combat_trial()
	var trial = ui.combat_trial
	var emitted := [0]
	trial.closed.connect(func(): emitted[0] += 1)
	assert_true(trial.visible); assert_eq(trial.session.units.size(),14)
	assert_false(ui.panel.visible,"school commands are inaccessible while the trial is open")
	_complete_opening(trial)
	trial.toggle_pause(); assert_true(trial.session.paused)
	trial.canvas.dragging = true
	trial.close_button.pressed.emit()
	assert_eq(trial.session.ending_snapshot()["outcome"],"player_exit")
	var pending: Dictionary = trial.session.ending_snapshot()
	trial.close_trial(); assert_eq(trial.session.ending_snapshot(),pending)
	assert_eq(emitted[0],0,"requesting exit does not close before summary")
	_consume_through_ui(trial)
	assert_eq(trial.result_title.text,"本次试验已结束")
	assert_eq(trial.session.ending_snapshot()["summary"]["remaining_enemies"],7)
	var retired = trial.session
	trial.return_button.pressed.emit()
	assert_eq(emitted[0],1); assert_false(trial.visible)
	assert_eq(retired.ending_snapshot()["phase"],"closed")
	assert_true(retired.units.is_empty()); assert_true(retired.events.is_empty())
	assert_eq(trial.canvas.session,null); assert_eq(trial.canvas.texture,null)
	assert_true(trial.canvas.sprites.is_empty()); assert_true(trial._sprites.is_empty())
	assert_true(trial.canvas.labels.is_empty()); assert_true(trial.member_buttons.is_empty())
	assert_false(trial.canvas.dragging)
	trial.close_trial(); trial.return_button.pressed.emit()
	assert_eq(emitted[0],1,"duplicate return emits no second handoff")
	assert_eq(ui.page,"adventure"); assert_true(ui._adventure.visible)
	assert_true(ui.panel.visible)
	assert_true(ui.adventure_combat_button.has_focus(),"school preparation regains focus")
	assert_eq(ui.model.state(),school_state); assert_eq(ui.model.export_save(),save)
	ui._open_combat_trial()
	assert_true(trial.visible); assert_true(trial.session != retired)
	assert_eq(trial.session.ending_snapshot()["phase"],"opening")
	_complete_opening(trial)
	assert_eq(trial.session.enemies().size(),7); assert_eq(trial.session.frame,0)
	assert_false(trial.result_panel.visible); assert_true(trial.canvas.visible)
	assert_true(trial.canvas.controls_enabled); assert_false(trial.pause_button.disabled)
	trial.close_trial(); _consume_through_ui(trial); trial.return_button.pressed.emit()
	assert_eq(emitted[0],2); assert_eq(ui.model.export_save(),save)
	ui.free()


func test_declared_enemy_and_student_endpoints_show_distinct_summaries() -> void:
	var ui = _school_ui()
	var state: Dictionary = ui.model.state(); var save: Dictionary = ui.model.export_save()
	for outcome in ["initial_enemies_cleared","squad_defeated"]:
		ui._open_combat_trial()
		var trial = ui.combat_trial
		_complete_opening(trial)
		# Explicit UI-boundary fixtures; combat/damage causality is tested separately.
		var affected: Array = trial.session.enemies() if outcome == "initial_enemies_cleared" else trial.session.controlled_units()
		for unit in affected: unit["limits"]["hp"] = 0
		trial._process(1.0/30.0)
		assert_eq(trial.session.ending_snapshot()["outcome"],outcome)
		_consume_through_ui(trial)
		var summary: Dictionary = trial.session.ending_snapshot()["summary"]
		assert_false(summary["rewards_applied"]); assert_false(summary["campaign_advanced"])
		if outcome == "initial_enemies_cleared":
			assert_eq(summary["defeated_enemies"],7); assert_eq(summary["remaining_enemies"],0)
			assert_eq(trial.result_title.text,"初始敌人已清除")
		else:
			assert_eq(summary["surviving_students"],0)
			assert_eq(trial.result_title.text,"当前学生已全部倒下")
		assert_true(trial.result_details.text.contains("仍可行动的学生"))
		trial.return_button.pressed.emit()
		assert_eq(ui.page,"adventure"); assert_false(trial.visible)
		assert_eq(ui.model.state(),state); assert_eq(ui.model.export_save(),save)
	ui.free()


func test_failed_open_preserves_live_trial_and_result_can_still_return() -> void:
	var ui = _school_ui(); ui._open_combat_trial()
	var trial = ui.combat_trial
	_complete_opening(trial)
	var active = trial.session
	var texture = trial.canvas.texture
	var units: Array = active.read_units()
	var ending: Dictionary = active.ending_snapshot()
	assert_false(trial.open_trial({},ui.model.adventure_combat_limits(),{}))
	assert_eq(trial.session,active); assert_eq(trial.canvas.texture,texture)
	assert_eq(active.read_units(),units); assert_eq(active.ending_snapshot(),ending)
	assert_true(trial.visible); assert_true(trial.canvas.controls_enabled)
	trial.close_trial(); _consume_through_ui(trial)
	ending = active.ending_snapshot()
	assert_false(trial.open_trial({},ui.model.adventure_combat_limits(),{}))
	assert_eq(active.ending_snapshot(),ending); assert_true(trial.result_panel.visible)
	trial.return_button.pressed.emit(); assert_false(trial.visible)
	ui.free()


func test_opening_freezes_combat_inputs_and_keeps_all_ten_pages_in_order() -> void:
	var ui = _school_ui()
	var school_state: Dictionary = ui.model.state(); var save: Dictionary = ui.model.export_save()
	ui._open_combat_trial()
	var trial = ui.combat_trial
	var units: Array = trial.session.read_units()
	var selected: int = trial.session.selected_id
	assert_true(trial.opening_panel.is_visible_in_tree())
	assert_true(trial.opening_next_button.has_focus())
	assert_false(trial.canvas.controls_enabled)
	for button in [trial.pause_button,trial.stop_button,trial.enemy_button,trial.center_button,trial.fit_button,trial.terrain_button,trial.zoom_in_button,trial.zoom_out_button]:
		assert_true(button.disabled)
	for button in trial.member_buttons.values(): assert_true(button.disabled)
	var mouse := InputEventMouseButton.new()
	mouse.button_index = MOUSE_BUTTON_RIGHT; mouse.pressed = true; mouse.position = Vector2(400,280)
	trial.canvas._gui_input(mouse)
	var key := InputEventKey.new(); key.pressed = true; key.keycode = KEY_S
	trial._input(key); trial.toggle_pause(); trial._process(0.5)
	assert_eq(trial.session.read_units(),units); assert_eq(trial.session.selected_id,selected)
	assert_eq(trial.session.frame,0); assert_false(trial.session.paused)
	assert_true(trial.session.events.is_empty())
	for available in [Vector2(760,350),Vector2(984,490),Vector2(1240,540)]:
		trial.opening_stage.size = available; trial.opening_stage._fit()
		var extent: Vector2 = Vector2(1024,768)*trial.opening_stage.stage_scale
		assert_true(extent.x <= available.x+0.001 and extent.y <= available.y+0.001,"opening remains within its layout area")
	_complete_opening(trial)
	trial.opening_next_button.pressed.emit()
	assert_eq(trial.session.frame,0,"a stale opening button cannot advance combat")
	assert_eq(ui.model.state(),school_state); assert_eq(ui.model.export_save(),save)
	trial.close_trial(); _consume_through_ui(trial); trial.return_button.pressed.emit()
	ui.free()


func test_escape_during_opening_releases_presentation_and_reopens_at_first_page() -> void:
	var ui = _school_ui(); var save: Dictionary = ui.model.export_save()
	ui._open_combat_trial()
	var trial = ui.combat_trial
	var stage = trial.opening_stage
	trial.opening_next_button.pressed.emit(); trial._process(0.0)
	assert_eq(trial.session.opening_snapshot()["page_index"],1)
	var key := InputEventKey.new(); key.pressed = true; key.keycode = KEY_ESCAPE
	trial._input(key)
	assert_false(is_instance_valid(stage)); assert_eq(trial.opening_stage,null)
	assert_false(trial.opening_panel.visible)
	assert_eq(trial.session.ending_snapshot()["outcome"],"player_exit")
	_consume_through_ui(trial)
	assert_eq(trial.session.ending_snapshot()["summary"]["battle_frames"],0)
	trial.return_button.pressed.emit()
	ui._open_combat_trial()
	assert_eq(trial.session.ending_snapshot()["phase"],"opening")
	assert_eq(trial.session.opening_snapshot()["page_index"],0)
	assert_eq(trial.opening_stage.page_index,0)
	assert_false(trial.opening_stage.display_ready())
	trial.close_trial(); _consume_through_ui(trial); trial.return_button.pressed.emit()
	assert_eq(ui.model.export_save(),save)
	ui.free()


func test_failed_opening_asset_or_session_preserves_current_page_and_school() -> void:
	var ui = _school_ui()
	var state: Dictionary = ui.model.state(); var save: Dictionary = ui.model.export_save()
	var trial := AssetFailureTrial.new()
	ui.add_child(trial)
	assert_true(trial.open_trial(ui.model.adventure_preparation(),ui.model.adventure_combat_limits(),{}))
	trial.opening_next_button.pressed.emit(); trial._process(0.0)
	var session = trial.session; var stage = trial.opening_stage; var texture = trial.canvas.texture
	var opening: Dictionary = session.opening_snapshot()
	var units: Array = session.read_units()
	trial.refuse_opening = true
	assert_false(trial.open_trial(ui.model.adventure_preparation(),ui.model.adventure_combat_limits(),{}))
	assert_eq(trial.session,session); assert_eq(trial.opening_stage,stage); assert_eq(trial.canvas.texture,texture)
	assert_eq(session.opening_snapshot(),opening); assert_eq(session.read_units(),units)
	trial.refuse_opening = false
	assert_false(trial.open_trial({},ui.model.adventure_combat_limits(),{}))
	assert_eq(trial.session,session); assert_eq(trial.opening_stage,stage); assert_eq(trial.canvas.texture,texture)
	assert_eq(session.opening_snapshot(),opening); assert_eq(session.read_units(),units)
	assert_true(trial.opening_panel.visible); assert_false(trial.canvas.controls_enabled)
	assert_eq(ui.model.state(),state); assert_eq(ui.model.export_save(),save)
	trial.close_trial(); _consume_through_ui(trial); trial.return_button.pressed.emit()
	ui.free()
