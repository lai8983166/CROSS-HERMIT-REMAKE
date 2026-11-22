extends "../devtools/verify_september_school.gd"
## --headless --path prototype -s ../devtools/verify_september_adventure22.gd --
## play PARENT NEW_SAVE SETTLEMENT_JSON  |  reload NEW_SAVE
const PARENT_22 := "d383a32961ed1224706b9f289ac8278c7b03b966e483b2592cb97d1d929f706f"
const TRACE := "res://sim/tests/mandatory_twenty_two_victory_trace.json"
const TEACHERS := [101,110,115,118,116]
const WIN_SELECTORS := {2:1,3:1,5:2,6:2,8:3}

func _run() -> void:
	var args:=OS.get_cmdline_user_args()
	var playing:=args.size()==4 and args[0]=="play"
	if not playing and not (args.size()==2 and args[0]=="reload"):
		printerr("Expected play PARENT NEW_SAVE SETTLEMENT_JSON or reload NEW_SAVE")
		quit(1)
		return
	if playing and (FileAccess.get_sha256(args[1])!=PARENT_22 or args[2]==args[3] or FileAccess.file_exists(args[2]) or FileAccess.file_exists(args[3])):
		printerr("Unexpected parent or an output already exists")
		quit(1)
		return
	var ui:=Screen.new()
	ui.auto_load=false
	ui.autosave=false
	root.add_child(ui)
	ui.save_path=args[1]
	ui.load_button.pressed.emit()
	var ok: bool=ui.model.stage()=="returned_school"
	if ok and playing:
		ok=_fight(ui,args[3]) and _return_and_save(ui,args[2])
	elif ok:
		ok=_continue_four(ui)
	if not ok:printerr("Adventure 22 acceptance stopped at ",ui.model.stage())
	ui.free()
	quit(0 if ok else 1)

func _school(ui, week: int, mission: int) -> bool:
	var s: Dictionary=ui.model.read_postbattle().bundle.school
	return [s.month,s.week,s.adventure_gate,s.teacher_count,s.student_count]==[9,week,1,5,11] and s.derived_student_ids==ROSTER and s.lecture_work_fields[2]==mission

func _fight(ui, output_path: String) -> bool:
	var model=ui.model
	var panel=ui.postbattle_panel
	if not _school(ui,3,22) or model.export_save().version!=28:return false
	var depart: Button=panel.find_child("depart",true,false)
	if depart==null or depart.disabled:return false
	depart.pressed.emit()
	if not panel.commit_dialog.visible:return false
	panel.commit_dialog.hide()
	panel.commit_dialog.confirmed.emit()
	if model.stage()!="sortie_pending" or model.export_save().version!=29:return false
	var prior: Dictionary=model.read_postbattle()
	var hand: Dictionary=prior.planning.handoff
	var party: Dictionary=hand.prepared.rounds[0]
	var ids: Array=[]
	var groups: Array=[]
	for g in ROSTER.size():
		for pupil in ROSTER[g]:
			if pupil>=0:
				ids.append(pupil)
				groups.append(g)
	if party!={"scene_id":22,"teacher_ids":TEACHERS,"student_ids":ids,"student_groups":groups} or not hand.idle_student_ids.is_empty():return false
	var capture: Dictionary={"before":prior.bundle,"ratings":hand.prepared.class_ratings,"round":party,"grades":model._postbattle._task_grades.duplicate()}
	panel.find_child("play_sortie",true,false).pressed.emit()
	var trial=ui.sortie_trial
	var session=trial.session
	if not session.ready or session.scene_id!=22:return false
	var trace: Dictionary=Week.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(TRACE)))
	var remaining:=trace.duplicate(true)
	var pages: Array=session._pages(1)
	if pages.size()!=5:return false
	for page in pages:
		if trial.text_label.text!="\n".join(page.map(func(line):return line.text)):return false
		if remaining.commands.pop_front()!=[0,1,1]:return false
		trial.continue_button.pressed.emit()
	var run: Dictionary=Screen.Playground.BattleRecord.run_trace(session,remaining)
	if not run.supported:
		printerr(run)
		return false
	var facts: Dictionary=session.result_inputs()
	if not WIN_SELECTORS.has(session.ending_sub) or facts.get("result_selector")!=WIN_SELECTORS[session.ending_sub] or session.battle_trace()!=trace:return false
	if not session._pages(session.ending_sub).is_empty():return false
	capture["facts"]=facts
	var endpoint: Dictionary={"ticks":trace.ticks,"commands":trace.commands.size(),"elapsed":session.elapsed,"sub":session.ending_sub,"selector":facts.result_selector,"tower_side":session.find_unit(1248).side,"objective_slots":facts.objective_slots,"survivors":session.controlled_units().filter(func(unit):return unit.limits.hp>0).size()}
	trial._refresh()
	trial.continue_button.pressed.emit()
	if model.stage()!="sortie_result":return false
	var view: Dictionary=model.read_postbattle()
	var result: Dictionary=view.planning.sortie_summary
	if [result.scene_id,result.date,result.history_index,result.result_selector]!=[22,[9,3],27,facts.result_selector] or result.students.map(func(row):return row.character_id)!=ids:return false
	if view.bundle.school.global_total_511c!=1930708+result.score.total_delta or model.execute({"op":"sortie_finish","trace":trace}).supported:return false
	for row in view.bundle.records:
		if row.week_records[81]!=2:return false
	capture["after"]=view.bundle
	var out:=FileAccess.open(output_path,FileAccess.WRITE)
	if out==null:return false
	out.store_string(JSON.stringify(capture))
	out.close()
	print("BATTLE22 ",JSON.stringify(endpoint))
	print("RESULT22 ",JSON.stringify({"score":result.score.total_delta,"total":view.bundle.school.global_total_511c,"mvp":result.recipient,"grade":result.task_grade,"items":result.loot_groups}))
	panel.find_child("continue_sortie_story",true,false).pressed.emit()
	return true

