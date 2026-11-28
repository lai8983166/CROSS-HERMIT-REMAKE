extends SceneTree
## Re-execute the entire final command campaign and capture exact weekly inputs.
const Eligibility := preload("res://sim/school_job_eligibility.gd")
const Model := preload("res://sim/school_playground.gd")
const FIELDS := ["character_id","attributes","job_progress","unlock_flags","skill_statuses","equipped_skills","equipped_items"]
class ObservedModel extends Model:
	static var observer: SceneTree

	func execute(command: Variant) -> Dictionary:
		if observer==null:return super.execute(command)
		observer.before_command(self,command)
		var result := super.execute(command)
		if result.supported:observer.after_command(self,command)
		return result


var transfers := []
var pending_transfer := {}
var assignments := []
var pending_assignment := {}
var pending_work := {}
var directory := ""
var weeks := []
var work := []
var parents := {}
var terminal_growth_sha256 := ""
var ending_chapter := ""
var command_index := 0
var failed := false


func _init() -> void:
	call_deferred("_run")


func _write(name: String, data: Variant) -> bool:
	var file := FileAccess.open(directory.path_join(name),FileAccess.WRITE)
	if file==null:return false
	file.store_string(JSON.stringify(data))
	file.close()
	return true


func _digest(data: Variant) -> String:
	return JSON.stringify(data,"",true).sha256_text()


func _week_fields(state: Dictionary) -> Dictionary:
	var rows := []
	for participant in state.participants:
		var row := {}
		for key in FIELDS:row[key]=participant[key]
		rows.append(row)
	return {"month":state.month,"week":state.week,"flags":state.flags,"availability":state.availability,
		"item_flags":state.item_flags,"participants":rows}


func _week(before: Dictionary, after: Dictionary) -> void:
	if after.month<10:return
	if [after.month,after.week]==[15,5]:
		var growth := []
		for r in before.participants:
			var fields := {"character_id":r.character_id}
			for key in Model.Postbattle.Return.GROWTH_KEYS:fields[key]=r[key]
			growth.append(fields)
		terminal_growth_sha256=_digest(growth)
	var tag := "%02d-%d" % [after.month,after.week]
	var expected := _week_fields(after)
	var selectable := {}
	var menu := Eligibility.menu_data()
	for r in after.participants:
		selectable[str(r.character_id)]=Eligibility.calculate_eligibility(r,menu)
	weeks.append({"date":[after.month,after.week],"command":command_index,"state_sha256":_digest(expected)})
	if not _write("original-week-"+tag+".json",{"before":_week_fields(before),"expected_sha256":_digest(expected),"selectable_jobs":selectable}):failed=true


func _settlement(before: Dictionary, after: Dictionary, op: String) -> void:
	var result: Dictionary=after.course_result if op=="return_settle" else after.sortie_result
	var row := {"date":[before.school.month,before.school.week],"command":command_index,
		"work":"lesson" if op=="return_settle" else "adventure","total":after.school.global_total_511c,
		"mvp":result.recipient,"growth_sha256":_digest(after.growth),"history_sha256":_digest(after.records),
		"mvp_counts_sha256":_digest(after.counts),"relationships_sha256":_digest(after.school.relationships)}
	if op=="sortie_finish":row.adventure=result.scene_id
	if row.date==[15,4]:row.growth_sha256=terminal_growth_sha256
	work.append(row)
	if row.date==[11,2] and not _write("lesson-11-2.json",{"before":before,"after":after}):failed=true


func _equipment(bundle: Dictionary, member: int) -> Dictionary:
	var student := Model.Postbattle.Return._find(bundle.participants,member)
	var result := {"item_flags":bundle.item_flags.duplicate()}
	for key in ["job","level_50","equipped_items","equipped_skills","skill_statuses"]:
		result[key]=student[key].duplicate() if student[key] is Array else student[key]
	return result


