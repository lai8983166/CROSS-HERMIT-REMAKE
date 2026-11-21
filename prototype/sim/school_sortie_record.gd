extends RefCounted
## Rebuild the terminal battle facts from commands and the saved departure.
const Sortie := preload("res://sim/school_sortie_session.gd")
const Record := preload("res://sim/school_battle_record.gd")
static var _cache: Dictionary = {}


static func valid_trace(trace: Variant, date: Variant, scene_id: Variant) -> bool:
	var fourteen: bool=date==[7,4] and scene_id==14
	if (date==[7,4] or scene_id==14) and not fourteen:return false
	var nine: bool=date==[7,3] and scene_id==9
	if (date==[7,3] or scene_id==9) and not nine:return false
	var july: bool=date in [[7,1],[7,2]]
	if july and scene_id not in ([17,18] if date==[7,1] else [17]):return false
	return Record.valid_trace(trace,true,date==[5,4],date==[5,5],date==[6,1],date==[6,2],
		date==[6,3],date==[6,4],date==[6,5] or (july and scene_id==17),july and scene_id==18,nine,fourteen)


static func replay(handoff: Dictionary, trace: Variant) -> Dictionary:
	if not handoff.get("prepared") is Dictionary:return {"supported":false,"reason":"invalid_sortie_handoff"}
	if not valid_trace(trace,handoff.get("date"),handoff["prepared"].get("adventure_id")):
		return {"supported":false,"reason":"invalid_sortie_trace"}
	var session := Sortie.new()
	if not session.open(handoff):
		return {"supported":false,"reason":"invalid_sortie_handoff"}
	var key := JSON.stringify([handoff,trace],"",true).sha256_text()
	if _cache.has(key): return _cache[key].duplicate(true)
	var run := Record.run_trace(session,trace)
	if not run["supported"]: return run
	var facts := session.result_inputs()
	if facts.is_empty() or session.battle_trace()!=trace:
		return {"supported":false,"reason":"sortie_objective_not_reached"}
	var result := {"supported":true,"facts":facts}
	if _cache.size()>=4: _cache.erase(_cache.keys()[0])
	_cache[key]=result.duplicate(true)
	return result
