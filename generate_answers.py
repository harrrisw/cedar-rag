"""Run the two prescribed answer prompts in separate, tool-disabled Codex sessions.

Requires an authenticated Codex CLI. This generates answers, not human audits.
Existing runs are never overwritten; a fresh uniquely named directory is created.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from uuid import uuid4

ROOT = Path(__file__).resolve().parent
DISABLED_FEATURES = (
    "shell_tool", "apps", "plugins", "remote_plugin", "multi_agent",
    "image_generation", "browser_use", "browser_use_external", "computer_use",
    "view_image", "sleep_tool", "code_mode_host", "in_app_chat", "in_app_browser",
    "skill_search", "memories",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--questions", nargs="+", choices=("q1", "q4"), default=["q1", "q4"])
    parser.add_argument("--instruction-file", type=Path,
                        help="Replacement instruction for a single-question correction; passages are unchanged.")
    args = parser.parse_args()
    if len(set(args.questions)) != len(args.questions):
        parser.error("Questions must be unique")
    if args.instruction_file and len(args.questions) != 1:
        parser.error("An instruction revision must target exactly one question")
    executable = shutil.which("codex")
    if not executable:
        raise SystemExit("Codex CLI was not found on PATH.")
    output = ROOT / "evidence" / ("answer-run-" + uuid4().hex[:12])
    output.mkdir(parents=True)
    version = subprocess.run([executable, "--version"], capture_output=True, text=True, check=True)
    manifest = {
        "cli_version": version.stdout.strip(),
        "purpose": "Fresh answer-generation conversations; no coding or audit delegation.",
        "input": "Only the handoff is passed on stdin; a requested correction replaces its instruction but retains the identical question and passages.",
        "instruction_revision": args.instruction_file.name if args.instruction_file else None,
        "disabled_features": list(DISABLED_FEATURES),
        "web_search": "disabled",
        "user_config": "ignored",
        "sandbox": "read-only",
        "project_doc_max_bytes": 0,
        "working_directory": "A separate empty OS temporary directory outside the project for each question.",
        "sessions": [],
        "human_audit": "Pending; machine event checks do not establish factual support.",
    }
    environment = os.environ.copy()
    for key in ("CODEX_THREAD_ID", "CODEX_TURN_ID"):
        environment.pop(key, None)
    for qid in args.questions:
        packet = (ROOT / "evidence" / f"answer-handoff-{qid}.txt").read_text(encoding="utf-8")
        if args.instruction_file:
            packet = args.instruction_file.read_text(encoding="utf-8").strip() + "\n\nQuestion: " + packet.split("\n\nQuestion: ", 1)[1]
        (output / f"input-{qid}.txt").write_text(packet, encoding="utf-8")
        scratch = Path(tempfile.gettempdir()) / ("cedar-answer-" + uuid4().hex)
        scratch.mkdir()
        command = [executable, "exec", "--ephemeral", "--ignore-user-config",
                   "--skip-git-repo-check", "--sandbox", "read-only", "-C", str(scratch),
                   "--config", 'web_search="disabled"',
                   "--config", "project_doc_max_bytes=0", "--json",
                   "--output-last-message", str(output / f"response-{qid}.md")]
        for feature in DISABLED_FEATURES:
            command.extend(["--disable", feature])
        command.append("-")
        print(f"Generating {qid.upper()} in a fresh empty directory...", flush=True)
        try:
            with (output / f"events-{qid}.jsonl").open("w", encoding="utf-8") as events, \
                 (output / f"stderr-{qid}.txt").open("w", encoding="utf-8") as errors:
                completed = subprocess.run(command, input=packet, text=True, encoding="utf-8",
                                           stdout=events, stderr=errors, env=environment)
        finally:
            # Only remove the empty directory created above; no recursive cleanup.
            try:
                scratch.rmdir()
            except OSError:
                pass
        if completed.returncode:
            raise SystemExit(f"{qid.upper()} failed; original logs retained in {output}")
        events = [json.loads(line) for line in (output / f"events-{qid}.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        items = [event["item"] for event in events if "item" in event]
        diagnostics = [item.get("message", "") for item in items if item.get("type") == "error"]
        allowed_diagnostic = "Code Mode is unavailable because code-mode host is disabled."
        unexpected = [item.get("type") for item in items
                      if item.get("type") not in ("agent_message", "reasoning")
                      and not (item.get("type") == "error" and item.get("message", "").startswith(allowed_diagnostic))]
        if unexpected:
            raise SystemExit(f"Unexpected tool/activity events {unexpected}; do not count this as an isolated answer run. Logs retained in {output}")
        thread_ids = [event["thread_id"] for event in events if event.get("type") == "thread.started"]
        if len(thread_ids) != 1:
            raise SystemExit(f"Could not verify a fresh thread for {qid}; logs retained in {output}")
        response = (output / f"response-{qid}.md").read_text(encoding="utf-8")
        if not response.strip():
            raise SystemExit(f"Empty response for {qid}; logs retained in {output}")
        if not any(event.get("type") == "turn.completed" for event in events):
            raise SystemExit(f"Turn did not complete for {qid}; logs retained in {output}")
        manifest["sessions"].append({"question": qid.upper(), "thread_id": thread_ids[0],
                                     "tool_events": 0, "input": f"input-{qid}.txt",
                                     "response": f"response-{qid}.md", "diagnostics": diagnostics})
        (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    if len({session["thread_id"] for session in manifest["sessions"]}) != len(args.questions):
        raise SystemExit("Answer sessions were not distinct.")
    print(f"Completed {len(args.questions)} fresh session(s) with zero tool events. Raw evidence: {output}")


if __name__ == "__main__":
    main()
