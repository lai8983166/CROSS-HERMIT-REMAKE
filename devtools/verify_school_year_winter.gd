extends SceneTree
## Continue the fixed v39 command campaign, or run a bounded probe on its replayed opening.
const Model := preload("res://sim/school_playground.gd")
const Flow := preload("res://sim/school_postbattle_flow.gd")
const PREFIX := "3bdc952ed0b41d40c0e1a0affb50de2ec6cac001488653801475f0c5548ef94f"
const PARENT := "05aa0e94a801cb687cab070210b1a105d5febe2dfc3e0a6e513e8fbed6d9aafe"
var session: RefCounted
var flow: Flow
var directory: String
var formal := false
var battle_directory: String
var wait_for_battles := false

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() not in [3,4] or args[0] not in ["campaign","campaign-live","resume","probe","replay"]:
		quit(1)
		return
	directory=args[2]
	battle_directory=args[3] if args.size()==4 else directory
	wait_for_battles=args[0]=="campaign-live"
	if args[0]=="replay":
		quit(0 if _replay(args[1]) else 1)
		return
	formal=args[0] in ["campaign","campaign-live","resume"]
	if formal:
		var model := Model.new()
		if (args[0] in ["campaign","campaign-live"] and FileAccess.get_sha256(args[1])!=PARENT) or not model.load_week_state(args[1]).supported:
			quit(1)
			return
		if args[0]=="resume":
			var save := model.export_save()
			if save.version!=40 or model.stage()!="sortie_pending" or JSON.stringify(save.commands.slice(0,1509),"",true).sha256_text()!=PREFIX:
				quit(1)
				return
		session=model
		flow=model._postbattle
	else:
		var opening: Dictionary=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(args[1])))
		flow=Flow.new()
		flow.bundle=opening.bundle
		flow.phase=opening.phase
		flow.planning=opening.planning
		session=flow
	quit(0 if _play() else 1)

func _replay(path: String) -> bool:
	var model := Model.new()
	var loaded := model.load_week_state(path)
	if not loaded.supported:
		printerr(loaded)
		return false
	var save := model.export_save()
	var snapshot := model.read_postbattle()
	var date: Array=[snapshot.bundle.school.month,snapshot.bundle.school.week]
	if save.version!=40:return false
	var tampered := save.duplicate(true)
	tampered.rules.winter_story="invalid"
	if model.restore(tampered).get("reason")!="save_rules_changed" or model.export_save()!=save:return false
	var evidence := {"date":date,"phase":snapshot.phase,"state_sha256":save.state_sha256,
		"file_sha256":FileAccess.get_sha256(path),"commands":save.commands.size(),"tamper_rejected":true}
	if snapshot.phase=="school_year_complete":
		if date!=[15,5] or model.execute({"op":"post_school"}).supported:return false
	elif snapshot.phase=="chapter310_choice":
		if not model.execute({"op":"post_choice","choice":0}).supported:return false
		evidence["continued_phase"]=model.stage()
	else:return false
	print(evidence)
	return _write("replay-"+snapshot.phase+".json",evidence)

func _act(cmd: Dictionary) -> bool:
	var result: Dictionary=session.execute(cmd)
	if not result.supported:printerr([flow.bundle.school.month,flow.bundle.school.week,flow.phase,cmd.op,result])
	return result.supported

func _write(name: String, value: Dictionary) -> bool:
	var path := directory.path_join(name)
	if FileAccess.file_exists(path):
		var existing: Variant=JSON.parse_string(FileAccess.get_file_as_string(path))
		if existing is Dictionary and Model.Roles._integers(existing)==value:return true
		printerr("Existing evidence differs: ",name)
		return false
	var file := FileAccess.open(path,FileAccess.WRITE)
	if file==null:return false
	file.store_string(JSON.stringify(value))
	file.close()
	return true