func _return_and_save(ui, path: String) -> bool:
	var story:=Week.story(3,9)
	if not story.supported or [story.pre_week.size(),story.week_start.size(),story.school_entry.size()]!=[107,14,0]:return false
	if not _pages(ui,"post_story",story.pre_week):return false
	var model=ui.model
	var panel=ui.postbattle_panel
	if model.read_postbattle().get("date_card",{}).get("image")!="res://assets/school_story/tc0904.png" or not panel.card_frame.visible or panel.card_image.texture==null:return false
	panel.next.pressed.emit()
	if not _pages(ui,"new_week_story",story.week_start) or model.stage()!="post_workroom":return false
	var room: Dictionary=model.read_postbattle().bundle
	if [room.flags["0x7a55f6"],room.flags["0x7e11a0"],room.adv_background]!=[9,1,10]:return false
	panel.next.pressed.emit()
	if model.stage()!="returned_school" or not _school(ui,4,24):return false
	var view: Dictionary=model.read_postbattle()
	if view.bundle.school.lecture_work_fields!=[3,22,24,0] or not panel.find_child("adventure_24",true,false).button_pressed:return false
	if Week.Adventures.available(view.planning.ledger).map(func(row):return row.id)!=[24,35,17]:return false
	if model.execute({"op":"return_select","adventure":17}).supported:return false
	ui.save_path=path
	panel.save_requested.emit()
	return FileAccess.file_exists(path) and model.export_save().version==29

func _continue_four(ui) -> bool:
	var model=ui.model
	var panel=ui.postbattle_panel
	var saved: Dictionary=model.export_save()
	if not _school(ui,4,24) or saved.version!=29 or saved.state_sha256!=JSON.parse_string(FileAccess.get_file_as_string(ui.save_path)).state_sha256:return false
	panel.find_child("member_13",true,false).pressed.emit()
	panel.assignments.get_child(4).get_child(3).pressed.emit()
	if model.read_postbattle().bundle.school.derived_student_ids[4]!=[-1,13,-1,-1] or model.export_save().commands.size()!=saved.commands.size()+1:return false
	var altered:=saved.duplicate(true)
	altered.rules.mandatory_twenty_two="changed"
	if model.restore(altered).get("reason")!="save_rules_changed":return false
	print("RELOADED ",saved.state_sha256," commands ",saved.commands.size()," continued with ",model.export_save().commands.back())
	return true
