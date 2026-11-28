extends "../devtools/verify_september_adventure24.gd"

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() not in [1,2] or FileAccess.get_sha256(args[0])!="1437a80bf7b27c16dec9304d52b2d54e686d4aa83f54d91ad5a3736612e24fad" or (args.size()==2 and FileAccess.file_exists(args[1])):
		quit(1)
		return
	var ui := Screen.new()
	ui.auto_load=false
	ui.autosave=false
	root.add_child(ui)
	ui.save_path=args[0]
	ui.load_button.pressed.emit()
	var ok := _school_five(ui)
	var panel=ui.postbattle_panel
	if ok:
		panel.find_child("member_14",true,false).pressed.emit()
		panel.assignments.get_child(4).get_child(3).pressed.emit()
		panel.find_child("adventure_11",true,false).pressed.emit()
		for group in range(5):
			panel.find_child("mode_%d_0"%group,true,false).pressed.emit()
		var depart: Button=panel.find_child("depart",true,false)
		ok=depart!=null and not depart.disabled
		if ok:
			depart.pressed.emit()
			panel.commit_dialog.hide()
			panel.commit_dialog.confirmed.emit()
			ok=ui.model.stage()=="sortie_pending"
	if ok:
		if args.size()==2:
			var checkpoint := FileAccess.open_compressed(args[1],FileAccess.WRITE,FileAccess.COMPRESSION_ZSTD)
			if checkpoint==null:
				ui.free()
				quit(1)
				return
			checkpoint.store_string(JSON.stringify(ui.model.read_postbattle().planning.handoff))
			checkpoint.close()
		panel.find_child("play_sortie",true,false).pressed.emit()
		var s=ui.sortie_trial.session
		ok=s.ready and s.scene_id==11 and s.remaining_ticks==108000 and not s.eleven_mission.timers.is_empty()
		if ok:
			print("MAP11 school sortie ",s.controlled_units().size()," units, timers ",s.eleven_mission.timers)
			ok=_battle_and_return(ui,s)
	if not ok:printerr("MAP11 stopped at ",ui.model.stage()," ",ui._message)
	ui.free()
	quit(0 if ok else 1)

func _battle_and_return(ui,s) -> bool:
	while s.ending_snapshot().phase=="opening":
		s.advance_opening(true)
	var unit: Dictionary=s.controlled_units()[0]
	var start: Vector2i=unit.cell
	for direction in [Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT,Vector2i.UP]:
		if s.command_move(unit.character_id,start+direction):break
	for i in range(60):s.tick()
	if unit.cell==start:return false
	var attacks := 0
	for i in range(54005):
		if i%300==0:
			for member in s.controlled_units():
				if member.limits.hp<=0:continue
				var targets: Array=s.enemies().filter(func(e):return e.category==5 and e.side==5 and e.limits.hp>0)
				targets.sort_custom(func(a,b):return member.cell.distance_squared_to(a.cell)<member.cell.distance_squared_to(b.cell))
				if not targets.is_empty() and member.target!=targets[0].instance_id and s.command_attack(member.character_id,targets[0].instance_id):attacks+=1
		s.tick()
		if s.ending_snapshot().phase=="summary":break
	var facts: Dictionary=s.result_inputs()
	if facts.is_empty() or facts.scene_id!=11 or attacks==0:return false
	var party_size: int=s.controlled_units().size()
	print("MAP11 result ",facts.result_selector," escaped ",s.eleven_mission.escaped," attack orders ",attacks," ticks ",s.frame)
	ui.sortie_trial._refresh()
	ui.sortie_trial.continue_button.pressed.emit()
	if ui.model.stage()!="sortie_result":return false
	var view: Dictionary=ui.model.read_postbattle()
	var result: Dictionary=view.planning.sortie_summary
	print("MAP11 settlement ",result.score.total_delta," students ",result.students.size()," MVP ",result.recipient)
	if result.scene_id!=11 or result.date!=[9,5] or result.students.size()!=party_size:return false
	ui.postbattle_panel.find_child("continue_sortie_story",true,false).pressed.emit()
	for op in ["post_skip","post_next","post_skip","post_school"]:
		var advanced: Dictionary=ui.model.execute({"op":op})
		if not advanced.supported:
			printerr(op," ",advanced)
			return false
	var school: Dictionary=ui.model.read_postbattle().bundle.school
	print("MAP11 returned ",[school.month,school.week]," students ",school.student_count," total ",school.global_total_511c)
	return ui.model.stage()=="returned_school" and [school.month,school.week,school.student_count]==[10,1,16]
