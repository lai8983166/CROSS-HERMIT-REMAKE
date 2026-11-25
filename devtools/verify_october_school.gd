extends SceneTree
const Model := preload("res://sim/school_playground.gd")
const PARENT := "1437a80bf7b27c16dec9304d52b2d54e686d4aa83f54d91ad5a3736612e24fad"

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size()!=2 or FileAccess.get_sha256(args[0])!=PARENT or FileAccess.file_exists(args[1]):
		quit(1)
		return
	var model := Model.new()
	var result := model.load_file(args[0])
	print("Verified parent ", model.stage())
	var joins := []
	var commands := []
	for group in range(5):
		commands.append({"op":"return_mode","group":group,"teaching":true})
		commands.append({"op":"return_course","group":group,"course":[7,19,25,30,36][group]})
	for op in ["return_settle","course_story","post_skip","post_next","post_skip","post_school"]:
		commands.append({"op":op})
	for command in commands:
		if not result.supported:break
		var before := model.read_postbattle().bundle as Dictionary
		result=model.execute(command)
		if result.supported:
			var after := model.read_postbattle().bundle as Dictionary
			var first: int=before.school.student_count
			if after.school.student_count>first:
				joins.append({"chapter":313 if first==14 else 233,"date":[before.school.month,before.school.week],"difficulty":before.school.difficulty,"initial_ids":before.school.student_ids.slice(0,first),"teacher_ids":before.school.teacher_ids.slice(0,before.school.teacher_count),"initial_items":before.item_flags,"items":after.item_flags,"new_students":after.participants.slice(first),"records":after.records.slice(first)})
		if not result.supported:printerr(command, " ",result)
	if result.supported:
		var bundle: Dictionary=model.read_postbattle().bundle
		var school: Dictionary=bundle.school
		var correct: bool = [model.stage(),school.month,school.week,school.student_count,school.student_ids.slice(14,16),bundle.flags["0x7a55f6"],bundle.flags["0x7e11a0"]]==["returned_school",10,1,16,[18,32],11,1]
		if correct and model.save_file(args[1]).supported:
			var capture := FileAccess.open(args[1]+".joins.json",FileAccess.WRITE)
			capture.store_string(JSON.stringify({"joins":joins}))
			capture.close()
			print("Saved October week one ",model.export_save().state_sha256)
			var replay := Model.new()
			result=replay.load_file(args[1])
			if result.supported and replay.export_save()==model.export_save() and _continue_october(replay):
				print("October cross-month replay verified ", model.export_save().state_sha256)
				quit(0)
				return
	printerr("October verification stopped at ",model.stage()," ",result.get("reason","unexpected state"))
	quit(1)

func _continue_october(model: Model) -> bool:
	for op in ["return_settle","course_story","post_skip","post_next","post_skip","post_school"]:
		var result := model.execute({"op":op})
		if not result.supported:
			printerr("October continuation ",op," ",result)
			return false
	var bundle: Dictionary = model.read_postbattle().bundle
	var school: Dictionary = bundle.school
	return [school.month,school.week,school.student_count,bundle.flags["0x7a55f6"],bundle.flags["0x7e11a0"],bundle.adv_background] == [10,2,16,3,1,14] and model.export_save().version==32
