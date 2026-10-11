extends Control
## Read-only current-map inspection; owns no school or battle state.

signal closed

const CATALOG := "res://assets/current_scene/catalog.json"
const ATLAS := "res://assets/current_scene/map05.png"
const DIALOGUE := "res://data/school_opening_dialogue.json"
const DIALOGUE_SHA256 := "645cf3b69aecc6806886b79080dc66eac583527d74dac6dc90e93431c35a7a10"
const SCRIPT_SHA256 := "44ca546b5ea90ec23a4bc7d8dffeac6547a44bfd035383c91983f7c13ae72a52"

class MapCanvas extends Control:

	var texture: Texture2D
	var zoom := 1.0
	var origin := Vector2.ZERO
	var dragging := false
	var fit_mode := true

	func _ready() -> void:
		clip_contents = true
		mouse_default_cursor_shape = Control.CURSOR_DRAG
		resized.connect(func(): fit_map() if fit_mode else clamp_origin())

	func fit_map() -> void:
		if texture == null or size.x <= 0 or size.y <= 0:
			return
		fit_mode = true
		zoom = minf(size.x/texture.get_width(),size.y/texture.get_height())
		origin = (size-texture.get_size()*zoom)*0.5
		queue_redraw()

	func clamp_origin() -> void:
		if texture == null:
			return
		var extent := texture.get_size()*zoom
		for axis in range(2):
			origin[axis] = (size[axis]-extent[axis])*0.5 if extent[axis] <= size[axis] \
				else clampf(origin[axis],size[axis]-extent[axis],0.0)
		queue_redraw()

	func zoom_at(factor: float, anchor: Vector2) -> void:
		if texture == null:
			return
		var image_point := (anchor-origin)/zoom
		var fit_zoom := minf(size.x/texture.get_width(),size.y/texture.get_height())
		zoom = clampf(zoom*factor,fit_zoom*0.5,2.0)
		origin = anchor-image_point*zoom
		fit_mode = false
		clamp_origin()

	func pan(delta: Vector2) -> void:
		origin += delta
		fit_mode = false
		clamp_origin()

	func _gui_input(event: InputEvent) -> void:
		if event is InputEventMouseButton:
			if event.button_index == MOUSE_BUTTON_LEFT:
				dragging = event.pressed
				accept_event()
			elif event.pressed and event.button_index in [MOUSE_BUTTON_WHEEL_UP,MOUSE_BUTTON_WHEEL_DOWN]:
				zoom_at(1.25 if event.button_index == MOUSE_BUTTON_WHEEL_UP else 0.8,event.position)
				accept_event()
		elif event is InputEventMouseMotion and dragging:
			pan(event.relative)
			accept_event()

	func _draw() -> void:
		draw_rect(Rect2(Vector2.ZERO,size),Color("0e181b"))
		if texture != null:
			draw_texture_rect(texture,Rect2(origin,texture.get_size()*zoom),false)


var canvas: MapCanvas
var close_button: Button
var fit_button: Button
var zoom_in_button: Button
var zoom_out_button: Button
var title: Label
var dialogue_button: Button
var dialogue_panel: PanelContainer
var dialogue_text: Label
var dialogue_position: Label
var dialogue_previous: Button
var dialogue_next: Button
var dialogue_close: Button
var dialogue_pages: Array = []
var dialogue_index := 0


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	z_index = 100
	mouse_filter = Control.MOUSE_FILTER_STOP
	var background := ColorRect.new()
	background.color = Color("142426")
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(background)
	var margin := MarginContainer.new()
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	for side in ["left","right","top","bottom"]:
		margin.add_theme_constant_override("margin_"+side,16)
	add_child(margin)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation",12)
	margin.add_child(column)
	var header := HBoxContainer.new()
	column.add_child(header)
	title = Label.new()
	title.text = "第五周 · 必修冒险地图"
	title.add_theme_font_size_override("font_size",22)
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	header.add_child(title)
	dialogue_button = _button("开场对白",open_dialogue)
	header.add_child(dialogue_button)
	fit_button = _button("显示全图",func(): canvas.fit_map())
	header.add_child(fit_button)
	zoom_out_button = _button("−",func(): canvas.zoom_at(0.8,canvas.size*0.5))
	header.add_child(zoom_out_button)
	zoom_in_button = _button("＋",func(): canvas.zoom_at(1.25,canvas.size*0.5))
	header.add_child(zoom_in_button)
	close_button = _button("返回队伍",close_preview)
	header.add_child(close_button)
	canvas = MapCanvas.new()
	canvas.size_flags_vertical = Control.SIZE_EXPAND_FILL
	column.add_child(canvas)
	_build_dialogue()
	var footer := Label.new()
	footer.text = "拖动查看 · 滚轮缩放 · Esc 返回    |    地图预览，战斗暂未开放"
	footer.add_theme_font_size_override("font_size",14)
	column.add_child(footer)
	visible = false


