extends SceneTree
const Model := preload("res://sim/school_playground.gd")
const Sortie := preload("res://sim/school_sortie_session.gd")
const ROOT_SHA := "3c1eee1843f5835493569835514268d4cb81a6dcc8dad69d3c393d592eb9d82e"

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size()==3 and args[0]=="--reload":
		_reload(args[1],args[2])
		return
	var mixed: bool=not args.is_empty() and args[0]=="--mixed"
	var victory: bool=not args.is_empty() and args[0]=="--victory"
	if mixed or victory:args.remove_at(0)
	if args.size() not in [1,2,3] or FileAccess.get_sha256(args[0])!=ROOT_SHA or (args.size()>=2 and FileAccess.file_exists(args[1])):quit(2);return
	for pair in [[0,2],[36000,2],[36001,5],[54000,5],[54001,8],[108000,8],[108001,11]]:
		for lost in [false,true]:
			if Sortie.ThirtyThree.terminal_sub(pair[0],true,lost)!=pair[1] or Sortie.ThirtyThree.terminal_sub(pair[0],false,lost)!=(11 if lost else -1):quit(1);return
	var model := Model.new()
	var loaded := model.load_file(args[0])
	if not loaded.supported:printerr(loaded);quit(1);return
	print("Restored October origin ",model.stage())
	var commands := []
	if victory:
		var school: Dictionary=model.read_postbattle().bundle.school
		var waiting: Array=school.idle_student_ids.filter(func(id):return id>0)
		for group in range(5):
			for slot in range(4):
				if school.derived_student_ids[group][slot]<0 and not waiting.is_empty():
					commands.append({"op":"return_move","kind":"student","member_id":waiting.pop_front(),"target_group":group,"target_slot":slot})
	commands.append({"op":"return_select","adventure":33})
	for g in range(1 if mixed else 5):commands.append({"op":"return_mode","group":g,"teaching":false})
	commands.append({"op":"return_depart"})
	for command in commands:
		var result := model.execute(command)
		if not result.supported:printerr(command,result);quit(1);return
	var screen=preload("res://ui/school_playground.gd").new()
	screen.auto_load=false
	screen.autosave=false
	root.add_child(screen)
	screen.model=model
	screen.refresh()
	var play:Button=screen.postbattle_panel.find_child("play_sortie",true,false)
	if play==null or play.disabled:printerr("Missing school battle button");quit(1);return
	play.pressed.emit()
	var s:Sortie=screen.sortie_trial.session
	var handoff: Dictionary=model.read_postbattle().planning.handoff
	if not screen.sortie_trial.visible or not s.ready or s.scene_id!=33:printerr("Failed to open MAP33");quit(1);return
	print("MAP33 opened ",s.controlled_units().size()," students, ",s.enemies().size()," enemies")
	while s.ending_snapshot().phase=="opening":s.advance_opening(true)
	var issued := 0
	var previous_count := 74
	var last_change := 0
	for i in range(160000):
		if s._ending_phase=="event20":s.advance_event()
		if s._ending_phase=="summary":break
		if i%120==0:
			var party := s.controlled_units().filter(func(u):return u.source_state==1)
			var enemies := s.enemies().filter(func(u):return u.source_state==1 and u.category==5)
			if not enemies.is_empty() and not party.is_empty():
				var lead: Vector2i=party[0].cell
				enemies.sort_custom(func(a,b):return lead.distance_squared_to(a.cell)<lead.distance_squared_to(b.cell))
				if enemies.size()!=previous_count:
					previous_count=enemies.size()
					last_change=i
				var enemy: Dictionary=enemies[int((i-last_change)/2400)%enemies.size()]
				var target: int=enemy.instance_id
				if mixed and enemies.any(func(u):return u.instance_id==1240):target=1240
				if victory:_cast_skills(s,party,enemy)
				for u in party:
					if u.target!=target and s.command_attack(u.character_id,target):issued+=1
		s.tick()
	print("MAP33 result ",s._terminal_choice," valid attacks ",issued," elapsed ",s.elapsed)
	if victory and (s.ending_sub!=8 or not Sortie.ThirtyThree.cleared(s.units)):printerr("Army failed to clear the field");quit(1);return
	if issued==0 or s._ending_phase!="summary" or s.battle_trace().overflow:quit(1);return
	var before: Dictionary=model.read_postbattle().bundle
	var result:=model.execute({"op":"sortie_finish","trace":s.battle_trace()})
	if result.supported:
		var summary: Dictionary=model.read_postbattle().planning.sortie_summary
		if args.size()==3:
			if DirAccess.make_dir_recursive_absolute(args[2])!=OK:quit(2);return
			var objects: Dictionary={"settlement":{"before":before,"after":model.read_postbattle().bundle},"submission":{"round":handoff.prepared.rounds[0],"ratings":handoff.prepared.class_ratings,"facts":s.result_inputs()}}
			for key in objects:
				var path: String=args[2].path_join(key+".json")
				if FileAccess.file_exists(path):quit(2);return
				var file:=FileAccess.open(path,FileAccess.WRITE)
				if file==null:quit(2);return
				file.store_string(JSON.stringify(objects[key]))
				file.close()
		print("MAP33 settled ",summary.score.total_delta," XP, MVP ",summary.get("recipient")," grade ",summary.get("task_grade"))
	for op in ["post_next","post_skip","post_next","post_skip","post_school"]:
		if not result.supported:break
		result=model.execute({"op":op})
	var bundle: Dictionary=model.read_postbattle().bundle
	print("October return ",model.stage()," ",result," date ",bundle.school.month,"/",bundle.school.week)
	if not result.supported or model.stage()!="returned_school" or [bundle.school.month,bundle.school.week]!=[10,2]:quit(1);return
	if args.size()>=2 and not model.save_file(args[1]).supported:quit(1);return
	print("Returned digest ",model.export_save().state_sha256)
	quit(0)

