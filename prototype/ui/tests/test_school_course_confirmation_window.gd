extends "res://ui/tests/test_school_course_window.gd"

const Roles = preload("res://sim/all_result_role_replay.gd")


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
	var source_before: Dictionary = source.read_snapshot()
	await _click(panel.course_button)
	_check(not panel.confirm_button.visible and not panel.confirmation_summary.visible,"week zero hides confirmation")
	await _click(panel.example_button)
	_check(panel.confirm_button.visible and panel.confirm_button.disabled,"example confirmation requires growth")
	await _option(panel.class_mode,1)
	await _course_row(panel.course_lists[0],2)
	await _click(panel.assign_button)
	_check(panel.confirm_button.disabled,"assignment is not growth")
	await _click(panel.settle_button)
	_check(not panel.confirm_button.disabled and panel.settle_button.disabled,"growth enables separate confirmation")
	await _capture("growth_pending_confirmation")
	await _click(panel.confirm_button)
	var data: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_confirmation_evidence_v3.json")))
	var expected: Dictionary = data["cases"][0]
	var example = panel.session
	_check(example.read_snapshot() == expected["rated_after"],"real confirmation matches complete native school")
	_check(example.read_confirmation_records() == expected["after_records"],"real confirmation matches complete native career/history")
	_check(example.read_growth_records() == expected["after_growth_records"],"source career sums updated without growth replay")
	_check(example.revision() == 7 and panel.confirm_button.disabled and panel.confirm_button.text.contains("已确认"),"confirmation completes once")
	_check(panel.confirmation_summary.visible and panel.confirmation_summary.text.contains("+1×12条"),"actual relation changes appear")
	_check(panel.confirmation_summary.text.contains("日期不变") and panel.status_label.text.contains("第4周"),"date boundary stays explicit")
	for index in range(3):
		var job: int = expected["before"]["member_profiles"][index+1]["job"]
		var old_value: int = expected["before_records"][index]["job_progress"][job]
		var new_value: int = expected["after_records"][index]["job_progress"][job]
		_check(panel.confirmation_summary.text.contains("学生 #%d · 职业 #%d 进度%d→%d" % [[3,4,9][index],job,old_value,new_value]),"source career summary renders")
	_check(panel.confirmation_summary.text.count("本周授课 #10") == 3,"source weekly course shown for all three")
	_check(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(panel.confirmation_summary.get_global_rect()),"confirmation summary stays inside viewport")
	_check(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(panel.growth_summary.get_global_rect()),"growth summary stays inside viewport")
	_check(panel._note.get_global_rect().position.y >= panel.confirmation_summary.get_global_rect().end.y,"summary does not overlap date note")
	await _capture("confirmed_course10")
	var snapshot: Dictionary = example.read_snapshot()
	var records: Array = example.read_confirmation_records()
	var journal: Array = example.journal()
	await _click(panel.confirm_button)
	await _click(panel.settle_button)
	await _key(KEY_R)
	await _key(KEY_SPACE)
	await _key(KEY_ESCAPE)
	main._physics_process(10000.0)
	_check(example.revision() == 7 and example.journal() == journal and example.read_snapshot() == snapshot,"duplicate buttons and keys do not publish")
	_check(main.battle == battle and battle.frame == frame,"confirmation blocks battle ticks and keys")
	await _click(panel.group_button)
	_check(panel._ratings[0].text.contains(str(expected["ratings"][0]["relationship_mean"])),"grouping shows native new relationship mean")
	await _capture("confirmed_grouping")
	await _click(panel.course_button)
	await _course_row(panel.course_lists[0],0)
	await _click(panel.assign_button)
	_check(panel.confirmation_summary.text.count("本周授课 #10") == 3,"later course12 does not rewrite historical course10")
	_check(panel.confirm_button.disabled and example.read_confirmation_records() == records,"later planning cannot reopen confirmation")
	await _click(panel.source_button)
	_check(panel.session == source and source.read_snapshot() == source_before and not panel.confirm_button.visible,"source is independent")
	await _click(panel.example_button)
	_check(panel.session == example and example.read_confirmation_records() == records,"switch preserves confirmed example")
	await _click(panel.close_button)
	_check(returned.view() == returned_before and main.return_panel.visible,"return school remains independent")
	await _click(main.return_panel.new_school_button)
	_check(panel.session == example and panel.confirm_button.disabled and panel.confirmation_summary.visible,"reopen preserves completion")
	await _click(panel.restart_button)
	_check(panel.session != example and panel.session.read_confirmation().is_empty() and panel.session.read_confirmation_records().is_empty(),"explicit restart clears confirmation")
	_check(panel.confirm_button.disabled and not panel.confirmation_summary.visible and source.read_snapshot() == source_before,"restart restores boundary and keeps source")
	await _capture("restart_confirmation")
	# Real input for a waiting student demonstrates asymmetric relationship/history handling.
	await _click(panel.group_button)
	await _click(panel.student_buttons[0][2])
	await _click(panel.wait_student_target)
	await _click(panel.course_button)
	await _option(panel.class_mode,1)
	await _course_row(panel.course_lists[0],2)
	await _click(panel.assign_button)
	await _click(panel.settle_button)
	await _click(panel.confirm_button)
	_check(panel.session.read_snapshot() == data["cases"][2]["rated_after"],"waiting case complete native school")
	_check(panel.session.read_confirmation_records() == data["cases"][2]["after_records"],"waiting case complete native history")
	_check(panel.confirmation_summary.text.contains("本周待命") and panel.confirmation_summary.text.contains("-1×2条"),"waiting and asymmetric loss visible")
	_check(panel.confirmation_summary.text.count("本周授课 #10") == 2,"only settled participants shown as course students")
	_check(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(panel.confirmation_summary.get_global_rect()),"waiting summary fits viewport")
	await _capture("confirmed_waiting9")
	main.queue_free()
	await process_frame
	if not capture_dir.is_empty():
		var screenshots := {}
		for name in captured:
			screenshots[name+".png"] = FileAccess.get_sha256(capture_dir.path_join(name+".png"))
		var file := FileAccess.open(capture_dir.path_join("verification.json"),FileAccess.WRITE)
		file.store_string(JSON.stringify({"checks":checks,"failures":failures,"godot_version":Engine.get_version_info()["string"],"display_driver":DisplayServer.get_name(),"screenshot_sha256":screenshots,"execution_scope":"local_prototype_once_only_declared_date_course_confirmation_fields_real_input"},"  ")+"\n")
		file.close()
	print("School course confirmation window: %d checks, %d failures" % [checks,failures.size()])
	quit(0 if failures.is_empty() else 1)
