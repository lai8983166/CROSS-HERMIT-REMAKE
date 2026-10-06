extends "res://ui/tests/test_new_game_school_window.gd"
## Cross-session navigation must preserve both returned and source-new-game schools.


func _run() -> void:
	root.size = Vector2i(1024,768)
	root.gui_embed_subwindows = true
	var main = load("res://main.tscn").instantiate()
	root.add_child(main)
	await process_frame
	main.set_physics_process(false)
	await _click(main.return_panel.start_button)
	main._physics_process(10000.0)
	_check(main.return_demo.stage == "result","actual terminal reaches result")
	await _click(main.return_panel.confirm_button)
	await _click(main.return_panel.school_button)
	_check(main.return_demo.stage == "school","returned school opens")
	var returned = main.return_demo
	var original: Dictionary = returned.view().duplicate(true)
	var battle = main.battle
	await _click(main.return_panel.new_school_button)
	var panel = main.school_panel
	var source = panel.session
	_check(source != null and panel.visible,"new source school opens from returned school")
	_check(main.return_demo == returned and returned.view() == original,"opening preserves returned campaign")
	await _click(panel.teacher_buttons[0])
	await _click(panel.teacher_buttons[3])
	_check(source.read_snapshot()["derived_teacher_ids"] == [-1,-1,-1,101,-1],"new school edits independently")
	var edited: Dictionary = source.read_snapshot()
	await _click(panel.close_button)
	_check(main.return_panel.visible and returned.view() == original,"close restores exact returned page and data")
	_check(main.return_panel.blocks_battle_input(),"restored returned page still blocks battle")
	_check(main.battle == battle and battle.frame == 330,"navigation leaves terminal battle intact")
	await _click(main.return_panel.new_school_button)
	_check(panel.session == source and source.read_snapshot() == edited,"source school retains edits across returned navigation")
	await _click(panel.close_button)
	await _click(main.return_panel.default_button)
	_check(main.return_demo == null and main.battle.units.size() == 8,"default action still restores normal battle")
	await _click(main.return_panel.new_school_button)
	_check(panel.session == source and source.read_snapshot() == edited,"default battle navigation preserves independent school")
	main.queue_free()
	await process_frame
	print("School cross-session navigation: %d checks, %d failures" % [checks,failures.size()])
	quit(0 if failures.is_empty() else 1)
