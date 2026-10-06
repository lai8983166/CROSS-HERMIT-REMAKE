extends CanvasLayer
## Point-and-click grouping over the independently owned source new-game school.

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
	column.add_child(heading)
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
	var header := HBoxContainer.new()
	header.add_theme_constant_override("separation",8)
	column.add_child(header)
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
		column.add_child(row)
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
	column.add_child(HSeparator.new())
	var waiting := HBoxContainer.new()
	waiting.add_theme_constant_override("separation",18)
	column.add_child(waiting)
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
	var spacer := Control.new()
	spacer.size_flags_vertical = Control.SIZE_EXPAND_FILL
	column.add_child(spacer)
	var note := Label.new()
	note.text = "本页用于新局编班试玩；课程安排和存档功能尚未开放。"
	note.add_theme_font_size_override("font_size",14)
	note.add_theme_color_override("font_color",Color("96aabc"))
	column.add_child(note)
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
	var started := fresh.initialize(parsed["origin_rules"],parsed["course_rules"],parsed)
	if not started["supported"]:
		_message = "学校初始化失败：" + str(started.get("reason",""))
		refresh()
		return
	var prepared := fresh.prepare_school(started["revision"])
	if not prepared["supported"]:
		_message = "学校准备失败：" + str(prepared.get("reason",""))
		refresh()
		return
	session = fresh
	_view = prepared
	_selected_id = -1
	_selected_kind = ""
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
	status_label.text = "4月 · 开学准备  |  学生%d / 教师%d" % [snapshot["student_count"],snapshot["teacher_count"]]
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
	_rebuild_waiting(_teacher_wait_box,waiting_teachers,snapshot["idle_teacher_ids"],"teacher",levels)
	_rebuild_waiting(_student_wait_box,waiting_students,snapshot["idle_student_ids"],"student",levels)


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
