extends SceneTree
## Verify actual viewport mouse/key input; optionally archive rendered captures.

var checks := 0
var failures: Array = []
var capture_dir := ""
var captured: Array = []
var observations: Array = []


func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="):
			capture_dir = arg.trim_prefix("--capture-dir=")
	if not capture_dir.is_empty() and FileAccess.file_exists(capture_dir.path_join("verification.json")):
		printerr("Refusing to overwrite archived verification")
		quit(1)
		return
	call_deferred("_run")


func _check(ok: bool, message: String) -> void:
	checks += 1
	if not ok:
		failures.append(message)
		printerr("FAIL ",message)


func _click(control: Control) -> void:
	await process_frame
	var pos := control.get_global_rect().get_center()
	_check(control.is_visible_in_tree() and Rect2(Vector2.ZERO,Vector2(root.size)).has_point(pos),"clickable control is visible and inside viewport")
	var motion := InputEventMouseMotion.new()
	motion.position = pos
	root.push_input(motion,true)
	for pressed in [true,false]:
		var event := InputEventMouseButton.new()
		event.position = pos
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = pressed
		root.push_input(event,true)
		await process_frame


func _key(key: Key) -> void:
	for pressed in [true,false]:
		var event := InputEventKey.new()
		event.keycode = key
		event.pressed = pressed
		root.push_input(event,true)
		await process_frame


func _capture(name: String) -> void:
	if capture_dir.is_empty() or DisplayServer.get_name() == "headless":
		return
	for index in range(3):
		await process_frame
	await RenderingServer.frame_post_draw
	_check(root.get_texture().get_image().save_png(capture_dir.path_join(name + ".png")) == OK,"capture " + name)
	captured.append(name)


func _observe(panel, name: String) -> void:
	var snapshot: Dictionary = panel.session.read_snapshot()
	observations.append({"name":name,"revision":panel.session.revision(),
		"teachers":snapshot["derived_teacher_ids"],"students":snapshot["derived_student_ids"],
		"waiting_students":snapshot["idle_student_ids"],"waiting_teachers":snapshot["idle_teacher_ids"]})


