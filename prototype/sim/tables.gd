class_name SimTables
## 数据表单点加载与缓存 (res://data/*.json, 由 tools/table_export.py 产出)
## 表结构与地址溯源见各 JSON 的 _meta.naming_ref 与 docs/REMAKE_BLUEPRINT.md §7

static var _cache: Dictionary = {}


static func _load(table: String) -> Dictionary:
	if not _cache.has(table):
		var filename := "%s.json" % table if table in ["skill_visuals", "attack_effects"] \
			else "%s_table.json" % table
		var txt := FileAccess.get_file_as_string("res://data/%s" % filename)
		if txt.is_empty():
			push_error("数据表缺失: %s" % filename)
			return {}
		var parsed: Variant = JSON.parse_string(txt)
		if parsed == null or not parsed is Dictionary:
			push_error("数据表解析失败: %s" % filename)
			return {}
		_cache[table] = parsed
	return _cache[table]


static func rows(table: String) -> Array:
	return _load(table).get("rows", [])


## 职业行 (id == 行序, 0..29)
static func job(id: int) -> Dictionary:
	var r := rows("job")
	return r[id] if 0 <= id and id < r.size() else {}


## 攻击/技能行 (id == 行序, 0..1025)
static func attack(id: int) -> Dictionary:
	var r := rows("attack")
	return r[id] if 0 <= id and id < r.size() else {}


## 技能视觉明细行 (0x611538；与攻击表玩法字段分离)
static func skill_visual(id: int) -> Dictionary:
	var r := rows("skill_visuals")
	return r[id] if 0 <= id and id < r.size() else {}


## 4DE8F0 selects the indexed skill-attribute row for ids < 101, otherwise the fallback row.
static func skill_attribute(id: int) -> Dictionary:
	if id < 0:
		return {}
	var data := _load("skill_attributes")
	var r: Array = data.get("rows", [])
	return r[id] if id < r.size() else data.get("fallback", {})


## EFCT 全局动画行；缺失 ID 安全返回空字典。
static func fx_animation(global_id: int) -> Dictionary:
	var data := _load("attack_effects")
	return data.get("animations", {}).get(str(global_id), {})


## ENGAGE 表行 {level, minutes}
static func engage_rows() -> Array:
	return rows("engage")
