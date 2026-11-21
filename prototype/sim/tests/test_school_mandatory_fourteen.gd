extends "res://sim/tests/test_school_mandatory_nine.gd"


func _save() -> Dictionary:
	var saved := super._save()
	var fixtures := Fixtures.new()
	var delta := fixtures._fixture("july_week4_saved_plan")
	assert_eq(saved.state_sha256,delta.parent)
	saved.commands.append({"op":"return_depart"})
	saved.commands.append({"op":"sortie_finish","trace":fixtures._fixture("mandatory_nine_victory_trace").trace})
	for i in range(delta.story_steps):saved.commands.append({"op":"post_next"})
	saved.commands.append_array(delta.after_story)
	saved.rules.merge(delta.rules_added)
	for key in ["version","context","state_sha256"]:saved[key]=delta[key]
	return saved


func _mission() -> Dictionary:
	return {"scene":14,"week":4,"opening_total":787700,"students":[3,4,8,6,2,5,9,1],
		"groups":[0,0,1,2,2,2,3,3],"version":20,"trace":"mandatory_fourteen_victory_trace"}


func _read_and_replan(ui, path: String) -> void:
	var model=ui.model
	var panel=ui.postbattle_panel
	var dated:=Model.Postbattle.SortieWeek.story(4,7)
	assert_eq([dated.pre_week.size(),dated.week_start.size()],[70,21])
	var school: Dictionary=model.read_postbattle().bundle.school
	assert_eq(model.stage(),"post_story")
	assert_eq(school.student_count,10)
	assert_eq(school.student_ids.slice(8,10),[16,17])
	for id in [16,17]:
		assert_eq(school.availability[id],1)
		assert_eq(school.student_ids.count(id),1)
	for page in dated.pre_week:
		assert_eq(model.read_postbattle().page,page)
		assert_eq(page.chapter,304)
		panel.next.pressed.emit()
	assert_eq(model.stage(),"new_week_story")
	var card: Dictionary=model.read_postbattle()
	assert_eq(card.get("date_card",{}).get("image"),"res://assets/school_story/tc0705.png")
	assert_true(panel.card_frame.visible and panel.card_image.texture!=null)
	panel.next.pressed.emit()
	for page in dated.week_start:
		assert_eq(model.read_postbattle().page,page)
		assert_eq(page.chapter,305)
		panel.next.pressed.emit()
	assert_eq(model.stage(),"post_workroom")
	panel.next.pressed.emit()
	assert_eq(model.stage(),"returned_school")
	if model.stage()!="returned_school":return
	var v: Dictionary=model.read_postbattle()
	school=v.bundle.school
	assert_eq([school.month,school.week,school.adventure_gate,school.teacher_count,school.student_count],[7,5,0,4,10])
	assert_eq(Model.Postbattle.Adventures.available(v.planning.ledger).map(func(a):return a.id),[17])
	assert_false(model.execute({"op":"return_select","adventure":14}).supported)
	for entry in [[16,0,1],[17,1,1]]:
		var member=panel.find_child("member_%d"%entry[0],true,false)
		assert_true(member!=null)
		if member==null:return
		assert_true(member.text.contains("格列佛") if entry[0]==16 else (member.text.contains("柏尔德") or member.text.contains("柏爾德")))
		member.pressed.emit()
		panel.assignments.get_child(entry[1]).get_child(2+entry[2]).pressed.emit()
		assert_eq(model.export_save().commands[-1],{"op":"return_move","kind":"student","member_id":entry[0],"target_group":entry[1],"target_slot":entry[2]})
	for group in range(4):
		panel.find_child("mode_%d_1"%group,true,false).pressed.emit()
		var course=panel.find_child("courses_%d"%group,true,false)
		var index: int=course.get_item_index([8,19,27,28][group])
		assert_true(index>0 and not course.disabled)
		if index<=0 or course.disabled:return
		course.item_selected.emit(index)
	var planned: Dictionary=model.read_postbattle().bundle.school
	assert_eq([planned.derived_student_ids[0][1],planned.derived_student_ids[1][1]],[16,17])
	assert_eq(model.export_save().version,20)
	assert_true(model.save_file(path).supported)
	var loaded:=Model.new()
	var receipt:=loaded.load_file(path)
	assert_true(receipt.supported,str(receipt))
	if not receipt.supported:return
	assert_eq(loaded.state(),model.state())
	assert_eq(loaded.export_save(),model.export_save())
	var altered:=loaded.export_save()
	altered.rules.fourteen_battle="changed"
	assert_eq(loaded.restore(altered).get("reason"),"save_rules_changed")
