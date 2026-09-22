extends "res://sim/tests/test_base.gd"
## Skill 22's 3027 has a fixed source-unit anchor, not a target-directed path.


func test_3027目标和时间变化不造成外部位移() -> void:
	var release := {"global_id": 3027, "anchor": "source",
		"from_cell": [10, 10], "to_cell": [30, 18]}
	assert_eq(FxPlacement.anchor_cell(release), Vector2i(10, 10), "释放锚点为施法者")
	for target in [[11, 10], [30, 18], [99, 99]]:
		release["to_cell"] = target
		assert_eq(FxPlacement.anchor_cell(release), Vector2i(10, 10),
			"目标变化不能诱发线性、追踪或抛物线位移")
	assert_false(release.has("path_mode"), "无证据不增加路径模式")


func test_目标锚点仍按事件定位() -> void:
	var impact := {"global_id": 2029, "anchor": "target",
		"from_cell": [10, 10], "to_cell": [30, 18]}
	assert_eq(FxPlacement.anchor_cell(impact), Vector2i(30, 18), "命中特效位于目标")


func test_技能22实际释放事件保持源锚点() -> void:
	var setup := {"move_interval": 9999, "attack_interval": 9999, "units": [
		{"name": "caster", "faction": 0, "job_id": 9, "level": 10,
			"stats": {}, "pos": [10, 10], "anim_id": "C1A"},
		{"name": "enemy", "faction": 1, "job_id": 1, "level": 10,
			"stats": {}, "pos": [30, 18], "anim_id": "B1A"},
	]}
	var battle := Battle.start(setup, 7, null)
	assert_true(battle.start_skill(battle.units[0], battle.units[1], 22), "敌方技能可启动")
	for _i in 75:
		battle.tick()
	var active := battle.active_fx_events()
	assert_eq(active.size(), 1, "施法结束后只有释放特效")
	var release: Dictionary = active[0]
	assert_eq(int(release.global_id), 3027, "释放使用3027")
	assert_eq(FxPlacement.anchor_cell(release), Vector2i(10, 10), "实际事件固定源锚点")
	assert_false(release.has("path_mode"), "实际事件没有臆造轨迹")
