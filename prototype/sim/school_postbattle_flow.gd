extends RefCounted
const Return := preload("res://sim/school_postbattle_return.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const Adventures := preload("res://sim/school_return_adventures.gd")
const Courses := preload("res://sim/school_return_courses.gd")
const SortieRecord := preload("res://sim/school_sortie_record.gd")
const SortieSettlement := preload("res://sim/school_sortie_settlement.gd")
const SortieWeek := preload("res://sim/school_sortie_week.gd")
const JobEligibility := preload("res://sim/school_job_eligibility.gd")
const PersonalSkills := preload("res://sim/school_personal_skills.gd")
const PLAN_OPS := ["return_plan","return_job","return_skill","return_mode","return_course","return_select","return_settle","return_depart"]
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
var _winter_story := {}
var _winter_choices := []
var _winter_applied := [0,0,0]
var revision := 0
var result_summary: Dictionary = {}
var planning: Dictionary = {}
# Rebuilt from each confirmed battle during command replay.
var _task_grades: Dictionary = {}
# An independent command replay can inspect the exact operands of a week call.
var week_observer := Callable()


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
	return _settle_replayed_sortie(replayed.facts)


func _settle_replayed_sortie(facts: Dictionary) -> Dictionary:
	if phase!="sortie_pending":return _failure("sortie_not_pending")
	var settled := SortieSettlement.apply(bundle,planning["handoff"],facts,planning.get("opening_ledger",{}),_task_grades)
	if not settled["supported"]: return settled
	var story := SortieWeek.story(bundle["school"]["week"],bundle["school"]["month"],_task_grades)
	if not story["supported"]: return story
	if [bundle.school.month,bundle.school.week]==[9,5]:
		var joined := SortieWeek.join_october_student(settled.after,313)
		if not joined.supported:return joined
		settled.after=joined.after
	if story.get("terminal",false):
		var advanced := SortieWeek.next_week(settled.after,week_observer)
		if not advanced.supported:return advanced
		bundle=advanced.after
	else:bundle=settled.after
	planning.erase("handoff")
	planning["sortie_summary"]=settled["summary"]
	_task_grades[settled["summary"]["scene_id"]]=settled["summary"]["task_grade"]
	_set_dated_story(story)
	phase="sortie_result"
	revision+=1
	return {"supported":true}


func _set_dated_story(story: Dictionary) -> void:
	_winter_story=story if story.get("winter",false) else {}
	_winter_choices=[]
	_winter_applied=[0,0,0]
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


func _winter_roster_through(section: int, next_page: int) -> Dictionary:
	if _winter_story.is_empty():return {"supported":true}
	var steps: Array=_winter_story.roster_steps[section]
	var end: int=_winter_applied[section]
	var pending := []
	while end<steps.size() and steps[end].page<=next_page:
		pending.append(steps[end].effect)
		end+=1
	if not pending.is_empty():
		var applied := SortieWeek.winter_effects(bundle,pending)
		if not applied.supported:return applied
		bundle=applied.after
		_winter_applied[section]=end
	return {"supported":true}


func course_continued() -> bool:
	return planning.has("course_summary") and phase!="course_result"


func execute(command: Dictionary) -> Dictionary:
	var op: String = command["op"]
	if bundle.get("school",{}).get("month",0)>=10 and not SortieWeek.YearLoop.accepts(phase,op):
		if phase=="returned_school" and op=="post_school":return {"supported":true,"status":"duplicate"}
		return _failure("invalid_school_year_phase_command")
	if op=="post_choice":
		if phase=="chapter310_choice":
			if typeof(command.get("choice"))!=TYPE_INT or command.choice<0 or command.choice>=_choice_labels.size():return _failure("invalid_chapter310_choice")
			_winter_choices.append(command.choice)
			var branch := SortieWeek.story(bundle.school.week,bundle.school.month,_task_grades,_winter_choices)
			if not branch.supported:return branch
			_winter_story=branch
			_choice_labels=branch.choice_labels
			pages=branch.pre_week
			var applied := _winter_roster_through(0,0)
			if not applied.supported:return applied
			cursor=0
			phase="post_story"
			revision+=1
			return {"supported":true}
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
		var story := SortieWeek.story(bundle["school"]["week"],bundle["school"]["month"],_task_grades)
		if not story["supported"]: return story
		if [bundle.school.month,bundle.school.week]==[9,5]:
			var joined := SortieWeek.join_october_student(bundle,313)
			if not joined.supported:return joined
			bundle=joined.after
		_set_dated_story(story)
		var applied := _winter_roster_through(0,0)
		if not applied.supported:return applied
		if _post_pages.is_empty():return _advance_work_week()
		phase="post_story"
		revision+=1
		return {"supported":true}
	if op=="sortie_finish": return finish_sortie(command["trace"])
	if phase=="sortie_result" and op=="post_next":
		var applied := _winter_roster_through(0,0)
		if not applied.supported:return applied
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
	if not _winter_story.is_empty():
		var section := 0 if phase=="post_story" else 1 if phase=="new_week_story" else 2
		var through := _week_pages.size() if phase=="new_week_story" and op=="post_skip" else next
		var applied := _winter_roster_through(section,through)
		if not applied.supported:return applied
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
		phase="chapter310_choice" if not _winter_story.is_empty() else "chapter309_choice"
		revision+=1
		return {"supported":true}
	if next==pages.size():
		if phase=="post_story" and not _winter_story.is_empty():return _advance_work_week()
		if phase=="post_story" and not _choice_labels.is_empty():
			var joined := SortieWeek.join_chapter309(bundle,_choice)
			if not joined.supported:return joined
			var advanced := SortieWeek.next_week(joined.after,week_observer)
			if not advanced.supported:return advanced
			bundle=advanced.after
			pages=[]
			cursor=0
			phase="new_week_story"
			revision+=1
			return {"supported":true}
		if phase=="school_entry_story": return _return_to_school()
		if phase=="post_story":
			var week := SortieWeek.next_week(bundle,week_observer) if planning.has("sortie_summary") or course_continued() else Return.next_week(bundle)
			if not week["supported"]: return week
			bundle=week["after"];pages=_week_pages if _date_card.is_empty() else [];phase="new_week_story";cursor=0
		else:
			if planning.has("sortie_summary") or course_continued():
				var finished := SortieWeek.finish_story(bundle,_winter_story.effects[1] if not _winter_story.is_empty() else null)
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
	var starting := bundle
	if not _winter_story.is_empty():
		if _winter_story.terminal:
			phase="school_year_complete"
			cursor=pages.size()
			revision+=1
			return {"supported":true}
		var effects := SortieWeek.winter_effects(starting,_winter_story.effects[0].filter(func(e):return e.opcode in [91,151]))
		if not effects.supported:return effects
		starting=effects.after
	var advanced := SortieWeek.next_week(starting,week_observer)
	if not advanced["supported"]:return advanced
	bundle=advanced.after
	var applied := _winter_roster_through(1,0)
	if not applied.supported:return applied
	pages=_week_pages if _date_card.is_empty() else [];phase="new_week_story";cursor=0
	revision+=1
	return {"supported":true}


func _return_to_school() -> Dictionary:
	var returned := SortieWeek.school_return(bundle,planning["ledger"],planning.get("opening_ledger",{}),_winter_story.effects[2] if not _winter_story.is_empty() else null) if planning.has("sortie_summary") or course_continued() else Return.school_return(bundle)
	if not returned["supported"]: return returned
	if returned.has("ledger_after"): planning["ledger"]=returned["ledger_after"]
	if phase=="school_entry_story": cursor=pages.size()
	bundle=returned["after"];phase="returned_school";revision+=1
	return {"supported":true}


func snapshot() -> Dictionary:
	var result := {"phase":phase,"cursor":cursor,"total":pages.size(),"bundle":bundle.duplicate(true),
		"page":pages[cursor].duplicate(true) if not pages.is_empty() and phase in ["post_story","new_week_story","school_entry_story","chapter309_choice","chapter310_choice"] else {},
		"result_summary":result_summary.duplicate(true),"revision":revision}
	if bundle.has("school") and (bundle.school.month>12 or bundle.school.month==12 and bundle.school.week>=3):
		result["week_phase"]=SortieWeek.YearLoop.phase_for(phase)
	if phase=="new_week_story" and not _date_card.is_empty():
		result["date_card"]=_date_card.duplicate(true)
		if not _week_pages.is_empty():result["story_after_card"]=true
	if phase in ["chapter309_choice","chapter310_choice"]:result["choice_labels"]=_choice_labels.duplicate()
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
		"return_skill":result=PersonalSkills.equip(bundle,command.member_id,command.skill,command.slot)
		"return_job":result=JobEligibility.change_job(bundle,command["member"],command["job"])
		"return_mode":result=Courses.set_mode(bundle,command["group"],command["teaching"])
		"return_course":result=Courses.assign_course(bundle,command["group"],command["course"])
		"return_select":result=Adventures.select(bundle,planning["ledger"],command["adventure"])
		"return_settle":result=Courses.settle(bundle)
		"return_depart":result=Adventures.submit(bundle,planning["ledger"])
	if not result["supported"]:return result
	if result["after"]==bundle:return {"supported":true,"status":"duplicate"}
	if (bundle["school"]["week"] in [2,3,4,5] or bundle["school"]["month"] in range(6,16)) and op in ["return_settle","return_depart"]:
		# Replace last week's display summary only when the new work is committed.
		# Keep its starting ledger for validating the battle and next school's entry.
		var opening: Dictionary=planning["ledger"]
		planning={"opening_ledger":opening,"ledger":opening,"adventure_catalog_complete":true}
		if bundle["school"]["month"] in range(6,16):
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
