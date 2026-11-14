extends RefCounted
## Reconstruct a local battle from player commands, not saved result fields.
const Combat := preload("res://sim/school_combat_session.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const MAX_TICKS := 54064
const MAX_COMMANDS := 4096
static var _cache: Dictionary = {}


static func replay(preparation: Dictionary, combat: Dictionary, trace: Variant) -> Dictionary:
	if not valid_trace(trace): return _failure("invalid_battle_trace")
	var session := Combat.new()
	if not session.open(preparation,combat): return _failure("battle_context_rejected")
	# Even a warm cache must pass the current source/context admission in open().
	# These additional rules are read later, during result confirmation.
	var key := _cache_key(preparation,combat,trace)
	if _cache.has(key): return _cache[key].duplicate(true)
	for row in trace["commands"]:
		if not _advance(session,row[0]): return _failure("battle_trace_timing_rejected")
		var accepted := false
		match row[1]:
			1: accepted = session.advance_opening(row[2]==1)
			2: accepted = session.advance_event()
			3: accepted = session.command_move(row[2],Vector2i(row[3],row[4]))
			4: accepted = session.command_attack(row[2],row[3])
			5: accepted = session.stop(row[2])
			6: accepted = session.request_return()
		if not accepted: return _failure("battle_trace_command_rejected")
	if not _advance(session,trace["ticks"]): return _failure("battle_trace_terminal_rejected")
	for i in range(4): session.advance_exit()
	var ending := session.ending_snapshot()
	if ending["phase"]!="summary" or ending["settlement"].get("phase")!="round_result":
		return _failure("battle_result_not_reached")
	session.confirm_result(); session.confirm_result()
	var receipt := session.take_handoff()
	if receipt.get("successor")!="adv_ch003_pending" or receipt["battle_trace"]!=trace:
		return _failure("battle_record_mismatch")
	var result := {"supported":true,"receipt":receipt}
	# Cache only successful executions, keyed by full source context and commands.
	# It avoids replaying the same battle for each story-page backup validation.
	if _cache.size()>=4: _cache.erase(_cache.keys()[0])
	_cache[key] = result.duplicate(true)
	return result


static func _cache_key(preparation: Dictionary, combat: Dictionary, trace: Dictionary) -> String:
	var sources := []
	for path in ["res://data/school_course_confirmation_rules.json",Combat.Settlement.Preparation.RULE_PATH]:
		sources.append(FileAccess.get_sha256(path))
	return JSON.stringify([preparation,combat,trace,sources],"",true).sha256_text()


static func _advance(session: Combat, target: int) -> bool:
	while session._trace_clock < target:
		if session._ending_phase!="active": return false
		session.tick()
	return session._trace_clock==target


static func valid_trace(trace: Variant) -> bool:
	if not trace is Dictionary or trace.size()!=4 or trace.get("version")!=1 or trace.get("overflow")!=false \
			or not Roles._bounded(trace.get("ticks"),0,MAX_TICKS) or not trace.get("commands") is Array \
			or trace["commands"].size()>MAX_COMMANDS: return false
	var previous := 0
	for row in trace["commands"]:
		if not row is Array or row.size()<2 or not Roles._bounded(row[0],previous,trace["ticks"]) \
				or not Roles._bounded(row[1],1,6): return false
		previous = row[0]
		if row.size()!=[0,3,2,5,4,3,2][row[1]]: return false
		for value in row:
			if not value is int: return false
		if row[1]==1 and row[2] not in [0,1]: return false
		if row[1] in [3,4,5] and row[2] not in [3,4,9,1249]: return false
		if row[1]==3 and (row[3]<0 or row[3]>63 or row[4]<0 or row[4]>95): return false
		if row[1]==4 and not Roles._bounded(row[3],1000,1249): return false
	return true


static func _failure(reason: String) -> Dictionary:
	return {"supported":false,"reason":reason}
