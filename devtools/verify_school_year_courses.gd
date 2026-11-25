extends SceneTree
## Play the October school weeks through the same session commands as the UI.
## Keep comparison inputs in an explicitly supplied, empty evidence directory.
const Model := preload("res://sim/school_playground.gd")

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size()!=2 or not DirAccess.dir_exists_absolute(args[1]) or not DirAccess.get_files_at(args[1]).is_empty():
		printerr("Expected the October week-one save and an empty output directory")
		quit(1)
		return
	var model := Model.new()
	var restored := model.load_file(args[0])
	if not restored.supported or model.export_save().version!=31:
		printerr("October opening save rejected ",restored.get("reason",""))
		quit(1)
		return
	for date in [[10,1],[10,2],[10,3],[10,4],[10,5],[11,1]]:
		if not _play_week(model,date,args[1]):
			printerr("Week failed ",date," at ",model.stage())
			quit(1)
			return
	var saved := model.save_file(args[1].path_join("november-two.json"))
	print("Final school ",model.export_save().state_sha256)
	quit(0 if saved.supported else 1)

func _command(model: Model, op: String) -> bool:
	var result := model.execute({"op":op})
	if not result.supported:printerr(op," ",result.get("reason"))
	return result.supported

func _play_week(model: Model, date: Array, directory: String) -> bool:
	var before: Dictionary = model.read_postbattle().bundle
	if model.stage()!="returned_school" or [before.school.month,before.school.week]!=date:
		return false
	if not _command(model,"return_settle"):return false
	var after: Dictionary = model.read_postbattle().bundle
	var file := FileAccess.open(directory.path_join("settlement-%02d-%d.json"%date),FileAccess.WRITE)
	if file==null:return false
	file.store_string(JSON.stringify({"before":before,"after":after}))
	file.close()
	if model.execute({"op":"return_settle"}).supported:return false
	if not _command(model,"course_story") or not _command(model,"post_skip"):return false
	if not _command(model,"post_next"):return false
	if model.stage()=="new_week_story" and not _command(model,"post_skip"):return false
	if model.stage()!="post_workroom" or not _command(model,"post_school"):return false
	if model.stage()=="school_entry_story" and not _command(model,"post_skip"):return false
	var returned: Dictionary=model.read_postbattle().bundle.school
	var expected := [date[0],date[1]+1] if date[1]<5 else [date[0]+1,1]
	print("Returned ",[returned.month,returned.week]," with ",returned.student_count," students")
	return model.stage()=="returned_school" and [returned.month,returned.week]==expected and returned.student_count==16
