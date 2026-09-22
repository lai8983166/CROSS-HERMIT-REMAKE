class_name AnimTimeline
extends RefCounted
## DxAnim schema v2 时间线工具；同时把 v1 {frame,dur} records 适配成单层 step。


static func normalize(animation: Dictionary) -> Dictionary:
	var steps: Array = []
	if animation.get("steps") is Array:
		for raw_step: Variant in animation.get("steps", []):
			if not raw_step is Dictionary:
				continue
			var step: Dictionary = raw_step
			var layers: Array = []
			for raw_layer: Variant in step.get("layers", []):
				if raw_layer is Dictionary:
					layers.append(raw_layer)
			steps.append({
				"duration_ticks": maxi(1, int(step.get("duration_ticks", 1))),
				"layers": layers,
			})
	else:
		for raw_record: Variant in animation.get("records", []):
			if not raw_record is Dictionary:
				continue
			var record: Dictionary = raw_record
			var layers: Array = []
			var frame := int(record.get("frame", -1))
			if frame >= 0:
				layers.append({
					"frame": frame, "x": 0, "y": 0,
					"flip_x": false, "flip_y": false,
					"legacy_anchor": true,
				})
			steps.append({
				"duration_ticks": maxi(1, int(record.get("dur", 1))),
				"layers": layers,
			})
	return {"steps": steps, "loop_from": animation.get("loop_from", null)}


static func resolve(data: Dictionary, entry: Dictionary) -> Dictionary:
	if entry.is_empty():
		return {}
	var animation: Dictionary = {}
	var block := int(entry.get("block", 0))
	var animation_id := int(entry.get("anim", -1))
	if block == 0:
		var animations: Array = data.get("anims", [])
		if animation_id >= 0 and animation_id < animations.size():
			animation = animations[animation_id]
	else:
		var blocks: Dictionary = data.get("anim_blocks", {})
		var block_anims: Dictionary = blocks.get(str(block), {})
		animation = block_anims.get(str(animation_id), {})
		if animation.is_empty() and block == 1:
			# Legacy v1 composites used a positional index instead of a block program.
			var composites: Array = data.get("composites", [])
			var composite := int(entry.get("composite", -1))
			if composite >= 0 and composite < composites.size():
				animation = composites[composite]
	if animation.is_empty():
		return {}
	var timeline := normalize(animation)
	timeline["flags"] = int(entry.get("flags", 0))
	timeline["anim"] = int(entry.get("anim", entry.get("composite", -1)))
	timeline["block"] = block
	return timeline


## Resolve a directional original action. Blank/missing action slots use the
## unit's configured idle entry instead of inventing a substitute animation.
static func unit_action_entry(data: Dictionary, action: int, direction: String) -> Dictionary:
	var anim_map: Dictionary = data.get("anim_map", {})
	var actions: Dictionary = anim_map.get("skill_actions", {})
	var directions: Dictionary = actions.get(str(action), {})
	var entry: Dictionary = directions.get(direction, {})
	if not entry.is_empty():
		return entry
	var idle_directions: Dictionary = anim_map.get("idle_by_dir", {})
	entry = idle_directions.get(direction, {})
	return entry if not entry.is_empty() else anim_map.get("IDLE", {})


static func total_ticks(timeline: Dictionary) -> int:
	var total := 0
	for step: Dictionary in timeline.get("steps", []):
		total += maxi(1, int(step.get("duration_ticks", 1)))
	return total


static func step_at(timeline: Dictionary, elapsed_ticks: int, repeat_without_loop := false) -> Dictionary:
	var steps: Array = timeline.get("steps", [])
	if steps.is_empty() or elapsed_ticks < 0:
		return {}
	var total := total_ticks(timeline)
	if total <= 0:
		return {}
	var tick := elapsed_ticks
	var loop_value: Variant = timeline.get("loop_from", null)
	if loop_value is int and int(loop_value) >= 0 and int(loop_value) < steps.size():
		var loop_tick := 0
		for index in int(loop_value):
			loop_tick += maxi(1, int(steps[index].get("duration_ticks", 1)))
		var loop_duration := total - loop_tick
		if tick >= total and loop_duration > 0:
			tick = loop_tick + (tick - loop_tick) % loop_duration
	elif repeat_without_loop:
		tick %= total
	elif tick >= total:
		return {}

	for index in steps.size():
		var duration := maxi(1, int(steps[index].get("duration_ticks", 1)))
		if tick < duration:
			return {"index": index, "step": steps[index]}
		tick -= duration
	return {}


static func clock_elapsed(clock: Dictionary, identity: String, sim_frame: int) -> int:
	if String(clock.get("identity", "")) != identity:
		clock["identity"] = identity
		clock["start_frame"] = sim_frame
	return maxi(0, sim_frame - int(clock.get("start_frame", sim_frame)))


static func layer_rect(frame_data: Dictionary, layer: Dictionary) -> Rect2:
	var width := float(frame_data.get("w", 0))
	var height := float(frame_data.get("h", 0))
	if bool(layer.get("legacy_anchor", false)) or not layer.has("descriptor"):
		var anchor: Dictionary = frame_data.get(
			"anchor", {"x": width * 0.5, "y": height})
		return Rect2(
			Vector2(-float(anchor.get("x", 0.0)) + float(layer.get("x", 0.0)),
				-float(anchor.get("y", 0.0)) + float(layer.get("y", 0.0))),
			Vector2(width, height))
	var canvas: Dictionary = frame_data.get("canvas", {})
	return Rect2(
		Vector2(float(canvas.get("x", 0.0)) - float(canvas.get("w", 0.0)) * 0.5
				+ float(layer.get("x", 0.0)),
			float(canvas.get("y", 0.0)) - float(canvas.get("h", 0.0)) * 0.5
				+ float(layer.get("y", 0.0))),
		Vector2(width, height))


static func combined_flip(layer: Dictionary, selection_flags: int) -> Vector2i:
	return Vector2i(
		1 if bool(layer.get("flip_x", false)) != bool(selection_flags & 1) else 0,
		1 if bool(layer.get("flip_y", false)) != bool(selection_flags & 2) else 0)
