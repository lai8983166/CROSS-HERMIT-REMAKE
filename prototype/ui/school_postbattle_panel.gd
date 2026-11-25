extends PanelContainer
## Source dialogue and current returned-school data; local Godot presentation.
signal command(value: Dictionary)
signal save_requested
signal load_requested
signal sortie_requested
const JobEligibility := preload("res://sim/school_job_eligibility.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")
const Courses := preload("res://sim/school_return_courses.gd")
const Adventures := preload("res://sim/school_return_adventures.gd")
const COURSE_NAMES := {1:"力量训练",2:"敏捷训练",3:"感知训练",4:"道德训练",5:"智力训练",6:"奉献活动",7:"魔法基础",10:"全面训练",11:"综合研习",12:"身心锻炼"}
var card_frame: AspectRatioContainer
var card_image: TextureRect
var card_wait := 0
var heading: Label
var speaker: Label
var dialogue: Label
var details: Label
var progress: Label
var previous: Button
var next: Button
var skip: Button
var skip_dialog: ConfirmationDialog
var roster: HFlowContainer
var assignments: VBoxContainer
var plans: VBoxContainer
var commit_dialog: ConfirmationDialog
var _pending: Dictionary = {}
var status: Label
var _view: Dictionary = {}
var _names: Dictionary = {}
var _selected := -1


func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	var style := StyleBoxFlat.new();style.bg_color=Color("172b28")
	for side in [SIDE_LEFT,SIDE_RIGHT,SIDE_TOP,SIDE_BOTTOM]:style.set_content_margin(side,24)
	add_theme_stylebox_override("panel",style)
	var column := VBoxContainer.new();column.add_theme_constant_override("separation",14);add_child(column)
	var toolbar := HBoxContainer.new();column.add_child(toolbar)
	heading=_label(24);heading.size_flags_horizontal=Control.SIZE_EXPAND_FILL;toolbar.add_child(heading)
	toolbar.add_child(_button("保存进度",func():save_requested.emit()))
	toolbar.add_child(_button("读取存档",func():load_requested.emit()))
	var scroll := ScrollContainer.new();scroll.size_flags_vertical=Control.SIZE_EXPAND_FILL;column.add_child(scroll)
	var body := VBoxContainer.new();body.size_flags_horizontal=Control.SIZE_EXPAND_FILL;body.add_theme_constant_override("separation",18);scroll.add_child(body)
	card_frame=AspectRatioContainer.new()
	card_frame.ratio=4.0/3.0
	card_frame.custom_minimum_size.y=240
	body.add_child(card_frame)
	var backdrop := ColorRect.new()
	backdrop.color=Color.BLACK
	card_frame.add_child(backdrop)
	card_image=TextureRect.new()
	card_image.expand_mode=TextureRect.EXPAND_IGNORE_SIZE
	backdrop.add_child(card_image)
	card_frame.hide()
	speaker=_label(23);body.add_child(speaker)
	dialogue=_label(22);dialogue.custom_minimum_size.y=220;body.add_child(dialogue)
	details=_label(17);body.add_child(details)
	roster=HFlowContainer.new();body.add_child(roster)
	assignments=VBoxContainer.new();body.add_child(assignments)
	plans=VBoxContainer.new();plans.add_theme_constant_override("separation",12);body.add_child(plans)
	var nav := HBoxContainer.new();column.add_child(nav)
	previous=_button("上一页",func():command.emit({"op":"post_prev"}));nav.add_child(previous)
	progress=_label(16);progress.size_flags_horizontal=Control.SIZE_EXPAND_FILL;nav.add_child(progress)
	skip=_button("跳过本段剧情",func():skip_dialog.popup_centered(Vector2i(460,170)));nav.add_child(skip)
	next=_button("下一页",func():command.emit({"op":"post_next" if _view["phase"] in ["post_story","new_week_story","school_entry_story"] else "post_school"}));nav.add_child(next)
	status=_label(15);column.add_child(status)
	skip_dialog=ConfirmationDialog.new();skip_dialog.title="跳过剩余剧情"
	skip_dialog.dialog_text="跳过本段剩余对白，继续后续剧情与学校流程。"
	skip_dialog.ok_button_text="跳过";skip_dialog.cancel_button_text="继续阅读"
	skip_dialog.confirmed.connect(func():command.emit({"op":"post_skip"}));add_child(skip_dialog)
	commit_dialog=ConfirmationDialog.new();commit_dialog.title="确认本周安排"
	commit_dialog.ok_button_text="确认";commit_dialog.cancel_button_text="继续调整"
	commit_dialog.confirmed.connect(func():
		var pending := _pending.duplicate();_pending.clear()
		if not pending.is_empty():command.emit(pending))
	commit_dialog.canceled.connect(func():_pending.clear())
	add_child(commit_dialog)
	hide()


