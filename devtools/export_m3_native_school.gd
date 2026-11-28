extends SceneTree
## Export the state actually opened by the original-save campaign.
const Campaign := preload("res://sim/school_native_campaign.gd")

func _initialize() -> void:
	var args:=OS.get_cmdline_user_args()
	if args.size()!=3 or args[1].length()!=64 or FileAccess.get_sha256(args[0])!=args[1] or FileAccess.file_exists(args[2]):
		quit(2)
		return
	var campaign:=Campaign.new()
	if not campaign.load_origin(args[0]):quit(1);return
	var file:=FileAccess.open(args[2],FileAccess.WRITE)
	if file==null:quit(2);return
	file.store_string(JSON.stringify(campaign.state))
	file.flush()
	var ok:=file.get_error()==OK
	file.close()
	quit(0 if ok else 1)
