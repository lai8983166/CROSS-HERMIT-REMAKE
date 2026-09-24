class_name Battle
extends RefCounted
## 战斗控制器 — 固定逻辑步长 tick + 事件日志 (add-unit-render design 决策 1/4)
## 全部随机性经唯一注入 RNG; 单位按数组序遍历 → 同种子整场确定

const LOGIC_STEP := 1.0 / 30.0
const CONDITION6_ID := 6
const CONDITION6_PRIORITY := 2
const CONDITION6_MIN_TICKS_EXCLUSIVE := 0xB7
const SOURCE_TICKS_PER_LOGIC_FRAME := 2
const SKILL22_ID := 22
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
# typed 特效事件流 (add-attack-effects): 只追加不改判, 战斗逻辑/确定性不受影响
var fx_events: Array[Dictionary] = []
var fx_events_keep := 64   # 最近保留条数 (视图消费用, 防长战内存涨; 数据字段非平衡常量)
var skill_events: Array[Dictionary] = []
var active_skills: Dictionary = {}   # caster instance id -> deterministic phase record
var skill_demo: Dictionary = {}
var _next_demo_frame := -1


static func start(setup: Dictionary, seed: int, p_map: SimMapData = null) -> Battle:
	var b := Battle.new()
	b.rng.seed = seed
	b.map = p_map
	b.walk_rules = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/walk_rules.json"))
	b.move_interval = maxi(1, int(setup.get("move_interval", 12)))
	b.attack_interval = maxi(1, int(setup.get("attack_interval", 30)))
	b.skill_demo = setup.get("skill_demo", {})
	if bool(b.skill_demo.get("enabled", false)):
		b._next_demo_frame = maxi(0, int(b.skill_demo.get("start_frame", 0)))
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
	_tick_condition_slots()
	_tick_skill_demo()
	_advance_skills()
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
		if active_skills.has(u.get_instance_id()):
			continue
		if bool(skill_demo.get("enabled", false)) and bool(skill_demo.get("exclusive", false)):
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
	# 格变更扫描 (add-unit-sprites): 朝向 8 向量化 + 视图插值快照
	for u in units:
		if u.cell != u._tick_prev_cell:
			u.facing = Vector2i(signi(u.cell.x - u._tick_prev_cell.x),
					signi(u.cell.y - u._tick_prev_cell.y))
			u.from_cell = u._tick_prev_cell
			u.move_started_frame = frame
			u._tick_prev_cell = u.cell
	_check_finish()


static func _anim_ticks_to_logic_frames(ticks: int) -> int:
	# DxAnim and attack-table timing are 60 Hz; battle simulation is fixed 30 Hz.
	return ceili(maxi(0, ticks) * (1.0 / 60.0) / LOGIC_STEP)


func _tick_skill_demo() -> void:
	if not bool(skill_demo.get("enabled", false)) or _next_demo_frame < 0 or frame < _next_demo_frame:
		return
	var caster_index := int(skill_demo.get("caster_unit", 0))
	var target_index := int(skill_demo.get("target_unit", 1))
	if caster_index < 0 or caster_index >= units.size() \
			or target_index < 0 or target_index >= units.size():
		_next_demo_frame = -1
		return
	var caster: BattleUnit = units[caster_index]
	if active_skills.has(caster.get_instance_id()):
		return
	if not start_skill(caster, units[target_index], int(skill_demo.get("skill_id", 29))):
		_next_demo_frame = -1
		return
	if not bool(skill_demo.get("repeat", true)):
		_next_demo_frame = -1
		return
	var record: Dictionary = active_skills.get(caster.get_instance_id(), {})
	var total_frames := 0
	for stage: Dictionary in record.get("stages", []):
		total_frames += int(stage.get("duration", 0))
	_next_demo_frame = frame + total_frames + maxi(0, int(skill_demo.get("repeat_delay_frames", 60)))


static func _fx_logic_frames(global_id: int) -> int:
	if global_id <= 0:
		return 0
	return _anim_ticks_to_logic_frames(int(
		SimTables.fx_animation(global_id).get("duration_ticks", 0)))


