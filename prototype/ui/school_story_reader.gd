extends Control
## Original scene resources in a remake dialogue layout.
signal command(op: String)
signal return_requested
signal save_requested

const ART := "res://assets/school_story/"
var background: TextureRect
var actors: Array = []
var portraits: Array = []
var heading: Label
var speaker: Label
var dialogue: Label
var progress: Label
var status: Label
var previous_button: Button
var next_button: Button
var return_button: Button
var save_button: Button
var skip_button: Button
var skip_dialog: ConfirmationDialog
var _textures: Dictionary = {}
var _command_prefix := "story"
var _art_root := ART


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	background = _image()
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	background.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
	add_child(background)
	var shade := ColorRect.new()
	shade.color = Color(0.015,0.03,0.04,0.2)
	shade.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	shade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(shade)
	for slot in range(2):
		var actor := _image()
		actor.position = Vector2(64 if slot == 0 else 600,98)
		actor.size = Vector2(360,540)
		actor.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		add_child(actor)
		actors.append(actor)
	for slot in range(3):
		var portrait := _image()
		portrait.position = Vector2(116+slot*280,108)
		portrait.size = Vector2(232,268)
		portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		add_child(portrait)
		portraits.append(portrait)
	var toolbar := PanelContainer.new()
	toolbar.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	toolbar.offset_left = 24
	toolbar.offset_right = -24
	toolbar.offset_top = 20
	toolbar.offset_bottom = 82
	add_child(toolbar)
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation",12)
	toolbar.add_child(row)
	heading = _label("",21,Color("ead6a3"))
	heading.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(heading)
	save_button = _button("保存",func(): save_requested.emit())
	return_button = _button("返回结果",func(): return_requested.emit())
	skip_button = _button("跳过剧情",func(): skip_dialog.popup_centered(Vector2i(440,180)))
	for button in [save_button,return_button,skip_button]:
		button.custom_minimum_size = Vector2(96,40)
		row.add_child(button)
	var box := PanelContainer.new()
	box.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
	box.offset_left = 24
	box.offset_right = -24
	box.offset_top = -332
	box.offset_bottom = -20
	add_child(box)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation",10)
	box.add_child(column)
	speaker = _label("",24,Color("ead6a3"))
	column.add_child(speaker)
	dialogue = _label("",22,Color("f0eadc"))
	dialogue.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue.size_flags_vertical = Control.SIZE_EXPAND_FILL
	column.add_child(dialogue)
	var navigation := HBoxContainer.new()
	navigation.add_theme_constant_override("separation",16)
	column.add_child(navigation)
	previous_button = _button("上一页",func(): command.emit(_command_prefix+"_prev"))
	previous_button.custom_minimum_size = Vector2(100,40)
	navigation.add_child(previous_button)
	progress = _label("",14,Color("adbfaf"))
	progress.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	navigation.add_child(progress)
	next_button = _button("下一页  →",func(): command.emit(_command_prefix+"_next"))
	next_button.custom_minimum_size = Vector2(170,40)
	navigation.add_child(next_button)
	status = _label("",13,Color("adbfaf"))
	column.add_child(status)
	skip_dialog = ConfirmationDialog.new()
	skip_dialog.title = "跳过剩余剧情"
	skip_dialog.dialog_text = "将结束本周的两段剧情。\n授课成长和本次MVP会保留。"
	skip_dialog.ok_button_text = "确认跳过"
	skip_dialog.cancel_button_text = "继续阅读"
	skip_dialog.confirmed.connect(func(): command.emit(_command_prefix+"_skip"))
	add_child(skip_dialog)


func show_page(page: Dictionary, cursor: int, total: int, catalog: Dictionary, save_status: String, options := {}) -> void:
	_command_prefix = options.get("command_prefix","story")
	_art_root = options.get("art_root",ART)
	heading.text = options.get("calendar","4月 · 第4周")+"　｜　"+page["scene_label"]
	return_button.text = options.get("return_label","返回结果")
	skip_dialog.dialog_text = options.get("skip_prompt","将结束本周的两段剧情。\n授课成长和本次MVP会保留。")
	speaker.text = catalog["actors"][str(page["speaker"])]["name"]
	dialogue.text = page["text"]
	background.texture = _texture(catalog["backgrounds"][str(page["background"])]["image"])
	for actor in actors+portraits:
		actor.visible = false
	for index in range(portraits.size()):
		portraits[index].position = Vector2(116+index*280,108)
	var ordinal := 0
	for member in page["characters"]:
		var portrait_index: int = options.get("portrait_slots",[7,8,9]).find(member["slot"])
		var actor: TextureRect = portraits[portrait_index] if member.get("kind") == "portrait" else actors[0 if member["slot"] == 5 else 1]
		if member.get("kind") == "portrait" and options.get("center_portraits",false):
			actor.position = Vector2(396 if page["characters"].size() == 1 else 186+ordinal*420,108)
		ordinal += 1
		var key: String = member.get("asset_key",str(member["id"]))
		actor.texture = _texture(catalog["actors"][key]["image"])
		actor.visible = true
		actor.modulate = Color.WHITE if key == str(page["speaker"]) else Color(0.68,0.72,0.73)
	previous_button.disabled = cursor == 0
	next_button.custom_minimum_size.x = 280 if _command_prefix in ["fifth","work"] else 170
	next_button.text = options.get("ending_text","结束本周剧情  →") if cursor == total-1 else "下一页  →"
	progress.text = "%d / %d　 ·　Enter / Space 下一页，← 上一页" % [cursor+1,total]
	status.text = save_status


func _texture(filename: String) -> Texture2D:
	var key := _art_root+filename
	if not _textures.has(key):
		var source := Image.load_from_file(key)
		_textures[key] = ImageTexture.create_from_image(source)
	return _textures[key]


static func _image() -> TextureRect:
	var image := TextureRect.new()
	image.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	image.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return image


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
