extends RefCounted
## Rebuild the terminal battle facts from commands and the saved departure.
const Sortie := preload("res://sim/school_sortie_session.gd")
const Record := preload("res://sim/school_battle_record.gd")
static var _cache: Dictionary = {}


static func valid_trace(trace: Variant, date: Variant, scene_id: Variant) -> bool:
	if trace is Dictionary and trace.get("version")==2:
		if date!=[7,4] or scene_id!=14 or trace.size()!=2 or not trace.get("floors") is Array or trace.floors.size() not in [2,3]:return false
		if not trace.floors[0] is Dictionary or trace.floors[0].get("version")!=1 or not valid_trace(trace.floors[0],date,scene_id):return false
		for i in range(1,trace.floors.size()):
			if not Record.valid_winter_trace(trace.floors[i],Vector2i(128,192),64 if i==1 else 62):return false
		return true
	var winter: bool=scene_id in Sortie.Winter.DATES
	if date==[10,1] or scene_id==33:
		return date==[10,1] and scene_id==33 and Record.valid_winter_trace(trace,Vector2i(128,192),83)
	if date==[9,5] or scene_id==11:
		return date==[9,5] and scene_id==11 and Record.valid_winter_trace(trace,Vector2i(64,192),100)
	if winter or date in Sortie.Winter.DATES.values():
		if not winter or date!=Sortie.Winter.DATES[scene_id]:return false
		return Record.valid_winter_trace(trace,Sortie.Winter.MAP_SIZE[scene_id],Sortie.Winter.TEMPLATES[scene_id])
	var thirty_one: bool=date==[12,1] and scene_id==31
	if (date==[12,1] or scene_id==31) and not thirty_one:return false
	var forty_one: bool=date==[11,3] and scene_id==41
	if (date==[11,3] or scene_id==41) and not forty_one:return false
	var twenty_four: bool=date==[9,4] and scene_id==24
	if (date==[9,4] or scene_id==24) and not twenty_four:return false
	var twenty_two: bool=date==[9,3] and scene_id==22
	if (date==[9,3] or scene_id==22) and not twenty_two:return false
	var thirty_five: bool=date==[8,5] and scene_id==35
	if (date==[8,5] or scene_id==35) and not thirty_five:return false
	var twenty_one: bool=date==[8,3] and scene_id==21
	if (date==[8,3] or scene_id==21) and not twenty_one:return false
	var twenty: bool=date==[8,2] and scene_id==20
	if (date==[8,2] or scene_id==20) and not twenty:return false
	var fourteen: bool=date==[7,4] and scene_id==14
	if (date==[7,4] or scene_id==14) and not fourteen:return false
	var nine: bool=date==[7,3] and scene_id==9
	if (date==[7,3] or scene_id==9) and not nine:return false
	var optional_week: bool=date in [[7,1],[7,2],[7,5],[8,4]]
	if optional_week and scene_id not in ([17,18] if date==[7,1] else [17]):return false
	return Record.valid_trace(trace,true,date==[5,4],date==[5,5],date==[6,1],date==[6,2],
		date==[6,3],date==[6,4],date==[6,5] or (optional_week and scene_id==17),date==[7,1] and scene_id==18,nine,fourteen,date in [[7,5],[8,4]],twenty,twenty_one,thirty_five,twenty_two,twenty_four,forty_one,thirty_one)


static func replay(handoff: Dictionary, trace: Variant) -> Dictionary:
	if not handoff.get("prepared") is Dictionary:return {"supported":false,"reason":"invalid_sortie_handoff"}
	if not valid_trace(trace,handoff.get("date"),handoff["prepared"].get("adventure_id")):
		return {"supported":false,"reason":"invalid_sortie_trace"}
	var session := Sortie.new()
	if not session.open(handoff):
		return {"supported":false,"reason":"invalid_sortie_handoff"}
	var key := JSON.stringify([handoff,trace],"",true).sha256_text()
	if _cache.has(key): return _cache[key].duplicate(true)
	var floors: Array=trace.floors if trace.get("version")==2 else [trace]
	for i in floors.size():
		if i>0:
			var next: Sortie=session.next_floor()
			if next==null:return {"supported":false,"reason":"sortie_floor_transition_rejected"}
			session=next
		var run := Record.run_trace(session,floors[i])
		if not run["supported"]: return run
	var facts := session.result_inputs()
	if facts.is_empty() or session.sortie_trace()!=trace:
		return {"supported":false,"reason":"sortie_objective_not_reached"}
	var result := {"supported":true,"facts":facts}
	if _cache.size()>=4: _cache.erase(_cache.keys()[0])
	_cache[key]=result.duplicate(true)
	return result
