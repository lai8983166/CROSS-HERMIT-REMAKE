extends Node2D
## 战斗模拟器视图 (add-unit-render) — 地图三层底图 + 实时战斗层
## 数据: data/map01.json + terrain_palette.json + battle_setup.json (全部可魔改)

const MARGIN := 8.0
const OBJECT_OUTLINE := Color(1.0, 0.85, 0.2, 0.9)
const FACTION_COLOR := [Color(0.85, 0.25, 0.2), Color(0.25, 0.45, 0.9)]
const LOGIC_STEP := 1.0 / 30.0

var map: SimMapData
var palette: Dictionary = {}
var origin := Vector2.ZERO
var view_scale := 1.0

var battle: Battle
var hover := Vector2i(-1, -1)
var locked_cell := Vector2i(-1, -1)
var selected: BattleUnit = null
var _accum := 0.0
var _map_tex: Texture2D = null            # 烘焙的静态地图纹理
var _world_min := Vector2.ZERO
var _world_size := Vector2.ZERO


## 静态地图画家 (烘进 SubViewport 一次性成像, _draw 每帧只贴纹理)
class MapPainter:
	extends Node2D
	var map: SimMapData
	var palette: Dictionary
	var offset := Vector2.ZERO   # 世界坐标 → 视口坐标

	func _draw() -> void:
		for y in map.cell_h:
			for x in map.cell_w:
				var t: int = map.layer_value("terrain", x, y)
				var v: int = map.layer_value("variant", x, y)
				var col: Color = palette.get(t, Color(0.35, 0.1, 0.35))
				if v != 0:
					col = col.lightened(clampf(v * 0.02, -0.3, 0.3))
				var center: Vector2 = map.cell_to_world(x, y) - offset
				var pts := PackedVector2Array([
					center + Vector2(0, -8), center + Vector2(16, 0),
					center + Vector2(0, 8), center + Vector2(-16, 0)])
				if t != 0 or v != 0:
					draw_colored_polygon(pts, col)
				if map.layer_value("object", x, y) != 0:
					draw_polyline(pts + PackedVector2Array([pts[0]]), Color(1.0, 0.85, 0.2, 0.9), 1.5)


func _ready() -> void:
	Engine.time_scale = 1.0
	map = SimMapData.load_map("01")
	_load_palette()
	if map.cell_w > 0:
		_fit_view()
	_start_battle(0)
	queue_redraw()


func _start_battle(seed: int) -> void:
	var setup: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var use_seed: int = setup.get("seed", 42) if seed == 0 else seed
	battle = Battle.start(setup, use_seed)
	selected = null
	_accum = 0.0


func _load_palette() -> void:
	var parsed: Variant = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/terrain_palette.json"))
	if parsed is Dictionary:
		for k: String in parsed.get("colors", {}):
			var rgb: Array = parsed["colors"][k]
			palette[int(k)] = Color8(int(rgb[0]), int(rgb[1]), int(rgb[2]))


func _fit_view() -> void:
	var min_x: float = (0 - (map.cell_h - 1)) * 16.0 - 16.0
	var max_x: float = (map.cell_w - 1) * 16.0 + 16.0
	var min_y: float = -8.0
	var max_y: float = (map.cell_w + map.cell_h - 2) * 8.0 + 8.0
	view_scale = min((1024.0 - MARGIN * 2) / (max_x - min_x),
			(768.0 - MARGIN * 2 - 24.0) / (max_y - min_y))
	origin = Vector2(MARGIN - min_x * view_scale, MARGIN + 24.0 - min_y * view_scale)
	_world_min = Vector2(min_x, min_y)
	_world_size = Vector2(max_x - min_x, max_y - min_y)
	_bake_map()


func _bake_map() -> void:
	var vp := SubViewport.new()
	vp.size = Vector2i(ceili(_world_size.x), ceili(_world_size.y))
	vp.transparent_bg = true
	vp.render_target_update_mode = SubViewport.UPDATE_ONCE
	var painter := MapPainter.new()
	painter.map = map
	painter.palette = palette
	painter.offset = _world_min
	vp.add_child(painter)
	add_child(vp)
	painter.queue_redraw()
	await RenderingServer.frame_post_draw
	_map_tex = vp.get_texture()
	queue_redraw()


func _physics_process(delta: float) -> void:
	if battle == null or battle.finished:
		return
	_accum += delta * Engine.time_scale
	while _accum >= LOGIC_STEP:
		battle.tick()
		_accum -= LOGIC_STEP
		if battle.finished:
			break
	queue_redraw()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		hover = _cell_at(event.position)
		queue_redraw()
	elif event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var c := _cell_at(event.position)
		locked_cell = c
		selected = _unit_at(c)
		queue_redraw()
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_1: Engine.time_scale = 1.0
			KEY_2: Engine.time_scale = 2.0
			KEY_3: Engine.time_scale = 3.0
			KEY_R: _start_battle(int(Time.get_ticks_msec()) % 100000)
			KEY_SPACE: Engine.time_scale = 0.0 if Engine.time_scale > 0 else 1.0


func _cell_at(screen: Vector2) -> Vector2i:
	if view_scale <= 0:
		return Vector2i(-1, -1)
	return map.world_to_cell((screen - origin) / view_scale)


func _unit_at(c: Vector2i) -> BattleUnit:
	if battle == null:
		return null
	for u in battle.units:
		if u.cell == c and u.state != BattleUnit.State.DEAD:
			return u
	return null


func _draw() -> void:
	if map.cell_w == 0:
		draw_string(ThemeDB.fallback_font, Vector2(16, 40),
			"map01.json 缺失 (先跑 python tools/map_export.py 01)",
			HORIZONTAL_ALIGNMENT_LEFT, -1, 14, Color.ORANGE_RED)
		return
	_draw_map()
	_draw_units()
	_draw_hud()


