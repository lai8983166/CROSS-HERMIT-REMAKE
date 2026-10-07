extends Control
## Player-facing school slice; all state changes belong to the verified controller.

const Playground := preload("res://sim/school_playground.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")
const StoryReader := preload("res://ui/school_story_reader.gd")
const ART := "res://assets/school/"

var model := Playground.new()
var auto_load := true
var autosave := true
var save_path := Playground.SAVE_PATH
var catalog: Dictionary = {}
var _textures: Dictionary = {}
var selected_id := -1
var selected_kind := ""
var detail_id := 3
var selected_class := 0
var page := "groups"
var _message := ""
var _save_message := "尚未保存"
var teacher_buttons: Array = []
var student_buttons: Array = []
var class_buttons: Array = []
var class_labels: Array = []
var waiting_buttons: Dictionary = {}
var course_buttons: Dictionary = {}
var tab_buttons: Dictionary = {}
var wait_target: Button
var cancel_button: Button
var next_button: Button
var save_button: Button
var load_button: Button
var restart_button: Button
var battle_button: Button
var restart_dialog: ConfirmationDialog
var result_cards: Dictionary = {}
var mvp_label: Label
var _groups: VBoxContainer
var _courses: VBoxContainer
var _results: VBoxContainer
var _waiting: HBoxContainer
var _detail: VBoxContainer
var _status: Label
var _class_caption: Label
var _guidance: Label
var _stage_labels: Array = []
var footer: Label
var panel: MarginContainer
var story_reader: StoryReader


