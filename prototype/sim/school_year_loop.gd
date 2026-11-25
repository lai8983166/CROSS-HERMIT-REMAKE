extends RefCounted
## Dated CH003, CH001 and CH002 sections for the existing school session.
const Roles := preload("res://sim/all_result_role_replay.gd")
const PATH := "res://data/school_year_october_continuation.json"
const SHA := "9ae5d47f6d49a0623f4aed39f86a20b79dfd5a265049e908ed75b66be5570781"


static func _source() -> Dictionary:
	var raw := FileAccess.get_file_as_string(PATH).replace("\r\n","\n")
	if raw.sha256_text() != SHA:return {}
	return Roles._integers(JSON.parse_string(raw))


static func has_departure(month: int, week: int) -> bool:
	return (month==10 and week in range(2,6)) or (month==11 and week==1)


static func has_arrival(month: int, week: int) -> bool:
	return (month==10 and week in range(3,6)) or (month==11 and week in [1,2])


static func story(month: int, week: int) -> Dictionary:
	var data := _source()
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
		return result
	return {"supported":false,"reason":"missing_school_year_route"}


static func apply_arrival_effects(after: Dictionary, at_school: bool) -> bool:
	var data := _source()
	for route in data.get("arrivals",[]):
		if route.arrival != [after.school.month,after.school.week]:continue
		var section: Dictionary=route.sections[2 if at_school else 1]
		for effect in section.effects:
			match effect.opcode:
				151:
					after.flags["0x7a55f6"]=effect.operands[0]
					after.flags["0x7e11a0"]=effect.operands[1]
				91:
					after.adv_background=effect.operands[0]
				_:
					return false
		return true
	return false