func _draw_map() -> void:
	if _map_tex != null:
		draw_set_transform(origin, 0.0, Vector2(view_scale, view_scale))
		draw_texture_rect(_map_tex, Rect2(_world_min, _world_size), false)
		draw_set_transform(Vector2.ZERO)
		return
	# 烘焙未完成的首帧兜底: 直接绘制 (静态一次)
	draw_set_transform(origin, 0.0, Vector2(view_scale, view_scale))
	for y in map.cell_h:
		for x in map.cell_w:
			var t: int = map.layer_value("terrain", x, y)
			var v: int = map.layer_value("variant", x, y)
			var col: Color = palette.get(t, Color(0.35, 0.1, 0.35))
			if v != 0:
				col = col.lightened(clampf(v * 0.02, -0.3, 0.3))
			var center: Vector2 = map.cell_to_world(x, y)
			var pts := PackedVector2Array([
				center + Vector2(0, -8), center + Vector2(16, 0),
				center + Vector2(0, 8), center + Vector2(-16, 0),
			])
			if t != 0 or v != 0:
				draw_colored_polygon(pts, col)
			if map.layer_value("object", x, y) != 0:
				draw_polyline(pts + PackedVector2Array([pts[0]]), OBJECT_OUTLINE, 1.5)
	draw_set_transform(Vector2.ZERO)


func _screen_pos(c: Vector2i) -> Vector2:
	return origin + map.cell_to_world(c.x, c.y) * view_scale


func _draw_units() -> void:
	if battle == null:
		return
	var r := maxf(6.0, 10.0 * view_scale)
	for u in battle.units:
		var p := _screen_pos(u.cell)
		var col: Color = FACTION_COLOR[u.faction]
		match u.state:
			BattleUnit.State.DEAD:
				col = Color(0.25, 0.25, 0.25, 0.8)
			BattleUnit.State.WITHDRAWN:
				col.a = 0.3
		draw_colored_polygon(PackedVector2Array([
			p + Vector2(0, -r * 0.6), p + Vector2(r * 0.7, 0),
			p + Vector2(0, r * 0.6), p + Vector2(-r * 0.7, 0)]), col)
		if u.state != BattleUnit.State.DEAD:
			# 头顶双条: HP 红 / ENGAGE 蓝 (屏幕空间, 不吃地图形变)
			var bw := 26.0
			var top := p - Vector2(bw * 0.5, r + 10)
			draw_rect(Rect2(top, Vector2(bw, 3)), Color.BLACK)
			draw_rect(Rect2(top, Vector2(bw * u.hp / maxi(u.hp_max, 1), 3)), Color(0.9, 0.2, 0.15))
			draw_rect(Rect2(top + Vector2(0, 4), Vector2(bw, 2)), Color.BLACK)
			draw_rect(Rect2(top + Vector2(0, 4),
					Vector2(bw * clampf(u.engage_left / 36000.0, 0, 1), 2)), Color(0.25, 0.55, 0.95))
		if selected == u:
			draw_arc(p, r + 4, 0, TAU, 24, Color.YELLOW, 1.5)


func _draw_hud() -> void:
	var font := ThemeDB.fallback_font
	var battle_state := "进行中"
	if battle.finished:
		battle_state = ("平局" if battle.winner < 0
				else "%s方胜利" % ("红" if battle.winner == 0 else "蓝"))
	var line1 := "CROSS HERMIT 战斗模拟器 — MAP01 %d×%d | %s (帧 %d) | 速度 %.1f× FPS %d" % [
		map.cell_w, map.cell_h, battle_state, battle.frame if battle else 0,
		Engine.time_scale, Engine.get_frames_per_second()]
	draw_string(font, Vector2(16, 20), line1, HORIZONTAL_ALIGNMENT_LEFT, -1, 13)
	# 悬停/锁定格三层值 (add-map-data 既有行为)
	for pair in [["悬停", hover], ["锁定", locked_cell]]:
		var label: String = pair[0]
		var c: Vector2i = pair[1]
		if c.x >= 0 and map.layer_value("terrain", c.x, c.y) >= 0:
			var txt := "%s (%d,%d) terrain=%d variant=%d object=%d" % [label, c.x, c.y,
				map.layer_value("terrain", c.x, c.y),
				map.layer_value("variant", c.x, c.y),
				map.layer_value("object", c.x, c.y)]
			draw_string(font, Vector2(16, 40 if label == "悬停" else 58), txt,
				HORIZONTAL_ALIGNMENT_LEFT, -1, 13,
				Color(1, 0.85, 0.2) if label == "锁定" else Color.WHITE)
	# 选中单位摘要
	if selected != null:
		var s := "单位 %s [%s] 职业%d Lv%d  HP %d/%d  MP %d/%d  ENGAGE %ds  %s" % [
			selected.name, "红" if selected.faction == 0 else "蓝",
			selected.unit.job_id, selected.unit.level,
			selected.hp, selected.hp_max, selected.mp, selected.mp_max,
			int(selected.engage_left), BattleUnit.State.keys()[selected.state]]
		draw_string(font, Vector2(16, 78), s, HORIZONTAL_ALIGNMENT_LEFT, -1, 13, Color(0.4, 1.0, 0.6))
	draw_string(font, Vector2(16, 758),
		"[1/2/3]速度 [空格]暂停 [R]重开(新种子) 点击=选单位/锁格 悬停=实时 | 阵容改 data/battle_setup.json",
		HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color(0.7, 0.7, 0.7))
