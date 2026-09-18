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
var _atlas: Texture2D = null      # 原版纹理图集 (assets/map01_atlas.png, 可缺)
var _base_mode := 0               # 0=纯贴图 1=贴图+数据叠加 2=纯数据 (T 循环)
const OVERLAY_ALPHA := 0.45       # 叠加态数据层透明度 (design 决策 4)
var hover := Vector2i(-1, -1)
var locked_cell := Vector2i(-1, -1)
var selected: BattleUnit = null
var _accum := 0.0
var _panning := false
var _map_tex: Texture2D = null            # 烘焙的静态地图纹理
var _world_min := Vector2.ZERO
var _world_size := Vector2.ZERO
# 单位精灵 (add-unit-sprites): unit_sprites.json 缺失/条目缺 → 色块回退, 功能不损
var _unit_sprites: Dictionary = {}
var _sprites_meta: Dictionary = {}
var _tex_cache: Dictionary = {}


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
				# 直角格: (x,y) = 像素矩形 [32x,16y,32,16] (add-map-composition 定案)
				var rect := Rect2(map.cell_to_world(x, y) - offset
						- Vector2(SimMapData.CELL_W, SimMapData.CELL_H) * 0.5,
						Vector2(SimMapData.CELL_W, SimMapData.CELL_H))
				if t != 0 or v != 0:
					draw_rect(rect, col)
				if map.layer_value("object", x, y) != 0:
					draw_rect(rect, Color(1.0, 0.85, 0.2, 0.9), false, 1.5)


func _ready() -> void:
	Engine.time_scale = 1.0
	map = SimMapData.load_map("01")
	_load_palette()
	_load_unit_sprites()
	if FileAccess.file_exists("res://assets/map01_composed.png"):
		_atlas = load("res://assets/map01_composed.png")   # 直角世界图 (add-map-composition)
		_base_mode = 0
	else:
		_base_mode = 2   # 无贴图回退数据视图
	if map.cell_w > 0:
		_fit_view()
	_start_battle(0)
	queue_redraw()


func _start_battle(seed: int) -> void:
	var setup: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var use_seed: int = setup.get("seed", 42) if seed == 0 else seed
	battle = Battle.start(setup, use_seed, map)
	selected = null
	_accum = 0.0


func _load_palette() -> void:
	var parsed: Variant = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/terrain_palette.json"))
	if parsed is Dictionary:
		for k: String in parsed.get("colors", {}):
			var rgb: Array = parsed["colors"][k]
			palette[int(k)] = Color8(int(rgb[0]), int(rgb[1]), int(rgb[2]))


func _load_unit_sprites() -> void:
	if not FileAccess.file_exists("res://data/unit_sprites.json"):
		return   # 无帧表 → _draw_units 走色块回退
	var parsed: Variant = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/unit_sprites.json"))
	if parsed is Dictionary and parsed.get("units") is Dictionary:
		_unit_sprites = parsed["units"]
		_sprites_meta = parsed.get("_meta", {})


func _fit_view() -> void:
	# 直角投影 (add-map-composition): 世界 = [0,0,px_w,px_h] == 图集尺寸
	# 默认视口 = composed 元数据里的实机验证窗口 (没有则全图)
	var min_x: float = 0.0
	var min_y: float = 0.0
	var max_x: float = map.cell_w * 32.0
	var max_y: float = map.cell_h * 16.0
	var win: Dictionary = _composed_window()
	if not win.is_empty():
		min_x = float(win.x)
		min_y = float(win.y)
		max_x = min_x + float(win.w)
		max_y = min_y + float(win.h)
	view_scale = min((1024.0 - MARGIN * 2) / (max_x - min_x),
			(768.0 - MARGIN * 2 - 24.0) / (max_y - min_y))
	origin = Vector2(MARGIN - min_x * view_scale, MARGIN + 24.0 - min_y * view_scale)
	_world_min = Vector2(0.0, 0.0)
	_world_size = Vector2(map.cell_w * 32.0, map.cell_h * 16.0)
	_bake_map()


## composed 元数据的实机验证窗口 (map_window_match: 屏幕≈图集该窗口×1.02 平移)
func _composed_window() -> Dictionary:
	if not FileAccess.file_exists("res://assets/map01_composed.png.json"):
		return {}
	var parsed: Variant = JSON.parse_string(
		FileAccess.get_file_as_string("res://assets/map01_composed.png.json"))
	if parsed is Dictionary and parsed.get("verified_window") is Dictionary:
		return parsed["verified_window"]
	return {}


