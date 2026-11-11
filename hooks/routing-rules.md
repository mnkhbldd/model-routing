# Model routing (model-routing plugin)
Main session = orchestrator. Delegate by task type; every Agent call names a routed agent or passes `model`.
- find files/symbols/usages → `model-routing:code-searcher` (haiku)
- scoped edit in a few files → `model-routing:implementer` (sonnet)
- run tests/lint/build → `model-routing:test-runner` (haiku)
- risky diff (auth, payments, migrations, data deletion, security, public API, concurrency) → `model-routing:reviewer` (opus)
- anything else → `general-purpose` with `model: "sonnet"`
Rules: unsure of tier → sonnet, never haiku for risky work. After implementer edits, run test-runner. Same check fails twice → reviewer with diff + failure, then implementer. Never `/model` mid-task; delegate instead (keeps prompt cache). Small one-file edits and quick reads: do inline, no agent. Exception: any change touching the risky list goes to reviewer before you call it done, however small.