func before_command(model: Model, cmd: Dictionary) -> void:
	command_index+=1
	pending_work={}
	pending_transfer={}
	pending_assignment={}
	if model._postbattle!=null:
		model._postbattle.week_observer=_week
		if cmd.op=="return_skill":
			var bundle: Dictionary=model._postbattle.bundle
			pending_assignment={"command":command_index,"date":[bundle.school.month,bundle.school.week],
				"member_id":cmd.member_id,"skill":cmd.skill,"slot":cmd.slot,"before":bundle.duplicate(true)}
		if cmd.op=="return_job":
			var bundle: Dictionary=model._postbattle.bundle
			var student := Model.Postbattle.Return._find(bundle.participants,cmd.member)
			pending_transfer={"command":command_index,"date":[bundle.school.month,bundle.school.week],
				"member":cmd.member,"target":cmd.job,"unlock_flags":student.unlock_flags.duplicate(),
				"before":_equipment(bundle,cmd.member)}
		if cmd.op in ["return_settle","sortie_finish"] and model._postbattle.bundle.school.month>=10:
			pending_work=model._postbattle.bundle


func after_command(model: Model, cmd: Dictionary) -> void:
	if not pending_assignment.is_empty():
		pending_assignment.after_sha256=_digest(model._postbattle.bundle)
		assignments.append(pending_assignment)
	if model._postbattle!=null and not model._postbattle._winter_story.is_empty() and model._postbattle._winter_story.terminal:
		var terminal_pages: Array=model._postbattle._winter_story.pre_week
		if not terminal_pages.is_empty():ending_chapter=terminal_pages[-1].chapter
	if not pending_transfer.is_empty():
		pending_transfer.after=_equipment(model._postbattle.bundle,cmd.member)
		transfers.append(pending_transfer)
	if not pending_work.is_empty():_settlement(pending_work,model._postbattle.bundle,cmd.op)
	if command_index in [1421,1455,1460,1468,1488,1500,1509]:
		var checkpoint: Dictionary=model.export_save()
		parents[str(command_index)]=checkpoint.state_sha256


func _runtime_sources() -> Dictionary:
	var result := {}
	for filename in ["school_sortie_week.gd","school_winter_story.gd","school_year_loop.gd","school_postbattle_flow.gd","week_settlement_replay.gd","school_playground.gd"]:
		var raw := FileAccess.get_file_as_string("res://sim/"+filename)
		result["prototype/sim/"+filename]=raw.replace("\r\n","\n").sha256_text()
	return result


func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size()!=2:
		quit(1)
		return
	directory=args[1]
	var saved: Dictionary=Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(args[0])))
	var runtime := _runtime_sources()
	var model := ObservedModel.new()
	ObservedModel.observer=self
	var restored := model.load_week_state(args[0])
	ObservedModel.observer=null
	if saved.get("version")!=40 or not restored.supported or restored.get("status")!="restored":
		printerr(["final load",command_index,restored])
		quit(1)
		return
	var replayed: Dictionary=model.export_save()
	if failed or runtime!=_runtime_sources() or ending_chapter!="097A" or replayed!=saved or model._postbattle.phase!="school_year_complete" or weeks.size()!=30 or work.size()!=29:
		printerr(["incomplete replay",weeks.size(),work.size(),model._postbattle.phase])
		quit(1)
		return
	var blocked := []
	for op in ["post_next","return_settle","return_depart","post_school"]:
		if model.execute({"op":op}).supported or model.export_save()!=saved:
			printerr(["terminal command accepted or mutated state",op])
			quit(1)
			return
		blocked.append(op)
	var altered := saved.duplicate(true)
	var winter_keys: Array=altered.rules.keys().filter(func(key):return str(key).contains("winter"))
	if winter_keys.is_empty():
		printerr("Missing winter rule identity")
		quit(1)
		return
	altered.rules[winter_keys[0]]="0".repeat(64)
	var rejected := model.restore(altered)
	if rejected.supported or rejected.reason!="save_rules_changed" or model.export_save()!=saved:
		printerr("Rule tamper changed final replay")
		quit(1)
		return
	if not _write("played-job-transfers.json",transfers) or not _write("played-skills.json",assignments):
		quit(1)
		return
	var summary := {"job_transfers_sha256":_digest(transfers),"played_skills_sha256":_digest(assignments),"runtime_sha256_lf":runtime,"save_sha256":FileAccess.get_sha256(args[0]),"state_sha256":saved.state_sha256,
		"commands":command_index,"phase":model._postbattle.phase,"parents":parents,"weeks":weeks,"work":work,
		"ending_chapter":ending_chapter,"terminal_commands_rejected":blocked,
		"tamper":{"key":winter_keys[0],"reason":rejected.reason,"preserved_state_sha256":model.export_save().state_sha256}}
	quit(0 if _write("independent-year-replay.json",summary) else 1)
