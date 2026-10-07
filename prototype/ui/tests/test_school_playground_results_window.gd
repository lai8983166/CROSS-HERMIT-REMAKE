extends "res://ui/tests/test_school_playground_window.gd"

const TEST_PATH := "user://test_graphical_school_results.json"

func _cleanup() -> void:
	for suffix in ["",".bak",".tmp",".corrupt"]:
		if FileAccess.file_exists(TEST_PATH+suffix):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(TEST_PATH+suffix))

func _dialog_click(control: Control) -> void:
	for index in range(3):
		await process_frame
	var viewport := control.get_viewport()
	var position := control.get_global_rect().get_center()
	if viewport is Window:
		position += Vector2(viewport.position)
	_check(control.is_visible_in_tree(),"dialog button visible")
	var motion := InputEventMouseMotion.new()
	motion.position = position
	root.push_input(motion,true)
	for pressed in [true,false]:
		var event := InputEventMouseButton.new()
		event.position = position
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = pressed
		root.push_input(event,true)
		await process_frame

func _result_bounds(panel) -> void:
	for index in range(3):
		await process_frame
	for button in panel.result_cards.values():
		_check(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(button.get_global_rect()),"growth portrait fits viewport")
	_check(panel.footer.get_global_rect().position.y > panel._results.get_global_rect().end.y,"results end before footer")
	_check(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(panel._guidance.get_global_rect()),"stage guidance fits viewport")
	_check(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(panel.footer.get_global_rect()),"footer fits viewport")

func _run() -> void:
	_cleanup()
	root.size = Vector2i(1024,768)
	root.gui_embed_subwindows = true
	var panel = load("res://school_playground.tscn").instantiate()
	panel.auto_load = false
	panel.save_path = TEST_PATH
	root.add_child(panel)
	for index in range(5):
		await process_frame
	await _click(panel.tab_buttons["courses"])
	await _click(panel.course_buttons[10])
	await _click(panel.next_button)
	_check(panel.model.stage() == "grown" and panel.page == "results","growth action opens actual results")
	_check(panel.result_cards.size() == 3,"three named growth cards")
	await _result_bounds(panel)
	await _capture("growth")
	await _click(panel.result_cards[4])
	_check(panel.detail_id == 4,"result portrait opens current attributes")
	await _click(panel.next_button)
	_check(panel.model.stage() == "confirmed","confirmation is guided second action")
	await _result_bounds(panel)
	await _capture("confirmed")
	await _click(panel.next_button)
	_check(panel.model.stage() == "completed" and panel.next_button.disabled,"MVP completes once")
	_check(panel.mvp_label.text == "帕弥菈","sourced student3 is visually named MVP")
	_check(panel.model.session.read_result_handoff()["recipient"] == 3,"controller MVP matches native source")
	var state: Dictionary = panel.model.state()
	await _click(panel.next_button)
	await _key(KEY_R)
	await _key(KEY_SPACE)
	_check(panel.model.state() == state,"disabled completion and old battle keys do not mutate")
	await _result_bounds(panel)
	await _capture("mvp")
	await _click(panel.tab_buttons["courses"])
	_check(panel.course_buttons[10].disabled,"captured result locks player planning")
	await _click(panel.course_buttons[10])
	_check(panel.model.state() == state,"locked course cannot repeat growth")
	await _click(panel.tab_buttons["results"])
	await _click(panel.save_button)
	_check(FileAccess.file_exists(TEST_PATH),"manual save exists")
	var restored = load("res://school_playground.tscn").instantiate()
	restored.save_path = TEST_PATH
	root.remove_child(panel)
	panel.queue_free()
	root.add_child(restored)
	panel = restored
	for index in range(5):
		await process_frame
	_check(panel.model.state() == state and panel.page == "results","fresh window automatically recovers completed state")
	_check(panel.mvp_label.text == "帕弥菈" and panel.next_button.disabled,"restored result visible once")
	await _capture("restored")
	var disk := FileAccess.get_sha256(TEST_PATH)
	await _click(panel.restart_button)
	_check(panel.restart_dialog.visible,"restart has explicit confirmation")
	await _capture("restart_confirmation")
	await _dialog_click(panel.restart_dialog.get_cancel_button())
	_check(not panel.restart_dialog.visible,"cancel closes confirmation")
	_check(panel.model.state() == state and FileAccess.get_sha256(TEST_PATH) == disk,"cancel preserves state and saved bytes")
	var broken := FileAccess.open(TEST_PATH,FileAccess.WRITE)
	broken.store_string("invalid"); broken.close()
	await _click(panel.load_button)
	_check(panel.model.state() == state and panel._status.text.contains("备份"),"corrupt primary recovers completed backup")
	await _capture("backup_recovered")
	await _click(panel.save_button)
	_check(panel._status.text.contains("已保存") and FileAccess.file_exists(TEST_PATH+".corrupt"),"explicit save preserves corrupt primary")
	await _click(panel.restart_button)
	await _dialog_click(panel.restart_dialog.get_ok_button())
	_check(panel.model.stage() == "planning" and panel.page == "groups","confirmed restart replaces progress")
	_check(panel.model.session.read_result_handoff().is_empty(),"restart clears previous MVP")
	_check(panel.model.session.read_snapshot()["week"] == 4,"restart maintains declared week")
	await _capture("restarted")
	await _click(panel.student_buttons[0][0])
	await _click(panel.wait_target)
	await _click(panel.tab_buttons["courses"])
	await _click(panel.course_buttons[11])
	await _click(panel.next_button)
	await _click(panel.next_button)
	await _click(panel.next_button)
	_check(panel.model.stage() == "completed" and panel.model.session.read_result_handoff()["recipient"] == 4,"waiting3 alternate course picks sourced student4")
	_check(panel.mvp_label.text == "瑟希莉丝","alternate MVP uses actual portrait/name")
	await _result_bounds(panel)
	await _capture("alternate_mvp")
	panel.save_path = "user://missing_graphical_school_directory/state.json"
	await _click(panel.save_button)
	_check(panel._status.text.contains("失败"),"failed save not presented as saved")
	panel.queue_free()
	await process_frame
	_cleanup()
	_finish()
