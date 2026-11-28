extends SceneTree
const Campaign := preload("res://sim/school_native_campaign.gd")
const Sortie := preload("res://sim/school_sortie_session.gd")

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() not in [1,2]:quit(2);return
	var resume: bool=args[0].get_extension()=="chschool"
	if not resume and FileAccess.get_sha256(args[0]) != "fe596120b84afb3e3197198fb1aecc1289479c40b489f2b2dc5b03b320d83261":
		quit(2)
		return
	var s := Sortie.new()
	var campaign := Campaign.new()
	var loaded := campaign.load_progress(args[0]) if resume else campaign.load_origin(args[0])
	if not loaded or not s.open(campaign.departure()) or s.scene_id != 2:
		printerr("Week-two admission failed")
		quit(1)
		return
	while s._ending_phase == "opening":
		s.advance_opening(true)
	var initial := {}
	var damaged := false
	var moved := false
	var saw_search := false
	var party := s.controlled_units()
	for u in party:
		initial[u.character_id] = u.cell
	var order_count := 0
	var sent_to_exit := {}
	for i in range(37000):
		if s._ending_phase == "event20":
			saw_search = true
			s.advance_event()
		if s._ending_phase == "active" and i % 120 == 0:
			for u in party:
				if u.limits.hp <= 0:
					continue
				if u.limits.hp < u.limits.hp_max:
					damaged = true
				if u.cell != initial[u.character_id]:
					moved = true
				if not saw_search and u.character_id % 3 == 0 and u.target < 0:
					var nearest := {}
					var distance := 999999
					for enemy in s.enemies():
						if enemy.character_id >= 393 or enemy.limits.hp <= 0:
							continue
						var d: int = u.cell.distance_squared_to(enemy.cell)
						if d < distance:
							distance = d
							nearest = enemy
					if not nearest.is_empty() and s.command_attack(u.character_id, nearest.instance_id):
						order_count += 1
				elif (saw_search and not sent_to_exit.has(u.character_id)) or u.path.is_empty():
					var cells: Array = s.catalog.regions["2" if saw_search else "1"]
					if not saw_search and u.character_id % 3 == 1:
						cells = []
						for y in range(108,114):
							for x in range(30,37):
								cells.append(y*s.field_width+x)
					for offset in range(cells.size()):
						var index: int = cells[(u.character_id + offset) % cells.size()]
						var goal := Vector2i(index % s.field_width, index / s.field_width)
						if s.at_cell(goal).is_empty() and s.command_move(u.character_id, goal):
							if saw_search: sent_to_exit[u.character_id] = true
							break
		if i % 2400 == 0: print("MAP02 frame ",i," search=",saw_search," survivors=",party.filter(func(u): return u.limits.hp>0).size())
		s.tick()
		if s._ending_phase == "summary":
			break
	print("MAP02 ",s._terminal_choice," search=",saw_search," moved=",moved," damage=",damaged," attack_orders=",order_count," elapsed=",s.elapsed)
	var passed: bool = moved and damaged and saw_search and order_count > 0 and s._ending_phase == "summary" and s.ending_sub == 5 and s.native_score.get("supported", false) and s.native_score.characters.size() == 20
	if args.size()==2:
		if not campaign.finish(s,args[1]):
			printerr("Failed to settle played April sortie");quit(1);return
		var output:=FileAccess.open(args[1].path_join("native-expected.json"),FileAccess.WRITE)
		if output==null:quit(1);return
		output.store_string(JSON.stringify({"score":s.native_score,"facts":s.result_inputs(),"state":campaign.state}))
		output.close()
		print("Saved ",campaign.save_path)
		if resume:
			quit(0 if passed else 1);return
		var recovered:=Campaign.new()
		if not recovered.load_progress(campaign.save_path) or recovered.state!=campaign.state or recovered.departure().date!=[4,3]:
			printerr("Replay did not recover the same returned school");quit(1);return
		var next:=Sortie.new()
		if not next.open(recovered.departure()) or next.scene_id!=3:
			printerr("Returned squad could not enter MAP03");quit(1);return
		print("Verified cold week-three departure ",next.controlled_units().size()," participants, total ",recovered.state.score)
	quit(0 if passed else 1)
