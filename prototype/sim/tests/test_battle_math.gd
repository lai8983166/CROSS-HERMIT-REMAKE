extends "res://sim/tests/test_base.gd"
## 伤害三式锚点 (tasks 2.4) — 数值结论抄自 battle_mechanics.md §3

class MockRng:
	extends RefCounted
	var seq: Array = []
	var i := 0
	func randi() -> int:
		var v: int = seq[i % seq.size()]
		i += 1
		return v


func _mock(seq: Array) -> MockRng:
	var m := MockRng.new()
	m.seq = seq
	return m


func test_physical_overflow_band() -> void:
	# 命中=200, 回避=0 → c=200 ≥150 → m=200; rolls[0]=0 → d=100×200/100=200
	var d := BattleMath.physical(
		{"power": 100, "power_range": 0, "accuracy": 200},
		{"evasion": 0, "evasion_coef": 100, "defense": 0, "defense_coef": 100},
		_mock([0]))
	assert_eq(d, 200, "命中溢出倍率档 → 200")

func test_physical_miss() -> void:
	# c = 10 − 50×100/100 − 50 = −90 <0; MISS roll=50 ∈(4,94] → MISS
	var d := BattleMath.physical(
		{"power": 100, "power_range": 0, "accuracy": 10},
		{"evasion": 50, "evasion_coef": 100, "defense": 0, "defense_coef": 100},
		_mock([50, 50]))
	assert_eq(d, BattleMath.MISS, "MISS 哨兵")

func test_physical_zero_damage() -> void:
	# c = 100−10−30 = 60 (<150, 回避>0), roll2=0 ∉(4,94] → m=100; d = 10−20 = −10 → 钳 0
	var d := BattleMath.physical(
		{"power": 10, "power_range": 0, "accuracy": 100},
		{"evasion": 10, "evasion_coef": 100, "defense": 20, "defense_coef": 100},
		_mock([30, 0]))
	assert_eq(d, 0, "普通命中可零伤")

func test_physical_band_minimum_one() -> void:
	# m=150 档: c≥150 且防高 → d<1 钳 1
	var d := BattleMath.physical(
		{"power": 1, "power_range": 0, "accuracy": 999},
		{"evasion": 0, "evasion_coef": 100, "defense": 99, "defense_coef": 100},
		_mock([0]))
	assert_eq(d, 1, "倍率档至少 1")

func test_magic_resist() -> void:
	assert_eq(BattleMath.magic(100, 40, 0), 60, "魔抗 40% → 60")
	assert_eq(BattleMath.magic(100, 0, 0), 100, "零抗")
	assert_eq(BattleMath.magic(10, 100, 0), 1, "至少 1")


func test_magic_snapshot_formula_includes_resist_and_body_modifiers() -> void:
	var rng := _mock([74])
	var damage := BattleMath.magic_from_snapshots(
		{"power": 200, "power_range": 50},
		{"magic_resist": 25, "magic_resist_modifier": 5,
			"body": 10, "body_modifier": 50}, rng)
	assert_eq(damage, 174, "(200+74%50)×80%-10×50% = 174")
	assert_eq(rng.i, 1, "威力浮动非零时仅消费一次随机值")


func test_magic_snapshot_does_not_consume_rng_without_power_range() -> void:
	var rng := _mock([19])
	var damage := BattleMath.magic_from_snapshots(
		{"power": 80, "power_range": 0},
		{"magic_resist": 100, "body": 99, "body_modifier": 100}, rng)
	assert_eq(damage, 1, "魔法伤害下限仍为1")
	assert_eq(rng.i, 0, "无浮动威力时不消费随机值")


func test_fixed() -> void:
	assert_eq(BattleMath.fixed(77), 77, "定值直出")

func test_determinism() -> void:
	var a := RandomNumberGenerator.new()
	a.seed = 42
	var b := RandomNumberGenerator.new()
	b.seed = 42
	var atk := {"power": 80, "power_range": 30, "accuracy": 120}
	var def := {"evasion": 30, "evasion_coef": 100, "defense": 15, "defense_coef": 100}
	var r1: int = BattleMath.physical(atk, def, a)
	var r2: int = BattleMath.physical(atk, def, b)
	assert_true(r1 is int and r2 is int, "返回值非空 (防 null==null 假绿)")
	assert_eq(r1, r2, "同种子两次一致")
