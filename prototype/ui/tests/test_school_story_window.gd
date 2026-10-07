extends "res://ui/tests/test_school_playground_results_window.gd"


func _story_bounds(reader) -> void:
	for index in range(3):
		await process_frame
	var screen := Rect2(Vector2.ZERO,Vector2(root.size))
	for control in [reader.heading,reader.speaker,reader.dialogue,reader.progress,reader.status,
			reader.next_button,reader.previous_button,reader.save_button,reader.return_button,reader.skip_button]:
		_check(screen.encloses(control.get_global_rect()),"dialogue control fits viewport")
	_check(reader.dialogue.get_global_rect().end.y <= reader.next_button.get_global_rect().position.y,
		"dialogue ends before navigation")
	_check(reader.dialogue.size.y >= reader.dialogue.get_line_count()*reader.dialogue.get_line_height(),
		"all original text lines fit")


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
	for index in range(3):
		await _click(panel.next_button)
	var school: Dictionary = panel.model._school_state()
	await _click(panel.next_button)
	var reader = panel.story_reader
	_check(reader.visible and panel.model.stage() == "story","result action opens graphical story")
	_check(reader.speaker.text == "瑟希莉絲" and reader.dialogue.text == "……老師。","original first dialogue and speaker")
	_check(reader.previous_button.disabled,"first page cannot move before start")
	await _story_bounds(reader)
	await _capture("scene16_opening")
	await _key(KEY_SPACE)
	_check(panel.model.state()["story"]["cursor"] == 1 and reader.speaker.text == "老师","space advances exactly one page")
	await _key(KEY_LEFT)
	_check(panel.model.state()["story"]["cursor"] == 0,"left re-reads previous text")
	for index in range(8):
		await _key(KEY_ENTER)
	_check(reader.actors[0].visible and reader.actors[0].texture != null,"source CHARDISP reveals original character art")
	await _story_bounds(reader)
	await _capture("scene16_character")
	# The longest source page exercises wrapping rather than a short sample.
	var longest := 0
	for index in range(panel.model._story_pages.size()):
		if panel.model._story_pages[index]["text"].split("\n").size() == 5:
			longest = index
			break
	while panel.model.state()["story"]["cursor"] < longest:
		panel._story_command("story_next")
	await _story_bounds(reader)
	await _capture("long_dialogue")
	await _click(reader.return_button)
	_check(not reader.visible and panel.page == "results","return retains cursor and exposes course results")
	_check(panel.model._school_state() == school,"reading retains growth and MVP")
	var cursor: int = panel.model.state()["story"]["cursor"]
	await _click(panel.next_button)
	_check(reader.visible and panel.model.state()["story"]["cursor"] == cursor,"continue resumes reading")
	while panel.model.state()["story"]["cursor"] < 68:
		panel._story_command("story_next")
	await _story_bounds(reader)
	_check(reader.actors[0].visible and reader.actors[1].visible,"second scene presents both source characters")
	await _capture("scene17_characters")
	await _click(reader.save_button)
	var partial: Dictionary = panel.model.state()
	root.remove_child(panel)
	panel.queue_free()
	panel = load("res://school_playground.tscn").instantiate()
	panel.save_path = TEST_PATH
	root.add_child(panel)
	for index in range(5):
		await process_frame
	reader = panel.story_reader
	_check(reader.visible and panel.model.state() == partial,"restarted window restores exact second-scene reading")
	await _capture("restored_scene17")
	await _click(reader.skip_button)
	_check(reader.skip_dialog.visible,"skip requires in-game confirmation")
	await _capture("skip_confirmation")
	var disk := FileAccess.get_sha256(TEST_PATH)
	await _dialog_click(reader.skip_dialog.get_cancel_button())
	_check(panel.model.state() == partial and FileAccess.get_sha256(TEST_PATH) == disk,"cancel preserves memory and disk")
	await _click(reader.skip_button)
	await _dialog_click(reader.skip_dialog.get_ok_button())
	_check(panel.model.stage() == "story_completed" and not reader.visible,"confirmed skip completes bounded story")
	_check(panel.model._school_state() == school,"skip retains actual course records")
	await _capture("story_completed")
	panel.queue_free()
	await process_frame
	_cleanup()
	_finish()
