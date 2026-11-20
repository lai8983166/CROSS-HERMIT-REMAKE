extends RefCounted
## Rebuild the terminal battle facts from commands and the saved departure.
const Sortie := preload("res://sim/school_sortie_session.gd")
const Record := preload("res://sim/school_battle_record.gd")
static var _cache: Dictionary = {}


static func replay(handoff: Dictionary, trace: Variant) -> Dictionary:
	if not Record.valid_trace(trace,true,handoff.get("date")==[5,4],handoff.get("date")==[5,5],handoff.get("date")==[6,1],handoff.get("date")==[6,2]):
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
