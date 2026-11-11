# model-routing

A Claude Code plugin that sends each step of a task to the cheapest model that does it well, so your usage limits last longer.

| Step | Helper | Model |
| - | - | - |
| Find files, symbols, usages | `model-routing:code-searcher` | Haiku 5.5 |
| Edits across a few files | `model-routing:implementer` | Sonnet 5.5 |
| Run tests, lint, build | `model-routing:test-runner` | Haiku 5.5 |
| Review risky changes (auth, payments, migrations, data deletion, security, public API, concurrency) | `model-routing:reviewer` | Opus 5.5 |

Your main session plans the work and hands steps to these helpers. You don't name them yourself.

## What's inside

- `agents/`: the four helpers, each with a fixed model and effort level.
- `hooks/routing-rules.md`: the routing rules, loaded into every session at start.
- `hooks/require-subagent-model.py`: blocks any helper launch that names no model, so nothing quietly runs on your expensive main model. Claude reads the reason and retries with a model.

## Requirements

- Claude Code **2.1.293 or later** (`claude --version`). Older versions map `haiku` to Haiku 4.5, which costs about 10× more. Update with `claude update` or `brew upgrade claude-code`.
- `python3` on your PATH (macOS and Linux have it).

## Install

This repo is private, so you need access to it on GitHub and git signed in to GitHub on your machine (for example with `gh auth login`). Then run:

```bash
claude plugin marketplace add mnkhbldd/model-routing
```

```bash
claude plugin install model-routing@model-routing
```

Or, inside a Claude Code session: `/plugin marketplace add mnkhbldd/model-routing`, then `/plugin install model-routing@model-routing`.

Start a new session afterwards. The helpers and rules load at session start.

## Update

```bash
claude plugin marketplace update model-routing
```

```bash
claude plugin update model-routing@model-routing
```

## Daily use

1. **Pick Sonnet as the main model.** In the desktop app, choose Sonnet in the model picker for each new session. In the terminal, run `/model sonnet` once; it is saved as your default.
2. **One model per session.** Switching with `/model` mid-task makes the next request re-read the whole conversation without cache. For a hard design task, start a new session on Opus instead.
3. **Then just work.** You'll sometimes see a blocked helper call followed by a retry. That's the hook doing its job.

Each helper card in the app shows which model it ran on.

## Uninstall

```bash
claude plugin uninstall model-routing@model-routing
```
