extends SceneTree
## Compare pagewise and skipped returns using a reproduced settlement and opening ledger.
const Flow := preload("res://sim/school_postbattle_flow.gd")


var observations := {}


func _init() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() not in [2,3]:
		printerr("Expected settlement (before/after) and departure school snapshot paths")
		quit(1)
		return
	var settled: Dictionary=Flow.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(args[0])))
	var school: Dictionary=Flow.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(args[1])))
	var skip := _return(settled.after,school.planning.ledger,true)
	var pages := _return(settled.after,school.planning.ledger,false)
	if pages.is_empty() or pages!=skip:
		printerr("November 4 return disagrees")
		quit(1)
		return
	var equipment_case: Dictionary=settled.after.duplicate(true)
	equipment_case.chapter071_absent.participants.equipped_items=[6,7,0,0,0,0,0,0]
	equipment_case.item_flags[5]=0xa105
	equipment_case.item_flags[6]=0x7600
	var equipped := Flow.SortieWeek.join_november(equipment_case,72)
	if not equipped.supported or equipped.after.participants[-1].equipped_items.slice(0,2)!=[0,7] or equipped.after.item_flags.slice(5,7)!=[0xa105,0x7305]:
		quit(1)
		return
	_observe("equipment",equipped.after,2)
	if args.size()==3:
		var file := FileAccess.open(args[2],FileAccess.WRITE)
		if file==null:
			quit(1)
			return
		file.store_string(JSON.stringify(observations))
	print("Chapter072/074/307/312 page and skip paths agree, including backtracking and roster effects.")
	quit(0)


func _return(settled: Dictionary, ledger: Dictionary, skip: bool) -> Dictionary:
	var flow := Flow.new()
	flow.bundle=settled.duplicate(true)
	flow.phase="sortie_result"
	flow.planning={"sortie_summary":{"scene_id":41},"opening_ledger":ledger,"ledger":Flow.Adventures.advance(ledger,41)}
	var story := Flow.SortieWeek.story(3,11)
	if not story.supported:return {}
	flow._set_dated_story(story)
	if not flow.execute({"op":"post_next"}).supported:return {}
	var absent: Dictionary=settled.chapter071_absent
	var rejoined: Dictionary=flow.bundle.participants[-1]
	if flow.bundle.school.student_count!=16 or flow.bundle.school.student_ids[15]!=2 or flow.bundle.records[-1]!=absent.records or flow.bundle.counts[-1]!=absent.counts:return {}
	for key in ["job_progress","attributes","growth_pools","job_sums","staged_total"]:
		if rejoined[key]!=absent.participants[key]:return {}
	_observe("72",flow.bundle,2)
	for row in absent.relationships:
		if not flow.bundle.school.relationships.has(row):return {}
	if not skip:
		for i in range(story.pre_week_join_page):
			if not flow.execute({"op":"post_next"}).supported:return {}
			var linked: bool=i==story.pre_week_join_page-1
			if flow.bundle.school.student_count!=(17 if linked else 16):return {}
		_observe("74",flow.bundle,7)
		var weekly:=Flow.Return.Week.project(Flow.Return._week_input(flow.bundle),Flow.Return._rules().week)
		if not weekly.supported:return {}
		observations["before307_items"]=weekly.after.item_flags
		if flow.pages[flow.cursor].chapter!=74 or flow.bundle.school.student_ids[16]!=7:return {}
		for op in ["post_prev","post_next"]:
			if not flow.execute({"op":op}).supported or flow.bundle.school.student_count!=17:return {}
	if not _finish_pages(flow,skip):return {}
	if flow.phase!="new_week_story" or flow._date_card.is_empty() or flow.bundle.school.student_count!=18 or flow.bundle.school.teacher_count!=6:return {}
	_observe("307",flow.bundle,28)
	if not flow.execute({"op":"post_next"}).supported or flow.pages[flow.cursor].chapter!=307:return {}
	if not _finish_pages(flow,skip) or flow.phase!="post_workroom":return {}
	if [flow.bundle.flags["0x7a55f6"],flow.bundle.flags["0x7e11a0"],flow.bundle.adv_background]!=[5,1,122]:return {}
	if not flow.execute({"op":"post_school"}).supported or flow.pages[flow.cursor].chapter!=312:return {}
	if not _finish_pages(flow,skip) or flow.phase!="returned_school":return {}
	var school: Dictionary=flow.bundle.school
	if flow.planning.ledger.unlock_flags[40]!=1 or Flow.Adventures.available(flow.planning.ledger).any(func(row):return row.id==41):return {}
	if school.student_ids.slice(0,18)!=[3,4,9,5,8,6,1,16,17,13,14,15,11,18,32,2,7,28] or school.teacher_ids.slice(0,6)!=[101,110,115,118,116,107]:return {}
	if [school.month,school.week,flow.bundle.flags["0x7a55f6"],flow.bundle.flags["0x7e11a0"]]!=[11,4,11,0]:return {}
	if not Flow.Return.validate_planning_roster(flow.bundle,Flow.Return._rules()).is_empty():return {}
	for cmd in [{"kind":"teacher","member_id":107,"target_group":0},{"kind":"student","member_id":28,"target_group":0,"target_slot":0},{"kind":"student","member_id":7,"target_group":0,"target_slot":1}]:
		cmd.op="return_move"
		var moved:=flow.execute(cmd)
		if not moved.supported:
			printerr(cmd,moved)
			return {}
	if flow.bundle.school.derived_teacher_ids[0]!=107 or flow.bundle.school.derived_student_ids[0].slice(0,2)!=[28,7]:return {}
	return {"bundle":flow.bundle,"ledger":flow.planning.ledger}


func _finish_pages(flow: RefCounted, skip: bool) -> bool:
	var initial: String=flow.phase
	for i in range(flow.pages.size()+1):
		if not flow.execute({"op":"post_skip" if skip else "post_next"}).supported:return false
		if flow.phase!=initial:return true
	return false


func _observe(stage: String, bundle: Dictionary, id: int) -> void:
	observations[stage]={"participant":Flow.Return._find(bundle.participants,id),
		"history":Flow.Return._find(bundle.records,id),"item_flags":bundle.item_flags,
		"students":bundle.school.student_ids.slice(0,bundle.school.student_count),
		"teachers":bundle.school.teacher_ids.slice(0,bundle.school.teacher_count)}
