extends "res://sim/tests/test_base.gd"
## ENGAGE TIME 锚点 (tasks 2.5) — battle_mechanics.md §8

func test_engage_low_level_cap() -> void:
	assert_eq(SimEngage.engage_seconds(1), 356400, "lv1 = 5940min×60 = 99h 封顶")
	assert_eq(SimEngage.engage_seconds(5), 356400, "lv5 同封顶段")

func test_engage_max_level() -> void:
	assert_eq(SimEngage.engage_seconds(50), 32400, "lv50 = 540min×60")

func test_engage_modifiers() -> void:
	assert_eq(SimEngage.engage_seconds(50, 1, 0), 36000, "lv50 + 1h = 32400+3600")
	assert_eq(SimEngage.engage_seconds(50, 0, 30), 32430, "+30s")

func test_engage_clamp() -> void:
	assert_eq(SimEngage.engage_seconds(0), 1, "lv0 表值 0 → 钳 1")
	assert_eq(SimEngage.engage_seconds(50, 999, 0), 356400, "超上限钳 99h")
