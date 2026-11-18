extends "res://sim/tests/test_base.gd"
const Combat := preload("res://sim/school_combat_session.gd")
const Paths := preload("res://sim/school_sortie_paths.gd")


func test_routes_match_forward_bfs_for_ties_obstructions_and_changed_occupancy() -> void:
	var session := Combat.new()
	session.field_width = 5
	session.field_height = 4
	session.ready = true
	var layers := [
		[1,1,1,0,1, 1,0,1,0,1, 1,1,1,0,1, 1,1,1,0,1],
		[1,1,0,1,1, 1,1,1,1,1, 1,1,1,1,1, 0,1,1,1,0]]
	session.catalog = {"passability":layers}
	var paths := Paths.new(5,4,layers)
	var attacker := {"character_id":3,"cell":Vector2i.ZERO,"limits":{"hp":3},"combat":{"attack_range":1},"movement_type":0}
	var target := {"character_id":1100,"cell":Vector2i.ZERO,"limits":{"hp":2}}
	var blocker := {"character_id":1101,"cell":Vector2i(2,2),"limits":{"hp":1}}
	session.units.assign([attacker,target,blocker])
	for active in [0,1]:
		blocker["limits"]["hp"]=active
		for from in range(20):
			attacker["cell"]=Vector2i(from%5,from/5)
			for to in range(20):
				target["cell"]=Vector2i(to%5,to/5)
				for mode in range(2):
					attacker["movement_type"]=mode
					for reach in [1,2]:
						attacker["combat"]["attack_range"]=reach
						var actual := paths.route(attacker["cell"],target["cell"],reach,mode,session.units)
						var expected := session._attack_path(attacker,target)
						if actual != expected:
							assert_eq(actual,expected,"from %d to %d mode %d range %d" % [from,to,mode,reach])
							return
