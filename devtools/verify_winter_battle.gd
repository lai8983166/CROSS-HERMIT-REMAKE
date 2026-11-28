extends SceneTree
## Verify a complete command trace from the submitted school handoff in a fresh process.
const Record := preload("res://sim/school_sortie_record.gd")


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	var args:=OS.get_cmdline_user_args()
	if args.size()!=3:
		printerr("Pass the submitted handoff, recorded commands and output facts path.")
		quit(1)
		return
	var handoff: Variant=Record.Sortie.Limits._source_numbers(JSON.parse_string(FileAccess.get_file_as_string(args[0])))
	var trace: Variant=Record.Sortie.Limits._source_numbers(JSON.parse_string(FileAccess.get_file_as_string(args[1])))
	if not handoff is Dictionary or not trace is Dictionary or handoff.get("date") not in Record.Sortie.Winter.DATES.values():
		quit(1)
		return
	var start:=Time.get_ticks_msec()
	var receipt:=Record.replay(handoff,trace)
	if not receipt.supported or receipt.facts.result_selector not in [1,2,3,4] or (receipt.facts.result_selector==4 and receipt.facts.scene_id!=29):
		printerr(receipt)
		quit(1)
		return
	var file:=FileAccess.open(args[2],FileAccess.WRITE)
	if file==null:
		quit(1)
		return
	file.store_string(JSON.stringify(receipt.facts))
	file.close()
	print("MAP",receipt.facts.scene_id," selector ",receipt.facts.result_selector," commands ",trace.commands.size()," ticks ",trace.ticks," replay_ms ",Time.get_ticks_msec()-start)
	quit()
