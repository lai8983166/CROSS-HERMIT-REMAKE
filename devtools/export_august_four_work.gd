extends SceneTree
## --headless --path prototype -s ../devtools/export_august_four_work.gd -- PARENT SAVE_OUTPUT course|mixed
const Model := preload("res://sim/school_playground.gd")
const TRAINING_TRACE := "res://sim/tests/august_week4_training_trace.json"


func _init() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size()!=3 or args[2] not in ["course","mixed"] or FileAccess.file_exists(args[1]):
		printerr("Expected accepted August 4 parent save, new JSON output, and course or mixed.")
		quit(1)
		return
	var model := Model.new()
	var loaded := model.load_file(args[0])
	if not loaded.supported:
		printerr(loaded)
		quit(1)
		return
	var opening := model.read_postbattle()
	if model.stage()!="returned_school" or [opening.bundle.school.month,opening.bundle.school.week]!=[8,4]:
		printerr("Expected the August week 4 planning save.")
		quit(1)
		return
	var commands: Array = []
	if args[2]=="course":
		for group in range(4):
			commands.append({"op":"return_mode","group":group,"teaching":true})
			commands.append({"op":"return_course","group":group,"course":[8,19,26,30][group]})
	else:
		commands=[{"op":"return_select","adventure":17},{"op":"return_depart"}]
	for command in commands:
		var planned := model.execute(command)
		if not planned.supported:
			printerr(command," ",planned)
			quit(1)
			return
	var prior := model.read_postbattle()
	var output := {"before":prior.bundle}
	var commit := {"op":"return_settle"}
	if args[2]=="mixed":
		output["round"]=prior.planning.handoff.prepared.rounds[0]
		output["ratings"]=prior.planning.handoff.prepared.class_ratings
		var trace: Dictionary=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(TRAINING_TRACE)))
		var played:=Model.Postbattle.SortieRecord.replay(prior.planning.handoff,trace)
		if not played.supported:
			printerr(played)
			quit(1)
			return
		output["facts"]=played.facts
		output["grades"]=model._postbattle._task_grades.duplicate()
		commit={"op":"sortie_finish","trace":trace}
	var result := model.execute(commit)
	if not result.supported:
		printerr(result)
		quit(1)
		return
	output["after"]=model.read_postbattle().bundle
	var out := FileAccess.open(args[1],FileAccess.WRITE)
	if out==null:
		printerr("Failed to create ",args[1])
		quit(1)
		return
	out.store_string(JSON.stringify(output))
	out.close()
	quit()
