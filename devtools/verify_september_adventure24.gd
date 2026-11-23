extends "../devtools/verify_september_adventure22.gd"
## play PARENT NEW_SAVE SETTLEMENT_JSON or reload NEW_SAVE, with absolute paths.
const PARENT_24 := "014de7db8675ee7c97d610f3ba4200847c79ec68bda51d2135a454d1f18185db"
const TRACE_24 := "res://sim/tests/mandatory_twenty_four_victory_trace.json"
const OLD_IDS := [3,4,9,5,8,6,1,2,16,17,13]

var joins:Array=[]
var settlement:Dictionary={}

func _capture_join(chapter:int,before:Dictionary,after:Dictionary) -> void:
	var first:int=before.school.student_count
	joins.append({"chapter":chapter,"date":[before.school.month,before.school.week],"difficulty":before.school.difficulty,
		"initial_ids":before.school.student_ids.slice(0,first),"teacher_ids":TEACHERS,"initial_items":before.item_flags,
		"items":after.item_flags,"new_students":after.participants.slice(first),"records":after.records.slice(first)})

func _run() -> void:
	var args:=OS.get_cmdline_user_args()
	var play:=args.size()==4 and args[0]=="play"
	if not play and not (args.size()==2 and args[0]=="reload"):
		printerr("Expected play PARENT NEW_SAVE SETTLEMENT_JSON or reload NEW_SAVE")
		quit(1)
		return
	if play and (FileAccess.get_sha256(args[1])!=PARENT_24 or args[2]==args[3] or FileAccess.file_exists(args[2]) or FileAccess.file_exists(args[3])):
		printerr("Unexpected parent or output already exists")
		quit(1)
		return
	var ui:=Screen.new()
	ui.auto_load=false
	ui.autosave=false
	root.add_child(ui)
	ui.save_path=args[1]
	ui.load_button.pressed.emit()
	var ok:bool=ui.model.stage()=="returned_school"
	if ok and play:
		ok=_play_battle(ui) and _story_and_save(ui,args[2])
		if ok:
			var file:=FileAccess.open(args[3],FileAccess.WRITE)
			if file==null:ok=false
			else:
				settlement["joins"]=joins
				file.store_string(JSON.stringify(settlement))
				file.close()
	elif ok:ok=_resume_five(ui)
	if not ok:printerr("Verification stopped at ",ui.model.stage()," ",ui._message)
	ui.free()
	quit(0 if ok else 1)

func _play_battle(ui) -> bool:
	var model=ui.model
	var panel=ui.postbattle_panel
	if not _school(ui,4,24) or model.export_save().version!=29:return false
	var depart:Button=panel.find_child("depart",true,false)
	if depart==null or depart.disabled:return false
	depart.pressed.emit()
	if not panel.commit_dialog.visible:return false
	panel.commit_dialog.hide()
	panel.commit_dialog.confirmed.emit()
	if model.stage()!="sortie_pending" or model.export_save().version!=30:return false
	var prior:Dictionary=model.read_postbattle()
	var hand:Dictionary=prior.planning.handoff
	var party:Dictionary=hand.prepared.rounds[0]
	var ids:=[3,16,4,8,17,6,5,2,9,1,13]
	if party!={"scene_id":24,"teacher_ids":TEACHERS,"student_ids":ids,"student_groups":[0,0,0,1,1,2,2,2,3,3,4]} or not hand.idle_student_ids.is_empty():return false
	var capture:Dictionary={"before":prior.bundle,"ratings":hand.prepared.class_ratings,"round":party,"grades":model._postbattle._task_grades.duplicate()}
	panel.find_child("play_sortie",true,false).pressed.emit()
	var trial=ui.sortie_trial
	var session=trial.session
	if not session.ready or session.scene_id!=24:return false
	var trace:Dictionary=Week.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(TRACE_24)))
	var remaining:=trace.duplicate(true)
	if session._pages(1).size()!=3:return false
	for page in session._pages(1):
		if trial.text_label.text!="\n".join(page.map(func(line):return line.text)) or remaining.commands.pop_front()!=[0,1,1]:return false
		trial.continue_button.pressed.emit()
	var event_at:int=remaining.commands.find_custom(func(row):return row[1]==2)
	if event_at<0:return false
	var rescue_start:Dictionary=remaining.duplicate(true)
	rescue_start.ticks=remaining.commands[event_at][0]
	rescue_start.commands=remaining.commands.slice(0,event_at)
	if not Screen.Playground.BattleRecord.run_trace(session,rescue_start).supported:return false
	if session._ending_phase!="event20" or session._event_pages.size()!=37:return false
	remaining.commands=remaining.commands.slice(event_at)
	trial._refresh()
	for page in session._event_pages.duplicate(true):
		if trial.text_label.text!="\n".join(page.map(func(line):return line.text)) or remaining.commands.pop_front()!=[rescue_start.ticks,2]:return false
		trial.continue_button.pressed.emit()
	var run:Dictionary=Screen.Playground.BattleRecord.run_trace(session,remaining)
	if not run.supported:
		printerr(run)
		return false
	var facts:Dictionary=session.result_inputs()
	var wins:={2:1,5:2,8:3}
	if not wins.has(session.ending_sub) or facts.get("result_selector")!=wins[session.ending_sub] or session.battle_trace()!=trace:return false
	capture["facts"]=facts
	print("BATTLE24 ",JSON.stringify({"ticks":trace.ticks,"commands":trace.commands.size(),"elapsed":session.elapsed,"sub":session.ending_sub,"selector":facts.result_selector,"slots":facts.objective_slots,"survivors":session.controlled_units().filter(func(u):return u.limits.hp>0).size()}))
	trial._refresh()
	var ending:Array=session._pages(session.ending_sub)
	if ending.size()!=28:return false
	for i in ending.size():
		if not trial.text_label.text.begins_with("\n".join(ending[i].map(func(line):return line.text))):return false
		if i+1<ending.size():trial.next_page.pressed.emit()
	trial.continue_button.pressed.emit()
	if model.stage()!="sortie_result":return false
	var view:Dictionary=model.read_postbattle()
	var result:Dictionary=view.planning.sortie_summary
	if [result.scene_id,result.date,result.history_index,result.result_selector]!=[24,[9,4],28,facts.result_selector] or result.students.map(func(row):return row.character_id)!=ids:return false
	if view.bundle.school.global_total_511c!=2108493+result.score.total_delta or model.execute({"op":"sortie_finish","trace":trace}).supported:return false
	for row in view.bundle.records:
		if row.week_records[84]!=2:return false
	capture["after"]=view.bundle
	settlement=capture
	print("RESULT24 ",JSON.stringify({"score":result.score.total_delta,"total":view.bundle.school.global_total_511c,"mvp":result.recipient,"grade":result.task_grade,"items":result.loot_groups}))
	panel.find_child("continue_sortie_story",true,false).pressed.emit()
	_capture_join(54,view.bundle,model.read_postbattle().bundle)
	return true

