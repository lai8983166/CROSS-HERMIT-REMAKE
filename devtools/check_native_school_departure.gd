extends SceneTree
const Native := preload("res://sim/school_native_departure.gd")
const Sortie := preload("res://sim/school_sortie_session.gd")

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size()!=1:quit(2);return
	var raw := FileAccess.get_file_as_bytes(args[0])
	var base := Native.decode(raw)
	if base.is_empty():quit(1);return
	# Exchange two valid occupied slots and recompute the native signed checksum.
	var group := 0x7aaa12-Native.BASE
	var swapped := raw.duplicate()
	var first := raw.decode_s16(group+16)
	var second := raw.decode_s16(group+18)
	swapped.encode_s16(group+16,second)
	swapped.encode_s16(group+18,first)
	_checksum(swapped)
	var variant := Native.decode(swapped)
	var battle := Sortie.new()
	if not battle.open(variant) or variant.native_sha256==base.native_sha256 or battle.controlled_units()[0].character_id!=second:
		printerr("Legal reordered native squad rejected");quit(1);return
	var corrupt := raw.duplicate()
	corrupt[group+16]^=1
	if not Native.decode(corrupt).is_empty():quit(1);return
	for patch in [[group+16,second],[group+16,200],[group+14,5],[group+14,0],[0x178,41],[0x7aab16-Native.BASE,99],[0x7a5662-Native.BASE+6,1],[0x7a5662-Native.BASE+14,1]]:
		corrupt=raw.duplicate()
		corrupt.encode_s16(patch[0],patch[1])
		_checksum(corrupt)
		if not Native.decode(corrupt).is_empty():
			printerr("Invalid native field accepted at ",patch[0]);quit(1);return
	var school=load("res://school_playground.tscn").instantiate()
	root.add_child(school)
	school._open_native_sortie(args[0])
	if not school.sortie_trial.visible or not school.sortie_trial.session.ready or school.sortie_trial.member_buttons.size()!=base.participants.size():
		printerr("School UI did not open the imported sortie");quit(1);return
	print("MAP",battle.scene_id," native admission, reordered slots, invalid records and school UI passed")
	quit(0)

func _checksum(raw: PackedByteArray) -> void:
	var sum := 0
	for i in raw.size():
		if i<44 or i>=48:sum+=raw[i] if raw[i]<128 else raw[i]-256
	raw.encode_s32(44,sum)