func _fit_full_map() -> void:
	# F 键: 回到全图视野
	var max_x: float = map.cell_w * 32.0
	var max_y: float = map.cell_h * 16.0
	view_scale = min((1024.0 - MARGIN * 2) / max_x, (768.0 - MARGIN * 2 - 24.0) / max_y)
	origin = Vector2(MARGIN, MARGIN + 24.0)
	queue_redraw()


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
		if _panning:
			# 拖拽平移: 世界偏移 = -屏幕位移/缩放
			origin += event.relative
			queue_redraw()
		else:
			queue_redraw()
	elif event is InputEventMouseButton:
		if event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
			var c := _cell_at(event.position)
			locked_cell = c
			selected = _unit_at(c)
			queue_redraw()
		elif event.pressed and event.button_index == MOUSE_BUTTON_MIDDLE:
			_panning = true
		elif not event.pressed and event.button_index == MOUSE_BUTTON_MIDDLE:
			_panning = false
		elif event.pressed and (event.button_index == MOUSE_BUTTON_WHEEL_UP
				or event.button_index == MOUSE_BUTTON_WHEEL_DOWN):
			_zoom_at(event.position, 1.25 if event.button_index == MOUSE_BUTTON_WHEEL_UP else 0.8)
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_1: Engine.time_scale = 1.0
			KEY_2: Engine.time_scale = 2.0
			KEY_3: Engine.time_scale = 3.0
			KEY_R: _start_battle(int(Time.get_ticks_msec()) % 100000)
			KEY_SPACE: Engine.time_scale = 0.0 if Engine.time_scale > 0 else 1.0
			KEY_T:
				_base_mode = (_base_mode + 1) % 3
				queue_redraw()
			KEY_F: _fit_view()


## 以屏幕点为中心缩放 (世界点不动)
func _zoom_at(screen: Vector2, factor: float) -> void:
	var world: Vector2 = (screen - origin) / view_scale
	view_scale = clampf(view_scale * factor, 0.15, 6.0)
	origin = screen - world * view_scale
	queue_redraw()


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
	if _base_mode > 0:
		_draw_units()
	_draw_hud()


func _draw_map() -> void:
	if _map_tex == null:
		return   # 烘焙未完成的首帧: 走下方直接绘制兜底
	var world_rect := Rect2(_world_min, _world_size)
	draw_set_transform(origin, 0.0, Vector2(view_scale, view_scale))
	# 直角定案: 世界图 == 图集 (恒等); 默认视口对准实机验证窗口 (compose meta 驱动)
	if _base_mode == 0 and _atlas != null:
		draw_texture_rect(_atlas, world_rect, false)
	elif _base_mode == 1 and _atlas != null:
		draw_texture_rect(_atlas, world_rect, false)
		draw_texture_rect(_map_tex, world_rect, false, Color(1, 1, 1, OVERLAY_ALPHA))
	else:
		draw_texture_rect(_map_tex, world_rect, false)
	draw_set_transform(Vector2.ZERO)
	if _map_tex == null:
		# 烘焙未完成的首帧兜底: 直接绘制 (仅首帧, 有烘焙后不再画 —— 否则会盖住贴图)
		draw_set_transform(origin, 0.0, Vector2(view_scale, view_scale))
		for y in map.cell_h:
			for x in map.cell_w:
				var t: int = map.layer_value("terrain", x, y)
				var v: int = map.layer_value("variant", x, y)
				var col: Color = palette.get(t, Color(0.35, 0.1, 0.35))
				if v != 0:
					col = col.lightened(clampf(v * 0.02, -0.3, 0.3))
				var rect := Rect2(Vector2(x * 32.0, y * 16.0), Vector2(32.0, 16.0))
				if t != 0 or v != 0:
					draw_rect(rect, col)
				if map.layer_value("object", x, y) != 0:
					draw_rect(rect, OBJECT_OUTLINE, false, 1.5)
		draw_set_transform(Vector2.ZERO)


func _screen_pos(c: Vector2i) -> Vector2:
	return origin + map.cell_to_world(c.x, c.y) * view_scale


func _draw_units() -> void:
	if battle == null:
		return
	var r := maxf(6.0, 10.0 * view_scale)
	for i in battle.units.size():
		var u: BattleUnit = battle.units[i]
		var p := origin + _unit_world_pos(u) * view_scale
		# 相位偏移按单位序错开 (同时出发不走齐步)
		var phase: float = battle.frame * Battle.LOGIC_STEP + float(i % 7) * 0.37
		if not _draw_sprite_unit(u, p, phase):
			var col: Color = FACTION_COLOR[u.faction]
			match u.state:
				BattleUnit.State.DEAD:
					col = Color(0.25, 0.25, 0.25, 0.8)
				BattleUnit.State.WITHDRAWN:
					col.a = 0.3
			draw_rect(Rect2(p - Vector2(r * 0.7, r * 0.5), Vector2(r * 1.4, r)), col)
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


## 单位绘制位置: 格间平滑插值 (from_cell → cell, 跨 move_interval 逻辑帧)
func _unit_world_pos(u: BattleUnit) -> Vector2:
	var cur := map.cell_to_world(u.cell.x, u.cell.y)
	if u.from_cell == u.cell or battle == null:
		return cur
	var span: float = maxf(1.0, float(battle.move_interval)) * Battle.LOGIC_STEP
	var t: float = clampf((battle.frame - u.move_started_frame) * Battle.LOGIC_STEP / span, 0.0, 1.0)
	if t >= 1.0:
		return cur
	return map.cell_to_world(u.from_cell.x, u.from_cell.y).lerp(cur, t)


