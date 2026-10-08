extends SceneTree
## Capture before v4 implementation; this must never regenerate newer snapshots.
const Playground := preload("res://sim/school_playground.gd")

func _initialize() -> void:
	var model := Playground.new()
	assert(model.start()["supported"])
	for command in [{"op":"mode","group":0,"teaching":true},{"op":"course","group":0,"course":10},
			{"op":"grow"},{"op":"confirm"},{"op":"complete"},{"op":"story_start"},
			{"op":"story_skip"},{"op":"week"},{"op":"fifth_start"}]:
		assert(model.execute(command)["supported"])
	for index in range(121):
		assert(model.execute({"op":"fifth_next"})["supported"])
	var cases: Array = [{"name":"portrait_replacements","save":model.export_save(),"state":model.state()}]
	assert(model.execute({"op":"fifth_skip"})["supported"])
	assert(model.execute({"op":"fifth_finish"})["supported"])
	cases.append({"name":"workroom_entry","save":model.export_save(),"state":model.state()})
	assert(cases[0]["save"]["version"] == 3)
	var path := "res://data/school_playground_legacy_v3.json"
	assert(not FileAccess.file_exists(path))
	var file := FileAccess.open(path,FileAccess.WRITE)
	file.store_string(JSON.stringify({"source_commit":"dfd0737","cases":cases},"  ",true)+"\n")
	file.close()
	print("Captured genuine v3 partial fifth dialogue and completed workroom entry")
	quit()
