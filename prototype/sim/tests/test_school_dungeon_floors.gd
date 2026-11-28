extends "res://sim/tests/test_base.gd"
const Dungeon:=preload("res://sim/school_fourteen_dungeon.gd")
const Record:=preload("res://sim/school_sortie_record.gd")

func test_cross_floor_accumulation() -> void:
	var first:={"scene_id":14,"result_selector":1,"objective_slots":[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		"time_key":1,"unit_condition_key":1,"units":[{"character_id":3,"count_field_aa":32764,"contribution_field_ac":2,"status_field_ae":126}]}
	var last:=first.duplicate(true)
	last.scene_id=15
	last.result_selector=4
	last.objective_slots[4]=1
	last.unit_condition_key=2
	var total:=Dungeon.aggregate([first,last])
	assert_eq(total.result_selector,3)
	assert_eq(total.objective_slots.slice(0,5),[1,0,0,0,1])
	assert_eq([total.time_key,total.unit_condition_key,total.dungeon_depth],[0,2,2])
	assert_eq(total.units,[{"character_id":3,"count_field_aa":32767,"contribution_field_ac":4,"status_field_ae":127}])
	assert_eq(first.units[0].contribution_field_ac,2)

func test_trace_envelope_keeps_early_return_and_rejects_malformed_chains() -> void:
	var trace:={"version":1,"overflow":false,"ticks":0,"commands":[]}
	assert_true(Record.valid_trace(trace,[7,4],14))
	assert_true(Record.valid_trace({"version":2,"floors":[trace,trace]},[7,4],14))
	assert_false(Record.valid_trace({"version":2,"floors":[trace]},[7,4],14))
	assert_false(Record.valid_trace({"version":2,"floors":[trace,trace,trace,trace]},[7,4],14))
	assert_false(Record.valid_trace({"version":2,"floors":[trace,trace]},[7,3],9))
	assert_false(Record.valid_trace({"version":2,"floors":[trace,{"version":2,"floors":[]}]},[7,4],14))

class Summit:
	var catalog:={"grade_groups":[[1,2,3,4],[5,6,7,8,9,10]]}
	var controlled: Array=[]
	var remaining_ticks:=10
	var _own_casualties:=0
	func find_unit(identity: int) -> Dictionary:
		return {"side":0 if controlled.has(1250-identity) else 5,"source_state":1}

func test_final_floor_tower_and_spring_precedence() -> void:
	var floor:=Summit.new()
	assert_eq(Dungeon.last_floor_result(floor,false),-1)
	assert_eq(Dungeon.last_floor_result(floor,true),14)
	floor.remaining_ticks=0
	assert_eq(Dungeon.last_floor_result(floor,true),11)
	floor.controlled=[1,2,3,4]
	assert_eq(Dungeon.last_floor_result(floor,false),8)
	floor.controlled.append_array([5,6,7,8,9,10])
	floor._own_casualties=1
	assert_eq(Dungeon.last_floor_result(floor,false),5)
	floor._own_casualties=0
	assert_eq(Dungeon.last_floor_result(floor,false),2)

func test_deployed_summoners_have_source_actions() -> void:
	for floor_id in [15,16]:
		var path:="res://assets/school_dungeon_%d/catalog.json"%floor_id
		var data: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
		var actors: Array=data.scenes[str(floor_id)].actors
		for actor in actors:
			if not actor.has("summon_interval"):continue
			var actions: Dictionary=data.skins[actor.skin_key].actions
			assert_true(actions.has("summon_prepare") and actions.has("summon"),str(actor.instance_id))
