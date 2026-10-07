extends "res://ui/tests/test_school_playground_results_window.gd"


func _arrival_bounds(view) -> void:
	for index in range(3):
		await process_frame
	var screen := Rect2(Vector2.ZERO,Vector2(root.size))
	for control in [view.review_button,view.battle_button,view.save_button,view.restart_button,
			view.calendar,view.status]+view.summaries:
		_check(screen.encloses(control.get_global_rect()),"arrival content fits viewport")


func _run() -> void:
	_cleanup()
	root.size = Vector2i(1024,768)
	root.gui_embed_subwindows = true
	if root.has_meta("school_playground_save_path"):
		root.remove_meta("school_playground_save_path")
	var panel = load("res://school_playground.tscn").instantiate()
	panel.auto_load = false
	panel.save_path = TEST_PATH
	root.add_child(panel)
	current_scene = panel
	for index in range(5):
		await process_frame
	await _click(panel.tab_buttons["courses"])
	await _click(panel.course_buttons[12])
	for index in range(4):
		await _click(panel.next_button)
	var records: Dictionary = panel.model._school_state()
	await _click(panel.story_reader.skip_button)
	await _dialog_click(panel.story_reader.skip_dialog.get_ok_button())
	_check(panel.model.stage() == "story_completed" and panel.next_button.text == "进入第五周","completed story unlocks next-week action")
	await _click(panel.next_button)
	_check(panel.model.stage() == "arrival" and panel.arrival.visible,"next-week action displays arrival")
	_check(panel.arrival.calendar.text == "4月 · 第5周" and panel.calendar.text.ends_with("第5周"),"date uses actual projected week")
	_check(not panel.model.state()["week"]["handoff"]["school_initialized"],"arrival does not invent school initialization")
	_check(panel.model._school_state() == records,"next week preserves course growth and MVP")
	await _arrival_bounds(panel.arrival)
	await _capture("fifth_week_arrival")
	var arrived: Dictionary = panel.model.state()
	var saved: Dictionary = panel.model.export_save()
	panel.model.execute({"op":"week"})
	_check(panel.model.export_save() == saved,"duplicate week never becomes a save command")
	await _click(panel.arrival.review_button)
	_check(panel.page == "results" and not panel.arrival.visible,"arrival can review course results")
	_check(panel.mvp_label.text == "帕弥菈","original MVP retained in review")
	await _result_bounds(panel)
	await _capture("fourth_week_review")
	await _click(panel.tab_buttons["courses"])
	_check(panel.course_buttons[12].disabled,"unsupported fifth-week courses remain locked")
	await _click(panel.tab_buttons["results"])
	await _click(panel.next_button)
	_check(panel.arrival.visible and panel.model.state() == arrived,"returning to arrival does not advance another week")
	await _click(panel.arrival.save_button)
	root.remove_child(panel)
	panel.queue_free()
	panel = load("res://school_playground.tscn").instantiate()
	panel.save_path = TEST_PATH
	root.add_child(panel)
	current_scene = panel
	for index in range(5):
		await process_frame
	_check(panel.arrival.visible and panel.model.state() == arrived,"fresh launch restores fifth-week arrival")
	await _capture("restored_arrival")
	var disk := FileAccess.get_sha256(TEST_PATH)
	await _click(panel.arrival.restart_button)
	await _dialog_click(panel.restart_dialog.get_cancel_button())
	_check(panel.model.state() == arrived and FileAccess.get_sha256(TEST_PATH) == disk,"cancel restart preserves arrival and disk")
	await _click(panel.arrival.battle_button)
	for index in range(8):
		await process_frame
	var battle = current_scene
	_check(battle.scene_file_path == "res://main.tscn","arrival opens battle preview")
	battle.set_physics_process(false)
	await _capture("arrival_battle_preview")
	await _key(KEY_SPACE)
	_check(Engine.time_scale == 0.0,"existing battle preview remains operable")
	await _click(battle.playground_button)
	for index in range(8):
		await process_frame
	panel = current_scene
	_check(panel.arrival.visible and panel.model.state() == arrived,"battle roundtrip restores exact week and result")
	_check(Engine.time_scale == 1.0,"arrival return clears battle pause")
	await _capture("arrival_after_battle")
	panel.save_path = "user://missing_school_arrival_directory/state.json"
	await _click(panel.arrival.battle_button)
	_check(current_scene == panel and panel.model.state() == arrived and panel.arrival.status.text.contains("保存失败"),
		"failed navigation save keeps arrival visible and retains memory")
	root.remove_meta("school_playground_save_path")
	current_scene = null
	panel.queue_free()
	await process_frame
	_cleanup()
	_finish()
