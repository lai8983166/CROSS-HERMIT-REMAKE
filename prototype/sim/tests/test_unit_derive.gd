extends "res://sim/tests/test_base.gd"
## SimUnit 构造与派生上限 (tasks 2.2 / 2.3)

func test_unit_defaults() -> void:
	var u := SimUnit.new()
	assert_eq(u.evasion, 0, "回避缺省 0")
	assert_eq(u.armor, 0, "装甲缺省 0")
	assert_eq(u.magic_resist, 0, "魔抗缺省 0")
	assert_eq(u.level, 1, "等级缺省 1")

func test_unit_ctor_and_readback() -> void:
	var u := SimUnit.new({
		"strength": 12, "agility": 13, "sense": 14, "vitality": 15,
		"intellect": 16, "constitution": 17, "spirit": 18,
		"job_id": 3, "level": 7, "evasion": 22,
	})
	assert_eq(u.strength, 12, "力")
	assert_eq(u.constitution, 17, "耐")
	assert_eq(u.spirit, 18, "精")
	assert_eq(u.job_id, 3, "职业")
	assert_eq(u.level, 7, "等级")
	assert_eq(u.evasion, 22, "回避读回")

func test_derive_hp_anchor() -> void:
	# (耐10 力10 敏10, hp_coef=100) → (30+10+10)×100/100 = 50 — combat-math spec 锚点
	var u := SimUnit.new({"constitution": 10, "strength": 10, "agility": 10})
	var d := SimDerive.derive_limits(u, {"hp_coef": 100, "mp_coef": 100, "spirit_coef": 100})
	assert_eq(d.hp_max, 50, "HP 锚点")

func test_derive_hp_clamp_floor() -> void:
	# 全 1 属性 + hp_coef=1 → 公式值 0 → 钳 1
	var u := SimUnit.new()
	var d := SimDerive.derive_limits(u, {"hp_coef": 1, "mp_coef": 100, "spirit_coef": 100})
	assert_eq(d.hp_max, 1, "HP 下限钳位")

func test_derive_formulas() -> void:
	# MP = (精×3+智+活)×coef/100 clamp 30..999; 精神系 = (感×3+智+活)×coef/100
	var u := SimUnit.new({"spirit": 10, "intellect": 10, "vitality": 10, "sense": 10})
	var d := SimDerive.derive_limits(u, {"hp_coef": 100, "mp_coef": 100, "spirit_coef": 100})
	assert_eq(d.mp_max, (30 + 10 + 10) * 100 / 100, "MP 公式 (精×3+智+活)")
	assert_eq(d.spirit_max, (30 + 10 + 10) * 100 / 100, "精神系 (感×3+智+活)")
	var d2 := SimDerive.derive_limits(u, {"hp_coef": 100, "mp_coef": 100, "spirit_coef": 100}, {"mp": 5})
	assert_eq(d2.mp_max, 55, "MP 修正参与")
