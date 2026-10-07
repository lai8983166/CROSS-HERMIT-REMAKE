extends "res://ui/tests/test_new_game_school_window.gd"

func _bounds(panel) -> void:
	for group in range(5):
		for button in [panel.teacher_buttons[group]]+panel.student_buttons[group]:
			_check(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(button.get_global_rect()),"member card fits viewport")
	_check(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(panel.footer.get_global_rect()),"footer fits viewport")
	_check(panel.footer.get_global_rect().position.y > panel._groups.get_global_rect().end.y,"grouping ends before footer")

func _finish() -> void:
	if not capture_dir.is_empty():
		var screenshots := {}
		for name in captured:
			screenshots[name+".png"] = FileAccess.get_sha256(capture_dir.path_join(name+".png"))
		var file := FileAccess.open(capture_dir.path_join("verification.json"),FileAccess.WRITE)
		file.store_string(JSON.stringify({"checks":checks,"failures":failures,"display_driver":DisplayServer.get_name(),"screenshots":screenshots},"  ")+"\n")
		file.close()
	print("Graphical school: %d checks, %d failures" % [checks,failures.size()])
	quit(0 if failures.is_empty() else 1)

func _run() -> void:
	root.size = Vector2i(1024,768)
	var panel = load("res://school_playground.tscn").instantiate()
	panel.auto_load = false
	panel.autosave = false
	root.add_child(panel)
	for index in range(5):
		await process_frame
	_check(panel.model.stage() == "planning","starts with independent fourth-week planning")
	_check(panel.teacher_buttons[0].icon != null and panel.student_buttons[0][0].text == "帕弥菈","original portrait and name displayed")
	_check(panel.next_button.disabled,"unplanned class cannot settle")
	_bounds(panel)
	await _capture("initial_class")
	await _click(panel.student_buttons[0][0])
	_check(panel.detail_id == 3 and panel.selected_id == 3,"portrait selects member and details")
	var before: Dictionary = panel.model.state()
	await _click(panel.student_buttons[1][0])
	_check(panel.model.state() == before and panel._guidance.text.contains("教师"),"teacherless class gives feedback without state writes")
	await _key(KEY_ESCAPE)
	_check(panel.selected_id == -1,"escape cancels")
	await _click(panel.teacher_buttons[0])
	await _click(panel.teacher_buttons[2])
	_check(panel.selected_class == 2 and panel.waiting_buttons.size() == 3,"teacher move returns original students to waiting")
	await _capture("teacher_moved")
	for pair in [[3,0],[4,1],[9,2]]:
		await _click(panel.waiting_buttons[pair[0]])
		await _click(panel.student_buttons[2][pair[1]])
	_check(panel._identity("teacher",2,-1) == 101 and panel._identity("student",2,0) == 3,"portrait moves own supported state")
	_bounds(panel)
	await _click(panel.tab_buttons["courses"])
	_check(not panel.course_buttons[10].disabled,"moved teacher retains source courses")
	await _click(panel.course_buttons[10])
	_check(not panel.next_button.disabled and panel.course_buttons[10].button_pressed,"course sets teaching mode and enables growth")
	_check(panel.model.session.read_snapshot()["week"] == 4,"planning does not invent a new week")
	for button in panel.course_buttons.values():
		_check(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(button.get_global_rect()),"course cards fit viewport")
	await _capture("course_selected")
	panel.queue_free()
	await process_frame
	_finish()
