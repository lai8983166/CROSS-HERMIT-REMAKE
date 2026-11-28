extends "res://sim/standalone_battle_session.gd"
## Standalone battle tutorial. Its fixed student record comes from 452CF0.
const DATA := "res://assets/tutorial_eighty/catalog.json"
const DATA_SHA := "24a4728d79b5b73432a3c15b58357f2760d55c5de2037107c1a2db8f3743b705"
var lesson := 0

func start() -> bool:
	var raw := FileAccess.get_file_as_string(DATA).replace("\r\n","\n")
	if raw.sha256_text()!=DATA_SHA:return false
	var source: Dictionary=Limits._source_numbers(JSON.parse_string(raw))
	close()
	scene_id=80
	catalog=source.scenes["80"]
	catalog.skins=source.skins
	combat_rules=source.attack_rules
	_open_terrain()
	for actor in catalog.actors:reserves[actor.instance_id]=actor
	var player: Dictionary=catalog.solo_player
	var unit := _actor_unit(player,Vector2i(catalog.origin[0],catalog.origin[1]))
	unit.controllable=true
	var record := String(player.record_hex).hex_decode()
	unit.input={"character_id":player.character_id,"level":record[14],"attributes":Array(record.slice(4,11)),
		"equipped_skills":[record.decode_u16(0x84)]}
	units.append(unit)
	selected_id=player.character_id
	_participant_ids=[selected_id]
	_battle_stats[selected_id]={"character_id":selected_id,"count_field_aa":0,"contribution_field_ac":0,"status_field_ae":0}
	scene_scripts=catalog.scripts
	_opening_pages=_pages(1)
	_opening_index=0
	_ending_phase="opening"
	ready=true
	reason="opening"
	lesson=0
	rng.seed=20261115+80
	return true

func _update_summoning() -> void:
	elapsed+=2
	_update_field_spell(field_spell)

func can_cast_spell(id: int, skill: int) -> bool:
	return _ending_phase=="active" and id==units[0].instance_id and units[0].input.equipped_skills.has(skill) and field_spell.is_empty() and units[0].limits.hp>0 and units[0].limits.mp>=String(catalog.spells.rows[str(skill)]).hex_decode().decode_u16(8)

func _check_before_actions() -> bool:
	return false

func _next_lesson(sub: int, block := 0) -> void:
	_event_pages=_pages(sub,block)
	_event_index=0
	_ending_phase="event20"
	_accumulator=0

func _wave_removed(first: int) -> bool:
	for number in range(first,first+5):
		if find_unit(1250-number).get("source_state",0)!=4:return false
	return true

func _detect_trial_end() -> bool:
	match lesson:
		0:
			if not _on_region(units[0],"1"):return false
			lesson=1
			_next_lesson(1,1)
		1:
			if not _wave_removed(1):return false
			lesson=2
			_next_lesson(2)
		2:
			if not _wave_removed(6):return false
			lesson=3
			_next_lesson(3)
		_:
			return false
	return true

func advance_event() -> bool:
	if _ending_phase!="event20":return false
	_record_command([2])
	_event_index+=1
	if _event_index<_event_pages.size():return true
	_ending_phase="active"
	if lesson in [1,2]:
		for section in scene_scripts:
			if section.sub!=lesson or section.block!=(1 if lesson==1 else 0):continue
			for command in section.commands:
				if command.opcode==130:
					var args: Array=command.values
					_spawn_group(args[0],Vector2i(args[1],args[2]),args[3])
	return true

func call_student(at: Vector2i) -> bool:
	if units[0].cell.distance_squared_to(at)>2:return false
	if lesson!=3 or _ending_phase!="active" or not _activate(1239,at,1):return false
	var ally := find_unit(1239)
	ally.side=0
	ally.controllable=true
	ally.category=0
	lesson=4
	_next_lesson(4)
	return true

func withdraw_student(id: int) -> bool:
	var unit:=find_unit(id)
	if lesson!=4 or _ending_phase!="active" or not unit.get("controllable",false):return false
	unit.source_state=2
	unit.controllable=false
	lesson=5
	ending_sub=5
	_terminal_choice={"tactical_result_selector":0,"script_sub":5}
	_begin_ending("mission_objectives_met")
	return true
