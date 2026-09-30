extends "res://sim/tests/test_base.gd"

const BattleReturnScript = preload("res://sim/battle_return.gd")


func _fixture() -> Dictionary:
	var file: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(
		"res://data/battle_exit_requests.json"))
	return file["requests"][0]


func test_winner_only_cannot_advance_return() -> void:
	var setup: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(
		"res://data/battle_setup.json"))
	var battle := Battle.start(setup, 42)
	battle.run_to_finish()
	var handoff := BattleReturnScript.new()
	assert_true(handoff.accept_terminal_snapshot(battle.get_terminal_snapshot()),
		"接收本地终局事实")
	assert_eq(handoff.status(), "pending_script_exit", "仅有 winner 不等于脚本结束")
	assert_false(handoff.accept_terminal_snapshot(battle.get_terminal_snapshot()),
		"同一终局不重复送达")
	assert_true(handoff.inputs()["script_exit_request"].is_empty(), "没有捏造脚本请求")


func test_sourced_script_request_stays_separate_from_result_branch() -> void:
	var handoff := BattleReturnScript.new()
	var request := _fixture()
	request["source_tick"] = 84
	assert_true(handoff.accept_script_exit_request(request), "接收有来源的 112 请求")
	assert_eq(handoff.status(), "pending_terminal", "脚本请求不等于本地终局")
	request["raw_cells"][0] = 99
	assert_eq(handoff.inputs()["script_exit_request"]["raw_cells"][0], 0,
		"请求输入已深拷贝")
	assert_false(handoff.accept_script_exit_request(_fixture()), "脚本请求只接收一次")
	var terminal := {"frame": 42, "winner": 0, "units": []}
	assert_true(handoff.accept_terminal_snapshot(terminal), "补入终局事实")
	assert_eq(handoff.status(), "pending_result_branch", "两路输入仍不能推出战果分支")
	assert_eq(handoff.inputs()["script_exit_request"]["instruction_offset"], 10984,
		"保留真实脚本偏移")


func test_request_requires_source_tick_and_opcode() -> void:
	var handoff := BattleReturnScript.new()
	var request := _fixture()
	assert_false(handoff.accept_script_exit_request(request), "离线模板不伪装运行时事件")
	request["source_tick"] = 1
	request["opcode"] = 148
	assert_false(handoff.accept_script_exit_request(request), "未证实的 148 不作为退出请求")
