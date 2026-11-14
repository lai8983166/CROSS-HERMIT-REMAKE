extends "res://ui/school_field_trial.gd"
const Combat := preload("res://sim/school_combat_session.gd")
const FieldTrial := preload("res://ui/school_field_trial.gd")
const OpeningStage := preload("res://ui/school_opening_stage.gd")

class CombatCanvas extends FieldTrial.FieldCanvas:
	var labels: Dictionary = {}
	var inspected_id := -1
	var controls_enabled := true

	func _gui_input(event: InputEvent) -> void:
		if controls_enabled: super._gui_input(event)

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
var result_panel: PanelContainer
var result_title: Label
var result_details: Label
var return_button: Button
var _handoff_emitted := false
var opening_panel: VBoxContainer
var opening_stage: OpeningStage
var opening_progress: Label
var opening_next_button: Button


func _new_session(): return Combat.new()


func _new_canvas() -> FieldCanvas: return CombatCanvas.new()


func _new_opening_stage(): return OpeningStage.new()


func _ready() -> void:
	super._ready()
	title_label.text = "第五周 · 战斗操作试验"
	enemy_button = _button("查看敌人",_focus_enemy)
	center_button.get_parent().add_child(enemy_button)
	center_button.get_parent().move_child(enemy_button,3)
	target_info = Label.new(); target_info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	info.get_parent().add_child(target_info); info.get_parent().move_child(target_info,info.get_index()+1)
	help_label.text = "左键选人/查看对象 · 右键移动/攻击敌人 · 中键拖图 · 空格暂停 · S停止 · Esc结束试验\n仅试验初始队伍与敌人，不推进正式冒险或发放奖励。"
	help_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	result_panel = PanelContainer.new()
	var result_margin := MarginContainer.new()
	for side in ["left","right","top","bottom"]: result_margin.add_theme_constant_override("margin_"+side,20)
	result_panel.add_child(result_margin)
	var result_column := VBoxContainer.new()
	result_column.add_theme_constant_override("separation",12)
	result_margin.add_child(result_column)
	result_title = Label.new(); result_title.add_theme_font_size_override("font_size",24)
	result_column.add_child(result_title)
	result_details = Label.new(); result_details.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	result_column.add_child(result_details)
	var scope := Label.new()
	scope.text = "本次仅结束战斗操作试验，不计正式通关、不发放奖励，也不推进日期。学校编班保持原样。"
	scope.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	result_column.add_child(scope)
	return_button = _button("返回学校准备",_return_to_school)
	result_column.add_child(return_button)
	canvas.get_parent().add_child(result_panel)
	canvas.get_parent().move_child(result_panel,canvas.get_index()+1)
	result_panel.hide()
	opening_panel = VBoxContainer.new()
	opening_panel.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	opening_panel.mouse_filter = Control.MOUSE_FILTER_STOP
	canvas.add_child(opening_panel)
	var opening_footer := HBoxContainer.new()
	opening_footer.add_theme_constant_override("separation",12)
	opening_panel.add_child(opening_footer)
	opening_progress = Label.new()
	opening_progress.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	opening_footer.add_child(opening_progress)
	opening_next_button = _button("显示完整",_advance_opening)
	opening_footer.add_child(opening_next_button)
	opening_panel.hide()
	visibility_changed.connect(func():
		if not visible: _release_opening())
	canvas.chosen.connect(func(identity): inspected_id = identity; canvas.inspected_id = identity; _refresh())
	canvas.commanded.connect(func(_cell):
		var selected: Dictionary = session.find_unit(session.selected_id)
		if not selected.is_empty() and selected["target"] >= 0:
			inspected_id = selected["target"]; canvas.inspected_id = inspected_id
			status.text = "攻击指令已下达 · 接近目标后自动攻击。"
		_refresh())


