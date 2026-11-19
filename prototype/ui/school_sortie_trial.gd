extends "res://ui/school_field_trial.gd"
const Sortie := preload("res://sim/school_sortie_session.gd")
const Record := preload("res://sim/school_battle_record.gd")
const CombatView := preload("res://ui/school_combat_trial.gd")
var text_panel: PanelContainer
var text_label: Label
var continue_button: Button
var targets: OptionButton
var summary_navigation: HBoxContainer
var summary_page := 0
var previous_page: Button
var next_page: Button
var _finished := false
signal result_confirmed(trace: Dictionary)


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
	summary_navigation=HBoxContainer.new()
	column.add_child(summary_navigation)
	previous_page=_button("上一段",func():summary_page-=1;_refresh())
	next_page=_button("下一段",func():summary_page+=1;_refresh())
	summary_navigation.add_child(previous_page)
	summary_navigation.add_child(next_page)
	continue_button=_button("继续",_continue);column.add_child(continue_button)
	text_panel.hide()


func open_trial(handoff: Dictionary, combat: Dictionary, names: Dictionary) -> bool:
	if not super.open_trial(handoff,combat,names):return false
	var date: Array=handoff["date"]
	_finished=false;summary_page=0;title_label.text="%d月第%d周 · 冒险%d · %s" % [date[0],date[1],session.scene_id,"山地救援" if session.scene_id==7 else "守城" if session.scene_id==8 else "自由训练"]
	targets.clear();targets.add_item("定位任务对象",-1)
	for unit in session.units:
		var id: int=session.unit_key(unit)
		if unit["controllable"]:continue
		_names[id]="%s #%d" % ["塔/泉" if unit["character_id"] in range(387,405) else "宝箱" if unit["character_id"] in [405,406] else "障碍" if unit["character_id"] in range(411,415) else "敌人",1250-id]
		if session.scene_id==7 and id in [1248,1247]:_names[id]="薛莉尔" if id==1248 else "艾尔雪"
		if Sortie._capture_role(unit["character_id"]) or (session.scene_id==7 and id in [1248,1247]):targets.add_item(_names[id],id)
	if session.scene_id==7:
		targets.add_item("会合区域",1)
		targets.add_item("护送终点",2)
	if session.scene_id==17:targets.add_item("撤离区域",0)
	canvas.labels=_names.duplicate(true);_refresh();return true


func _focus_target(id: int) -> void:
	if not session.ready or id<0:return
	var point := Vector2(91*32+16,17*16+8)
	if session.scene_id==7 and id in [1,2]:
		var cells: Array=session.catalog["regions"][str(id)]
		var index: int=cells[cells.size()/2]
		point=Vector2((index%session.field_width)*32+16,(index/session.field_width)*16+8)
	elif id>0:
		var unit: Dictionary=session.find_unit(id)
		if unit.is_empty():return
		point=session.position(unit);canvas.inspected_id=id
	canvas.zoom=1.25;canvas.fit_mode=false;canvas.origin=canvas.size*0.5-point*canvas.zoom;canvas.clamp_origin()


