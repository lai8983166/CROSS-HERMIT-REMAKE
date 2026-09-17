extends "res://sim/tests/test_base.gd"

func test_smoke() -> void:
	assert_eq(1 + 1, 2, "整数加法")
	assert_true(true)