## Start one deterministic skill presentation. This entry point is independent
## of UI so tests and data-driven demos use the exact same phase machine.
func start_skill(caster: BattleUnit, target: BattleUnit, p_skill_id: int) -> bool:
	if caster == null or target == null:
		return false
	if active_skills.has(caster.get_instance_id()):
		return false
	var attack := SimTables.attack(p_skill_id)
	var visual := SimTables.skill_visual(p_skill_id)
	if attack.is_empty() or visual.is_empty():
		return false
	var target_filter := int(attack.get("target_filter", 0))
	if not _target_filter_allows(caster, target, target_filter):
		return false
	var delta := target.cell - caster.cell
	if delta != Vector2i.ZERO:
		caster.facing = Vector2i(signi(delta.x), signi(delta.y))
	var cast_fx := int(visual.get("cast_fx", 0))
	var release_fx := int(visual.get("release_fx", 0))
	var sync_fx := int(visual.get("sync_fx", 0))
	var impact_fx := int(visual.get("impact_fx", 0))
	var stages := [
		{"name": "cast", "state": BattleUnit.State.CAST,
			"action": int(visual.get("cast_action", 0)), "global_id": cast_fx,
			"duration": _anim_ticks_to_logic_frames(int(attack.get("cast_frames", 0))),
			"anchor": "source"},
		{"name": "release", "state": BattleUnit.State.RELEASE,
			"action": int(visual.get("release_action", 0)), "global_id": release_fx,
			"duration": _fx_logic_frames(release_fx), "anchor": "source"},
		{"name": "sync", "state": BattleUnit.State.SYNC,
			"action": int(visual.get("release_action", 0)), "global_id": sync_fx,
			"duration": _fx_logic_frames(sync_fx), "anchor": "target"},
		{"name": "impact", "state": BattleUnit.State.IMPACT,
			"action": int(visual.get("release_action", 0)), "global_id": impact_fx,
			"duration": _fx_logic_frames(impact_fx), "anchor": "target"},
		{"name": "recovery", "state": BattleUnit.State.RECOVER,
			"action": int(visual.get("recover_action", 0)), "global_id": 0,
			"duration": _anim_ticks_to_logic_frames(int(attack.get("recovery_frames", 0))),
			"anchor": "source"},
	]
	var record := {
		"skill_id": p_skill_id, "caster": caster, "target": target,
		"from_cell": [caster.cell.x, caster.cell.y],
		"to_cell": [target.cell.x, target.cell.y],
		"cast_action": int(visual.get("cast_action", 0)),
		"release_action": int(visual.get("release_action", 0)),
		"recover_action": int(visual.get("recover_action", 0)),
		"cast_fx": cast_fx, "release_fx": release_fx,
		"sync_fx": sync_fx, "impact_fx": impact_fx,
		"gameplay_effect_id": int(attack.get("hit_effect", 0)),
		"target_filter": target_filter,
		"stages": stages, "phase_index": -1, "phase_started_frame": frame,
	}
	caster.skill_id = p_skill_id
	caster.skill_started_frame = frame
	active_skills[caster.get_instance_id()] = record
	_enter_next_skill_phase(caster.get_instance_id())
	return true


func _enter_next_skill_phase(caster_key: int) -> void:
	if not active_skills.has(caster_key):
		return
	var record: Dictionary = active_skills[caster_key]
	var caster: BattleUnit = record["caster"]
	while true:
		record["phase_index"] = int(record["phase_index"]) + 1
		if int(record["phase_index"]) >= record["stages"].size():
			caster.state = BattleUnit.State.IDLE
			caster.skill_id = -1
			caster.skill_action = 0
			active_skills.erase(caster_key)
			return
		var stage: Dictionary = record["stages"][int(record["phase_index"])]
		record["phase_started_frame"] = frame
		caster.state = int(stage["state"])
		caster.skill_action = int(stage["action"])
		caster.skill_phase_started_frame = frame
		active_skills[caster_key] = record
		_emit_skill_stage(record, stage)
		if String(stage["name"]) == "impact":
			_resolve_skill_impact(record)
		if int(stage["duration"]) > 0:
			return