func _run() -> void:
	root.size = Vector2i(1024,768)
	root.gui_embed_subwindows = true
	var main = load("res://main.tscn").instantiate()
	root.add_child(main)
	await process_frame
	main.set_physics_process(false)
	var panel = main.school_panel
	_check(not panel.visible,"school starts closed")
	var battle = main.battle
	var frame: int = battle.frame
	await _capture("launcher")
	await _click(main.return_panel.new_school_button)
	_check(panel.visible and not main.return_panel.visible,"launcher opens school")
	if panel.session == null:
		_check(false,"launcher initialized source session")
		quit(1)
		return
	_check(panel.session.revision() == 2,"initialization and preparation publish separately")
	_check(panel.session.read_snapshot()["derived_teacher_ids"] == [101,-1,-1,-1,-1],"source teacher101 occupies first class")
	_check(panel.session.read_snapshot()["derived_student_ids"][0] == [3,4,9,-1],"three source students start in first class")
	_check(panel.session.read_snapshot()["group_raw_bytes"][14] == 3,"prepared source count is three")
	_check(panel.teacher_buttons[0].text.contains("101") and panel.student_buttons[0][0].text.contains("31"),"source teacher and recalculated student level render")
	_check(panel.wait_student_target.disabled and panel.wait_teacher_target.disabled,"waiting targets require selection")
	for row in panel.student_buttons:
		for cell in row:
			_check(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(cell.get_global_rect()),"student cell stays inside viewport")
	var boot: Dictionary = panel.session.read_snapshot()
	await _key(KEY_R)
	await _key(KEY_SPACE)
	main._physics_process(10000.0)
	_check(main.battle == battle and battle.frame == frame,"school blocks battle restart, pause and ticks")
	_check(main.locked_cell == Vector2i(-1,-1),"school clicks do not select map cells")
	await _capture("source_class")
	await _click(panel.student_buttons[0][0])
	_check(panel._selected_id == 3 and panel.student_buttons[0][0].button_pressed,"student selection highlights actual member")
	await _key(KEY_ESCAPE)
	_check(panel._selected_id == -1 and panel.cancel_button.disabled,"Escape cancels selection")
	_check(panel.session.revision() == 2 and panel.session.read_snapshot() == boot,"cancel has no school writes")
	await _click(panel.teacher_buttons[0])
	_check(panel._selected_kind == "teacher" and panel.wait_student_target.disabled,"teacher selection only enables teacher waiting")
	await _click(panel.teacher_buttons[1])
	var moved: Dictionary = panel.session.read_snapshot()
	_check(moved["derived_teacher_ids"] == [-1,101,-1,-1,-1],"mouse moves teacher to second class")
	_check(moved["idle_student_ids"] == [3,4,9],"teacher move returns all students to waiting")
	_check(moved["derived_student_ids"][0] == [-1,-1,-1,-1] and moved["group_raw_bytes"][14] == 0,"old class clears students and count")
	_check(panel.session.revision() == 3 and panel.session.journal().size() == 7,"one move publishes one revision and three phases")
	_observe(panel,"teacher_relocated")
	await _capture("teacher_relocated")
	await _click(panel.waiting_students[3])
	await _click(panel.student_buttons[0][0])
	_check(panel._selected_id == 3 and panel.session.revision() == 3,"teacherless target retains selection without moving")
	_check(panel.instruction.text.contains("先为这个班安排教师"),"teacherless target explains how to proceed")
	await _click(panel.student_buttons[1][3])
	_check(not panel.waiting_students.has(3),"assigned student leaves waiting controls")
	await _click(panel.waiting_students[4])
	await _click(panel.student_buttons[1][1])
	await _click(panel.waiting_students[9])
	await _click(panel.student_buttons[1][2])
	_check(panel.session.read_snapshot()["derived_student_ids"][1] == [-1,4,9,3],"mouse fills exact chosen cells")
	_check(panel.session.read_snapshot()["group_raw_bytes"][42] == 3,"class count follows published state")
	_check(panel.waiting_students.is_empty(),"waiting list refreshes after three joins")
	_observe(panel,"second_class_filled")
	await _capture("second_class_filled")
	await _click(panel.student_buttons[1][3])
	await _click(panel.student_buttons[1][1])
	_check(panel.session.read_snapshot()["derived_student_ids"][1] == [-1,3,9,4],"mouse swaps occupied student cells")
	await _click(panel.student_buttons[1][2])
	await _click(panel.wait_student_target)
	_check(panel.session.read_snapshot()["idle_student_ids"] == [9],"student target returns selected student to waiting")
	_check(panel.session.read_snapshot()["derived_student_ids"][1] == [-1,3,-1,4],"return clears only chosen slot")
	var owned = panel.session
	var saved: Dictionary = owned.read_snapshot()
	var revision: int = owned.revision()
	await _click(panel.close_button)
	_check(not panel.visible and main.return_panel.visible,"close restores launcher")
	await _key(KEY_R)
	_check(main.battle != battle,"battle restart works again after closing school")
	battle = main.battle
	await _click(main.return_panel.new_school_button)
	_check(panel.session == owned and owned.revision() == revision and owned.read_snapshot() == saved,"reopening preserves owned school edits")
	await _click(panel.student_buttons[1][3])
	await _click(panel.cancel_button)
	_check(panel._selected_id == -1 and owned.revision() == revision,"cancel button also preserves session")
	await _click(panel.teacher_buttons[1])
	await _click(panel.wait_teacher_target)
	_check(owned.read_snapshot()["idle_teacher_ids"] == [101] and owned.read_snapshot()["idle_student_ids"] == [3,4,9],"teacher return restores all waiting members")
	_check(owned.read_snapshot()["derived_teacher_ids"] == [-1,-1,-1,-1,-1],"teacher return clears all taught classes")
	await _click(panel.waiting_teachers[101])
	await _click(panel.teacher_buttons[4])
	_check(owned.read_snapshot()["derived_teacher_ids"] == [-1,-1,-1,-1,101],"waiting teacher can enter fifth class")
	_check(owned.read_snapshot()["idle_student_ids"] == [3,4,9],"moving teacher does not automatically assign waiting students")
	for key in ["member_profiles","relationships","availability","raw_student_ids","raw_teacher_ids","month","week","global_total_511c","course_buffers","course_counts","course_unlocked_flags"]:
		_check(owned.read_snapshot()[key] == boot[key],"grouping preserves " + key)
	await _click(panel.restart_button)
	_check(panel.session != owned and panel.session.revision() == 2,"explicit restart creates fresh prepared school")
	_check(panel.session.read_snapshot() == boot,"restart restores exact source start")
	_check(panel.session.journal().size() == 4 and panel._selected_id == -1,"restart clears old move journal and selection")
	_check(main.battle == battle,"school restart leaves battle intact")
	_observe(panel,"restart")
	await _capture("restart")
	main.queue_free()
	await process_frame
	if not capture_dir.is_empty():
		var screenshots := {}
		for name in captured:
			screenshots[name + ".png"] = FileAccess.get_sha256(capture_dir.path_join(name + ".png"))
		var report := {"godot_version":Engine.get_version_info()["string"],"display_driver":DisplayServer.get_name(),
			"checks":checks,"failures":failures,"observations":observations,"screenshot_sha256":screenshots,
			"execution_scope":"local_prototype_source_initialized_grouping_mouse_and_key_input"}
		var file := FileAccess.open(capture_dir.path_join("verification.json"),FileAccess.WRITE)
		file.store_string(JSON.stringify(report,"  ") + "\n")
		file.close()
	print("New game school window: %d checks, %d failures" % [checks,failures.size()])
	quit(0 if failures.is_empty() else 1)
