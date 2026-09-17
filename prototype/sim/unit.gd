class_name SimUnit
extends RefCounted
## 战斗单位数据 (字段语义 = 原作 wk 属性块, character_growth.md §1.3)
## 七属性顺序: 力/敏/感/活/智/耐/精 = str/agi/sen/vir/int/con/spi
## v1 只承载战斗数值; 成长池/技能槽属未来 change

var strength := 0      # 力 (+0x0C)
var agility := 0       # 敏 (+0x14)
var sense := 0         # 感 (+0x1C)
var vitality := 0      # 活 (+0x24)
var intellect := 0     # 智 (+0x2C)
var constitution := 0  # 耐 (+0x34)
var spirit := 0        # 精 (+0x3C)

var job_id := 0        # 职业 (wk+0xE, → SimTables.job)
var level := 1         # 等级 (wk+0xF)

var hp := 0            # 现值/上限 (wk+0x18/+0x16)
var hp_max := 0
var mp := 0            # (wk+0x1E/+0x1C)
var mp_max := 0

var evasion := 0       # 回避 (wk+0x4D)
var armor := 0         # 装甲/防御 (wk+0x4E)
var magic_resist := 0  # 魔抗 (wk+0x50)
var mental_resist := 0 # 精神抗性 (wk+0x52)


func _init(stats: Dictionary = {}) -> void:
	for k in stats:
		if get(k) != null:
			set(k, stats[k])
