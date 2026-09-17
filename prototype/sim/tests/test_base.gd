extends RefCounted
## 轻量测试基类 (design.md 决策 6 的备选方案转正: GUT 9.3/9.6 与 Godot 4.7.2 无头均挂起)
## 用法: 继承本类, 写 test_ 开头的方法, 由 test_runner.gd 发现并执行

var _failures: Array[String] = []
var _current := ""


func _run_all() -> int:  # 返回失败数; 由 runner 调用
	var methods := get_method_list()
	var names: Array[String] = []
	for m in methods:
		if String(m.name).begins_with("test_") and m.args.is_empty():
			names.append(String(m.name))
	names.sort()
	for n in names:
		_current = n
		call(n)
	var total := names.size()
	if total == 0:
		_failures.append("%s: 无 test_ 方法" % _name())
	print("%-28s %d tests, %d failed" % [_name(), total, _failures.size()])
	for f in _failures:
		print("  FAIL ", f)
	return _failures.size()


func _name() -> String:
	return get_script().resource_path.get_file()


# ── 断言 ──────────────────────────────────────────────
func _fail(msg: String) -> void:
	_failures.append("%s::%s: %s" % [_name(), _current, msg])


func assert_true(cond: bool, msg := "expected true") -> void:
	if not cond:
		_fail(msg)


func assert_eq(got: Variant, want: Variant, msg := "") -> void:
	if got != want:
		_fail("%s got=%s want=%s" % [msg, str(got), str(want)])


func assert_lt(a: Variant, b: Variant, msg := "") -> void:
	if not (a < b):
		_fail("%s %s !< %s" % [msg, str(a), str(b)])
