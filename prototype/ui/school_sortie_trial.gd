extends "res://ui/school_field_trial.gd"
const Sortie := preload("res://sim/school_sortie_session.gd")
const Record := preload("res://sim/school_battle_record.gd")
const CombatView := preload("res://ui/school_combat_trial.gd")
var text_panel: PanelContainer
var text_label: Label
var continue_button: Button
var spell_choice: OptionButton
var targets: OptionButton
var summary_navigation: HBoxContainer
var summary_page := 0
var previous_page: Button
var next_page: Button
var _finished := false
signal result_confirmed(trace: Dictionary)


func _skin_overrides(next: Field) -> Variant:
	if next.get("scene_id")!=22:return {}
	var raw:=FileAccess.get_file_as_string("res://assets/school_twenty_two_actions/catalog.json").replace("\r\n","\n")
	if raw.sha256_text()!="cf4a75758957a53121500e14428f96a4883b6f61228f86f4891ab6c721f67e20":return null
	var delta: Dictionary=Sortie.Limits._source_numbers(JSON.parse_string(raw))
	var result:={}
	for key in delta:
		var skin: Dictionary=next.catalog.skins[key].duplicate(true)
		skin.actions.merge(delta[key].actions)
		skin.frames.merge(delta[key].frames)
		result[key]=skin
	return result


func _new_session():return Sortie.new()


func _new_canvas() -> FieldCanvas:return CombatView.CombatCanvas.new()


func _ready() -> void:
	super._ready()
	spell_choice=OptionButton.new()
	spell_choice.add_item("移动／普通攻击",0)
	spell_choice.add_item("雷击术 · 75 MP",59)
	spell_choice.add_item("气流障壁 · 15 MP",57)
	center_button.get_parent().add_child(spell_choice)
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
	if session.scene_id in [21,22,24,35] and spell_choice.get_item_index(31)<0:spell_choice.add_item("治愈 · 30 MP",31)
	elif session.scene_id not in [21,22,24,35] and spell_choice.get_item_index(31)>=0:spell_choice.remove_item(spell_choice.get_item_index(31))
	if session.scene_id in [22,24,35] and spell_choice.get_item_index(11)<0:spell_choice.add_item("空壓斬 · 35 MP",11)
	elif session.scene_id not in [22,24,35] and spell_choice.get_item_index(11)>=0:spell_choice.remove_item(spell_choice.get_item_index(11))
	if session.scene_id in [22,24,35] and spell_choice.get_item_index(20)<0:spell_choice.add_item("毒箭 · 30 MP",20)
	elif session.scene_id not in [22,24,35] and spell_choice.get_item_index(20)>=0:spell_choice.remove_item(spell_choice.get_item_index(20))
	var date: Array=handoff["date"]
	_finished=false;summary_page=0;title_label.text="%d月第%d周 · 冒险%d · %s" % [date[0],date[1],session.scene_id,"安蒂米昂避難救援" if session.scene_id==24 else "中央守護塔爭奪戰" if session.scene_id==22 else "计时训练" if session.scene_id==35 else "安蒂米昂守護塔與聖者之泉" if session.scene_id==21 else "古雷納汀的封印" if session.scene_id==20 else "地下城砦－貝倫" if session.scene_id==14 else "攸利亞守護塔" if session.scene_id==9 else "達雷西昂攻城演習" if session.scene_id==18 else "石碑與祈禱" if session.scene_id==13 else "法爾德長老護送" if session.scene_id==10 else "討伐班奇涅爾" if session.scene_id==6 else "尤安瀑布殲滅戰" if session.scene_id==4 else "山地救援" if session.scene_id==7 else "守城" if session.scene_id==8 else "自由训练"]
	targets.clear();targets.add_item("定位任务对象",-1)
	for unit in session.units:
		var id: int=session.unit_key(unit)
		if unit["controllable"]:continue
		_names[id]="%s #%d" % ["塔/泉" if unit["character_id"] in range(387,405) else "宝箱" if unit["character_id"] in [405,406] else "障碍" if unit["character_id"] in range(411,415) else "敌人",1250-id]
		if session.scene_id==35:_names[id]="训练石像 #%d" % [1250-id]
		if session.scene_id==7 and id in [1248,1247]:_names[id]="薛莉尔" if id==1248 else "艾尔雪"
		if session.scene_id in [21,22,24] and unit.character_id in [388,394]:
			_names[id]=("%s #%d" % ["守護塔" if unit.character_id==388 else "聖者之泉",1250-id])
		if session.scene_id==24 and id in [1241,1240]:_names[id]="避难者 #%d" % (1250-id)
		if session.scene_id==20 and id==1244:_names[id]="匍伏蔓延而來之物"
		if session.scene_id==6 and id==1245:_names[id]="燈火的盾衛－班奇涅爾"
		if session.scene_id==10 and id==1249:_names[id]="法爾德長老"
		if (session.scene_id==24 and id in [1241,1240]) or (session.scene_id==20 and id in range(1244,1250)) or (session.scene_id==10 and id==1249) or (session.scene_id==6 and id==1245) or (session.scene_id in [4,22,24,35] and unit["category"]==5) or Sortie._capture_role(unit["character_id"]) or (session.scene_id==7 and id in [1248,1247]):targets.add_item(_names[id],id)
	if session.scene_id==24:targets.add_item("避难区域",1)
	if session.scene_id==13:
		for n in range(1,10):targets.add_item("石碑 %d" % n if n<=3 else "祈祷点 %d" % n,n)
	if session.scene_id==10:
		for n in range(1,7):targets.add_item("护送停靠区 %d" % n,n)
	if session.scene_id==7:
		targets.add_item("会合区域",1)
		targets.add_item("护送终点",2)
	if session.scene_id==14:targets.add_item("地下城砦出口",1)
	if session.scene_id==17:targets.add_item("撤离区域",0)
	canvas.labels=_names.duplicate(true);_refresh();return true