func _advance_skills() -> void:
	for caster_key in active_skills.keys():
		if not active_skills.has(caster_key):
			continue
		var record: Dictionary = active_skills[caster_key]
		var stage: Dictionary = record["stages"][int(record["phase_index"])]
		if frame - int(record["phase_started_frame"]) >= int(stage["duration"]):
			_enter_next_skill_phase(int(caster_key))


func _emit_skill_stage(record: Dictionary, stage: Dictionary) -> void:
	var event := {
		"type": "skill_stage", "frame": frame, "phase": stage["name"],
		"duration_frames": stage["duration"], "global_id": stage["global_id"],
		"anchor": stage["anchor"], "skill_id": record["skill_id"],
		"from_cell": record["from_cell"], "to_cell": record["to_cell"],
		"cast_action": record["cast_action"], "release_action": record["release_action"],
		"recover_action": record["recover_action"], "cast_fx": record["cast_fx"],
		"release_fx": record["release_fx"], "sync_fx": record["sync_fx"],
		"impact_fx": record["impact_fx"],
		"gameplay_effect_id": record["gameplay_effect_id"],
		"target_filter": record["target_filter"],
	}
	skill_events.append(event)
	fx_events.append(event)
	if fx_events.size() > fx_events_keep:
		fx_events = fx_events.slice(fx_events.size() - fx_events_keep)


## Current stage-owned visual instances. Renderers consume this projection and
## never decide their own hit timing or keep effects alive beyond the stage.
func active_fx_events() -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for event in fx_events:
		if int(event.get("global_id", 0)) <= 0:
			continue
		var age := frame - int(event.get("frame", frame))
		if age >= 0 and age < int(event.get("duration_frames", 0)):
			result.append(event)
	return result


func _resolve_skill_impact(record: Dictionary) -> void:
	var caster: BattleUnit = record["caster"]
	var target: BattleUnit = record["target"]
	if target.state == BattleUnit.State.DEAD or target.state == BattleUnit.State.WITHDRAWN:
		_record_skill_gameplay_result({"outcome": "target_unavailable",
			"target_state": target.state})
		return
	# Nonzero gameplay effects have their own original dispatch. Until their
	# field writes are reconstructed, a physical hit would fabricate gameplay.
	var effect_id := int(record["gameplay_effect_id"])
	if effect_id == CONDITION6_ID:
		var skill_id := int(record["skill_id"])
		if skill_id != SKILL22_ID:
			_record_skill_gameplay_result({"outcome": "unresolved_base_hit_path"})
			_log("f%d %s->%s skill%d effect6 base-hit path unresolved" % [frame,
				caster.name, target.name, skill_id])
			return
		# Skill 22 is use_condition=2 / magic (4826F0), which clamps damage to >=1.
		# Its single-cell target must still occupy the cell selected when the cast began.
		var aim_cell: Array = record.get("to_cell", [])
		if aim_cell.size() != 2 or target.cell != Vector2i(int(aim_cell[0]), int(aim_cell[1])):
			_record_skill_gameplay_result({"outcome": "target_left_aim_cell",
				"aim_cell": aim_cell.duplicate(),
				"target_cell": [target.cell.x, target.cell.y]})
			_log("f%d %s skill22 effect6 target left aim cell" % [frame, target.name])
			return
		var mp_result := _apply_skill22_mp_damage(caster, target)
		var result := _apply_effect6(caster, target, int(record["skill_id"]))
		result["mp_result"] = mp_result
		result["condition_id"] = CONDITION6_ID
		result["slot_index"] = 0
		if String(result.get("outcome", "")) == "applied":
			result["application"] = target.condition_slots[0].duplicate(true)
		_record_skill_gameplay_result(result)
		_log("f%d %s->%s skill%d effect6 %s (%d/%d ticks)" % [frame,
			caster.name, target.name, int(record["skill_id"]), String(result["outcome"]),
			int(result.get("applied_ticks", 0)), int(result.get("base_ticks", 0))])
		return
	if effect_id != 0:
		_record_skill_gameplay_result({"outcome": "unresolved_effect",
			"effect_id": effect_id})
		_log("f%d %s->%s skill%d gameplay effect %d unresolved" % [frame,
			caster.name, target.name, int(record["skill_id"]), effect_id])
		return
	# Friendly/self gameplay effects are not reconstructed yet. Preserve the
	# original presentation and target semantics without inventing damage.
	if target.faction == caster.faction:
		_record_skill_gameplay_result({"outcome": "friendly_effect_unresolved"})
		_log("f%d %s->%s skill%d friendly effect unresolved" % [frame,
			caster.name, target.name, int(record["skill_id"])])
		return
	var hp_before := target.hp
	var damage: int = BattleMath.physical(
		{"power": caster.atk_power, "power_range": caster.atk_power_range,
			"accuracy": caster.atk_accuracy},
		{"evasion": target.evasion, "evasion_coef": 100,
			"defense": target.defense, "defense_coef": 100}, rng)
	var hit := damage != BattleMath.MISS
	if hit:
		target.hp = maxi(0, target.hp - damage)
		if target.hp == 0:
			target.state = BattleUnit.State.DEAD
	_record_skill_gameplay_result({
		"outcome": "hit" if hit else "miss",
		"applied_value": damage if hit else 0,
		"hp_before": hp_before, "hp_after": target.hp,
	})
	_log("f%d %s->%s skill%d %s" % [frame, caster.name, target.name,
		int(record["skill_id"]), "hit %d" % damage if hit else "MISS"])


