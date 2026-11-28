extends RefCounted
## Replay the dated ADV control flow using the current battle grades and choices.
const Roles := preload("res://sim/all_result_role_replay.gd")
const PATH := "res://data/school_year_winter.json"
const SHA := "2194e641ca3753edd3bc94217ec8bd5b0e5b7eb1e384bcfe2ab9ad097624cbe8"
static var _data := {}


static func source() -> Dictionary:
	if _data.is_empty():
		var raw := FileAccess.get_file_as_string(PATH).replace("\r\n","\n")
		if raw.sha256_text()==SHA:
			_data=Roles._integers(JSON.parse_string(raw))
	return _data


static func departure(month: int, week: int) -> bool:
	return (month==12 and week in range(3,6)) or (month in [13,14] and week in range(1,6)) or (month==15 and week in range(1,5))


static func arrival(month: int, week: int) -> bool:
	return (month==12 and week in [4,5]) or (month in [13,14,15] and week in range(1,6))


static func _flush(state: Dictionary) -> void:
	if state.lines.is_empty():return
	var board: Array = state.boards.get(state.active,[0xfffffff,"旁白"])
	state.pages.append({"chapter":state.chapter,"speaker_id":board[0],"speaker":board[1],
		"text_indices":state.indices.duplicate(),"text":"\n".join(state.lines),"source_offset":state.offset})
	state.lines.clear()
	state.indices.clear()


static func ending_member(spending: Dictionary) -> int:
	# 4D1560 reads signed personal spending totals. A strict comparison keeps
	# the first tied member. The native loop stops before member twelve.
	var winner := 1
	var maximum := 0
	for id in range(1,12):
		var total: Variant=spending.get(id,0)
		if typeof(total)!=TYPE_INT or total < -2147483648 or total > 2147483647:return -1
		if total>maximum:
			winner=id
			maximum=total
	return winner


static func _section(section: Dictionary, grades: Dictionary, choices: Array, spending: Dictionary) -> Dictionary:
	var state := {"pages":[],"lines":[],"indices":[],"effects":section.effects.duplicate(true),
		"roster_steps":[],"boards":{},"active":-1,"offset":0,"choice_labels":[],"chapter":section.chapter}
	var name: String=section.chapter
	var selected := 0
	var value := 0
	while not name.is_empty():
		var program: Array=source().scenes[name].program
		var cursor := 0
		var jumps := {}
		for i in range(program.size()):
			jumps[program[i][0]]=i
		state.chapter=name
		name=""
		while cursor<program.size():
			var op: Array=program[cursor]
			cursor+=1
			state.offset=op[0]
			match op[1]:
				"board":
					_flush(state)
					state.boards[op[2]]=[op[3],op[4]]
				"active":
					_flush(state)
					state.active=op[2]
				"line":
					state.indices.append(op[2])
					state.lines.append(op[3])
				"page":_flush(state)
				"effect":
					var effect := {"opcode":op[2],"operands":op.slice(3)}
					state.effects.append(effect)
					if op[2] in [144,145]:
						state.roster_steps.append({"page":state.pages.size(),"effect":effect})
				"choice":
					_flush(state)
					if selected==choices.size():
						state.choice_labels=op[2]
						return state
					value=choices[selected]
					selected+=1
					if value<0 or value>=op[2].size():return {}
					state.pages.clear()
				"grade":value=grades.get(op[2],0)
				"winner":
					value=ending_member(spending)
					if value<0:return {}
				"if","jump":
					if op[1]=="jump" or value==op[2]:
						var target: int=op[-1]
						# Presentation instructions excluded from the program can occupy
						# the branch destination immediately before a retained operation.
						while not jumps.has(target) and target<=program[-1][0]:target+=1
						if not jumps.has(target):return {}
						cursor=jumps[target]
				"chapter":
					_flush(state)
					name=op[2]
					break
				"end":
					_flush(state)
					break
	return state


# 49EE30 clears personal spending at new game. Current campaign commands do
# not purchase skills or goods, so their input to the ending selector is empty.
static func story(month: int, week: int, grades: Dictionary, choices: Array=[], spending: Dictionary={}) -> Dictionary:
	for row in source().get("arrivals",[]):
		if row.departure!=[month,week]:continue
		var result := {"supported":true,"winter":true,"terminal":row.terminal,"date_card":row.get("date_card",{}),
			"pre_week":[],"week_start":[],"school_entry":[],"effects":[[],[],[]],"roster_steps":[[],[],[]],"choice_labels":[]}
		if not row.terminal and FileAccess.get_sha256(row.date_card.image)!=row.date_card.png_sha256:
			return {"supported":false,"reason":"school_year_date_card_changed"}
		for i in range(row.sections.size()):
			var state := _section(row.sections[i],grades,choices if i==0 else [],spending)
			if state.is_empty():return {"supported":false,"reason":"invalid_winter_story_branch"}
			result[["pre_week","week_start","school_entry"][i]]=state.pages
			result.effects[i]=state.effects
			result.roster_steps[i]=state.roster_steps
			if i==0:result.choice_labels=state.choice_labels
		return result
	return {"supported":false,"reason":"missing_winter_story"}
