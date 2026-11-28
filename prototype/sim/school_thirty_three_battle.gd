extends "res://sim/school_winter_battle.gd"
## Scene 33, 4359C0. Clearing the field takes priority over the party loss predicate.

static func load_search(catalog: Dictionary) -> bool:
	var raw := FileAccess.get_file_as_string("res://data/school_october_thirty_three_ai.json").replace(String.chr(13),"")
	if raw.sha256_text()!="97f9038452456e746a4aa4913a0821cd224d62dad6d6625903d826e62671c5bb":return false
	var data: Dictionary=Roles._integers(JSON.parse_string(raw))
	var modes:=String(data.search_modes_hex).hex_decode()
	if modes.size()!=catalog.actors.size():return false
	catalog.patrol_routes=data.routes
	for i in catalog.actors.size():
		var actor: Dictionary=catalog.actors[i]
		actor.search_mode=modes[i]
		actor.vision=String(actor.record_hex).hex_decode()[0x2c]
	return true

func start(s) -> void:
	patrol_mask=String(s.catalog.spells.masks["3"]).hex_decode()

func advance(s) -> void:
	_advance_units(s)

static func terminal_sub(elapsed: int, cleared: bool, unavailable: bool) -> int:
	if cleared:
		if elapsed<=36000:return 2
		if elapsed<=54000:return 5
		if elapsed<=108000:return 8
		return 11
	return 11 if unavailable else -1

static func cleared(units: Array) -> bool:
	return not units.any(func(unit):return unit.side==5 and unit.source_state==1 and unit.category==5)
