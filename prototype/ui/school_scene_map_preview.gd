extends Control
## Read-only current-map inspection; owns no school or battle state.

signal closed

const CATALOG := "res://assets/current_scene/catalog.json"
const ATLAS := "res://assets/current_scene/map05.png"

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
	var footer := Label.new()
	footer.text = "拖动查看 · 滚轮缩放 · Esc 返回    |    地图预览，战斗暂未开放"
	footer.add_theme_font_size_override("font_size",14)
	column.add_child(footer)
	visible = false


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
	canvas.dragging = false
	canvas.fit_map()
	visible = true
	close_button.grab_focus()
	return true


func close_preview() -> void:
	canvas.dragging = false
	visible = false
	closed.emit()


func _unhandled_key_input(event: InputEvent) -> void:
	if visible and event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE:
		close_preview()
		get_viewport().set_input_as_handled()


static func _button(caption: String, action: Callable) -> Button:
	var button := Button.new()
	button.text = caption
	button.custom_minimum_size = Vector2(44,38)
	button.pressed.connect(action)
	return button
