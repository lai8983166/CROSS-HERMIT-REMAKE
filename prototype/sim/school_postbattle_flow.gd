extends RefCounted
const Return := preload("res://sim/school_postbattle_return.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const STORY_PATH := "res://data/school_postbattle_story.json"
const STORY_SHA := "7810a795b702e90cd439e3916e03ecaf824646c9f09db93c5ba6e1c7a5be1aaf"
var bundle: Dictionary = {}
var phase := "closed"
var cursor := 0
var pages: Array = []
var _post_pages: Array = []
var _week_pages: Array = []
var revision := 0
var result_summary: Dictionary = {}


func begin(context: Dictionary, receipt: Dictionary, participants: Array, flags: Dictionary) -> Dictionary:
	if phase!="closed": return _failure("postbattle_already_started")
	var raw := FileAccess.get_file_as_string(STORY_PATH).replace("\r\n","\n")
	if raw.sha256_text()!=STORY_SHA: return _failure("postbattle_story_changed")
	if receipt.get("successor")!="adv_ch003_pending" or not receipt.get("settlement") is Dictionary:
		return _failure("postbattle_requires_confirmed_result")
	var result: Dictionary = receipt["settlement"]
	if result.get("phase")!="adv_pending": return _failure("postbattle_requires_confirmed_result")
	var confirmed: Dictionary = result["confirmation"]
	var growth: Array = context["growth"].duplicate(true)
	for row in result["growth"]["after"]["characters"]:
		for i in range(growth.size()):
			if growth[i]["character_id"]==row["character_id"]: growth[i]=row.duplicate(true)
	var input := {"school":confirmed["after"].duplicate(true),"growth":growth,
		"records":confirmed["records"].duplicate(true),"counts":confirmed["counts"].duplicate(true),
		"item_flags":result["item_flags"].duplicate(),"participants":participants.duplicate(true),"flags":flags.duplicate(true)}
	var joined := Return.join(input)
	if not joined["supported"]: return joined
	var data: Dictionary = Roles._integers(JSON.parse_string(raw))
	for scene in data["scenes"]:
		if scene["chapter"] in [20,21]: _post_pages.append_array(scene["pages"])
		else: _week_pages.append_array(scene["pages"])
	bundle = joined["after"]; pages = _post_pages; phase = "post_story"; cursor=0; revision=1
	result_summary={"outcome":receipt["outcome"],"score":result["score"].duplicate(true),"recipient":result["recipient"]}
	return {"supported":true}


func execute(command: Dictionary) -> Dictionary:
	var op: String = command["op"]
	if op=="return_move":
		if phase!="returned_school": return _failure("school_not_returned")
		var request := command.duplicate(true); request.erase("op")
		var moved := Return.move_member(bundle,request)
		if not moved["supported"]: return moved
		if moved["after"]==bundle: return {"supported":true,"status":"duplicate"}
		bundle=moved["after"];revision+=1; return {"supported":true}
	if op=="post_school":
		if phase=="returned_school": return {"supported":true,"status":"duplicate"}
		if phase!="post_workroom": return _failure("workroom_not_reached")
		var returned := Return.school_return(bundle)
		if not returned["supported"]: return returned
		bundle=returned["after"];phase="returned_school";revision+=1;return {"supported":true}
	if op not in ["post_next","post_prev","post_skip"] or phase not in ["post_story","new_week_story"]:
		return _failure("postbattle_story_not_active")
	if op=="post_prev":
		if cursor==0: return {"supported":true,"status":"duplicate"}
		cursor-=1;revision+=1;return {"supported":true}
	var next := pages.size() if op=="post_skip" else cursor+1
	if next==pages.size():
		if phase=="post_story":
			var week := Return.next_week(bundle)
			if not week["supported"]: return week
			bundle=week["after"];pages=_week_pages;phase="new_week_story";cursor=0
		else:
			# Chapter208 op151 [9,1], op91 [8,2], then END to workroom8.
			bundle["flags"]["0x7a55f6"]=9;bundle["flags"]["0x7e11a0"]=1
			bundle["adv_background"]=8
			phase="post_workroom";cursor=next
	else: cursor=next
	revision+=1
	return {"supported":true}


func snapshot() -> Dictionary:
	return {"phase":phase,"cursor":cursor,"total":pages.size(),"bundle":bundle.duplicate(true),
		"page":pages[cursor].duplicate(true) if phase in ["post_story","new_week_story"] else {},
		"result_summary":result_summary.duplicate(true),"revision":revision}


static func _failure(reason: String) -> Dictionary:
	return {"supported":false,"reason":reason}
