extends PanelContainer
## Source dialogue and current returned-school data; local Godot presentation.
signal command(value: Dictionary)
signal save_requested
signal load_requested
const Groups := preload("res://sim/school_teacher_group_replay.gd")
var heading: Label
var speaker: Label
var dialogue: Label
var details: Label
var progress: Label
var previous: Button
var next: Button
var skip: Button
var skip_dialog: ConfirmationDialog
var roster: HBoxContainer
var assignments: VBoxContainer
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
	speaker=_label(23);body.add_child(speaker)
	dialogue=_label(22);dialogue.custom_minimum_size.y=220;body.add_child(dialogue)
	details=_label(17);body.add_child(details)
	roster=HBoxContainer.new();body.add_child(roster)
	assignments=VBoxContainer.new();body.add_child(assignments)
	var nav := HBoxContainer.new();column.add_child(nav)
	previous=_button("上一页",func():command.emit({"op":"post_prev"}));nav.add_child(previous)
	progress=_label(16);progress.size_flags_horizontal=Control.SIZE_EXPAND_FILL;nav.add_child(progress)
	skip=_button("跳过本段剧情",func():skip_dialog.popup_centered(Vector2i(460,170)));nav.add_child(skip)
	next=_button("下一页",func():command.emit({"op":"post_next" if _view["phase"] in ["post_story","new_week_story"] else "post_school"}));nav.add_child(next)
	status=_label(15);column.add_child(status)
	skip_dialog=ConfirmationDialog.new();skip_dialog.title="跳过剩余剧情"
	skip_dialog.dialog_text="跳过本段剩余对白。入队、成长和周结算仍会按顺序保留。"
	skip_dialog.ok_button_text="跳过";skip_dialog.cancel_button_text="继续阅读"
	skip_dialog.confirmed.connect(func():command.emit({"op":"post_skip"}));add_child(skip_dialog)
	hide()


func show_state(view: Dictionary, names: Dictionary, message: String) -> void:
	_view=view.duplicate(true);_names=names.duplicate();status.text=message
	var phase: String=view["phase"];var school: Dictionary=view["bundle"]["school"]
	var reading := phase in ["post_story","new_week_story"]
	var returned := phase=="returned_school"
	heading.text="%d月 · 第%d周　｜　%s" % [school["month"],school["week"],"战后剧情" if phase=="post_story" else "新一周" if phase=="new_week_story" else "学校" if returned else "职务室"]
	speaker.text=view["page"]["speaker"] if reading else "已返回学校" if returned else "准备返校"
	dialogue.text=view["page"]["text"] if reading else "法娜已正式加入，可以调整四名学生的编班，并保存当前进度。" if returned else "新一周的剧情已结束。继续返回学校，保留本场战果、成长与法娜的入队记录。"
	dialogue.custom_minimum_size.y=220 if reading else 60
	progress.text="%d / %d · Enter / Space 下一页" % [view["cursor"]+1,view["total"]] if reading else "战果、入队和周结算各执行一次"
	previous.visible=reading;previous.disabled=view["cursor"]==0
	skip.visible=reading;next.visible=not returned
	next.text="下一页" if reading and view["cursor"]+1<view["total"] else "进入下一周" if phase=="post_story" else "前往职务室" if phase=="new_week_story" else "返回学校"
	var inventory: Array=view["bundle"]["item_flags"]
	details.text="教师：%s　学生：%d人　累计战果：%d　已持有道具：%d" % [names.get(101,"老师"),school["student_count"],school["global_total_511c"],inventory.filter(func(v):return (v&1)!=0).size()]
	roster.visible=returned;assignments.visible=returned
	for container in [roster,assignments]:
		for child in container.get_children():
			container.remove_child(child);child.queue_free()
	if returned:
		for profile in school["member_profiles"]:
			var id: int=profile["member_id"]
			var button := _button("%s%s" % [names.get(id,str(id))," · 教师" if id==101 else " · Lv.%d" % profile["level_50"]],func():_selected=id;show_state(_view,_names,status.text))
			button.toggle_mode=true;button.button_pressed=id==_selected;roster.add_child(button)
		for group in range(5):
			var row := HBoxContainer.new();assignments.add_child(row)
			var caption := _label(17);caption.text="%d班" % (group+1);row.add_child(caption)
			var teacher := Groups._word(school["group_raw_bytes"],group*28)
			row.add_child(_button(names.get(teacher,"教师空位"),func():_move(group,-1,true)))
			for slot in range(4):
				var id := Groups._word(school["group_raw_bytes"],group*28+16+slot*2)
				row.add_child(_button(names.get(id,"空位"),func():_move(group,slot,false)))
		var waiting := _label(17);waiting.text="待命："+", ".join(school["idle_student_ids"].map(func(id):return names.get(id,str(id))))
		assignments.add_child(waiting)
		assignments.add_child(_button("移到待命",func():_move(-1,-1,_selected==101)))
		var note := _label(15);note.text="本段已开放成员查看、编班和存档；下一场冒险及授课结算尚未开放。";assignments.add_child(note)
	show()


func _move(group: int, slot: int, teacher: bool) -> void:
	if _selected<0 or (_selected==101)!=teacher: return
	command.emit({"op":"return_move","kind":"teacher" if teacher else "student","member_id":_selected,"target_group":group,"target_slot":slot})


func key(event: InputEventKey) -> void:
	if not visible or skip_dialog.visible or _view["phase"] not in ["post_story","new_week_story"]:return
	if event.keycode in [KEY_ENTER,KEY_SPACE,KEY_RIGHT]:command.emit({"op":"post_next"})
	elif event.keycode==KEY_LEFT:command.emit({"op":"post_prev"})
	else:return
	get_viewport().set_input_as_handled()


static func _button(text: String, action: Callable) -> Button:
	var button := Button.new();button.text=text;button.custom_minimum_size=Vector2(115,40);button.pressed.connect(action);return button


static func _label(size: int) -> Label:
	var label := Label.new();label.add_theme_font_size_override("font_size",size);label.add_theme_color_override("font_color",Color("e7e5d6"));label.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART;return label