func _refresh() -> void:
	if session.ready and session.scene_id==7 and session.rendezvous:
		for identity in [1248,1247]:
			var unit: Dictionary=session.find_unit(identity)
			var character: int=unit["character_id"]
			if member_buttons.has(character):continue
			var button := _button("",func():session.select(identity);_refresh())
			button.toggle_mode=true
			button.size_flags_horizontal=Control.SIZE_EXPAND_FILL
			button.custom_minimum_size.y=54
			roster.add_child(button)
			member_buttons[character]=button
			_names[character]=_names.get(identity,str(character))
	super._refresh()
	if session.ready and (session.scene_id==7 or session.departure["date"]==[5,5]):
		var leaders: Array=session.departure["prepared"]["rounds"][0]["teacher_ids"]
		info.text=info.text.get_slice("    |",0)+"    |    班级领队："+ "、".join(leaders.map(func(id):return str(_names.get(id,id))))
		if session.rendezvous:
			for identity in [1248,1247]:
				member_buttons[session.find_unit(identity)["character_id"]].set_pressed_no_signal(session.selected_id==identity)
	if text_panel==null or not session.ready:return
	var ending: Dictionary=session.ending_snapshot();var phase: String=ending["phase"]
	summary_navigation.visible=session.scene_id==7 and phase=="summary" and ending["text"].size()>1
	var active := phase=="active";canvas.controls_enabled=active
	for button in [pause_button,stop_button,terrain_button]:button.disabled=not active
	for button in member_buttons.values():button.disabled=not active
	close_button.disabled=phase=="consuming"
	close_button.text="结束本次战斗" if phase in ["active","opening","event20"] else "返回出击记录"
	text_panel.visible=phase in ["opening","event20","summary"]
	if phase=="opening":
		var page: Dictionary=session.opening_snapshot()
		text_label.text="\n".join(page["page"].map(func(r):return r["text"]))
		continue_button.text="开始战斗" if page["page_index"]+1==page["page_count"] else "继续 · %d/%d" % [page["page_index"]+1,page["page_count"]]
	elif phase=="event20":
		text_label.text="\n".join(session._event_pages[session._event_index].map(func(r):return r["text"]))
		continue_button.text="继续 · %d/%d" % [session._event_index+1,session._event_pages.size()]
	elif phase=="summary":
		var lines := []
		var pages: Array=ending["text"]
		if session.scene_id==7 and not pages.is_empty():
			summary_page=clampi(summary_page,0,pages.size()-1)
			previous_page.disabled=summary_page==0
			next_page.disabled=summary_page+1==pages.size()
			for row in pages[summary_page]:lines.append(row["text"])
			lines.append("（%d/%d）" % [summary_page+1,pages.size()])
		else:
			for page in pages:
				for row in page:lines.append(row["text"])
		text_label.text="\n".join(lines) if not lines.is_empty() else "本次战斗已结束。"
		text_label.text+="\n\n任务评价：%s　·　击倒敌人：%d" % [str(ending["summary"]["terminal_choice"].get("tactical_result_selector","中止")),ending["summary"]["defeated_enemies"]]
		continue_button.text="确认战果" if session.ending_sub>=0 else "返回出击记录"
	status.text="已进行 %02d:%02d　·　可行动 %d/%d　·　敌方 %d" % [session.elapsed/3600,(session.elapsed/60)%60,session.controlled_units().filter(func(u):return u["limits"]["hp"]>0).size(),session.controlled_units().size(),session.enemies().size()]
	help_label.text="左键选人 · 右键移动/攻击 · 中键拖图 · 空格暂停 · S停止\n"+("坚守30分钟，保护3处己方基地；靠近基地可占领。" if session.scene_id==8 else "训练后前往东北撤离区；15分钟前撤离获得最低评价。塔、泉与宝箱靠近占领，障碍右键攻击。")
	if session.scene_id==7:
		help_label.text="带学生到东北会合区域寻找薛莉尔。占领两座守卫塔可提高评价。" if not session.rendezvous else "选中薛莉尔，护送她到西南终点。"
	if phase=="summary":
		help_label.text="确认后保存奖励和成长，继续战后剧情。" if session.ending_sub>=0 else "已中止本场，可从保存的出击队伍重新开始。"
	var commands_left: int=Record.MAX_COMMANDS-session._trace.size()
	var ticks_left: int=Record.MAX_SORTIE_TICKS-session._trace_clock
	var exceeded: bool=session._trace_overflow or ticks_left<0
	if exceeded:
		help_label.text="已超出单场存档记录上限。本场可以返回出击记录重开。"
		if phase=="summary": continue_button.text="返回出击记录"
	elif active and (commands_left<=128 or ticks_left<=18000):
		help_label.text="接近存档记录上限：剩余 %d 条操作，%d 秒模拟时间。" % [commands_left,ceili(ticks_left/30.0)]
	canvas.queue_redraw()


func _continue() -> void:
	if not session.ready:return
	if session.ending_snapshot()["phase"]=="opening":session.advance_opening(true);_refresh()
	elif session.ending_snapshot()["phase"]=="event20":session.advance_event();_refresh()
	elif session.ending_snapshot()["phase"]=="summary":
		if session.ending_sub>=0 and not session._trace_overflow and session._trace_clock<=Record.MAX_SORTIE_TICKS:
			result_confirmed.emit(session.battle_trace())
		else: _leave()


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
	elif session.ending_snapshot()["phase"] in ["opening","event20","summary"]:
		if event.keycode in [KEY_SPACE,KEY_ENTER,KEY_KP_ENTER]:_continue()
		else:return
	elif event.keycode==KEY_SPACE:toggle_pause()
	elif event.keycode==KEY_S:session.stop(session.selected_id);_refresh()
	else:return
	get_viewport().set_input_as_handled()
