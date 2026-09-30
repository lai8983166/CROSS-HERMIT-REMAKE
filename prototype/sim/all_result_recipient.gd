class_name AllResultRecipient
extends RefCounted
## Evidence-backed subset of 4C00C0: choose the display recipient by original
## character ID. This is a pure selector, not proof that state 12 was reached.


static func select(group_slots: Array, participant_ids: Array, rank_values: Dictionary) -> Dictionary:
	if group_slots.size() != 5:
		return {"status": "unresolved_input", "reason": "group_count"}
	var best_id := -1
	var best_rank := 0
	var best_group := -1
	var best_slot := -1
	for group_index in range(5):
		var slots: Variant = group_slots[group_index]
		if not slots is Array or slots.size() != 4:
			return {"status": "unresolved_input", "reason": "slots_per_group"}
		for slot_index in range(4):
			if typeof(slots[slot_index]) != TYPE_INT:
				return {"status": "unresolved_input", "reason": "participant_index_type"}
			var participant_index: int = int(slots[slot_index])
			if participant_index < 0:
				continue
			if participant_index >= participant_ids.size():
				return {"status": "unresolved_input", "reason": "participant_index"}
			if typeof(participant_ids[participant_index]) != TYPE_INT:
				return {"status": "unresolved_input", "reason": "character_id_type"}
			var character_id: int = int(participant_ids[participant_index])
			# Original EXE reads before checking <13; reject unsafe IDs here.
			if character_id < 0 or character_id >= 13:
				return {"status": "unresolved_input", "reason": "character_id"}
			if not rank_values.has(character_id):
				return {"status": "unresolved_input", "reason": "rank_value"}
			if typeof(rank_values[character_id]) != TYPE_INT:
				return {"status": "unresolved_input", "reason": "rank_value_type"}
			var rank_value: int = int(rank_values[character_id])
			if rank_value > best_rank:
				best_rank = rank_value
				best_id = character_id
				best_group = group_index
				best_slot = slot_index
	if best_id < 0:
		return {"status": "no_eligible_recipient"}
	return {
		"status": "selected", "character_id": best_id,
		"rank_value": best_rank, "group_index": best_group,
		"slot_index": best_slot,
	}
