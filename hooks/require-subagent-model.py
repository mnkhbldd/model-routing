#!/usr/bin/env python3
"""PreToolUse hook on Agent: deny a subagent launch that would silently inherit the main model.

Allowed when the call passes `model`, the agent is a fork, or the agent's file
(project, user or plugin) pins a `model:` other than `inherit`. Any error fails open.
"""
import json
import os
import re
import sys
from pathlib import Path

HOME = Path.home() / ".claude"
PLUGIN_AGENTS = Path(__file__).resolve().parent.parent / "agents"
ALWAYS_ALLOWED = {"fork"}


def pinned_model(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    head = text.split("---", 2)[1] if text.startswith("---") else ""
    match = re.search(r"^model:\s*([^\s#]+)", head, re.MULTILINE)
    return bool(match) and match.group(1).strip("'\"") != "inherit"


def candidate_files(agent: str, cwd: str):
    if ":" in agent:
        _, name = agent.split(":", 1)
        yield PLUGIN_AGENTS / f"{name}.md"
        yield from (HOME / "plugins").glob(f"**/agents/{name}.md")
        return
    yield Path(cwd) / ".claude" / "agents" / f"{agent}.md"
    yield HOME / "agents" / f"{agent}.md"


def deny(agent: str) -> None:
    reason = (
        f"Subagent '{agent}' has no explicit model, so it would run on the expensive main model. "
        "Retry with model set to haiku (search, tests), sonnet (edits) or opus (risky review), "
        "or delegate to model-routing:code-searcher, model-routing:implementer, model-routing:test-runner or model-routing:reviewer."
    )
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))


def main() -> None:
    data = json.load(sys.stdin)
    if data.get("tool_name") not in ("Agent", "Task"):
        return
    tool_input = data.get("tool_input") or {}
    agent = tool_input.get("subagent_type") or "general-purpose"
    log = os.environ.get("ROUTING_HOOK_LOG")
    if log:
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps({"agent": agent, "model": tool_input.get("model")}) + "\n")
    if tool_input.get("model") or agent in ALWAYS_ALLOWED:
        return
    cwd = data.get("cwd") or os.getcwd()
    if any(p.is_file() and pinned_model(p) for p in candidate_files(agent, cwd)):
        return
    deny(agent)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
