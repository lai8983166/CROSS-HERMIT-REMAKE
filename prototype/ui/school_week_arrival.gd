extends Control
signal review_requested
signal battle_requested
signal save_requested
signal restart_requested
signal continue_requested

const ART := "res://assets/school/"
var review_button: Button
var battle_button: Button
var save_button: Button
var restart_button: Button
var continue_button: Button
var boundary: Label
var introduction: Label
var calendar: Label
var status: Label
var summaries: Array = []
var _textures: Dictionary = {}


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var background := TextureRect.new()
	background.texture = _texture("background.png")
	background.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	background.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)
	var shade := ColorRect.new()
	shade.color = Color(0.03,0.08,0.07,0.87)
	shade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	shade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(shade)
	var margin := MarginContainer.new()
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	for side in ["left","right"]:
		margin.add_theme_constant_override("margin_"+side,80)
	for side in ["top","bottom"]:
		margin.add_theme_constant_override("margin_"+side,48)
	add_child(margin)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation",14)
	margin.add_child(column)
	column.add_child(_label("纯洁之盾 · 新的一周",24,Color("b7cbbc")))
	calendar = _label("4月 · 第5周",42,Color("ead6a3"))
	column.add_child(calendar)
	introduction = _label("本周剧情已结束，学生们带着成长进入新的一周。",19,Color("c6d6c6"))
	column.add_child(introduction)
	var cards := HBoxContainer.new()
	cards.add_theme_constant_override("separation",16)
	cards.size_flags_vertical = Control.SIZE_EXPAND_FILL
	column.add_child(cards)
	for identity in [3,4,9]:
		var card := PanelContainer.new()
		card.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		cards.add_child(card)
		var content := VBoxContainer.new()
		content.add_theme_constant_override("separation",10)
		content.alignment = BoxContainer.ALIGNMENT_CENTER
		card.add_child(content)
		var portrait := TextureRect.new()
		portrait.texture = _texture("portrait_%d.png" % identity)
		portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		portrait.custom_minimum_size = Vector2(88,88)
		portrait.mouse_filter = Control.MOUSE_FILTER_IGNORE
		content.add_child(portrait)
		var summary := _label("",18,Color("ead6a3"))
		summary.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		summary.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		content.add_child(summary)
		summaries.append(summary)
	boundary = _label("第五周剧情已开放，可继续阅读并前往职务室。\n学校安排正在开发，也可以回顾授课成长。",18,Color("bfd0c0"))
	boundary.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	column.add_child(boundary)
	continue_button = _button("阅读第五周剧情  →",func(): continue_requested.emit())
	continue_button.custom_minimum_size.y = 48
	column.add_child(continue_button)
	var toolbar := HBoxContainer.new()
	toolbar.add_theme_constant_override("separation",12)
	column.add_child(toolbar)
	review_button = _button("回顾授课成长",func(): review_requested.emit())
	battle_button = _button("战斗预览",func(): battle_requested.emit())
	save_button = _button("保存进度",func(): save_requested.emit())
	restart_button = _button("重开本段",func(): restart_requested.emit())
	for button in [review_button,battle_button,save_button,restart_button]:
		button.custom_minimum_size.y = 46
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		toolbar.add_child(button)
	status = _label("",14,Color("a6bfae"))
	column.add_child(status)


func show_arrival(state: Dictionary, catalog: Dictionary, save_status: String) -> void:
	var week: Dictionary = state["week"]
	var exited: bool = not state.get("fifth_exit",{}).is_empty()
	calendar.text = "4月 · 第5周　职务室入口" if exited else "%d月 · 第%d周" % [week["after"]["month"],week["after"]["week"]]
	introduction.text = "第五周剧情已结束，已到达职务室入口。" if exited else "学生们带着成长进入新的一周，可以继续阅读剧情。"
	boundary.text = "可以进入职务室，听取巡逻班建议，再前往第五周学校编班。" if exited else "第五周剧情已开放，可继续阅读并前往职务室。\n也可以回顾第四周授课成长。"
	continue_button.visible = true
	continue_button.text = "进入职务室  →" if exited else "前往职务室  →" if state.get("fifth_story",{}).get("completed",false) else "继续第五周剧情  →" if state.get("fifth_story",{}).get("cursor",-1) >= 0 else "阅读第五周剧情  →"
	for index in range(3):
		var before: Dictionary = week["before"]["participants"][index]
		var after: Dictionary = week["after"]["participants"][index]
		var unlocked := 0
		for job in range(30):
			if before["unlock_flags"][job] == 0 and after["unlock_flags"][job] == 1:
				unlocked += 1
		var identity: int = after["character_id"]
		summaries[index].text = "%s · Lv.%d\n职业资格新增 %d" % [
			catalog["characters"][str(identity)]["name"],state["growth"][index]["level_50"],unlocked]
	status.text = save_status+"　 ·　授课成长与MVP已保留"


func _texture(filename: String) -> Texture2D:
	if not _textures.has(filename):
		_textures[filename] = ImageTexture.create_from_image(Image.load_from_file(ART+filename))
	return _textures[filename]


static func _label(text: String, size: int, color: Color) -> Label:
	var label := Label.new()
	label.text = text
	label.add_theme_font_size_override("font_size",size)
	label.add_theme_color_override("font_color",color)
	return label


static func _button(text: String, callback: Callable) -> Button:
	var button := Button.new()
	button.text = text
	button.pressed.connect(callback)
	return button
