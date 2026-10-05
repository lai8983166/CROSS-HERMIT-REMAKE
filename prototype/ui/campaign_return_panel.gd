extends CanvasLayer
## Read-only view; session methods alone publish campaign state.

signal start_requested(route: int)
signal default_requested

const Demo = preload("res://sim/campaign_return_demo.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const ATTRIBUTES := ["力量", "敏捷", "感觉", "活力", "智力", "耐力", "精神"]

var session: Demo
var route_select: OptionButton
var start_button: Button
var default_button: Button
var confirm_button: Button
var school_button: Button
var back_button: Button
var roster: ItemList
var detail: RichTextLabel
var result_text: RichTextLabel
var status_label: Label
var notice: Label
var body: PanelContainer
var school_content: HBoxContainer
var _heading: Label
var _page := "result"
var _student_ids: Array = []
var _selected_id := -1


func _ready() -> void:
	layer = 10
	var root := Control.new()
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var theme := Theme.new()
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Microsoft YaHei", "Noto Sans CJK SC", "sans-serif"])
	theme.default_font = font
	theme.default_font_size = 17
	root.theme = theme
	add_child(root)
	var toolbar := PanelContainer.new()
	toolbar.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	toolbar.offset_left = 16
	toolbar.offset_right = -16
	toolbar.offset_top = 34
	toolbar.offset_bottom = 94
	toolbar.add_theme_stylebox_override("panel", _style())
	root.add_child(toolbar)
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 12)
	toolbar.add_child(row)
	route_select = OptionButton.new()
	route_select.add_item("场景5 · 源路线A")
	route_select.add_item("场景5 · 源路线B")
	row.add_child(route_select)
	start_button = _button("开始返回流程演示", func(): start_requested.emit(route_select.selected))
	row.add_child(start_button)
	default_button = _button("回到战斗原型", func(): default_requested.emit())
	row.add_child(default_button)
	status_label = Label.new()
	status_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	status_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	row.add_child(status_label)
	notice = Label.new()
	var notice_box := PanelContainer.new()
	notice_box.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	notice_box.offset_left = 24
	notice_box.offset_right = -24
	notice_box.offset_top = 96
	notice_box.offset_bottom = 120
	var notice_style := _style()
	notice_style.set_border_width_all(0)
	notice_style.content_margin_top = 0
	notice_style.content_margin_bottom = 0
	notice_box.add_theme_stylebox_override("panel", notice_style)
	root.add_child(notice_box)
	notice.add_theme_font_size_override("font_size", 14)
	notice.add_theme_color_override("font_color", Color("f0d797"))
	notice.mouse_filter = Control.MOUSE_FILTER_IGNORE
	notice_box.add_child(notice)
	body = PanelContainer.new()
	body.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	body.offset_left = 24
	body.offset_right = -24
	body.offset_top = 128
	body.offset_bottom = -24
	body.add_theme_stylebox_override("panel", _style())
	root.add_child(body)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation", 12)
	body.add_child(column)
	_heading = Label.new()
	_heading.add_theme_font_size_override("font_size", 25)
	_heading.add_theme_color_override("font_color", Color("f0d797"))
	column.add_child(_heading)
	result_text = _rich()
	column.add_child(result_text)
	school_content = HBoxContainer.new()
	school_content.size_flags_vertical = Control.SIZE_EXPAND_FILL
	school_content.add_theme_constant_override("separation", 20)
	column.add_child(school_content)
	roster = ItemList.new()
	roster.custom_minimum_size.x = 230
	roster.size_flags_vertical = Control.SIZE_EXPAND_FILL
	roster.item_selected.connect(_select_student)
	school_content.add_child(roster)
	detail = _rich()
	school_content.add_child(detail)
	var footer := HBoxContainer.new()
	footer.add_theme_constant_override("separation", 12)
	column.add_child(footer)
	confirm_button = _button("确认战果", _confirm)
	footer.add_child(confirm_button)
	school_button = _button("进入学校", show_school)
	footer.add_child(school_button)
	back_button = _button("返回战果", show_result)
	footer.add_child(back_button)
	var unfinished := Label.new()
	unfinished.text = "编班 / 排课：尚未开放"
	unfinished.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	unfinished.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	footer.add_child(unfinished)
	refresh()


func bind_session(value: Demo) -> void:
	session = value
	_page = "result"
	_selected_id = -1
	refresh()


func blocks_battle_input() -> bool:
	return body != null and body.visible


