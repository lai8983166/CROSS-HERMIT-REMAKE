extends "res://sim/tests/test_base.gd"

const Handshake = preload("res://sim/tactics_exit_handshake.gd")


func _fixture() -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string(
		"res://data/tactics_exit_handshake_evidence.json"))


func test_each_frame_matches_original_x86_execution() -> void:
	var fixture := _fixture()
	assert_eq(fixture["evidence_kind"], "original_x86_with_synthetic_external_inputs",
		"明确区分机器指令仿真与实机证据")
	for example in fixture["cases"]:
		var state: Dictionary = example["initial_state"].duplicate(true)
		for expected in example["states"]:
			var result := Handshake.step(state, example["external_inputs"])
			assert_true(result["supported"], example["name"] + " 支持已核对的收尾部分")
			for key in ["transition_phase", "script_phase", "script_control_active", "exit_flag",
					"script_completion_phase", "fade_in_value", "fade_out_value"]:
				assert_eq(result["state"][key], expected[key], example["name"] + ":" + key)
			for index in range(3):
				assert_eq(int(result["state"]["finish_flags"][index]),
					int(expected["finish_flags"][index]), example["name"] + ":flag" + str(index))
			for key in ["script_function_return", "transition_function_return"]:
				assert_eq(result[key], expected[key], example["name"] + ":" + key)
			assert_false(result["authorizes_persistent_write"], "逐帧核对不授权持久事务")
			state = result["state"]


func test_input_is_copied_and_missing_phases_stay_unresolved() -> void:
	var example: Dictionary = _fixture()["cases"][0]
	var state: Dictionary = example["initial_state"].duplicate(true)
	var original := state.duplicate(true)
	var result := Handshake.step(state, example["external_inputs"])
	assert_eq(state, original, "不会改写调用方状态或标志数组")
	result["state"]["finish_flags"][0] = 99
	assert_eq(state, original, "返回标志也与调用方隔离")
	state["script_phase"] = 2
	assert_false(Handshake.step(state, example["external_inputs"])["supported"],
		"不模拟未实现的 VM 执行")
	state.erase("transition_phase")
	assert_false(Handshake.step(state, example["external_inputs"])["supported"],
		"缺少任务收尾阶段保持未解析")


func test_no_implicit_clock_or_animation_defaults() -> void:
	var state: Dictionary = _fixture()["cases"][0]["initial_state"]
	assert_false(Handshake.step(state, {})["supported"], "外部输入必须显式提供")
	assert_false(Handshake.step(state, {"fade_step": -1, "animation_ready": true})["supported"],
		"未核对的时间范围保持未解析")


func test_native_script_execution_supplies_post_vm_handoff() -> void:
	var fixture: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(
		"res://data/scene5_script_execution_evidence.json"))
	assert_false(fixture["state11_observed"], "原版 CPU 回放不是状态 11 实机轨迹")
	assert_false(fixture["authorizes_persistent_write"], "模拟完成回调不授权持久事务")
	var last_command: Dictionary = fixture["commands"][-1]
	assert_eq(int(last_command["opcode"]), 19, "必须真正执行脚本 END")
	assert_eq(int(last_command["offset"]), 0x774, "来自场景 5 子程序 2 的 END")
	assert_true(int(last_command["frame"]) < int(fixture["handoff_frame"]),
		"END 先于收尾交接")
	var state: Dictionary = fixture["initial_state"].duplicate(true)
	assert_eq(int(state["script_phase"]), 5, "交接阶段来自原版 VM 执行")
	for expected in fixture["states"]:
		var result := Handshake.step(state, {"fade_step": 255, "animation_ready": true})
		assert_true(result["supported"], "已执行脚本交接到已核对收尾部分")
		for key in ["transition_phase", "script_phase", "script_completion_phase",
				"fade_in_value", "fade_out_value"]:
			assert_eq(int(result["state"][key]), int(expected[key]), "script handoff:" + key)
		for index in range(3):
			assert_eq(int(result["state"]["finish_flags"][index]),
				int(expected["finish_flags"][index]), "script handoff:flags")
		assert_eq(int(result["transition_function_return"]),
			int(expected["transition_function_return"]), "只有收尾返回值表示局部退出")
		state = result["state"]