func _apply_skill22_mp_damage(caster: BattleUnit, target: BattleUnit) -> Dictionary:
	# Attribute byte +6=2 routes the independently computed magic hit to MP.
	# Do this before effect6: the original calculates the base hit before condition resistance.
	var mp_before := target.mp
	var damage := BattleMath.magic_from_snapshots(
		{"power": caster.atk_power, "power_range": caster.atk_power_range},
		{"magic_resist": target.unit.magic_resist,
			"magic_resist_modifier": target.unit.magic_resist_modifier,
			"body": target.unit.body, "body_modifier": target.unit.body_modifier}, rng)
	target.mp = clampi(target.mp - damage, 0, target.mp_max)
	return {
		"resource": "mp", "outcome": "drained" if target.mp < mp_before else "already_empty",
		"computed_damage": damage, "applied_damage": mp_before - target.mp,
		"mp_before": mp_before, "mp_after": target.mp,
	}


func _record_skill_gameplay_result(result: Dictionary) -> void:
	if skill_events.is_empty():
		return
	var event_index := skill_events.size() - 1
	var event: Dictionary = skill_events[event_index]
	if String(event.get("phase", "")) != "impact" or int(event.get("frame", -1)) != frame:
		return
	var gameplay_result := result.duplicate(true)
	gameplay_result["resolved_frame"] = frame
	event["gameplay_result"] = gameplay_result
	skill_events[event_index] = event