func _ready() -> void:
	Engine.time_scale = 1.0
	if get_tree().root.has_meta("school_playground_save_path"):
		save_path = get_tree().root.get_meta("school_playground_save_path")
	catalog = JSON.parse_string(FileAccess.get_file_as_string(ART+"catalog.json"))
	var theme := Theme.new()
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Microsoft YaHei","Noto Sans CJK SC","sans-serif"])
	theme.default_font = font
	theme.default_font_size = 16
	for state in ["normal","hover","pressed","disabled","focus"]:
		var color := "253d3d" if state == "normal" else "375953"
		if state == "disabled":
			color = "1d2c2d"
		var style := _style(color,6)
		style.content_margin_left = 8
		style.content_margin_right = 8
		theme.set_stylebox(state,"Button",style)
	theme.set_color("font_color","Button",Color("f0e7d0"))
	theme.set_color("font_disabled_color","Button",Color("738783"))
	theme.set_stylebox("panel","PanelContainer",_style("132b2b",12))
	self.theme = theme
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var background := TextureRect.new()
	background.texture = _texture("background.png")
	background.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	background.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)
	var shade := ColorRect.new()
	shade.color = Color(0.035,0.085,0.075,0.86)
	shade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	shade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(shade)
	panel = MarginContainer.new()
	panel.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	for side in ["left","right","top","bottom"]:
		panel.add_theme_constant_override("margin_"+side,20)
	add_child(panel)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation",10)
	panel.add_child(column)
	var heading := HBoxContainer.new()
	column.add_child(heading)
	var title_box := VBoxContainer.new()
	title_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	heading.add_child(title_box)
	title_box.add_child(_label("纯洁之盾 · 学校",30,Color("ead6a3")))
	title_box.add_child(_label("安排课程，让每一位学生有所成长。",15,Color("bacac0")))
	var calendar := _label("APRIL\n4月 · 第4周",20,Color("ead6a3"))
	calendar.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	heading.add_child(calendar)
	var toolbar := HBoxContainer.new()
	column.add_child(toolbar)
	for item in [["groups","编班"],["courses","授课安排"],["results","成长结果"]]:
		var key: String = item[0]
		var button := _button(item[1],func(): page = key; _message = ""; refresh())
		button.toggle_mode = true
		button.custom_minimum_size = Vector2(115,38)
		toolbar.add_child(button)
		tab_buttons[key] = button
	save_button = _button("保存",_manual_save)
	load_button = _button("读取",_load)
	restart_button = _button("重开",func(): restart_dialog.popup_centered(Vector2i(440,180)))
	for button in [save_button,load_button,restart_button]:
		button.custom_minimum_size = Vector2(64,38)
		toolbar.add_child(button)
	battle_button = _button("战斗预览",_open_battle)
	battle_button.custom_minimum_size = Vector2(96,38)
	toolbar.add_child(battle_button)
	restart_dialog = ConfirmationDialog.new()
	restart_dialog.title = "重新开始本段试玩"
	restart_dialog.dialog_text = "将清空本段的编班、课程和成长结果，\n并替换当前保存的试玩进度。"
	restart_dialog.ok_button_text = "确认重开"
	restart_dialog.cancel_button_text = "保留当前进度"
	restart_dialog.confirmed.connect(_restart_confirmed)
	add_child(restart_dialog)
	_status = _label("",14,Color("becfc3"))
	_status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_status.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	toolbar.add_child(_status)
	var steps := HBoxContainer.new()
	steps.add_theme_constant_override("separation",8)
	column.add_child(steps)
	for caption in ["01  编班 / 选课","02  授课成长","03  确认记录","04  本次MVP"]:
		var step := _label(caption,16)
		step.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		step.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		steps.add_child(step)
		_stage_labels.append(step)
	var body := HBoxContainer.new()
	body.size_flags_vertical = Control.SIZE_EXPAND_FILL
	body.add_theme_constant_override("separation",14)
	column.add_child(body)
	var left := PanelContainer.new()
	left.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	body.add_child(left)
	var contents := VBoxContainer.new()
	left.add_child(contents)
	_build_groups(contents)
	_courses = VBoxContainer.new()
	_courses.add_theme_constant_override("separation",12)
	contents.add_child(_courses)
	_results = VBoxContainer.new()
	_results.add_theme_constant_override("separation",12)
	contents.add_child(_results)
	var right := PanelContainer.new()
	right.custom_minimum_size.x = 300
	body.add_child(right)
	_detail = VBoxContainer.new()
	_detail.add_theme_constant_override("separation",8)
	right.add_child(_detail)
	var bottom := HBoxContainer.new()
	bottom.add_theme_constant_override("separation",10)
	column.add_child(bottom)
	_guidance = _label("",16,Color("e2d3b2"))
	_guidance.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_guidance.custom_minimum_size.y = 48
	_guidance.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	bottom.add_child(_guidance)
	next_button = _button("",_next)
	next_button.custom_minimum_size = Vector2(210,48)
	bottom.add_child(next_button)
	footer = _label("第四周养成试玩 · 授课、成长、MVP与两段原版剧情。",13,Color("9ab1a4"))
	column.add_child(footer)
	story_reader = StoryReader.new()
	add_child(story_reader)
	story_reader.visible = false
	story_reader.command.connect(_story_command)
	story_reader.return_requested.connect(_close_story)
	story_reader.save_requested.connect(_manual_save)
	model.start()
	if auto_load:
		var loaded := model.load_file(save_path)
		if loaded["supported"]:
			_save_message = "已恢复备份" if loaded["status"] == "recovered_backup" else "已读取试玩存档"
			_restore_view()
		elif loaded["reason"] != "save_missing":
			_save_message = "存档读取失败，当前为新试玩"
	refresh()


func _open_battle() -> void:
	var saved := model.save_file(save_path)
	if not saved["supported"]:
		_save_message = "保存失败"
		_message = "进度未能保存，暂时不能离开学校。"
		refresh()
		return
	get_tree().root.set_meta("school_playground_save_path",save_path)
	Engine.time_scale = 1.0
	get_tree().change_scene_to_file("res://main.tscn")


func _restore_view() -> void:
	selected_id = -1
	selected_kind = ""
	detail_id = 3
	for group in range(5):
		if _identity("teacher",group,-1) >= 0:
			selected_class = group
	page = "groups" if model.stage() == "planning" else "results"
	if model.stage() == "story":
		page = "story"


func _manual_save() -> void:
	var result := model.save_file(save_path)
	_save_message = "已保存试玩进度" if result["supported"] else "保存失败，当前进度尚未写入"
	_message = "编班、课程和成长结果已保存。" if result["supported"] else "保存未成功。请保留当前窗口，稍后重试。"
	refresh()


