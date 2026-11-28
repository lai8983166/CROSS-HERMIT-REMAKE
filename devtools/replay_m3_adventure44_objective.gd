extends SceneTree
## Observe the original objective routine's input fields at every evaluation.
const Record := preload("res://sim/school_sortie_record.gd")

class ObservedBattle extends Record.Sortie:
	var evaluations := 0
	var samples := []

	func _detect_trial_end() -> bool:
		evaluations += 1
		var active := {}
		for unit in units:
			active[unit_key(unit)] = unit
		var actors := []
		for actor in catalog.actors:
			var id: int = actor.instance_id
			if active.has(id):
				var unit: Dictionary = active[id]
				actors.append([actor.work_index, actor.character_id, unit.side, unit.source_state])
			elif reserves.has(id):
				var record := String(reserves[id].record_hex).hex_decode()
				actors.append([actor.work_index, actor.character_id, int(record[0xa4]), int(record[15])])
		for slot in _participant_ids.size():
			var id: int = _participant_ids[slot]
			var unit: Dictionary = active[id]
			actors.append([slot, id, unit.side, unit.source_state])
		var ended := super._detect_trial_end()
		var sub := ending_sub if ended else -1
		if not samples.is_empty():
			var prior: Dictionary = samples.back()
			if prior.actors == actors and prior.losses == _own_casualties and prior.sub == sub and (prior.remaining == 0) == (remaining_ticks == 0):
				prior.last_tick = _trace_clock
				return ended
		samples.append({"tick": _trace_clock, "last_tick": _trace_clock, "remaining": remaining_ticks,
			"losses": _own_casualties, "actors": actors, "sub": sub})
		return ended


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() != 3:
		quit(1)
		return
	var handoff: Dictionary = Record.Sortie.Limits._source_numbers(JSON.parse_string(FileAccess.get_file_as_string(args[0])))
	var trace: Dictionary = Record.Sortie.Limits._source_numbers(JSON.parse_string(FileAccess.get_file_as_string(args[1])))
	var battle := ObservedBattle.new()
	if handoff.prepared.adventure_id != 44 or not Record.valid_trace(trace, handoff.date, 44) or not battle.open(handoff):
		quit(1)
		return
	if not Record.Record.run_trace(battle, trace).supported or battle.battle_trace() != trace or battle.evaluations != trace.ticks:
		quit(1)
		return
	var file := FileAccess.open(args[2], FileAccess.WRITE)
	if file == null:
		quit(1)
		return
	file.store_string(JSON.stringify({"facts": battle.result_inputs(), "samples": battle.samples}))
	file.close()
	print("Objective sample count ", battle.samples.size())
	quit(0)
