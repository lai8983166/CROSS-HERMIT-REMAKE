extends SceneTree
## Rebuild the January departure and return through the normal school command API.
const Model := preload("res://sim/school_playground.gd")


func _init() -> void:
	call_deferred("_run")


func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() != 3 or FileAccess.get_sha256(args[1]) != "deca0122f6ae5f19bf0c8a29decdee04c5baee0a3a097ae2825aaa94b32a8906":
		quit(1)
		return
	var saved: Dictionary = Model.Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(args[1])))
	var model := Model.new()
	var loaded := model.load_week_state(args[0])
	if not loaded.supported or loaded.get("status") != "restored":
		printerr(loaded)
		quit(1)
		return
	var prefix: Array = model.export_save().commands
	if prefix.size() > 1577 or saved.commands.slice(0, prefix.size()) != prefix:
		printerr("Parent does not precede this departure")
		quit(1)
		return
	var observed := {}
	for index in range(prefix.size(), 1585):
		var cmd: Dictionary = saved.commands[index]
		var result := model.execute(cmd)
		if not result.supported:
			printerr([index, cmd.op, result])
			quit(1)
			return
		match index:
			1578:
				observed.handoff = model._postbattle.planning.handoff.duplicate(true)
				observed.before = model._postbattle.bundle.duplicate(true)
			1579:
				observed.after = model._postbattle.bundle.duplicate(true)
			1584:
				observed.returned = model._postbattle.bundle.duplicate(true)
				observed.phase = model._postbattle.phase
	if observed.phase != "returned_school":
		printerr(["Incomplete school return", observed.phase])
		quit(1)
		return
	var file := FileAccess.open(args[2], FileAccess.WRITE)
	if file == null:
		quit(1)
		return
	file.store_string(JSON.stringify(observed))
	file.close()
	print("Replayed school command 1585, phase ", observed.phase)
	quit(0)
