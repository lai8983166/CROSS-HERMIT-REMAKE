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
var _unit_anim_clocks: Dictionary = {}   # instance_id → {identity,start_frame}
# 换色 (add-unit-recolor): 块7 表 + (档,色) 重映射字典 + 阵营默认色
var _unit_recolors: Dictionary = {}
var _recolor_maps: Dictionary = {}
var _faction_palettes: Dictionary = {}
# EFCT 全局动画；模拟层决定阶段、锚点和生命周期，视图只消费。
var _fx_animations: Dictionary = {}
var _fx_frames: Dictionary = {}
var _fx_frame_list: Array = []
var _fx_base := "res://assets/fx/EFCT"


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
	_load_unit_recolors()
	_load_attack_effects()
	if FileAccess.file_exists("res://assets/map01_composed.png"):
		_atlas = load("res://assets/map01_composed.png")   # 直角世界图 (add-map-composition)
		_base_mode = 0   # 默认纯贴图；单位与特效战斗层始终单独绘制
	else:
		_base_mode = 2   # 无贴图回退数据视图
	if map.cell_w > 0:
		_fit_view()
	_start_battle(0)
	queue_redraw()


func _start_battle(seed: int) -> void:
	var setup: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/battle_setup.json"))
	if FileAccess.file_exists("res://data/skill_demo.json"):
		var demo: Variant = JSON.parse_string(
			FileAccess.get_file_as_string("res://data/skill_demo.json"))
		if demo is Dictionary:
			setup["skill_demo"] = demo
	var use_seed: int = setup.get("seed", 42) if seed == 0 else seed
	_faction_palettes = {}   # 阵营默认换色 (add-unit-recolor): {"阵营str": palette_id}
	var fp: Variant = setup.get("faction_palettes", {})
	if fp is Dictionary:
		for k: String in fp:
			_faction_palettes[k] = int(fp[k])
	battle = Battle.start(setup, use_seed, map)
	selected = null
	_accum = 0.0
	_unit_anim_clocks.clear()


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
		for id: String in _unit_sprites:
			_unit_sprites[id]["_base"] = "res://assets/unit/%s" % id   # 帧资产寻址 (fx 并入后统一)


func _load_unit_recolors() -> void:
	if not FileAccess.file_exists("res://data/unit_recolors.json"):
		return   # 无换色表 → 全部基色
	var parsed: Variant = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/unit_recolors.json"))
	if parsed is Dictionary and parsed.get("units") is Dictionary:
		_unit_recolors = parsed["units"]


func _load_attack_effects() -> void:
	if not FileAccess.file_exists("res://data/attack_effects.json"):
		return   # 无特效表 → 不播不报错
	var parsed: Variant = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/attack_effects.json"))
	if not (parsed is Dictionary and parsed.get("animations") is Dictionary
			and parsed.get("frames") is Dictionary):
		return
	_fx_animations = parsed["animations"]
	_fx_frames = parsed["frames"]
	_fx_frame_list.resize(int(parsed.get("_meta", {}).get("frame_count", 0)))
	_fx_frame_list.fill({})
	for frame_key: String in _fx_frames:
		var frame_index := int(frame_key)
		if frame_index >= 0 and frame_index < _fx_frame_list.size():
			_fx_frame_list[frame_index] = _fx_frames[frame_key]
	# Reuse the proven unit texture cache/draw path. Sparse non-exported slots stay
	# empty and can never be referenced by validated EFCT timelines.
	_unit_sprites["EFCT"] = {"frames": _fx_frame_list, "_base": _fx_base}


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
	_auto_shot(delta)
	queue_redraw()


## 调试: 自动轮转截图 (0.4s/张 × 8 滚动) — "窗口异常但数据全亮"类问题抓现行
var _shot_timer := 0.0
var _shot_idx := 0
var auto_shots := OS.has_environment("CH_AUTO_SHOTS")   # 键 A 或诊断环境变量开启
var _last_draw: Dictionary = {}   # 单位名 → 最近一次绘制信息 (截图时落盘对账)

