extends SceneTree
## Real main scene and button/input integration. Optional --capture-dir=<absolute path>.

var failures: Array[String] = []
var capture_dir := ""
var checks := 0
var observations: Array = []


func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="):
			capture_dir = arg.trim_prefix("--capture-dir=")
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


func _run() -> void:
	root.size = Vector2i(1024, 768)
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
		observations.append({"route": route, "stage": final["stage"], "revision": final["revision"],
			"month": snapshot["month"], "week": snapshot["week"], "total_points": snapshot["global_total_511c"],
			"student_ids": snapshot["school"]["student_ids"].slice(0, 4),
			"idle_student_ids": snapshot["school"]["school_control"]["idle_student_ids"],
			"terminal": {"frame": final["terminal"]["frame"], "winner": final["terminal"]["winner"]},
			"live_witness": final["live_witness"], "authorizes_persistent_write": final["authorizes_persistent_write"]})
		await _click(panel.roster, panel.roster.global_position + Vector2(80, 98))
		_check(panel.detail.text.contains("学生 #5"), "mouse selects joined student")
		_check(panel.roster.get_selected_items() == PackedInt32Array([3]), "roster highlight matches details")
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
		_check(main.return_demo.view() == final, "navigation leaves all campaign fields intact")
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
		for name in ["default", "route_0_result", "route_0_school", "route_1_result", "route_1_school"]:
			screenshots[name + ".png"] = FileAccess.get_sha256(capture_dir.path_join(name + ".png"))
		var report := {"godot_version": Engine.get_version_info()["string"], "display_driver": DisplayServer.get_name(),
			"checks": checks, "failures": failures, "routes": observations, "screenshot_sha256": screenshots,
			"execution_scope": "local_prototype_ui_with_explicit_native_replay_inputs"}
		var file := FileAccess.open(capture_dir.path_join("verification.json"), FileAccess.WRITE)
		file.store_string(JSON.stringify(report, "  ") + "\n")
		file.close()
	print("Campaign return window: 2 routes, %d checks, %d failures" % [checks, failures.size()])
	quit(0 if failures.is_empty() else 1)
