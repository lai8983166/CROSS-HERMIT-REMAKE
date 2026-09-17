class_name SimPath
extends RefCounted
## BFS 最短路 (add-pathfinding, design 决策 1/2) — 四连通等距下 BFS 即最短
## 邻居扩展序固定 右/左/下/上 → 同输入恒同路径 (整场确定性依赖)
## 全 PackedInt32Array, 无 Dictionary 哈希开销 (idx = y*cell_w + x)

const DIRS: Array[Vector2i] = [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]
const DIRX := [1, -1, 0, 0]
const DIRY := [0, 0, 1, -1]


## 返回路径 (不含 from, 含 to); 目标阻挡/被占时终点退化为目标的最近可达邻格; 不可达返回 []
static func find_path(map: SimMapData, rules: Dictionary, from: Vector2i, to: Vector2i,
		blocked: Dictionary = {}) -> Array[Vector2i]:
	var w := map.cell_w
	var h := map.cell_h
	if w == 0 or h == 0:
		return []
	var targets := _target_set(map, rules, to, blocked)
	if targets.is_empty():
		return []   # 目标及其四邻全不可达

	var n := w * h
	var prev := PackedInt32Array()
	prev.resize(n)
	prev.fill(-1)
	var visited := PackedInt32Array()
	visited.resize(n)
	var start_i: int = from.y * w + from.x
	if not _open(map, rules, from, blocked, from):
		return []
	visited[start_i] = 1
	var queue := PackedInt32Array()
	queue.resize(n + 8)
	var head := 0
	var tail := 0
	queue[tail] = start_i
	tail += 1
	var goal_i := -1
	var dofs := [1, -1, w, -w]   # 右/左/下/上 的索引增量 (边界由 nx/ny 检查保证)
	var terrain: Array = map._layers.get("terrain", [])
	var variant: Array = map._layers.get("variant", [])
	var obj: Array = map._layers.get("object", [])
	var bt: Array = rules.get("blocked_terrain", [])
	var bv: Array = rules.get("blocked_variant", [])
	var bo: Variant = rules.get("blocked_objects", [])
	var bo_nonzero: bool = typeof(bo) == TYPE_STRING and bo == "nonzero"
	var bo_arr: Array = bo if bo is Array else []
	while head < tail:
		var cur: int = queue[head]
		head += 1
		if targets.has(cur):
			goal_i = cur
			break
		var cx: int = cur % w
		var cy: int = cur / w
		for k in 4:
			var nx: int = cx + DIRX[k]
			var ny: int = cy + DIRY[k]
			if nx < 0 or ny < 0 or nx >= w or ny >= h:
				continue
			var ni: int = cur + dofs[k]
			if visited[ni] != 0:
				continue
			visited[ni] = 1
			if ni != start_i:
				if bt.has(terrain[ni]):
					continue
				if bv.has(variant[ni]):
					continue
				var o: int = obj[ni]
				if (bo_nonzero and o != 0) or bo_arr.has(o):
					continue
				if blocked.has(Vector2i(nx, ny)):
					continue
			prev[ni] = cur
			queue[tail] = ni
			tail += 1
	if goal_i < 0:
		return []
	var path: Array[Vector2i] = []
	var node := goal_i
	while node != start_i and node >= 0:
		path.append(Vector2i(node % w, node / w))
		node = prev[node]
	path.reverse()
	return path


static func _open(map: SimMapData, rules: Dictionary, pos: Vector2i,
		blocked: Dictionary, from: Vector2i) -> bool:
	if pos == from:
		return true   # 自身所在格不判阻挡
	if not map.is_walkable(pos.x, pos.y, rules):
		return false
	return not blocked.has(pos)


## 目标集合: to 本身可走则 {to}; 否则其可走四邻 (多源退化, design 决策 4)
static func _target_set(map: SimMapData, rules: Dictionary, to: Vector2i,
		blocked: Dictionary) -> Dictionary:
	var t := {}
	if map.is_walkable(to.x, to.y, rules) and not blocked.has(to):
		t[to.y * map.cell_w + to.x] = true
		return t
	for d in DIRS:
		var p: Vector2i = to + d
		if p.x >= 0 and p.y >= 0 and p.x < map.cell_w and p.y < map.cell_h \
				and map.is_walkable(p.x, p.y, rules) and not blocked.has(p):
			t[p.y * map.cell_w + p.x] = true
	return t
