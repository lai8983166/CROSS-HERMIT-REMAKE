extends SceneTree
## Replay the fixed order history against an imported v7 departure, recording the first rejection.
const Campaign := preload("res://sim/school_native_campaign.gd")
const Record := preload("res://sim/school_battle_record.gd")
const TRACE_SHA := "b759b1f62f2bdcc3db937d52da17649985fb30c3df6835029093befb552f8107"
const REFERENCE_SHA := "7364582c5aaf000907a3d82b94d2e59c58db8cea73616881abf2d9e5646d0edb"
var battle := Campaign.Sortie.new()
var receipts := []
var samples := []

func _initialize() -> void:
	call_deferred("_run")

func _observe(row: Array, accepted: bool) -> void:
	receipts.append({"sequence":receipts.size()+1,"expected_frame":row[0],"actual_frame":battle._trace_clock,
		"elapsed":battle.elapsed,"accepted":accepted})
	if not samples.is_empty() and samples.back().elapsed==battle.elapsed:return
	var students := []
	for unit in battle.controlled_units():
		students.append([unit.character_id,unit.side,unit.source_state,unit.cell.x,unit.cell.y,
			unit.limits.hp_max,unit.limits.hp,unit.limits.mp_max,unit.limits.mp])
	samples.append({"elapsed":battle.elapsed,"frame":battle._trace_clock,"students":students})

func _run() -> void:
	var args:=OS.get_cmdline_user_args()
	if args.size()!=5 or FileAccess.file_exists(args[4]) or FileAccess.get_sha256(args[1])!=args[2] or FileAccess.get_sha256(args[3])!=TRACE_SHA:
		quit(2)
		return
	var campaign:=Campaign.new()
	var handoff: Dictionary
	match args[0]:
		"original_save":
			if not campaign.load_origin(args[1]):quit(2);return
			handoff=campaign.departure()
		"reference":
			if args[2]!=REFERENCE_SHA:quit(2);return
			handoff=battle.Limits._source_numbers(JSON.parse_string(FileAccess.get_file_as_string(args[1])))
		_:quit(2);return
	if handoff.is_empty() or handoff.date!=[13,2] or handoff.prepared.adventure_id!=44 or not battle.open(handoff):quit(2);return
	var trace: Dictionary=battle.Limits._source_numbers(JSON.parse_string(FileAccess.get_file_as_string(args[3])))
	var result:=Record.run_trace(battle,trace,_observe)
	var first_attempt:=result.duplicate()
	var first_rejection:=0
	while not result.supported and receipts.size()<trace.commands.size() and battle._ending_phase=="active":
		var remaining:=trace.duplicate()
		remaining.commands=trace.commands.slice(receipts.size())
		var previous:=receipts.size()
		result=Record.run_trace(battle,remaining,_observe)
		if receipts.size()==previous:break
	for receipt in receipts:
		if not receipt.accepted:
			first_rejection=receipt.sequence
			break
	# Different starting attributes can change the end time even with identical inputs.
	var deadline:=battle._trace_clock+maxi(0,battle.remaining_ticks)+4
	while battle._ending_phase=="active" and battle._trace_clock<deadline:battle.tick()
	for step in range(4):
		if battle._ending_phase=="summary":break
		battle.advance_exit()
	var report:={"source_kind":args[0],"source_sha256":args[2],"trace_sha256":TRACE_SHA,
		"replay":first_attempt,"first_rejected_sequence":first_rejection,"unattempted":trace.commands.size()-receipts.size(),
		"receipts":receipts,"samples":samples,"facts":battle.result_inputs()}
	if args[0]=="original_save":
		report.returned=battle._ending_phase=="summary" and campaign.finish(battle,args[4].get_base_dir())
		if report.returned:report.school_save=campaign.save_path
	var output:=FileAccess.open(args[4],FileAccess.WRITE)
	if output==null:quit(2);return
	output.store_string(JSON.stringify(report))
	output.close()
	print("MAP44 ",args[0]," orders ",receipts.size()," first rejected ",first_rejection," replay ",first_attempt," checkpoints ",samples.size())
	quit(0 if first_attempt.supported and battle._ending_phase=="summary" and report.get("returned",true) else 1)
