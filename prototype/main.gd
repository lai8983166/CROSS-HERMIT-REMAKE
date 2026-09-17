extends Node2D
## 入口占位场景 — 战斗模拟器骨架 (蓝图 §4)
## 当前能力: 绘制 64×96 格网格 (格=32×16px, 原作坐标系) + 速度档切换 + FPS
## 后续按 openspec change 逐模块替换 (伤害/命中/ENGAGE TIME/AI/寻路)

const CELL_W := 32          # 原作格 = 32×16 px (battle_mechanics.md)
const CELL_H := 16
const GRID_W := 64          # MAP01 尺寸, 后续从 data/maps/*.json 读取
const GRID_H := 96
const ORIGIN := Vector2(512, 32)   # 网格绘制起点 (屏幕居中上半)

var _frame := 0


func _ready() -> void:
	# 原作速度档 1/2/3 (+0xb17c) → Engine.time_scale
	Engine.time_scale = 1.0
	queue_redraw()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_1: Engine.time_scale = 1.0
			KEY_2: Engine.time_scale = 2.0
			KEY_3: Engine.time_scale = 3.0
			KEY_R: queue_redraw()   # 重绘 (临时)


func _process(_delta: float) -> void:
	_frame += 1
	if _frame % 15 == 0:
		queue_redraw()


func _draw() -> void:
	# 菱形格 (斜视角): 每格宽32高16, 行间错位半个格
	for y in GRID_H:
		for x in GRID_W:
			var cx: float = ORIGIN.x + (x - y) * (CELL_W * 0.5)
			var cy: float = ORIGIN.y + (x + y) * (CELL_H * 0.5)
			if cx < -CELL_W or cx > 1024 or cy > 768 + CELL_H:
				continue
			draw_polyline(
				PackedVector2Array([
					Vector2(cx, cy - CELL_H * 0.5),
					Vector2(cx + CELL_W * 0.5, cy),
					Vector2(cx, cy + CELL_H * 0.5),
					Vector2(cx - CELL_W * 0.5, cy),
				]),
				Color(0.3, 0.5, 0.4, 0.25), 1.0)
	_draw_hud()


func _draw_hud() -> void:
	var font := ThemeDB.fallback_font
	var info := "CROSS HERMIT 重制模拟器骨架\n" \
		+ "格: %d×%d (%d×%d px)   速度档: %.1f×   FPS: %d" % [
			GRID_W, GRID_H, CELL_W, CELL_H,
			Engine.time_scale, Engine.get_frames_per_second()]
	draw_string(font, Vector2(16, 24), info, HORIZONTAL_ALIGNMENT_LEFT, -1, 14)
	draw_string(font, Vector2(16, 760),
		"[1/2/3] 速度档  [R] 重绘  — 数据与模块待 openspec change 注入",
		HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color(0.7, 0.7, 0.7))
