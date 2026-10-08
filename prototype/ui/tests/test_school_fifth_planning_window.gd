extends "res://ui/tests/test_school_story_window.gd"
const Roles := preload("res://sim/all_result_role_replay.gd")


func _new_panel():
	var panel = load("res://school_playground.tscn").instantiate()
	panel.save_path = TEST_PATH
	root.add_child(panel)
	current_scene = panel
	for index in range(5):
		await process_frame
	return panel


func _workroom_bounds(panel) -> void:
	for index in range(3):
		await process_frame
	var screen := Rect2(Vector2.ZERO,Vector2(root.size))
	for control in [panel.workroom.continue_button,panel.workroom.review_button,panel.workroom.save_button,
			panel.workroom.battle_button,panel.workroom.restart_button,panel.workroom.guidance,panel.workroom.status]:
		_check(screen.encloses(control.get_global_rect()),"workroom control fits screen")


func _run() -> void:
	_cleanup()
	root.size = Vector2i(1024,768)
	root.gui_embed_subwindows = true
	if root.has_meta("school_playground_save_path"):
		root.remove_meta("school_playground_save_path")
	var fixture: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_playground_legacy_v3.json")))
	var file := FileAccess.open(TEST_PATH,FileAccess.WRITE)
	file.store_string(JSON.stringify(fixture["cases"][1]["save"]))
	file.close()
	var panel = await _new_panel()
	_check(panel.model._version3_state() == fixture["cases"][1]["state"],"genuine old v3 exit restores before new entry")
	_check(panel.arrival.visible and panel.arrival.continue_button.text.contains("进入职务室"),"old exit offers new workroom")
	await _click(panel.arrival.continue_button)
	_check(panel.workroom.visible and panel.model.stage() == "workroom","entry button opens source workroom")
	await _workroom_bounds(panel)
	await _capture("workroom_open")
	await _click(panel.workroom.save_button)
	var work_state: Dictionary = panel.model.state()
	root.remove_child(panel);panel.queue_free()
	panel = await _new_panel()
	_check(panel.workroom.visible and panel.model.state() == work_state,"fresh launch restores workroom")
	await _capture("restored_workroom")
	await _click(panel.workroom.continue_button)
	var reader = panel.story_reader
	_check(reader.visible and panel.page == "work_story","continue enters actual Chapter205")
	_check(reader.dialogue.text == "……您是說巡邏班吧？" and reader.speaker.text == "老师","source narrator and original first text")
	await _story_bounds(reader)
	await _capture("patrol_opening")
	await _key(KEY_SPACE)
	_check(panel.model.state()["work_story"]["cursor"] == 1,"space advances actual workroom cursor once")
	_check(reader.portraits[0].visible and reader.portraits[0].texture != null,"original portrait117 visible")
	await _key(KEY_LEFT)
	_check(panel.model.state()["work_story"]["cursor"] == 0,"left revisits narrator")
	for index in range(8):
		await _key(KEY_ENTER)
	await _story_bounds(reader)
	_check(reader.portraits[0].visible and reader.portraits[1].visible,"source workroom portrait pair")
	await _capture("patrol_portraits")
	await _key(KEY_ESCAPE)
	_check(panel.workroom.visible and panel.model.state()["work_story"]["cursor"] == 8,"escape preserves patrol position")
	await _click(panel.workroom.continue_button)
	_check(reader.visible and panel.model.state()["work_story"]["cursor"] == 8,"workroom resumes patrol")
	await _click(reader.save_button)
	var partial: Dictionary = panel.model.state()
	root.remove_child(panel);panel.queue_free()
	panel = await _new_panel()
	reader = panel.story_reader
	_check(reader.visible and panel.model.state() == partial,"fresh launch restores exact patrol text and art")
	await _capture("restored_patrol")
	await _click(reader.skip_button)
	_check(reader.skip_dialog.visible,"patrol skip requests in-game confirmation")
	await _capture("patrol_skip_confirmation")
	var disk := FileAccess.get_sha256(TEST_PATH)
	await _dialog_click(reader.skip_dialog.get_cancel_button())
	_check(panel.model.state() == partial and FileAccess.get_sha256(TEST_PATH) == disk,"cancel retains patrol memory and disk")
	while panel.model.state()["work_story"]["cursor"] < 31:
		await _key(KEY_RIGHT)
	_check(reader.next_button.text.contains("学校"),"last patrol page has correct school destination")
	await _key(KEY_ENTER)
	_check(panel.model.stage() == "fifth_planning" and panel.page == "groups","normal source END opens fifth-week school")
	_check(panel.calendar.text.contains("第5周") and not panel.next_button.disabled and panel.next_button.text.contains("出发准备"),"fifth calendar offers mandatory adventure preparation")
	_check(panel._guidance.text.contains("必修冒险") and panel.workroom_button.visible,"school explains native course lock and offers workroom return")
	_check(panel.model._school_state()["counts"] == fixture["cases"][1]["state"]["counts"],"MVP preserved without second award")
	await process_frame
	_bounds(panel)
	await _capture("fifth_school_initial")
	await _click(panel.student_buttons[0][0])
	await _click(panel.student_buttons[1][0])
	_check(panel._guidance.text.contains("教师"),"teacherless fifth class refuses student without writes")
	await _key(KEY_ESCAPE)
	await _click(panel.teacher_buttons[0])
	await _click(panel.teacher_buttons[4])
	_check(panel.selected_class == 4 and panel.waiting_buttons.size() == 3,"fifth teacher move returns current students to waiting")
	for pair in [[3,0],[4,1]]:
		await _click(panel.waiting_buttons[pair[0]])
		await _click(panel.student_buttons[4][pair[1]])
	_check(panel._identity("teacher",4,-1) == 101 and panel._identity("student",4,0) == 3,"actual fifth member assignment works")
	_check(panel.waiting_buttons.has(9) and panel.model.session.read_snapshot()["group_raw_bytes"][0] == 101,"fifth edits retain independent fourth review")
	_bounds(panel)
	await _capture("fifth_school_edited")
	await _click(panel.tab_buttons["courses"])
	var state: Dictionary = panel.model.state()
	for button in panel.course_buttons.values():
		_check(button.disabled,"mandatory adventure disables every course")
	await _click(panel.course_buttons[10])
	_check(panel.model.state() == state,"course click cannot bypass source mandatory adventure")
	await _capture("fifth_courses_locked")
	await _click(panel.tab_buttons["results"])
	_check(panel.mvp_label.text == "帕弥菈" and not panel.next_button.disabled,"fourth-week review still has source MVP and return")
	await _result_bounds(panel)
	await _capture("fourth_week_review")
	await _click(panel.next_button)
	_check(panel.page == "groups" and panel.model.state() == state,"review returns exact fifth class plan")
	await _click(panel.save_button)
	root.remove_child(panel);panel.queue_free()
	panel = await _new_panel()
	_check(panel.page == "groups" and panel.model.state() == state and panel._identity("teacher",4,-1) == 101,"fresh school launch restores edits and source lock")
	await _capture("restored_fifth_school")
	await _click(panel.workroom_button)
	_check(panel.workroom.visible and panel.workroom.continue_button.text.contains("返回第五周"),"workroom returns existing school rather than replaying CH002")
	await _click(panel.workroom.continue_button)
	_check(panel.page == "groups" and panel.model.state() == state,"return school is idempotent")
	disk = FileAccess.get_sha256(TEST_PATH)
	await _click(panel.restart_button)
	await _dialog_click(panel.restart_dialog.get_cancel_button())
	_check(panel.model.state() == state and FileAccess.get_sha256(TEST_PATH) == disk,"cancel restart preserves fifth plan and file")
	await _click(panel.battle_button)
	for index in range(8):
		await process_frame
	var battle = current_scene
	_check(battle.scene_file_path == "res://main.tscn","fifth plan can preview independent battle")
	battle.set_physics_process(false)
	await _capture("fifth_school_battle_preview")
	await _key(KEY_SPACE)
	_check(Engine.time_scale == 0.0,"battle pause still works")
	await _click(battle.playground_button)
	for index in range(8):
		await process_frame
	panel = current_scene
	_check(panel.page == "groups" and panel.model.state() == state and Engine.time_scale == 1.0,"battle return restores fifth plan and clears pause")
	await _capture("fifth_school_after_battle")
	panel.save_path = "user://missing_fifth_planning_directory/state.json"
	await _click(panel.battle_button)
	_check(current_scene == panel and panel.model.state() == state and panel._save_message.contains("失败"),"failed battle departure preserves current fifth plan")
	panel.save_path = TEST_PATH
	# Confirmed skip is a separate real UI path from normal source reading.
	file = FileAccess.open(TEST_PATH,FileAccess.WRITE)
	file.store_string(JSON.stringify(fixture["cases"][1]["save"]))
	file.close()
	await _click(panel.load_button)
	await _click(panel.arrival.continue_button)
	await _click(panel.workroom.continue_button)
	reader = panel.story_reader
	await _click(reader.skip_button)
	await _dialog_click(reader.skip_dialog.get_ok_button())
	_check(panel.model.stage() == "fifth_planning" and panel.model.state()["work_story"]["completed"],"confirmed patrol skip enters actual fifth school")
	_check(panel.model.fifth_session.read_snapshot()["adventure_gate"] == 1,"skip preserves compulsory adventure gate")
	await _capture("patrol_confirmed_skip_school")
	panel.queue_free()
	await process_frame
	if root.has_meta("school_playground_save_path"):
		root.remove_meta("school_playground_save_path")
	_cleanup()
	_finish()