func _build_dialogue() -> void:
	dialogue_panel = PanelContainer.new()
	dialogue_panel.mouse_filter = Control.MOUSE_FILTER_STOP
	canvas.add_child(dialogue_panel)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.045,0.09,0.10,0.97)
	style.border_color = Color("bfa66b")
	style.set_border_width_all(2)
	style.set_corner_radius_all(6)
	style.content_margin_left = 24
	style.content_margin_right = 24
	style.content_margin_top = 18
	style.content_margin_bottom = 18
	dialogue_panel.add_theme_stylebox_override("panel",style)
	var content := VBoxContainer.new()
	content.add_theme_constant_override("separation",12)
	dialogue_panel.add_child(content)
	var heading := HBoxContainer.new()
	content.add_child(heading)
	var label := Label.new()
	label.text = "开场对白预览"
	label.add_theme_font_size_override("font_size",18)
	label.add_theme_color_override("font_color",Color("e2c890"))
	label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	heading.add_child(label)
	dialogue_position = Label.new()
	heading.add_child(dialogue_position)
	dialogue_text = Label.new()
	dialogue_text.add_theme_font_size_override("font_size",24)
	dialogue_text.add_theme_color_override("font_color",Color("f6f1e7"))
	dialogue_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_text.custom_minimum_size.y = 76
	content.add_child(dialogue_text)
	var controls := HBoxContainer.new()
	controls.add_theme_constant_override("separation",12)
	content.add_child(controls)
	dialogue_previous = _button("上一段",func(): _turn_dialogue(-1))
	controls.add_child(dialogue_previous)
	dialogue_next = _button("下一段",func(): _turn_dialogue(1))
	controls.add_child(dialogue_next)
	var spacer := Control.new()
	spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	controls.add_child(spacer)
	dialogue_close = _button("关闭对白",close_dialogue)
	controls.add_child(dialogue_close)
	canvas.resized.connect(_layout_dialogue)
	dialogue_panel.minimum_size_changed.connect(_layout_dialogue)
	dialogue_panel.visible = false


func _layout_dialogue() -> void:
	if dialogue_panel == null:
		return
	# Width first permits wrapped text to determine the panel's minimum height.
	dialogue_panel.size.x = maxf(0,canvas.size.x-32)
	dialogue_panel.size.y = dialogue_panel.get_combined_minimum_size().y
	dialogue_panel.position = Vector2(16,maxf(16,canvas.size.y-dialogue_panel.size.y-16))


static func valid_dialogue(catalog: Variant) -> bool:
	if not catalog is Dictionary or catalog.get("schema_version") != 1 \
			or catalog.get("adventure_id") != 5 or catalog.get("scene_id") != 5 \
			or catalog.get("source_script_sha256") != SCRIPT_SHA256 \
			or catalog.get("encoding") != "Big5" or catalog.get("mode") != "read_only_opening_preview":
		return false
	for key in ["schema_version","adventure_id","scene_id"]:
		if typeof(catalog.get(key)) not in [TYPE_INT,TYPE_FLOAT]:
			return false
	var pages = catalog.get("pages")
	if not pages is Array or pages.size() != 10:
		return false
	for index in range(pages.size()):
		var page = pages[index]
		if not page is Dictionary or typeof(page.get("text_index")) not in [TYPE_INT,TYPE_FLOAT] \
				or page.get("text_index") != index or not page.get("text") is String \
				or page["text"].is_empty() or page["text"].length() > 127:
			return false
	return true


