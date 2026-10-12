#!/usr/bin/env python3
"""Run a bounded REA MCP/Ghidra pilot without changing agent registration.

Install rea-agents@6.4.0 into a separate npm prefix, then pass its package
directory as --rea-root. Results are observations, not runtime validation.
Uses only Python's standard library; one server owns one imported program.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import subprocess
import threading
import time


PROCEDURES = ("0x405160", "0x4cb220", "0x4ce8f0")
REPO = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class MCP:
    def __init__(self, entry, env, output, node):
        self.stderr = (output / "server-stderr.log").open("w", encoding="utf-8")
        self.process = subprocess.Popen(
            [node, str(entry), "mcp"], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=self.stderr, text=True,
            encoding="utf-8", env=env,
        )
        self.messages = queue.Queue()
        self.sequence = 0
        self.notifications = []
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        try:
            for line in self.process.stdout:
                self.messages.put(json.loads(line))
        except Exception as error:
            self.messages.put(error)
        finally:
            self.messages.put(None)

    def notify(self, method, params=None):
        message = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            message["params"] = params
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def request(self, method, params, timeout):
        self.sequence += 1
        request_id = self.sequence
        self.process.stdin.write(json.dumps({
            "jsonrpc": "2.0", "id": request_id, "method": method, "params": params,
        }) + "\n")
        self.process.stdin.flush()
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                self.notify("notifications/cancelled", {
                    "requestId": request_id, "reason": "Pilot request deadline exceeded",
                })
                raise TimeoutError(f"{method} exceeded {timeout}s")
            try:
                message = self.messages.get(timeout=min(remaining, 10))
            except queue.Empty:
                continue
            if message is None:
                raise RuntimeError(f"REA exited ({self.process.poll()})")
            if isinstance(message, Exception):
                raise message
            if message.get("id") == request_id:
                if "error" in message:
                    raise RuntimeError(json.dumps(message["error"]))
                return message["result"]
            if "method" in message:
                self.notifications.append(message)
                if message["method"] == "notifications/progress":
                    print(message.get("params", {}).get("message", "REA progress"), flush=True)

    def shutdown(self):
        # REA owns its Ghidra process tree; close_binary runs before stdin EOF.
        self.process.stdin.close()
        try:
            self.process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait(timeout=30)
        self.stderr.close()
        return self.process.returncode


def evidence(result):
    if "structuredContent" in result:
        return result["structuredContent"]
    texts = [block["text"] for block in result.get("content", []) if block.get("type") == "text"]
    if len(texts) == 1:
        try:
            return json.loads(texts[0])
        except ValueError:
            pass
    return {"content": result.get("content", [])}


def write_seeds(output):
    # Reuse existing analyst names; these are not discoveries by REA.
    lines = ["# Analyst assertions from tools/ghidra_analyze.py and hermit_real_iat.json"]
    names = {"0x405160": "text_render_A", "0x4cb220": "pilot_text_update_4cb220",
             "0x4ce8f0": "pilot_story_vm_4ce8f0"}
    for address, name in names.items():
        lines.append(f"{address}\tfunction\t{name}")
    iat = json.loads((REPO / "analysis/hermit_real_iat.json").read_text(encoding="utf-8"))
    for slot, name in sorted(iat.items(), key=lambda pair: int(pair[0])):
        safe = "API_" + name.replace("!", "_").replace(".", "_")
        lines.append(f"{int(slot):#x}\tlabel\t{safe}")
    path = output / "seeds.tsv"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rea-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="New results directory")
    parser.add_argument("--node", default="node")
    parser.add_argument("--target", type=Path, default=REPO / "analysis/hermit_game.exe")
    parser.add_argument("--ghidra", default="F:/ghidra/ghidra_12.1.3_PUBLIC")
    parser.add_argument("--java-home", default="C:/Program Files/Eclipse Adoptium/jdk-21.0.12.101-hotspot")
    parser.add_argument("--startup-seconds", type=int, default=900)
    parser.add_argument("--seed", action="store_true", help="Seed three function names and the current IAT labels")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    root = args.rea_root.resolve()
    entry = root / "scripts/rea.mjs"
    target = args.target.resolve()
    version = json.loads((root / "package.json").read_text(encoding="utf-8"))["version"]
    report = {"rea_version": version, "target": str(target), "target_sha256_before": digest(target),
              "ghidra": args.ghidra, "java_home": args.java_home,
              "seeded": args.seed, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "queries": [], "scope": "Three known native functions; no agent registration writes"}
    env = dict(os.environ)
    # Explicit local session settings prevent an inherited profile changing this trial.
    for key in list(env):
        if key.startswith("REA_GHIDRA_"):
            del env[key]
    env.update(GHIDRA_INSTALL_DIR=args.ghidra, JAVA_HOME=args.java_home,
               REA_ANALYSIS_PROVIDER="ghidra",
               REA_GHIDRA_STARTUP_TIMEOUT_MS=str(args.startup_seconds * 1000))
    if args.seed:
        seeds = write_seeds(output)
        env["REA_GHIDRA_SEED_FILE"] = str(seeds)
        report["seed_sha256"] = digest(seeds)
        report["iat_source_sha256"] = digest(REPO / "analysis/hermit_real_iat.json")
    client = MCP(entry, env, output, args.node)
    opened = False

    def call(label, name, arguments, timeout=90):
        print(f"START {label}", flush=True)
        started = time.monotonic()
        result = client.request("tools/call", {"name": name, "arguments": arguments,
                                "_meta": {"progressToken": label}}, timeout)
        elapsed = round(time.monotonic() - started, 3)
        value = evidence(result)
        save(output / f"{label}.json", value)
        record = {"label": label, "tool": name, "arguments": arguments,
                  "seconds": elapsed, "is_error": bool(result.get("isError")),
                  "file": f"{label}.json"}
        report["queries"].append(record)
        save(output / "run.json", report)
        print(f"DONE {label} {elapsed}s error={record['is_error']}", flush=True)
        return value, record["is_error"]

    try:
        report["initialize"] = client.request("initialize", {
            "protocolVersion": "2025-03-26", "capabilities": {},
            "clientInfo": {"name": "chaomofa-rea-pilot", "version": "1"},
        }, 90)
        client.notify("notifications/initialized")
        tools = client.request("tools/list", {}, 90)["tools"]
        required = {"open_binary", "close_binary", "binary_session", "binary_overview",
                    "analyze_function", "procedure_pseudo_code", "procedure_assembly",
                    "procedure_callers", "procedure_callees", "read_bytes", "address_name", "xrefs"}
        missing = required - {tool["name"] for tool in tools}
        if missing:
            raise RuntimeError(f"Missing live MCP tools: {sorted(missing)}")
        save(output / "tool-input-schemas.json", [
            {key: tool[key] for key in ("name", "description", "inputSchema")}
            for tool in tools if tool["name"] in required
        ])
        _, failed = call("open", "open_binary", {"path": str(target), "provider_id": "ghidra"})
        if failed:
            raise RuntimeError("open_binary failed; see open.json")
        opened = True
        call("session", "binary_session", {"expected_package_version": version})
        _, failed = call("overview-cold", "binary_overview", {}, args.startup_seconds + 90)
        if failed:
            raise RuntimeError("Cold Ghidra query failed; see overview-cold.json")
        call("overview-warm", "binary_overview", {})
        for address in PROCEDURES:
            suffix = address[2:]
            for tool in ("procedure_pseudo_code", "procedure_assembly", "procedure_callers", "procedure_callees"):
                call(f"{suffix}-{tool}", tool, {"procedure": address})
            call(f"{suffix}-name", "address_name", {"address": address})
            call(f"{suffix}-bytes", "read_bytes", {"address": address, "length": 32})
        call("4cb220-xrefs", "xrefs", {"address": "0x4cb220"})
        call("4cb220-dossier", "analyze_function", {"procedure": "0x4cb220"})
        iat = json.loads((REPO / "analysis/hermit_real_iat.json").read_text(encoding="utf-8"))
        for slot, name in iat.items():
            if name.upper().endswith("!GETTEXTEXTENTPOINT32A"):
                call("iat-name", "address_name", {"address": f"{int(slot):#x}"})
                break
        report["completed"] = not any(row["is_error"] for row in report["queries"])
        if not report["completed"]:
            report["failure"] = "One or more MCP queries failed; inspect individual query files"
    except Exception as error:
        report["completed"] = False
        report["failure"] = str(error)
        print(f"FAILED {error}", flush=True)
    finally:
        if opened:
            try:
                _, failed = call("close", "close_binary", {}, 120)
                report["close_succeeded"] = not failed
            except Exception as error:
                report["close_succeeded"] = False
                report["close_error"] = str(error)
        report["server_exit_code"] = client.shutdown()
        save(output / "notifications.json", client.notifications)
        report["target_sha256_after"] = digest(target)
        report["target_unchanged"] = report["target_sha256_before"] == report["target_sha256_after"]
        save(output / "run.json", report)
    return 0 if report["completed"] and report.get("close_succeeded") and report["target_unchanged"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
