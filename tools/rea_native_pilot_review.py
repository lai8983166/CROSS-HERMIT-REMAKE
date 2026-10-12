#!/usr/bin/env python3
"""Verify captured REA pilot results against the selected PE and old exports.

This checks artifact identity, exact entry bytes and known direct calls. It
does not prove runtime semantics or assume that decompiler signatures are true.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import statistics
import struct


REPO = Path(__file__).resolve().parents[1]
ADDRESSES = ("405160", "4cb220", "4ce8f0")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def value(path):
    raw = load(path)["raw_result"]
    return raw["value"] if isinstance(raw, dict) and "value" in raw else raw


def entry_bytes(image, address):
    pe = struct.unpack_from("<I", image, 0x3C)[0]
    opt = pe + 24
    base = struct.unpack_from("<I", image, opt + 28)[0]
    section_count = struct.unpack_from("<H", image, pe + 6)[0]
    opt_size = struct.unpack_from("<H", image, pe + 20)[0]
    rva = address - base
    for index in range(section_count):
        offset = opt + opt_size + index * 40
        _, start, size, file_offset = struct.unpack_from("<IIII", image, offset + 8)
        if start <= rva and rva + 32 <= start + size:
            return image[file_offset + rva - start:file_offset + rva - start + 32].hex()
    raise ValueError(f"No initialized PE section at {address:#x}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    args = parser.parse_args()
    root = args.results.resolve()
    target = REPO / "analysis/hermit_game.exe"
    image = target.read_bytes()
    target_hash = hashlib.sha256(image).hexdigest()
    checks = []
    report = {"target_sha256": target_hash, "trials": [], "functions": [], "checks": checks}

    def check(name, passed):
        checks.append({"name": name, "passed": bool(passed)})

    for trial in ("seeded", "unseeded"):
        directory = root / trial
        run = load(directory / "run.json")
        check(f"{trial}: closed and exited", run["close_succeeded"] and run["server_exit_code"] == 0)
        check(f"{trial}: target preserved", run["target_sha256_before"] == run["target_sha256_after"] == target_hash)
        check(f"{trial}: REA version pinned", run["rea_version"] == "6.4.0")
        failures = [q for q in run["queries"] if q["is_error"]]
        if trial == "seeded":
            check("seeded: completed with all queries successful", run["completed"] and not failures)
        else:
            # Negative control: no declared entry seeds -> these three functions
            # are absent, despite mapped bytes and successful full auto-analysis.
            check("unseeded: 13 expected missing-procedure errors", not run["completed"] and len(failures) == 13)
            for query in failures:
                captured = load(directory / query["file"])
                check(f"unseeded: {query['label']} rejected for absent procedure", "No procedure exists at the requested address" in json.dumps(captured))
        warm_times = [q["seconds"] for q in run["queries"] if not q["is_error"] and q["label"] not in ("open", "session", "overview-cold", "close")]
        cold_time = next(q["seconds"] for q in run["queries"] if q["label"] == "overview-cold")
        report["trials"].append({"trial": trial, "query_count": len(run["queries"]),
                                  "query_error_count": len(failures),
                                  "cold_overview_seconds": cold_time,
                                  "warm_query_median_seconds": statistics.median(warm_times),
                                  "warm_query_max_seconds": max(warm_times)})
        opened = load(directory / "open.json")["result"]
        check(f"{trial}: native x86 PE admitted", opened["architecture"] == "x86" and opened["format"] == "pe" and opened["sha256"] == target_hash)
        for query in run["queries"]:
            captured = load(directory / query["file"])
            if "subject" in captured and captured["subject"] is not None:
                check(f"{trial}: {query['label']} subject identity", captured["subject"]["digest"]["sha256"] == target_hash)

    for address in ADDRESSES:
        baseline_file = REPO / f"analysis/decomp_all/{address}.c"
        baseline = baseline_file.read_text(encoding="utf-8")
        body = baseline[baseline.index("{") + 1:]
        expected_calls = {f"0x{int(x, 16):x}" for x in re.findall(r"(?:FUN__text__|FUN_|func_0x)([0-9a-fA-F]{8})\s*\(", body)}
        if "__chkesp(" in baseline:
            expected_calls.add("0x56ce80")
        row = {"address": f"0x{address}", "baseline_path": baseline_file.relative_to(REPO).as_posix(),
               "baseline_sha256": hashlib.sha256(baseline_file.read_bytes()).hexdigest(),
               "baseline_api_names": sorted(set(re.findall(r"API_\w+", baseline))),
               "baseline_direct_call_addresses": sorted(expected_calls), "trials": []}
        for trial in ("seeded", "unseeded"):
            directory = root / trial
            observed_bytes = value(directory / f"{address}-bytes.json")
            check(f"{trial}: {address} exact entry bytes", observed_bytes["complete"] and observed_bytes["bytes_hex"] == entry_bytes(image, int(address, 16)))
            if trial == "unseeded":
                row["trials"].append({"trial": trial,
                                      "name": value(directory / f"{address}-name.json"),
                                      "pseudocode_available": False,
                                      "error": load(directory / f"{address}-procedure_pseudo_code.json")["error"]})
                continue
            pseudo = value(directory / f"{address}-procedure_pseudo_code.json")
            assembly = value(directory / f"{address}-procedure_assembly.json")
            callees = value(directory / f"{address}-procedure_callees.json")
            missing = sorted(expected_calls - set(callees))
            check(f"{trial}: {address} nonempty pseudocode", isinstance(pseudo, str) and bool(pseudo.strip()))
            check(f"{trial}: {address} reaches a return", assembly.splitlines()[-1].split(": ")[1].startswith("RET"))
            check(f"{trial}: {address} old named direct calls preserved", not missing)
            observed_name = value(directory / f"{address}-name.json")
            row["trials"].append({"trial": trial, "name": observed_name,
                                  "pseudocode_characters": len(pseudo),
                                  "assembly_instruction_count": len(assembly.splitlines()),
                                  "last_instruction": assembly.splitlines()[-1],
                                  "callers": value(directory / f"{address}-procedure_callers.json"),
                                  "callee_count": len(callees), "missing_old_direct_calls": missing,
                                  "api_names_in_pseudocode": sorted(set(re.findall(r"API_\w+", pseudo))),
                                  "ecx_explicitly_recovered_as_parameter": "in_ECX" not in pseudo})
        report["functions"].append(row)

    expected_names = {"405160": "text_render_A", "4cb220": "pilot_text_update_4cb220", "4ce8f0": "pilot_story_vm_4ce8f0"}
    for address, name in expected_names.items():
        check(f"seeded: {address} declared name retained", value(root / f"seeded/{address}-name.json") == name)
    check("seeded: IAT name retained", value(root / "seeded/iat-name.json") == "API_GDI32_DLL_GetTextExtentPoint32A")
    # A narrow textual comparison makes normalization explicit; it is not a
    # claim of semantic equivalence for all three decompiled functions.
    fade_old = (REPO / "analysis/decomp_all/4cb220.c").read_text(encoding="utf-8")
    fade_new = value(root / "seeded/4cb220-procedure_pseudo_code.json")
    fade_old = fade_old[fade_old.index("{"):].replace("param_1", "object")
    fade_old = fade_old.replace("param_2", "ARG1").replace("param_3", "ARG2")
    fade_old = fade_old.replace("FUN__text__", "FUN_").replace("FUN_0056ce80", "__chkesp")
    fade_new = fade_new[fade_new.index("{"):].replace("in_ECX", "object")
    fade_new = fade_new.replace("param_1", "ARG1").replace("param_2", "ARG2")
    fade_new = fade_new.replace("int object;", "")
    fade_equal = re.sub(r"\s+", "", fade_old) == re.sub(r"\s+", "", fade_new)
    check("seeded: fade body matches old export after declared normalization", fade_equal)
    report["fade_comparison"] = {"equal_after_normalization": fade_equal,
                                 "normalizations": ["Exclude function signature", "Unify ECX object and argument names",
                                                    "Unify FUN__text__ and __chkesp names", "Remove the new in_ECX local declaration",
                                                    "Ignore whitespace"]}
    captured_baselines = load(root / "baselines.json")
    for recorded in captured_baselines["functions"]:
        path = REPO / recorded["baseline_path"]
        check(f"baseline preserved: {recorded['address']}", hashlib.sha256(path.read_bytes()).hexdigest() == recorded["baseline_sha256"])
    report["iat_names"] = {trial: value(root / trial / "iat-name.json") for trial in ("seeded", "unseeded")}
    report["limitations"] = [
        "The unseeded control completed auto-analysis but all three function-based probes failed for absent procedure entries; those are retained expected failures, not successful function analysis.",
        "Entry bytes and direct-call checks do not prove runtime behavior or complete callgraph coverage.",
        "Names introduced by seeds are analyst assertions. Seeds do not import the existing Ghidra project's pointer types, signatures, comments or data mutability.",
        "Static callers can omit dispatch through tables or computed calls; an empty caller list is not evidence a function is unused.",
        "Captured text-render pseudocode loses the existing API names; ECX object parameters and one VM global pointer expression require independent verification.",
        "Two cold sessions and warm queries are a local sample, not a general performance benchmark.",
    ]
    report["passed"] = all(item["passed"] for item in checks)
    write(root / "review.json", report)
    files = [p for p in root.rglob("*") if p.is_file() and p.name != "artifact-manifest.json"]
    write(root / "artifact-manifest.json", [{"path": p.relative_to(root).as_posix(),
                                            "bytes": p.stat().st_size,
                                            "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                                           for p in sorted(files)])
    print(json.dumps({"passed": report["passed"], "checks": len(checks),
                      "failed": [item["name"] for item in checks if not item["passed"]],
                      "trials": report["trials"]}, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
