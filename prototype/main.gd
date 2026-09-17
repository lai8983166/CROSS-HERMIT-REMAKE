extends Node2D
## 地图数据视图 (add-map-data) — MAP01 三层逻辑数据占位渲染 + 悬停/点击回显
## 数据: data/map01.json (tools/map_export.py) + data/terrain_palette.json (可魔改)
## 后续: 寻路/单位/原版纹理贴图 (openspec change 逐个替换)

const MARGIN := 8.0
const OBJECT_OUTLINE := Color(1.0, 0.85, 0.2, 0.9)

var map: SimMapData
var palette: Dictionary = {}
var origin := Vector2.ZERO      # 局部坐标 → 屏幕
var view_scale := 1.0

var hover := Vector2i(-1, -1)
var locked := Vector2i(-1, -1)


func _ready() -> void:
	Engine.time_scale = 1.0
	map = SimMapData.load_map("01")
	_load_palette()
	if map.cell_w > 0:
		_fit_view()
	queue_redraw()


func _load_palette() -> void:
	var parsed: Variant = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/terrain_palette.json"))
	if parsed is Dictionary:
		for k: String in parsed.get("colors", {}):
			var rgb: Array = parsed["colors"][k]
			palette[int(k)] = Color8(int(rgb[0]), int(rgb[1]), int(rgb[2]))


## 世界包围盒 → 缩放与原点 (任意地图自适应, 不写死 MAP01)
func _fit_view() -> void:
	var min_x: float = (0 - (map.cell_h - 1)) * 16.0 - 16.0
	var max_x: float = (map.cell_w - 1) * 16.0 + 16.0
	var min_y: float = -8.0
	var max_y: float = (map.cell_w + map.cell_h - 2) * 8.0 + 8.0
	view_scale = min((1024.0 - MARGIN * 2) / (max_x - min_x),
			(768.0 - MARGIN * 2 - 24.0) / (max_y - min_y))
	origin = Vector2(MARGIN - min_x * view_scale, MARGIN + 24.0 - min_y * view_scale)


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		hover = _cell_at(event.position)
		queue_redraw()
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var c := _cell_at(event.position)
		if c != hover or locked != c:
			locked = c
			queue_redraw()
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_1: Engine.time_scale = 1.0
			KEY_2: Engine.time_scale = 2.0
			KEY_3: Engine.time_scale = 3.0


func _cell_at(screen: Vector2) -> Vector2i:
	if view_scale <= 0:
		return Vector2i(-1, -1)
	return map.world_to_cell((screen - origin) / view_scale)


func _draw() -> void:
	if map.cell_w == 0:
		draw_string(ThemeDB.fallback_font, Vector2(16, 40),
			"map01.json 缺失 (先跑 python tools/map_export.py 01)",
			HORIZONTAL_ALIGNMENT_LEFT, -1, 14, Color.ORANGE_RED)
		return
	draw_set_transform(origin, 0.0, Vector2(view_scale, view_scale))
	for y in map.cell_h:
		for x in map.cell_w:
			var t: int = map.layer_value("terrain", x, y)
			var v: int = map.layer_value("variant", x, y)
			var o: int = map.layer_value("object", x, y)
			var col: Color = palette.get(t, Color(0.35, 0.1, 0.35))
			if v != 0:   # 变体 → 明度微调 (占位语义)
				col = col.lightened(clampf(v * 0.02, -0.3, 0.3))
			var center: Vector2 = map.cell_to_world(x, y)
			var pts := PackedVector2Array([
				center + Vector2(0, -8), center + Vector2(16, 0),
				center + Vector2(0, 8), center + Vector2(-16, 0),
			])
			if t != 0 or v != 0:
				draw_colored_polygon(pts, col)
			if o != 0:
				draw_polyline(pts + PackedVector2Array([pts[0]]), OBJECT_OUTLINE, 1.5)
	draw_set_transform(Vector2.ZERO)
	_draw_hud()


func _draw_hud() -> void:
	var font := ThemeDB.fallback_font
	var line1 := "CROSS HERMIT 地图数据视图 — MAP01 %d×%d 格  缩放 %.2f  速度 %.1f×  FPS %d" % [
		map.cell_w, map.cell_h, view_scale, Engine.time_scale,
		Engine.get_frames_per_second()]
	draw_string(font, Vector2(16, 20), line1, HORIZONTAL_ALIGNMENT_LEFT, -1, 13)
	# 悬停/锁定格三层值回显
	for pair in [["悬停", hover], ["锁定", locked]]:
		var label: String = pair[0]
		var c: Vector2i = pair[1]
		if c.x < 0 or map.layer_value("terrain", c.x, c.y) < 0:
			continue
		var txt := "%s (%d,%d)  terrain=%d variant=%d object=%d" % [label, c.x, c.y,
			map.layer_value("terrain", c.x, c.y),
			map.layer_value("variant", c.x, c.y),
			map.layer_value("object", c.x, c.y)]
		draw_string(font, Vector2(16, 40 if label == "悬停" else 58), txt,
			HORIZONTAL_ALIGNMENT_LEFT, -1, 13,
			Color(1, 0.85, 0.2) if label == "锁定" else Color.WHITE)
	draw_string(font, Vector2(16, 758),
		"[1/2/3] 速度档  悬停=实时  点击=锁定  调色板可改 data/terrain_palette.json",
		HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color(0.7, 0.7, 0.7))
