extends SceneTree
const Mission := preload("res://sim/school_two_battle.gd")

class Sample:
	var _event_pages: Array
	var _event_index := -1
	var _ending_phase := "active"
	var _accumulator := 1.0
	var _own_casualties := 0
	var remaining_ticks := 2
	var cell_region := "0"
	var owned := 3
	func controlled_units() -> Array:
		return [{}]
	func _on_region(_unit, region) -> bool:
		return region == cell_region
	func _pages(sub, block) -> Array:
		return [block, sub]
	func find_unit(id) -> Dictionary:
		return {"side":0 if 1249-id < owned else 5,"source_state":1}

func _initialize() -> void:
	var s := Sample.new()
	var m := Mission.new()
	var observed := [m.result(s,false)]
	s.cell_region = "1"
	observed.append(m.result(s,false))
	observed.append(s._event_pages.duplicate())
	s._ending_phase = "active"
	observed.append(m.result(s,false))
	observed.append(s._ending_phase)
	observed.append(m.result(s,true))
	s.remaining_ticks = 0
	observed.append(m.result(s,true))
	s.cell_region = "2"
	observed.append(m.result(s,true))
	s._own_casualties = 1
	observed.append(m.result(s,true))
	s.owned = 2
	observed.append(m.result(s,true))
	var expected := [-1,-1,[1,1],-1,"active",14,11,2,5,8]
	print("MAP02 result branches ",observed)
	quit(0 if observed == expected else 1)