func _command_cell(cell: Vector2i) -> bool:
	var skill := spell_choice.get_selected_id()
	if skill>0:
		var accepted: bool=session.cast_field_spell(session.selected_id,cell,skill)
		if accepted:spell_choice.select(0)
		return accepted
	return super._command_cell(cell)


func _focus_target(id: int) -> void:
	if not session.ready or id<0:return
	var point := Vector2(91*32+16,17*16+8)
	if (session.scene_id in [14,24] and id==1) or (session.scene_id==7 and id in [1,2]) or (session.scene_id==10 and id in range(1,7)) or (session.scene_id==13 and id in range(1,10)):
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
	if session.ready and (session.scene_id==7 or session.departure["date"] in [[5,5],[6,1],[6,2],[6,3],[6,4],[6,5],[7,1],[7,2],[7,3],[7,4],[7,5],[8,2],[8,3],[8,5],[9,3],[9,4]]):
		var leaders: Array=session.departure["prepared"]["rounds"][0]["teacher_ids"]
		info.text=info.text.get_slice("    |",0)+"    |    班级领队："+ "、".join(leaders.map(func(id):return str(_names.get(id,id))))
		if session.rendezvous:
			for identity in [1248,1247]:
				member_buttons[session.find_unit(identity)["character_id"]].set_pressed_no_signal(session.selected_id==identity)
	if text_panel==null or not session.ready:return
	var ending: Dictionary=session.ending_snapshot();var phase: String=ending["phase"]
	var paged_summary: bool = session.scene_id in [4,6,7,9,10,13,14,17,18,20,21,22,24,35]
	summary_navigation.visible=paged_summary and phase=="summary" and ending["text"].size()>1
	spell_choice.visible=session.scene_id in [4,6,9,10,13,14,18,20,21,22,24,35]
	for option in range(1,spell_choice.item_count):
		spell_choice.set_item_disabled(option,not session.can_cast_spell(session.selected_id,spell_choice.get_item_id(option)))
	if spell_choice.is_item_disabled(spell_choice.selected):spell_choice.select(0)
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
		if paged_summary and not pages.is_empty():
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
	if session.scene_id==10:
		var elder: Dictionary=session.find_unit(1249)
		status.text+="　·　长老 HP %d/%d" % [elder.limits.hp,elder.limits.hp_max]
		if session.escort_route.enabled_region>0:status.text+="　·　前往停靠区 %d" % session.escort_route.enabled_region
	help_label.text="左键选人 · 右键移动/攻击 · 中键拖图 · 空格暂停 · S停止\n"+("坚守30分钟，保护3处己方基地；靠近基地可占领。" if session.scene_id==8 else "训练后前往东北撤离区；15分钟前撤离获得最低评价。塔、泉与宝箱靠近占领，障碍右键攻击。")
	if session.scene_id==35:
		help_label.text="击破全部36尊石像。石像不会反击，三、五、十分钟决定评价；超过十分钟仍可完成。"
	elif session.scene_id==24:
		var rescue:=session.siege as Sortie.TwentyFour
		help_label.text="前往西南避难区寻找克莉丝汀与艾克索。" if not rescue.rescued else "保护两名避难者，击败东北的两只怪物。守住两座塔和三处泉可提高评价。"
		if rescue.rescued:
			for id in [1194,1193]:
				if targets.get_item_index(id)<0 and not session.find_unit(id).is_empty():
					_names[id]="薩魯德斯 #%d" % (1250-id)
					targets.add_item(_names[id],id)
					canvas.labels[id]=_names[id]
	elif session.scene_id==22:
		status.text+="　·　中央守护塔："+("己方" if session.find_unit(1248).side==0 else "敌方" if session.find_unit(1248).side==5 else "中立")
		help_label.text="十分钟结束时占有中央守护塔，或提前击倒五名对手。五分钟内全灭敌方可提高评价。"
	elif session.scene_id==21:
		status.text+="　·　塔 %d/4　泉 %d/13　·　连续守备 %02d:%02d / 15:00" % [session.siege.owned[0],session.siege.owned[1],session.siege.hold/3600,(session.siege.hold/60)%60]
		help_label.text="占领至少两座塔和四处圣者之泉，连续守住十五分钟。留意桥上的增援，失守会重置计时。"
	elif session.scene_id==20:
		var boss: Dictionary=session.find_unit(1244)
		status.text+="　·　封印 HP %d/%d" % [boss.limits.hp,boss.limits.hp_max]
		help_label.text="击倒中央的「匍伏蔓延而來之物」。守住两座塔、一处泉和两扇门，可提高评价。"
	elif session.scene_id==14:
		help_label.text="带任一学生进入西南出口。十分钟内撤出可提高评价，沿途可占领三个宝箱。"
	elif session.scene_id==9:
		if session.knight_released and targets.get_item_index(1203)<0:
			_names[1203]="赤铜骑士邬尔戈"
			targets.add_item(_names[1203],1203)
			canvas.labels[1203]=_names[1203]
		var count: int=[1205,1204].filter(func(id):return session.find_unit(id).side==0).size()
		status.text+="　·　南部守护塔 %d/2" % count
		help_label.text="三十分钟内同时夺回南部两座守护塔（#45、#46），再击倒赤铜骑士。"
	elif session.scene_id==18:
		status.text+="　·　守护塔与圣者之泉 %d/3" % session.castle.owned(session)
		help_label.text="靠近城内两座守护塔和圣者之泉，保持人数优势直至三处变蓝。摧毁城门可阻止部分增援。"
	elif session.scene_id==13:
		status.text+="　·　石碑 %d/3　就位 %d/6　祈祷 %d/300" % [session.prayer.discovered.size(),session.prayer.occupied,session.prayer.duration]
		help_label.text="踏入三处石碑后同步站定六处祈祷点。4号需近战，5、6号需施法者，7至9号任意学生。限时二十分钟。"
	elif session.scene_id==4:
		help_label.text="十分钟内消灭全部敌人。优先击破召唤者，靠近宝箱可以占领。"
	elif session.scene_id==10:
		help_label.text="沿途保护法尔德长老前往六处停靠区。控制六处泉可提高评价。"
	elif session.scene_id==6:
		help_label.text="击败敌方首领班奇涅尔。控制四座塔和泉并歼灭其余敌人可提高评价。"
	elif session.scene_id==7:
		help_label.text="带学生到东北会合区域寻找薛莉尔。占领两座守卫塔可提高评价。" if not session.rendezvous else "选中薛莉尔，护送她到西南终点。"
	if session._normal_healer(session.find_unit(session.selected_id)):help_label.text="右键受伤的友军进行普通治疗，也可以指定敌人攻击。"
	if spell_choice.get_selected_id()==20:help_label.text="右键指定射程内的敌人。毒箭命中后可使目标持续损失体力。"
	elif spell_choice.get_selected_id()==11:help_label.text="右键指定敌人，以远距物理攻击造成伤害。消耗35 MP，射程随敏捷增加。"
	elif spell_choice.get_selected_id()==59:help_label.text="右键指定雷击中心。射程18格，消耗75 MP。"
	elif spell_choice.get_selected_id()==31:help_label.text="右键指定治愈中心。射程8格，消耗30 MP，恢复范围内友方的体力。"
	elif spell_choice.get_selected_id()==57:help_label.text="右键指定障壁中心。射程10格，消耗15 MP。"
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
	_finished=true;session.close();canvas.session=null;canvas.texture=null;canvas.sprites.clear();canvas.labels.clear();canvas.skin_overrides.clear()
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
