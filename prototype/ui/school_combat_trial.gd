extends "res://ui/school_field_trial.gd"
const Combat := preload("res://sim/school_combat_session.gd")
const FieldTrial := preload("res://ui/school_field_trial.gd")

class CombatCanvas extends FieldTrial.FieldCanvas:
	var labels: Dictionary = {}
	var inspected_id := -1

	func _draw() -> void:
		super._draw()
		if session == null or not session.ready: return
		var font := get_theme_font("font","Label")
		for unit in session.units:
			if unit["limits"]["hp"] <= 0: continue
			var ground := origin+session.position(unit)*zoom
			var color := Color("d67a63") if unit["category"] == 5 else Color("d4d5a9") if not unit["controllable"] else Color("99d6bd")
			var width := 38.0*zoom
			draw_rect(Rect2(ground+Vector2(-width*0.5,9),Vector2(width,4)),Color("172726"))
			draw_rect(Rect2(ground+Vector2(-width*0.5,9),Vector2(width*unit["limits"]["hp"]/unit["limits"]["hp_max"],4)),color)
			if inspected_id == session.unit_key(unit):
				draw_arc(ground,20*zoom,0,TAU,32,color,2,true)
			if zoom >= 0.7:
				var text: String = labels.get(session.unit_key(unit),"")
				draw_string(font,ground+Vector2(-22,30),text,HORIZONTAL_ALIGNMENT_LEFT,-1,13,color)
		for event in session.events:
			var age: int = session.frame-event["frame"]
			if age > 30: continue
			var target: Dictionary = session.find_unit(event["target"])
			var ground := origin+session.position(target)*zoom
			var text := "MISS" if event["damage"] < 0 else "−%d" % event["damage"]
			draw_string(font,ground+Vector2(-15,-70-age),text,HORIZONTAL_ALIGNMENT_LEFT,-1,18,Color(1,0.8,0.55,1-age/30.0))


var enemy_button: Button
var target_info: Label
var inspected_id := -1
var _last_event := -1


func _new_session(): return Combat.new()


func _new_canvas() -> FieldCanvas: return CombatCanvas.new()


func _ready() -> void:
	super._ready()
	title_label.text = "第五周 · 战斗操作试验"
	enemy_button = _button("查看敌人",_focus_enemy)
	center_button.get_parent().add_child(enemy_button)
	center_button.get_parent().move_child(enemy_button,3)
	target_info = Label.new(); target_info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	info.get_parent().add_child(target_info); info.get_parent().move_child(target_info,info.get_index()+1)
	help_label.text = "左键选人/查看对象 · 右键移动/攻击敌人 · 中键拖图 · 空格暂停 · S停止 · Esc返回\n战斗试验 · 暂无正式通关与奖励"
	help_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	canvas.chosen.connect(func(identity): inspected_id = identity; canvas.inspected_id = identity; _refresh())
	canvas.commanded.connect(func(_cell):
		var selected: Dictionary = session.find_unit(session.selected_id)
		if not selected.is_empty() and selected["target"] >= 0:
			inspected_id = selected["target"]; canvas.inspected_id = inspected_id
			status.text = "攻击指令已下达 · 接近目标后自动攻击。"
		_refresh())


func open_trial(preparation: Dictionary, combat: Dictionary, names: Dictionary) -> bool:
	if not super.open_trial(preparation,combat,names): return false
	var index := 1
	for unit in session.units:
		if unit["controllable"]: continue
		var identity: int = session.unit_key(unit)
		_names[identity] = "敌人 %d" % index if unit["category"] == 5 else "石碑" if unit["job"] == 387 \
			else "泉" if unit["job"] == 393 else "宝箱" if unit["job"] == 406 else "场景角色"
		if unit["category"] == 5: index += 1
	canvas.labels = _names.duplicate(true); inspected_id = -1; canvas.inspected_id = -1; _last_event = -1
	status.text = "右键敌人下达攻击指令；「查看敌人」可定位最近目标。"
	_refresh()
	return true


func _refresh() -> void:
	super._refresh()
	if target_info == null or not session.ready or not session is Combat: return
	var selected: Dictionary = session.find_unit(session.selected_id)
	if not selected.is_empty():
		var state := "已倒下" if selected["limits"]["hp"] <= 0 else "施法中" if selected["visual"] == "cast" \
			else "攻击中" if selected["visual"] == "attack" else "收势中" if selected["visual"] == "recover" \
			else "接近目标" if selected["target"] >= 0 and not selected["path"].is_empty() else "待命"
		info.text = "%s · 格 %d,%d · %s    |    班级领队：%s" % [_names.get(session.selected_id,str(session.selected_id)),
			selected["cell"].x,selected["cell"].y,"已暂停" if session.paused else state,_names.get(101,"101")]
	var target: Dictionary = session.find_unit(inspected_id)
	target_info.text = "初始敌人 · 剩余 %d / 7" % session.enemies().size()
	if not target.is_empty():
		target_info.text += "    |    %s · HP %d/%d · %s" % [_names.get(inspected_id,"对象"),target["limits"]["hp"],target["limits"]["hp_max"],
			"已清除" if target["limits"]["hp"] <= 0 else "可攻击" if target["category"] == 5 else "场景对象"]
	if session.trial_complete: status.text = "初始敌人已清除 · 试验完成，可返回学校；正式冒险尚未结束。"
	stop_button.disabled = selected.is_empty() or selected["limits"]["hp"] <= 0
	canvas.queue_redraw()


func _focus_enemy() -> void:
	if not session.ready or session.enemies().is_empty(): return
	var candidates: Array = session.enemies().duplicate()
	var selected: Dictionary = session.find_unit(session.selected_id)
	candidates.sort_custom(func(a,b): return session._distance(selected,a) < session._distance(selected,b))
	var unit: Dictionary = candidates[0]
	inspected_id = session.unit_key(unit); canvas.inspected_id = inspected_id
	canvas.zoom = 1.25; canvas.fit_mode = false
	canvas.origin = canvas.size*0.5-session.position(unit)*canvas.zoom; canvas.clamp_origin()
	_refresh()