func _cast_skills(s: Sortie, party: Array, enemy: Dictionary) -> void:
	var caster:=s.find_unit(3)
	if not caster.is_empty() and caster.source_state==1:
		if not s.cast_field_spell(3,enemy.cell,59) and caster.get("barrier_until",0)<=s.elapsed:
			s.cast_field_spell(3,caster.cell,57)
	var wounded: Array=party.duplicate()
	wounded.sort_custom(func(a,b):return a.limits.hp*b.limits.hp_max<b.limits.hp*a.limits.hp_max)
	if wounded[0].limits.hp*100<80*wounded[0].limits.hp_max:s.cast_field_spell(9,wounded[0].cell,31)
	s.cast_aimed_skill(4,enemy.instance_id,20)
	s.cast_aimed_skill(5,enemy.instance_id,11)


func _reload(origin: String, saved: String) -> void:
	if FileAccess.get_sha256(origin)!=ROOT_SHA:quit(2);return
	var base: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(origin))
	var restored: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(saved))
	if restored.version!=32 or restored.commands.size()<=base.commands.size() or restored.commands.slice(0,base.commands.size())!=base.commands:
		printerr("October save does not continue the expected root");quit(1);return
	var model:=Model.new()
	var read:=model.load_file(saved)
	if not read.supported:printerr(read);quit(1);return
	var bundle: Dictionary=model.read_postbattle().bundle
	var score:Dictionary=bundle.sortie_result.score
	var ok: bool=model.stage()=="returned_school" and [bundle.school.month,bundle.school.week]==[10,2] and bundle.sortie_result.scene_id==33 and model.export_save().state_sha256==restored.state_sha256
	print("Cold MAP33 return ",model.stage()," grade ",score.task_grade," score ",score.total_after," state ",restored.state_sha256)
	quit(0 if ok else 1)
