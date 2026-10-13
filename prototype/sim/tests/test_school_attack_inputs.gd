extends "res://sim/tests/test_base.gd"
const Inputs := preload("res://sim/school_attack_inputs.gd")
const Limits := preload("res://sim/school_combat_limits.gd")
const FIXTURE := "res://sim/tests/fixtures/school_attack_inputs_native.json"

class Rolls extends RefCounted:
	var values: Array
	var cursor := 0
	func _init(raw: Array): values = raw.duplicate()
	func randi() -> int:
		var value: int = values[cursor]; cursor += 1; return value


func _fixture() -> Dictionary:
	return Limits._source_numbers(JSON.parse_string(FileAccess.get_file_as_string(FIXTURE)))


func test_all_original_current_field_and_clamp_cases() -> void:
	var rules := Inputs.load_rules(); assert_false(rules.is_empty())
	for row in _fixture()["fields"]:
		var before: Dictionary = row["input"].duplicate(true)
		var result := Inputs.project(row["input"],rules)
		assert_true(result["supported"])
		for key in row["expected"]: assert_eq(result["fields"][key],row["expected"][key])
		assert_eq(row["input"],before)


func test_original_snapshots_and_scalar_random_consumption() -> void:
	var fixture := _fixture(); var rules := Inputs.load_rules()
	for row in fixture["snapshots"]:
		var fields: Dictionary = Inputs.project(row["input"],rules)["fields"]
		var result := Inputs.snapshot(fields,row["terrain"],0,rules)
		for key in row["expected"]: assert_eq(result[key],row["expected"][key])
	for row in fixture["scalar"]:
		var rng := Rolls.new(row["rolls"])
		assert_eq(Inputs.damage(row["attack"],row["defense"],rng,row["magic"]),row["damage"])
		assert_eq(rng.cursor,row["random_calls"],"same original roll consumption")


func test_unsupported_roles_equipment_and_terrain_refuse() -> void:
	var input: Dictionary = _fixture()["fields"][0]["input"]
	var rules := Inputs.load_rules()
	for pair in [["character_id",101],["job",6],["equipped_items",[1,0,0,0,0,0,0,0]],["attributes",[1,1]]]:
		var bad: Dictionary = input.duplicate(true); bad[pair[0]] = pair[1]
		assert_false(Inputs.project(bad,rules)["supported"])
	assert_false(Inputs.project(input,{})["supported"])
	var fields: Dictionary = Inputs.project(input,rules)["fields"]
	assert_true(Inputs.snapshot(fields,-1,0,rules).is_empty())
	assert_true(Inputs.snapshot(fields,0,5,rules).is_empty())
