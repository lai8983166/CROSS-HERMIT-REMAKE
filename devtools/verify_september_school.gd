extends SceneTree
## Headless UI acceptance. Pass play PARENT NEW_SAVE or reload NEW_SAVE after --.
const Screen := preload("res://ui/school_playground.gd")
const Week := preload("res://sim/school_sortie_week.gd")
const ROSTER := [[3,16,-1,4],[8,-1,17,-1],[6,5,2,-1],[9,1,-1,-1],[13,-1,-1,-1]]
const COURSES := [7,19,24,30,36]
const WEEK_TWO_PARENT_SHA := "5a744a08217ef0a0fe19c56fb14be3f5568d000533751894325bdf5d54fd0957"
const WEEK_TWO_COURSES := [7,19,25,30,36]
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
	if playing and (FileAccess.file_exists(args[2]) or FileAccess.get_sha256(args[1]) not in [PARENT_SHA,WEEK_TWO_PARENT_SHA]):
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
		ok = _play(ui,args[2],2 if FileAccess.get_sha256(args[1])==WEEK_TWO_PARENT_SHA else 1)
	elif ok:
		ok = _continue_school(ui)
	if not ok:
		printerr("September verification failed at ",ui.model.stage()," ",ui.model.read_postbattle().get("phase",""))
	ui.free()
	quit(0 if ok else 1)

func _school_matches(ui, week: int) -> bool:
	var school: Dictionary=ui.model.read_postbattle().bundle.school
	var mandatory := week==3
	var expected_courses := WEEK_TWO_COURSES if mandatory else COURSES
	if [school.month,school.week,school.teacher_count,school.student_count,school.adventure_gate]!=[9,week,5,11,int(mandatory)] or school.derived_student_ids!=ROSTER:
		return false
	for group in range(5):
		var courses: OptionButton=ui.postbattle_panel.find_child("courses_%d"%group,true,false)
		if courses==null or courses.disabled!=mandatory or courses.get_selected_id()!=expected_courses[group]:
			return false
	return true

func _pages(ui, phase: String, pages: Array) -> bool:
	for page in pages:
		var view: Dictionary=ui.model.read_postbattle()
		if view.phase!=phase or view.page!=page or ui.postbattle_panel.dialogue.text!=page.text or ui.postbattle_panel.speaker.text!=page.speaker:
			return false
		ui.postbattle_panel.next.pressed.emit()
	return true

func _play(ui, path: String, week: int) -> bool:
	var model=ui.model
	var panel=ui.postbattle_panel
	if not _school_matches(ui,week) or model.export_save().version!=25+week:
		return false
	if week==2:
		var third: OptionButton=panel.find_child("courses_2",true,false)
		var index:=third.get_item_index(25)
		if index<1:return false
		third.item_selected.emit(index)
		if model.export_save().commands.back()!={"op":"return_course","group":2,"course":25}:return false
	var before: Dictionary=model.read_postbattle().bundle
	var plan := WEEK_TWO_COURSES if week==2 else COURSES
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
			if pupil>=0:expected.append([pupil,plan[group]])
	if students!=expected or result.history_index!=24+week or view.bundle.school.global_total_511c!=1930708+result.bonus or model.execute({"op":"return_settle"}).supported:
		return false
	var story:=Week.story(week,9)
	var page_counts := [0,22,0] if week==2 else [88,51,0]
	if not story.supported or [story.pre_week.size(),story.week_start.size(),story.school_entry.size()]!=page_counts:
		return false
	print("COURSES ",JSON.stringify({"bonus":result.bonus,"mvp":result.recipient,"total":view.bundle.school.global_total_511c,"students":students}))
	panel.find_child("continue_course_story",true,false).pressed.emit()
	if not _pages(ui,"post_story",story.pre_week):
		return false
	if model.read_postbattle().get("date_card",{}).get("image")!="res://assets/school_story/tc090%d.png"%(week+1) or not panel.card_frame.visible or panel.card_image.texture==null:
		return false
	panel.next.pressed.emit()
	if not _pages(ui,"new_week_story",story.week_start) or model.stage()!="post_workroom":
		return false
	var workroom: Dictionary=model.read_postbattle().bundle
	var expected_room := [12,1,10] if week==2 else [1,1,13]
	if [workroom.flags["0x7a55f6"],workroom.flags["0x7e11a0"],workroom.adv_background]!=expected_room:
		return false
	panel.next.pressed.emit()
	if model.stage()!="returned_school" or not _school_matches(ui,week+1):
		return false
	var expected_selection: Array=[3,21,22,0] if week==2 else before.school.lecture_work_fields
	if model.read_postbattle().bundle.school.lecture_work_fields!=expected_selection:
		return false
	if week==2 and (not panel.find_child("adventure_22",true,false).button_pressed or model.execute({"op":"return_select","adventure":17}).supported):
		return false
	ui.save_path=path
	panel.save_requested.emit()
	return FileAccess.file_exists(path) and model.export_save().version==26+week

func _continue_school(ui) -> bool:
	var model=ui.model
	var saved: Dictionary=model.export_save()
	var week: int=model.read_postbattle().bundle.school.week
	if week not in [2,3] or not _school_matches(ui,week) or saved.version!=25+week or saved.state_sha256!=JSON.parse_string(FileAccess.get_file_as_string(ui.save_path)).state_sha256:
		return false
	var panel=ui.postbattle_panel
	if week==3:
		if model.read_postbattle().bundle.school.lecture_work_fields!=[3,21,22,0]:return false
		panel.find_child("member_13",true,false).pressed.emit()
		panel.assignments.get_child(4).get_child(3).pressed.emit()
		if model.read_postbattle().bundle.school.derived_student_ids[4]!=[-1,13,-1,-1]:return false
	else:
		var select: Button=panel.find_child("adventure_17",true,false)
		if select==null or select.disabled or select.button_pressed:return false
		select.pressed.emit()
		if model.read_postbattle().bundle.school.lecture_work_fields[2]!=17:return false
	if model.export_save().commands.size()!=saved.commands.size()+1:
		return false
	var altered:=saved.duplicate(true)
	altered.rules["september_three_story" if week==3 else "september_two_story"]="changed"
	if model.restore(altered).get("reason")!="save_rules_changed":
		return false
	print("RELOADED ",saved.state_sha256," commands ",saved.commands.size()," continued with ",model.export_save().commands.back())
	return true
