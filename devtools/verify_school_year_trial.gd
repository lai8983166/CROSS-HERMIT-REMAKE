extends SceneTree
## Check the shipped command tape and the October starting state in a fresh process.
const Trial := preload("res://ui/school_year_trial.gd")

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var trial := Trial.new()
	var result := trial.open(false)
	if not result.supported:
		printerr(result.reason)
		quit(1)
		return
	var model: RefCounted=result.model
	var file: Dictionary=model.export_save()
	var school: Dictionary=model.read_postbattle().bundle.school
	var ok: bool=file.version==31 and file.state_sha256==Trial.OCTOBER_STATE and [school.month,school.week]==[10,1]
	print("October trial ",file.version," ",file.state_sha256)
	quit(0 if ok else 1)
