extends SceneTree
const Model := preload("res://sim/school_playground.gd")

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size()==1:
		quit(0 if _verify_final(args[0]) else 1)
		return
	if args.size()!=2 or FileAccess.file_exists(args[1]) or FileAccess.get_sha256(args[0])!="bd8442a88105ef9e3ea8f2a881a2683b41c98850720918ca101c329b276e4d9c":
		quit(1)
		return
	var model := Model.new()
	var loaded := model.load_file(args[0])
	if not loaded.supported:
		printerr(loaded.get("reason"))
		quit(1)
		return
	for op in ["return_settle","course_story","post_next","post_skip","post_school"]:
		var result := model.execute({"op":op})
		if not result.supported:
			printerr(op," ",result.get("reason"))
			quit(1)
			return
		if op=="course_story":
			var bundle: Dictionary=model.read_postbattle().bundle
			if model.stage()!="new_week_story" or bundle.school.student_count!=15 or bundle.chapter071_absent.participants.character_id!=2:
				quit(1)
				return
	var school: Dictionary=model.read_postbattle().bundle.school
	if [model.stage(),school.month,school.week,school.lecture_work_fields[2],school.adventure_gate]!=["returned_school",11,3,41,1] or model.execute({"op":"return_settle"}).supported:
		quit(1)
		return
	var saved := model.save_file(args[1])
	print("November week three ",school.student_count," students, mandatory ",school.lecture_work_fields," version ",model.export_save().version)
	quit(0 if saved.supported and model.export_save().version==35 else 1)


func _verify_final(path: String) -> bool:
	var model := Model.new()
	var restored := model.load_file(path)
	if not restored.supported:
		printerr("November replay failed: ",restored.reason)
		return false
	var view := model.read_postbattle()
	var bundle: Dictionary=view.bundle
	var school: Dictionary=bundle.school
	var saved := model.export_save()
	if model.stage()!="returned_school" or saved.version!=35 or [school.month,school.week,school.student_count]!=[11,3,15]:
		return false
	var absent: Dictionary=bundle.chapter071_absent
	for key in ["participants","growth","records","counts"]:
		if absent[key].character_id!=2 or bundle[key].any(func(row):return row.character_id==2):return false
	if absent.profile.member_id!=2 or school.availability[2]!=0 or school.raw_student_ids[15]!=32:return false
	var prepared := Model.Postbattle.Adventures.prepare(bundle,view.planning.ledger)
	if not prepared.supported:return false
	var round_data: Dictionary=prepared.prepared.rounds[0]
	if round_data.scene_id!=41 or 2 in round_data.student_ids or round_data.student_ids.is_empty():return false
	if model.execute({"op":"return_settle"}).supported or model.export_save()!=saved:return false
	print("Verified v35 replay ",saved.state_sha256,", scene 41 squad ",round_data.student_ids)
	return true