func open_trial(preparation: Dictionary, combat: Dictionary, names: Dictionary) -> bool:
	# Validate every opening asset before replacing an already valid session.
	var next_stage = _new_opening_stage()
	if not next_stage.load_presentation():
		next_stage.free()
		return false
	if not super.open_trial(preparation,combat,names):
		next_stage.free()
		return false
	_release_opening()
	opening_stage = next_stage
	opening_stage.size_flags_vertical = Control.SIZE_EXPAND_FILL
	opening_panel.add_child(opening_stage)
	opening_panel.move_child(opening_stage,0)
	opening_stage.show_page(0)
	opening_panel.show()
	var index := 1
	for unit in session.units:
		if unit["controllable"]: continue
		var identity: int = session.unit_key(unit)
		_names[identity] = "敌人 %d" % index if unit["category"] == 5 else "石碑" if unit["job"] == 387 \
			else "泉" if unit["job"] == 393 else "宝箱" if unit["job"] == 406 else "场景角色"
		if unit["category"] == 5: index += 1
	canvas.labels = _names.duplicate(true); inspected_id = -1; canvas.inspected_id = -1; _last_event = -1
	_handoff_emitted = false
	result_panel.hide(); canvas.show(); canvas.controls_enabled = false
	_refresh()
	opening_next_button.grab_focus()
	return true


func _advance_opening() -> void:
	if not visible or not session is Combat or session.ending_snapshot()["phase"] != "opening" or opening_stage == null: return
	if not opening_stage.display_ready():
		opening_stage.finish_display()
	elif session.opening_snapshot()["awaiting_confirmation"]:
		_step_opening(true)
	_refresh()


func _step_opening(confirmed: bool) -> void:
	if session.advance_opening(confirmed):
		var opening: Dictionary = session.opening_snapshot()
		if opening["completed"]:
			_release_opening()
			canvas.focus_units()
			status.text = "右键敌人下达攻击指令；「查看敌人」可定位最近目标。"
			close_button.grab_focus()
		else:
			opening_stage.show_page(opening["page_index"])
		_refresh()


func _process(delta: float) -> void:
	super._process(delta)
	if visible and session is Combat and session.ending_snapshot()["phase"] == "opening" \
			and opening_stage != null and opening_stage.display_ready() \
			and not session.opening_snapshot()["awaiting_confirmation"]:
		_step_opening(false)


func _release_opening() -> void:
	if opening_stage != null:
		opening_stage.current_text = null
		opening_stage.layers.clear(); opening_stage.textures.clear(); opening_stage.catalog.clear()
		opening_stage.free()
		opening_stage = null
	if opening_panel != null: opening_panel.hide()
	if opening_progress != null: opening_progress.text = ""


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
	stop_button.disabled = selected.is_empty() or selected["limits"]["hp"] <= 0
	_refresh_ending()
	canvas.queue_redraw()


func _focus_enemy() -> void:
	if not session.ready or session.ending_snapshot()["phase"] != "active" or session.enemies().is_empty(): return
	var candidates: Array = session.enemies().duplicate()
	var selected: Dictionary = session.find_unit(session.selected_id)
	candidates.sort_custom(func(a,b): return session._distance(selected,a) < session._distance(selected,b))
	var unit: Dictionary = candidates[0]
	inspected_id = session.unit_key(unit); canvas.inspected_id = inspected_id
	canvas.zoom = 1.25; canvas.fit_mode = false
	canvas.origin = canvas.size*0.5-session.position(unit)*canvas.zoom; canvas.clamp_origin()
	_refresh()


