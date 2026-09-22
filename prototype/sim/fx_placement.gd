class_name FxPlacement
extends RefCounted
## Original EFCT slots are anchored to their owning unit; no path is inferred
## merely because a stage event also carries a target cell.


static func anchor_cell(event: Dictionary) -> Vector2i:
	var cells: Array = event.get("from_cell", [0, 0]) if \
		String(event.get("anchor", "target")) == "source" else event.get("to_cell", [0, 0])
	return Vector2i(int(cells[0]), int(cells[1]))
