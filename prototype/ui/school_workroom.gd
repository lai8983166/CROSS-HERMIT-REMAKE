extends Control
signal continue_requested
signal review_requested
signal battle_requested
signal save_requested
signal restart_requested

var continue_button: Button
var review_button: Button
var battle_button: Button
var save_button: Button
var restart_button: Button
var guidance: Label
var status: Label


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var background := TextureRect.new()
	background.texture = ImageTexture.create_from_image(Image.load_from_file("res://assets/school_workroom/background.png"))
	background.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	background.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)
	var margin := MarginContainer.new()
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	for side in ["left","right","top","bottom"]:
		margin.add_theme_constant_override("margin_"+side,40)
	add_child(margin)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation",16)
	margin.add_child(column)
	var heading := PanelContainer.new()
	column.add_child(heading)
	var titles := VBoxContainer.new()
	heading.add_child(titles)
	titles.add_child(_label("纯洁之盾 · 职务室",34,Color("ead6a3")))
	titles.add_child(_label("4月 · 第5周",20,Color("bfd0c0")))
	var spacer := Control.new()
	spacer.size_flags_vertical = Control.SIZE_EXPAND_FILL
	column.add_child(spacer)
	var card := PanelContainer.new()
	column.add_child(card)
	var content := VBoxContainer.new()
	content.add_theme_constant_override("separation",12)
	card.add_child(content)
	guidance = _label("",20,Color("eadfc1"))
	guidance.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	content.add_child(guidance)
	continue_button = _button("听取巡逻班建议  →",func(): continue_requested.emit())
	continue_button.custom_minimum_size.y = 48
	content.add_child(continue_button)
	var toolbar := HBoxContainer.new()
	toolbar.add_theme_constant_override("separation",12)
	content.add_child(toolbar)
	review_button = _button("回顾第四周成长",func(): review_requested.emit())
	battle_button = _button("战斗预览",func(): battle_requested.emit())
	save_button = _button("保存进度",func(): save_requested.emit())
	restart_button = _button("重开本段",func(): restart_requested.emit())
	for button in [review_button,battle_button,save_button,restart_button]:
		button.custom_minimum_size.y = 44
		button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		toolbar.add_child(button)
	status = _label("",14,Color("a6bfae"))
	content.add_child(status)


func show_workroom(state: Dictionary, save_status: String) -> void:
	var prepared: bool = not state["fifth_school"].is_empty()
	var cursor: int = state["work_story"]["cursor"]
	continue_button.text = "返回第五周编班  →" if prepared else "进入第五周学校  →" if state["work_story"]["completed"] \
		else "继续巡逻班对白  →" if cursor >= 0 else "听取巡逻班建议  →"
	guidance.text = "第五周编班安排已保留，可以返回学校继续调整。" if prepared else "先听取巡逻班的建议，再进入第五周学校安排。"
	guidance.text += "\n第四周的成长、关系与MVP已保留。"
	status.text = save_status+"　 ·　战斗预览使用独立试玩队伍"


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
