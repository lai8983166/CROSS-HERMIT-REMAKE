extends "res://ui/tests/test_school_scene_map_preview_window.gd"


func _click(control: Control) -> void:
	for index in range(3): await process_frame
	var pos := control.get_global_rect().get_center()
	var ready := control.is_visible_in_tree() and root.get_visible_rect().has_point(pos)
	_check(ready,"clickable control is visible inside logical viewport")
	if not ready:
		quit(1)
		return
	var motion := InputEventMouseMotion.new()
	motion.position = pos
	root.push_input(motion,true)
	for pressed in [true,false]:
		var event := InputEventMouseButton.new()
		event.position = pos; event.button_index = MOUSE_BUTTON_LEFT; event.pressed = pressed
		root.push_input(event,true); await process_frame


func _dialogue_bounds(viewer) -> void:
	for index in range(5): await process_frame
	var screen := root.get_visible_rect()
	for control in [viewer.dialogue_button,viewer.dialogue_panel,viewer.dialogue_text,
			viewer.dialogue_position,viewer.dialogue_previous,viewer.dialogue_next,viewer.dialogue_close]:
		_check(screen.encloses(control.get_global_rect()),"dialogue control fits viewport")
	_check(viewer.canvas.get_global_rect().encloses(viewer.dialogue_panel.get_global_rect()),"dialogue panel stays inside map")
	_check(viewer.dialogue_text.get_line_count() <= 2,"original dialogue remains readable in at most two lines")
	_check(viewer.dialogue_text.size.y >= viewer.dialogue_text.get_line_height()*viewer.dialogue_text.get_line_count(),"wrapped text is not clipped")


func _unchanged(panel, state: Dictionary, disk: String) -> void:
	_check(panel.model.state() == state and FileAccess.get_sha256(TEST_PATH) == disk,"dialogue navigation preserves state and save")
	_check(panel.adventure_start_button.disabled and panel.model.fifth_session.read_snapshot()["adventure_gate"] == 1,"dialogue preview never clears mandatory battle gate")


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
	var viewer = panel.map_preview
	_check(not viewer.open_dialogue(),"dialogue requires current supported map to be open")
	await _click(panel.adventure_map_button); await _click(viewer.dialogue_button)
	_check(viewer.dialogue_panel.visible and viewer.dialogue_index == 0,"opening dialogue begins on first page")
	_check(viewer.dialogue_text.text == "瑟希莉絲、伊里安。" and viewer.dialogue_position.text == "1 / 10","first original Big5 text is displayed")
	_check(viewer.dialogue_previous.disabled and not viewer.dialogue_next.disabled,"previous disabled at first page")
	_unchanged(panel,before,disk); await _dialogue_bounds(viewer); await _capture("opening_first_1024")
	var catalog: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(viewer.DIALOGUE))
	for index in range(1,10):
		await _click(viewer.dialogue_next)
		_check(viewer.dialogue_text.text == catalog["pages"][index]["text"] and viewer.dialogue_index == index,"next shows source text in exact order")
		_unchanged(panel,before,disk)
		if index == 2:
			await _dialogue_bounds(viewer); await _capture("opening_long_1024")
	_check(viewer.dialogue_next.disabled and not viewer.dialogue_previous.disabled,"next disabled at last page")
	await _click(viewer.dialogue_next)
	_check(viewer.dialogue_index == 9 and viewer.dialogue_text.text == "那麼，就開始吧。","last page grants no completion or battle")
	await _capture("opening_last_1024")
	await _click(viewer.dialogue_previous)
	_check(viewer.dialogue_index == 8,"previous revisits original page")
	await _key(KEY_LEFT)
	_check(viewer.dialogue_index == 7,"left arrow revisits source text")
	await _key(KEY_RIGHT)
	_check(viewer.dialogue_index == 8,"right arrow advances preview only")
	root.size = Vector2i(1280,800)
	await _dialogue_bounds(viewer); await _capture("opening_wide_1280")
	root.size = Vector2i(1024,768)
	await _dialogue_bounds(viewer)
	await _key(KEY_ESCAPE)
	_check(viewer.visible and not viewer.dialogue_panel.visible,"first Escape closes dialogue while retaining map")
	await _click(viewer.dialogue_button)
	_check(viewer.dialogue_index == 0,"reopening resets read-only preview to first page")
	await _click(viewer.dialogue_close)
	_check(viewer.visible and not viewer.dialogue_panel.visible,"dialogue close retains current map")
	await _wheel(viewer.canvas,true)
	_check(not viewer.canvas.fit_mode,"map remains interactive after dialogue closes")
	await _click(viewer.fit_button); await _key(KEY_ESCAPE)
	_check(not viewer.visible and panel.page == "adventure","second Escape returns to squad")
	_unchanged(panel,before,disk)
	await _click(panel.adventure_map_button); await _click(viewer.dialogue_button); await _click(viewer.close_button)
	_check(not viewer.visible and not viewer.dialogue_panel.visible,"closing whole map also closes dialogue")
	var unsupported: Dictionary = panel.model.adventure_preparation()
	unsupported["prepared"]["rounds"][0]["scene_id"] = 1
	_check(not viewer.open_preview(unsupported) and not viewer.open_dialogue(),"unsupported scene cannot expose opening")
	_check(viewer.valid_dialogue(catalog),"pinned original catalog passes validation")
	var raw := FileAccess.get_file_as_string(viewer.DIALOGUE)
	_check(not viewer.validated_dialogue_text(raw.replace("\n","\r\n")).is_empty(),"Windows CRLF checkout preserves source catalog identity")
	_check(viewer.validated_dialogue_text(raw.replace("瑟希莉絲","假文字")).is_empty(),"changed text cannot pass pinned catalog identity")
	for malformed in [null,true,{}, {"pages":[true]}]:
		_check(not viewer.valid_dialogue(malformed),"malformed top-level catalog refuses")
	for pair in [["scene_id",1],["mode","live_playback"],["source_script_sha256","wrong"],["pages",[true]]]:
		var changed: Dictionary = catalog.duplicate(true); changed[pair[0]] = pair[1]
		_check(not viewer.valid_dialogue(changed),"wrong identity or page shape refuses")
	for pair in [["text_index",true],["text_index",1],["text",""],["text",true]]:
		var changed: Dictionary = catalog.duplicate(true); changed["pages"][0][pair[0]] = pair[1]
		_check(not viewer.valid_dialogue(changed),"malformed page content refuses")
	# The project scales its 1024x768 canvas into smaller native windows.
	await _click(panel.adventure_map_button); await _click(viewer.dialogue_button)
	root.size = Vector2i(800,600)
	await _dialogue_bounds(viewer); await _capture("opening_compact_800")
	await _click(viewer.dialogue_next)
	_check(viewer.dialogue_index == 1,"scaled window retains working dialogue controls")
	await _click(viewer.close_button)
	root.size = Vector2i(1024,768)
	for index in range(5): await process_frame
	await _click(panel.next_button); await _click(panel.teacher_buttons[0]); await _click(panel.wait_target); await _click(panel.next_button)
	before = panel.model.state(); disk = FileAccess.get_sha256(TEST_PATH)
	panel._open_current_map()
	_check(not viewer.visible and not viewer.open_dialogue(),"unready squad cannot expose dialogue")
	_unchanged(panel,before,disk)
	panel.queue_free(); await process_frame; _cleanup(); _finish()
