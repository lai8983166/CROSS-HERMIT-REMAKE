extends SceneTree
const Campaign := preload("res://sim/school_native_campaign.gd")
const Sortie := preload("res://sim/school_sortie_session.gd")
const SAVE_SHA := "d97cdbcb6e76ad8f285f8733c6a63561e0dab102ad5e3c2457a3750ccf0336e4"

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() not in [1,2] or FileAccess.get_sha256(args[0])!=SAVE_SHA:
		quit(2)
		return
	var s := Sortie.new()
	var campaign := Campaign.new()
	if not campaign.load_origin(args[0]) or not s.open(campaign.departure()) or s.scene_id!=1:
		printerr("Prepared week-one school admission failed")
		quit(1)
		return
	while s._ending_phase=="opening": s.advance_opening(true)
	var party:=s.controlled_units()
	var attack_orders:=0
	for tick in range(24000):
		if s._ending_phase=="event20": s.advance_event()
		if tick%180==0 and s._ending_phase=="active":
			for i in party.size():
				var u: Dictionary=party[i]
				if u.limits.hp<=0: continue
				var object: Dictionary=s.find_unit(1244+i%3)
				if object.side!=0:
					var cell: Vector2i=object.cell+Vector2i(i/3%3-1,1+i/9)
					if u.path.is_empty() and cell!=u.cell: s.command_move(u.character_id,cell)
				else:
					var closest: Dictionary={}
					var distance:=999999
					for e in s.enemies():
						if e.character_id>=387 or e.limits.hp<=0: continue
						var d:int=u.cell.distance_squared_to(e.cell)
						if d<distance:
							closest=e
							distance=d
					if not closest.is_empty() and u.target!=closest.instance_id and s.command_attack(u.character_id,closest.instance_id):
						attack_orders+=1
		s.tick()
		if s._ending_phase=="summary": break
	print("MAP01 ",s._terminal_choice," waves=",s.one_mission.wave_index," escaped=",s.one_mission.escaped," events=",s.one_mission.shown," attack orders=",attack_orders," elapsed=",s.elapsed," score=",s.native_score.get("total_delta"))
	if args.size()==2:
		if not campaign.finish(s,args[1]):printerr("MAP01 return failed");quit(1);return
		var output:=FileAccess.open(args[1].path_join("native-expected.json"),FileAccess.WRITE)
		if output==null:quit(1);return
		output.store_string(JSON.stringify({"score":s.native_score,"facts":s.result_inputs(),"state":campaign.state}))
		output.close()
		print("Saved ",campaign.save_path)
	quit(0 if s._ending_phase=="summary" and s._terminal_choice.tactical_result_selector in [1,2,3] and s.one_mission.wave_index==4 and attack_orders>0 and s.native_score.get("characters",[]).size()==20 else 1)
