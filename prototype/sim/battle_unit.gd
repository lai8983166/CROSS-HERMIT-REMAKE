class_name BattleUnit
extends RefCounted
## 战斗侧单位 — 组合 SimUnit 纯数据 (design 决策 6: 不继承) + 战斗字段
## 字段语义对照原作 wk: hp/hp_max(+0x16/+0x18) mp(+0x1C/+0x1E) engage(4b93c0 派生)

enum State { IDLE, MOVE, ATTACK, DEAD, WITHDRAWN }

var unit: SimUnit
var faction := 0
var name := ""
var cell := Vector2i.ZERO
var hp := 0
var hp_max := 0
var mp := 0
var mp_max := 0
var spirit_max := 0
var engage_left := 0.0    # 秒
var state := State.IDLE

# 普攻条目快照 (v1 简化: 威力=攻击表主威力基数, 命中=精度基础×10; 完整 0x4C 快照链后续 change)
var atk_power := 1
var atk_power_range := 0
var atk_accuracy := 0
# 防御快照 (v1: 回避=敏, 防御=耐 — 见 battle_mechanics.md §3.1 def 语义)
var evasion := 0
var defense := 0


func setup(def: Dictionary) -> void:
	name = def.get("name", "unit")
	faction = int(def.get("faction", 0))
	cell = Vector2i(int(def.pos[0]), int(def.pos[1]))
	unit = SimUnit.new(def.get("stats", {}))
	unit.job_id = int(def.get("job_id", 0))
	unit.level = int(def.get("level", 1))

	var job := SimTables.job(unit.job_id)
	var derived: Dictionary = SimDerive.derive_limits(unit, job)
	hp_max = derived.hp_max
	mp_max = derived.mp_max
	spirit_max = derived.spirit_max
	hp = hp_max
	mp = mp_max
	engage_left = float(def.get("engage_seconds",
			SimEngage.engage_seconds(unit.level)))   # 见 battle_mechanics.md §8

	# 职业默认攻击 (职业表+0x18 → 攻击表条目, 4b93c0 用法)
	# v1 威力快照 ≈ 48A380 模式4 (battle_mechanics.md §3.4): 力 + 主基数 + 力×A系数/100
	# (默认攻击 power_base 多为 0, 原作伤害实际来自属性缩放链 — 完整快照链后续 change)
	var atk: Dictionary = SimTables.attack(int(job.get("default_attack", 0)))
	var str_: int = unit.strength
	atk_power = maxi(1, str_ + int(atk.get("power_base", 0))
			+ str_ * int(atk.get("power_a_scale", 0)) / 100)
	atk_power_range = 0          # v1 无浮动 (原作浮动来自 44B 快照)
	atk_accuracy = int(atk.get("accuracy_base", 0)) * 10 + unit.agility
	evasion = unit.agility       # 回避快照 (原作 0x4D 派生链后续)
	defense = unit.armor        # 装甲 (wk+0x4E 语义; v1 默认 0)
