extends "res://ui/tests/test_school_playground_results_window.gd"

func _run() -> void:
	_cleanup()
	root.size = Vector2i(1024,768)
	root.gui_embed_subwindows = true
	_check(ProjectSettings.get_setting("application/run/main_scene") == "res://school_playground.tscn","graphical school is default launch")
	var panel = load("res://school_playground.tscn").instantiate()
	panel.auto_load = false
	panel.save_path = TEST_PATH
	root.add_child(panel)
	current_scene = panel
	for index in range(5):
		await process_frame
	await _click(panel.tab_buttons["courses"])
	await _click(panel.course_buttons[12])
	var before: Dictionary = panel.model.state()
	await _click(panel.battle_button)
	for index in range(8):
		await process_frame
	var battle = current_scene
	_check(battle.scene_file_path == "res://main.tscn","button opens existing battle scene")
	battle.set_physics_process(false)
	_check(battle.battle != null and battle.playground_button.visible,"battle initialized and school return available")
	_check(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(battle.playground_button.get_global_rect()),"battle return button fits viewport")
	await _capture("battle_preview")
	await _key(KEY_SPACE)
	_check(Engine.time_scale == 0.0,"battle preview remains operable")
	await _click(battle.playground_button)
	for index in range(8):
		await process_frame
	panel = current_scene
	_check(panel.scene_file_path == "res://school_playground.tscn","battle returns to graphical scene")
	_check(panel.model.state() == before,"return restores saved course choice and membership")
	_check(Engine.time_scale == 1.0,"return clears battle pause")
	await _click(panel.tab_buttons["courses"])
	_check(panel.course_buttons[12].button_pressed,"restored course visible")
	await _click(panel.next_button)
	await _click(panel.next_button)
	await _click(panel.next_button)
	_check(panel.model.stage() == "completed","third course remains usable after scene navigation")
	await _result_bounds(panel)
	await _capture("returned_school")
	var completed: Dictionary = panel.model.state()
	panel.save_path = "user://missing_graphical_school_directory/state.json"
	await _click(panel.battle_button)
	_check(current_scene == panel and panel.model.state() == completed and panel._guidance.text.contains("不能离开"),"failed navigation save retains live progress")
	root.remove_meta("school_playground_save_path")
	current_scene = null
	panel.queue_free()
	await process_frame
	_cleanup()
	_finish()
