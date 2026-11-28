extends SceneTree
## Three arguments play from the fixed parent. One argument reloads a saved milestone.
const Model := preload("res://sim/school_playground.gd")
const SchoolPanel := preload("res://ui/school_postbattle_panel.gd")
const START_SHA := "12118416dc0e9d40601e89463593a3b2d1d938d5a99a106f9131e257d3f7e0f8"
const ACTIVE := [3,9,5,8,6,1,16,17,13,14,15,11,18,32,2,7,28]
const PARTY := [28,7,16,8,17,6,5,9,1,13]

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() not in [1,3]:
		printerr("Pass a milestone save, or the fixed v38, victory trace and empty output directory.")
		quit(1)
		return
	if args.size()==3 and (FileAccess.get_sha256(args[0])!=START_SHA or not DirAccess.dir_exists_absolute(args[2]) or not DirAccess.get_files_at(args[2]).is_empty()):
		quit(1)
		return
	var model := Model.new()
	var loaded := model.load_file(args[0])
	if not loaded.supported:
		printerr("Save rejected: ",loaded.reason)
		quit(1)
		return
	var ok: bool
	if args.size()==3:
		var trace: Variant=JSON.parse_string(FileAccess.get_file_as_string(args[1]))
		ok=trace is Dictionary and _play(model,Model.Roles._integers(trace),args[2])
	else:
		ok=_reload(model)
	print("MAP31 campaign verification ",ok," at ",model.stage()," ",model.export_save().state_sha256)
	quit(0 if ok else 1)

func _act(model: Model, cmd: Dictionary) -> bool:
	var result := model.execute(cmd)
	if not result.supported:printerr(cmd.op," ",result.reason)
	return result.supported

func _panel_command(model: Model, button_name: String, expected: Dictionary, confirm := false) -> bool:
	var panel := SchoolPanel.new()
	root.add_child(panel)
	panel.show_state(model.read_postbattle(),{},"")
	var button := panel.find_child(button_name,true,false) as Button
	var commands := []
	panel.command.connect(func(cmd):commands.append(cmd))
	if button!=null and button.visible and not button.disabled:
		button.pressed.emit()
		if confirm and panel.commit_dialog.visible and commands.is_empty():panel.commit_dialog.confirmed.emit()
	panel.free()
	if commands!=[expected]:
		printerr("Panel command unavailable ",button_name," at ",model.stage())
		return false
	return _act(model,commands[0])

func _write(path: String, data: Dictionary) -> bool:
	var file := FileAccess.open(path,FileAccess.WRITE)
	if file==null:return false
	file.store_string(JSON.stringify(data))
	return file.get_error()==OK

func _pending(model: Model) -> bool:
	if model.stage()!="sortie_pending" or model.export_save().version!=39:return false
	var view := model.read_postbattle()
	var handoff: Dictionary=view.planning.handoff
	var round_data: Dictionary=handoff.prepared.rounds[0]
	return handoff.date==[12,1] and handoff.prepared.adventure_id==31 and round_data.scene_id==31 and round_data.student_ids==PARTY and round_data.teacher_ids==[107,110,115,118,116] and handoff.requested_states==[10,16]

func _play(model: Model, trace: Dictionary, out: String) -> bool:
	var opening := model.read_postbattle()
	if model.stage()!="returned_school" or model.export_save().version!=38 or opening.bundle.school.lecture_work_fields!=[3,24,31,0]:return false
	if model.execute({"op":"return_settle"}).supported:return false
	if not _act(model,{"op":"return_move","kind":"student","member_id":7,"target_group":0,"target_slot":1}):return false
	if not _panel_command(model,"depart",{"op":"return_depart"},true) or not _pending(model):return false
	if not model.save_file(out.path_join("pending.json")).supported:return false
	var submitted := model.read_postbattle()
	var handoff: Dictionary=submitted.planning.handoff
	trace=trace.get("trace",trace)
	var forged := trace.duplicate(true)
	forged.overflow=true
	if model.execute({"op":"sortie_finish","trace":forged}).supported:return false
	var receipt := Model.Postbattle.SortieRecord.replay(handoff,trace)
	if not receipt.supported:
		printerr(receipt.reason)
		return false
	if receipt.facts.result_selector not in [1,2,3]:return false
	if not _act(model,{"op":"sortie_finish","trace":trace}):return false
	if model.stage()!="sortie_result" or model.execute({"op":"sortie_finish","trace":trace}).supported:return false
	var settled := model.read_postbattle()
	if not _write(out.path_join("settled.json"),{"before":submitted.bundle,"after":settled.bundle}):return false
	if not _write(out.path_join("submission.json"),{"round":handoff.prepared.rounds[0],"ratings":handoff.prepared.class_ratings,"facts":receipt.facts}):return false
	if not _act(model,{"op":"post_next"}) or not _act(model,{"op":"post_skip"}):return false
	if model.stage()!="chapter309_choice" or model.read_postbattle().choice_labels.size()!=2:return false
	if model.execute({"op":"post_choice","choice":2}).supported:return false
	if not model.save_file(out.path_join("choice.json")).supported:return false
	if not _finish(model,0):return false
	return model.save_file(out.path_join("december-two-v39.json")).supported

func _finish(model: Model, choice: int) -> bool:
	if not _panel_command(model,"post_choice_%d"%choice,{"op":"post_choice","choice":choice}):return false
	if model.execute({"op":"post_choice","choice":choice}).supported:return false
	for i in range(8):
		match model.stage():
			"returned_school":return _school(model,choice)
			"post_story","new_week_story","school_entry_story":
				var op := "post_next" if model.read_postbattle().has("date_card") else "post_skip"
				if not _act(model,{"op":op}):return false
			"post_workroom":
				if not _act(model,{"op":"post_school"}):return false
			_:return false
	return false

func _school(model: Model, choice: int) -> bool:
	var view := model.read_postbattle()
	var bundle: Dictionary=view.bundle
	var school: Dictionary=bundle.school
	var ids := ACTIVE+([20,21] if choice==0 else [19])
	if [school.month,school.week,school.teacher_count,school.student_count]!=[12,2,6,ids.size()] or school.student_ids.slice(0,ids.size())!=ids:return false
	if bundle.sortie_result.scene_id!=31 or bundle.sortie_result.result_selector not in [1,2,3]:return false
	if bundle.chapter076_absent.participants.character_id!=4 or school.availability[4]!=0:return false
	if [bundle.flags["0x7a55f6"],bundle.flags["0x7e11a0"],bundle.adv_background]!=[11,1,13]:return false
	if view.planning.ledger.unlock_flags[30]!=1 or Model.Postbattle.Adventures.available(view.planning.ledger).any(func(row):return row.id==31):return false
	return model.export_save().version==39 and Model.Postbattle.Return.validate_planning_roster(bundle,Model.Postbattle.Return._rules()).is_empty()

func _reload(model: Model) -> bool:
	var payload := model.export_save()
	if payload.version!=39:return false
	var tampered := payload.duplicate(true)
	tampered.rules.mandatory_thirty_one="changed"
	if model.restore(tampered).supported or model.export_save()!=payload:return false
	match model.stage():
		"sortie_pending":return _pending(model)
		"chapter309_choice":return _finish(model,1)
		"returned_school":
			var choices: Array=payload.commands.filter(func(cmd):return cmd.op=="post_choice")
			return choices.size()==1 and _school(model,choices[0].choice)
	return false
