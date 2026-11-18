extends RefCounted
## Reverse BFS to every unoccupied firing cell within Manhattan attack range.
## The immutable terrain has a blocked border so neighbor probes stay in bounds.
var width: int
var height: int
var stride: int
var offsets: PackedInt32Array
var terrain: Array[PackedInt32Array] = []
var occupied := PackedInt32Array()
var fields: Dictionary = {}
var queue := PackedInt32Array()


func _init(w: int, h: int, layers: Array) -> void:
	width = w
	height = h
	stride = w+2
	offsets = PackedInt32Array([1,-1,stride,-stride])
	queue.resize(stride*(h+2))
	for layer in layers:
		var mask := PackedInt32Array()
		mask.resize(queue.size())
		mask.fill(-1)
		for y in range(h):
			for x in range(w):
				if layer[y*w+x] != 0: mask[(y+1)*stride+x+1] = 0
		terrain.append(mask)


func _index(cell: Vector2i) -> int:
	return (cell.y+1)*stride+cell.x+1


func _field(target: Vector2i, reach: int, mode: int) -> PackedInt32Array:
	var distance := terrain[mode].duplicate()
	for index in occupied: distance[index] = -1
	var tail := 0
	for y in range(maxi(0,target.y-reach),mini(height,target.y+reach+1)):
		var dx := reach-absi(y-target.y)
		for x in range(maxi(0,target.x-dx),mini(width,target.x+dx+1)):
			var index := (y+1)*stride+x+1
			if distance[index] != 0: continue
			distance[index] = 1
			queue[tail] = index
			tail += 1
	var head := 0
	while head < tail:
		var index := queue[head]
		head += 1
		var next_distance := distance[index]+1
		for step in offsets:
			var neighbor := index+step
			if distance[neighbor] != 0: continue
			distance[neighbor] = next_distance
			queue[tail] = neighbor
			tail += 1
	return distance


func route(start: Vector2i, target: Vector2i, reach: int, mode: int, units: Array) -> Array[Vector2i]:
	var result: Array[Vector2i] = []
	if absi(start.x-target.x)+absi(start.y-target.y) <= reach: return result
	var current := PackedInt32Array()
	for unit in units:
		if unit["limits"]["hp"] > 0: current.append(_index(unit["cell"]))
	if current != occupied:
		occupied = current
		fields.clear()
	var key := Vector4i(target.x,target.y,reach,mode)
	if not fields.has(key): fields[key] = _field(target,reach,mode)
	var distance: PackedInt32Array = fields[key]
	var cursor := _index(start)
	# Leaving the attacker's own occupied cell is always legal. No shortest
	# path returns to it. Equal-distance neighbors follow the original BFS order.
	while true:
		var best := 0x7fffffff
		var next := -1
		for step in offsets:
			var neighbor := cursor+step
			var value := distance[neighbor]
			if value > 0 and value < best:
				best = value
				next = neighbor
		if next < 0: break
		result.append(Vector2i(next%stride-1,next/stride-1))
		if best == 1: break
		cursor = next
	return result