func _refresh_ending() -> void:
	if result_panel == null: return
	var ending: Dictionary = session.ending_snapshot()
	var active: bool = ending["phase"] == "active"
	canvas.controls_enabled = active
	if not active: canvas.dragging = false
	for button in [pause_button,center_button,fit_button,terrain_button,zoom_in_button,zoom_out_button,enemy_button]:
		button.disabled = not active
	for button in member_buttons.values(): button.disabled = not active
	if not active: stop_button.disabled = true
	close_button.disabled = ending["phase"] == "consuming"
	close_button.text = "结束试验" if active or ending["phase"] == "opening" else "正在结束…" if ending["phase"] == "consuming" else "返回学校准备"
	if ending["phase"] == "opening":
		var opening: Dictionary = session.opening_snapshot()
		opening_progress.text = "开场对白 · %d / %d" % [opening["page_index"]+1,opening["page_count"]]
		if opening_stage != null:
			opening_next_button.text = "显示完整" if not opening_stage.display_ready() or not opening["awaiting_confirmation"] else "开始操作" if opening["page_index"] == opening["page_count"]-1 else "继续"
		status.text = "阅读开场对白后开始操作；此时战斗尚未推进。"
		help_label.text = "空格 / Enter确认 · Esc结束试验\n仅试验初始队伍与敌人，不推进正式冒险或发放奖励。"
	elif ending["phase"] == "consuming":
		_release_opening()
		status.text = "试验已停止，正在整理本次结果…"
	elif ending["phase"] == "summary":
		_release_opening()
		var first_summary := not result_panel.visible
		var summary: Dictionary = ending["summary"]
		result_title.text = {"initial_enemies_cleared":"初始敌人已清除", "squad_defeated":"当前学生已全部倒下", "player_exit":"本次试验已结束"}.get(ending["outcome"],"本次试验已结束")
		result_details.text = "已清除敌人：%d / %d　　剩余敌人：%d\n仍可行动的学生：%d / %d" % [summary["defeated_enemies"],summary["initial_enemies"],summary["remaining_enemies"],summary["surviving_students"],summary["total_students"]]
		status.text = "结果已整理，可返回学校调整队伍后再次试验。"
		result_panel.show(); canvas.hide()
		if first_summary: return_button.grab_focus()
	if active:
		help_label.text = "左键选人/查看对象 · 右键移动/攻击敌人 · 中键拖图 · 空格暂停 · S停止 · Esc结束试验\n仅试验初始队伍与敌人，不推进正式冒险或发放奖励。"


func toggle_pause() -> void:
	if not session is Combat or session.ending_snapshot()["phase"] != "active": return
	super.toggle_pause()


func close_trial() -> void:
	if not visible or not session is Combat or not session.ready: return
	var phase: String = session.ending_snapshot()["phase"]
	if phase in ["opening","active"]:
		session.request_return()
		_refresh()
	elif phase == "summary":
		_return_to_school()


func _return_to_school() -> void:
	if _handoff_emitted or not visible or not session is Combat: return
	var handoff: Dictionary = session.take_handoff()
	if handoff.is_empty() or handoff.get("successor","") != "school_adventure_preparation": return
	_handoff_emitted = true
	_release_opening()
	session.close()
	canvas.session = null; canvas.texture = null; canvas.sprites.clear(); canvas.labels.clear()
	canvas.controls_enabled = false; canvas.dragging = false; canvas.hover = Vector2i(-1,-1)
	canvas.show_terrain = false; canvas.origin = Vector2.ZERO; canvas.zoom = 1.0; canvas.fit_mode = true
	canvas.inspected_id = -1; inspected_id = -1
	_last_event = -1
	_sprites.clear(); _names.clear(); member_buttons.clear()
	for child in roster.get_children(): child.free()
	result_panel.hide(); result_title.text = ""; result_details.text = ""
	info.text = ""; target_info.text = ""; status.text = ""
	hide()
	closed.emit()


func _input(event: InputEvent) -> void:
	if not visible or not event is InputEventKey or not event.pressed or event.echo: return
	if event.keycode == KEY_ESCAPE:
		close_trial()
	elif session.ending_snapshot()["phase"] == "opening":
		if event.keycode in [KEY_SPACE,KEY_ENTER,KEY_KP_ENTER]: _advance_opening()
		else: return
	elif session.ending_snapshot()["phase"] == "active":
		if event.keycode == KEY_SPACE: toggle_pause()
		elif event.keycode == KEY_S: session.stop(session.selected_id); _refresh()
		else: return
	else: return
	get_viewport().set_input_as_handled()
