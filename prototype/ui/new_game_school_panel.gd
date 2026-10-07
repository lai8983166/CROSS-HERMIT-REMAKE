extends CanvasLayer
## Grouping and course planning over independent source and declared-date schools.

signal closed

const Session = preload("res://sim/new_game_school_session.gd")
const Group = preload("res://sim/school_teacher_group_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const WIDTHS := [62,136,133,133,133,133,124]

var session: Session
var close_button: Button
var restart_button: Button
var cancel_button: Button
var wait_student_target: Button
var wait_teacher_target: Button
var teacher_buttons: Array = []
var student_buttons: Array = []
var waiting_students: Dictionary = {}
var waiting_teachers: Dictionary = {}
var status_label: Label
var instruction: Label
var _teacher_wait_box: HBoxContainer
var _student_wait_box: HBoxContainer
var _ratings: Array = []
var _selected_id := -1
var _selected_kind := ""
var _message := ""
var _view: Dictionary = {}
var group_button: Button
var course_button: Button
var source_button: Button
var example_button: Button
var course_group: OptionButton
var class_mode: OptionButton
var course_lists: Array = []
var assign_button: Button
var settle_button: Button
var growth_summary: Label
var confirm_button: Button
var confirmation_summary: Label
var course_info: Label
var _group_content: VBoxContainer
var _course_content: VBoxContainer
var _note: Label
var _source_session: Session
var _example_session: Session
var _example_mode := false
var _page := "groups"
var _course_selected := -1


func _ready() -> void:
	layer = 20
	var root := PanelContainer.new()
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.offset_left = 16
	root.offset_top = 16
	root.offset_right = -16
	root.offset_bottom = -16
	var theme := Theme.new()
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Microsoft YaHei","Noto Sans CJK SC","sans-serif"])
	theme.default_font = font
	theme.default_font_size = 17
	root.theme = theme
	var style := StyleBoxFlat.new()
	style.bg_color = Color("142130")
	style.border_color = Color("82744e")
	style.set_border_width_all(1)
	style.set_corner_radius_all(8)
	style.content_margin_left = 18
	style.content_margin_right = 18
	style.content_margin_top = 16
	style.content_margin_bottom = 16
	root.add_theme_stylebox_override("panel",style)
	add_child(root)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation",10)
	root.add_child(column)
	var heading := Label.new()
	heading.text = "学校 · 新局编班"
	heading.add_theme_font_size_override("font_size",27)
	heading.add_theme_color_override("font_color",Color("f0d797"))
	var navigation := HBoxContainer.new()
	column.add_child(navigation)
	heading.text = "学校"
	heading.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	navigation.add_child(heading)
	group_button = _button("编班",func(): _show_page("groups"))
	course_button = _button("课程安排",func(): _show_page("courses"))
	source_button = _button("第0周新局",func(): _switch_school(false))
	example_button = _button("第4周课程示例",func(): _switch_school(true))
	for button in [group_button,course_button,source_button,example_button]:
		navigation.add_child(button)
	var actions := HBoxContainer.new()
	actions.add_theme_constant_override("separation",12)
	column.add_child(actions)
	close_button = _button("返回战斗",func(): hide(); closed.emit())
	restart_button = _button("重开学校新局",_restart)
	cancel_button = _button("取消选择 · Esc",_cancel)
	for button in [close_button,restart_button,cancel_button]:
		actions.add_child(button)
	status_label = Label.new()
	status_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	actions.add_child(status_label)
	instruction = Label.new()
	instruction.custom_minimum_size.y = 48
	instruction.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	instruction.add_theme_color_override("font_color",Color("bed0de"))
	column.add_child(instruction)
	column.add_child(HSeparator.new())
	_group_content = VBoxContainer.new()
	_group_content.add_theme_constant_override("separation",10)
	column.add_child(_group_content)
	var header := HBoxContainer.new()
	header.add_theme_constant_override("separation",8)
	_group_content.add_child(header)
	var names := ["班级","教师","学生1","学生2","学生3","学生4","班级情况"]
	for index in range(7):
		var label := Label.new()
		label.text = names[index]
		label.custom_minimum_size.x = WIDTHS[index]
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		header.add_child(label)
	for group in range(5):
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation",8)
		_group_content.add_child(row)
		var name_label := Label.new()
		name_label.text = "%d班" % (group + 1)
		name_label.custom_minimum_size.x = WIDTHS[0]
		name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		row.add_child(name_label)
		var teacher := _button("",func(): _cell("teacher",group,-1))
		teacher.toggle_mode = true
		teacher.custom_minimum_size = Vector2(WIDTHS[1],62)
		row.add_child(teacher)
		teacher_buttons.append(teacher)
		var students := []
		for slot in range(4):
			var student := _button("",func(): _cell("student",group,slot))
			student.toggle_mode = true
			student.custom_minimum_size = Vector2(WIDTHS[2+slot],62)
			row.add_child(student)
			students.append(student)
		student_buttons.append(students)
		var rating := Label.new()
		rating.custom_minimum_size.x = WIDTHS[6]
		rating.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		rating.add_theme_font_size_override("font_size",15)
		row.add_child(rating)
		_ratings.append(rating)
	_group_content.add_child(HSeparator.new())
	var waiting := HBoxContainer.new()
	waiting.add_theme_constant_override("separation",18)
	_group_content.add_child(waiting)
	var teacher_column := VBoxContainer.new()
	teacher_column.custom_minimum_size.x = 220
	waiting.add_child(teacher_column)
	wait_teacher_target = _button("移至教师待命",func(): _move(-1,-1))
	teacher_column.add_child(wait_teacher_target)
	_teacher_wait_box = HBoxContainer.new()
	teacher_column.add_child(_teacher_wait_box)
	var student_column := VBoxContainer.new()
	student_column.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	waiting.add_child(student_column)
	wait_student_target = _button("移至学生待命",func(): _move(-1,-1))
	student_column.add_child(wait_student_target)
	_student_wait_box = HBoxContainer.new()
	student_column.add_child(_student_wait_box)
	_build_courses(column)
	var spacer := Control.new()
	spacer.size_flags_vertical = Control.SIZE_EXPAND_FILL
	column.add_child(spacer)
	_note = Label.new()
	_note.add_theme_font_size_override("font_size",14)
	_note.add_theme_color_override("font_color",Color("96aabc"))
	column.add_child(_note)
	hide()


func open_school() -> void:
	if session == null:
		_restart()
	show()
	refresh()


func blocks_battle_input() -> bool:
	return visible


func _restart() -> void:
	var parsed: Variant = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/new_game_school_rules.json")))
	var fresh := Session.new()
	var started := fresh.initialize_course_example(parsed["origin_rules"],parsed["course_rules"],parsed) if _example_mode else fresh.initialize(parsed["origin_rules"],parsed["course_rules"],parsed)
	if not started["supported"]:
		_message = "学校初始化失败：" + str(started.get("reason",""))
		refresh()
		return
	var prepared: Dictionary = fresh.view() if _example_mode else fresh.prepare_school(started["revision"])
	if not prepared["supported"]:
		_message = "学校准备失败：" + str(prepared.get("reason",""))
		refresh()
		return
	session = fresh
	if _example_mode:
		_example_session = fresh
	else:
		_source_session = fresh
	_view = prepared
	_selected_id = -1
	_selected_kind = ""
	_course_selected = -1
	_message = ""
	refresh()


func _cancel() -> void:
	_selected_id = -1
	_selected_kind = ""
	_message = ""
	refresh()


func _unhandled_key_input(event: InputEvent) -> void:
	if visible and event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_ESCAPE:
		_cancel()
		get_viewport().set_input_as_handled()


func _cell(kind: String, group: int, slot: int) -> void:
	if session == null:
		return
	var snapshot := session.read_snapshot()
	var identity := Group._word(snapshot["group_raw_bytes"],group * 28 + (0 if kind == "teacher" else 16 + slot * 2))
	if _selected_id >= 0 and _selected_kind == kind:
		if kind == "student" and Group._word(snapshot["group_raw_bytes"],group * 28) == -1:
			_message = "请先为这个班安排教师，再安排学生。"
			refresh()
			return
		_move(group,slot)
	elif identity != -1:
		_select(kind,identity)
	else:
		_message = "先点选待命区或其他班的" + ("教师。" if kind == "teacher" else "学生。")
		refresh()


func _select(kind: String, identity: int) -> void:
	_selected_kind = kind
	_selected_id = identity
	_message = ""
	refresh()


func _move(group: int, slot: int) -> void:
	if session == null or _selected_id < 0:
		return
	var result := session.move_member({"kind":_selected_kind,"member_id":_selected_id,
		"target_group":group,"target_slot":slot},session.revision())
	if not result["supported"]:
		_message = "未能移动：" + str(result.get("reason",""))
	else:
		_view = result
		_message = "编班已更新。" if result["status"] == "member_moved" else "成员位置未变化。"
		_selected_id = -1
		_selected_kind = ""
	refresh()


func refresh() -> void:
	if instruction == null:
		return
	instruction.text = "点击成员，再点击同类的班级位置或待命按钮。教师移到空班时，原班学生会退回待命。"
	if _selected_id >= 0:
		instruction.text = "已选%s #%d：点击目标位置或待命按钮。Esc取消选择。" % ["教师" if _selected_kind == "teacher" else "学生",_selected_id]
	if not _message.is_empty():
		instruction.text += "\n" + _message
	cancel_button.disabled = _selected_id < 0
	wait_student_target.disabled = _selected_kind != "student"
	wait_teacher_target.disabled = _selected_kind != "teacher"
	if session == null:
		return
	var snapshot := session.read_snapshot()
	_group_content.visible = _page == "groups"
	_course_content.visible = _page == "courses"
	status_label.text = ("4月 · 第4周课程示例" if _example_mode else "4月 · 开学准备") + "  |  学生%d / 教师%d" % [snapshot["student_count"],snapshot["teacher_count"]]
	_note.text = "第4周日期为独立示例输入；结算后可确认关系与职业，尚不推进日历或存档。" if _example_mode else "第0周来源新局；编班和课程模式可操作，教师101最早在4月第4周开放课程。"
	restart_button.text = "重开课程示例" if _example_mode else "重开学校新局"
	var levels := {}
	for row in snapshot["member_profiles"]:
		levels[row["member_id"]] = row["level_50"]
	for group in range(5):
		var teacher := Group._word(snapshot["group_raw_bytes"],group * 28)
		teacher_buttons[group].text = "教师 #%d" % teacher if teacher != -1 else "无教师"
		teacher_buttons[group].button_pressed = teacher != -1 and teacher == _selected_id
		for slot in range(4):
			var identity := Group._word(snapshot["group_raw_bytes"],group * 28 + 16 + slot * 2)
			student_buttons[group][slot].text = "学生 #%d\nLv.%d" % [identity,levels[identity]] if identity != -1 else "空位"
			student_buttons[group][slot].button_pressed = identity != -1 and identity == _selected_id
		var rating: Dictionary = _view["ratings"][group]
		_ratings[group].text = "未编班" if teacher == -1 else "%d名学生\n关系%d · %d级" % [snapshot["group_raw_bytes"][group * 28 + 14],rating["relationship_mean"],rating["relationship_rank"]]
		if teacher != -1 and snapshot["group_raw_bytes"][group * 28 + 3] == 1:
			_ratings[group].text = "关系%d · %d级\n" % [rating["relationship_mean"],rating["relationship_rank"]]
			_ratings[group].text += "授课 · 课程 #%d" % Group._word(snapshot["group_raw_bytes"],group * 28 + 10) if Group._word(snapshot["group_raw_bytes"],group * 28 + 8) >= 0 else "授课 · 未安排课程"
	_rebuild_waiting(_teacher_wait_box,waiting_teachers,snapshot["idle_teacher_ids"],"teacher",levels)
	_rebuild_waiting(_student_wait_box,waiting_students,snapshot["idle_student_ids"],"student",levels)
	_refresh_courses(snapshot)
	if _page == "courses":
		instruction.text = "选择班级，切换为授课，再从教师可用课程中选课并安排。" + ("\n" + _message if not _message.is_empty() else "")
		cancel_button.disabled = true


func _build_courses(column: VBoxContainer) -> void:
	_course_content = VBoxContainer.new()
	_course_content.add_theme_constant_override("separation",12)
	column.add_child(_course_content)
	var controls := HBoxContainer.new()
	_course_content.add_child(controls)
	course_group = OptionButton.new()
	course_group.custom_minimum_size.x = 180
	for group in range(5):
		course_group.add_item("%d班" % (group + 1))
	course_group.item_selected.connect(func(_index): _course_selected = -1; _message = ""; refresh())
	controls.add_child(course_group)
	class_mode = OptionButton.new()
	class_mode.custom_minimum_size.x = 200
	class_mode.add_item("冒险")
	class_mode.add_item("授课")
	class_mode.item_selected.connect(func(index): _plan_mode(index == 1))
	controls.add_child(class_mode)
	course_info = Label.new()
	course_info.custom_minimum_size.y = 48
	course_info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_course_content.add_child(course_info)
	var categories := HBoxContainer.new()
	categories.add_theme_constant_override("separation",18)
	_course_content.add_child(categories)
	for category in range(3):
		var box := VBoxContainer.new()
		box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		categories.add_child(box)
		var caption := Label.new()
		caption.text = ["初级课程","中级课程","高级课程"][category]
		box.add_child(caption)
		var list := ItemList.new()
		list.custom_minimum_size = Vector2(250,140)
		list.item_selected.connect(func(index): _choose_course(category,index))
		box.add_child(list)
		course_lists.append(list)
	assign_button = _button("安排选中课程",_assign_course)
	var actions := HBoxContainer.new()
	_course_content.add_child(actions)
	assign_button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	actions.add_child(assign_button)
	settle_button = _button("结算授课示例",_settle_courses)
	settle_button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	actions.add_child(settle_button)
	confirm_button = _button("确认关系与职业",_confirm_courses)
	confirm_button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	actions.add_child(confirm_button)
	growth_summary = Label.new()
	growth_summary.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	growth_summary.add_theme_font_size_override("font_size",16)
	growth_summary.add_theme_color_override("font_color",Color("d6e4c4"))
	_course_content.add_child(growth_summary)
	confirmation_summary = Label.new()
	confirmation_summary.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	confirmation_summary.add_theme_font_size_override("font_size",16)
	confirmation_summary.add_theme_color_override("font_color",Color("b9d5ef"))
	_course_content.add_child(confirmation_summary)


func _show_page(page: String) -> void:
	_page = page
	_cancel()


func _switch_school(example: bool) -> void:
	_example_mode = example
	_page = "courses" if example else "groups"
	session = _example_session if example else _source_session
	_course_selected = -1
	if session == null:
		_restart()
	else:
		_view = session.view()
		_cancel()


func _plan_mode(teaching: bool) -> void:
	var result := session.set_class_mode(course_group.selected,teaching,session.revision())
	_plan_result(result)


func _assign_course() -> void:
	var result := session.assign_course(course_group.selected,_course_selected,session.revision())
	_plan_result(result)


func _settle_courses() -> void:
	var rules: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_settlement_rules.json")))
	var result := session.settle_courses(rules,session.revision())
	if result["supported"]:
		_view = result
		_message = "授课示例已结算；学生成长已更新，日期保持第4周。"
	else:
		_message = "未能结算：" + str(result.get("reason",""))
	refresh()


func _confirm_courses() -> void:
	var rules: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_course_confirmation_rules.json")))
	var result := session.confirm_courses(rules,session.revision())
	if result["supported"]:
		_view = result
		_message = "关系、职业进度和本周记录已确认；第4周日期不变。"
	else:
		_message = "未能确认：" + str(result.get("reason",""))
	refresh()


func _plan_result(result: Dictionary) -> void:
	if result["supported"]:
		_view = result
		_message = "课程安排已更新。" if result["status"] != "duplicate" else "安排未变化。"
	else:
		_message = "未能安排：" + str(result.get("reason",""))
	refresh()


func _choose_course(category: int, index: int) -> void:
	_course_selected = course_lists[category].get_item_metadata(index)
	refresh()


func _refresh_courses(snapshot: Dictionary) -> void:
	var group := course_group.selected
	var teacher := Group._word(snapshot["group_raw_bytes"],group * 28)
	var teaching: bool = snapshot["group_raw_bytes"][group * 28 + 3] == 1
	class_mode.select(1 if teaching else 0)
	class_mode.disabled = teacher == -1
	var result := session.list_courses(group)
	var available := false
	var selected_available := false
	for category in range(3):
		var list: ItemList = course_lists[category]
		list.clear()
		if result["supported"]:
			for row in result["courses"][category]:
				var index := list.add_item("课程 #%d" % row[1])
				list.set_item_metadata(index,row[1])
				available = true
				if row[1] == _course_selected:
					list.select(index)
					selected_available = true
	assign_button.disabled = teacher == -1 or not teaching or not selected_available
	course_info.text = "请先在编班页面为这个班安排教师。" if teacher == -1 else "教师 #%d · %s" % [teacher,"授课模式" if teaching else "冒险模式"]
	if teacher != -1 and not available:
		course_info.text += "\n当前没有可用课程；教师101最早在4月第4周开放，可进入独立课程示例。"
	elif teacher != -1:
		course_info.text += "\n当前课程：#%d" % Group._word(snapshot["group_raw_bytes"],group * 28 + 10) if Group._word(snapshot["group_raw_bytes"],group * 28 + 8) >= 0 else "\n当前未安排课程。"
	_refresh_settlement()
	_refresh_confirmation()


func _refresh_confirmation() -> void:
	confirm_button.visible = _example_mode
	var completed := session.read_confirmation()
	confirm_button.disabled = not _example_mode or session.read_settlement().is_empty() or not completed.is_empty()
	confirm_button.text = "本次结果已确认" if not completed.is_empty() else "确认关系与职业"
	confirmation_summary.visible = _example_mode and not completed.is_empty()
	if completed.is_empty():
		confirmation_summary.text = ""
		return
	var differences := {}
	for index in range(completed["after"]["relationships"].size()):
		var delta: int = completed["after"]["relationships"][index]["value"] - completed["settled_school"]["relationships"][index]["value"]
		if delta != 0:
			differences[delta] = differences.get(delta,0)+1
	var relation_parts := PackedStringArray()
	for delta in differences:
		relation_parts.append("%s%d×%d条" % ["+" if delta > 0 else "",delta,differences[delta]])
	var lines := PackedStringArray(["确认完成 · 关系变化 %s · 第4周日期不变" % " / ".join(relation_parts)])
	for index in range(3):
		var record: Dictionary = completed["records"][index]
		var job := 0
		for profile in completed["settled_school"]["member_profiles"]:
			if profile["member_id"] == record["character_id"]:
				job = profile["job"]
		var activity := "待命"
		if record["week_records"][9] == 1:
			for group in range(5):
				for slot in range(4):
					if Group._word(completed["settled_school"]["group_raw_bytes"],group*28+16+2*slot) == record["character_id"]:
						activity = "授课 #%d" % Group._word(completed["settled_school"]["group_raw_bytes"],group*28+10)
		lines.append("学生 #%d · 职业 #%d 进度%d→%d · 本周%s" % [record["character_id"],job,
			completed["before_records"][index]["job_progress"][job],record["job_progress"][job],activity])
	confirmation_summary.text = "\n".join(lines)


func _refresh_settlement() -> void:
	settle_button.visible = _example_mode
	var completed := session.read_settlement()
	var ready := false
	var supported := true
	for rating in _view.get("ratings",[]):
		if rating["state"] in [2,3,5]:
			supported = false
		if rating["state"] == 4:
			ready = true
			if rating["work_fields"][2] not in [10,11,12]:
				supported = false
	settle_button.disabled = not _example_mode or not ready or not supported or not completed.is_empty()
	settle_button.text = "本次示例已结算" if not completed.is_empty() else "结算授课示例"
	growth_summary.visible = _example_mode and not completed.is_empty()
	if completed.is_empty():
		growth_summary.text = ""
		return
	var lines := PackedStringArray(["授课结果 · 成长加成 +%d · 第4周日期不变；重开示例可再次演示。" % completed["bonus"]])
	var ids := []
	for packet in completed["packets"]:
		ids.append(packet["character_id"])
	for index in range(3):
		var old: Dictionary = completed["before_records"][index]
		var record: Dictionary = completed["records"][index]
		if record["character_id"] not in ids:
			continue
		var changes := PackedStringArray()
		for k in range(7):
			if old["attributes"][k] != record["attributes"][k]:
				changes.append("%s%d→%d" % [["力","敏","感","活","智","耐","精"][k],old["attributes"][k],record["attributes"][k]])
		for sid in range(84):
			if old["skill_statuses"][sid] != 2 and record["skill_statuses"][sid] == 2:
				changes.append("新技能 #%d" % (sid+1))
		lines.append("学生 #%d · Lv.%d→%d · %s" % [record["character_id"],old["level_50"],record["level_50"]," / ".join(changes)])
	growth_summary.text = "\n".join(lines)


func _rebuild_waiting(box: HBoxContainer, buttons: Dictionary, identities: Array, kind: String, levels: Dictionary) -> void:
	for child in box.get_children():
		box.remove_child(child)
		child.queue_free()
	buttons.clear()
	for identity in identities:
		var caption := "教师 #%d" % identity if kind == "teacher" else "学生 #%d\nLv.%d" % [identity,levels[identity]]
		var button := _button(caption,func(): _select(kind,identity))
		button.toggle_mode = true
		button.button_pressed = identity == _selected_id
		button.custom_minimum_size = Vector2(133,62)
		box.add_child(button)
		buttons[identity] = button
	if identities.is_empty():
		var label := Label.new()
		label.text = "无人待命"
		label.custom_minimum_size.y = 62
		label.add_theme_color_override("font_color",Color("96aabc"))
		box.add_child(label)


static func _button(text: String, action: Callable) -> Button:
	var button := Button.new()
	button.text = text
	button.pressed.connect(action)
	return button
