extends "res://ui/school_field_trial.gd"
const Sortie := preload("res://sim/school_sortie_session.gd")
const CombatView := preload("res://ui/school_combat_trial.gd")
var text_panel: PanelContainer
var text_label: Label
var continue_button: Button
var targets: OptionButton
var _finished := false


func _new_session():return Sortie.new()


func _new_canvas() -> FieldCanvas:return CombatView.CombatCanvas.new()


func _ready() -> void:
	super._ready()
	targets=OptionButton.new();targets.custom_minimum_size=Vector2(170,36)
	center_button.get_parent().add_child(targets)
	targets.item_selected.connect(func(index):_focus_target(targets.get_item_id(index)))
	text_panel=PanelContainer.new();canvas.get_parent().add_child(text_panel)
	var column := VBoxContainer.new();text_panel.add_child(column)
	text_label=Label.new();text_label.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	text_label.add_theme_font_size_override("font_size",20);column.add_child(text_label)
	continue_button=_button("继续",_continue);column.add_child(continue_button)
	text_panel.hide()


func open_trial(handoff: Dictionary, combat: Dictionary, names: Dictionary) -> bool:
	if not super.open_trial(handoff,combat,names):return false
	_finished=false;title_label.text="5月第1周 · 冒险%d · %s" % [session.scene_id,"守城" if session.scene_id==8 else "自由训练"]
	targets.clear();targets.add_item("定位任务对象",-1)
	for unit in session.units:
		var id: int=session.unit_key(unit)
		if unit["controllable"]:continue
		_names[id]="%s #%d" % ["塔/泉" if unit["character_id"] in range(387,405) else "宝箱" if unit["character_id"] in [405,406] else "障碍" if unit["character_id"] in range(411,415) else "敌人",1250-id]
		if Sortie._capture_role(unit["character_id"]):targets.add_item(_names[id],id)
	if session.scene_id==17:targets.add_item("撤离区域",0)
	canvas.labels=_names.duplicate(true);_refresh();return true


func _focus_target(id: int) -> void:
	if not session.ready or id<0:return
	var point := Vector2(91*32+16,17*16+8)
	if id>0:
		var unit: Dictionary=session.find_unit(id)
		if unit.is_empty():return
		point=session.position(unit);canvas.inspected_id=id
	canvas.zoom=1.25;canvas.fit_mode=false;canvas.origin=canvas.size*0.5-point*canvas.zoom;canvas.clamp_origin()


func _refresh() -> void:
	super._refresh()
	if text_panel==null or not session.ready:return
	var ending: Dictionary=session.ending_snapshot();var phase: String=ending["phase"]
	var active := phase=="active";canvas.controls_enabled=active
	for button in [pause_button,stop_button,terrain_button]:button.disabled=not active
	for button in member_buttons.values():button.disabled=not active
	close_button.disabled=phase=="consuming"
	close_button.text="结束本次战斗" if phase in ["active","opening"] else "返回出击记录"
	text_panel.visible=phase in ["opening","summary"]
	if phase=="opening":
		var page: Dictionary=session.opening_snapshot()
		text_label.text="\n".join(page["page"].map(func(r):return r["text"]))
		continue_button.text="开始战斗" if page["page_index"]+1==page["page_count"] else "继续 · %d/%d" % [page["page_index"]+1,page["page_count"]]
	elif phase=="summary":
		var lines := []
		for page in ending["text"]:
			for row in page:lines.append(row["text"])
		text_label.text="\n".join(lines) if not lines.is_empty() else "本次战斗已结束。"
		text_label.text+="\n\n任务评价：%s　·　击倒敌人：%d" % [str(ending["summary"]["terminal_choice"].get("tactical_result_selector","中止")),ending["summary"]["defeated_enemies"]]
		continue_button.text="返回出击记录"
	status.text="已进行 %02d:%02d　·　可行动 %d/%d　·　敌方 %d" % [session.elapsed/3600,(session.elapsed/60)%60,session.controlled_units().filter(func(u):return u["limits"]["hp"]>0).size(),session.controlled_units().size(),session.enemies().size()]
	help_label.text="左键选人 · 右键移动/攻击 · 中键拖图 · 空格暂停 · S停止\n"+("坚守30分钟，保护3处己方基地；靠近基地可占领。" if session.scene_id==8 else "训练后前往东北撤离区；15分钟前撤离获得最低评价。塔、泉与宝箱靠近占领，障碍右键攻击。")
	if phase=="summary":help_label.text="本次结果保留在结果页；新战果结算与战后周推进尚未接入。返回后可从已保存的出击队伍重新开始。"
	canvas.queue_redraw()


func _continue() -> void:
	if not session.ready:return
	if session.ending_snapshot()["phase"]=="opening":session.advance_opening(true);_refresh()
	elif session.ending_snapshot()["phase"]=="summary":_leave()


func _leave() -> void:
	if _finished:return
	_finished=true;session.close();canvas.session=null;canvas.texture=null;canvas.sprites.clear();canvas.labels.clear()
	_sprites.clear();_names.clear();member_buttons.clear()
	for child in roster.get_children():child.free()
	text_panel.hide();hide();closed.emit()


func close_trial() -> void:
	if not visible or not session.ready:return
	if session.ending_snapshot()["phase"]=="summary":_leave()
	else:session.request_return();_refresh()


func toggle_pause() -> void:
	if session.ready and session.ending_snapshot()["phase"]=="active":super.toggle_pause()


func _input(event: InputEvent) -> void:
	if not visible or not event is InputEventKey or not event.pressed or event.echo:return
	if event.keycode==KEY_ESCAPE:close_trial()
	elif session.ending_snapshot()["phase"] in ["opening","summary"]:
		if event.keycode in [KEY_SPACE,KEY_ENTER,KEY_KP_ENTER]:_continue()
		else:return
	elif event.keycode==KEY_SPACE:toggle_pause()
	elif event.keycode==KEY_S:session.stop(session.selected_id);_refresh()
	else:return
	get_viewport().set_input_as_handled()
