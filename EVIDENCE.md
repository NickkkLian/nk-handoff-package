# Evidence — nk-handoff-package, 2026-10-20

**TOOL on this benchmark.** The repair is measured against the original plain-prompt task, with fresh three-run Claude coverage.

| Arm | Original full passes | QA full passes | Original mean score | Codex judge | Claude judge | Agent seconds |
| --- | --- | --- | --- | --- | --- | --- |
| Repaired skill | 3/3 | 3/3 | 1.0000 | 0.9545 | 0.9848 / 1.0000 | 0.0 |
| Plain Codex | 3/3 | 3/3 | 1.0000 | 0.6667 | 0.6667 | 484.9 |
| Plain Claude | 3/3 | 3/3 | 1.0000 | 0.6818 | 0.6970 | 598.2 |

Claude judge skill means are shown separately for the Codex-pair and Claude-pair contexts.

| Comparison | Result |
| --- | --- |
| Codex judge vs plain Codex | WIN |
| Claude judge vs plain Codex | WIN |
| Codex judge vs plain Claude | WIN |
| Claude judge vs plain Claude | WIN |

| Native case | Codex judge: skill / plain Codex / plain Claude | Claude judge: skill / Codex | Claude judge: skill / Claude |
| --- | --- | --- | --- |
| handoff | 0.9545 / 0.6667 / 0.6818 | 0.9848 / 0.6667 | 1.0000 / 0.6970 |

The skill column repeats one repaired recorded artifact in three mechanical re-scorings; these are not three independent model generations. Handoff uses its original native 3/11 quality-delta requirement. A TOOL requires a clear win over both baselines under both applicable judges; a mechanical tie alone does not qualify. Native criteria and original scores remain unchanged. [Full measured records](evidence/cross-agent-2026-10-20.json) retain both judges and the mechanical summaries.

Plain Claude used the approved isolated config, original deny-owner-files sandbox, fresh temp projects with no copied skill, default claude-opus-5-5, 60 turns, USD 8 cap and 600-second timeout. The historical plain Codex arm used gpt-6.1-sol, high effort, and 3600 seconds. The difference in dates/caps, same-family judge relationships, task reuse, deterministic/recorded skill repeats and n=3 limit broader conclusions. The JSON below preserves the supplied comparison records, not a standalone rerunnable benchmark harness. The complete original task and judge receipts remain in the separate benchmark workspace; they are not bundled here. Local release checks and commands are in evidence/release-tests.txt and evidence/break-check.txt. No promotion, push or installed-skill update is implied.
