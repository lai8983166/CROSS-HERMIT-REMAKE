extends Control
## Current-school movement trial, with no persistent battle result authority.
signal closed
const Field := preload("res://sim/school_field_session.gd")
const MapPreview := preload("res://ui/school_scene_map_preview.gd")
const ART := "res://assets/school_field/"

class FieldCanvas extends MapPreview.MapCanvas:
	signal chosen(identity: int)
	signal commanded(cell: Vector2i)
	var session: Field
	var sprites: Dictionary = {}
	var show_terrain := false
	var hover := Vector2i(-1,-1)

	func point(cell: Vector2i) -> Vector2:
		return origin+(Vector2(cell)*Vector2(32,16)+Vector2(16,8))*zoom

	func focus_units() -> void:
		if session == null or not session.ready: return
		zoom = 1.25; fit_mode = false
		var center := Vector2.ZERO
		for unit in session.controlled_units(): center += session.position(unit)
		center /= session.controlled_units().size()
		origin = size*0.5-center*zoom; clamp_origin()

	func _gui_input(event: InputEvent) -> void:
		if session == null or not session.ready: return
		if event is InputEventMouseButton:
			if event.button_index == MOUSE_BUTTON_MIDDLE:
				dragging = event.pressed; accept_event()
			elif event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
				# Hit visible sprites as well as the selected unit's ground marker.
				var best := -1; var distance := INF
				for unit in session.units:
					if unit["limits"]["hp"] <= 0: continue
					var ground := origin+session.position(unit)*zoom
					var region := Rect2(ground-Vector2(23,100)*zoom,Vector2(46,116)*zoom)
					var current: float = ground.distance_to(event.position)
					if region.has_point(event.position) and current < distance:
						best = session.unit_key(unit); distance = current
				if best >= 0: chosen.emit(best)
				accept_event()
			elif event.pressed and event.button_index == MOUSE_BUTTON_RIGHT:
				commanded.emit(Vector2i(floori((event.position.x-origin.x)/zoom/32),
					floori((event.position.y-origin.y)/zoom/16)))
				accept_event()
			elif event.pressed and event.button_index in [MOUSE_BUTTON_WHEEL_UP,MOUSE_BUTTON_WHEEL_DOWN]:
				zoom_at(1.25 if event.button_index == MOUSE_BUTTON_WHEEL_UP else 0.8,event.position)
				accept_event()
		elif event is InputEventMouseMotion:
			hover = Vector2i(floori((event.position.x-origin.x)/zoom/32),floori((event.position.y-origin.y)/zoom/16))
			if dragging: pan(event.relative); accept_event()
			queue_redraw()

	func _draw() -> void:
		super._draw()
		if session == null or not session.ready: return
		if show_terrain:
			for y in range(96):
				for x in range(64):
					var cell := Vector2i(x,y)
					if not session.walkable(cell) or session._reserved.has(cell):
						draw_rect(Rect2(origin+Vector2(x*32,y*16)*zoom,Vector2(32,16)*zoom),Color(0.8,0.15,0.1,0.3))
		var selected := session.find_unit(session.selected_id)
		if not selected.is_empty():
			var points := PackedVector2Array([origin+session.position(selected)*zoom])
			for cell in selected["path"]: points.append(point(cell))
			if points.size() > 1: draw_polyline(points,Color("e7d288"),2.0,true)
			if selected["destination"].x >= 0:
				draw_rect(Rect2(point(selected["destination"])-Vector2(16,8)*zoom,Vector2(32,16)*zoom),Color("e7d288"),false,2.0)
		if Field._inside(hover):
			draw_rect(Rect2(point(hover)-Vector2(16,8)*zoom,Vector2(32,16)*zoom),Color(1,1,1,0.4),false)
		var ordered: Array = session.units.duplicate()
		ordered.sort_custom(func(a,b): return session.position(a).y < session.position(b).y)
		for unit in ordered:
			if unit.get("dead_at",-1) >= 0 and session.frame-unit["dead_at"] >= 30: continue
			var ground := origin+session.position(unit)*zoom
			draw_set_transform(ground,0,Vector2(1,0.45))
			draw_circle(Vector2.ZERO,13*zoom,Color(0,0,0,0.4))
			if session.unit_key(unit) == session.selected_id:
				draw_arc(Vector2.ZERO,17*zoom,0,TAU,32,Color("ffe38a"),2.0,true)
			draw_set_transform_matrix(Transform2D())
			_draw_student(unit,ground)

	func _draw_student(unit: Dictionary, ground: Vector2) -> void:
		var skin: Dictionary = session.catalog["skins"][unit.get("skin_key",str(unit["character_id"]))]
		var timeline: Dictionary = skin["actions"][unit["visual"]][unit["facing"]]
		var picked := AnimTimeline.step_at(timeline,(session.frame-unit["visual_started_frame"])*2,true)
		if picked.is_empty(): return
		for layer in picked["step"]["layers"]:
			var frame_data: Dictionary = skin["frames"][str(layer["frame"])]
			var image: Texture2D = sprites[frame_data["file"]]
			var rect := AnimTimeline.layer_rect(frame_data,layer)
			# Original layer y already offsets the canvas center to the ground.
			var flip := AnimTimeline.combined_flip(layer,timeline["flags"])
			draw_set_transform_matrix(Transform2D(0,Vector2(-zoom if flip.x else zoom,-zoom if flip.y else zoom),0,ground))
			var alpha := clampf(1.0-(session.frame-unit["dead_at"])/30.0,0,1) if unit.get("dead_at",-1) >= 0 else 1.0
			draw_texture_rect(image,rect,false,Color(1,1,1,alpha))
			draw_set_transform_matrix(Transform2D())