func _auto_shot(delta: float) -> void:
	if not auto_shots:
		return
	_shot_timer += delta
	if _shot_timer < 0.4:
		return
	_shot_timer = 0.0
	_capture("auto_%d" % _shot_idx)
	_shot_idx = (_shot_idx + 1) % 8

func _capture(tag: String) -> void:
	var img := get_viewport().get_texture().get_image()
	img.save_png("user://dbg_%s.png" % tag)
	if not _last_draw.is_empty():
		var f := FileAccess.open("user://dbg_state.txt", FileAccess.WRITE)
		f.store_line("battle.frame=%d tag=%s" % [battle.frame if battle else -1, tag])
		for k in _last_draw:
			f.store_line("%s %s" % [k, str(_last_draw[k])])
		f.close()


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
			KEY_A:
				auto_shots = not auto_shots
				_shot_idx = 0
				printerr("[截图] 自动轮转 ", "开" if auto_shots else "关",
						" -> ", OS.get_user_data_dir())
			KEY_P: _capture("manual")


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
	_draw_units()
	_draw_fx()
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
		if not _draw_sprite_unit(u, p):
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


## v2 steps/layers 与 v1 records/composites 的统一入口。
func _resolve_timeline(udata: Dictionary, entry: Dictionary) -> Dictionary:
	return AnimTimeline.resolve(udata, entry)

## 朝向向量 → 8 向罗盘键 (引擎行走带选择)
func _facing_dir8(f: Vector2i) -> String:
	if f.x < 0 and f.y < 0:
		return "NW"
	if f.x > 0 and f.y < 0:
		return "NE"
	if f.x < 0 and f.y > 0:
		return "SW"
	if f.x > 0 and f.y > 0:
		return "SE"
	if f.x < 0:
		return "W"
	if f.x > 0:
		return "E"
	if f.y < 0:
		return "N"
	return "S"


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


