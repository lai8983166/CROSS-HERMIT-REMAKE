extends SceneTree
## Full campaign verification. Input is the played v35 save and a real battle trace.
const Model := preload("res://sim/school_playground.gd")
const START_SHA := "66a5f47ca9b3dfeea6d1ad65559a807031fee72b844e761443ce470fbd73760f"

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	var model := Model.new()
	if args.size()==1:
		var replayed := model.load_file(args[0])
		var ok: bool=replayed.supported and _final_school(model)
		if ok:
			var tampered := model.export_save()
			tampered.rules["mandatory_forty_one"]="changed"
			ok=not Model.new().restore(tampered).supported
			print("Independently replayed November school ",model.export_save().state_sha256)
		else:printerr("November week four restore failed ",replayed.get("reason"))
		quit(0 if ok else 1)
		return
	if args.size()!=3 or FileAccess.get_sha256(args[0])!=START_SHA or not FileAccess.file_exists(args[1]) or not DirAccess.dir_exists_absolute(args[2]) or not DirAccess.get_files_at(args[2]).is_empty():
		printerr("Expected the v35 parent, a battle trace, and an empty output directory")
		quit(1)
		return
	var loaded := model.load_file(args[0])
	if not loaded.supported or not _play(model,args[1],args[2]):
		printerr("Campaign stopped at ",model.stage()," ",loaded.get("reason",""))
		quit(1)
		return
	quit(0)

func _play(model: Model, trace_path: String, directory: String) -> bool:
	var trace: Dictionary=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(trace_path)))
	trace=trace.get("trace",trace)
	if not _command(model,{"op":"return_depart"}):return false
	var submitted := model.read_postbattle()
	var handoff: Dictionary=submitted.planning.handoff
	var receipt := Model.Postbattle.SortieRecord.replay(handoff,trace)
	if not receipt.supported:
		printerr("Battle replay ",receipt.reason)
		return false
	var invalid_trace := trace.duplicate(true)
	invalid_trace.overflow=true
	if Model.Postbattle.SortieRecord.replay(handoff,invalid_trace).supported:return false
	if not _command(model,{"op":"sortie_finish","trace":trace}):return false
	var settled := model.read_postbattle()
	if not _write(directory.path_join("settled.json"),{"before":submitted.bundle,"after":settled.bundle}):return false
	if not _write(directory.path_join("submission.json"),{"round":handoff.prepared.rounds[0],
			"ratings":handoff.prepared.class_ratings,"facts":receipt.facts}):return false
	for i in range(12):
		var phase := model.stage()
		if phase=="returned_school":break
		var op: String
		match phase:
			"sortie_result":op="post_next"
			"post_story","school_entry_story":op="post_skip"
			"new_week_story":op="post_next" if model.read_postbattle().has("date_card") else "post_skip"
			"post_workroom":op="post_school"
			_:return false
		if not _command(model,{"op":op}):return false
	if not _final_school(model):return false
	var save := model.save_file(directory.path_join("november-four.json"))
	print("Returned to November week four, result ",receipt.facts.result_selector,", state ",model.export_save().state_sha256)
	return save.supported

func _final_school(model: Model) -> bool:
	if model.stage()!="returned_school" or model.export_save().version!=36:return false
	var bundle: Dictionary=model.read_postbattle().bundle
	var school: Dictionary=bundle.school
	if [school.month,school.week,school.student_count,school.teacher_count]!=[11,4,18,6]:return false
	var roster: Array=school.student_ids.slice(0,school.student_count)
	return roster.slice(-3)==[2,7,28] and school.teacher_ids.slice(0,6).has(107) and bundle.sortie_result.scene_id==41

func _command(model: Model, command: Dictionary) -> bool:
	var result:=model.execute(command)
	if not result.supported:printerr(command.op," ",result.reason)
	return result.supported

func _write(path: String, value: Dictionary) -> bool:
	var file:=FileAccess.open(path,FileAccess.WRITE)
	if file==null:return false
	file.store_string(JSON.stringify(value))
	return file.get_error()==OK
