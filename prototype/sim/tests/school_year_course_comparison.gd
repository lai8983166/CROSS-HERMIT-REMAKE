extends RefCounted
## Digests of the six campaign settlements already checked against the original x86.
const SOURCE := "res://data/school_year_loop_evidence_oct_nov.json"
const Roles := preload("res://sim/all_result_role_replay.gd")
const Jobs := preload("res://sim/school_job_eligibility.gd")

static func compare_menus(before: Dictionary) -> bool:
	var reference: Dictionary=Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(
		"res://data/school_year_campaign_jobs.json")))
	var menu := Jobs.menu_data()
	for row in reference.weeks:
		if row.date!=[before.school.month,before.school.week]:continue
		var actual := []
		for student in before.participants:
			actual.append({"member":student.character_id,"flags":student.unlock_flags,
				"selectable_jobs":Jobs.calculate_eligibility(student,menu)})
		return actual.size()==row.students and JSON.stringify(actual,"",true).sha256_text()==row.menus_sha256
	return false

static func compare(after: Dictionary) -> String:
	var reference: Dictionary=Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(SOURCE)))
	for row in reference.weeks:
		if row.date!=[after.school.month,after.school.week]:continue
		if [row.total,row.mvp]!=[after.school.global_total_511c,after.course_result.recipient]:
			return "total or MVP"
		var fields := {"growth":after.growth,"history":after.records,
			"relationships":after.school.relationships,"mvp_counts":after.counts}
		for key in fields:
			if JSON.stringify(fields[key],"",true).sha256_text()!=row[key+"_sha256"]:
				return key
		return ""
	return "unverified settlement date"