## 精灵绘制: 状态+八向选择时间线；身份变化时重置独立 sim 时钟，绘制当前 step 的全部图层。
## 返回 false = 无帧表/无序列/资产缺失 → 调用方走色块回退。
func _draw_sprite_unit(u: BattleUnit, p_screen: Vector2) -> bool:
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
		BattleUnit.State.CAST, BattleUnit.State.RELEASE, BattleUnit.State.SYNC, \
				BattleUnit.State.IMPACT, BattleUnit.State.RECOVER:
			key = "SKILL"
		BattleUnit.State.DEAD:
			key = "DEAD"
	var direction := _facing_dir8(u.facing)
	var entry: Dictionary = {}
	if key == "MOVE" and amap.has("walk_by_dir"):
		entry = amap["walk_by_dir"].get(direction, {})
	if key == "ATTACK" and amap.has("attack_by_dir"):
		entry = amap["attack_by_dir"].get(direction, {})
	if key == "SKILL":
		entry = AnimTimeline.unit_action_entry(udata, u.skill_action, direction)
	if entry.is_empty() and key == "IDLE" and amap.has("idle_by_dir"):
		entry = amap["idle_by_dir"].get(direction, {})
	if entry.is_empty():
		entry = amap.get(key, amap.get("IDLE", {}))
	var timeline := _resolve_timeline(udata, entry)
	if timeline.is_empty() or timeline.get("steps", []).is_empty():
		return false
	var frames: Array = udata.get("frames", [])
	if frames.is_empty():
		return false
	var flags := int(timeline.get("flags", 0))
	# v1 的 facing-right 开关只影响兼容输入；v2 使用方向表低两位 flags。
	if bool(entry.get("flip_x_when_facing_right", false)) and u.facing.x > 0:
		flags ^= 1
	var tick_seconds: float = float(_sprites_meta.get(
		"tick_seconds", _sprites_meta.get("dur_unit_seconds", 1.0 / 60.0)))
	var unit_id := u.get_instance_id()
	var clock: Dictionary = _unit_anim_clocks.get(unit_id, {})
	var identity := "%d/%s/%d/%d" % [u.state, direction, int(timeline.get("anim", -1)), flags]
	var elapsed_frames: int
	if key == "ATTACK":
		# 攻击时钟由 sim 挂点驱动；同方向连续攻击也会从首帧重新开始。
		elapsed_frames = maxi(0, battle.frame - u.attack_started_frame)
		identity += "/%d" % u.attack_started_frame
		clock["identity"] = identity
		clock["start_frame"] = u.attack_started_frame
	elif key == "SKILL":
		# Simulation owns phase boundaries. Each new phase/action therefore begins
		# at the first frame even when consecutive casts use the same direction.
		elapsed_frames = maxi(0, battle.frame - u.skill_phase_started_frame)
		identity += "/%d/%d/%d" % [u.skill_id, u.skill_action, u.skill_phase_started_frame]
		clock["identity"] = identity
		clock["start_frame"] = u.skill_phase_started_frame
	else:
		elapsed_frames = AnimTimeline.clock_elapsed(clock, identity, battle.frame)
	_unit_anim_clocks[unit_id] = clock
	var elapsed_ticks := int(floor(elapsed_frames * Battle.LOGIC_STEP / maxf(tick_seconds, 0.000001)))
	var picked := AnimTimeline.step_at(timeline, elapsed_ticks, key != "ATTACK")
	if picked.is_empty() and key == "ATTACK":
		# 原版普通攻击是非循环动作；播完后视觉回待机，战斗状态无需依赖素材时长。
		key = "IDLE"
		entry = amap.get("idle_by_dir", {}).get(direction, {})
		if entry.is_empty():
			entry = amap.get("IDLE", {})
		timeline = _resolve_timeline(udata, entry)
		if timeline.is_empty() or timeline.get("steps", []).is_empty():
			return false
		flags = int(timeline.get("flags", 0))
		identity = "IDLE/%s/%d/%d" % [direction, int(timeline.get("anim", -1)), flags]
		elapsed_frames = AnimTimeline.clock_elapsed(clock, identity, battle.frame)
		_unit_anim_clocks[unit_id] = clock
		elapsed_ticks = int(floor(elapsed_frames * Battle.LOGIC_STEP / maxf(tick_seconds, 0.000001)))
		picked = AnimTimeline.step_at(timeline, elapsed_ticks, true)
	if picked.is_empty():
		return false
	var step: Dictionary = picked["step"]
	# 脚底阴影 (43d270 印章语义的椭圆近似)
	draw_set_transform(p_screen, 0.0, Vector2(1.0, 0.45))
	draw_circle(Vector2.ZERO, 9.0 * view_scale, Color(0, 0, 0, 0.35))
	draw_set_transform(Vector2.ZERO)
	var layers: Array = step.get("layers", [])
	if layers.is_empty():
		return true   # 空白帧时段: 只画阴影不画本体 (序列本身有效)
	var pal := u.palette_id if u.palette_id >= 0 else int(_faction_palettes.get(str(u.faction), 0))
	var mod := Color(1, 1, 1, 0.55) if u.state == BattleUnit.State.WITHDRAWN else Color.WHITE
	_last_draw[u.name] = "anim=%s state=%s visual=%s dir=%s step=%d frames=%s pal=%d cell=%s" % [
		u.anim_id, BattleUnit.State.keys()[u.state], key, direction, int(picked["index"]),
		str(layers.map(func(layer): return int(layer.get("frame", -1)))), pal, str(u.cell)]
	var drawn := _draw_timeline_layers(u.anim_id, frames, layers, p_screen, pal, flags, mod)
	if drawn:
		for layer: Dictionary in layers:
			_check_dark_frame(u.anim_id, int(layer.get("frame", -1)), pal, u)
	return drawn


