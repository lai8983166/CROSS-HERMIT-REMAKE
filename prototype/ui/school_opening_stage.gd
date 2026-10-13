extends Control
## Read-only source layer projection. The local visual clock does not run a battle VM.

const CATALOG := "res://assets/school_opening/catalog.json"
const DIRECTORY := "res://assets/school_opening/"
const CATALOG_SHA := "9d19edc6ceb0ba650ef5f60c21112f6bbff8bec58d4492d9862f12b830768d4d"

class LayerCanvas extends Control:

	var config: Dictionary
	var actor: Dictionary
	var atlas: Texture2D
	var portrait: Texture2D
	var frame_alpha := 1.0
	var actor_alpha := 1.0
	var fill_alpha := 0.8

	func _draw() -> void:
		var fill: Array = config["fill_rect"]
		draw_rect(Rect2(fill[0],fill[1],fill[2],fill[3]),Color(34.0/255,52.0/255,56.0/255,fill_alpha))
		var origin: Array = config["frame_origin"]
		for r in config["pieces"]:
			draw_texture_rect_region(atlas,Rect2(origin[0]+r[0],origin[1]+r[1],r[4],r[5]),Rect2(r[2],r[3],r[4],r[5]),Color(1,1,1,frame_alpha))
		if portrait != null:
			var point: Array = config["actor_origin"]
			for rect in [actor["body_rect"],actor["face_rect"]]:
				draw_texture_rect_region(portrait,Rect2(point[0],point[1],rect[2],rect[3]),Rect2(rect[0],rect[1],rect[2],rect[3]),Color(1,1,1,actor_alpha))


var catalog: Dictionary = {}
var textures: Dictionary = {}
var logical: Control
var layers: Array = []
var current_text: Label
var page_index := 0
var age_ticks := 0
var _fraction := 0.0
var ready_ticks := 24
var stage_scale := 1.0


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	logical = Control.new()
	logical.mouse_filter = Control.MOUSE_FILTER_IGNORE
	logical.size = Vector2(1024,768)
	add_child(logical)
	resized.connect(_fit)


func load_presentation() -> bool:
	if not FileAccess.file_exists(CATALOG):
		return false
	var raw := FileAccess.get_file_as_string(CATALOG).replace("\r\n","\n")
	if raw.sha256_text() != CATALOG_SHA:
		return false
	var data = JSON.parse_string(raw)
	if not data is Dictionary or data.get("mode") != "read_only_graphical_opening" \
			or int(data["logical_size"][0]) != 1024 or int(data["logical_size"][1]) != 768 or data.get("pages",[]).size() != 10:
		return false
	var loaded := {}
	for filename in data["outputs"]:
		var path: String = DIRECTORY+filename
		if not FileAccess.file_exists(path) or FileAccess.get_sha256(path) != data["outputs"][filename]["sha256"]:
			return false
		var image := Image.load_from_file(path)
		if image == null or image.get_width() != int(data["outputs"][filename]["size"][0]) or image.get_height() != int(data["outputs"][filename]["size"][1]):
			return false
		loaded[filename] = ImageTexture.create_from_image(image)
	catalog = data
	textures = loaded
	return true


func show_page(index: int) -> void:
	if catalog.is_empty() or index < 0 or index >= 10:
		return
	for layer in layers:
		logical.remove_child(layer["canvas"])
		layer["canvas"].queue_free()
	layers.clear()
	page_index = index
	age_ticks = 0
	_fraction = 0.0
	var page: Dictionary = catalog["pages"][index]
	var new_actor := index in [2,4]
	ready_ticks = 104 if new_actor else (73 if index == 0 else 25)
	for bank in page["layers"]:
		var config: Dictionary = catalog["configs"][str(int(bank["config"]))]
		var paint := LayerCanvas.new()
		paint.config = config
		paint.atlas = textures["gybc_00.png"]
		paint.mouse_filter = Control.MOUSE_FILTER_IGNORE
		paint.size = Vector2(1024,768)
		logical.add_child(paint)
		var name: Label
		if bank["actor"] != 0:
			paint.actor = catalog["actors"][str(int(bank["actor"]))]
			paint.portrait = textures[paint.actor["filename"].to_lower().replace(".bin",".png")]
			name = _label(paint.actor["name"],20)
			name.position = Vector2(config["name_origin"][0]-100,config["name_origin"][1]-15)
			name.size = Vector2(200,30)
			name.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			name.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
			paint.add_child(name)
		var column := VBoxContainer.new()
		column.mouse_filter = Control.MOUSE_FILTER_IGNORE
		column.add_theme_constant_override("separation",0)
		column.position = Vector2(config["text_origin"][0],config["text_origin"][1])
		column.size = Vector2(config["text_width"],110)
		paint.add_child(column)
		var records: Array = []
		for text_index in bank["text_indices"]:
			var label := _label(catalog["pages"][int(text_index)]["text"],21)
			label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
			label.custom_minimum_size.y = 26
			column.add_child(label)
			records.append({"label":label,"current":text_index == index})
			if text_index == index:
				current_text = label
		layers.append({"canvas":paint,"name":name,"records":records,"entering":new_actor and bank["config"] == page["config"],"initial":index == 0})
	_refresh()
	_fit()


static func _label(text: String, font_size: int) -> Label:
	var label := Label.new()
	label.text = text
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	label.add_theme_font_size_override("font_size",font_size)
	label.add_theme_color_override("font_color",Color("f6f1e7"))
	label.add_theme_color_override("font_outline_color",Color("080808"))
	label.add_theme_constant_override("outline_size",2)
	return label


func advance_ticks(count: int) -> void:
	age_ticks = mini(ready_ticks,age_ticks+maxi(0,count))
	_refresh()


func finish_display() -> void:
	advance_ticks(ready_ticks)


func display_ready() -> bool:
	return age_ticks >= ready_ticks


func _process(delta: float) -> void:
	if not is_visible_in_tree() or catalog.is_empty() or display_ready():
		return
	_fraction += minf(delta,0.2)*60.0
	var ticks := int(_fraction)
	_fraction -= ticks
	if ticks > 0:
		advance_ticks(ticks)


func _refresh() -> void:
	for layer in layers:
		var paint: LayerCanvas = layer["canvas"]
		paint.actor_alpha = _opacity(age_ticks,60,255) if layer["entering"] else 1.0
		var frame_count := maxi(0,age_ticks-31) if layer["entering"] else age_ticks
		paint.frame_alpha = _opacity(frame_count,45,255) if layer["entering"] or layer["initial"] else 1.0
		paint.fill_alpha = _opacity(frame_count,45,204) if layer["entering"] or layer["initial"] else 204.0/255
		if layer["name"] != null:
			layer["name"].visible = not layer["entering"] or age_ticks >= 77
		var start := 78 if layer["entering"] else (48 if layer["initial"] else 0)
		for record in layer["records"]:
			record["label"].modulate.a = _opacity(maxi(0,age_ticks-start),24,255) if record["current"] else 1.0
		paint.queue_redraw()


static func _opacity(count: int, limit: int, maximum: int) -> float:
	return mini(int(count*maximum/float(limit)),maximum)/255.0


func _fit() -> void:
	if logical == null:
		return
	stage_scale = minf(size.x/1024.0,size.y/768.0)
	logical.scale = Vector2.ONE*stage_scale
	logical.position = (size-Vector2(1024,768)*stage_scale)*0.5
