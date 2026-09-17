class_name SimDerive
## 战备合成 — 进战斗前的派生上限 (原作 4b93c0, 见 character_growth.md §2 / REMAKE_BLUEPRINT.md §2)
## 整数运算, /100 向零截断 (Godot int 语义与 C 一致)

## mods: {"hp": int, "mp": int, "spirit": int} 装备/技能加成合计 (0x4C 缓冲对应槽, v1 由外部传入)
static func derive_limits(u: SimUnit, job: Dictionary, mods: Dictionary = {}) -> Dictionary:
	var m_hp: int = mods.get("hp", 0)
	var m_mp: int = mods.get("mp", 0)
	var m_sp: int = mods.get("spirit", 0)
	var hp_coef: int = job.get("hp_coef", 100)
	var mp_coef: int = job.get("mp_coef", 100)
	var sp_coef: int = job.get("spirit_coef", 100)

	# HP = (耐×3 + 力 + 敏 + 修正) × hp_coef / 100, clamp 1..999 — 见 character_growth.md §2
	var hp_max: int = clampi(
		(u.constitution * 3 + u.strength + u.agility + m_hp) * hp_coef / 100, 1, 999)
	# MP = (精×3 + 智 + 活 + 修正) × mp_coef / 100, clamp 30..999
	var mp_max: int = clampi(
		(u.spirit * 3 + u.intellect + u.vitality + m_mp) * mp_coef / 100, 30, 999)
	# 精神系 = (感×3 + 智 + 活 + 修正) × spirit_coef / 100, clamp 1..999
	# (旧档写"精×3+智+感?"; 4b93c0 实参核对 = 感×3 + 智 + 活)
	var spirit_max: int = clampi(
		(u.sense * 3 + u.intellect + u.vitality + m_sp) * sp_coef / 100, 1, 999)

	return {"hp_max": hp_max, "mp_max": mp_max, "spirit_max": spirit_max}
