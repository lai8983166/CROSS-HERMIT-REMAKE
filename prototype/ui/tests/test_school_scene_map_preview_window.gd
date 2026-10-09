extends "res://ui/tests/test_school_adventure_preparation_window.gd"


func _map_bounds(viewer) -> void:
	for index in range(3): await process_frame
	var screen := Rect2(Vector2.ZERO,Vector2(root.size))
	for control in [viewer,viewer.canvas,viewer.title,viewer.fit_button,viewer.zoom_in_button,
			viewer.zoom_out_button,viewer.close_button]:
		_check(screen.encloses(control.get_global_rect()),"map viewer control fits viewport")
	var image_size: Vector2 = viewer.canvas.texture.get_size()*viewer.canvas.zoom
	for axis in range(2):
		if image_size[axis] > viewer.canvas.size[axis]:
			_check(viewer.canvas.origin[axis] <= 0.01 and viewer.canvas.origin[axis]+image_size[axis] >= viewer.canvas.size[axis]-0.01,"pan does not expose outside-map edges")


func _wheel(canvas, up: bool) -> void:
	var event := InputEventMouseButton.new()
	event.position = canvas.get_global_rect().get_center()
	event.button_index = MOUSE_BUTTON_WHEEL_UP if up else MOUSE_BUTTON_WHEEL_DOWN
	event.pressed = true
	root.push_input(event,true)
	await process_frame
	event.pressed = false
	root.push_input(event,true)
	await process_frame


func _drag(canvas) -> void:
	var start: Vector2 = canvas.get_global_rect().get_center()
	var initial := InputEventMouseMotion.new()
	initial.position = start
	root.push_input(initial,true); await process_frame
	var button := InputEventMouseButton.new()
	button.position = start; button.button_index = MOUSE_BUTTON_LEFT; button.pressed = true
	root.push_input(button,true); await process_frame
	var motion := InputEventMouseMotion.new()
	motion.position = start+Vector2(-120,70); motion.relative = Vector2(-120,70)
	motion.button_mask = MOUSE_BUTTON_MASK_LEFT
	root.push_input(motion,true); await process_frame
	button = InputEventMouseButton.new()
	button.position = motion.position; button.button_index = MOUSE_BUTTON_LEFT; button.pressed = false
	root.push_input(button,true); await process_frame


func _run() -> void:
	_cleanup(); root.size = Vector2i(1024,768); root.gui_embed_subwindows = true
	if root.has_meta("school_playground_save_path"): root.remove_meta("school_playground_save_path")
	var fixture: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_playground_legacy_v3.json")))
	var file := FileAccess.open(TEST_PATH,FileAccess.WRITE)
	file.store_string(JSON.stringify(fixture["cases"][1]["save"])); file.close()
	var panel = await _new_panel()
	await _click(panel.arrival.continue_button); await _click(panel.workroom.continue_button)
	await _click(panel.story_reader.skip_button); await _dialog_click(panel.story_reader.skip_dialog.get_ok_button())
	await _click(panel.next_button)
	var before: Dictionary = panel.model.state(); var disk := FileAccess.get_sha256(TEST_PATH)
	_check(not panel.adventure_map_button.disabled,"ready current scene exposes map action")
	await _preparation_bounds(panel); await _capture("departure_map_action")
	await _click(panel.adventure_map_button)
	var viewer = panel.map_preview
	_check(viewer.visible and viewer.canvas.texture.get_size() == Vector2(2048,1536),"opens exact current MAP05 art")
	_check(panel.page == "adventure" and panel.model.state() == before and FileAccess.get_sha256(TEST_PATH) == disk,"opening map preserves school and disk")
	await _map_bounds(viewer); await _capture("map_fit")
	root.size = Vector2i(1280,800)
	await _map_bounds(viewer)
	_check(viewer.canvas.fit_mode,"resizing keeps the fitted map visible")
	await _capture("map_wide")
	root.size = Vector2i(1024,768)
	await _map_bounds(viewer)
	var fit_zoom: float = viewer.canvas.zoom
	await _wheel(viewer.canvas,true)
	_check(viewer.canvas.zoom > fit_zoom,"mouse wheel zooms real map canvas")
	await _click(viewer.zoom_in_button); await _click(viewer.zoom_in_button)
	var origin: Vector2 = viewer.canvas.origin
	await _drag(viewer.canvas)
	_check(viewer.canvas.origin != origin and not viewer.canvas.dragging,"mouse drag pans and releases")
	await _map_bounds(viewer); await _capture("map_zoom_pan")
	for index in range(18): viewer.canvas.zoom_at(1.25,viewer.canvas.size*0.5)
	viewer.canvas.pan(Vector2(-100000,100000))
	_check(viewer.canvas.zoom == 2.0,"zoom upper bound enforced")
	await _map_bounds(viewer); await _capture("map_edge")
	await _click(viewer.fit_button)
	_check(is_equal_approx(viewer.canvas.zoom,fit_zoom) and viewer.canvas.fit_mode,"fit restores complete source map")
	await _key(KEY_ESCAPE)
	_check(not viewer.visible and panel.page == "adventure" and panel.model.state() == before,"Escape returns exact squad")
	await _capture("map_returned")
	await _click(panel.adventure_map_button); await _click(viewer.close_button)
	_check(not viewer.visible and FileAccess.get_sha256(TEST_PATH) == disk,"close button preserves save")
	var unsupported: Dictionary = panel.model.adventure_preparation()
	unsupported["prepared"]["rounds"][0]["scene_id"] = 1
	_check(not viewer.open_preview(unsupported) and not viewer.visible,"unsupported scene cannot open demo map")
	for malformed in [{},{"supported":true,"ready":true,"prepared":true},
			{"supported":true,"ready":true,"prepared":{"rounds":[true]}}]:
		_check(not viewer.open_preview(malformed) and not viewer.visible,"malformed scene projection refuses without a runtime error")
	await _click(panel.next_button)
	await _click(panel.student_buttons[0][2]); await _click(panel.wait_target)
	await _click(panel.next_button)
	before = panel.model.state(); disk = FileAccess.get_sha256(TEST_PATH)
	await _click(panel.adventure_map_button)
	_check(viewer.visible and panel.adventure_member_buttons.size() == 3,"edited current squad retains same map identity")
	_check(panel.model.state() == before and FileAccess.get_sha256(TEST_PATH) == disk,"edited preview never appends saved command")
	await _capture("map_waiting_squad"); await _click(viewer.close_button)
	await _click(panel.next_button); await _click(panel.teacher_buttons[0]); await _click(panel.wait_target)
	await _click(panel.next_button)
	before = panel.model.state(); disk = FileAccess.get_sha256(TEST_PATH)
	_check(panel.adventure_map_button.disabled,"unready school cannot open current map")
	await _click(panel.adventure_map_button); panel._open_current_map()
	_check(not viewer.visible and panel.model.state() == before and FileAccess.get_sha256(TEST_PATH) == disk,"direct unready call also refuses without writes")
	_check(panel.adventure_start_button.disabled and panel.model.fifth_session.read_snapshot()["adventure_gate"] == 1,"map inspection grants neither battle nor gate clearance")
	await _capture("map_unready")
	panel.queue_free(); await process_frame; _cleanup(); _finish()