func _roster(ui, ids: Array) -> bool:
	var b:Dictionary=ui.model.read_postbattle().bundle
	return b.school.teacher_ids.slice(0,5)==TEACHERS and b.school.student_count==ids.size() and b.school.student_ids.slice(0,ids.size())==ids and b.participants.map(func(row):return row.character_id)==ids and b.school.relationships.size()==(5+ids.size())*(4+ids.size())

func _story_and_save(ui, path: String) -> bool:
	var week:=Week.story(4,9)
	var panel=ui.postbattle_panel
	if not _roster(ui,OLD_IDS+[14,15]) or not _pages(ui,"post_story",week.pre_week):return false
	var view:Dictionary=ui.model.read_postbattle()
	if view.get("date_card",{}).get("image")!="res://assets/school_story/tc0905.png" or not panel.card_frame.visible or panel.card_image.texture==null:return false
	panel.next.pressed.emit()
	if not _pages(ui,"new_week_story",week.week_start) or ui.model.stage()!="post_workroom":return false
	var room:Dictionary=ui.model.read_postbattle().bundle
	if [room.flags["0x7a55f6"],room.flags["0x7e11a0"],room.adv_background]!=[9,1,14] or not _roster(ui,OLD_IDS+[14,15]):return false
	panel.next.pressed.emit()
	_capture_join(56,room,ui.model.read_postbattle().bundle)
	if not _roster(ui,OLD_IDS+[14,15,11]) or not _pages(ui,"school_entry_story",week.school_entry):return false
	if not _school_five(ui):return false
	ui.save_path=path
	panel.save_requested.emit()
	return FileAccess.file_exists(path) and ui.model.export_save().version==30

func _school_five(ui) -> bool:
	var view:Dictionary=ui.model.read_postbattle()
	var b:Dictionary=view.bundle
	var waiting:Array=b.school.idle_student_ids.duplicate()
	waiting.sort()
	return ui.model.stage()=="returned_school" and _roster(ui,OLD_IDS+[14,15,11]) and b.school.derived_student_ids==ROSTER and waiting==[11,14,15] and [b.school.month,b.school.week,b.school.adventure_gate,b.school.lecture_active,b.flags["0x7a55f6"],b.flags["0x7e11a0"]]==[9,5,0,0,11,0] and Week.Adventures.available(view.planning.ledger).map(func(row):return row.id)==[11,35,17]

func _resume_five(ui) -> bool:
	var saved:Dictionary=ui.model.export_save()
	if not _school_five(ui) or saved.version!=30 or saved.state_sha256!=JSON.parse_string(FileAccess.get_file_as_string(ui.save_path)).state_sha256:return false
	var panel=ui.postbattle_panel
	panel.find_child("member_14",true,false).pressed.emit()
	panel.assignments.get_child(4).get_child(3).pressed.emit()
	if ui.model.read_postbattle().bundle.school.derived_student_ids[4]!=[13,14,-1,-1]:return false
	panel.find_child("adventure_11",true,false).pressed.emit()
	if ui.model.read_postbattle().bundle.school.lecture_work_fields!=[1,2,11,0] or ui.model.export_save().commands.size()!=saved.commands.size()+2:return false
	var altered:=saved.duplicate(true)
	altered.rules.mandatory_twenty_four="changed"
	if ui.model.restore(altered).get("reason")!="save_rules_changed":return false
	print("RELOADED ",saved.state_sha256," commands ",saved.commands.size()," continued with ",ui.model.export_save().commands.slice(-2))
	return true