func _load() -> void:
	var result := model.load_file(save_path)
	if result["supported"]:
		_restore_view()
		_save_message = "已恢复备份" if result["status"] == "recovered_backup" else "已读取试玩存档"
		_message = "当前存档无法读取，已恢复上一份备份。" if result["status"] == "recovered_backup" else "已恢复保存的安排与成长。"
	else:
		_message = "尚无试玩存档，请先保存。" if result["reason"] == "save_missing" else "存档读取失败，当前进度已保留。"
	refresh()


func _restart_confirmed() -> void:
	var candidate := Playground.new()
	if not candidate.start()["supported"]:
		_message = "重新开始失败，当前进度已保留。"
		refresh()
		return
	if autosave and not candidate.save_file(save_path)["supported"]:
		_message = "无法替换存档，当前进度已保留。"
		refresh()
		return
	model = candidate
	_restore_view()
	selected_class = 0
	_save_message = "新试玩已保存" if autosave else "尚未保存"
	_message = "已重新开始，可尝试其他课程或安排。"
	refresh()


func _build_groups(parent: VBoxContainer) -> void:
	_groups = VBoxContainer.new()
	_groups.add_theme_constant_override("separation",8)
	parent.add_child(_groups)
	var heading := HBoxContainer.new()
	_groups.add_child(heading)
	heading.add_child(_label("班级安排",22,Color("ead6a3")))
	_class_caption = _label("",13,Color("bacdbf"))
	_class_caption.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_class_caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_class_caption.clip_text = true
	heading.add_child(_class_caption)
	for group in range(5):
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation",6)
		_groups.add_child(row)
		var select := _button("%d班" % (group+1),func(): selected_class = group; refresh())
		select.custom_minimum_size = Vector2(46,58)
		select.toggle_mode = true
		row.add_child(select)
		class_buttons.append(select)
		var teacher := _button("",func(): _cell("teacher",group,-1))
		teacher.custom_minimum_size = Vector2(105,58)
		row.add_child(teacher)
		teacher_buttons.append(teacher)
		var students := []
		for slot in range(4):
			var student := _button("",func(): _cell("student",group,slot))
			student.custom_minimum_size = Vector2(96,58)
			row.add_child(student)
			students.append(student)
		student_buttons.append(students)
		var status := _label("",13,Color("c9c9aa"))
		status.visible = false
		_groups.add_child(status)
		class_labels.append(status)
	var wait_heading := HBoxContainer.new()
	_groups.add_child(wait_heading)
	var title := _label("待命区",18,Color("ead6a3"))
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	wait_heading.add_child(title)
	wait_target = _button("移到待命",func(): _move(-1,-1))
	wait_heading.add_child(wait_target)
	cancel_button = _button("取消选择",_cancel)
	wait_heading.add_child(cancel_button)
	_waiting = HBoxContainer.new()
	_waiting.custom_minimum_size.y = 58
	_groups.add_child(_waiting)


func _cell(kind: String, group: int, slot: int) -> void:
	if model.stage() != "planning":
		var existing := _identity(kind,group,slot)
		if existing >= 0:
			detail_id = existing
		refresh()
		return
	if selected_id >= 0 and selected_kind == kind:
		_move(group,slot)
		return
	var identity := _identity(kind,group,slot)
	if identity >= 0:
		selected_id = identity
		selected_kind = kind
		detail_id = identity
		_message = ""
	else:
		_message = "先选择一位%s，再点击目标位置。" % ("教师" if kind == "teacher" else "学生")
	refresh()


func _identity(kind: String, group: int, slot: int) -> int:
	return Groups._word(model.session.read_snapshot()["group_raw_bytes"],group*28+(0 if kind == "teacher" else 16+slot*2))


