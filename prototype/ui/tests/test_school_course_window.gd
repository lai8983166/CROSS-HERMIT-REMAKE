extends "res://ui/tests/test_new_game_school_window.gd"
## Real viewport input across source, example, course and grouping pages.

const Group = preload("res://sim/school_teacher_group_replay.gd")


func _option(control: OptionButton, index: int) -> void:
	await _click(control)
	var popup := control.get_popup()
	var pos := Vector2(popup.position) + Vector2(popup.size.x / 2.0,4 + (popup.size.y - 8.0) / popup.item_count * (index + 0.5))
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
	_check(control.selected == index,"popup selects requested option")


func _course_row(list: ItemList, index: int) -> void:
	await process_frame
	var pos := list.get_global_rect().position + list.get_item_rect(index).get_center()
	_check(Rect2(Vector2.ZERO,Vector2(root.size)).has_point(pos),"course row is inside viewport")
	for pressed in [true,false]:
		var event := InputEventMouseButton.new()
		event.position = pos
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = pressed
		root.push_input(event,true)
		await process_frame


func _words(panel, group: int) -> Array:
	var raw: Array = panel.session.read_snapshot()["group_raw_bytes"]
	var words := []
	for offset in [6,8,10,12]:
		words.append(Group._word(raw,group * 28 + offset))
	return words


