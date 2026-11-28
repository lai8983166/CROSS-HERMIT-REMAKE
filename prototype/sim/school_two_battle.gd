extends RefCounted
## T0002 block 1 uses the numbered MAP02 event cells; 433040 samples bit 0.
var searched_first_region := false

func result(s, unavailable: bool) -> int:
	for unit in s.controlled_units():
		if s._on_region(unit, "2"):
			# Block 1 sub 2 writes bit 0. The exit takes priority over time and defeat.
			var owned := 0
			# 5FF758 holds source actor numbers 1, 2, 3 and the -1 sentinel.
			for id in [1249,1248,1247]:
				var object: Dictionary = s.find_unit(id)
				if object.source_state != 0 and object.side == 0:
					owned += 1
			if owned < 3:
				return 8
			return 2 if s._own_casualties == 0 else 5
	if s.remaining_ticks == 0:
		return 11
	if unavailable:
		return 14
	if not searched_first_region:
		for unit in s.controlled_units():
			if s._on_region(unit, "1"):
				searched_first_region = true
				s._event_pages = s._pages(1, 1)
				s._event_index = 0
				s._ending_phase = "event20"
				s._accumulator = 0.0
				break
	return -1
