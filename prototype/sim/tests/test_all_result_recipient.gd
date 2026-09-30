extends "res://sim/tests/test_base.gd"

const Recipient = preload("res://sim/all_result_recipient.gd")


func _empty_groups() -> Array:
	var groups := []
	for _group in range(5):
		groups.append([-1, -1, -1, -1])
	return groups


func test_selects_first_strict_max_by_original_id() -> void:
	var groups := _empty_groups()
	groups[0][0] = 0
	groups[0][1] = 1
	groups[1][0] = 2
	var result: Dictionary = Recipient.select(groups, [3, 7, 9], {3: 4, 7: 10, 9: 10})
	assert_eq(result["status"], "selected")
	assert_eq(result["character_id"], 7, "同分时保留首位")
	assert_eq(result["group_index"], 0)
	assert_eq(result["slot_index"], 1)
	assert_eq(groups[0][1], 1, "输入未被改写")


func test_zero_rank_keeps_original_unset_sentinel_as_rejection() -> void:
	var groups := _empty_groups()
	groups[4][3] = 0
	assert_eq(Recipient.select(groups, [6], {6: 0})["status"],
		"no_eligible_recipient", "原版未选中时不能写 0xFFFF 角色")


func test_invalid_mapping_rejects_entire_selection() -> void:
	var groups := _empty_groups()
	groups[0][0] = 0
	groups[0][1] = 1
	assert_eq(Recipient.select(groups, [3, 13], {3: 9, 13: 11})["reason"],
		"character_id", "不能保留部分选择并忽略后续无效角色")
	assert_eq(Recipient.select(groups, [3], {3: 9})["reason"],
		"participant_index")
	assert_eq(Recipient.select(groups, [3, 7], {3: 9})["reason"],
		"rank_value")


func test_rejects_malformed_source_arrays() -> void:
	assert_eq(Recipient.select([], [], {})["reason"], "group_count")
	var groups := _empty_groups()
	groups[0] = [-1]
	assert_eq(Recipient.select(groups, [], {})["reason"], "slots_per_group")
	groups = _empty_groups()
	groups[0][0] = "0"
	assert_eq(Recipient.select(groups, [3], {3: 9})["reason"],
		"participant_index_type")