func show_state(view: Dictionary, names: Dictionary, message: String) -> void:
	_view=view.duplicate(true);_names=names.duplicate();status.text=message
	var phase: String=view["phase"];var school: Dictionary=view["bundle"]["school"]
	var date := "%d月 · 第%d周" % [school["month"],school["week"]]
	var date_card: Dictionary=view.get("date_card",{})
	var reading := date_card.is_empty() and phase in ["post_story","new_week_story","school_entry_story"]
	var returned := phase=="returned_school"
	heading.text="%d月 · 第%d周　｜　%s" % [school["month"],school["week"],"战后剧情" if phase=="post_story" else "新一周" if phase=="new_week_story" else "返校剧情" if phase=="school_entry_story" else "学校" if returned else "职务室"]
	if phase=="post_story" and view.get("planning",{}).has("course_summary"):
		heading.text=date+"　｜　课后剧情"
	speaker.text=view["page"]["speaker"] if reading else "已返回学校" if returned else "准备返校"
	dialogue.text=view["page"]["text"] if reading else "法娜已正式加入，可以调整四名学生的编班，并保存当前进度。" if returned else "新一周的剧情已结束。继续返回学校，保留本场战果、成长与法娜的入队记录。"
	if phase=="post_workroom" and [school.month,school.week]==[8,4]:
		dialogue.text="前往学校，阅读本周的返校剧情。"
	dialogue.custom_minimum_size.y=220 if reading else 60
	progress.text="%d / %d · Enter / Space 下一页" % [view["cursor"]+1,view["total"]] if reading else "战果、入队和周结算各执行一次"
	previous.visible=reading;previous.disabled=view["cursor"]==0
	skip.visible=reading;next.visible=reading or phase=="post_workroom"
	next.text="下一页" if reading and view["cursor"]+1<view["total"] else "进入下一周" if phase=="post_story" else "前往职务室" if phase=="new_week_story" else "返回学校"
	card_wait=int(date_card.get("wait_ticks",0))
	set_process(card_wait>0)
	card_frame.visible=not date_card.is_empty()
	speaker.visible=date_card.is_empty()
	dialogue.visible=date_card.is_empty()
	if card_frame.visible:
		var decoded := Image.new()
		if decoded.load_png_from_buffer(FileAccess.get_file_as_bytes(date_card["image"]))==OK:
			card_image.texture=ImageTexture.create_from_image(decoded)
		var pos: Array=date_card["position"]
		var size_px: Array=date_card["size"]
		var canvas_px: Array=date_card["canvas_size"]
		card_image.anchor_left=float(pos[0])/canvas_px[0]
		card_image.anchor_top=float(pos[1])/canvas_px[1]
		card_image.anchor_right=float(pos[0]+size_px[0])/canvas_px[0]
		card_image.anchor_bottom=float(pos[1]+size_px[1])/canvas_px[1]
		next.visible=true
		next.text="继续剧情" if view.get("story_after_card",false) else "前往职务室"
		progress.text=""
	else:
		card_image.texture=null
	var inventory: Array=view["bundle"]["item_flags"]
	details.text="教师：%s　学生：%d人　累计战果：%d　已持有道具：%d" % [_member_names(school["teacher_ids"].slice(0,school["teacher_count"])),school["student_count"],school["global_total_511c"],inventory.filter(func(v):return (v&1)!=0).size()]
	roster.visible=returned;assignments.visible=returned
	for container in [roster,assignments,plans]:
		for child in container.get_children():
			container.remove_child(child);child.queue_free()
	if returned:
		for profile in school["member_profiles"]:
			var id: int=profile["member_id"]
			var button := _button("%s%s" % [names.get(id,str(id))," · 教师" if _is_teacher(id) else " · Lv.%d" % profile["level_50"]],func():_selected=id;show_state(_view,_names,status.text))
			button.name="member_%d" % id;button.toggle_mode=true;button.button_pressed=id==_selected;roster.add_child(button)
		for group in range(5):
			var row := HBoxContainer.new();assignments.add_child(row)
			var caption := _label(17);caption.text="%d班" % (group+1);row.add_child(caption)
			var teacher := Groups._word(school["group_raw_bytes"],group*28)
			row.add_child(_button(names.get(teacher,"教师空位"),func():_move(group,-1,true)))
			for slot in range(4):
				var id := Groups._word(school["group_raw_bytes"],group*28+16+slot*2)
				row.add_child(_button(names.get(id,"空位"),func():_move(group,slot,false)))
		if school.month >= 10 and _selected > 0 and not _is_teacher(_selected):
			var menu := JobEligibility.menu_data()
			var students: Array = view.bundle.participants.filter(func(student):return student.character_id==_selected)
			if not menu.is_empty() and not students.is_empty():
				var jobs := JobEligibility.calculate_eligibility(students[0],menu)
				var picker := OptionButton.new()
				picker.name="eligible_jobs"
				for job in jobs:
					picker.add_item(menu.names[job],job)
					if job==students[0].job:picker.select(picker.item_count-1)
				var choices := HBoxContainer.new()
				assignments.add_child(choices)
				var caption := _label(17)
				caption.text="已解锁职业"
				choices.add_child(caption)
				choices.add_child(picker)
				var change := _button("确认转职",func():
					var target := picker.get_selected_id()
					_confirm("return_job","将职业改为%s？已装备的技能和物品将卸下。"%menu.names[target],{"member":_selected,"job":target}))
				change.name="change_job"
				change.disabled=picker.get_selected_id()==students[0].job or picker.item_count==0
				picker.item_selected.connect(func(_index):change.disabled=picker.get_selected_id()==students[0].job)
				choices.add_child(change)
		var waiting := _label(17);waiting.text="待命："+", ".join((school["idle_teacher_ids"]+school["idle_student_ids"]).map(func(id):return names.get(id,str(id))))
		assignments.add_child(waiting)
		var to_wait := _button("移到待命",func():_move(-1,-1,_is_teacher(_selected)))
		to_wait.name="move_to_waiting";assignments.add_child(to_wait)
		if not view.has("planning"):
			var button := _button("继续安排本周",func():command.emit({"op":"return_plan"}))
			button.name="plan_start";plans.add_child(button)
	if school["month"]>5 or (school["month"]==5 and school["week"]>=2):
		if phase=="post_workroom":
			dialogue.text="本周的剧情已结束。返回学校后可以查看队伍成长，并安排本周活动。"
			progress.text="本周成长与换周记录已保留"
			if [school["month"],school["week"]] in [[5,4],[6,2]]: next.text="继续返校剧情"
		elif returned:
			progress.text="当前编班和本周安排可随时保存"
	if view.has("planning"):_show_plan(view)
	show()


