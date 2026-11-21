extends "res://sim/tests/test_base.gd"
const Record := preload("res://sim/school_sortie_record.gd")


func test_training_accepts_returning_students_on_the_scene_17_map() -> void:
	var trace := {"version":1,"ticks":0,"overflow":false,"commands":[[0,1,1],[0,3,17,95,143],[0,4,16,1235]]}
	assert_true(Record.valid_trace(trace,[8,4],17))
	for scene in [8,20,21]:
		assert_false(Record.valid_trace(trace,[8,4],scene))
	assert_false(Record.valid_trace(trace,[8,3],17))
	for bad_command in [[0,3,17,96,143],[0,3,17,95,144],[0,7,3,15,15],[0,2]]:
		var bad := trace.duplicate(true)
		bad.commands=[bad_command]
		assert_false(Record.valid_trace(bad,[8,4],17))


func test_fifth_teacher_and_training_script_pages() -> void:
	var helpers=preload("res://sim/tests/test_school_sortie_session.gd").new()
	var handoff: Dictionary=helpers.handoff(17)
	handoff.date=[8,4]
	handoff.prepared.rounds[0].teacher_ids=[116]
	var session := Record.Sortie.new()
	assert_true(session.open(handoff))
	if not session.ready:return
	assert_eq(session.opening_snapshot().page_count,3)
	assert_eq(session._pages(14).size(),2)
	for sub in [2,5,8,11]:assert_eq(session._pages(sub).size(),1)
	session.close()
	handoff.date=[7,5]
	assert_false(session.open(handoff))
