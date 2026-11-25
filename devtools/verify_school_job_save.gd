extends SceneTree
const Model := preload("res://sim/school_playground.gd")
const PARENT_SHA := "3c1eee1843f5835493569835514268d4cb81a6dcc8dad69d3c393d592eb9d82e"

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size()!=2 or FileAccess.get_sha256(args[0])!=PARENT_SHA or FileAccess.file_exists(args[1]):
		printerr("Expected the October week-one parent and a new output path")
		quit(1)
		return
	var model := Model.new()
	if not model.load_file(args[0]).supported:
		quit(1)
		return
	var command := {"op":"return_job","member":3,"job":2}
	var student: Dictionary=model.read_postbattle().bundle.participants[0]
	if [student.character_id,student.job]!=[3,10] or not model.execute(command).supported:
		quit(1)
		return
	var expected := model.export_save()
	if expected.version!=34 or expected.commands.back()!=command or not model.execute(command).supported or model.export_save()!=expected:
		quit(1)
		return
	if not model.save_file(args[1]).supported:
		quit(1)
		return
	var fresh := Model.new()
	var loaded := fresh.load_file(args[1])
	if not loaded.supported or fresh.export_save()!=expected or fresh.read_postbattle().bundle.participants[0].job!=2:
		printerr("Job save replay failed ",loaded.get("reason",""))
		quit(1)
		return
	var modified := expected.duplicate(true)
	modified.rules.job_change="changed"
	if fresh.restore(modified).supported or fresh.export_save()!=expected:
		quit(1)
		return
	print("Verified v34 job 10 -> 2, duplicate confirmation and changed rules rejected, state ",expected.state_sha256)
	quit(0)
