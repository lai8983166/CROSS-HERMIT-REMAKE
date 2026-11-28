extends "res://sim/tests/test_base.gd"
const Mission := preload("res://sim/school_eleven_battle.gd")

class Field:
	var catalog: Dictionary
	var scene_scripts: Array
	var elapsed := 0
	var frame := 12
	var gate_state := 1
	var phases := {1183:{}}
	var units := [{"instance_id":1183,"side":5,"source_state":1,"limits":{"hp":40},"path":[Vector2i.DOWN]}]
	var arrivals: Array=[]
	func controlled_units() -> Array:return []
	func find_unit(_id):return {"source_state":gate_state}
	func _on_region(_unit, region):return region=="1"
	func _spawn_group(group,cell,radius):arrivals.append([group,cell,radius])
	func _activate(id,cell,radius):arrivals.append([-id,cell,radius])

func test_original_reinforcement_script_and_escape() -> void:
	var field := Field.new()
	var raw := FileAccess.get_file_as_string("res://assets/school_eleven/catalog.json")
	var data: Dictionary=preload("res://sim/school_combat_limits.gd")._source_numbers(JSON.parse_string(raw))
	field.catalog=data.scenes["11"]
	field.scene_scripts=field.catalog.scripts
	var mission := Mission.new()
	mission.start(field)
	assert_eq(mission.timers.size(),7)
	field.elapsed=10800
	mission.advance(field)
	assert_eq(field.arrivals,[[12,Vector2i(60,22),3]])
	assert_eq([mission.escaped,field.units[0].source_state,field.phases.size()],[1,2,0])
	field.elapsed=25200
	field.gate_state=4
	mission.advance(field)
	mission.advance(field)
	assert_eq(field.arrivals,[[12,Vector2i(60,22),3],[-1183,Vector2i(21,21),10],[18,Vector2i(27,4),3]])
	assert_eq(mission.escaped,1)

func test_escape_grades() -> void:
	var mission := Mission.new()
	var actual := []
	for escaped in [0,1,3,4,9,10]:
		mission.escaped=escaped
		actual.append(mission.result(0,false))
	assert_eq(actual,[2,5,5,8,8,11])
	mission.escaped=0
	assert_eq([mission.result(20,true),mission.result(20,false)],[14,-1])
