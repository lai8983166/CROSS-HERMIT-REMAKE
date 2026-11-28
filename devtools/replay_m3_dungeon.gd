extends SceneTree
const Sortie := preload("res://sim/school_sortie_session.gd")
const Record := preload("res://sim/school_sortie_record.gd")
const Model := preload("res://sim/school_playground.gd")

func _initialize() -> void:
	var args:=OS.get_cmdline_user_args()
	if args.size() not in [1,2]:quit(2);return
	if FileAccess.get_sha256(args[0])!="ec60f7b3f2b8ccd7894c25647d569b5bb759168f9d90aa5985d2c5fccc8c3b7d":quit(2);return
	var model:=Model.new()
	model.replay_progress=func(i,total):
		if i%100==0:print("Restored school commands ",i,"/",total)
		return true
	var restored:=model.load_week_state(args[0])
	if not restored.supported or model.export_save().state_sha256!="9edcc29f95200b70fc8da0c1f558c59bc39f376fdcbddc888a152d51639704b7":
		printerr("July-four source rejected ",restored);quit(1);return
	var view:=model.read_postbattle()
	var departure: Dictionary=Sortie.Adventures.submit(view.bundle,view.planning.ledger).handoff
	var trace_path:=args[1] if args.size()==2 else "res://sim/tests/mandatory_fourteen_dungeon_trace.json"
	if args.size()==1 and FileAccess.get_sha256(trace_path)!="a869ae313aa0b819df85c5a6ba0634d7cab4f3c440ea80f9da79a87b99f42717":quit(2);return
	var trace=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(trace_path)))
	if not trace is Dictionary or trace.get("version")!=2 or not trace.get("floors") is Array or trace.floors.size()!=3:quit(1);return
	var proof:=Record.replay(departure,trace)
	if not proof.supported or proof.facts.get("dungeon_depth")!=3:printerr(proof);quit(1);return
	if not _settle(model,trace):quit(1);return
	print("Authenticated three-floor replay ",FileAccess.get_sha256(trace_path)," grade ",proof.facts.result_selector)
	quit(0);return

func _settle(model: Model,trace: Dictionary) -> bool:
	if not model.execute({"op":"return_depart"}).supported:return false
	var result:=model.execute({"op":"sortie_finish","trace":trace})
	if not result.supported:
		printerr("School settlement rejected ",result)
		return false
	var school:=model.read_postbattle()
	if school.phase!="sortie_result" or school.planning.sortie_summary.scene_id!=14:return false
	print("Dungeon school settlement ",school.phase," task grade ",school.planning.sortie_summary.task_grade)
	return true
