extends RefCounted
## Dated CH003, CH001 and CH002 sections for the existing school session.
const Roles := preload("res://sim/all_result_role_replay.gd")
const PATH := "res://data/school_year_october_continuation.json"
const SHA := "9ae5d47f6d49a0623f4aed39f86a20b79dfd5a265049e908ed75b66be5570781"


const NOVEMBER_SHA := "eee1d7ed1c0a7c769c767073f64423150822a3a608b3757a873b4166e1dc2f01"


const NOVEMBER_FIVE_SHA := "d26b6a0ac4ba24e9ddb47cada2b0147fb0f4d1b06e329d1ed859187625230896"


const DECEMBER_ONE_SHA := "2b1d8314ca688c0d559b44c0085de68ddd3399ef9ac901506290590ef57e77f1"


const DECEMBER_TWO_SHA := "efbe777908b59b088c8945f1952a9b45f8a68cfd57f877bfaf586e2bbade2ed2"


static func _source(month: int, arrival_week: int) -> Dictionary:
	var path := PATH
	var digest := SHA
	if month==11 and arrival_week==3:
		path="res://data/school_year_november_three.json"
		digest=NOVEMBER_SHA
	elif month==11 and arrival_week==5:
		path="res://data/school_year_november_five.json"
		digest=NOVEMBER_FIVE_SHA
	if month==12 and arrival_week==1:
		path="res://data/school_year_december_one.json"
		digest=DECEMBER_ONE_SHA
	if month==12 and arrival_week==2:
		path="res://data/school_year_december_two.json"
		digest=DECEMBER_TWO_SHA
	var raw := FileAccess.get_file_as_string(path).replace("\r\n","\n")
	if raw.sha256_text() != digest:return {}
	return Roles._integers(JSON.parse_string(raw))


static func has_departure(month: int, week: int) -> bool:
	return (month==10 and week in range(2,6)) or (month==11 and week in [1,2,4,5]) or [month,week]==[12,1]


static func has_arrival(month: int, week: int) -> bool:
	return (month==10 and week in range(3,6)) or (month==11 and week in [1,2,3,5]) or (month==12 and week in [1,2])


static func story(month: int, week: int) -> Dictionary:
	var data := _source(month+1,1) if week==5 else _source(month,week+1)
	for route in data.get("arrivals",[]):
		if route.departure != [month,week]:continue
		var card: Dictionary = route.date_card
		if not FileAccess.file_exists(card.image) or FileAccess.get_sha256(card.image)!=card.png_sha256:
			return {"supported":false,"reason":"school_year_date_card_changed"}
		var result := {"supported":true,"date_card":card}
		for section in range(3):
			var pages := []
			var chapter: Variant = route.sections[section].chapter
			if chapter != null:
				for scene in data.scenes:
					if scene.chapter==chapter:
						pages=scene.pages
						break
				if pages.is_empty():return {"supported":false,"reason":"missing_school_year_chapter"}
			result[["pre_week","week_start","school_entry"][section]]=pages
		if [month,week]==[12,1]:
			var scene: Dictionary=data.scenes[0]
			result.pre_week=scene.pages.filter(func(p):return p.text_indices[0]<47)
			result.choice_labels=scene.choice_labels
			result.choice_pages=[scene.pages.filter(func(p):return p.text_indices[0]>=49 and p.text_indices[0]<93),
				scene.pages.filter(func(p):return p.text_indices[0]>=93)]
		return result
	return {"supported":false,"reason":"missing_school_year_route"}


static func apply_arrival_effects(after: Dictionary, at_school: bool) -> bool:
	var data := _source(after.school.month,after.school.week)
	for route in data.get("arrivals",[]):
		if route.arrival != [after.school.month,after.school.week]:continue
		var section: Dictionary=route.sections[2 if at_school else 1]
		for effect in section.effects:
			match effect.opcode:
				145:
					var key := "chapter071_absent" if effect.operands[0]==2 else "chapter076_absent"
					if after.get(key,{}).get("participants",{}).get("character_id")!=effect.operands[0]:return false
				151:
					after.flags["0x7a55f6"]=effect.operands[0]
					after.flags["0x7e11a0"]=effect.operands[1]
				91:
					after.adv_background=effect.operands[0]
				_:
					return false
		return true
	return false