func _apply_effect6(caster: BattleUnit, target: BattleUnit, skill_id: int) -> Dictionary:
	var attr_row := SimTables.skill_attribute(skill_id)
	var attr_bytes: Array = attr_row.get("bytes", [])
	if attr_bytes.size() != 7:
		return {"outcome": "unresolved_attributes", "base_ticks": 0, "applied_ticks": 0}
	var attack := SimTables.attack(skill_id)
	if attack.is_empty():
		return {"outcome": "unresolved_attack_row", "base_ticks": 0, "applied_ticks": 0}

	var base_ticks := 0
	match int(attr_bytes[3]):
		1:
			base_ticks = caster.unit.sp_effect
		2:
			base_ticks = int(attack.power_base) + int(caster.unit.char_no * int(attack.power_scale) / 100)
		3:
			base_ticks = int(attack.power_base) + int(caster.unit.agility * int(attack.power_scale) / 100)
		4:
			base_ticks = int(attack.power_base) + int(caster.unit.sense * int(attack.power_scale) / 100)
		5:
			base_ticks = int(attack.power_base) + int(caster.unit.vitality * int(attack.power_scale) / 100)
		6:
			base_ticks = int(attack.power_base) + int(caster.unit.strength * int(attack.power_scale) / 100)
		_:
			return {"outcome": "unresolved_value_selector", "base_ticks": 0, "applied_ticks": 0}

	# 4828A0 consumes rand()%100 even though condition 6 bypasses the random resist gate.
	var resistance_roll := rng.randi() % 100
	var job := SimTables.job(target.unit.job_id)
	var job_modifier := int(job.get("u16_0x22", 0)) & 0xff
	var resistance_factor := mini(100, 100 - target.unit.magic_resist + job_modifier)
	if resistance_factor == 0:
		return {"outcome": "resisted", "base_ticks": base_ticks, "applied_ticks": 0,
			"resistance_factor": 0, "resistance_roll": resistance_roll}
	if resistance_factor < 0:
		resistance_factor = 100 - resistance_factor
	var applied_ticks := int(base_ticks * resistance_factor / 100)
	if applied_ticks <= CONDITION6_MIN_TICKS_EXCLUSIVE:
		return {"outcome": "resisted", "base_ticks": base_ticks, "applied_ticks": 0,
			"resistance_factor": resistance_factor, "resistance_roll": resistance_roll}

	# IDs above 100 use the fallback attribute row and an additional skill-type chance gate.
	var high_id_roll := -1
	if skill_id > 100:
		high_id_roll = rng.randi() % 100
		if caster.unit.skill_type <= high_id_roll:
			return {"outcome": "resisted", "base_ticks": base_ticks, "applied_ticks": 0,
				"resistance_factor": resistance_factor, "resistance_roll": resistance_roll,
				"high_id_roll": high_id_roll}

	# Condition 6 conflicts with 46/47; original removes the conflicting state and rejects apply.
	var conflict_found := false
	for slot_index in target.condition_slots.size():
		var old_condition: Dictionary = target.condition_slots[slot_index]
		var old_id := int(old_condition.get("condition_id", 0))
		if old_id == 46 or old_id == 47:
			target.condition_slots[slot_index] = {}
			conflict_found = true
	if conflict_found:
		return {"outcome": "conflict_rejected", "base_ticks": base_ticks,
			"applied_ticks": 0, "resistance_factor": resistance_factor}

	var current: Dictionary = target.condition_slots[0]
	var current_id := int(current.get("condition_id", 0))
	if current_id != 0 and current_id != CONDITION6_ID:
		# Other condition priorities have not been exported; do not overwrite an unknown state.
		return {"outcome": "priority_unresolved", "base_ticks": base_ticks,
			"applied_ticks": 0, "resistance_factor": resistance_factor}
	if current_id == CONDITION6_ID and int(current.get("priority", 0)) > CONDITION6_PRIORITY:
		return {"outcome": "priority_rejected", "base_ticks": base_ticks,
			"applied_ticks": 0, "resistance_factor": resistance_factor}

	target.condition_slots[0] = {
		"condition_id": CONDITION6_ID,
		"source_skill_id": skill_id,
		"priority": CONDITION6_PRIORITY,
		"ticks_remaining": applied_ticks,
		"tick_counter": 0,
		"base_ticks": base_ticks,
		"resistance_factor": resistance_factor,
		"applied_frame": frame,
	}
	return {"outcome": "applied", "base_ticks": base_ticks,
		"applied_ticks": applied_ticks, "resistance_factor": resistance_factor,
		"resistance_roll": resistance_roll, "high_id_roll": high_id_roll}


func _tick_condition_slots() -> void:
	for unit_variant in units:
		var unit: BattleUnit = unit_variant
		for slot_index in unit.condition_slots.size():
			var condition: Dictionary = unit.condition_slots[slot_index]
			if int(condition.get("condition_id", 0)) == 0:
				continue
			for _source_tick in SOURCE_TICKS_PER_LOGIC_FRAME:
				var remaining := int(condition.get("ticks_remaining", 0))
				if remaining <= 0:
					unit.condition_slots[slot_index] = {}
					break
				remaining -= 1
				condition["ticks_remaining"] = remaining
				if remaining == 0:
					unit.condition_slots[slot_index] = {}
					_log("f%d %s condition%d expired" % [frame, unit.name,
						int(condition.get("condition_id", 0))])
					break
				if int(condition.get("condition_id", 0)) == CONDITION6_ID:
					condition["tick_counter"] = (int(condition.get("tick_counter", 0)) + 1) % 180


