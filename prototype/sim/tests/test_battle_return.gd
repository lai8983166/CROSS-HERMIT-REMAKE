extends "res://sim/tests/test_base.gd"

const BattleReturnScript = preload("res://sim/battle_return.gd")


func _fixture() -> Dictionary:
	var file: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(
		"res://data/battle_script_signals.json"))
	return file["signals"][0]


func test_winner_only_cannot_advance_return() -> void:
	var setup: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(
		"res://data/battle_setup.json"))
	var battle := Battle.start(setup, 42)
	battle.run_to_finish()
	var handoff := BattleReturnScript.new()
	assert_true(handoff.accept_terminal_snapshot(battle.get_terminal_snapshot()),
		"接收本地终局事实")
	assert_eq(handoff.status(), "pending_task_exit", "仅有 winner 不等于战术任务退出")
	assert_false(handoff.accept_terminal_snapshot(battle.get_terminal_snapshot()),
		"同一终局不重复送达")
	assert_true(handoff.inputs()["script_signal"].is_empty(), "没有捏造脚本信号")


func test_sourced_script_signal_stays_separate_from_task_exit() -> void:
	var handoff := BattleReturnScript.new()
	var request := _fixture()
	request["source_tick"] = 84
	assert_true(handoff.accept_script_signal(request), "接收有来源的 112 中途信号")
	assert_eq(handoff.status(), "pending_terminal", "脚本信号不等于本地终局")
	request["raw_cells"][0] = 99
	assert_eq(handoff.inputs()["script_signal"]["raw_cells"][0], 0,
		"信号输入已深拷贝")
	assert_false(handoff.accept_script_signal(_fixture()), "脚本信号只接收一次")
	var terminal := {"frame": 42, "winner": 0, "units": []}
	assert_true(handoff.accept_terminal_snapshot(terminal), "补入终局事实")
	assert_eq(handoff.status(), "pending_task_exit", "两路输入仍不能推出任务退出或战果分支")
	assert_eq(handoff.inputs()["script_signal"]["instruction_offset"], 10984,
		"保留真实脚本偏移")
	assert_false(handoff.inputs().has("task_exit_evidence"), "不伪造任务退出证据")
	assert_false(handoff.inputs().has("result_branch"), "不伪造战果分支")


func test_signal_requires_source_tick_opcode_and_classification() -> void:
	var handoff := BattleReturnScript.new()
	var request := _fixture()
	assert_false(handoff.accept_script_signal(request), "离线模板不伪装运行时事件")
	request["source_tick"] = 1
	request["opcode"] = 148
	assert_false(handoff.accept_script_signal(request), "未证实的 148 不作为 112 信号")
	request["opcode"] = 112
	request["interpretation"] = "script_exit_request_only"
	assert_false(handoff.accept_script_signal(request), "旧退出请求分类不可再接收")
