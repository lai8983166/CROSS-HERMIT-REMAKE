extends SceneTree
## Headless UI acceptance. Pass play PARENT NEW_SAVE or reload NEW_SAVE after --.
const Screen := preload("res://ui/school_playground.gd")
const Week := preload("res://sim/school_sortie_week.gd")
const ROSTER := [[3,16,-1,4],[8,-1,17,-1],[6,5,2,-1],[9,1,-1,-1],[13,-1,-1,-1]]
const COURSES := [7,19,24,30,36]
const PARENT_SHA := "03ffb8511b3606e25f2b0c3d9a2985c1189830ec1680f9697d2beb10bc16d31e"

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	var playing := args.size()==3 and args[0]=="play"
	if not playing and not (args.size()==2 and args[0]=="reload"):
		printerr("Expected play PARENT NEW_SAVE or reload NEW_SAVE")
		quit(1)
		return
	if playing and (FileAccess.file_exists(args[2]) or FileAccess.get_sha256(args[1])!=PARENT_SHA):
		printerr("Invalid parent or output already exists")
		quit(1)
		return
	var ui := Screen.new()
	ui.auto_load=false
	ui.autosave=false
	root.add_child(ui)
	ui.save_path=args[1]
	ui.load_button.pressed.emit()
	var ok := ui.model.stage()=="returned_school"
	if ok and playing:
		ok = _play(ui,args[2])
	elif ok:
		ok = _continue_week_two(ui)
	if not ok:
		printerr("September verification failed at ",ui.model.stage()," ",ui.model.read_postbattle().get("phase",""))
	ui.free()
	quit(0 if ok else 1)

func _school_matches(ui, week: int) -> bool:
	var school: Dictionary=ui.model.read_postbattle().bundle.school
	if [school.month,school.week,school.teacher_count,school.student_count,school.adventure_gate]!=[9,week,5,11,0] or school.derived_student_ids!=ROSTER:
		return false
	for group in range(5):
		var courses: OptionButton=ui.postbattle_panel.find_child("courses_%d"%group,true,false)
		if courses==null or courses.disabled or courses.get_selected_id()!=COURSES[group]:
			return false
	return true

func _pages(ui, phase: String, pages: Array) -> bool:
	for page in pages:
		var view: Dictionary=ui.model.read_postbattle()
		if view.phase!=phase or view.page!=page or ui.postbattle_panel.dialogue.text!=page.text or ui.postbattle_panel.speaker.text!=page.speaker:
			return false
		ui.postbattle_panel.next.pressed.emit()
	return true

func _play(ui, path: String) -> bool:
	var model=ui.model
	var panel=ui.postbattle_panel
	if not _school_matches(ui,1) or model.export_save().version!=26:
		return false
	var before: Dictionary=model.read_postbattle().bundle
	var settle: Button=panel.find_child("settle",true,false)
	if settle==null or settle.disabled:
		return false
	settle.pressed.emit()
	if not panel.commit_dialog.visible:
		return false
	panel.commit_dialog.hide()
	panel.commit_dialog.confirmed.emit()
	if model.stage()!="course_result":
		return false
	var view: Dictionary=model.read_postbattle()
	var result: Dictionary=view.planning.course_summary
	var students: Array=result.students.map(func(row):return [row.character_id,row.work_id])
	var expected := []
	for group in range(5):
		for pupil in ROSTER[group]:
			if pupil>=0:expected.append([pupil,COURSES[group]])
	if students!=expected or result.history_index!=25 or view.bundle.school.global_total_511c!=1930708+result.bonus or model.execute({"op":"return_settle"}).supported:
		return false
	var story:=Week.story(1,9)
	if not story.supported or [story.pre_week.size(),story.week_start.size(),story.school_entry.size()]!=[88,51,0]:
		return false
	print("COURSES ",JSON.stringify({"bonus":result.bonus,"mvp":result.recipient,"total":view.bundle.school.global_total_511c,"students":students}))
	panel.find_child("continue_course_story",true,false).pressed.emit()
	if not _pages(ui,"post_story",story.pre_week):
		return false
	if model.read_postbattle().get("date_card",{}).get("image")!="res://assets/school_story/tc0902.png" or not panel.card_frame.visible or panel.card_image.texture==null:
		return false
	panel.next.pressed.emit()
	if not _pages(ui,"new_week_story",story.week_start) or model.stage()!="post_workroom":
		return false
	var workroom: Dictionary=model.read_postbattle().bundle
	if [workroom.flags["0x7a55f6"],workroom.flags["0x7e11a0"],workroom.adv_background]!=[1,1,13]:
		return false
	panel.next.pressed.emit()
	if model.stage()!="returned_school" or not _school_matches(ui,2):
		return false
	if model.read_postbattle().bundle.school.lecture_work_fields!=before.school.lecture_work_fields:
		return false
	ui.save_path=path
	panel.save_requested.emit()
	return FileAccess.file_exists(path) and model.export_save().version==27

func _continue_week_two(ui) -> bool:
	var model=ui.model
	var saved: Dictionary=model.export_save()
	if not _school_matches(ui,2) or saved.version!=27 or saved.state_sha256!=JSON.parse_string(FileAccess.get_file_as_string(ui.save_path)).state_sha256:
		return false
	var select: Button=ui.postbattle_panel.find_child("adventure_17",true,false)
	if select==null or select.disabled or select.button_pressed:
		return false
	select.pressed.emit()
	if model.read_postbattle().bundle.school.lecture_work_fields[2]!=17 or model.export_save().commands.size()!=saved.commands.size()+1:
		return false
	var altered:=saved.duplicate(true)
	altered.rules.september_two_story="changed"
	if model.restore(altered).get("reason")!="save_rules_changed":
		return false
	print("RELOADED ",saved.state_sha256," commands ",saved.commands.size()," continued with adventure 17")
	return true
