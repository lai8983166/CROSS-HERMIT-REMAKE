extends RefCounted
const Return := preload("res://sim/school_native_return.gd")
const Sortie := preload("res://sim/school_sortie_session.gd")
const Record := preload("res://sim/school_battle_record.gd")
const SAVE_DIR := "user://original-school"
const EXTENSION := "chschool"
var origin_path := ""
var state := {}
var rounds: Array = []
var save_path := ""

func load_origin(path: String) -> bool:
	var file := FileAccess.open(path,FileAccess.READ)
	if file==null or file.get_length()!=0x306d4:return false
	var next := Return.from_save(file.get_buffer(0x306d4))
	if next.is_empty():return false
	origin_path=path
	state=next
	rounds=[]
	save_path=""
	return true


func departure() -> Dictionary:
	return Return.handoff(state) if not state.is_empty() else {}


func finish(battle: Sortie, directory := SAVE_DIR) -> bool:
	if state.is_empty() or battle._ending_phase!="summary":return false
	var admission := departure()
	if admission.is_empty() or admission!=battle.departure or battle.scene_id!=admission.prepared.adventure_id:return false
	var trace := battle.battle_trace()
	if not _valid_trace(trace):return false
	var next := Return.settle(state,admission,battle.result_inputs(),battle.native_score)
	if next.is_empty():return false
	var entry := {"scene":battle.scene_id,"trace":trace,"state_sha256":_state_hash(next)}
	var completed := rounds.duplicate()
	completed.append(entry)
	var body := {"version":1,"source_path":origin_path,"source_sha256":state.origin_sha,"rounds":completed}
	var payload := JSON.stringify(body,"",true)
	var hash := payload.sha256_text()
	var root_path := ProjectSettings.globalize_path(directory)
	if DirAccess.make_dir_recursive_absolute(root_path)!=OK:return false
	var month := "january" if next.school.month==13 else "april"
	var path := root_path.path_join("%s-%d-%s.%s" % [month,next.school.week,hash,EXTENSION])
	if FileAccess.file_exists(path):
		if FileAccess.get_file_as_string(path)!=payload:return false
	else:
		var temporary := path+".%d-%d.tmp" % [OS.get_process_id(),Time.get_ticks_usec()]
		var output := FileAccess.open(temporary,FileAccess.WRITE)
		if output==null:return false
		output.store_string(payload)
		output.flush()
		var ok := output.get_error()==OK
		output.close()
		if not ok or DirAccess.rename_absolute(temporary,path)!=OK:
			if FileAccess.file_exists(temporary):DirAccess.remove_absolute(temporary)
			if not FileAccess.file_exists(path) or FileAccess.get_file_as_string(path)!=payload:return false
	state=next
	rounds=completed
	save_path=path
	return true


func load_progress(path: String) -> bool:
	var input := FileAccess.open(path,FileAccess.READ)
	if input==null or input.get_length()>4194304:return false
	var payload := input.get_as_text()
	var body=JSON.parse_string(payload)
	if not body is Dictionary or body.size()!=4 or body.get("version")!=1 or not body.get("source_path") is String or not body.get("rounds") is Array:return false
	if body.rounds.is_empty() or body.rounds.size()>3:return false
	var candidate = get_script().new()
	if not candidate.load_origin(body.source_path) or body.get("source_sha256")!=candidate.state.origin_sha:return false
	for entry in body.rounds:
		var admission: Dictionary=candidate.departure()
		if admission.is_empty() or not entry is Dictionary or entry.size()!=3 or entry.get("scene")!=admission.prepared.adventure_id or not _valid_trace(entry.get("trace")):return false
		var battle := Sortie.new()
		if not battle.open(admission):return false
		var trace: Dictionary=Sortie.Limits._source_numbers(entry.trace)
		if not Record.run_trace(battle,trace).supported or battle.battle_trace()!=trace or battle._ending_phase!="summary":return false
		var next := Return.settle(candidate.state,admission,battle.result_inputs(),battle.native_score)
		if next.is_empty() or _state_hash(next)!=entry.get("state_sha256"):return false
		candidate.state=next
		candidate.rounds.append({"scene":battle.scene_id,"trace":trace,"state_sha256":entry.state_sha256})
		battle.close()
	origin_path=candidate.origin_path
	state=candidate.state
	rounds=candidate.rounds
	save_path=path
	return true


static func _state_hash(value: Dictionary) -> String:
	return JSON.stringify(value,"",true).sha256_text()


static func _valid_trace(value: Variant) -> bool:
	if not value is Dictionary or value.size()!=4 or value.get("version")!=1 or value.get("overflow")!=false:return false
	if not value.get("commands") is Array or value.commands.size()>Record.MAX_COMMANDS:return false
	if not _integer(value.get("ticks"),0,Record.MAX_SORTIE_TICKS):return false
	var previous := 0
	for row in value.commands:
		if not row is Array or row.size()<2 or not _integer(row[0],previous,int(value.ticks)) or not _integer(row[1],1,11):return false
		previous=int(row[0])
		var sizes := [0,3,2,5,4,3,2,5,5,5,4,4]
		if row.size()!=sizes[int(row[1])]:return false
		for i in range(2,row.size()):
			if not _integer(row[i],0,1249):return false
	return true


static func _integer(value: Variant, low: int, high: int) -> bool:
	return (value is int or value is float) and value==int(value) and value>=low and value<=high
