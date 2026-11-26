extends SceneTree
## Check returned-school commands through the actual controls, using the played inputs.
const SchoolPanel := preload("res://ui/school_postbattle_panel.gd")
const Flow := preload("res://sim/school_postbattle_flow.gd")

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size()!=2:
		quit(1)
		return
	var opening := _read(args[0])
	var settlement := _read(args[1])
	if opening.is_empty() or settlement.is_empty():
		quit(1)
		return
	var panel := SchoolPanel.new()
	root.add_child(panel)
	panel.show_state(opening,{},"")
	var opening_settle := panel.plans.find_child("settle",true,false) as Button
	if opening_settle==null or not opening_settle.visible or panel.plans.find_child("depart",true,false)!=null:
		quit(1)
		return
	var flow := Flow.new()
	flow.phase="returned_school"
	flow.planning=opening.planning
	flow.bundle=settlement.before
	panel.show_state(flow.snapshot(),{},"")
	var picker := panel.plans.find_child("courses_0",true,false) as OptionButton
	var settle := panel.plans.find_child("settle",true,false) as Button
	if picker==null or picker.disabled or settle==null or settle.disabled or not settle.visible or flow.bundle.school.derived_teacher_ids[0]!=107:
		quit(1)
		return
	var options := []
	for i in range(1,picker.item_count):options.append(picker.get_item_id(i))
	options.sort()
	if options!=[37,38]:
		printerr("Unexpected teacher 107 courses ",options)
		quit(1)
		return
	var signals := []
	panel.command.connect(func(cmd):signals.append(cmd))
	picker.item_selected.emit(picker.selected)
	if signals!=[{"op":"return_course","group":0,"course":picker.get_selected_id()}] or not flow.execute(signals[0]).supported:
		quit(1)
		return
	# Return to the class selected in the recorded plan before comparing its entire state.
	var group: int=settlement.before.school.selected_group
	var last_picker := panel.plans.find_child("courses_%d"%group,true,false) as OptionButton
	signals.clear()
	last_picker.item_selected.emit(last_picker.selected)
	if signals.size()!=1 or not flow.execute(signals[0]).supported:
		quit(1)
		return
	signals.clear()
	settle.pressed.emit()
	if not panel.commit_dialog.visible or not signals.is_empty():
		quit(1)
		return
	panel.commit_dialog.confirmed.emit()
	if signals!=[{"op":"return_settle"}] or not flow.execute(signals[0]).supported or flow.bundle!=settlement.after:
		quit(1)
		return
	panel.show_state(flow.snapshot(),{},"")
	var proceed := panel.plans.find_child("continue_course_story",true,false) as Button
	if proceed==null:
		quit(1)
		return
	signals.clear()
	proceed.pressed.emit()
	var ok: bool=signals==[{"op":"course_story"}] and flow.execute(signals[0]).supported and flow.phase=="new_week_story" and flow.bundle.school.student_count==17
	print("November four school panel, teacher 107 courses ",options,", confirmed settlement and story ",ok)
	quit(0 if ok else 1)

func _read(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):return {}
	return Flow.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(path)))