func _play() -> bool:
	for step in range(400):
		var school: Dictionary=flow.bundle.school
		var date := "%02d-%d" % [school.month,school.week]
		match flow.phase:
			"returned_school":
				print("School ",date)
				if school.adventure_gate!=0:
					var mission: int=school.lecture_work_fields[2]
					if wait_for_battles:
						print("Waiting for independently replayed mission ",mission)
						while not FileAccess.file_exists(battle_directory.path_join("facts-%d.json"%mission)):
							OS.delay_msec(1000)
					for group in range(5):
						if school.derived_teacher_ids[group]<0:continue
						for slot in range(4):
							var current: Dictionary=flow.bundle.school
							if current.idle_student_ids.is_empty():break
							if current.derived_student_ids[group][slot]<0:
								var member: int=current.idle_student_ids[0]
								if not _act({"op":"return_move","kind":"student","member_id":member,"target_group":group,"target_slot":slot}):return false
					var plan_path := battle_directory.path_join("planning-%d.json"%mission)
					if FileAccess.file_exists(plan_path):
						var plan: Variant=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(plan_path)))
						if not plan is Array:return false
						for command in plan:
							if not command is Dictionary or command.get("op") not in ["return_job","return_move","return_skill"] or not _act(command):return false
					if not _act({"op":"return_depart"}):return false
				else:
					for group in range(5):
						if school.derived_teacher_ids[group]<0:continue
						if not _act({"op":"return_mode","group":group,"teaching":true}):return false
						var options := Flow.Courses.list_courses(flow.bundle,group)
						if not options.supported:return false
						var course := -1
						for category in options.courses:
							if not category.is_empty():
								course=category[0][1]
								break
						if not _act({"op":"return_course","group":group,"course":course}):return false
					var before := flow.bundle
					if not _act({"op":"return_settle"}):return false
					if not _write("lesson-"+date+".json",{"before":before,"after":flow.bundle}):return false
			"sortie_pending":
				var handoff: Dictionary=flow.planning.handoff
				var id: int=handoff.prepared.adventure_id
				if not _write("handoff-%d.json" % id,handoff):return false
				if formal:
					var checkpoint := directory.path_join("pending-%d-v40.json" % id)
					if not FileAccess.file_exists(checkpoint) and not session.save_week_state(checkpoint).supported:return false
				if battle_directory!=directory:
					var expected_path := battle_directory.path_join("handoff-%d.json"%id)
					var expected: Variant=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(expected_path)))
					if expected!=handoff:
						printerr("Formal departure differs from replayed battle ",id)
						return false
				var trace_path := battle_directory.path_join("trace-%d.json" % id)
				if not FileAccess.file_exists(trace_path):
					printerr("Awaiting battle trace ",trace_path)
					return false
				var before := flow.bundle
				var opening_ledger: Dictionary=flow.planning.opening_ledger
				var grades: Dictionary=flow._task_grades.duplicate()
				var trace: Dictionary=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(trace_path)))
				if not _act({"op":"sortie_finish","trace":trace}):return false
				var settled := flow.bundle
				if id==45:
					var facts_path := battle_directory.path_join("facts-45.json")
					if not FileAccess.file_exists(facts_path):return false
					var facts: Dictionary=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(facts_path)))
					var result := Flow.SortieSettlement.apply(before,handoff,facts,opening_ledger,grades)
					if not result.supported or result.summary!=flow.planning.sortie_summary:return false
					settled=result.after
					if not _write("terminal-arrival.json",{"participants":flow.bundle.participants}):return false
				if not _write("settled-"+date+".json",{"before":before,"after":settled}):return false
			"school_year_complete":
				if [school.month,school.week]!=[15,5]:return false
				for op in ["post_next","return_settle","return_depart","post_school"]:
					if session.execute({"op":op}).supported:return false
				if formal:return session.save_week_state(directory.path_join("march-ending-v40.json")).supported
				return true
			"course_result":
				if not _act({"op":"course_story"}):return false
			"post_workroom":
				if not _act({"op":"post_school"}):return false
			"post_story","new_week_story","school_entry_story":
				if not _act({"op":"post_next" if flow.snapshot().has("date_card") else "post_skip"}):return false
			"sortie_result":
				if not _act({"op":"post_next"}):return false
			_:
				if flow.phase.ends_with("_choice"):
					if formal and flow.phase=="chapter310_choice":
						var path := directory.path_join("chapter310-v40.json")
						if not FileAccess.file_exists(path) and not session.save_week_state(path).supported:return false
					if not _act({"op":"post_choice","choice":0}):return false
				else:
					printerr("Unverified boundary ",date," ",flow.phase)
					return false
	return false
