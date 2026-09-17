class_name SimMapData
extends RefCounted
## 地图逻辑层 (docs/formats.md §5) — 加载 map##.json + 格值访问 + 菱形坐标换算
## 格 = 32×16 px; cell_to_world 返回"格心"局部坐标 (不含 ORIGIN/缩放, 由渲染方叠加)

const CELL_W := 32
const CELL_H := 16

var cell_w := 0
var cell_h := 0
var _layers: Dictionary = {}   # 层名 -> Array[int] (行优先, idx = y*cell_w + x)
var meta: Dictionary = {}


static func load_map(map_id: String) -> SimMapData:
	var m := SimMapData.new()
	var txt := FileAccess.get_file_as_string("res://data/map%s.json" % map_id)
	if txt.is_empty():
		push_error("地图缺失: map%s.json" % map_id)
		return m
	var parsed: Variant = JSON.parse_string(txt)
	if parsed == null or not parsed is Dictionary:
		push_error("地图解析失败: map%s.json" % map_id)
		return m
	m.meta = parsed.get("_meta", {})
	m.cell_w = int(m.meta.get("cell_w", 0))
	m.cell_h = int(m.meta.get("cell_h", 0))
	var layers: Dictionary = parsed.get("layers", {})
	for k in layers:
		m._layers[k] = layers[k]
	return m


func has_layer(name: String) -> bool:
	return _layers.has(name)


## 格值; 越界/未知层返回 -1
func layer_value(name: String, x: int, y: int) -> int:
	if not _layers.has(name) or x < 0 or y < 0 or x >= cell_w or y >= cell_h:
		return -1
	return _layers[name][y * cell_w + x]


## 格心局部坐标 (菱形: 中心 = ((x−y)·16, (x+y)·8))
func cell_to_world(x: int, y: int) -> Vector2:
	return Vector2((x - y) * (CELL_W * 0.5), (x + y) * (CELL_H * 0.5))


## 任意局部坐标 → 所在格 (旋转度量下最近格心 = 菱形归属; 格心点往返恒等)
func world_to_cell(w: Vector2) -> Vector2i:
	var s: float = w.x / (CELL_W * 0.5)
	var t: float = w.y / (CELL_H * 0.5)
	return Vector2i(roundi((t + s) * 0.5), roundi((t - s) * 0.5))


## 可行走判定 (add-pathfinding) — 规则 Dictionary 由调用方从 data/walk_rules.json 加载缓存
## rules: {blocked_terrain: Array, blocked_variant: Array, blocked_objects: "nonzero"|Array}
func is_walkable(x: int, y: int, rules: Dictionary) -> bool:
	if x < 0 or y < 0 or x >= cell_w or y >= cell_h:
		return false
	if rules.get("blocked_terrain", []).has(layer_value("terrain", x, y)):
		return false
	if rules.get("blocked_variant", []).has(layer_value("variant", x, y)):
		return false
	var obj_rule: Variant = rules.get("blocked_objects", [])
	var o: int = layer_value("object", x, y)
	if typeof(obj_rule) == TYPE_STRING and obj_rule == "nonzero":
		if o != 0:
			return false
	elif obj_rule is Array and obj_rule.has(o):
		return false
	return true
