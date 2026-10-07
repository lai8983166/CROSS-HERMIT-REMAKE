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
	_check(not panel.settle_button.visible and not panel.growth_summary.visible,"source does not offer example settlement")
	await _click(panel.example_button)
	var example = panel.session
	var boot: Dictionary = example.read_snapshot()
	_check(panel.settle_button.visible and panel.settle_button.disabled,"example requires an assigned course")
	await _course_row(panel.course_lists[0],2)
	_check(panel._course_selected == 10 and panel.settle_button.disabled,"course selection alone is insufficient")
	await _option(panel.class_mode,1)
	_check(panel.settle_button.disabled,"teaching alone is insufficient")
	await _click(panel.assign_button)
	_check(not panel.settle_button.disabled,"source-ready assigned class enables settlement")
	_check(example.revision() == 5 and example.read_growth_records().is_empty(),"planning has not grown students")
	await _capture("before_settlement")
	await _click(panel.settle_button)
	var data: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_settlement_evidence_v1.json")))
	var expected: Dictionary = data["cases"][2]
	_check(example.revision() == 6 and example.read_snapshot() == expected["after"],"real settlement click matches native source school")
	_check(example.read_growth_records() == expected["after_records"],"real click publishes complete native growth records")
	_check(panel.settle_button.disabled and panel.settle_button.text.contains("已结算"),"completed button prevents replay")
	_check(panel.growth_summary.visible and panel.growth_summary.text.contains("10350"),"source bonus is visible")
	for record in expected["after_records"]:
		_check(panel.growth_summary.text.contains("学生 #%d" % record["character_id"]),"participating student appears in summary")
	for index in range(3):
		_check(panel.growth_summary.text.contains("Lv.%d→%d" % [expected["before_records"][index]["level_50"],expected["after_records"][index]["level_50"]]),"source-recalculated student level renders")
		for k in range(7):
			var old_value: int = expected["before_records"][index]["attributes"][k]
			var new_value: int = expected["after_records"][index]["attributes"][k]
			if old_value != new_value:
				_check(panel.growth_summary.text.contains("%s%d→%d" % [["力","敏","感","活","智","耐","精"][k],old_value,new_value]),"source attribute change renders")
		for sid in range(84):
			if expected["before_records"][index]["skill_statuses"][sid] != 2 and expected["after_records"][index]["skill_statuses"][sid] == 2:
				_check(panel.growth_summary.text.contains("新技能 #%d" % (sid+1)),"source new skill renders")
	_check(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(panel.growth_summary.get_global_rect()),"complete summary stays inside viewport")
	_check(panel.status_label.text.contains("第4周") and panel.growth_summary.text.contains("日期不变"),"settlement date boundary remains explicit")
	_check(source.read_snapshot() == source_before and returned.view() == returned_before,"growth preserves source and returned sessions")
	var grown: Dictionary = example.read_snapshot()
	var growth: Array = example.read_growth_records()
	var journal: Array = example.journal()
	await _capture("settled_course10")
	await _click(panel.settle_button)
	_check(example.revision() == 6 and example.read_snapshot() == grown and example.journal() == journal,"disabled repeat click has no writes")
	await _key(KEY_R)
	await _key(KEY_SPACE)
	await _key(KEY_ESCAPE)
	main._physics_process(10000.0)
	_check(main.battle == battle and battle.frame == frame,"settlement page blocks battle keys and ticks")
	_check(example.read_growth_records() == growth,"keys do not replay growth")
	await _click(panel.group_button)
	for index in range(3):
		_check(panel.student_buttons[0][index].text.contains("Lv.%d" % expected["after_records"][index]["level_50"]),"grouping cell reflects source grown level")
	await _capture("grown_grouping")
	await _click(panel.student_buttons[0][2])
	await _click(panel.wait_student_target)
	_check(example.revision() == 7 and example.read_growth_records() == growth,"grouping after settlement preserves growth")
	await _click(panel.course_button)
	await _course_row(panel.course_lists[0],0)
	await _click(panel.assign_button)
	_check(example.revision() == 8 and panel.settle_button.disabled,"new assignment cannot reopen completed example")
	var edited: Dictionary = example.read_snapshot()
	await _click(panel.source_button)
	_check(panel.session == source and source.read_snapshot() == source_before,"source switch restores original week zero")
	await _click(panel.example_button)
	_check(panel.session == example and example.read_snapshot() == edited and example.read_growth_records() == growth,"example switch retains completed growth")
	_check(panel.growth_summary.text.contains("10350") and panel.settle_button.disabled,"summary retains actual settlement, not changed plan")
	await _click(panel.close_button)
	_check(returned.view() == returned_before and main.return_panel.visible,"close restores returned school")
	await _click(main.return_panel.new_school_button)
	_check(panel.session == example and example.read_growth_records() == growth,"reopen retains completed example")
	await _click(panel.restart_button)
	_check(panel.session != example and panel.session.revision() == 3 and panel.session.read_snapshot() == boot,"restart creates pristine example")
	_check(panel.session.read_settlement().is_empty() and panel.session.read_growth_records().is_empty() and not panel.growth_summary.visible,"restart clears active growth and summary")
	_check(panel.settle_button.disabled and source.read_snapshot() == source_before,"restart needs new plan and preserves source")
	await _capture("restarted_example")
	# Exercise a different native packet and summary after explicit reset.
	await _option(panel.class_mode,1)
	await _course_row(panel.course_lists[0],0)
	await _click(panel.assign_button)
	await _click(panel.settle_button)
	_check(panel.session.read_snapshot() == data["cases"][0]["after"],"reset example can settle source course12 independently")
	_check(panel.session.read_growth_records() == data["cases"][0]["after_records"],"second course has its own source records")
	_check(panel.growth_summary.text.contains("成长加成 +0"),"course12 distinct bonus renders")
	_check(Rect2(Vector2.ZERO,Vector2(root.size)).encloses(panel.growth_summary.get_global_rect()),"second summary stays inside viewport")
	await _capture("settled_course12")
	main.queue_free()
	await process_frame
	if not capture_dir.is_empty():
		var screenshots := {}
		for name in captured:
			screenshots[name + ".png"] = FileAccess.get_sha256(capture_dir.path_join(name + ".png"))
		var file := FileAccess.open(capture_dir.path_join("verification.json"),FileAccess.WRITE)
		file.store_string(JSON.stringify({"checks":checks,"failures":failures,"godot_version":Engine.get_version_info()["string"],"display_driver":DisplayServer.get_name(),"screenshot_sha256":screenshots,"execution_scope":"local_prototype_once_only_declared_date_course_growth_real_input"},"  ") + "\n")
		file.close()
	print("School course settlement window: %d checks, %d failures" % [checks,failures.size()])
	quit(0 if failures.is_empty() else 1)