func _run() -> void:
	root.size = Vector2i(1024,768)
	root.gui_embed_subwindows = true
	var main = load("res://main.tscn").instantiate()
	root.add_child(main)
	await process_frame
	main.set_physics_process(false)
	await _click(main.return_panel.start_button)
	main._physics_process(10000.0)
	await _click(main.return_panel.confirm_button)
	await _click(main.return_panel.school_button)
	var returned = main.return_demo
	var returned_before: Dictionary = returned.view().duplicate(true)
	var battle = main.battle
	var frame: int = battle.frame
	await _click(main.return_panel.new_school_button)
	var panel = main.school_panel
	var source = panel.session
	var boot: Dictionary = source.read_snapshot()
	await _capture("source_grouping")
	await _click(panel.course_button)
	_check(panel._course_content.visible and not panel._group_content.visible,"course navigation shows its own page")
	_check(panel.course_lists[0].item_count == 0 and panel.course_lists[1].item_count == 0 and panel.course_lists[2].item_count == 0,"source week zero has no courses")
	_check(source.revision() == 2 and source.read_snapshot() == boot,"course browsing has no writes")
	await _option(panel.class_mode,1)
	_check(source.revision() == 3 and source.read_snapshot()["group_raw_bytes"][3] == 1,"source mode change publishes once")
	_check(panel.assign_button.disabled and panel.course_info.text.contains("最早在4月第4周"),"empty source list explains example and prevents assignment")
	var source_edited: Dictionary = source.read_snapshot()
	await _capture("source_no_courses")
	await _click(panel.example_button)
	var example = panel.session
	var example_boot: Dictionary = example.read_snapshot()
	_check(example != source and example.revision() == 3 and example.school_context() == "declared_course_example_4_4","example owns separate declared date session")
	_check(example_boot["month"] == 4 and example_boot["week"] == 4,"example date is 4/4")
	_check(panel.status_label.text.contains("第4周课程示例") and panel._note.text.contains("独立示例输入"),"example scope is visible")
	_check(panel.course_lists[0].item_count == 3 and panel.course_lists[1].item_count == 0 and panel.course_lists[2].item_count == 0,"example displays three source basic courses")
	var identities := []
	for index in range(3):
		identities.append(panel.course_lists[0].get_item_metadata(index))
	_check(identities == [12,11,10],"source course order is preserved")
	_check(panel.assign_button.disabled and panel.class_mode.selected == 0,"adventure cannot assign")
	await _capture("example_available")
	await _course_row(panel.course_lists[0],0)
	_check(panel._course_selected == 12 and panel.assign_button.disabled,"choosing course alone does not assign in adventure")
	_check(example.revision() == 3 and example.read_snapshot() == example_boot,"row browsing does not publish")
	await _option(panel.class_mode,1)
	_check(example.revision() == 4 and not panel.assign_button.disabled,"teaching enables selected course")
	await _click(panel.assign_button)
	_check(example.revision() == 5 and _words(panel,0) == [0,11,12,0],"real click assigns source four words")
	_check(panel.course_info.text.contains("#12") and panel._view["ratings"][0]["state"] == 4,"assignment and source rating render")
	await _course_row(panel.course_lists[0],2)
	await _click(panel.assign_button)
	_check(example.revision() == 6 and _words(panel,0) == [0,9,10,2],"replacement selects real source ordinal")
	await _click(panel.assign_button)
	_check(example.revision() == 6,"duplicate assignment does not republish")
	for key in ["member_profiles","relationships","availability","raw_student_ids","raw_teacher_ids","month","week","global_total_511c","course_buffers","course_counts","course_unlocked_flags"]:
		_check(example.read_snapshot()[key] == example_boot[key],"planning preserves " + key)
	await _capture("example_assigned")
	await _option(panel.course_group,1)
	_check(panel.class_mode.disabled and panel.assign_button.disabled and panel.course_info.text.contains("先在编班页面"),"teacherless class refuses through controls")
	_check(example.revision() == 6,"class navigation has no writes")
	await _option(panel.course_group,0)
	_check(panel.course_info.text.contains("#10"),"returning class retains assignment")
	await _click(panel.group_button)
	_check(panel._ratings[0].text.contains("课程 #10"),"grouping displays assigned course")
	await _click(panel.teacher_buttons[0])
	await _click(panel.teacher_buttons[1])
	_check(example.revision() == 7 and example.read_snapshot()["derived_teacher_ids"] == [-1,101,-1,-1,-1],"example still supports grouping")
	_check(_words(panel,0)[1] == -1,"teacher movement clears old course view")
	var example_edited: Dictionary = example.read_snapshot()
	await _capture("example_teacher_moved")
	await _click(panel.source_button)
	_check(panel.session == source and source.revision() == 3 and source.read_snapshot() == source_edited,"source switch restores exact owned edits")
	await _click(panel.course_button)
	_check(panel.course_lists[0].item_count == 0 and not panel.status_label.text.contains("示例"),"example courses do not enter source school")
	await _click(panel.example_button)
	_check(panel.session == example and example.read_snapshot() == example_edited,"example switch preserves its edits")
	await _key(KEY_R)
	await _key(KEY_SPACE)
	await _key(KEY_ESCAPE)
	main._physics_process(10000.0)
	_check(main.battle == battle and battle.frame == frame,"course window isolates battle keys and ticks")
	_check(example.read_snapshot() == example_edited and example.revision() == 7,"cancel and battle keys preserve course session")
	_check(returned.view() == returned_before,"returned campaign remains independent of both schools")
	await _click(panel.close_button)
	_check(main.return_panel.visible and returned.view() == returned_before,"close restores original returned page")
	await _click(main.return_panel.new_school_button)
	_check(panel.session == example and example.read_snapshot() == example_edited,"reopening retains active example")
	await _click(panel.restart_button)
	_check(panel.session != example and panel.session.revision() == 3 and panel.session.read_snapshot() == example_boot,"restart resets active example only")
	_check(source.read_snapshot() == source_edited and source.revision() == 3,"example restart preserves source")
	await _capture("example_restart")
	await _click(panel.source_button)
	await _click(panel.restart_button)
	_check(panel.session != source and panel.session.revision() == 2 and panel.session.read_snapshot() == boot,"source restart retains original week zero")
	_check(panel._example_session.read_snapshot() == example_boot,"source restart preserves example")
	main.queue_free()
	await process_frame
	if not capture_dir.is_empty():
		var screenshots := {}
		for name in captured:
			screenshots[name + ".png"] = FileAccess.get_sha256(capture_dir.path_join(name + ".png"))
		var file := FileAccess.open(capture_dir.path_join("verification.json"),FileAccess.WRITE)
		file.store_string(JSON.stringify({"checks":checks,"failures":failures,"godot_version":Engine.get_version_info()["string"],"display_driver":DisplayServer.get_name(),"screenshot_sha256":screenshots,"execution_scope":"local_prototype_declared_4_4_example_course_and_grouping_real_input"},"  ") + "\n")
		file.close()
	print("School course window: %d checks, %d failures" % [checks,failures.size()])
	quit(0 if failures.is_empty() else 1)