func _move(group: int, slot: int) -> void:
	if selected_id < 0 or model.stage() != "planning":
		return
	if selected_kind == "student" and group >= 0 and _identity("teacher",group,-1) == -1:
		_message = "请先为这个班安排教师。"
		refresh()
		return
	var result := model.execute({"op":"move","kind":selected_kind,"member_id":selected_id,
		"target_group":group,"target_slot":slot})
	if result["supported"]:
		selected_class = group if group >= 0 else selected_class
		selected_id = -1
		selected_kind = ""
		_message = "班级安排已更新。"
		_save()
	else:
		_message = "请先为这个班安排教师。" if group >= 0 and _identity("teacher",group,-1) == -1 else "这个位置暂时无法安排该成员。"
	refresh()


func _cancel() -> void:
	selected_id = -1
	selected_kind = ""
	_message = ""
	refresh()


func _act(command: Dictionary) -> bool:
	var result := model.execute(command)
	if not result["supported"]:
		_message = "当前安排还不能完成这一步，请检查教师、学生和课程。"
		return false
	_save()
	return true


func _save() -> void:
	if not autosave:
		return
	var result := model.save_file(save_path)
	_save_message = "已自动保存" if result["supported"] else "保存失败：本次修改仅保留在内存"


func _choose(course: int) -> void:
	if model.stage() != "planning":
		return
	if _act({"op":"mode","group":selected_class,"teaching":true}) and _act({"op":"course","group":selected_class,"course":course}):
		_message = "%d班已安排%s。" % [selected_class+1,catalog["courses"][str(course)]["name"]]
	refresh()


func _next() -> void:
	match model.stage():
		"planning":
			if _act({"op":"grow"}):
				page = "results"
				_message = "授课完成，可以查看学生的成长。"
		"grown":
			if _act({"op":"confirm"}):
				_message = "关系和职业进度已记录。"
		"confirmed":
			if _act({"op":"complete"}):
				_message = "本次MVP已记录。"
		"completed":
			if _act({"op":"story_start"}):
				page = "story"
		"story":
			page = "story"
	refresh()


func _story_command(op: String) -> void:
	if page != "story" or model.stage() != "story":
		return
	if _act({"op":op}):
		page = "story" if model.stage() == "story" else "results"
		_message = "" if page == "story" else "本周剧情已结束，成长和MVP已保留。"
	refresh()


func _close_story() -> void:
	page = "results"
	_message = "阅读位置已保留，可继续阅读。"
	refresh()


func refresh() -> void:
	if model.session == null:
		return
	var stage := model.stage()
	var snapshot := model.session.read_snapshot()
	_status.text = _save_message
	_groups.visible = page == "groups"
	_courses.visible = page == "courses"
	_results.visible = page == "results"
	for key in tab_buttons:
		tab_buttons[key].button_pressed = page == key
	var current := ["planning","grown","confirmed","completed"].find(stage)
	if current < 0:
		current = 3
	for index in range(4):
		_stage_labels[index].add_theme_color_override("font_color",Color("ead6a3") if index <= current else Color("728b7d"))
	for group in range(5):
		class_buttons[group].button_pressed = selected_class == group
		var teacher := _identity("teacher",group,-1)
		_set_member(teacher_buttons[group],teacher,"教师")
		for slot in range(4):
			_set_member(student_buttons[group][slot],_identity("student",group,slot),"空位")
		var count: int = snapshot["group_raw_bytes"][group*28+14]
		var course := Groups._word(snapshot["group_raw_bytes"],group*28+10)
		var teaching: bool = snapshot["group_raw_bytes"][group*28+3] == 1
		var caption := "尚无教师 · 可安排教师后加入学生"
		if teacher >= 0:
			caption = "%d名学生 · 关系 %d" % [count,model.session.view()["ratings"][group]["relationship_mean"]]
			caption += " · "+catalog["courses"].get(str(course),{"name":"未选课程"})["name"] if teaching else " · 等待安排授课"
		class_labels[group].text = caption
		class_buttons[group].tooltip_text = caption
	_class_caption.text = "%d班 · %s" % [selected_class+1,class_labels[selected_class].text]
	wait_target.disabled = selected_id < 0 or stage != "planning"
	cancel_button.disabled = selected_id < 0
	_clear(_waiting)
	waiting_buttons.clear()
	for kind in ["teacher","student"]:
		for identity in snapshot["idle_teacher_ids" if kind == "teacher" else "idle_student_ids"]:
			var button := _button("",func(): selected_id = identity; selected_kind = kind; detail_id = identity; refresh())
			button.custom_minimum_size = Vector2(105,58)
			_waiting.add_child(button)
			_set_member(button,identity,"")
			waiting_buttons[identity] = button
	if waiting_buttons.is_empty():
		_waiting.add_child(_label("全部成员均已编班",15,Color("a0b5a8")))
	_refresh_courses()
	_refresh_detail()
	_refresh_results()
	next_button.text = {"planning":"开始授课","grown":"确认本周记录","confirmed":"评选本次MVP",
		"completed":"阅读本周剧情","story":"继续阅读剧情","story_completed":"本周剧情已完成","arrival":"已到达第五周"}[stage]
	var ready := false
	for rating in model.session.view()["ratings"]:
		if rating["state"] == 4:
			ready = true
	next_button.disabled = stage in ["story_completed","arrival"] or (stage == "planning" and not ready)
	_guidance.text = {"planning":"选择成员，再点目标位置。进入「授课安排」选择课程。",
		"grown":"学生成长已完成。确认记录后，可评选本次MVP。","confirmed":"本周记录已确认。下一步记录MVP。",
		"completed":"本次MVP已记录，接下来阅读本周剧情。","story":"可从保存的位置继续阅读本周剧情。",
		"story_completed":"本周剧情已结束，成长和MVP均已保留。","arrival":"已到达第五周。"}[stage]
	if selected_id >= 0:
		_guidance.text = "已选%s · 点击目标%s位置，或移到待命。Esc取消。" % [_name(selected_id),"教师" if selected_kind == "teacher" else "学生"]
	if not _message.is_empty():
		_guidance.text = _message
	story_reader.visible = page == "story" and stage == "story"
	if story_reader.visible:
		story_reader.show_page(model.read_story_page(),model.state()["story"]["cursor"],
			model.state()["story"]["total"],model.story_catalog(),_save_message)


