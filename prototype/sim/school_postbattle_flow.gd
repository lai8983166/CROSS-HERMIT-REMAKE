extends RefCounted
const Return := preload("res://sim/school_postbattle_return.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const Adventures := preload("res://sim/school_return_adventures.gd")
const Courses := preload("res://sim/school_return_courses.gd")
const SortieRecord := preload("res://sim/school_sortie_record.gd")
const SortieSettlement := preload("res://sim/school_sortie_settlement.gd")
const SortieWeek := preload("res://sim/school_sortie_week.gd")
const JobEligibility := preload("res://sim/school_job_eligibility.gd")
const PLAN_OPS := ["return_plan","return_job","return_mode","return_course","return_select","return_settle","return_depart"]
const STORY_PATH := "res://data/school_postbattle_story.json"
const STORY_SHA := "7810a795b702e90cd439e3916e03ecaf824646c9f09db93c5ba6e1c7a5be1aaf"
var bundle: Dictionary = {}
var phase := "closed"
var cursor := 0
var pages: Array = []
var _post_pages: Array = []
var _week_pages: Array = []
var _date_card: Dictionary = {}
var _school_pages: Array = []
var _pre_week_join_page := -1
var _choice_labels: Array = []
var _choice_pages: Array = []
var _choice := -1
var revision := 0
var result_summary: Dictionary = {}
var planning: Dictionary = {}
# Rebuilt from each confirmed battle during command replay.
var _task_grades: Dictionary = {}


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
	var settled := SortieSettlement.apply(bundle,planning["handoff"],replayed["facts"],planning.get("opening_ledger",{}),_task_grades)
	if not settled["supported"]: return settled
	var story := SortieWeek.story(bundle["school"]["week"],bundle["school"]["month"])
	if not story["supported"]: return story
	bundle=settled["after"]
	planning.erase("handoff")
	planning["sortie_summary"]=settled["summary"]
	_task_grades[settled["summary"]["scene_id"]]=settled["summary"]["task_grade"]
	_set_dated_story(story)
	phase="sortie_result"
	revision+=1
	return {"supported":true}


func _set_dated_story(story: Dictionary) -> void:
	_pre_week_join_page=story.get("pre_week_join_page",-1)
	_choice_labels=story.get("choice_labels",[])
	_choice_pages=story.get("choice_pages",[])
	_choice=-1
	_post_pages=story["pre_week"]
	_week_pages=story["week_start"]
	_date_card=story.get("date_card",{})
	_school_pages=story.get("school_entry",[])
	pages=_post_pages
	cursor=0


func course_continued() -> bool:
	return planning.has("course_summary") and phase!="course_result"


func execute(command: Dictionary) -> Dictionary:
	var op: String = command["op"]
	if op=="post_choice":
		if phase!="chapter309_choice" or typeof(command.get("choice"))!=TYPE_INT or command.choice not in [0,1]:
			return _failure("invalid_chapter309_choice")
		_choice=command.choice
		pages=_choice_pages[_choice]
		cursor=0
		phase="post_story"
		revision+=1
		return {"supported":true}
	if op=="course_story":
		if phase!="course_result" or bundle.get("phase")!="courses_confirmed":
			return _failure("course_not_confirmed")
		var story := SortieWeek.story(bundle["school"]["week"],bundle["school"]["month"])
		if not story["supported"]: return story
		if [bundle.school.month,bundle.school.week]==[9,5]:
			var joined := SortieWeek.join_october_student(bundle,313)
			if not joined.supported:return joined
			bundle=joined.after
		_set_dated_story(story)
		if _post_pages.is_empty():return _advance_work_week()
		phase="post_story"
		revision+=1
		return {"supported":true}
	if op=="sortie_finish": return finish_sortie(command["trace"])
	if phase=="sortie_result" and op=="post_next":
		if pages.is_empty():
			return _advance_work_week()
		if [bundle.school.month,bundle.school.week]==[11,3]:
			var joined := SortieWeek.join_november(bundle,72)
			if not joined.supported:return joined
			bundle=joined.after
		if bundle.school.week==4 and bundle.school.month in [5,6,7,9]:
			var started := SortieWeek.begin_story(bundle)
			if not started["supported"]:return started
			bundle=started["after"]
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
		if _school_pages.is_empty(): return _return_to_school()
		if [bundle.school.month,bundle.school.week] in [[8,4],[9,5]]:
			var joined := SortieWeek.begin_school_entry(bundle)
			if not joined.supported:return joined
			bundle=joined.after
		pages=_school_pages;cursor=0;phase="school_entry_story";revision+=1
		return {"supported":true}
	if op not in ["post_next","post_prev","post_skip"] or phase not in ["post_story","new_week_story","school_entry_story"]:
		return _failure("postbattle_story_not_active")
	if phase=="new_week_story" and not _date_card.is_empty() and not _week_pages.is_empty() and op=="post_next":
		_date_card={}
		pages=_week_pages
		cursor=0
		revision+=1
		return {"supported":true}
	if op=="post_prev":
		if cursor==0: return {"supported":true,"status":"duplicate"}
		cursor-=1;revision+=1;return {"supported":true}
	var next := pages.size() if op=="post_skip" or pages.is_empty() else cursor+1
	if phase=="post_story" and bundle.phase=="chapter072_joined" and next>=_pre_week_join_page:
		var joined := SortieWeek.join_november(bundle,74)
		if not joined.supported:return joined
		bundle=joined.after
	if phase=="post_story" and _pre_week_join_page>=0 and next>=_pre_week_join_page and bundle["phase"]=="sortie_settled":
		var joined := SortieWeek.begin_story(bundle)
		if not joined["supported"]:return joined
		bundle=joined["after"]
	if phase=="new_week_story" and [bundle.school.month,bundle.school.week]==[10,1] and bundle.school.student_count==15 and (next==pages.size() or int(pages[next].chapter)==233):
		var joined := SortieWeek.join_october_student(bundle,233)
		if not joined.supported:return joined
		bundle=joined.after
	if phase=="post_story" and not _choice_labels.is_empty() and _choice==-1 and next>=pages.size()-1:
		cursor=pages.size()-1
		phase="chapter309_choice"
		revision+=1
		return {"supported":true}
	if next==pages.size():
		if phase=="post_story" and not _choice_labels.is_empty():
			var joined := SortieWeek.join_chapter309(bundle,_choice)
			if not joined.supported:return joined
			var advanced := SortieWeek.next_week(joined.after)
			if not advanced.supported:return advanced
			bundle=advanced.after
			pages=[]
			cursor=0
			phase="new_week_story"
			revision+=1
			return {"supported":true}
		if phase=="school_entry_story": return _return_to_school()
		if phase=="post_story":
			var week := SortieWeek.next_week(bundle) if planning.has("sortie_summary") or course_continued() else Return.next_week(bundle)
			if not week["supported"]: return week
			bundle=week["after"];pages=_week_pages if _date_card.is_empty() else [];phase="new_week_story";cursor=0
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


func _advance_work_week() -> Dictionary:
	var advanced := SortieWeek.next_week(bundle)
	if not advanced["supported"]:return advanced
	bundle=advanced["after"];pages=_week_pages if _date_card.is_empty() else [];phase="new_week_story";cursor=0
	revision+=1
	return {"supported":true}


func _return_to_school() -> Dictionary:
	var returned := SortieWeek.school_return(bundle,planning["ledger"],planning.get("opening_ledger",{})) if planning.has("sortie_summary") or course_continued() else Return.school_return(bundle)
	if not returned["supported"]: return returned
	if returned.has("ledger_after"): planning["ledger"]=returned["ledger_after"]
	if phase=="school_entry_story": cursor=pages.size()
	bundle=returned["after"];phase="returned_school";revision+=1
	return {"supported":true}


func snapshot() -> Dictionary:
	var result := {"phase":phase,"cursor":cursor,"total":pages.size(),"bundle":bundle.duplicate(true),
		"page":pages[cursor].duplicate(true) if not pages.is_empty() and phase in ["post_story","new_week_story","school_entry_story","chapter309_choice"] else {},
		"result_summary":result_summary.duplicate(true),"revision":revision}
	if phase=="new_week_story" and not _date_card.is_empty():
		result["date_card"]=_date_card.duplicate(true)
		if not _week_pages.is_empty():result["story_after_card"]=true
	if phase=="chapter309_choice":result["choice_labels"]=_choice_labels.duplicate()
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
		"return_job":result=JobEligibility.change_job(bundle,command["member"],command["job"])
		"return_mode":result=Courses.set_mode(bundle,command["group"],command["teaching"])
		"return_course":result=Courses.assign_course(bundle,command["group"],command["course"])
		"return_select":result=Adventures.select(bundle,planning["ledger"],command["adventure"])
		"return_settle":result=Courses.settle(bundle)
		"return_depart":result=Adventures.submit(bundle,planning["ledger"])
	if not result["supported"]:return result
	if result["after"]==bundle:return {"supported":true,"status":"duplicate"}
	if (bundle["school"]["week"] in [2,3,4,5] or bundle["school"]["month"] in [6,7,8,9,10,11,12]) and op in ["return_settle","return_depart"]:
		# Replace last week's display summary only when the new work is committed.
		# Keep its starting ledger for validating the battle and next school's entry.
		var opening: Dictionary=planning["ledger"]
		planning={"opening_ledger":opening,"ledger":opening,"adventure_catalog_complete":true}
		if bundle["school"]["month"] in [6,7,8,9,10,11,12]:
			planning["committed_date"]=[bundle["school"]["month"],bundle["school"]["week"]]
		elif bundle["school"]["week"]>=3:
			planning["committed_week"]=bundle["school"]["week"]
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
