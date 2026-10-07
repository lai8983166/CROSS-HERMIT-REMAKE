extends "res://sim/tests/test_base.gd"
const Playground := preload("res://sim/school_playground.gd")

func _ready_model():
	var model := Playground.new()
	assert_true(model.start()["supported"])
	return model

func _course(model, group := 0, course := 10) -> void:
	assert_true(model.execute({"op":"mode","group":group,"teaching":true})["supported"])
	assert_true(model.execute({"op":"course","group":group,"course":course})["supported"])

func test_completed_replay_and_once_only() -> void:
	var model = _ready_model()
	_course(model)
	for op in ["grow","confirm","complete"]:
		assert_true(model.execute({"op":op})["supported"])
	assert_eq(model.stage(),"completed")
	var saved: Dictionary = model.export_save()
	var restored = _ready_model()
	assert_true(restored.restore_text(JSON.stringify(saved))["supported"])
	assert_eq(restored.state(),model.state())
	assert_eq(restored.export_save(),saved)
	for op in ["grow","confirm","complete"]:
		assert_true(restored.execute({"op":op})["supported"])
	assert_eq(restored.export_save(),saved,"duplicates never become save commands")
	assert_false(restored.state()["result"]["adv_request"]["week_advanced"])

func test_partial_and_moved_class_replay() -> void:
	var model = _ready_model()
	assert_true(model.execute({"op":"move","kind":"teacher","member_id":101,"target_group":2,"target_slot":-1})["supported"])
	for pair in [[4,0],[9,1]]:
		assert_true(model.execute({"op":"move","kind":"student","member_id":pair[0],"target_group":2,"target_slot":pair[1]})["supported"])
	_course(model,2,11)
	for op in ["grow","confirm","complete"]:
		var candidate = _ready_model()
		assert_true(candidate.restore(model.export_save())["supported"])
		assert_eq(candidate.state(),model.state())
		assert_true(model.execute({"op":op})["supported"])
	assert_eq(model.state()["result"]["recipient"],4)
	var candidate = _ready_model()
	assert_true(candidate.restore(model.export_save())["supported"])
	assert_eq(candidate.state(),model.state())

func test_refusals_are_atomic_and_owned() -> void:
	var model = _ready_model()
	_course(model)
	var before: Dictionary = model.state()
	var good: Dictionary = model.export_save()
	var bad: Dictionary = good.duplicate(true)
	bad["commands"].append({"op":"complete"})
	assert_false(model.restore(bad)["supported"])
	bad = good.duplicate(true); bad["version"] = 2
	assert_false(model.restore(bad)["supported"])
	bad = good.duplicate(true); bad["rules"]["school"] = "changed"
	assert_false(model.restore(bad)["supported"])
	bad = good.duplicate(true); bad["state_sha256"] = "0".repeat(64)
	assert_false(model.restore(bad)["supported"])
	bad = good.duplicate(true); bad["commands"] = [{"op":"mode","group":0,"teaching":true,"injected":1}]
	assert_false(model.restore(bad)["supported"])
	bad = good.duplicate(true); bad["commands"] = [{"op":"mode","group":0,"teaching":true},{"op":"mode","group":0,"teaching":true}]
	assert_false(model.restore(bad)["supported"])
	bad = good.duplicate(true); bad["commands"].resize(513)
	assert_false(model.restore(bad)["supported"])
	assert_false(model.restore_text("x".repeat(Playground.MAX_BYTES+1))["supported"])
	assert_false(model.restore_text("{broken}")["supported"])
	assert_eq(model.state(),before)
	good["commands"].clear()
	assert_eq(model.export_save()["commands"].size(),2)
	assert_false(model.execute({"op":"course","group":0,"course":10.5})["supported"])
	assert_eq(model.state(),before)

func test_file_recovery_and_write_failure() -> void:
	var path := "user://test_school_playground_save.json"
	for suffix in ["",".bak",".tmp",".corrupt"]:
		if FileAccess.file_exists(path+suffix):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
	var model = _ready_model()
	assert_true(model.save_file(path)["supported"])
	var first: Dictionary = model.state()
	_course(model)
	assert_true(model.save_file(path)["supported"])
	var fresh = _ready_model()
	assert_true(fresh.load_file(path)["supported"])
	assert_eq(fresh.state(),model.state())
	var broken := FileAccess.open(path,FileAccess.WRITE)
	broken.store_string("invalid"); broken.close()
	assert_eq(fresh.load_file(path)["status"],"recovered_backup")
	assert_eq(fresh.state(),first)
	assert_true(fresh.save_file(path)["supported"])
	assert_eq(FileAccess.get_file_as_string(path+".corrupt"),"invalid")
	assert_true(FileAccess.file_exists(path+".bak"))
	var before: Dictionary = fresh.state()
	assert_false(fresh.save_file("user://missing_playground_directory/state.json")["supported"])
	assert_eq(fresh.state(),before)
	for suffix in ["",".bak",".tmp",".corrupt"]:
		if FileAccess.file_exists(path+suffix):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path+suffix))