func _draw_timeline_layers(anim_id: String, frames: Array, layers: Array, p_screen: Vector2,
		pal_id: int, selection_flags: int, modulate := Color.WHITE) -> bool:
	var prepared: Array = []
	for layer: Dictionary in layers:
		var frame_index := int(layer.get("frame", -1))
		if frame_index < 0 or frame_index >= frames.size():
			return false
		var tex := _frame_tex(anim_id, frame_index, pal_id)
		if tex == null:
			return false
		var flip := AnimTimeline.combined_flip(layer, selection_flags)
		prepared.append({
			"texture": tex,
			"rect": AnimTimeline.layer_rect(frames[frame_index], layer),
			"flip_x": flip.x != 0,
			"flip_y": flip.y != 0,
		})
	for item: Dictionary in prepared:
		var sx := -view_scale if item["flip_x"] else view_scale
		var sy := -view_scale if item["flip_y"] else view_scale
		draw_set_transform_matrix(Transform2D(0.0, Vector2(sx, sy), 0.0, p_screen))
		draw_texture_rect(item["texture"], item["rect"], false, modulate)
		draw_set_transform_matrix(Transform2D())
	return true


## 换色重映射字典 (add-unit-recolor): 基色 hex → 目标 hex 的 int 键值表, 按 (档,色) 缓存
func _recolor_map(anim_id: String, pal_id: int) -> Dictionary:
	var key := "%s/%d" % [anim_id, pal_id]
	if _recolor_maps.has(key):
		return _recolor_maps[key]
	var m := {}
	var upal: Array = _unit_recolors.get(anim_id, {}).get("palettes", [])
	if pal_id >= 0 and pal_id < upal.size() and upal.size() > 0:
		var base: Array = upal[0]
		var targ: Array = upal[pal_id]
		if base.size() == 256 and targ.size() == 256:
			for c in 256:
				var bhex := String(base[c])
				var thex := String(targ[c])
				if bhex != thex:
					m[bhex.hex_to_int()] = thex.hex_to_int()
	_recolor_maps[key] = m
	return m


## 按模拟层阶段事件播放 EFCT 全局动画。持续施法的循环在阶段结束时由
## active_fx_events 淘汰；同步空白动画保留时长但没有可绘制图层。
func _draw_fx() -> void:
	if battle == null or _fx_animations.is_empty() or _fx_frames.is_empty():
		return
	for ev in battle.active_fx_events():
		var global_id := int(ev.get("global_id", 0))
		var animation: Dictionary = _fx_animations.get(str(global_id), {})
		if animation.is_empty():
			continue
		var timeline := AnimTimeline.normalize(animation)
		var age_frames := battle.frame - int(ev.get("frame", 0))
		var age_ticks := int(floor(age_frames * Battle.LOGIC_STEP / (1.0 / 60.0)))
		var picked := AnimTimeline.step_at(timeline, age_ticks, false)
		if picked.is_empty():
			continue
		var layers: Array = picked["step"].get("layers", [])
		if layers.is_empty():
			continue   # 空白帧时段 → 本帧不画
		var from_c: Array = ev.get("from_cell", [0, 0])
		var to_c: Array = ev.get("to_cell", [0, 0])
		var at_c: Array = from_c if String(ev.get("anchor", "target")) == "source" else to_c
		var p := origin + map.cell_to_world(int(at_c[0]), int(at_c[1])) * view_scale
		var flags := 1 if int(to_c[0]) < int(from_c[0]) else 0
		_last_draw["FX"] = "global=%d phase=%s step=%d frames=%s age_frames=%d at=(%d,%d)" % [
			global_id, String(ev.get("phase", "")), int(picked["index"]),
			str(layers.map(func(layer): return int(layer.get("frame", -1)))),
			age_frames, int(at_c[0]), int(at_c[1])]
		_draw_timeline_layers("EFCT", _fx_frame_list, layers, p, 0, flags)


## 暗帧检测 (调试): 记录每键平均亮度; 画出异常暗帧时打印 + 截图 (目检"黑色怪物"抓现行用)
var _frame_luma: Dictionary = {}
var _last_dark_shot_msec := -10000