static func _target_filter_allows(caster: BattleUnit, target: BattleUnit,
		target_filter: int) -> bool:
	var same_faction := caster.faction == target.faction
	match target_filter:
		1:
			return true
		2, 5:
			return not same_faction
		3, 4:
			return same_faction
		_:
			return false


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
	# 缓存命中: 目标未变且缓存下一步仍可走 → 直接走; 否则重算
	if u.path_cache.is_empty() or u.path_target != target:
		u.path_cache = _path(u, target)
		u.path_target = target
	while not u.path_cache.is_empty():
		var next: Vector2i = u.path_cache[0]
		if _cell_free(next, u):
			u.cell = next
			u.path_cache.remove_at(0)
			u.state = BattleUnit.State.MOVE
			return true
		u.path_cache.remove_at(0)   # 前方被占, 弹出重试后续步
	# 缓存耗尽/不可达 → 重算一次; 仍空则原地等待
	u.path_cache = _path(u, target)
	u.path_target = target
	if u.path_cache.is_empty():
		return false
	var step: Vector2i = u.path_cache[0]
	if not _cell_free(step, u):
		u.path_cache = []
		return false
	u.cell = step
	u.path_cache.remove_at(0)
	u.state = BattleUnit.State.MOVE
	return true


func _path(u: BattleUnit, target: Vector2i) -> Array[Vector2i]:
	var blocked := {}
	for o in units:
		if o != u and o.state != BattleUnit.State.DEAD and o.state != BattleUnit.State.WITHDRAWN:
			blocked[o.cell] = true
	return SimPath.find_path(map, walk_rules, u.cell, target, blocked)


func _cell_free(c: Vector2i, u: BattleUnit) -> bool:
	if map != null and not map.is_walkable(c.x, c.y, walk_rules):
		return false
	for o in units:
		if o != u and o.cell == c and o.state != BattleUnit.State.DEAD 				and o.state != BattleUnit.State.WITHDRAWN:
			return false
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
	a.attack_started_frame = frame
	var attack_delta := d.cell - a.cell
	if attack_delta != Vector2i.ZERO:
		a.facing = Vector2i(signi(attack_delta.x), signi(attack_delta.y))
	var dmg: int = BattleMath.physical(
		{"power": a.atk_power, "power_range": a.atk_power_range, "accuracy": a.atk_accuracy},
		{"evasion": d.evasion, "evasion_coef": 100, "defense": d.defense, "defense_coef": 100},
		rng)
	if dmg == BattleMath.MISS:
		_log("f%d %s->%s MISS" % [frame, a.name, d.name])
		_emit_fx(a, d, false, 0)
		return
	d.hp -= dmg
	_log("f%d %s->%s hit %d (hp %d)" % [frame, a.name, d.name, dmg, maxi(d.hp, 0)])
	_emit_fx(a, d, true, dmg)
	d.hp -= dmg
	_log("f%d %s->%s hit %d (hp %d)" % [frame, a.name, d.name, dmg, maxi(d.hp, 0)])
	if d.hp <= 0:
		d.hp = 0
		d.state = BattleUnit.State.DEAD
		_log("f%d %s dead" % [frame, d.name])


## 特效事件 (add-attack-effects): MISS 也播 (错位斩击是原版演出的一部分)
func _emit_fx(a: BattleUnit, d: BattleUnit, hit: bool, damage: int) -> void:
	fx_events.append({
		"type": "attack", "frame": frame,
		"from_cell": [a.cell.x, a.cell.y], "to_cell": [d.cell.x, d.cell.y],
		"hit": hit, "damage": damage,
		"job_id": a.unit.job_id,
		"attack_id": a.attack_id,
		"gameplay_effect_id": a.gameplay_effect_id,
		"visual_ids": {
			"cast": a.cast_fx, "release": a.release_fx,
			"sync": a.sync_fx, "impact": a.impact_fx,
		},
	})
	if fx_events.size() > fx_events_keep:
		fx_events = fx_events.slice(fx_events.size() - fx_events_keep)


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
