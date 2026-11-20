extends RefCounted
## T0013 tablets and 434300's continuous six-region requirement.
const MASKS := [3,24,24,31,31,31]
var discovered := {}
var cells := {}
var previous := {}
var regions := {}
var reading := 0
var occupied := 0
var duration := 0
var last_clock := -1


func start(s) -> void:
	for number in range(1,10):
		for index in s.catalog.regions[str(number)]:regions[index]=number
	for unit in s.controlled_units():
		cells[unit.instance_id]=unit.cell
		previous[unit.instance_id]=0


func check_event(s) -> bool:
	for unit in s.controlled_units():
		if unit.side!=0 or unit.source_state!=1 or unit.limits.hp<=0:continue
		var id: int=unit.instance_id
		if cells[id]==unit.cell:continue
		cells[id]=unit.cell
		var region: int=regions.get(unit.cell.y*s.field_width+unit.cell.x,0)
		if region>3 or discovered.has(region):region=0
		var entered: bool=previous[id]!=region and region>0
		previous[id]=region
		if entered:
			reading=region
			s._event_pages=s._pages(region,1)
			s._event_index=0
			s._ending_phase="event20"
			s._accumulator=0.0
			return true
	return false


func finish_event(s) -> void:
	discovered[reading]=true
	reading=0
	s._ending_phase="active"
	s.reason="ready"


func held(s) -> bool:
	if discovered.size()!=3 or last_clock==s._trace_clock:return duration>=300
	last_clock=s._trace_clock
	var pads := {}
	for unit in s.controlled_units():
		if unit.side!=0 or unit.source_state!=1 or unit.limits.hp<=0:continue
		var region: int=regions.get(unit.cell.y*s.field_width+unit.cell.x,0)
		if region>=4 and unit.family_bit & MASKS[region-4]:pads[region]=true
	occupied=pads.size()
	duration=duration+1 if occupied==6 else 0
	return duration>=300
