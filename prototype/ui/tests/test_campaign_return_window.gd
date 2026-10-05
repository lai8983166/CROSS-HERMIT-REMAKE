extends SceneTree
## Real main scene and button/input integration. Optional --capture-dir=<absolute path>.

var failures: Array[String] = []
var capture_dir := ""
var checks := 0
var observations: Array = []
var captured_names: Array[String] = []


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
		printerr("FAIL ", message)


func _capture(name: String) -> void:
	if capture_dir.is_empty() or DisplayServer.get_name() == "headless":
		return
	for i in range(3):
		await process_frame
	await RenderingServer.frame_post_draw
	_check(root.get_texture().get_image().save_png(capture_dir.path_join(name + ".png")) == OK, "capture " + name)
	captured_names.append(name)


func _click(control: Control, at := Vector2(-1, -1)) -> void:
	await process_frame
	var pos := control.get_global_rect().get_center() if at.x < 0 else at
	var motion := InputEventMouseMotion.new()
	motion.position = pos
	root.push_input(motion, true)
	for pressed in [true, false]:
		var event := InputEventMouseButton.new()
		event.position = pos
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = pressed
		root.push_input(event, true)
		await process_frame


func _key(target: Viewport, key: Key) -> void:
	for pressed in [true, false]:
		var event := InputEventKey.new()
		event.keycode = key
		event.pressed = pressed
		target.push_input(event, true)
		await process_frame


func _choose_sort(control: OptionButton, mode: int) -> void:
	await _click(control)
	var popup := control.get_popup()
	_check(popup.visible, "sort dropdown opens through mouse input")
	if not popup.visible:
		return
	if popup.get_focused_item() < 0:
		await _key(root, KEY_DOWN)
	var focused := popup.get_focused_item()
	for i in range(absi(mode - focused)):
		await _key(root, KEY_DOWN if mode > focused else KEY_UP)
	await _key(root, KEY_ENTER)
	_check(control.selected == mode and not popup.visible, "dropdown keyboard selects mode %d" % mode)


