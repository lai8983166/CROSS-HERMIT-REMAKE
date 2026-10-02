extends "res://sim/tests/test_base.gd"

const Handshake = preload("res://sim/tactics_exit_handshake.gd")
const Transition = preload("res://sim/tactics_result_transition.gd")


func _fixture() -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string(
		"res://data/scene5_task_execution_evidence.json"))


func test_native_end_to_exit_to_result_dispatch() -> void:
	var fixture := _fixture()
	assert_eq(fixture["evidence_kind"], "original_task_loop_with_synthetic_world",
		"声明世界和任务初态仍为合成输入")
	for example in fixture["cases"]:
		if not example["state11_dispatched_in_emulation"]:
			continue
		var last_command: Dictionary = example["commands"][-1]
		assert_eq(int(last_command["opcode"]), 19, "必须运行实际 END")
		var state: Dictionary = example["post_vm_initial"].duplicate(true)
		for expected in example["post_vm_frames"]:
			var step := Handshake.step(state, example["external_inputs"])
			assert_true(step["supported"], "使用原版完成回调后的收尾状态")
			for key in ["script_phase", "transition_phase", "script_completion_phase",
					"fade_in_value", "fade_out_value"]:
				assert_eq(int(step["state"][key]), int(expected[key]), example["name"] + ":" + key)
			for index in range(3):
				assert_eq(int(step["state"]["finish_flags"][index]),
					int(expected["finish_flags"][index]), "完成标志与原版一致")
			assert_eq(int(step["transition_function_return"]),
				int(expected["transition_function_return"]), "原版局部退出判据")
			state = step["state"]
		var result := Transition.step(example["exit_frame"], example["dispatch_context"])
		assert_true(result["supported"], "已核对的场景 5 状态分派子集")
		assert_eq(result["status"], "tactics_result_requested", "完成后请求战术结果任务")
		assert_eq(int(result["requested_state"]), int(example["dispatch_events"][0]["state"]),
			"结果状态来自原版请求函数")
		assert_eq(int(result["dispatch_target_va"]), 0x4BD6F0, "状态表选择战果构造入口")
		assert_eq(example["result_task"]["vtable"], "0x5a0dfc", "真实构造函数安装战果虚表")
		assert_false(example["live_state11_observed"], "隔离回放不是实机轨迹")
		assert_false(result["authorizes_persistent_write"], "结果请求不授权角色或日历事务")


func test_waits_block_result_dispatch() -> void:
	for example in _fixture()["cases"]:
		if not example["bounded_stop"]:
			continue
		var result := Transition.step(example["exit_frame"], example["dispatch_context"])
		assert_true(result["supported"], "阻塞状态可以保留待定")
		assert_eq(result["status"], "pending_task_exit", example["name"] + " 保持待定")
		assert_eq(int(result["requested_state"]), -1, "不能伪造结果状态")
		assert_true(example["dispatch_events"].is_empty(), "原版尚未发出结果请求")
		assert_false(result["authorizes_persistent_write"], "阻塞不授权事务")


func test_existing_request_and_unknown_context_remain_unresolved() -> void:
	var example: Dictionary = _fixture()["cases"][0]
	var context: Dictionary = example["dispatch_context"].duplicate(true)
	context["request_pending"] = 1
	assert_false(Transition.step(example["exit_frame"], context)["supported"],
		"不能覆盖控制器已有请求")
	context = example["dispatch_context"].duplicate(true)
	context["scene_id"] = 45
	assert_false(Transition.step(example["exit_frame"], context)["supported"],
		"其它场景有不同出口，不使用场景 5 的投影")
	context = example["dispatch_context"].duplicate(true)
	context["next_scene"] = 1
	assert_false(Transition.step(example["exit_frame"], context)["supported"],
		"存在后继场景时保持未解析")
	context = example["dispatch_context"].duplicate(true)
	context["network_mode"] = true
	assert_false(Transition.step(example["exit_frame"], context)["supported"],
		"联机出口未纳入当前子集")
	context.erase("network_mode")
	assert_false(Transition.step(example["exit_frame"], context)["supported"],
		"没有隐式假定单机模式")


func test_inconsistent_exit_does_not_mutate_inputs() -> void:
	var example: Dictionary = _fixture()["cases"][0]
	var state: Dictionary = example["exit_frame"].duplicate(true)
	var context: Dictionary = example["dispatch_context"].duplicate(true)
	var original := state.duplicate(true)
	var original_context := context.duplicate(true)
	Transition.step(state, context)
	assert_eq(state, original, "分派投影不改变收尾输入")
	assert_eq(context, original_context, "分派投影不改变控制器输入")
	state["finish_flags"][1] = 0
	assert_false(Transition.step(state, context)["supported"], "完成标志与退出返回矛盾")
	state = original.duplicate(true)
	state["transition_phase"] = 17
	assert_false(Transition.step(state, context)["supported"], "动画等待不能冒充完成")


func test_menu_exit_requests_state_one_without_result_task() -> void:
	for example in _fixture()["cases"]:
		if example["name"] != "menu_exit":
			continue
		var result := Transition.step(example["exit_frame"], example["dispatch_context"])
		assert_true(result["supported"], "主菜单退出优先于场景 5 战果分派")
		assert_eq(result["status"], "menu_requested", "保留退出到主菜单的分支")
		assert_eq(int(result["requested_state"]), int(example["dispatch_events"][0]["state"]),
			"状态 1 来自原版请求")
		assert_eq(int(result["dispatch_target_va"]), 0x45E8D0, "主菜单任务入口")
		assert_false(example["state11_dispatched_in_emulation"], "此分支不构造战果任务")
		assert_false(result["authorizes_persistent_write"], "主菜单退出也不授权事务")
