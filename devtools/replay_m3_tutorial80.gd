extends SceneTree
const Tutorial := preload("res://sim/tutorial_eighty_session.gd")

func _initialize() -> void:
	call_deferred("_run")


func _run() -> void:
	var view := preload("res://ui/school_sortie_trial.gd").new()
	root.add_child(view)
	if not view.open_tutorial():quit(1);return
	await process_frame
	var session := view.session as Tutorial
	while session._ending_phase=="opening":view._continue()
	var player: Dictionary=session.units[0]
	if not view._command_cell(Vector2i(18,8)):quit(1);return
	var attacks := 0
	var spells := 0
	for i in range(60000):
		while session._ending_phase=="event20":view._continue()
		if session.lesson==3:
			view._tutorial_action()
			if session.lesson!=4:break
			continue
		if session.lesson==4:
			session.select(1239)
			view._tutorial_action()
			if session.lesson!=5:break
		if session._ending_phase=="summary":break
		if i%45==0 and session.lesson in [1,2]:
			var targets := session.enemies().filter(func(u):return u.source_state==1 and u.limits.hp>0)
			targets.sort_custom(func(a,b):return player.cell.distance_squared_to(a.cell)<player.cell.distance_squared_to(b.cell))
			if session.lesson==2 and not targets.is_empty():
				view.spell_choice.select(view.spell_choice.get_item_index(59))
				if view._command_cell(targets[0].cell):
					spells+=1
					continue
				view.spell_choice.select(0)
			if not targets.is_empty() and player.target!=targets[0].instance_id and session.command_attack(player.instance_id,targets[0].instance_id):attacks+=1
		session.tick()
		if player.limits.hp<=0:break
	print("MAP80 lesson ",session.lesson," attacks ",attacks," lightning casts ",spells," elapsed ",session.elapsed," HP ",player.limits.hp," phase ",session._ending_phase," outcome ",session._terminal_choice)
	var passed := session.lesson==5 and session._ending_phase=="summary" and attacks>=5 and spells>0
	view._continue()
	await process_frame
	quit(0 if passed and not view.visible and not session.ready else 1)