func refresh() -> void:
	if body == null:
		return
	var view := session.view() if session != null else {"stage": "idle"}
	var stage: String = view["stage"]
	body.visible = stage in ["result", "settled", "school", "error"]
	default_button.disabled = stage == "idle"
	start_button.text = "开始返回流程演示" if stage == "idle" else "重开返回流程演示"
	notice.text = "选择源路线，开始本地战斗 → 查看战果 → 确认 → 学校名单。" if stage == "idle" else Demo.NOTICE
	status_label.text = {"idle": "战斗原型", "battle": "演示 · 战斗中", "result": "待确认战果",
		"settled": "可进入学校", "school": "学校数据浏览", "error": "演示未完成"}[stage]
	confirm_button.disabled = stage != "result"
	school_button.disabled = stage not in ["settled", "school"]
	back_button.visible = stage == "school" and _page == "school"
	confirm_button.visible = _page == "result"
	school_button.visible = _page == "result"
	school_content.visible = stage == "school" and _page == "school"
	result_text.visible = not school_content.visible
	if not body.visible:
		return
	if stage == "error":
		_heading.text = "无法继续返回流程"
		result_text.text = "来源文件或战斗角色未通过检查。\n请重开演示，或回到战斗原型。\n\n学校与战果后续操作已停止。"
		return
	var snapshot: Dictionary = view["snapshot"]
	var date := "%d月 · 第%d周" % [snapshot["month"], snapshot["week"]]
	_heading.text = "%s    %s    总点数 %d" % ["学校" if school_content.visible else "战果",
		date, snapshot["global_total_511c"]]
	if school_content.visible:
		_render_roster(snapshot)
	else:
		_render_result(view)


func _confirm() -> void:
	if session != null:
		session.confirm_result()
	refresh()


func show_school() -> void:
	if session != null and session.enter_school():
		_page = "school"
	refresh()


func show_result() -> void:
	_page = "result"
	refresh()


func _render_result(view: Dictionary) -> void:
	var terminal: Dictionary = view["terminal"]
	var winner := "平局" if int(terminal["winner"]) < 0 else ("红方胜利" if int(terminal["winner"]) == 0 else "蓝方胜利")
	var lines := ["[b]本地战斗[/b]  %s · 逻辑帧 %d" % [winner, terminal["frame"]],
		"[b]战果来源[/b]  场景5源路线%s" % ("A" if view["route"] == 0 else "B"), "",
		"[b]本次总点数[/b]  +%d" % view["summary"]["total_delta"]]
	var items := []
	for group in view["loot"]:
		for item in group:
			if int(item) > 0:
				items.append("道具 #%d" % item)
	lines.append("[b]战利品[/b]  " + ("、".join(items) if not items.is_empty() else "无"))
	lines.append("\n[b]学生成长[/b]  七属性顺序：力量 / 敏捷 / 感觉 / 活力 / 智力 / 耐力 / 精神")
	var before := Roles._records(view["before"])
	var after := Roles._records(view["snapshot"])
	for id in Demo.IDS:
		var record: Dictionary = after[id]
		lines.append("\n[color=#f0d797]学生 #%d[/color]  等级 %d → %d   成长包 %d" %
			[id, before[id]["level_50"], record["level_50"], record["staged_total"]])
		lines.append("属性  %s → %s" % [str(before[id]["attributes"]), str(record["attributes"])])
	lines.append("\n" + ("战果已确认。可进入学校；返回浏览不会再次结算。" if view["stage"] in ["settled", "school"] else
		"成长已按源流程初始化；确认后完成战果记录，再进入学校。"))
	result_text.text = "\n".join(lines)


func _render_roster(snapshot: Dictionary) -> void:
	_student_ids = snapshot["school"]["student_ids"].slice(0, int(snapshot["school"]["student_count"]))
	roster.clear()
	for id in _student_ids:
		roster.add_item("学生 #%d" % id)
	var index := _student_ids.find(_selected_id)
	if index < 0:
		index = 0
	roster.select(index)
	_select_student(index)


func _select_student(index: int) -> void:
	if index < 0 or index >= _student_ids.size() or session == null:
		return
	_selected_id = int(_student_ids[index])
	var snapshot: Dictionary = session.view()["snapshot"]
	var record: Dictionary = Roles._records(snapshot)[_selected_id]
	var school: Dictionary = snapshot["school"]
	var lines := ["[color=#f0d797][b]学生 #%d[/b][/color]    职业 #%d · 等级 %d" %
		[_selected_id, record["job"], record["level_50"]], "", "[b]属性与成长池[/b]"]
	for i in range(7):
		lines.append("%s    %d    ·    成长池 %d" % [ATTRIBUTES[i], record["attributes"][i], record["growth_pools"][i]])
	lines.append("\n[b]待命顺序[/b]  " + str(school["school_control"]["idle_student_ids"]))
	lines.append("[b]教师人数[/b]  %d" % school["teacher_count"])
	lines.append("\n[b]当前班级[/b]")
	for i in range(5):
		var members: Array = school["group_student_ids"][i].filter(func(id): return int(id) >= 0)
		lines.append("%d班  %s" % [i + 1, "未编班" if members.is_empty() else str(members)])
	lines.append("\n学校名单与详情可浏览；教师课程、编班和排课尚未开放。")
	detail.text = "\n".join(lines)


static func _rich() -> RichTextLabel:
	var node := RichTextLabel.new()
	node.bbcode_enabled = true
	node.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	node.size_flags_vertical = Control.SIZE_EXPAND_FILL
	node.selection_enabled = true
	return node


static func _button(text: String, action: Callable) -> Button:
	var button := Button.new()
	button.text = text
	button.custom_minimum_size.y = 36
	button.pressed.connect(action)
	return button


static func _style() -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = Color("17241e")
	style.border_color = Color("69795a")
	style.set_border_width_all(1)
	style.set_corner_radius_all(8)
	style.content_margin_left = 16
	style.content_margin_right = 16
	style.content_margin_top = 12
	style.content_margin_bottom = 12
	return style
