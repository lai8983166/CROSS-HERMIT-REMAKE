extends SceneTree
const Arena := preload("res://sim/network_battle_session.gd")

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var school=load("res://school_playground.tscn").instantiate()
	school.auto_load=false
	school.autosave=false
	root.add_child(school)
	var entry: Array=school.find_children("*","Button",true,false).filter(func(b):return b.text=="对战练习")
	if entry.size()!=1:quit(1);return
	var args:=OS.get_cmdline_user_args()
	var scenario:=71 if args.is_empty() else int(args[0])
	entry[0].get_popup().id_pressed.emit(scenario)
	var view=school.sortie_trial
	if not view.visible or not view.session.ready:quit(1);return
	await process_frame
	var arena:=view.session as Arena
	var attacks:=0
	for tick in 27500:
		if tick%60==0 and arena._ending_phase=="active":
			for student in arena.controlled_units():
				if student.source_state!=1:continue
				if scenario==42 and student.cell.y>45:
					if student.path.is_empty():
						view.member_buttons[student.character_id].pressed.emit()
						view._command_cell(Vector2i(35,28))
					continue
				var opponents:=arena.enemies()
				if scenario==42:opponents=opponents.filter(func(u):return u.instance_id==1249)
				opponents.sort_custom(func(a,b):return student.cell.distance_squared_to(a.cell)<student.cell.distance_squared_to(b.cell))
				if not opponents.is_empty() and student.target!=opponents[0].instance_id:
					view.member_buttons[student.character_id].pressed.emit()
					if view._command_cell(opponents[0].cell) and student.target==opponents[0].instance_id:attacks+=1
		arena.tick()
		if arena._ending_phase=="summary":break
	print("Scene ",scenario," local practice ",arena._terminal_choice," attacks ",attacks," elapsed ",arena.elapsed," damage events ",arena.events.size())
	if arena._ending_phase!="summary":print("survivors ",arena.controlled_units().map(func(u):return [u.character_id,u.cell,u.limits.hp,u.target])," boss ",arena.find_unit(1249).get("cell"))
	var passed:=arena._ending_phase=="summary" and attacks>0 and not arena.events.is_empty()
	view._continue()
	await process_frame
	quit(0 if passed and not view.visible and not arena.ready else 1)
