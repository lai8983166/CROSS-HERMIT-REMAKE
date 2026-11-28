extends SceneTree
## Reuse one confirmed battle & departure ledger to compare both native Chapter309 choices.
const Flow := preload("res://sim/school_postbattle_flow.gd")


var observations := {}


func _init() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() not in [2,3]:
		printerr("Expected confirmed settlement and opening school paths")
		quit(1)
		return
	var settled: Dictionary=Flow.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(args[0])))
	var opening: Dictionary=Flow.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(args[1])))
	for choice in range(2):
		var skipped := _run(settled.after,opening.planning.ledger,choice,true)
		var pagewise := _run(settled.after,opening.planning.ledger,choice,false)
		if skipped.is_empty() or skipped!=pagewise:
			printerr("December return differs for choice ",choice)
			quit(1)
			return
	if args.size()==3:
		var file := FileAccess.open(args[2],FileAccess.WRITE)
		if file==null:
			quit(1)
			return
		file.store_string(JSON.stringify(observations))
		file.close()
	print("Chapter309 both choices verified, including skip, pagewise, once-only joins, date card, school and movement")
	quit(0)


func _run(settled: Dictionary, ledger: Dictionary, choice: int, skip: bool) -> Dictionary:
	var flow := Flow.new()
	flow.bundle=settled.duplicate(true)
	flow.phase="sortie_result"
	flow.planning={"sortie_summary":{"scene_id":31},"opening_ledger":ledger,"ledger":Flow.Adventures.advance(ledger,31)}
	if skip:
		var observed := Flow.SortieWeek.join_chapter309(settled,choice)
		if not observed.supported:return {}
		var joined: Dictionary=observed.after
		observations[str(choice)]={"participants":joined.participants.slice(17),"records":joined.records.slice(17),
			"items":joined.item_flags,"students":joined.school.raw_student_ids,"availability":joined.school.availability}
	var source := Flow.SortieWeek.story(1,12)
	if not source.supported:return {}
	flow._set_dated_story(source)
	if not _ok(flow,{"op":"post_next"}) or flow.pages.size()!=29:return {}
	if not _finish(flow,skip) or flow.phase!="chapter309_choice" or flow.bundle!=settled:return {}
	if flow.snapshot().page.text_indices!=[46] or flow.snapshot().choice_labels.size()!=2 or flow.execute({"op":"post_skip"}).supported or flow.execute({"op":"post_choice","choice":2}).supported:return {}
	if not _ok(flow,{"op":"post_choice","choice":choice}) or flow.pages.size()!=(26 if choice==0 else 42):return {}
	if flow.execute({"op":"post_choice","choice":1-choice}).supported:return {}
	if not _ok(flow,{"op":"post_next"}) or not _ok(flow,{"op":"post_prev"}) or not _finish(flow,skip):return {}
	var suffix := [20,21] if choice==0 else [19]
	var count: int=17+suffix.size()
	var school: Dictionary=flow.bundle.school
	if flow.phase!="new_week_story" or [school.month,school.week,school.student_count]!=[12,2,count] or school.student_ids.slice(17,count)!=suffix:return {}
	if not flow.snapshot().date_card.image.ends_with("tc1202.png") or flow.bundle.chapter076_absent!=settled.chapter076_absent:return {}
	if not _ok(flow,{"op":"post_next"}) or flow.phase!="post_workroom" or [flow.bundle.flags["0x7a55f6"],flow.bundle.flags["0x7e11a0"],flow.bundle.adv_background]!=[11,0,13]:return {}
	if not _ok(flow,{"op":"post_school"}) or flow.phase!="returned_school" or [flow.bundle.flags["0x7a55f6"],flow.bundle.flags["0x7e11a0"],flow.bundle.adv_background]!=[11,1,13]:return {}
	if flow.bundle.school.adventure_gate!=0 or not Flow.Return.validate_planning_roster(flow.bundle,Flow.Return._rules()).is_empty():return {}
	for i in range(suffix.size()):
		if not _ok(flow,{"op":"return_move","kind":"student","member_id":suffix[i],"target_group":0,"target_slot":i}):return {}
	if flow.bundle.school.derived_student_ids[0].slice(0,suffix.size())!=suffix:return {}
	return {"school":flow.bundle,"ledger":flow.planning.ledger}


func _finish(flow: RefCounted, skip: bool) -> bool:
	if skip:return _ok(flow,{"op":"post_skip"})
	var initial: Array=flow.pages
	for i in range(initial.size()):
		if flow.cursor!=i or not _ok(flow,{"op":"post_next"}):return false
		if flow.phase=="chapter309_choice":return i==initial.size()-2
	return true


func _ok(flow: RefCounted, command: Dictionary) -> bool:
	var result: Dictionary=flow.execute(command)
	if not result.supported:printerr(command," ",result)
	return result.supported
