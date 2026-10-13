extends "res://ui/tests/test_school_opening_dialogue_window.gd"


func _field_bounds(trial) -> void:
	for index in range(4): await process_frame
	# Controls and input use logical viewport coordinates under canvas_items stretch.
	var screen := root.get_visible_rect()
	for control in [trial.canvas,trial.close_button,trial.pause_button,trial.stop_button,
		trial.center_button,trial.fit_button,trial.terrain_button,trial.zoom_in_button,
		trial.zoom_out_button,trial.info,trial.status]:
		_check(screen.encloses(control.get_global_rect()),"field control fits viewport: %s %s" % [control.name,control.get_global_rect()])
	for button in trial.member_buttons.values():
		_check(screen.encloses(button.get_global_rect()),"current student control fits viewport: %s %s" % [button.text,button.get_global_rect()])


func _map_click(canvas, cell: Vector2i, button_index: MouseButton) -> void:
	var point: Vector2 = canvas.global_position+canvas.point(cell)
	_check(canvas.get_global_rect().has_point(point),"command ground cell is visible: %s %s" % [cell,point])
	var motion := InputEventMouseMotion.new(); motion.position = point
	root.push_input(motion,true)
	for pressed in [true,false]:
		var event := InputEventMouseButton.new(); event.position = point
		event.button_index = button_index; event.pressed = pressed
		root.push_input(event,true); await process_frame


