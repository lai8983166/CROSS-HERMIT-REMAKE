extends SceneTree
## headless 测试入口: ~/bin/godot --headless --path prototype -s res://sim/tests/test_runner.gd
## 退出码 0=全绿, 1=有失败 (满足 combat-math spec "可测试性与确定性")

const BASE := preload("res://sim/tests/test_base.gd")


func _init() -> void:
	var dir := DirAccess.open("res://sim/tests")
	var files: Array[String] = []
	dir.list_dir_begin()
	var f := dir.get_next()
	while f != "":
		if f.begins_with("test_") and f.ends_with(".gd") and f != "test_runner.gd" and f != "test_base.gd":
			files.append(f)
		f = dir.get_next()
	dir.list_dir_end()
	files.sort()

	var total_failed := 0
	var suites := 0
	for name in files:
		var script: GDScript = load("res://sim/tests/" + name)
		var inst: RefCounted = script.new()
		if inst == null or not inst.has_method("_run_all"):
			print("SKIP ", name, " (不继承 test_base)")
			continue
		suites += 1
		total_failed += inst._run_all()

	print("=== %d suites, %d failures ===" % [suites, total_failed])
	quit(1 if total_failed > 0 else 0)
