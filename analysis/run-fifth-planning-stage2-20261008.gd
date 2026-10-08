extends SceneTree
func _initialize() -> void:
	var suite = load("res://sim/tests/test_school_fifth_planning.gd").new()
	quit(1 if suite._run_all() > 0 else 0)
