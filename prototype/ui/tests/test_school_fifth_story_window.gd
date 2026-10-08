extends "res://ui/tests/test_school_story_window.gd"
const Roles := preload("res://sim/all_result_role_replay.gd")


func _portrait_bounds(reader) -> void:
	await _story_bounds(reader)
	for portrait in reader.portraits:
		_check(portrait.visible and portrait.texture != null,"three source SC portraits are visible")
		_check(portrait.get_global_rect().end.y < reader.dialogue.get_global_rect().position.y,
			"small portraits end above dialogue")
	_check(reader.portraits[0].get_global_rect().end.x < reader.portraits[1].get_global_rect().position.x,
		"first two small portraits do not overlap")
	_check(reader.portraits[1].get_global_rect().end.x < reader.portraits[2].get_global_rect().position.x,
		"last two small portraits do not overlap")
	_check(not reader.actors[0].visible and not reader.actors[1].visible,"source ALLOFF removes preceding body art")


func _run() -> void:
	_cleanup()
	root.size = Vector2i(1024,768)
	root.gui_embed_subwindows = true
	if root.has_meta("school_playground_save_path"):
		root.remove_meta("school_playground_save_path")
	var fixture: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_playground_legacy_v2.json")))
	var legacy: Dictionary = fixture["cases"][1]
	var file := FileAccess.open(TEST_PATH,FileAccess.WRITE)
	file.store_string(JSON.stringify(legacy["save"]))
	file.close()
	var panel = load("res://school_playground.tscn").instantiate()
	panel.save_path = TEST_PATH
	root.add_child(panel)
	current_scene = panel
	for index in range(5):
		await process_frame
	_check(panel.arrival.visible and panel.model._version2_state() == legacy["state"],"old version2 arrival loads into current UI")
	_check(panel.arrival.continue_button.visible,"arrival offers actual fifth-week story")
	await _capture("migrated_arrival")
	var school: Dictionary = panel.model._school_state()
	var week: Dictionary = panel.model.state()["week"]
	await _click(panel.arrival.continue_button)
	var reader = panel.story_reader
	_check(reader.visible and panel.page == "fifth_story","continue opens fifth-week reader")
	_check(reader.heading.text.begins_with("4月 · 第5周") and reader.speaker.text == "伊里安","fifth calendar and source first speaker")
	_check(reader.dialogue.text == "為什麼……\n為什麼事情會變成這樣呢……","first source text")
	await _story_bounds(reader)
	await _capture("fifth_opening")
	await _key(KEY_SPACE)
	_check(panel.model.state()["fifth_story"]["cursor"] == 1,"space advances fifth cursor exactly once")
	_check(panel.model.state()["story"]["cursor"] == 109,"fourth story stays completed")
	await _key(KEY_LEFT)
	_check(panel.model.state()["fifth_story"]["cursor"] == 0,"left revisits fifth text")
	for index in range(17):
		await _key(KEY_ENTER)
	_check(reader.actors[0].visible and reader.actors[1].visible,"source large-character pair")
	_check(reader.speaker.text == "奧吉爾","current board speaker follows source")
	await _story_bounds(reader)
	await _capture("fifth_body_pair")
	while panel.model.state()["fifth_story"]["cursor"] < 83:
		panel._story_command("fifth_next")
	await _story_bounds(reader)
	await _capture("fifth_long_dialogue")
	await _key(KEY_ESCAPE)
	_check(panel.arrival.visible and panel.model.state()["fifth_story"]["cursor"] == 83,"escape returns to arrival retaining fifth cursor")
	await _click(panel.arrival.continue_button)
	_check(reader.visible and panel.model.state()["fifth_story"]["cursor"] == 83,"arrival resumes the fifth scene")
	while panel.model.state()["fifth_story"]["cursor"] < 116:
		panel._story_command("fifth_next")
	await _portrait_bounds(reader)
	await _capture("fifth_three_portraits")
	for index in range(5):
		await _key(KEY_RIGHT)
	_check(reader.speaker.text == "娜芙忒卡" and panel.model.state()["fifth_story"]["cursor"] == 121,"CHARSET updates visible speaker and resource")
	await _portrait_bounds(reader)
	await _click(reader.save_button)
	var partial: Dictionary = panel.model.state()
	root.remove_child(panel)
	panel.queue_free()
	panel = load("res://school_playground.tscn").instantiate()
	panel.save_path = TEST_PATH
	root.add_child(panel)
	current_scene = panel
	for index in range(5):
		await process_frame
	reader = panel.story_reader
	_check(reader.visible and panel.model.state() == partial,"fresh launch restores exact fifth reading and portraits")
	await _portrait_bounds(reader)
	await _capture("fifth_restored_replacements")
	await _click(reader.skip_button)
	_check(reader.skip_dialog.visible,"fifth skip asks in-game confirmation")
	await _capture("fifth_skip_confirmation")
	var disk := FileAccess.get_sha256(TEST_PATH)
	await _dialog_click(reader.skip_dialog.get_cancel_button())
	_check(panel.model.state() == partial and FileAccess.get_sha256(TEST_PATH) == disk,"cancel skip retains memory and disk")
	for index in range(4):
		await _key(KEY_ENTER)
	_check(panel.model.state()["fifth_story"]["cursor"] == 125 and reader.next_button.text.contains("职务室"),"last source page exposes correct exit")
	await _key(KEY_ENTER)
	_check(panel.model.stage() == "workroom_entry" and panel.arrival.visible and not reader.visible,"last page enters workroom summary")
	_check(not panel.arrival.continue_button.visible and panel.arrival.calendar.text.contains("职务室"),"exit cannot repeat story action")
	_check(panel.model._school_state() == school and panel.model.state()["week"] == week,"all fifth reading and exit preserve course/MVP/week")
	_check(panel.model.state()["fifth_exit"]["after"]["flags"]["0x7a55f6"] == 2,"verified native exit flag applied")
	_check(not panel.model.state()["fifth_exit"]["handoff"]["school_initialized"],"workroom entry does not invent school boot")
	await _capture("workroom_entry")
	var exited: Dictionary = panel.model.state()
	var saved: Dictionary = panel.model.export_save()
	panel.model.execute({"op":"fifth_finish"})
	panel.model.execute({"op":"week"})
	_check(panel.model.export_save() == saved,"repeat finish/week do not append commands")
	await _click(panel.arrival.review_button)
	_check(panel.page == "results" and panel.mvp_label.text == "帕弥菈","exit can review preserved course results")
	await _result_bounds(panel)
	await _click(panel.next_button)
	_check(panel.arrival.visible and panel.model.state() == exited,"review returns to exact workroom entry")
	await _click(panel.arrival.save_button)
	root.remove_child(panel)
	panel.queue_free()
	panel = load("res://school_playground.tscn").instantiate()
	panel.save_path = TEST_PATH
	root.add_child(panel)
	current_scene = panel
	for index in range(5):
		await process_frame
	_check(panel.page == "workroom_entry" and panel.model.state() == exited,"fresh launch restores completed fifth exit")
	await _capture("restored_workroom_entry")
	disk = FileAccess.get_sha256(TEST_PATH)
	await _click(panel.arrival.restart_button)
	await _dialog_click(panel.restart_dialog.get_cancel_button())
	_check(panel.model.state() == exited and FileAccess.get_sha256(TEST_PATH) == disk,"cancel restart preserves fifth exit")
	await _click(panel.arrival.battle_button)
	for index in range(8):
		await process_frame
	var battle = current_scene
	_check(battle.scene_file_path == "res://main.tscn","workroom exit opens battle preview")
	battle.set_physics_process(false)
	await _capture("fifth_exit_battle_preview")
	await _key(KEY_SPACE)
	_check(Engine.time_scale == 0.0,"battle preview still responds to pause")
	await _click(battle.playground_button)
	for index in range(8):
		await process_frame
	panel = current_scene
	_check(panel.page == "workroom_entry" and panel.model.state() == exited,"battle return restores exact fifth exit")
	_check(Engine.time_scale == 1.0,"battle return clears pause")
	await _capture("fifth_exit_after_battle")
	panel.save_path = "user://missing_school_fifth_directory/state.json"
	await _click(panel.arrival.battle_button)
	_check(current_scene == panel and panel.model.state() == exited and panel.arrival.status.text.contains("保存失败"),
		"failed departure save retains fifth exit")
	# Verify confirmed skipping through actual UI, separately from normal END.
	panel.save_path = TEST_PATH
	await _click(panel.arrival.review_button)
	file = FileAccess.open(TEST_PATH,FileAccess.WRITE)
	file.store_string(JSON.stringify(legacy["save"]))
	file.close()
	await _click(panel.load_button)
	_check(panel.arrival.visible and panel.model.stage() == "arrival","load UI restores older arrival for skip scenario")
	await _click(panel.arrival.continue_button)
	await _click(panel.story_reader.skip_button)
	await _dialog_click(panel.story_reader.skip_dialog.get_ok_button())
	var skipped: Dictionary = panel.model.state()
	var expected_exit: Dictionary = exited.duplicate(true)
	expected_exit["revision"] = skipped["revision"] # Reading and skipping have different command counts.
	_check(panel.model.stage() == "workroom_entry" and skipped == expected_exit,
		"confirmed fifth skip reaches the same exact native exit as all pages")
	await _capture("fifth_confirmed_skip_exit")
	root.remove_meta("school_playground_save_path")
	current_scene = null
	panel.queue_free()
	await process_frame
	_cleanup()
	_finish()