func _run() -> void:
	root.size = Vector2i(1024, 768)
	root.gui_embed_subwindows = true
	var scene: PackedScene = load("res://main.tscn")
	var main = scene.instantiate()
	root.add_child(main)
	await process_frame
	main.set_physics_process(false)
	var panel = main.return_panel
	_check(main.battle.units.size() == 8, "default roster starts intact")
	await _capture("default")
	for route in range(2):
		panel.route_select.select(route)
		await _click(panel.start_button)
		if main.return_demo == null:
			_check(false, "launcher click did not start session; viewport=%s button=%s" % [str(root.size), str(panel.start_button.get_global_rect())])
			quit(1)
			return
		_check(main.battle.units.size() == 7, "demo has three allies plus four enemies")
		_check(main.return_demo.stage == "battle", "battle before result")
		main._physics_process(10000.0)
		_check(main.battle.finished, "actual battle finishes")
		_check(main.return_demo.stage == "result", "main publishes terminal to demo")
		_check(main.return_demo.view()["summary"]["total_after"] == [35881, 53324][route], "route-specific calculated total")
		_check(panel.blocks_battle_input(), "result panel blocks map input")
		var battle_before = main.battle
		var r := InputEventKey.new()
		r.keycode = KEY_R
		r.pressed = true
		main._unhandled_input(r)
		_check(main.battle == battle_before, "result blocks restart shortcut")
		var mouse := InputEventMouseButton.new()
		mouse.pressed = true
		mouse.button_index = MOUSE_BUTTON_LEFT
		mouse.position = Vector2(400, 400)
		main._unhandled_input(mouse)
		_check(main.locked_cell == Vector2i(-1, -1), "result blocks map selection")
		await _capture("route_%d_result" % route)
		await _click(panel.confirm_button)
		_check(main.return_demo.stage == "settled", "button confirms")
		await _click(panel.school_button)
		_check(main.return_demo.stage == "school", "button enters school")
		_check(panel.roster.item_count == 4, "school roster includes joined student")
		var final = main.return_demo.view()
		var snapshot: Dictionary = final["snapshot"]
		var observation := {"route": route, "stage": final["stage"], "boot_revision": final["revision"],
			"month": snapshot["month"], "week": snapshot["week"], "total_points": snapshot["global_total_511c"],
			"student_ids": snapshot["school"]["student_ids"].slice(0, 4),
			"idle_student_ids": snapshot["school"]["school_control"]["idle_student_ids"],
			"terminal": {"frame": final["terminal"]["frame"], "winner": final["terminal"]["winner"]},
			"live_witness": final["live_witness"], "authorizes_persistent_write": final["authorizes_persistent_write"]}
		await _click(panel.roster, panel.roster.global_position + panel.roster.get_item_rect(1).get_center())
		_check(panel.detail.text.contains("学生 #5"), "mouse selects joined student")
		_check(panel.roster.get_selected_items() == PackedInt32Array([1]), "roster highlight matches details")
		await _choose_sort(panel.sort_select, 1)
		_check(panel._student_ids == [5, 4, 9, 3], "category choice changes actual waiting order")
		_check(panel.roster.get_selected_items() == PackedInt32Array([0]) and panel._selected_id == 5,
			"category sorting preserves selected student")
		var category = main.return_demo.view()
		var expected: Dictionary = final["snapshot"].duplicate(true)
		expected["school"]["school_control"]["idle_student_ids"] = [5, 4, 9, 3]
		expected["school"]["school_control"]["idle_sort_mode"] = 1
		_check(category["snapshot"] == expected and category["revision"] == 7, "category writes only list and mode")
		await _capture("route_%d_school" % route)
		var wheel := InputEventMouseButton.new()
		wheel.position = panel.detail.get_global_rect().get_center()
		wheel.button_index = MOUSE_BUTTON_WHEEL_DOWN
		wheel.pressed = true
		root.push_input(wheel, true)
		wheel.pressed = false
		root.push_input(wheel, true)
		await process_frame
		_check(panel.detail.get_v_scroll_bar().value > 0, "mouse wheel scrolls school details")
		await _click(panel.back_button)
		await _click(panel.school_button)
		_check(main.return_demo.view() == category, "navigation retains category order without resettlement")
		_check(panel.sort_select.selected == 1 and panel._selected_id == 5, "navigation retains selector and student")
		await _choose_sort(panel.sort_select, 1)
		_check(main.return_demo.view() == category, "same-mode menu action does not publish")
		await _choose_sort(panel.sort_select, 0)
		_check(panel._student_ids == [3, 5, 4, 9] and panel._selected_id == 5, "level choice preserves selection")
		_check(main.return_demo.view()["revision"] == 8, "level changes publish once")
		await _choose_sort(panel.sort_select, 2)
		_check(panel._student_ids == [3, 5, 4, 9] and panel._selected_id == 5, "attribute choice preserves selection")
		var sorted_view = main.return_demo.view()
		expected["school"]["school_control"]["idle_student_ids"] = [3, 5, 4, 9]
		expected["school"]["school_control"]["idle_sort_mode"] = 2
		_check(sorted_view["snapshot"] == expected and sorted_view["revision"] == 9, "three modes leave all other fields intact")
		_check(main.return_demo.journal().filter(func(row): return row["phase"] == "state7_week").size() == 1,
			"sorting never repeats week settlement")
		observation["sorted_revision"] = sorted_view["revision"]
		observation["category_order"] = category["snapshot"]["school"]["school_control"]["idle_student_ids"]
		observation["final_mode"] = 2
		observations.append(observation)
		await _capture("route_%d_attributes" % route)
		await _click(panel.start_button)
		_check(main.return_demo.stage == "battle" and main.return_demo.view()["revision"] == 0,
			"restart after sorting creates a fresh campaign")
		_check(main.return_demo.journal().is_empty(), "restart clears previous ordering journal")
		await _click(panel.default_button)
		_check(main.return_demo == null, "default removes old session")
		_check(main.battle.units.size() == 8, "default restores full roster")
		_check(not panel.blocks_battle_input(), "default restores map input")
		main._unhandled_input(r)
		_check(main.battle.units.size() == 8, "default R still restarts normal battle")
	main.queue_free()
	await process_frame
	if not capture_dir.is_empty():
		var screenshots := {}
		for name in captured_names:
			screenshots[name + ".png"] = FileAccess.get_sha256(capture_dir.path_join(name + ".png"))
		var report := {"godot_version": Engine.get_version_info()["string"], "display_driver": DisplayServer.get_name(),
			"checks": checks, "failures": failures, "routes": observations, "screenshot_sha256": screenshots,
			"execution_scope": "local_prototype_ui_with_explicit_native_replay_inputs"}
		var file := FileAccess.open(capture_dir.path_join("verification.json"), FileAccess.WRITE)
		file.store_string(JSON.stringify(report, "  ") + "\n")
		file.close()
	print("Campaign return window: 2 routes, %d checks, %d failures" % [checks, failures.size()])
	quit(0 if failures.is_empty() else 1)