var session = Field.new()
var canvas: FieldCanvas
var close_button: Button
var pause_button: Button
var stop_button: Button
var center_button: Button
var fit_button: Button
var terrain_button: Button
var zoom_in_button: Button
var zoom_out_button: Button
var member_buttons: Dictionary = {}
var roster: HBoxContainer
var info: Label
var status: Label
var title_label: Label
var help_label: Label
var _names: Dictionary = {}
var _sprites: Dictionary = {}


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	z_index = 110; mouse_filter = Control.MOUSE_FILTER_STOP
	var background := ColorRect.new()
	background.color = Color("142426")
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(background)
	var margin := MarginContainer.new()
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	for side in ["left","right","top","bottom"]: margin.add_theme_constant_override("margin_"+side,16)
	add_child(margin)
	var column := VBoxContainer.new()
	column.add_theme_constant_override("separation",8)
	margin.add_child(column)
	var heading := HBoxContainer.new()
	column.add_child(heading)
	var title := Label.new()
	title_label = title
	title.text = "第五周 · 队伍操作试验"
	title.add_theme_font_size_override("font_size",22)
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	heading.add_child(title)
	close_button = _button("返回学校",close_trial); heading.add_child(close_button)
	var tools := HBoxContainer.new(); column.add_child(tools)
	pause_button = _button("暂停",toggle_pause); tools.add_child(pause_button)
	stop_button = _button("停止移动",func(): session.stop(session.selected_id); _refresh()); tools.add_child(stop_button)
	center_button = _button("查看队伍",func(): canvas.focus_units()); tools.add_child(center_button)
	fit_button = _button("显示全图",func(): canvas.fit_map()); tools.add_child(fit_button)
	zoom_out_button = _button("−",func(): canvas.zoom_at(0.8,canvas.size*0.5)); tools.add_child(zoom_out_button)
	zoom_in_button = _button("＋",func(): canvas.zoom_at(1.25,canvas.size*0.5)); tools.add_child(zoom_in_button)
	terrain_button = _button("显示阻挡",func(): canvas.show_terrain = not canvas.show_terrain; _refresh()); tools.add_child(terrain_button)
	canvas = _new_canvas(); canvas.size_flags_vertical = Control.SIZE_EXPAND_FILL
	column.add_child(canvas)
	canvas.resized.connect(func():
		if visible and session.ready: canvas.focus_units())
	canvas.chosen.connect(func(identity): session.select(identity); _refresh())
	canvas.commanded.connect(func(cell):
		var accepted := session.command_move(session.selected_id,cell)
		status.text = "目的格 %d,%d · %s" % [cell.x,cell.y,"已下达移动命令" if accepted else "目标被阻挡、占用或无法到达"]
		_refresh())
	roster = HBoxContainer.new(); roster.add_theme_constant_override("separation",10); column.add_child(roster)
	info = Label.new(); info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	column.add_child(info)
	status = Label.new(); status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	status.add_theme_font_size_override("font_size",14); column.add_child(status)
	var help := Label.new()
	help_label = help
	help.text = "左键选人 · 右键移动 · 中键拖图 · 滚轮缩放 · 空格暂停 · Esc 返回\n移动试验 · 敌人与战斗结算待接"
	help.add_theme_font_size_override("font_size",14)
	column.add_child(help)
	visible = false


