extends "res://ui/tests/test_school_opening_dialogue_window.gd"


func _stage_bounds(viewer) -> void:
	for index in range(5): await process_frame
	var stage = viewer.opening_stage
	_check(stage.get_global_rect().encloses(stage.logical.get_global_rect()),"original 1024x768 stage fits available map area")
	for layer in stage.layers:
		for record in layer["records"]:
			var label: Label = record["label"]
			_check(root.get_visible_rect().encloses(label.get_global_rect()),"all retained dialogue rows fit viewport")
			_check(label.size.y >= label.get_line_count()*label.get_line_height(),"every wrapped row is readable without clipping")
		if layer["name"] != null:
			_check(root.get_visible_rect().encloses(layer["name"].get_global_rect()),"source actor name fits viewport")
	for control in [viewer.dialogue_previous,viewer.dialogue_next,viewer.dialogue_finish,viewer.dialogue_close]:
		_check(root.get_visible_rect().encloses(control.get_global_rect()),"stage controls remain accessible")


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
	var state: Dictionary = panel.model.state(); var disk := FileAccess.get_sha256(TEST_PATH)
	var viewer = panel.map_preview
	await _click(panel.adventure_map_button); await _click(viewer.dialogue_button)
	var stage = viewer.opening_stage
	stage.set_process(false)
	_check(viewer.dialogue_index == 0 and stage.layers.size() == 1,"opening begins with original narrator frame")
	stage.show_page(0)
	stage._process(0.1)
	_check(stage.age_ticks == 6,"visible visual clock advances at declared 60 ticks per second")
	stage._process(1000.0)
	_check(stage.age_ticks == 18,"large frame delta is bounded rather than completing an entire scene")
	await _key(KEY_SPACE)
	_check(stage.display_ready() and viewer.dialogue_index == 0,"space completes current visual fade without skipping text")
	await _stage_bounds(viewer); await _capture("narrator_1024")
	await _key(KEY_ENTER)
	_check(viewer.dialogue_index == 1 and stage.layers[0]["records"].size() == 2,"enter retains first line when adding second")
	await _click(viewer.dialogue_finish)
	await _key(KEY_RIGHT)
	_check(viewer.dialogue_index == 2 and stage.layers.size() == 2,"source character4 enters beside retained narrator")
	var native: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://ui/tests/fixtures/school_opening_native_visual.json")))
	for point in native["character_points"]:
		stage.show_page(2); stage.advance_ticks(point["tick"])
		var actor = stage.layers[0]
		_check(roundi(actor["canvas"].actor_alpha*255) == point["actor_alpha"],"body opacity matches captured original update")
		_check(roundi(actor["canvas"].frame_alpha*255) == point["frame_alpha"],"frame opacity matches captured original update")
		_check(roundi(actor["canvas"].fill_alpha*255) == point["fill_alpha"],"fill opacity matches captured original update")
		_check(actor["name"].visible == point["name_visible"],"name appears at original steady-frame boundary")
	for point in native["text_points"]:
		stage.show_page(2); stage.advance_ticks(point["tick"])
		_check(roundi(stage.current_text.modulate.a*255) == point["alpha"],"third-line opacity matches captured original text updates")
	stage.finish_display()
	await _stage_bounds(viewer); await _capture("cecily_1024")
	for index in range(3,10):
		await _click(viewer.dialogue_next); stage.finish_display()
		_check(viewer.dialogue_index == index and viewer.dialogue_text.text == viewer.dialogue_pages[index]["text"],"all ten source texts remain in order")
		await _stage_bounds(viewer); _unchanged(panel,state,disk)
		if index == 4:
			_check(stage.layers.size() == 3 and stage.layers[0]["name"].text == "伊里安" and stage.layers[1]["name"].text == "瑟希莉絲","source actor switch retains both named original portraits")
			await _capture("both_characters_1024")
		if index == 6:
			_check(stage.layers[0]["records"].size() == 3,"three student lines accumulate in source layer")
			await _capture("three_lines_1024")
	_check(viewer.dialogue_next.disabled,"final source page has no battle-start action")
	await _capture("final_1024")
	for window_size in [Vector2i(1280,800),Vector2i(800,600)]:
		root.size = window_size
		await _stage_bounds(viewer)
		await _capture("final_%d" % window_size.x)
		await _key(KEY_LEFT); stage.finish_display()
		_check(viewer.dialogue_index == 8,"previous works in resized viewport")
		await _key(KEY_RIGHT); stage.finish_display()
		_unchanged(panel,state,disk)
	root.size = Vector2i(1024,768)
	await _key(KEY_ESCAPE)
	_check(viewer.visible and not viewer.dialogue_panel.visible,"escape returns to interactive map")
	await _click(viewer.dialogue_button)
	_check(viewer.dialogue_index == 0,"reopen resets presentation without saving plot progress")
	stage.finish_display(); await _click(viewer.dialogue_close)
	await _wheel(viewer.canvas,true)
	_check(not viewer.canvas.fit_mode,"map dragging/zoom ownership returns after close")
	await _key(KEY_ESCAPE); _unchanged(panel,state,disk)
	_check(not viewer.open_dialogue(),"closed map cannot expose opening")
	panel.queue_free(); await process_frame; _cleanup(); _finish()