func _process(_delta: float) -> void:
	if not is_visible_in_tree() or card_wait<=0:return
	card_wait-=1
	if card_wait==0:command.emit({"op":"post_next"})


func _show_plan(view: Dictionary) -> void:
	var phase: String=view["phase"];var bundle: Dictionary=view["bundle"]
	var plan: Dictionary=view["planning"];var school: Dictionary=bundle["school"]
	var date := "%d月 · 第%d周" % [school["month"],school["week"]]
	if phase=="sortie_result":
		var summary: Dictionary=plan["sortie_summary"]
		heading.text=date+"　｜　冒险%d战果" % summary["scene_id"]
		speaker.text="本场最佳："+_names.get(summary["recipient"],str(summary["recipient"]))
		dialogue.text="新增战果 %d　｜　累计 %d" % [summary["score"]["total_delta"],summary["score"]["total_after"]]
		var items := []
		for group in summary["loot_groups"]:
			for item in group:
				if item>0: items.append(str(item))
		progress.text="本场评价 %d　｜　获得道具：%s" % [summary["result_selector"],"、".join(items) if not items.is_empty() else "无"]
		for student in summary["students"]:
			var row := _label(18)
			row.text="%s　Lv.%d → %d　能力 %s → %s" % [_names.get(student["character_id"],str(student["character_id"])),student["before_level"],student["level"],student["before_attributes"],student["attributes"]]
			plans.add_child(row)
		if summary.has("lessons") and not summary["lessons"]["students"].is_empty():
			speaker.text="本周最佳："+_names.get(summary["recipient"],str(summary["recipient"]))
			dialogue.text="出击战果 %d　｜　授课奖励 %d　｜　累计 %d" % [summary["score"]["total_delta"],summary["lessons"]["bonus"],bundle["school"]["global_total_511c"]]
			for student in summary["lessons"]["students"]:
				var row := _label(18)
				row.text="%s　课程%d　Lv.%d → %d　能力 %s → %s" % [_names.get(student["character_id"],str(student["character_id"])),student["work_id"],student["before_level"],student["level"],student["before_attributes"],student["attributes"]]
				plans.add_child(row)
		var proceed := _button("继续战后剧情",func():command.emit({"op":"post_next"}))
		proceed.name="continue_sortie_story"
		plans.add_child(proceed)
		return
	if phase=="course_result":
		heading.text=date+"　｜　授课结算"
		speaker.text="本周授课已结算"
		dialogue.text="成长、技能和本周最佳已记录。继续课后剧情即可进入下一周。"
		progress.text="本周不能再次授课或出击；可保存结果，或读取提交前的备份。"
		var summary: Dictionary=plan["course_summary"]
		var best := _label(21);best.text="本周最佳：%s　·　新增总战果：%d" % [_names.get(summary["recipient"],"无"),summary["bonus"]];plans.add_child(best)
		for row in summary["students"]:
			var label := _label(18)
			label.text="%s　%s　Lv.%d → %d\n能力：%s → %s　·　新技能：%d项" % [_names.get(row["character_id"],""),COURSE_NAMES.get(row["work_id"],"课程%d" % row["work_id"]),row["before_level"],row["level"],str(row["before_attributes"]),str(row["attributes"]),row["new_skill_ids"].size()]
			plans.add_child(label)
		var proceed := _button("继续课后剧情",func():command.emit({"op":"course_story"}))
		proceed.name="continue_course_story"
		plans.add_child(proceed)
		return
	if phase=="sortie_pending":
		var handoff: Dictionary=plan["handoff"];var prepared: Dictionary=handoff["prepared"]
		heading.text=date+"　｜　出击交接"
		speaker.text="冒险%d · 出击交接完成" % prepared["adventure_id"]
		dialogue.text="出击队伍与成长已保存，可以进入本次任务的战场。"
		progress.text="完成目标后确认战果，即可继续剧情。单场存档支持 4096 条操作和 120 分钟模拟时间。"
		var label := _label(20)
		label.text="场景%d　｜　带队：%s\n参战：%s\n待命：%s" % [prepared["rounds"][0]["scene_id"],_member_names(prepared["rounds"][0]["teacher_ids"]),_member_names(prepared["rounds"][0]["student_ids"]),_member_names(handoff["idle_student_ids"])]
		plans.add_child(label)
		var play := _button("进入战场",func():sortie_requested.emit());play.name="play_sortie";plans.add_child(play)
		return
	if phase!="returned_school":return
	var planning_only: bool=[school["month"],school["week"]]==[11,2]
	var mandatory: bool=school["adventure_gate"]!=0
	dialogue.text="安排本周授课，或选择冒险并提交出击队伍。每班本周只能执行一种安排。"
	progress.text="可调整编班与课程并保存安排。" if planning_only else "课程与出击准备均可存档；选择仍开放的冒险，提交后即可进入对应战场。"
	if planning_only:
		dialogue.text="11 月第 2 周可调整编班与课表。"
		progress.text="调整后可保存本周安排。"
	elif school.month==9 and school.week in [1,2,5] or school.month==10 or [school.month,school.week]==[11,1]:
		dialogue.text="核对五个班的课表后，确认本周授课即可结算并进入下周剧情。"
		progress.text="可调整编班和课程，保存后继续。"
	elif [school.month,school.week]==[8,5]:
		dialogue.text="选择冒险 35，把要出击的班设为冒险。其他班按课表授课。"
	elif school.month==8 and school.week==1:
		dialogue.text="确认四个班的课程后，即可结算并进入下周剧情。"
		progress.text="本周可重新排课并保存。"
	elif mandatory and school["month"] in [6,7,8,9]:
		dialogue.text="%d 月第 %d 周为必修冒险 %d。确认已保存的出击编班后即可进入战场。" % [school["month"],school["week"],school["lecture_work_fields"][2]]
	elif mandatory:
		dialogue.text="奎丝忒和帕佩修已加入。第4周为必修冒险7，确认已保存的出击编班后即可进入战场。"
	for group in range(5):
		if Groups._word(school["group_raw_bytes"],group*28)<0:continue
		var row := HBoxContainer.new();plans.add_child(row)
		var caption := _label(17);caption.text="%d班安排" % (group+1);row.add_child(caption)
		for teaching in [true,false]:
			var button := _button("授课" if teaching else "冒险",func():command.emit({"op":"return_mode","group":group,"teaching":teaching}))
			button.name="mode_%d_%d" % [group,int(teaching)];button.toggle_mode=true
			button.disabled=mandatory
			button.button_pressed=bool(school["group_raw_bytes"][group*28+3])==teaching;row.add_child(button)
		var options := OptionButton.new();options.name="courses_%d" % group;options.custom_minimum_size=Vector2(180,40)
		options.add_item("选择课程",-1)
		var list := Courses.list_courses(bundle,group)
		if list["supported"]:
			for category in list["courses"]:
				for course in category:
					options.add_item(COURSE_NAMES.get(course[1],"课程%d" % course[1]),course[1])
					if Groups._word(school["group_raw_bytes"],group*28+10)==course[1]:options.select(options.item_count-1)
		options.disabled=school["group_raw_bytes"][group*28+3]!=1
		options.item_selected.connect(func(index):
			var id := options.get_item_id(index)
			if id>0:command.emit({"op":"return_course","group":group,"course":id}))
		row.add_child(options)
	var caption := _label(19);caption.text="本周必修冒险" if mandatory else "本周可选冒险";plans.add_child(caption)
	for adventure in Adventures.available(plan["ledger"]):
		var id: int=adventure["id"]
		if mandatory and id!=school["lecture_work_fields"][2]: continue
		var label: String={4:"必修 · 冒险4",6:"必修 · 冒险6",7:"必修 · 冒险7",8:"守城 · 冒险8",9:"必修 · 冒险9",10:"必修 · 冒险10",11:"冒险11",13:"必修 · 冒险13",14:"必修 · 冒险14",17:"自由训练 · 冒险17",18:"限时 · 冒险18",20:"必修 · 冒险20",21:"必修 · 冒险21",22:"必修 · 冒险22",24:"必修 · 冒险24",35:"石像训练 · 冒险35"}.get(id,"冒险%d" % id)
		label+="　剩余%d周" % adventure["remaining"] if adventure["remaining"]>0 else "　无期限"
		var button := _button(label,func():command.emit({"op":"return_select","adventure":id}))
		button.name="adventure_%d" % id;button.toggle_mode=true
		button.disabled=mandatory
		button.button_pressed=school["lecture_active"]==1 and school["lecture_work_fields"][2]==id;plans.add_child(button)
	if planning_only: return
	var row := HBoxContainer.new();plans.add_child(row)
	var settle := _button("确认本周授课",func():_confirm("return_settle","确认后结算本周授课，保留成长、技能与成员记录。本周不能再出击。"))
	settle.name="settle";row.add_child(settle);settle.visible=not mandatory and [school.month,school.week]!=[8,5]
	var ratings := Groups.rate(school,Courses.Return.group_rules(school))
	settle.disabled=not ratings["supported"] or not ratings["ratings"].any(func(r):return r["state"]==4) or ratings["ratings"].any(func(r):return r["state"] not in [0,4])
	if school["week"]==5 and school.month!=8 and ratings["supported"] and ratings["ratings"].any(func(r):return r["state"]==3):
		progress.text="有班级设为冒险但尚未选择任务。要全校授课，请将该班切换为授课并确认课程；也可选择冒险，让其余班级照常上课。"

	if school.month==10 or [school.month,school.week] in [[8,1],[9,1],[9,2],[9,5],[11,1]]:return
	var depart := _button("确认出击交接",func():_confirm("return_depart","确认后锁定本周出击队伍并更新冒险使用记录，随后可进入战场。可以保存出击记录后稍后继续。"))
	depart.name="depart";row.add_child(depart)
	var prepared := Adventures.prepare(bundle,plan["ledger"])
	depart.disabled=not prepared["supported"]
	var ready := _label(16)
	ready.text="出击队伍："+_member_names(prepared["prepared"]["rounds"][0]["student_ids"]) if prepared["supported"] else "出击前请选择冒险，并将有学生的教师班设为冒险。"
	if prepared.get("reason")=="unsupported_training_student_13":
		ready.text="攸莉目前可上课或待命。调整她的安排后即可出击训练。"
	plans.add_child(ready)


