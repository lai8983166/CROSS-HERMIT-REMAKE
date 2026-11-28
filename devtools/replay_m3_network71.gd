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
				var opponents:=arena.enemies()
				opponents.sort_custom(func(a,b):return student.cell.distance_squared_to(a.cell)<student.cell.distance_squared_to(b.cell))
				if not opponents.is_empty() and student.target!=opponents[0].instance_id:
					view.member_buttons[student.character_id].pressed.emit()
					if view._command_cell(opponents[0].cell) and student.target==opponents[0].instance_id:attacks+=1
		arena.tick()
		if arena._ending_phase=="summary":break
	print( "MAP",scenario," local practice ",arena._terminal_choice," attacks ",attacks," elapsed ",arena.elapsed," damage events ",arena.events.size())
	var passed:=arena._ending_phase=="summary" and attacks>0 and not arena.events.is_empty()
	view._continue()
	await process_frame
	quit(0 if passed and not view.visible and not arena.ready else 1)
