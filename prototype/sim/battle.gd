class_name Battle
extends RefCounted
## 战斗控制器 — 固定逻辑步长 tick + 事件日志 (add-unit-render design 决策 1/4)
## 全部随机性经唯一注入 RNG; 单位按数组序遍历 → 同种子整场确定

const LOGIC_STEP := 1.0 / 30.0
const RANGE := 1          # 普攻射程 (格, 曼哈顿)

var units: Array = []     # Array[BattleUnit] (无类型标注: 测试直接塞构造体)
var rng := RandomNumberGenerator.new()
var frame := 0
var events: Array[String] = []
var finished := false
var winner := -1          # -1 进行中/平局
var move_interval := 12
var attack_interval := 30
var map: SimMapData = null                      # 传入则启用寻路 (add-pathfinding)
var walk_rules: Dictionary = {}


static func start(setup: Dictionary, seed: int, p_map: SimMapData = null) -> Battle:
	var b := Battle.new()
	b.rng.seed = seed
	b.map = p_map
	b.walk_rules = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/walk_rules.json"))
	b.move_interval = maxi(1, int(setup.get("move_interval", 12)))
	b.attack_interval = maxi(1, int(setup.get("attack_interval", 30)))
	for u in setup.get("units", []):
		var bu := BattleUnit.new()
		bu.setup(u)
		b.units.append(bu)
	b._log("start units=%d seed=%d" % [b.units.size(), seed])
	return b


func tick() -> void:
	if finished:
		return
	frame += 1
	# ENGAGE 计时 (先扣再判, 归零→撤退; battle_mechanics.md §8 语义)
	for u in units:
		if u.state == BattleUnit.State.DEAD:
			continue
		if u.engage_left <= 0.0:
			u.state = BattleUnit.State.WITHDRAWN
			_log("f%d %s withdraw" % [frame, u.name])
		else:
			u.engage_left -= LOGIC_STEP
	# 行动
	for u in units:
		if u.state == BattleUnit.State.DEAD or u.state == BattleUnit.State.WITHDRAWN:
			continue
		var t := _nearest_enemy(u)
		if t == null:
			continue
		var dist: int = absi(u.cell.x - t.cell.x) + absi(u.cell.y - t.cell.y)
		if dist > RANGE:
			if frame % move_interval == 0 and _step_along_path(u, t.cell):
				_log("f%d %s move %d,%d" % [frame, u.name, u.cell.x, u.cell.y])
		elif frame % attack_interval == 0:
			_attack(u, t)
	_check_finish()


func _nearest_enemy(u: BattleUnit) -> BattleUnit:
	var best: BattleUnit = null
	var best_d := -1
	for t in units:
		if t.faction == u.faction:
			continue
		if t.state == BattleUnit.State.DEAD or t.state == BattleUnit.State.WITHDRAWN:
			continue
		var d: int = absi(u.cell.x - t.cell.x) + absi(u.cell.y - t.cell.y)
		if best == null or d < best_d:
			best = t
			best_d = d
	return best


## 沿 BFS 路径步进一步 (add-pathfinding); 地图缺失时退化为直线步进; 返回是否移动
func _step_along_path(u: BattleUnit, target: Vector2i) -> bool:
	if map == null:
		_step_straight(u, target)
		return true
	var blocked := {}
	for o in units:
		if o != u and o.state != BattleUnit.State.DEAD and o.state != BattleUnit.State.WITHDRAWN:
			blocked[o.cell] = true
	var path := SimPath.find_path(map, walk_rules, u.cell, target, blocked)
	if path.is_empty():
		return false   # 不可达/挤死 → 原地等待
	u.cell = path[0]
	u.state = BattleUnit.State.MOVE
	return true


func _step_straight(u: BattleUnit, target: Vector2i) -> void:
	var dx: int = target.x - u.cell.x
	var dy: int = target.y - u.cell.y
	if dx == 0:
		u.cell.y += signi(dy)
	elif dy == 0:
		u.cell.x += signi(dx)
	elif absi(dx) > absi(dy):
		u.cell.x += signi(dx)
	else:
		u.cell.y += signi(dy)
	u.state = BattleUnit.State.MOVE


func _attack(a: BattleUnit, d: BattleUnit) -> void:
	a.state = BattleUnit.State.ATTACK
	var dmg: int = BattleMath.physical(
		{"power": a.atk_power, "power_range": a.atk_power_range, "accuracy": a.atk_accuracy},
		{"evasion": d.evasion, "evasion_coef": 100, "defense": d.defense, "defense_coef": 100},
		rng)
	if dmg == BattleMath.MISS:
		_log("f%d %s->%s MISS" % [frame, a.name, d.name])
		return
	d.hp -= dmg
	_log("f%d %s->%s hit %d (hp %d)" % [frame, a.name, d.name, dmg, maxi(d.hp, 0)])
	if d.hp <= 0:
		d.hp = 0
		d.state = BattleUnit.State.DEAD
		_log("f%d %s dead" % [frame, d.name])


func _check_finish() -> void:
	var alive := [false, false]
	for u in units:
		if u.state != BattleUnit.State.DEAD and u.state != BattleUnit.State.WITHDRAWN:
			alive[u.faction] = true
	if alive[0] == alive[1]:   # 双方都在 → 继续; 都空 → 平局
		if not alive[0]:
			finished = true
			winner = -1
			_log("f%d finish draw" % frame)
	else:
		finished = true
		winner = 0 if alive[0] else 1
		_log("f%d finish winner=%d" % [frame, winner])


func _log(msg: String) -> void:
	events.append(msg)


## 离屏跑完整场 (测试用); 上限帧防死循环
func run_to_finish(max_frames := 100000) -> void:
	while not finished and frame < max_frames:
		tick()
