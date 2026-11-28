extends "res://sim/school_sortie_session.gd"

func _open_terrain() -> void:
	field_width=catalog.cell_size[0]
	field_height=catalog.cell_size[1]
	attack_paths=AttackPaths.new(field_width,field_height,catalog.passability)
	var zeros := []
	zeros.resize(field_width*field_height)
	zeros.fill(0)
	for layer in catalog.passability:
		var map := SimMapData.new()
		map.cell_w=field_width
		map.cell_h=field_height
		map._layers={"terrain":layer,"object":zeros,"variant":zeros}
		_maps.append(map)

func _update_captures() -> void:
	pass
