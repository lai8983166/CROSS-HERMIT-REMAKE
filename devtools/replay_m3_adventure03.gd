extends SceneTree
const Three := preload("res://sim/school_three_departure.gd")
const Sortie := preload("res://sim/school_sortie_session.gd")

func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size()!=1:quit(2);return
	var handoff := Three.load_save(args[0])
	var session := Sortie.new()
	if handoff.is_empty() or not session.open(handoff):printerr("MAP03 admission failed");quit(1);return
	print("MAP03 admitted ",session.controlled_units().size()," students")
	while session.ending_snapshot().phase=="opening":session.advance_opening(true)
	var unit: Dictionary=session.controlled_units()[0]
	var moved := false
	for d in [Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT,Vector2i.UP]:
		if session.command_move(unit.character_id,unit.cell+d):moved=true;break
	if not moved:printerr("No legal move");quit(1);return
	var start: Vector2i=unit.cell
	for i in range(24):session.tick()
	if unit.cell==start:printerr("Unit did not move");quit(1);return
	var target: Dictionary=session.enemies()[0]
	var attacked := false
	for member in session.controlled_units():
		if session.command_attack(member.character_id,target.instance_id):attacked=true
	if not attacked:printerr("No legal attack");quit(1);return
	for i in range(36500):
		if i%120==0 and session._ending_phase=="active":
			for member in session.controlled_units():
				if member.limits.hp<=0:continue
				var closest := {}
				var distance := 999999
				for enemy in session.enemies():
					if enemy.category!=5 or enemy.limits.hp<=0:continue
					var delta: int=member.cell.distance_squared_to(enemy.cell)
					if delta<distance:
						distance=delta
						closest=enemy
				if not closest.is_empty():
					if member.target!=closest.instance_id:session.command_attack(member.character_id,closest.instance_id)
				else:
					for object_id in [1248,1247,1246]:
						var object:=session.find_unit(object_id)
						if object.side!=0:
							session.command_move(member.character_id,object.cell+Vector2i.DOWN)
							break
		session.tick()
		if session._ending_phase=="event20":session.advance_event()
		if session._ending_phase=="summary":break
	if session.ending_sub<0 or session.ending_snapshot().phase!="summary":
		printerr("No objective result");quit(1);return
	if not session.three_score.get("supported",false):printerr(session.three_score);quit(1);return
	var trace := session.battle_trace()
	if trace.overflow or session._terminal_choice!={"tactical_result_selector":1,"script_sub":5} or session.ending_snapshot().summary.defeated_enemies!=38 or session.three_score.characters.size()!=20 or session.three_score.total_delta!=40174:
		printerr("MAP03 replay differs from the accepted result");quit(1);return
	print("MAP03 commands ",trace.commands.size()," ticks ",trace.ticks," SHA-256 ",JSON.stringify(trace).sha256_text())
	print("MAP03 score ",session.three_score.total_delta," packages ",session.three_score.characters.size())
	print("MAP03 selector ",session._terminal_choice," defeated ",session.ending_snapshot().summary.defeated_enemies)
	print("MAP03 tick ",session.elapsed," cell ",unit.cell)
	quit(0)
