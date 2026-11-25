extends SceneTree
const Comparison := preload("res://sim/tests/school_year_course_comparison.gd")
func _init() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size()!=1:
		printerr("Expected the directory containing the six played settlement captures")
		quit(1)
		return
	var directory := args[0]
	for date in [[10,1],[10,2],[10,3],[10,4],[10,5],[11,1]]:
		var path := directory.path_join("settlement-%02d-%d.json"%date)
		if not FileAccess.file_exists(path):
			printerr("Missing ",path)
			quit(1)
			return
		var case: Dictionary=Comparison.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(path)))
		if date!=[10,1] and not Comparison.compare_menus(case.before):
			printerr(date," job menu")
			quit(1)
			return
		var row: Dictionary=case.after
		var result:=Comparison.compare(row)
		if not result.is_empty():
			printerr(date," ",result)
			quit(1)
			return
		row.records[0].job_progress[1]+=1
		if Comparison.compare(row)!="history":
			quit(1)
			return
	print("Six played settlement snapshots matched and six changed careers rejected.")
	quit(0)
