extends "res://sim/tests/test_base.gd"
## add-attack-effects: 特效表加载 / 效果序列有效 / 事件字段与上限 / 配置与回退 (tasks 3.1)


func test_特效表加载() -> void:
	var parsed: Variant = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/attack_effects.json"))
	assert_true(parsed is Dictionary, "attack_effects.json 应可解析")
	var files: Dictionary = parsed.get("files", {})
	assert_true(files.has("01E"), "01E 已导出")
	var e: Dictionary = files.get("01E", {})
	assert_eq(e.get("frames", []).size(), int(e.get("frame_count", -1)), "帧数与声明一致")
	var effects: Dictionary = parsed.get("effects", {})
	var default: String = parsed.get("default", "")
	assert_true(default != "" and effects.has(default), "default 非空且在 effects 中")
	for fxname in effects:
		var cfg: Dictionary = effects[fxname]
		assert_true(files.has(String(cfg.get("file", ""))), "%s 指向已导出档" % fxname)


func test_效果序列有效() -> void:
	var parsed: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/attack_effects.json"))
	var files: Dictionary = parsed["files"]
	var effects: Dictionary = parsed["effects"]
	for fxname in effects:
		var cfg: Dictionary = effects[fxname]
		var e: Dictionary = files[String(cfg["file"])]
		var anims: Array = e["anims"]
		var amap: Dictionary = e.get("anim_map", {})
		var ai: int = int(cfg.get("anim", amap.get("PLAY", {}).get("anim", -1)))
		assert_true(ai >= 0 and ai < anims.size(), "%s anim id 在界内" % fxname)
		var recs: Array = anims[ai]["records"]
		assert_true(recs.size() >= 4, "%s 播一次序列 ≥4 记录" % fxname)
		for r in recs:
			assert_true(int(r["frame"]) < e["frames"].size(),
				"%s 帧引用在界内 (默认效果不取外部引用)" % fxname)
	# 帧资产抽样存在
	var e01: Dictionary = files["01E"]
	for i in range(0, e01["frames"].size(), 20):
		var p := "res://assets/fx/01E/%s" % e01["frames"][i]["file"]
		assert_true(ResourceLoader.exists(p), "特效帧存在: " + p)


func test_攻击产事件() -> void:
	var setup: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var b := Battle.start(setup, 7, null)
	for i in 2000:
		b.tick()
		if b.finished:
			break
	assert_true(b.fx_events.size() > 0, "应有攻击特效事件产生")
	for ev in b.fx_events:
		assert_eq(ev.get("type", ""), "attack", "事件类型")
		assert_true(ev.get("from_cell", []).size() == 2 and ev.get("to_cell", []).size() == 2,
			"双方格坐标")
		assert_true(ev.get("hit") is bool and int(ev.get("damage", -1)) >= 0, "命中/伤害字段")
	assert_true(b.fx_events.size() <= b.fx_events_keep, "事件流封顶 (%d ≤ %d)" % [
		b.fx_events.size(), b.fx_events_keep])


func test_职业覆盖配置() -> void:
	var setup: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var fx: Dictionary = JSON.parse_string(
		FileAccess.get_file_as_string("res://data/attack_effects.json"))
	var effects: Dictionary = fx["effects"]
	for k in setup.get("attack_effects", {}):
		assert_true(effects.has(String(setup["attack_effects"][k])),
			"attack_effects[%s] 指向已定义特效" % k)
	# 回退语义: 未知效果名不在表中 → 视图不播 (数据侧验证)
	assert_false(effects.has("__nope__"), "未知特效名不在表")