func _pan_field(canvas) -> void:
	var start: Vector2 = canvas.get_global_rect().get_center()
	var initial := InputEventMouseMotion.new(); initial.position = start
	root.push_input(initial,true); await process_frame
	var button := InputEventMouseButton.new(); button.position = start
	button.button_index = MOUSE_BUTTON_MIDDLE; button.pressed = true
	root.push_input(button,true); await process_frame
	var motion := InputEventMouseMotion.new(); motion.position = start+Vector2(-100,40)
	motion.relative = Vector2(-100,40); motion.button_mask = MOUSE_BUTTON_MASK_MIDDLE
	root.push_input(motion,true); await process_frame
	button = InputEventMouseButton.new(); button.position = motion.position
	button.button_index = MOUSE_BUTTON_MIDDLE; button.pressed = false
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
	var state: Dictionary = panel.model.state(); var disk := FileAccess.get_sha256(TEST_PATH)
	_check(not panel.adventure_trial_button.disabled,"ready current squad exposes labelled trial")
	await _capture("departure_trial_entry")
	await _click(panel.adventure_trial_button)
	var trial = panel.field_trial; trial.set_process(false)
	_check(trial.visible and trial.session.ready,"trial opens current student session")
	_check(trial.member_buttons.keys() == [3,4,9] and not trial.member_buttons.has(101),"three real students; teacher retained as leader")
	_check(trial.member_buttons[3].text.contains("HP 117/117") and trial.member_buttons[3].text.contains("MP 445/445"),"grown current limits appear on active roster")
	_check(trial.session.find_unit(3)["cell"] == Vector2i(10,17),"native formation starts at correct source grid")
	_check(trial.canvas.sprites.size() == 96,"source student presentation assets loaded without demo fallback")
	await _field_bounds(trial); _unchanged(panel,state,disk)
	await _capture("squad_1024")
	await _map_click(trial.canvas,Vector2i(11,16),MOUSE_BUTTON_LEFT)
	_check(trial.session.selected_id == 4 and trial.member_buttons[4].button_pressed,"map ground click selects actual student")
	await _click(trial.member_buttons[3])
	_check(trial.session.selected_id == 3 and trial.member_buttons[3].button_pressed,"roster control selects actual student")
	await _map_click(trial.canvas,Vector2i(12,20),MOUSE_BUTTON_RIGHT)
	_check(trial.session.find_unit(3)["destination"] == Vector2i(12,20) and not trial.session.find_unit(3)["path"].is_empty(),"right click sends exact reachable movement command")
	await _capture("move_command")
	for index in range(24): trial.session.tick()
	trial._refresh()
	_check(trial.session.find_unit(3)["cell"] != Vector2i(10,17) and trial.session.find_unit(3)["visual"] == "move","command produces moving source sprite")
	await _capture("walking")
	await _key(KEY_SPACE)
	var frame: int = trial.session.frame; var units: Array = trial.session.read_units()
	trial._process(10.0)
	_check(trial.session.paused and trial.pause_button.text == "继续" and trial.session.frame == frame and trial.session.read_units() == units,"keyboard pause freezes entire movement and animation clock")
	await _capture("paused")
	await _click(trial.pause_button)
	_check(not trial.session.paused,"button resumes held movement")
	await _click(trial.stop_button)
	_check(trial.session.find_unit(3)["path"].is_empty() and trial.session.find_unit(3)["visual"] == "idle","stop cancels current command")
	await _map_click(trial.canvas,Vector2i(12,20),MOUSE_BUTTON_RIGHT)
	for index in range(180): trial.session.tick()
	trial._refresh()
	_check(trial.session.find_unit(3)["cell"] == Vector2i(12,20),"moving student reaches exact destination")
	_check(trial.session.find_unit(3)["limits"]["hp"] == 117,"trial movement causes no invented damage")
	await _map_click(trial.canvas,trial.session.find_unit(4)["cell"],MOUSE_BUTTON_RIGHT)
	_check(trial.status.text.contains("被阻挡") and trial.session.find_unit(3)["path"].is_empty(),"occupied destination visibly refused")
	await _click(trial.terrain_button)
	_check(trial.canvas.show_terrain,"terrain control displays source blocked and reserved cells")
	await _capture("terrain_obstacles")
	await _click(trial.terrain_button); await _click(trial.fit_button)
	_check(trial.canvas.fit_mode,"full map control fits MAP05")
	await _capture("map_fit")
	var zoom: float = trial.canvas.zoom
	await _wheel(trial.canvas,true)
	_check(trial.canvas.zoom > zoom,"wheel zoom reaches field map")
	await _click(trial.center_button)
	var origin: Vector2 = trial.canvas.origin
	await _pan_field(trial.canvas)
	_check(trial.canvas.origin != origin and not trial.canvas.dragging,"middle mouse pans and releases field camera")
	await _click(trial.center_button)
	for window in [Vector2i(1280,800),Vector2i(800,600)]:
		root.size = window; await _field_bounds(trial); await _click(trial.center_button)
		for unit in trial.session.units:
			_check(trial.canvas.get_rect().has_point(trial.canvas.point(unit["cell"])+trial.canvas.position),"recentered students remain visible after resize")
		await _capture("squad_%d" % window.x); _unchanged(panel,state,disk)
	root.size = Vector2i(1024,768)
	await _key(KEY_ESCAPE)
	_check(not trial.visible and not trial.session.ready and trial.session.units.is_empty(),"Escape destroys transient session and returns exact school")
	_unchanged(panel,state,disk)
	await _capture("returned_school")
	await _click(panel.adventure_trial_button)
	_check(trial.session.frame == 0 and trial.session.find_unit(3)["cell"] == Vector2i(10,17),"reopen recomputes source deployment rather than saving trial movement")
	await _map_click(trial.canvas,Vector2i(12,20),MOUSE_BUTTON_RIGHT)
	trial.set_process(true)
	await create_timer(0.15).timeout
	trial.set_process(false)
	_check(trial.session.frame > 0,"real viewport frame processing advances the isolated movement clock")
	await _key(KEY_S)
	_check(trial.session.find_unit(3)["path"].is_empty(),"S keyboard command stops active movement")
	_unchanged(panel,state,disk)
	await _click(trial.close_button)
	await _click(panel.next_button)
	await _click(panel.student_buttons[0][2]); await _click(panel.wait_target)
	await _click(panel.next_button)
	state = panel.model.state(); disk = FileAccess.get_sha256(TEST_PATH)
	await _click(panel.adventure_trial_button)
	_check(trial.member_buttons.keys() == [3,4] and trial.session.find_unit(9).is_empty(),"edited waiting student excluded from actual field")
	await _field_bounds(trial); await _capture("edited_squad")
	_unchanged(panel,state,disk)
	var current: Array = trial.session.read_units()
	_check(not trial.open_trial({},panel.adventure_limits,{}) and trial.visible and trial.session.read_units() == current,"malformed reopen preserves active session atomically")
	await _click(trial.close_button)
	var entry: Dictionary = panel.model._school_entry.duplicate(true)
	panel.model._school_entry["after"]["participants"][0]["equipped_items"][0] = 1
	panel.refresh()
	_check(panel.adventure_trial_button.disabled,"unsupported equipment disables trial with no demo fallback")
	_check(not trial.open_trial(panel.model.adventure_preparation(),panel.model.adventure_combat_limits(),{}) and not trial.visible,"invalid current loadout cannot open field")
	panel.model._school_entry = entry; panel.refresh()
	await _click(panel.next_button); await _click(panel.teacher_buttons[0]); await _click(panel.wait_target)
	await _click(panel.next_button)
	_check(panel.adventure_trial_button.disabled and not trial.visible,"unready teacher plan prevents trial")
	_check(panel.adventure_start_button.disabled,"formal mandatory combat remains gated")
	panel.queue_free(); await process_frame; _cleanup(); _finish()