## 精灵绘制 (add-unit-sprites): 状态→anim_map 序列循环, 锚点=画布底中对格心, 脚底椭圆阴影。
## 返回 false = 无帧表/无序列/资产缺失 → 调用方走色块回退。
func _draw_sprite_unit(u: BattleUnit, p_screen: Vector2, phase: float) -> bool:
	if _unit_sprites.is_empty() or u.anim_id.is_empty():
		return false
	var udata: Dictionary = _unit_sprites.get(u.anim_id, {})
	if udata.is_empty():
		return false
	var amap: Dictionary = udata.get("anim_map", {})
	var key := "IDLE"
	match u.state:
		BattleUnit.State.MOVE:
			key = "MOVE"
		BattleUnit.State.ATTACK:
			key = "ATTACK"
		BattleUnit.State.DEAD:
			key = "DEAD"
	var entry: Dictionary = amap.get(key, amap.get("IDLE", {}))
	var anims: Array = udata.get("anims", [])
	var anim_idx := int(entry.get("anim", -1))   # JSON 数字为 float, 统一 int 化
	if entry.is_empty() or anim_idx < 0 or anim_idx >= anims.size():
		return false
	var recs: Array = anims[anim_idx].get("records", [])
	var frames: Array = udata.get("frames", [])
	var dur_s: float = float(_sprites_meta.get("dur_unit_seconds", 1.0 / 60.0))
	var total := 0.0
	for r in recs:
		total += maxf(1.0, float(r.get("dur", 1))) * dur_s
	if total <= 0.0 or frames.is_empty():
		return false
	var phase_t := fposmod(maxf(0.0, phase), total)
	var pick_frame := -1
	for ri in recs.size():
		var r: Dictionary = recs[ri]
		var d := maxf(1.0, float(r.get("dur", 1))) * dur_s
		if phase_t < d or ri == recs.size() - 1:
			pick_frame = int(r.get("frame", -1))
			break
		phase_t -= d
	# 脚底阴影 (43d270 印章语义的椭圆近似)
	draw_set_transform(p_screen, 0.0, Vector2(1.0, 0.45))
	draw_circle(Vector2.ZERO, 9.0 * view_scale, Color(0, 0, 0, 0.35))
	draw_set_transform(Vector2.ZERO)
	if pick_frame < 0 or pick_frame >= frames.size():
		return true   # 空白帧时段: 只画阴影不画本体 (序列本身有效)
	var tex := _frame_tex(u.anim_id, pick_frame)
	if tex == null:
		return false
	var f: Dictionary = frames[pick_frame]
	var anchor: Dictionary = f.get("anchor",
			{"x": float(f.get("w", 0)) * 0.5, "y": float(f.get("h", 0))})
	var flip := bool(entry.get("flip_x_when_facing_right", false)) and u.facing.x > 0
	var mod := Color(1, 1, 1, 0.55) if u.state == BattleUnit.State.WITHDRAWN else Color.WHITE
	var fx := -1.0 if flip else 1.0
	draw_set_transform_matrix(Transform2D(0.0, Vector2(view_scale * fx, view_scale), 0.0, p_screen))
	draw_texture_rect(tex, Rect2(Vector2(-float(anchor.get("x", 0.0)),
			-float(anchor.get("y", 0.0))), Vector2(tex.get_width(), tex.get_height())), false, mod)
	draw_set_transform_matrix(Transform2D())
	return true


func _frame_tex(anim_id: String, frame_idx: int) -> Texture2D:
	var key := "%s/%d" % [anim_id, frame_idx]
	if _tex_cache.has(key):
		return _tex_cache[key]
	var udata: Dictionary = _unit_sprites.get(anim_id, {})
	var frames: Array = udata.get("frames", [])
	if frame_idx < 0 or frame_idx >= frames.size():
		return null
	var path := "res://assets/unit/%s/%s" % [anim_id, frames[frame_idx].get("file", "")]
	if not ResourceLoader.exists(path):
		return null
	var tex: Texture2D = load(path)
	_tex_cache[key] = tex
	return tex


func _draw_hud() -> void:
	var font := ThemeDB.fallback_font
	var battle_state := "进行中"
	if battle.finished:
		battle_state = ("平局" if battle.winner < 0
				else "%s方胜利" % ("红" if battle.winner == 0 else "蓝"))
	var mode_name: String = ["纯贴图", "贴图+数据+单位", "数据+单位"][_base_mode] if _atlas != null else "数据(缺图集)"
	var sprite_state := ("精灵%d档" % _unit_sprites.size()) if not _unit_sprites.is_empty() else "精灵缺失(色块回退)"
	var line1 := "CROSS HERMIT 战斗模拟器 — MAP01 %d×%d | 底图:%s | %s | %s (帧 %d) | 速度 %.1f× FPS %d" % [
		map.cell_w, map.cell_h, mode_name, sprite_state, battle_state, battle.frame if battle else 0,
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
		"[1/2/3]速度 [空格]暂停 [R]重开 [T]底图: 纯贴图/贴图+数据+单位/纯数据+单位 [F]回验证窗口 | 滚轮=缩放 中键拖=平移 点击=选单位",
		HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color(0.7, 0.7, 0.7))
