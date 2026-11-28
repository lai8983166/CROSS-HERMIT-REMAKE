extends SceneTree
const Campaign := preload("res://sim/school_native_campaign.gd")

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() not in [1,2]:quit(2);return
	var path: String=args[0]
	var school=load("res://school_playground.tscn").instantiate()
	root.add_child(school)
	school._open_native_sortie(path)
	var campaign: Campaign=school.imported_campaign
	if campaign==null or not school.native_return_dialog.visible or campaign.save_path!=path:
		printerr("Could not load returned school from disk");quit(1);return
	var week: int=campaign.state.school.week
	var baseline := campaign.state.duplicate(true)
	var original: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
	var bad := path+".test.tmp"
	if FileAccess.file_exists(bad):quit(2);return
	for field in ["source","trace","state"]:
		var data := original.duplicate(true)
		match field:
			"source":data.source_sha256="wrong"
			"trace":data.rounds[0].trace.commands[0]=[0,99]
			"state":data.rounds[0].state_sha256="wrong"
		var output:=FileAccess.open(bad,FileAccess.WRITE)
		if output==null:quit(1);return
		output.store_string(JSON.stringify(data))
		output.close()
		var rejected := not campaign.load_progress(bad)
		DirAccess.remove_absolute(bad)
		if not rejected or campaign.state!=baseline:
			printerr("Corruption admitted or state changed: ",field);quit(1);return
	if args.size()==2:
		if campaign.state.school.month!=13 or week!=3 or FileAccess.file_exists(args[1]):quit(2);return
		var output:=FileAccess.open(args[1],FileAccess.WRITE)
		if output==null:quit(1);return
		output.store_string(JSON.stringify(campaign.state))
		output.flush()
		if output.get_error()!=OK:quit(1);return
		output.close()
	if not campaign.departure().is_empty():
		school.native_return_dialog.hide()
		school._play_imported_sortie()
		if not school.sortie_trial.visible or school.sortie_trial.session.scene_id!=week:quit(1);return
	print("UI recovered week ",week,", score ",campaign.state.score,", completed ",campaign.rounds.size(),"; rejected changed source, command and state")
	quit(0)
