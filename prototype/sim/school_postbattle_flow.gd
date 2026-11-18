extends RefCounted
const Return := preload("res://sim/school_postbattle_return.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const Adventures := preload("res://sim/school_return_adventures.gd")
const Courses := preload("res://sim/school_return_courses.gd")
const SortieRecord := preload("res://sim/school_sortie_record.gd")
const SortieSettlement := preload("res://sim/school_sortie_settlement.gd")
const SortieWeek := preload("res://sim/school_sortie_week.gd")
const PLAN_OPS := ["return_plan","return_mode","return_course","return_select","return_settle","return_depart"]
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
var planning: Dictionary = {}


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


func finish_sortie(trace: Dictionary) -> Dictionary:
	if phase!="sortie_pending": return _failure("sortie_not_pending")
	var replayed := SortieRecord.replay(planning["handoff"],trace)
	if not replayed["supported"]: return replayed
	var settled := SortieSettlement.apply(bundle,planning["handoff"],replayed["facts"])
	if not settled["supported"]: return settled
	var story := SortieWeek.story()
	if not story["supported"]: return story
	bundle=settled["after"]
	planning.erase("handoff")
	planning["sortie_summary"]=settled["summary"]
	_set_may_story(story)
	phase="sortie_result"
	revision+=1
	return {"supported":true}


func _set_may_story(story: Dictionary) -> void:
	_post_pages=story["pre_week"]
	_week_pages=story["week_start"]
	pages=_post_pages
	cursor=0


func course_continued() -> bool:
	return planning.has("course_summary") and phase!="course_result"


func execute(command: Dictionary) -> Dictionary:
	var op: String = command["op"]
	if op=="course_story":
		if phase!="course_result" or bundle.get("phase")!="courses_confirmed":
			return _failure("course_not_confirmed")
		var story := SortieWeek.story()
		if not story["supported"]: return story
		_set_may_story(story)
		phase="post_story"
		revision+=1
		return {"supported":true}
	if op=="sortie_finish": return finish_sortie(command["trace"])
	if phase=="sortie_result" and op=="post_next":
		phase="post_story"
		revision+=1
		return {"supported":true}
	if op in PLAN_OPS:return _plan(command)
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
		var returned := SortieWeek.school_return(bundle,planning["ledger"]) if planning.has("sortie_summary") or course_continued() else Return.school_return(bundle)
		if not returned["supported"]: return returned
		if returned.has("ledger_after"): planning["ledger"]=returned["ledger_after"]
		bundle=returned["after"];phase="returned_school";revision+=1;return {"supported":true}
	if op not in ["post_next","post_prev","post_skip"] or phase not in ["post_story","new_week_story"]:
		return _failure("postbattle_story_not_active")
	if op=="post_prev":
		if cursor==0: return {"supported":true,"status":"duplicate"}
		cursor-=1;revision+=1;return {"supported":true}
	var next := pages.size() if op=="post_skip" else cursor+1
	if next==pages.size():
		if phase=="post_story":
			var week := SortieWeek.next_week(bundle) if planning.has("sortie_summary") or course_continued() else Return.next_week(bundle)
			if not week["supported"]: return week
			bundle=week["after"];pages=_week_pages;phase="new_week_story";cursor=0
		else:
			if planning.has("sortie_summary") or course_continued():
				var finished := SortieWeek.finish_story(bundle)
				if not finished["supported"]: return finished
				bundle=finished["after"]
			else:
				# Chapter208 op151 [9,1], op91 [8,2], then END to workroom8.
				bundle["flags"]["0x7a55f6"]=9;bundle["flags"]["0x7e11a0"]=1
				bundle["adv_background"]=8
			phase="post_workroom";cursor=next
	else: cursor=next
	revision+=1
	return {"supported":true}


func snapshot() -> Dictionary:
	var result := {"phase":phase,"cursor":cursor,"total":pages.size(),"bundle":bundle.duplicate(true),
		"page":pages[cursor].duplicate(true) if phase in ["post_story","new_week_story"] else {},
		"result_summary":result_summary.duplicate(true),"revision":revision}
	# Older v5 snapshots retain their exact shape until an explicit new command.
	if not planning.is_empty():result["planning"]=planning.duplicate(true)
	return result


func _plan(command: Dictionary) -> Dictionary:
	if phase!="returned_school":return _failure("return_plan_already_committed")
	var op: String=command["op"]
	if op=="return_plan":
		if not planning.is_empty():return {"supported":true,"status":"duplicate"}
		var ledger := Adventures.initial()
		if ledger.is_empty():return _failure("adventure_sources_changed")
		planning={"ledger":ledger,"adventure_catalog_complete":true};revision+=1
		return {"supported":true}
	if planning.is_empty():return _failure("return_plan_not_open")
	var result: Dictionary
	match op:
		"return_mode":result=Courses.set_mode(bundle,command["group"],command["teaching"])
		"return_course":result=Courses.assign_course(bundle,command["group"],command["course"])
		"return_select":result=Adventures.select(bundle,planning["ledger"],command["adventure"])
		"return_settle":result=Courses.settle(bundle)
		"return_depart":result=Adventures.submit(bundle,planning["ledger"])
	if not result["supported"]:return result
	if result["after"]==bundle:return {"supported":true,"status":"duplicate"}
	bundle=result["after"]
	if op=="return_settle":
		planning["ledger"]=Adventures.advance(planning["ledger"],0)
		planning["course_summary"]=result["summary"];phase="course_result"
	elif op=="return_depart":
		planning["ledger"]=result["ledger_after"]
		planning["handoff"]=result["handoff"];phase="sortie_pending"
	revision+=1
	return {"supported":true}


static func _failure(reason: String) -> Dictionary:
	return {"supported":false,"reason":reason}
