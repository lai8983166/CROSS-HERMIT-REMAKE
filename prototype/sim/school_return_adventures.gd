extends RefCounted
## Current first-game school ledger and legal departure; scene8/17 play is separate.
const Return := preload("res://sim/school_postbattle_return.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const PATH := "res://data/school_return_adventures.json"
const SHA := "8ab8d1183a0a1594bfde53b508b1f1aa8974c9cd5788546abee7b9904760d0cb"


const SEVEN_PATH := "res://data/school_mandatory_seven.json"
const SEVEN_SHA := "213e7e0eebfae975b34ef46848de7d932802189d882e7709c077333a01e165e9"


const FOUR_PATH := "res://data/school_mandatory_four.json"
const FOUR_SHA := "1945461b23001b3fedee7bc1dadd60d83879cfee7c7a8831d6ae18a44d89345b"


const SIX_SHA := "c36bf8780a7cac839f5d252553ce5c6cf1bbee9079cf2642bc4241f1c66ae2ef"


const TEN_SHA := "c7fd4cfc64a1db8ecac16f4b38a20659ff60eb58f859448d891ad0902c4daf07"


const TWENTY_ONE_SHA := "dba560bf13643b6a508aa78dc124e659daa65ffd242f0de28c36e0a17b7dd591"
const TWENTY_SHA := "b9905930c50f7dba9e38e11ac3147dc44d435dd0b3702ee2a257fa88742fb111"
const FOURTEEN_SHA := "5ec40375187a29298bc201e49d8609b2bcee485f7133d52be1e4f85dd47b20a6"


const NINE_SHA := "603b38da89fed576a3b7c337186eb6c8d12336887db6e39a90ff206abe80d068"


const EIGHTEEN_SHA := "09aa3f8c4beed7d571f067c7145eb06a4b9e6c54b96436a8bbfdc3875ee6d018"


const THIRTEEN_SHA := "89f0df1ec15347a5c01402a5f9accba74854dac155ce95f91a1be0b013ecd61d"


static func twenty_one_rules() -> Dictionary:
	var raw := FileAccess.get_file_as_string("res://data/school_mandatory_twenty_one.json").replace("\r\n","\n")
	return {} if raw.sha256_text()!=TWENTY_ONE_SHA else Roles._integers(JSON.parse_string(raw))


static func twenty_rules() -> Dictionary:
	var raw := FileAccess.get_file_as_string("res://data/school_mandatory_twenty.json").replace("\r\n","\n")
	return {} if raw.sha256_text()!=TWENTY_SHA else Roles._integers(JSON.parse_string(raw))


static func fourteen_rules() -> Dictionary:
	var raw := FileAccess.get_file_as_string("res://data/school_mandatory_fourteen.json").replace("\r\n","\n")
	return {} if raw.sha256_text()!=FOURTEEN_SHA else Roles._integers(JSON.parse_string(raw))


static func nine_rules() -> Dictionary:
	var raw := FileAccess.get_file_as_string("res://data/school_mandatory_nine.json").replace("\r\n","\n")
	return {} if raw.sha256_text()!=NINE_SHA else Roles._integers(JSON.parse_string(raw))


static func eighteen_rules() -> Dictionary:
	var raw := FileAccess.get_file_as_string("res://data/school_july_eighteen.json").replace("\r\n","\n")
	if raw.sha256_text()!=EIGHTEEN_SHA:return {}
	return Roles._integers(JSON.parse_string(raw))


static func thirteen_rules() -> Dictionary:
	var raw := FileAccess.get_file_as_string("res://data/school_mandatory_thirteen.json").replace("\r\n","\n")
	return {} if raw.sha256_text()!=THIRTEEN_SHA else Roles._integers(JSON.parse_string(raw))


static func ten_rules() -> Dictionary:
	var raw := FileAccess.get_file_as_string("res://data/school_mandatory_ten.json").replace("\r\n","\n")
	return {} if raw.sha256_text()!=TEN_SHA else Roles._integers(JSON.parse_string(raw))


static func six_rules() -> Dictionary:
	var raw := FileAccess.get_file_as_string("res://data/school_mandatory_six.json").replace("\r\n","\n")
	return {} if raw.sha256_text()!=SIX_SHA else Roles._integers(JSON.parse_string(raw))


static func four_rules() -> Dictionary:
	var raw := FileAccess.get_file_as_string(FOUR_PATH).replace("\r\n","\n")
	return {} if raw.sha256_text()!=FOUR_SHA else Roles._integers(JSON.parse_string(raw))


static func seven_rules() -> Dictionary:
	var raw := FileAccess.get_file_as_string(SEVEN_PATH).replace("\r\n","\n")
	return {} if raw.sha256_text()!=SEVEN_SHA else Roles._integers(JSON.parse_string(raw))


static func mandatory_rules(id: int) -> Dictionary:
	match id:
		4:return four_rules()
		6:return six_rules()
		7:return seven_rules()
		9:return nine_rules()
		10:return ten_rules()
		13:return thirteen_rules()
		14:return fourteen_rules()
		20:return twenty_rules()
		21:return twenty_one_rules()
	return {}


static func rules() -> Dictionary:
	var raw := FileAccess.get_file_as_string(PATH).replace("\r\n","\n")
	return {} if raw.sha256_text()!=SHA else Roles._integers(JSON.parse_string(raw))


static func initial() -> Dictionary:
	var source := rules()
	if source.is_empty():return {}
	# Reconstruct only the owned new-game command lineage, not arbitrary saves.
	var ledger := {"entries":[],"unlock_flags":[]}
	ledger["unlock_flags"].resize(100);ledger["unlock_flags"].fill(0)
	_open(ledger,4,4,source)
	ledger=advance(ledger,0) # The first course week submits with no adventure.
	_open(ledger,4,5,source)
	ledger=advance(ledger,5) # Mandatory5 was committed before the first battle.
	_open(ledger,5,1,source)
	return ledger


static func _open(ledger: Dictionary, month: int, week: int, source: Dictionary) -> void:
	for row in source["adventures"]:
		if ledger["unlock_flags"][row["id"]-1]!=0 or not row["present"] or not row["gate"] or not row["kind"] or row["month"]!=month or row["week"]!=week:continue
		var limit: int=-1 if row["duration"]==99 else row["duration"]
		ledger["entries"].push_front({"id":row["id"],"metadata":[row["kind"]-1,(row["subkind"]-1)&255,0 if row["kind"]==4 else 1 if limit==-1 else 2],
			"busy":0,"limit":limit,"duration":row["cooldown"],"busy_elapsed":0,"elapsed":0})
		ledger["unlock_flags"][row["id"]-1]=1


static func advance(ledger: Dictionary, selected: int) -> Dictionary:
	var after := ledger.duplicate(true)
	for row in after["entries"]:
		if row["id"]==selected:
			if row["duration"]<1:after["entries"].erase(row)
			else:row["busy"]=1;row["busy_elapsed"]=0
			break
	var kept := []
	for row in after["entries"]:
		row["elapsed"]+=1
		if row["busy"]==0:row["busy_elapsed"]=0
		elif row["busy"]==1:
			row["busy_elapsed"]+=1
			if row["busy_elapsed"]>=row["duration"]:row["busy"]=0
		if row["limit"]<0 or row["elapsed"]<row["limit"]:kept.append(row)
	after["entries"]=kept
	return after


static func available(ledger: Dictionary) -> Array:
	var result := []
	for row in ledger["entries"]:
		if row["busy"]!=0:continue
		result.append({"id":row["id"],"category":row["metadata"][2],"remaining":row["limit"]-row["elapsed"] if row["limit"]>0 else row["limit"],"cooldown":row["duration"]})
	return result


## A departure ledger can be reconstructed from the legal earlier submissions.
static func valid_opening(ledger: Dictionary, week: int, month := 5) -> bool:
	if not ((month in [5,6,7] and week in range(1,6)) or (month==8 and week in range(1,6))): return false
	var last := (month-5)*5+week
	var source := rules()
	var first := initial()
	if source.is_empty() or first.is_empty(): return false
	var candidates := [first]
	for date in range(2,last+1):
		var next := []
		for candidate in candidates:
			var previous := date-2
			var required := _mandatory_id(5+int(previous/5),previous%5+1)
			var selections := [] if required else [0]
			for row in available(candidate):
				if not required or row["id"]==required: selections.append(row["id"])
			for id in selections:
				var advanced := advance(candidate,id)
				_open(advanced,5+int((date-1)/5),(date-1)%5+1,source)
				if not next.has(advanced): next.append(advanced)
		candidates = next
	return candidates.has(ledger)


static func _mandatory_id(month: int, week: int) -> int:
	match month:
		5:return 7 if week==4 else 0
		6:return {1:4,2:6,3:10,4:13}.get(week,0)
		7:return {3:9,4:14}.get(week,0)
		8:return {2:20,3:21}.get(week,0)
	return 0


static func select(bundle: Dictionary, ledger: Dictionary, id: int) -> Dictionary:
	if not _valid_bundle(bundle):return _failure("outside_returned_school")
	if rules().is_empty():return _failure("adventure_sources_changed")
	var school: Dictionary=bundle["school"]
	var date := [school["month"],school["week"]]
	var mandatory := _mandatory_id(school["month"],school["week"])
	if id in [4,6,7,9,10,13,14,20,21] and (school["adventure_gate"]!=1 or id!=mandatory):
		return _failure("adventure_not_available")
	if bundle["school"]["adventure_gate"] != 0 and id != mandatory:
		return _failure("mandatory_adventure_required")
	if (id==18 and date!=[7,1]) or (id==35 and date!=[8,5]):return _failure("adventure_not_available")
	if id not in [4,6,7,8,9,10,13,14,17,18,20,21,35] or available(ledger).filter(func(r):return r["id"]==id).is_empty():return _failure("adventure_not_available")
	var row: Dictionary=ledger["entries"].filter(func(r):return r["id"]==id)[0]
	var index := available(ledger).filter(func(r):return r["category"]==row["metadata"][2]).find(available(ledger).filter(func(r):return r["id"]==id)[0])
	var after := bundle.duplicate(true)
	after["school"]["lecture_active"]=1
	after["school"]["lecture_work_fields"]=[row["metadata"][0],row["metadata"][1],id,index]
	return {"supported":true,"after":after}


static func prepare(bundle: Dictionary, ledger: Dictionary) -> Dictionary:
	if not _valid_bundle(bundle):return _failure("outside_returned_school")
	var source := rules()
	if source.is_empty():return _failure("adventure_sources_changed")
	var school: Dictionary=bundle["school"]
	var id: int=school["lecture_work_fields"][2]
	var june: bool=school["month"]==6
	var july: bool=school["month"]==7 and school["week"] in range(1,6)
	var required := _mandatory_id(school["month"],school["week"])
	if (june and required==0 and school["week"]!=5) or (school["month"] not in [5,6] and not july and [school.month,school.week] not in [[8,2],[8,3],[8,4]]):return _failure("outside_supported_sortie_week")
	if (required and (id!=required or school["adventure_gate"]!=1)) or (id==7 and required!=7):
		return _failure("mandatory_adventure_required")
	var options := [required] if required else ([17,18] if july and school["week"]==1 else [17] if july or june or school.month==8 else [8,17])
	if school["lecture_active"]!=1 or id not in options or available(ledger).filter(func(r):return r["id"]==id).is_empty():return _failure("select_available_adventure")
	var rated := Groups.rate(school,Return.group_rules(school))
	if not rated["supported"]:return rated
	var teachers := [];var students := [];var groups := []
	for group in range(5):
		var state: int=rated["ratings"][group]["state"]
		if state not in [0,2,4]:return _failure("incomplete_class")
		if state!=2:continue
		teachers.append(Groups._word(school["group_raw_bytes"],group*28))
		for slot in range(4):
			var student := Groups._word(school["group_raw_bytes"],group*28+16+slot*2)
			if student<0:continue
			# Student 13 can attend class, but her field animations are not in the scene 17 catalog.
			if school.month==8 and school.week==4 and student==13:return _failure("unsupported_training_student_13")
			students.append(student);groups.append(group)
	if students.is_empty():return _failure("no_adventure_class")
	var specs: Array=source["adventures"][id-1]["rounds"]
	if specs!=[{"scene_id":id,"selection_word":1}]:return _failure("unsupported_round_selection")
	var scenes: Dictionary=source["scenes"]
	if required or id==18:
		var mission := eighteen_rules() if id==18 else mandatory_rules(id)
		if mission.is_empty():return _failure("adventure_sources_changed")
		scenes={str(id):mission["scene"]}
	var round_data := {"scene_id":id,"teacher_ids":teachers,"student_ids":students,"student_groups":groups}
	return {"supported":true,"ready":true,"prepared":{"adventure_id":id,"round_index":0,"round_count":1,
		"class_ratings":rated["ratings"],"rounds":[round_data]},"scene":scenes[str(id)].duplicate(true),
		"growth":bundle["growth"].filter(func(r):return students.has(r["character_id"])).duplicate(true),
		"participants":bundle["participants"].filter(func(r):return students.has(r["character_id"])).duplicate(true),
		"idle_student_ids":school["idle_student_ids"].duplicate(),"battle_executed":false}


static func submit(bundle: Dictionary, ledger: Dictionary) -> Dictionary:
	if bundle.get("school") is Dictionary and (bundle["school"].get("week") in [3,4,5] or bundle["school"].get("month") in [6,7,8]) and not valid_opening(ledger,bundle["school"]["week"],bundle["school"]["month"]):
		return _failure("sortie_opening_ledger_mismatch")
	var ready := prepare(bundle,ledger)
	if not ready["supported"]:return ready
	if bundle["school"]["week"] not in [1,2,3,4,5]:return _failure("outside_supported_sortie_week")
	var after := bundle.duplicate(true);after["phase"]="sortie_committed"
	var handoff := ready.duplicate(true)
	handoff["requested_states"]=[10,16];handoff["round_cursor"]=1
	handoff["scene_playable"]=false;handoff["combat_units_constructed"]=false
	handoff["date"]=[bundle["school"]["month"],bundle["school"]["week"]]
	return {"supported":true,"after":after,"ledger_after":advance(ledger,ready["prepared"]["adventure_id"]),"handoff":handoff}


static func _valid_bundle(bundle: Dictionary) -> bool:
	var source := Return._rules()
	return not source.is_empty() and bundle.get("phase")=="school_returned" and Return.validate_planning_roster(bundle,source).is_empty()


static func _failure(reason: String) -> Dictionary:
	return {"supported":false,"reason":reason}
