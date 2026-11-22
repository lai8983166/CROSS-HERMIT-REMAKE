extends SceneTree
## --headless --path prototype -s ../devtools/export_august_four_work.gd -- PARENT RESULT_OUTPUT course|mixed|adventure35|september
const Model := preload("res://sim/school_playground.gd")
const TRAINING_TRACE := "res://sim/tests/august_week4_training_trace.json"


func _init() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size()!=3 or args[2] not in ["course","mixed","adventure35","september"] or FileAccess.file_exists(args[1]):
		printerr("Expected a parent save, a new JSON output and course, mixed, adventure35 or september.")
		quit(1)
		return
	var model := Model.new()
	var loaded := model.load_file(args[0])
	if not loaded.supported:
		printerr(loaded)
		quit(1)
		return
	var opening := model.read_postbattle()
	var week := 5 if args[2]=="adventure35" else 4
	var date := [9,1] if args[2]=="september" else [8,week]
	if model.stage()!="returned_school" or [opening.bundle.school.month,opening.bundle.school.week]!=date:
		printerr("Expected planning save for ",date,".")
		quit(1)
		return
	var commands: Array = []
	var lessons_only := args[2] in ["course","september"]
	if args[2]=="course":
		var courses := [8,19,26,30]
		for group in range(courses.size()):
			commands.append({"op":"return_mode","group":group,"teaching":true})
			commands.append({"op":"return_course","group":group,"course":courses[group]})
	elif args[2]=="adventure35":
		for group in [0,2,3]:
			commands.append({"op":"return_mode","group":group,"teaching":false})
		commands.append({"op":"return_depart"})
	elif args[2]=="mixed":
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
	if not lessons_only:
		output["round"]=prior.planning.handoff.prepared.rounds[0]
		output["ratings"]=prior.planning.handoff.prepared.class_ratings
		var trace_path := "res://sim/tests/august_week5_adventure35_trace.json" if week==5 else TRAINING_TRACE
		var trace: Dictionary=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(trace_path)))
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