func _note_frame_luma(key: String, buf: PackedByteArray) -> void:
	if _frame_luma.has(key) or buf.size() < 4:
		return
	var sum := 0
	var n := 0
	var i := 0
	while i < buf.size():
		if buf[i + 3] > 0:
			sum += (int(buf[i]) + int(buf[i + 1]) + int(buf[i + 2])) / 3
			n += 1
		i += 4
	_frame_luma[key] = [float(sum) / maxf(1, n), float(n) / (buf.size() / 4)]


func _check_dark_frame(anim_id: String, frame_idx: int, pal_id: int, u: BattleUnit) -> void:
	var key := "%s/%d/%d" % [anim_id, frame_idx, pal_id]
	if not _frame_luma.has(key):
		return
	var lv: Array = _frame_luma[key]
	if float(lv[0]) < 45.0 and float(lv[1]) > 0.25:
		var now := Time.get_ticks_msec()
		if now - _last_dark_shot_msec < 1000:
			return
		_last_dark_shot_msec = now
		printerr("[暗帧] %s state=%s facing=%s frame=%d pal=%d 亮度=%.0f 覆盖=%.0f%%" % [
			u.name, BattleUnit.State.keys()[u.state], str(u.facing), frame_idx,
			pal_id, float(lv[0]), float(lv[1]) * 100.0])
		var shot := get_viewport().get_texture().get_image()
		shot.save_png("user://dark_frame_%d.png" % now)


func _frame_tex(anim_id: String, frame_idx: int, pal_id: int = 0) -> Texture2D:
	var key := "%s/%d/%d" % [anim_id, frame_idx, pal_id]
	if _tex_cache.has(key):
		return _tex_cache[key]
	# 基色纹理独立缓存 (不递归 — GDScript VM 递归+早退触发 Stack underflow)
	var base_key := "%s/%d/0" % [anim_id, frame_idx]
	var base_tex: Texture2D = _tex_cache.get(base_key, null)
	if base_tex == null:
		var udata: Dictionary = _unit_sprites.get(anim_id, {})
		var frames: Array = udata.get("frames", [])
		if frame_idx < 0 or frame_idx >= frames.size():
			return null
		var base_dir: String = udata.get("_base", "res://assets/unit/%s" % anim_id)
		var path := "%s/%s" % [base_dir, frames[frame_idx].get("file", "")]
		if not ResourceLoader.exists(path):
			return null
		base_tex = load(path)
		_tex_cache[base_key] = base_tex
		if base_tex != null:
			var bimg := base_tex.get_image()
			if bimg.get_format() != Image.FORMAT_RGBA8:
				bimg.convert(Image.FORMAT_RGBA8)
			_note_frame_luma(base_key, bimg.get_data())
	if pal_id <= 0 or base_tex == null:
		return base_tex
	var m := _recolor_map(anim_id, pal_id)
	if m.is_empty():   # 无该换色 (越界/缺表) → 基色回退
		return base_tex
	var img := base_tex.get_image()
	if img.get_format() != Image.FORMAT_RGBA8:
		img.convert(Image.FORMAT_RGBA8)
	var buf := img.get_data()   # PackedByteArray, RGBA 字节序 (Image.data 属性是 Dictionary!)
	var i := 0
	var n := buf.size()
	while i < n:
		var k := (int(buf[i]) << 16) | (int(buf[i + 1]) << 8) | int(buf[i + 2])
		if m.has(k):
			var v: int = m[k]
			buf[i] = (v >> 16) & 0xFF
			buf[i + 1] = (v >> 8) & 0xFF
			buf[i + 2] = v & 0xFF
		i += 4
	var tex := ImageTexture.create_from_image(Image.create_from_data(
			img.get_width(), img.get_height(), false, Image.FORMAT_RGBA8, buf))
	_tex_cache[key] = tex
	_note_frame_luma(key, buf)
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