func _refresh_courses() -> void:
	_clear(_courses)
	course_buttons.clear()
	_courses.add_child(_label("%d班 · 授课安排" % (selected_class+1),22,Color("ead6a3")))
	var selector := HBoxContainer.new()
	_courses.add_child(selector)
	for group in range(5):
		var button := _button("%d班" % (group+1),func(): selected_class = group; _message = ""; refresh())
		button.toggle_mode = true
		button.button_pressed = group == selected_class
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		selector.add_child(button)
	var teacher := _identity("teacher",selected_class,-1)
	var caption := "这个班尚无教师。请返回编班安排教师。"
	if teacher >= 0:
		caption = "授课教师 · "+_name(teacher)+"\n选择一门课程，所有在班学生都会参加。"
	var info := _label(caption,17,Color("bdd1c4"))
	info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_courses.add_child(info)
	var available := []
	var listed := model.session.list_courses(selected_class)
	if listed["supported"]:
		for category in listed["courses"]:
			for row in category:
				available.append(row[1])
	var snapshot := model.session.read_snapshot()
	var assigned := Groups._word(snapshot["group_raw_bytes"],selected_class*28+10)
	var teaching: bool = snapshot["group_raw_bytes"][selected_class*28+3] == 1
	for course in [10,11,12]:
		var data: Dictionary = catalog["courses"][str(course)]
		var button := _button(data["name"]+"    "+("✓ 已安排" if teaching and assigned == course else "选择此课")+"\n"+data["subtitle"],func(): _choose(course))
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.custom_minimum_size.y = 72
		button.disabled = course not in available or model.stage() != "planning"
		button.toggle_mode = true
		button.button_pressed = teaching and assigned == course
		button.tooltip_text = data["description"]
		_courses.add_child(button)
		course_buttons[course] = button
	var note := _label("课程影响成长点和技能学习机会。\n实际属性提升可在授课后查看；待命学生不参加。",15,Color("9db6a6"))
	note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_courses.add_child(note)