func open_trial(preparation: Dictionary, combat: Dictionary, names: Dictionary) -> bool:
	var next = _new_session()
	if not next.open(preparation,combat): return false
	var map_catalog = JSON.parse_string(FileAccess.get_file_as_string(MapPreview.CATALOG))
	if not map_catalog is Dictionary or FileAccess.get_sha256(MapPreview.ATLAS) != map_catalog.get("atlas_file_sha256"):
		return false
	var map_image := Image.load_from_file(MapPreview.ATLAS)
	if map_image == null or map_image.get_size() != Vector2i(2048,1536): return false
	if _sprites.is_empty():
		var images := {}
		for skin in next.catalog["skins"].values():
			for frame_data in skin["frames"].values():
				var path: String = frame_data["file"] if String(frame_data["file"]).begins_with("res://") else ART+frame_data["file"]
				if FileAccess.get_sha256(path) != frame_data["file_sha256"]: return false
				var image := Image.load_from_file(path)
				if image == null or image.get_size() != Vector2i(frame_data["w"],frame_data["h"]): return false
				images[frame_data["file"]] = ImageTexture.create_from_image(image)
		_sprites = images
	session = next; canvas.session = next; canvas.sprites = _sprites
	canvas.texture = ImageTexture.create_from_image(map_image)
	canvas.dragging = false; canvas.show_terrain = false; canvas.hover = Vector2i(-1,-1)
	_names = names.duplicate(true)
	for child in roster.get_children(): roster.remove_child(child); child.queue_free()
	member_buttons.clear()
	for unit in session.controlled_units():
		var identity: int = unit["character_id"]
		var button := _button("",func(): session.select(identity); _refresh())
		button.toggle_mode = true; button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		button.custom_minimum_size.y = 54; roster.add_child(button)
		member_buttons[identity] = button
	status.text = "选择学生，在地图上右键指定目的格。"
	visible = true; canvas.focus_units(); canvas.call_deferred("focus_units")
	_refresh(); close_button.grab_focus()
	return true


func _refresh() -> void:
	if not session.ready: return
	pause_button.text = "继续" if session.paused else "暂停"
	terrain_button.text = "隐藏阻挡" if canvas.show_terrain else "显示阻挡"
	for unit in session.controlled_units():
		var identity: int = unit["character_id"]
		var limits: Dictionary = unit["limits"]
		member_buttons[identity].text = "%s\nHP %d/%d · MP %d/%d" % [_names.get(identity,str(identity)),limits["hp"],limits["hp_max"],limits["mp"],limits["mp_max"]]
		member_buttons[identity].set_pressed_no_signal(identity == session.selected_id)
	var selected: Dictionary = session.find_unit(session.selected_id)
	info.text = "%s · 格 %d,%d · %s    |    班级领队：%s" % [_names.get(session.selected_id,str(session.selected_id)),
		selected["cell"].x,selected["cell"].y,"已暂停" if session.paused else "移动中" if not selected["path"].is_empty() else "待命",_names.get(101,"101")]
	canvas.queue_redraw()


func _new_session():
	return Field.new()


func _new_canvas() -> FieldCanvas:
	return FieldCanvas.new()


func _process(delta: float) -> void:
	if visible and session.ready:
		session.advance(delta); _refresh()


func toggle_pause() -> void:
	if not session.ready: return
	session.paused = not session.paused; _refresh()


func close_trial() -> void:
	canvas.dragging = false; visible = false; session.close(); closed.emit()


func _input(event: InputEvent) -> void:
	if not visible or not event is InputEventKey or not event.pressed or event.echo: return
	if event.keycode == KEY_ESCAPE: close_trial()
	elif event.keycode == KEY_SPACE: toggle_pause()
	elif event.keycode == KEY_S: session.stop(session.selected_id); _refresh()
	else: return
	get_viewport().set_input_as_handled()


static func _button(text: String, action: Callable) -> Button:
	var button := Button.new(); button.text = text
	button.custom_minimum_size = Vector2(44,36); button.pressed.connect(action)
	return button
