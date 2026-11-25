extends SceneTree
const SchoolPanel := preload("res://ui/school_postbattle_panel.gd")
const Flow := preload("res://sim/school_postbattle_flow.gd")

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size()!=1 or not FileAccess.file_exists(args[0]):
		printerr("Expected the October week-one settlement capture")
		quit(1)
		return
	var flow := Flow.new()
	var capture: Dictionary=Flow.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(args[0])))
	flow.bundle=capture.before
	flow.phase="returned_school"
	var ledger := Flow.Adventures.initial()
	Flow.Adventures._open(ledger,10,1,Flow.Adventures.rules())
	flow.planning={"ledger":ledger}
	var panel := SchoolPanel.new()
	root.add_child(panel)
	panel.show_state(flow.snapshot(),{},"")
	var member_button := panel.roster.find_child("member_3",false,false) as Button
	if member_button==null:
		quit(1)
		return
	member_button.pressed.emit()
	var picker := panel.assignments.find_child("eligible_jobs",true,false) as OptionButton
	var courses := panel.plans.find_child("courses_0",true,false) as OptionButton
	var mission := panel.plans.find_child("adventure_33",true,false) as Button
	if picker==null or courses==null or mission==null or not panel.heading.text.begins_with("10月 · 第1周"):
		quit(1)
		return
	var student: Dictionary=flow.bundle.participants[0]
	var expected := Flow.JobEligibility.calculate_eligibility(student,Flow.JobEligibility.menu_data())
	var displayed := range(picker.item_count).map(func(i):return picker.get_item_id(i))
	if displayed!=expected or courses.item_count<2:
		quit(1)
		return
	var sent := []
	panel.command.connect(func(c):sent.append(c))
	mission.pressed.emit()
	if sent!=[{"op":"return_select","adventure":33}] or not flow.execute(sent[0]).supported:
		printerr("October adventure 33 did not become the school selection")
		quit(1)
		return
	sent.clear()
	for i in range(picker.item_count):
		var job := picker.get_item_id(i)
		if job==student.job:continue
		picker.select(i)
		picker.item_selected.emit(i)
		panel.assignments.find_child("change_job",true,false).pressed.emit()
		panel.commit_dialog.confirmed.emit()
		var command := {"op":"return_job","member":3,"job":job}
		var ok: bool=sent==[command] and flow.execute(command).supported and flow.bundle.participants[0].job==job
		print("October controls: course options ",courses.item_count-1,", adventure 33, eligible jobs ",displayed,", confirmed job ",job)
		quit(0 if ok else 1)
		return
	quit(1)
