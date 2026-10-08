extends SceneTree
## One-time pre-version3 capture. Refuses to regenerate with changed controller.
const Playground := preload("res://sim/school_playground.gd")

func _initialize() -> void:
	var model := Playground.new()
	model.start()
	for command in [{"op":"mode","group":0,"teaching":true},{"op":"course","group":0,"course":10},
			{"op":"grow"},{"op":"confirm"},{"op":"complete"},{"op":"story_start"}]:
		assert(model.execute(command)["supported"])
	for index in range(68):
		assert(model.execute({"op":"story_next"})["supported"])
	var cases: Array = [{"name":"second_scene","save":model.export_save(),"state":model.state()}]
	model.execute({"op":"story_skip"})
	model.execute({"op":"week"})
	cases.append({"name":"arrival","save":model.export_save(),"state":model.state()})
	assert(cases[0]["save"]["version"] == 2)
	var path := "res://data/school_playground_legacy_v2.json"
	assert(not FileAccess.file_exists(path))
	var file := FileAccess.open(path,FileAccess.WRITE)
	file.store_string(JSON.stringify({"source_commit":"b88b4b4","cases":cases},"  ",true)+"\n")
	file.close()
	print("Captured original version2 second-scene and arrival saves")
	quit()