func open_dialogue() -> bool:
	if not visible or not FileAccess.file_exists(DIALOGUE):
		return false
	var catalog := validated_dialogue_text(FileAccess.get_file_as_string(DIALOGUE))
	if catalog.is_empty():
		return false
	dialogue_pages = catalog["pages"].duplicate(true)
	dialogue_index = 0
	canvas.dragging = false
	_refresh_dialogue()
	dialogue_panel.visible = true
	_layout_dialogue()
	dialogue_close.grab_focus()
	return true


static func validated_dialogue_text(raw: String) -> Dictionary:
	# Git may check UTF-8 JSON out with CRLF on Windows; pin the original LF text.
	if raw.replace("\r\n","\n").sha256_text() != DIALOGUE_SHA256:
		return {}
	var catalog = JSON.parse_string(raw)
	return catalog if valid_dialogue(catalog) else {}


func _refresh_dialogue() -> void:
	dialogue_text.text = dialogue_pages[dialogue_index]["text"]
	dialogue_position.text = "%d / %d" % [dialogue_index+1,dialogue_pages.size()]
	dialogue_previous.disabled = dialogue_index == 0
	dialogue_next.disabled = dialogue_index == dialogue_pages.size()-1


func _turn_dialogue(delta: int) -> void:
	if not dialogue_panel.visible:
		return
	dialogue_index = clampi(dialogue_index+delta,0,dialogue_pages.size()-1)
	_refresh_dialogue()


func close_dialogue() -> void:
	dialogue_panel.visible = false
	dialogue_pages.clear()
	dialogue_index = 0
	if visible:
		dialogue_button.grab_focus()


static func supports(projection: Dictionary) -> bool:
	if not projection.get("supported",false) or not projection.get("ready",false):
		return false
	var prepared = projection.get("prepared",{})
	if not prepared is Dictionary:
		return false
	var rounds = prepared.get("rounds",[])
	if not rounds is Array or rounds.size() != 1 or not rounds[0] is Dictionary:
		return false
	return prepared.get("adventure_id",-1) == 5 and rounds.size() == 1 \
		and rounds[0].get("scene_id",-1) == 5


func open_preview(projection: Dictionary) -> bool:
	if not supports(projection):
		return false
	if not FileAccess.file_exists(CATALOG) or not FileAccess.file_exists(ATLAS):
		return false
	var catalog = JSON.parse_string(FileAccess.get_file_as_string(CATALOG))
	if not catalog is Dictionary or catalog.get("scene_id",-1) != 5 or catalog.get("atlas","") != ATLAS \
		or not catalog.get("pixel_size",[]) is Array or catalog.get("pixel_size",[]).size() != 2 \
		or FileAccess.get_sha256(ATLAS) != catalog.get("atlas_file_sha256",""):
		return false
	if int(catalog["pixel_size"][0]) != 2048 or int(catalog["pixel_size"][1]) != 1536:
		return false
	var image := Image.load_from_file(ATLAS)
	if image == null or image.get_size() != Vector2i(2048,1536):
		return false
	canvas.texture = ImageTexture.create_from_image(image)
	close_dialogue()
	canvas.dragging = false
	canvas.fit_map()
	visible = true
	close_button.grab_focus()
	return true


func close_preview() -> void:
	close_dialogue()
	canvas.dragging = false
	visible = false
	closed.emit()


func _unhandled_key_input(event: InputEvent) -> void:
	if not visible or not event is InputEventKey or not event.pressed or event.echo:
		return
	if event.keycode == KEY_ESCAPE:
		if dialogue_panel.visible:
			close_dialogue()
		else:
			close_preview()
	else:
		return
	get_viewport().set_input_as_handled()


func _input(event: InputEvent) -> void:
	# Handle paging before focused buttons consume arrow keys for GUI navigation.
	if visible and dialogue_panel.visible and event is InputEventKey and event.pressed \
			and not event.echo and event.keycode in [KEY_RIGHT,KEY_LEFT]:
		_turn_dialogue(1 if event.keycode == KEY_RIGHT else -1)
		get_viewport().set_input_as_handled()


static func _button(caption: String, action: Callable) -> Button:
	var button := Button.new()
	button.text = caption
	button.custom_minimum_size = Vector2(44,38)
	button.pressed.connect(action)
	return button
