extends "res://sim/tests/test_base.gd"

func test_smoke() -> void:
	assert_eq(1 + 1, 2, "整数加法")
	assert_true(true)


func test_main_gd_可解析() -> void:
	# main.gd 不进测试树, 解析错误只有窗口启动才暴露 (空白窗口事故 2026-09-18) —
	# load() 即触发 GDScript 解析, Parse Error 时返回 null / 报错
	var script: GDScript = load("res://main.gd")
	assert_true(script != null, "main.gd 应可解析加载")
	assert_true(script.can_instantiate(), "main.gd 应可实例化 (非抽象)")
