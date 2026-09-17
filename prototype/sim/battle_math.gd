class_name BattleMath
## 伤害/命中三式 (公式见 battle_mechanics.md §3 / REMAKE_BLUEPRINT.md §4.2)
## RNG 由调用方注入 (测试用 MockRng 控序列, 实机用 RandomNumberGenerator 播种)

const MISS := -1  # 哨兵: 未命中 (伤害值域非负)


## 物理攻击 (原作 4824D0 语义)
## atk = {power, power_range, accuracy}; def = {evasion, evasion_coef, defense, defense_coef}
## rng 需提供 randi() -> int; 调用序列: 命中roll → (未进倍率档时)MISS判定roll → (浮动>0时)威力roll
static func physical(atk: Dictionary, def: Dictionary, rng) -> int:
	# c = 命中 − (回避×系数)/100 − rand%100 — 见 battle_mechanics.md §3.1
	var c: int = atk.accuracy - def.evasion * def.evasion_coef / 100 - rng.randi() % 100
	var m := 100
	if def.evasion == 0 or c >= 150:
		m = maxi(c, 150)  # 命中溢出 → ≥1.5 倍档
	else:
		var r: int = rng.randi() % 100
		if r > 4 and r <= 94 and c < 0:
			# 原作 rand∈(4,0x5E] = r∈5..94 段 (c<0 时约 90% MISS)
			return MISS
	# 威力 p = 威力 + (浮动>0 ? rand%浮动 : 0)
	var p: int = atk.power
	if atk.power_range > 0:
		p += rng.randi() % atk.power_range
	# 伤害 d = p×m/100 − (防御×系数)/100
	var d: int = p * m / 100 - def.defense * def.defense_coef / 100
	# m==100 可 0 伤; 倍率档至少 1
	if m == 100:
		if d < 1:
			d = 0
	elif d < 1:
		d = 1
	return d


## 魔法攻击 (原作 4826F0): d = 基础×(100−魔抗+修正)/100, 至少 1 — 见 battle_mechanics.md §3.2
static func magic(base: int, resist: int, mod: int = 0) -> int:
	return maxi(base * (100 - resist + mod) / 100, 1)


## 固定/特效伤害 (原作 482810): 无减项直接输出 — 见 battle_mechanics.md §3.3
static func fixed(value: int) -> int:
	return value