func _confirm(op: String, message: String, fields: Dictionary = {}) -> void:
	_pending=fields.duplicate();_pending["op"]=op;commit_dialog.dialog_text=message;commit_dialog.popup_centered(Vector2i(520,190))


func _member_names(ids: Array) -> String:
	return "、".join(ids.map(func(id):return _names.get(id,str(id)))) if not ids.is_empty() else "无"


func _is_teacher(id: int) -> bool:
	var school: Dictionary=_view["bundle"]["school"]
	return school["teacher_ids"].slice(0,school["teacher_count"]).has(id)


func _move(group: int, slot: int, teacher: bool) -> void:
	if _selected<0 or (_is_teacher(_selected))!=teacher: return
	command.emit({"op":"return_move","kind":"teacher" if teacher else "student","member_id":_selected,"target_group":group,"target_slot":slot})


func key(event: InputEventKey) -> void:
	if not visible or skip_dialog.visible or _view["phase"] not in ["post_story","new_week_story","school_entry_story"]:return
	if event.keycode in [KEY_ENTER,KEY_SPACE,KEY_RIGHT]:command.emit({"op":"post_next"})
	elif event.keycode==KEY_LEFT:command.emit({"op":"post_prev"})
	else:return
	get_viewport().set_input_as_handled()


static func _button(text: String, action: Callable) -> Button:
	var button := Button.new();button.text=text;button.custom_minimum_size=Vector2(115,40);button.pressed.connect(action);return button


static func _label(size: int) -> Label:
	var label := Label.new();label.add_theme_font_size_override("font_size",size);label.add_theme_color_override("font_color",Color("e7e5d6"));label.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART;return label
