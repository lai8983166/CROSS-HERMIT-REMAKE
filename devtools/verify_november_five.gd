extends SceneTree
const Model := preload("res://sim/school_playground.gd")
const START_SHA := "e691ab2ec7f1faedc8580447b0ef87135d5c230400f6ef28b441ebdf2c43b0c2"

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() not in [1,2]:
		quit(1)
		return
	if args.size()==2 and (FileAccess.get_sha256(args[0])!=START_SHA or FileAccess.file_exists(args[1]) or FileAccess.file_exists(args[1]+".settlement.json") or FileAccess.file_exists(args[1]+".opening.json")):
		quit(1)
		return
	var model := Model.new()
	var loaded := model.load_file(args[0])
	if not loaded.supported:
		printerr("Rejected school save ",loaded.get("reason"))
		quit(1)
		return
	var ok := false
	if args.size()==2:
		ok=_play(model,args[1])
	else:
		ok=_final(model)
		var tampered := model.export_save()
		tampered.rules.november_five_story="changed"
		ok=ok and not Model.new().restore(tampered).supported
	print("November five verification ",ok," at ",model.stage()," ",model.export_save().state_sha256)
	quit(0 if ok else 1)

func _command(model: Model, cmd: Dictionary) -> bool:
	var result := model.execute(cmd)
	if not result.supported:printerr(cmd," ",result.reason)
	return result.supported

func _play(model: Model, path: String) -> bool:
	if model.export_save().version!=36 or model.stage()!="returned_school":return false
	var snapshot := FileAccess.open(path+".opening.json",FileAccess.WRITE)
	if snapshot==null:return false
	snapshot.store_string(JSON.stringify(model.read_postbattle()))
	snapshot.close()
	for move in [{"kind":"teacher","member_id":107,"target_group":0,"target_slot":-1},{"kind":"student","member_id":28,"target_group":0,"target_slot":0},{"kind":"student","member_id":4,"target_group":0,"target_slot":1}]:
		move.op="return_move"
		if not _command(model,move):return false
	var school: Dictionary=model.read_postbattle().bundle.school
	for group in range(5):
		if school.derived_teacher_ids[group]<0:continue
		if not _command(model,{"op":"return_mode","group":group,"teaching":true}):return false
		var list := Model.Postbattle.Courses.list_courses(model.read_postbattle().bundle,group)
		if not list.supported:return false
		var course := -1
		for category in list.courses:
			if not category.is_empty():
				course=category[0][1]
				break
		if course<1:return false
		if not _command(model,{"op":"return_course","group":group,"course":course}):return false
	if model.export_save().version!=37:return false
	var before: Dictionary=model.read_postbattle().bundle
	if not _command(model,{"op":"return_settle"}):return false
	var after: Dictionary=model.read_postbattle().bundle
	var file := FileAccess.open(path+".settlement.json",FileAccess.WRITE)
	if file==null:return false
	file.store_string(JSON.stringify({"before":before,"after":after}))
	file.close()
	if model.execute({"op":"return_settle"}).supported or not _command(model,{"op":"course_story"}):return false
	var view := model.read_postbattle()
	if model.stage()!="new_week_story" or not view.has("date_card") or view.bundle.school.student_count!=17 or view.bundle.chapter076_absent.participants.character_id!=4:return false
	for op in ["post_next","post_next","post_prev","post_skip"]:
		if not _command(model,{"op":op}):return false
	view=model.read_postbattle()
	if model.stage()!="post_workroom" or [view.bundle.flags["0x7a55f6"],view.bundle.flags["0x7e11a0"],view.bundle.adv_background]!=[11,0,10]:return false
	if not _command(model,{"op":"post_school"}) or not _final(model):return false
	return model.save_file(path).supported

func _final(model: Model) -> bool:
	var view := model.read_postbattle()
	var school: Dictionary=view.bundle.school
	if model.stage()!="returned_school" or model.export_save().version!=37 or [school.month,school.week,school.student_count,school.teacher_count]!=[11,5,17,6]:return false
	var absent: Dictionary=view.bundle.chapter076_absent
	for key in ["participants","growth","records","counts"]:
		if absent[key].character_id!=4 or view.bundle[key].any(func(row):return row.character_id==4):return false
	for members in school.derived_student_ids:
		if 4 in members:return false
	return absent.profile.member_id==4 and school.availability[4]==0 and [view.bundle.flags["0x7a55f6"],view.bundle.flags["0x7e11a0"]]==[11,1] and Model.Postbattle.Return.validate_planning_roster(view.bundle,Model.Postbattle.Return._rules()).is_empty()