func _refresh_detail() -> void:
	_clear(_detail)
	var profile := {}
	for row in model.session.read_snapshot()["member_profiles"]:
		if row["member_id"] == detail_id:
			profile = row
	if profile.is_empty():
		return
	_detail.add_child(_label("成员详情",18,Color("ead6a3")))
	var header := HBoxContainer.new()
	header.add_theme_constant_override("separation",14)
	_detail.add_child(header)
	header.add_child(_portrait(detail_id,Vector2(78,78)))
	var title := VBoxContainer.new()
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header.add_child(title)
	var name_label := _label(_name(detail_id),22,Color("f0e4c3"))
	name_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	title.add_child(name_label)
	title.add_child(_label("教师" if detail_id >= 101 else "Lv.%d" % profile["level_50"],18))
	if detail_id >= 101:
		var note := _label("负责授课与班级安排。\n点击教师头像可调整班级。",16,Color("bacdbf"))
		note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		_detail.add_child(note)
		return
	_detail.add_child(HSeparator.new())
	for index in range(7):
		var row := HBoxContainer.new()
		_detail.add_child(row)
		var caption := _label(catalog["attribute_names"][index],15,Color("becfc3"))
		caption.custom_minimum_size.x = 42
		row.add_child(caption)
		var bar := ProgressBar.new()
		bar.min_value = 0
		bar.max_value = 135
		bar.value = profile["attributes"][index]
		bar.show_percentage = false
		bar.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		bar.custom_minimum_size.y = 14
		bar.add_theme_stylebox_override("background",_style("0d2020",0))
		bar.add_theme_stylebox_override("fill",_style("779d86",0))
		row.add_child(bar)
		var value := _label(str(profile["attributes"][index]),16,Color("ead6a3"))
		value.custom_minimum_size.x = 32
		value.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
		row.add_child(value)
	_detail.add_child(HSeparator.new())
	var info := _label("点击头像查看能力。\n同班成员共同授课，待命成员保留原有成长。",15,Color("9db6a6"))
	info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_detail.add_child(info)


func _refresh_results() -> void:
	_clear(_results)
	result_cards.clear()
	mvp_label = null
	_results.add_child(_label("本周成长",22,Color("ead6a3")))
	var growth := model.session.read_settlement()
	if growth.is_empty():
		var hint := _label("安排课程并开始授课后，可以在这里查看成长与MVP。\n\n进入「授课安排」，选择一门课程后点击「开始授课」。",18,Color("bacdbf"))
		hint.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		_results.add_child(hint)
		return
	var completed := model.session.read_result_handoff()
	if not completed.is_empty():
		var hero := PanelContainer.new()
		hero.add_theme_stylebox_override("panel",_style("3b4935",10))
		_results.add_child(hero)
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation",16)
		hero.add_child(row)
		row.add_child(_label("MVP",27,Color("f4d386")))
		row.add_child(_portrait(completed["recipient"],Vector2(64,64)))
		var text := VBoxContainer.new()
		row.add_child(text)
		mvp_label = _label(_name(completed["recipient"]),24,Color("f4dfad"))
		text.add_child(mvp_label)
		text.add_child(_label("本次成长累计 %d · MVP次数 %d→%d" % [completed["staged_total"],completed["old_count"],mini(completed["old_count"]+1,5)],14))
	var participants := []
	for packet in growth["packets"]:
		participants.append(packet["character_id"])
	var confirmation := model.session.read_confirmation()
	for index in range(3):
		var record: Dictionary = growth["records"][index]
		var old: Dictionary = growth["before_records"][index]
		var identity: int = record["character_id"]
		var card := PanelContainer.new()
		card.add_theme_stylebox_override("panel",_style("213a34",8))
		_results.add_child(card)
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation",12)
		card.add_child(row)
		var portrait := _button("",func(): detail_id = identity; refresh())
		portrait.custom_minimum_size = Vector2(68,60)
		_set_member(portrait,identity,"")
		portrait.text = ""
		portrait.add_theme_constant_override("icon_max_width",56)
		row.add_child(portrait)
		result_cards[identity] = portrait
		var content := VBoxContainer.new()
		content.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		row.add_child(content)
		var skill_count := 0
		for skill in range(84):
			if old["skill_statuses"][skill] != 2 and record["skill_statuses"][skill] == 2:
				skill_count += 1
		var caption := "%s · Lv.%d → %d" % [_name(identity),old["level_50"],record["level_50"]]
		if skill_count > 0:
			caption += " · 领悟%d项技能" % skill_count
		content.add_child(_label(caption,16,Color("e9d9ac")))
		var changes := PackedStringArray()
		for attribute in range(7):
			if old["attributes"][attribute] != record["attributes"][attribute]:
				changes.append("%s %d→%d" % [catalog["attribute_names"][attribute],old["attributes"][attribute],record["attributes"][attribute]])
		var summary := " · ".join(changes)
		if identity not in participants:
			summary = "本周待命 · 未参加授课"
		elif summary.is_empty():
			summary = "成长点已累计，属性尚未跨越下一阈值。"
		if not confirmation.is_empty() and identity in participants:
			summary += " · 本周记录已确认"
		var description := _label(summary,13,Color("bdd3bf"))
		description.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		content.add_child(description)
	var note := _label("成长已结算；确认后记录关系、职业进度及本周活动。",15,Color("a9c6af"))
	if not confirmation.is_empty():
		note.text = "关系与职业进度已确认；本次结算不会重复发放。"
	if not completed.is_empty():
		note.text = "本次MVP已记录。继续阅读本周剧情，进度会自动保存。"
		if model.stage() == "story_completed":
			note.text = "本周剧情已结束。授课成长、关系、职业进度和MVP均已保留。"
	note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_results.add_child(note)


