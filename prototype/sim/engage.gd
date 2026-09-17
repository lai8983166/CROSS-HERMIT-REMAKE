class_name SimEngage
## ENGAGE TIME 计算 (原作 4b93c0 状态合成, 见 battle_mechanics.md §8 / REMAKE_BLUEPRINT.md §4.1)
## engage = 修正h×3600 + 表[clamp(等级,0,50)]×60 + 修正s, clamp(1, 356400)  [单位: 秒]
## 表以分钟存储 (data/engage_table.json), ×60 换算发生在消费侧 (design 决策 5)

static func engage_seconds(level: int, mod_h: int = 0, mod_s: int = 0) -> int:
	var rows := SimTables.engage_rows()
	var lv := clampi(level, 0, 50)
	var minutes: int = rows[lv].minutes  # lv1~5=5940(99h 封顶), lv50=540
	return clampi(mod_h * 3600 + minutes * 60 + mod_s, 1, 356400)
