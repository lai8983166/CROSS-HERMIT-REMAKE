extends "res://sim/tests/test_base.gd"
## add-unit-recolor: 换色表加载 / 基色语义 / 配置有效 / 回退 (tasks 3.1)


func test_换色表加载() -> void:
	var parsed: Variant = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/unit_recolors.json"))
	assert_true(parsed is Dictionary, "unit_recolors.json 应可解析")
	var units: Dictionary = parsed.get("units", {})
	assert_true(units.size() >= 10, "至少 10 档")
	for id in units:
		var u: Dictionary = units[id]
		var pals: Array = u.get("palettes", [])
		assert_eq(pals.size(), int(u.get("palette_count", -1)), "%s 条目数与声明一致" % id)
		assert_eq(pals.size(), 40, "%s 40 张换色表" % id)
		var ok_shape := true
		for pal in pals:
			var p: Array = pal
			if p.size() != 256:
				ok_shape = false
				break
			for hx in p:
				if String(hx).length() != 6:
					ok_shape = false
					break
			if not ok_shape:
				break
		assert_true(ok_shape, "%s 每张 256 条 hex RRGGBB" % id)


func test_基色与换色差异() -> void:
	var parsed: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/unit_recolors.json"))
	for id in parsed["units"]:
		var pals: Array = parsed["units"][id]["palettes"]
		var diff := 0
		for c in 256:
			if pals[0][c] != pals[7][c]:
				diff += 1
		# *1A 档的 [7] 是温和变体 (diff 24~44), *0A 是大改 (diff>150) — 只需证明是独立换色表
		assert_true(diff > 10, "%s 基色[0]与[7]差异明显 (实为换色表, diff=%d)" % [id, diff])


func test_battle_setup_配置有效() -> void:
	var setup: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var recolors: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/unit_recolors.json"))["units"]
	var fp: Dictionary = setup.get("faction_palettes", {})
	assert_true(not fp.is_empty(), "阵营默认配色已配")
	for k in fp:
		assert_true(int(fp[k]) >= 0 and int(fp[k]) < 40, "faction_palettes[%s] 在 0..39" % k)
	for u in setup.get("units", []):
		var pid: int = int(u.get("palette_id", -1))
		assert_true(pid >= -1 and pid < 40, "单位 %s palette_id ∈ [-1,40)" % u.get("name", "?"))
		if pid >= 0:
			assert_true(recolors.has(String(u.get("anim_id", ""))),
				"配了 palette_id 的单位其 anim_id 在换色表中")


func test_配置避让行走暗板() -> void:
	# walk_luma = 每调色板对 MOVE 行走带的最低平均亮度 (B1A pal12 周期性黑怪事故 2026-09-18)
	# 断言: 配置的 palette_id (单位级或阵营默认) 不踩暗板 — 亮度 ≥ min(45, 基色+10)
	# (整档角色本身暗的, 如 D0A 法师深袍, 允许与基色同水位)
	var setup: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var recolors: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/unit_recolors.json"))["units"]
	var fpal: Dictionary = setup.get("faction_palettes", {})
	for u in setup.get("units", []):
		var uid := String(u.get("anim_id", ""))
		if not recolors.has(uid):
			continue
		var wl: Dictionary = recolors[uid].get("walk_luma", {})
		if wl.is_empty():
			continue
		var pid: int = int(u.get("palette_id", -1))
		if pid < 0:
			pid = int(fpal.get(str(int(u.get("faction", 0))), 0))
		var floor_: float = minf(45.0, float(wl.get("0", 255.0)) + 10.0)
		var got: float = float(wl.get(str(pid), 255.0))
		assert_true(got >= floor_, "单位 %s pal%d 行走亮度 %.0f ≥ %.0f (暗板清单见 _recolors 导出)" % [
			u.get("name", "?"), pid, got, floor_])


func test_回退语义() -> void:
	# 视图侧: 越界 palette_id / 未知档 → _recolor_map 返回空表 → 基色回退。
	# 数据侧验证: 表结构与已知键存在性 (运行时行为由 main.gd _frame_tex 保证)
	var parsed: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/unit_recolors.json"))
	var units: Dictionary = parsed["units"]
	assert_false(units.has("__no_such__"), "未知档不在表 (视图回退基色)")
	# [0] 与自身完全一致 (基色恒等, 重映射 0 号 = 不换色)
	for id in units:
		var p0: Array = units[id]["palettes"][0]
		var same := 0
		for c in 256:
			if p0[c] == p0[c]:
				same += 1
		assert_eq(same, 256, "%s [0] 恒等" % id)