func _set_member(button: Button, identity: int, empty: String) -> void:
	button.text = _name(identity) if identity >= 0 else empty
	button.icon = _texture(catalog["characters"][str(identity)]["portrait"]) if catalog["characters"].has(str(identity)) else null
	button.expand_icon = true
	button.add_theme_constant_override("icon_max_width",38)
	button.add_theme_font_size_override("font_size",13)
	button.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	button.toggle_mode = true
	button.button_pressed = identity >= 0 and identity == selected_id
	button.tooltip_text = "点击选择"+_name(identity) if identity >= 0 else "点击放入已选择的成员"


func _name(identity: int) -> String:
	return catalog["characters"].get(str(identity),{"name":"成员 #%d" % identity})["name"]


func _texture(filename: String) -> Texture2D:
	if not _textures.has(filename):
		var image := Image.load_from_file(ART+filename)
		if image == null or image.is_empty():
			return null
		_textures[filename] = ImageTexture.create_from_image(image)
	return _textures[filename]


func _portrait(identity: int, dimensions: Vector2) -> TextureRect:
	var rect := TextureRect.new()
	rect.texture = _texture(catalog["characters"][str(identity)]["portrait"])
	rect.custom_minimum_size = dimensions
	rect.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	rect.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	rect.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return rect


static func _label(caption: String, font_size := 16, color := Color("d8e1d6")) -> Label:
	var label := Label.new()
	label.text = caption
	label.add_theme_font_size_override("font_size",font_size)
	label.add_theme_color_override("font_color",color)
	return label


static func _button(caption: String, action: Callable) -> Button:
	var button := Button.new()
	button.text = caption
	button.pressed.connect(action)
	return button


static func _style(background: String, margin: int) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(background)
	style.border_color = Color("577267")
	style.set_border_width_all(1)
	style.set_corner_radius_all(5)
	style.content_margin_left = margin
	style.content_margin_right = margin
	style.content_margin_top = margin
	style.content_margin_bottom = margin
	return style


static func _clear(container: Node) -> void:
	for child in container.get_children():
		container.remove_child(child)
		child.queue_free()


func _input(event: InputEvent) -> void:
	if story_reader.visible and event is InputEventKey and event.pressed and not event.echo \
			and not story_reader.skip_dialog.visible:
		if event.keycode in [KEY_ENTER,KEY_SPACE,KEY_RIGHT]:
			_story_command("story_next")
		elif event.keycode == KEY_LEFT:
			_story_command("story_prev")
		elif event.keycode == KEY_ESCAPE:
			_close_story()
		else:
			return
		get_viewport().set_input_as_handled()
		return


func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE:
		_cancel()
		get_viewport().set_input_as_handled()
